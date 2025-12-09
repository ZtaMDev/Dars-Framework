# Dars Framework - Core Source File
#
# This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0.
# If a copy of the MPL was not distributed with this file, You can obtain one at
# https://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2025 ZtaDev
from typing import Optional
import os

from dars.core.app import App
from dars.core.component import Component
from dars.exporters.base import Exporter
from dars.exporters.web.html_css_js import HTMLCSSJSExporter
from dars.desktop.api import get_schema
from dars.desktop.js_generator import generate_preload_js, generate_stub_js
import shutil

class ElectronExporter(Exporter):
    """Electron exporter (Phase 3)
    Generates web app (under app/), desktop bridge files (preload.js, stub.js),
    and minimal Electron backend (package.json, main.js).
    """

    def get_platform(self) -> str:
        return "desktop"

    def export(self, app: 'App', output_path: str, bundle: bool = False) -> bool:
        try:
            self.create_output_directory(output_path)
            # 1) Generate web frontend into app/
            base_out = os.path.join(output_path, 'source-electron') if bundle else output_path
            os.makedirs(base_out, exist_ok=True)
            web_out = os.path.join(base_out, 'app')
            os.makedirs(web_out, exist_ok=True)
            web_exporter = HTMLCSSJSExporter()
            if not web_exporter.export(app, web_out, bundle=bundle):
                return False

            # 2) Generate bridge files from schema
            schema = get_schema()
            preload_js = generate_preload_js(schema)
            stub_js = generate_stub_js(schema)
            # write preload.js at root
            with open(os.path.join(base_out, 'preload.js'), 'w', encoding='utf-8') as f:
                f.write(preload_js)
            # write stub.js inside app assets
            lib_dir = os.path.join(web_out, 'lib')
            os.makedirs(lib_dir, exist_ok=True)
            stub_path = os.path.join(lib_dir, 'dars_desktop_stub.js')
            with open(stub_path, 'w', encoding='utf-8') as f:
                f.write(stub_js)

            # 3) Inject desktop stub into index.html
            try:
                index_path = os.path.join(web_out, 'index.html')
                with open(index_path, 'r', encoding='utf-8') as f:
                    html = f.read()
                tag = "\n<script type=\"module\" src=\"lib/dars_desktop_stub.js\"></script>\n"
                if '</body>' in html:
                    html = html.replace('</body>', f"{tag}</body>")
                    html = html + tag
                with open(index_path, 'w', encoding='utf-8') as f:
                    f.write(html)
            except Exception:
                # Non-fatal: continue even if injection fails
                pass

            # 4) Handle desktop icon from app.icon property
            app_icon = getattr(app, 'icon', '') or ''
            icon_path = None
            if app_icon:
                # Resolve icon path (relative to project root or absolute)
                project_root = os.getcwd()
                if os.path.isabs(app_icon):
                    icon_path = app_icon
                else:
                    icon_path = os.path.join(project_root, app_icon)
                # Check if icon exists
                if not os.path.isfile(icon_path):
                    # Try in icons/ directory
                    alt_path = os.path.join(project_root, 'icons', os.path.basename(app_icon))
                    if os.path.isfile(alt_path):
                        icon_path = alt_path
                    else:
                        # Try default icon.png in icons/
                        default_icon = os.path.join(project_root, 'icons', 'icon.png')
                        if os.path.isfile(default_icon):
                            icon_path = default_icon
                        else:
                            icon_path = None
            else:
                # Try default icon.png in icons/
                default_icon = os.path.join(os.getcwd(), 'icons', 'icon.png')
                if os.path.isfile(default_icon):
                    icon_path = default_icon
            
            # Copy icon to build directory if found
            build_icon_dir = os.path.join(base_out, 'build', 'icons')
            build_icon_path = None
            root_icon_path = None
            if icon_path and os.path.isfile(icon_path):
                try:
                    os.makedirs(build_icon_dir, exist_ok=True)
                    # Copy icon with appropriate name for electron-builder
                    icon_ext = os.path.splitext(icon_path)[1].lower()
                    if icon_ext in ['.png', '.ico', '.icns']:
                        # electron-builder expects icon.png, icon.ico, or icon.icns
                        build_icon_name = f'icon{icon_ext}'
                        build_icon_path = os.path.join(build_icon_dir, build_icon_name)
                        shutil.copy2(icon_path, build_icon_path)
                        # Also copy to root of base_out for electron-builder to find
                        root_icon_path = os.path.join(base_out, build_icon_name)
                        shutil.copy2(icon_path, root_icon_path)
                except Exception:
                    build_icon_path = None
                    root_icon_path = None

            # 5) Backend: use user-provided backend/ if present; else generate defaults
            backend_dir = os.path.join(os.getcwd(), 'backend')
            # Compute metadata from App
            app_title = getattr(app, 'title', 'Dars App') or 'Dars App'
            app_desc = getattr(app, 'description', '') or 'Built with Dars'
            app_author = getattr(app, 'author', '') or 'Unknown'
            app_version = getattr(app, 'version', '') or ''
            default_version = app_version if app_version else '0.1.0'
            def _slugify(s: str) -> str:
                import re
                slug = re.sub(r"[^a-z0-9]+", "-", (s or '').lower())
                slug = re.sub(r"-+", "-", slug).strip('-')
                return slug or 'dars-app'
            pkg_name = _slugify(app_title)
            # Write meta file for backend to consume
            try:
                import json
                meta_path = os.path.join(base_out, 'dars.meta.json')
                with open(meta_path, 'w', encoding='utf-8') as mf:
                    json.dump({"title": app_title, "packageName": pkg_name}, mf, indent=2)
            except Exception:
                pass
            try:
                if os.path.isdir(backend_dir):
                    # Copy user backend files
                    for fname in ('package.json', 'main.js', 'preload.js'):
                        src = os.path.join(backend_dir, fname)
                        if os.path.isfile(src):
                            dest = os.path.join(base_out, fname)
                            shutil.copy2(src, dest)
                            # If it's main.js and we have an icon, inject icon configuration
                            if fname == 'main.js' and root_icon_path and os.path.isfile(root_icon_path):
                                try:
                                    with open(dest, 'r', encoding='utf-8') as f:
                                        main_content = f.read()
                                    # Check if icon is already configured
                                    if 'icon:' not in main_content:
                                        icon_rel = os.path.basename(root_icon_path)
                                        # Try to inject icon in BrowserWindow options
                                        # Look for BrowserWindow({ pattern
                                        import re
                                        pattern = r'(new BrowserWindow\s*\(\s*\{)'
                                        replacement = f'\\1\n    icon: path.join(__dirname, {repr(icon_rel)}),'
                                        new_content = re.sub(pattern, replacement, main_content, count=1)
                                        if new_content != main_content:
                                            with open(dest, 'w', encoding='utf-8') as f:
                                                f.write(new_content)
                                except Exception:
                                    # If injection fails, continue with original file
                                    pass
                    # Override package.json name and ensure build fields
                    try:
                        import json
                        pkg_path = os.path.join(base_out, 'package.json')
                        if os.path.isfile(pkg_path):
                            with open(pkg_path, 'r', encoding='utf-8') as pf:
                                data = json.load(pf)
                            data['name'] = pkg_name
                            # basic metadata
                            if not data.get('description') and app_desc:
                                data['description'] = app_desc
                            if not data.get('author') and app_author:
                                data['author'] = app_author
                            # version (required by electron-builder)
                            if not data.get('version'):
                                data['version'] = default_version
                            # devDeps: ensure electron-builder present
                            devd = data.get('devDependencies') or {}
                            devd.setdefault('electron-builder', 'latest')
                            # prefer a pinned, security-reviewed Electron version if missing or not exact
                            if not devd.get('electron') or devd.get('electron').startswith(('^','~','latest')):
                                devd['electron'] = '39.2.6'
                            data['devDependencies'] = devd
                            # Force npm to avoid bun ENOENT inside electron-builder
                            if not data.get('packageManager'):
                                data['packageManager'] = 'npm@10'
                            # build fields
                            b = data.get('build') or {}
                            # Ensure explicit electronVersion for electron-builder
                            b.setdefault('electronVersion', '39.1.1')
                            dirs = b.get('directories') or {}
                            dirs['output'] = '../'
                            b['directories'] = dirs
                            b.setdefault('appId', f"com.dars.{pkg_name}")
                            b.setdefault('productName', app_title)
                            
                            # Configure icon if available (use root_icon_path for electron-builder)
                            if root_icon_path and os.path.isfile(root_icon_path):
                                icon_ext = os.path.splitext(root_icon_path)[1].lower()
                                # Use relative path from base_out for electron-builder
                                icon_rel_path = os.path.basename(root_icon_path)
                                if icon_ext == '.png':
                                    b['icon'] = icon_rel_path
                                elif icon_ext == '.ico':
                                    b['icon'] = icon_rel_path
                                    # Also set win.icon
                                    if 'win' not in b:
                                        b['win'] = {}
                                    b['win']['icon'] = icon_rel_path
                                elif icon_ext == '.icns':
                                    b['icon'] = icon_rel_path
                                    # Also set mac.icon
                                    if 'mac' not in b:
                                        b['mac'] = {}
                                    b['mac']['icon'] = icon_rel_path
                            
                            # Configure to generate direct executables (not installers)
                            # Windows: generate dir (unpacked) instead of installer
                            if 'win' not in b:
                                b['win'] = {}
                            # Use "dir" as string target for unpacked directory
                            b['win']['target'] = "dir"
                            
                            # Linux: generate dir (unpacked directory)
                            if 'linux' not in b:
                                b['linux'] = {}
                            b['linux']['target'] = "dir"
                            
                            # macOS: generate dir (unpacked directory)
                            if 'mac' not in b:
                                b['mac'] = {}
                            b['mac']['target'] = "dir"
                            
                            # Ensure files are included correctly
                            # Don't override if user already has files configured
                            if 'files' not in b:
                                b['files'] = [
                                    "app/**/*",
                                    "main.js",
                                    "preload.js",
                                    "package.json",
                                    "dars.meta.json",
                                    "!**/node_modules/**",
                                    "!**/.git/**"
                                ]
                            # Ensure extraFiles includes icon if available
                            if root_icon_path and os.path.isfile(root_icon_path):
                                if 'extraFiles' not in b:
                                    b['extraFiles'] = []
                                icon_name = os.path.basename(root_icon_path)
                                if icon_name not in [f.get('from', '') for f in b.get('extraFiles', [])]:
                                    b['extraFiles'].append({"from": icon_name, "to": "."})
                            
                            data['build'] = b
                            with open(pkg_path, 'w', encoding='utf-8') as pf:
                                json.dump(data, pf, indent=2)
                    except Exception:
                        pass
                else:
                    raise FileNotFoundError('No backend dir')
            except Exception:
                # Fallback: generate defaults
                pkg = {
                    "name": "dars-electron-app",
                    "private": True,
                    # Use CommonJS for Electron main process
                    "main": "main.js",
                    "scripts": {"start": "electron ."},
                    "devDependencies": {"electron": "39.2.6", "electron-builder": "latest"},
                    "packageManager": "npm@10",
                    "description": app_desc,
                    "author": app_author,
                    "version": default_version,
                    "build": {
                        "directories": {"output": "../"},
                        "electronVersion": "39.2.6",
                        "appId": "com.dars.TBD",
                        "productName": "TBD",
                        "files": [
                            "app/**/*",
                            "main.js",
                            "preload.js",
                            "package.json",
                            "dars.meta.json",
                            "!**/node_modules/**",
                            "!**/.git/**"
                        ],
                        "win": {"target": "dir"},
                        "linux": {"target": "dir"},
                        "mac": {"target": "dir"}
                    }
                }
                import json
                pkg['name'] = pkg_name
                pkg['build']['appId'] = f"com.dars.{pkg_name}"
                pkg['build']['productName'] = app_title
                
                # Configure icon if available (use root_icon_path for electron-builder)
                if root_icon_path and os.path.isfile(root_icon_path):
                    icon_ext = os.path.splitext(root_icon_path)[1].lower()
                    # Use relative path from base_out for electron-builder
                    icon_rel_path = os.path.basename(root_icon_path)
                    if icon_ext == '.png':
                        pkg['build']['icon'] = icon_rel_path
                    elif icon_ext == '.ico':
                        pkg['build']['icon'] = icon_rel_path
                        pkg['build']['win']['icon'] = icon_rel_path
                    elif icon_ext == '.icns':
                        pkg['build']['icon'] = icon_rel_path
                        pkg['build']['mac']['icon'] = icon_rel_path
                
                with open(os.path.join(base_out, 'package.json'), 'w', encoding='utf-8') as f:
                    json.dump(pkg, f, indent=2)

                # Prepare icon path for main.js
                icon_js_code = ""
                if root_icon_path and os.path.isfile(root_icon_path):
                    # Use relative path from base_out for main.js
                    icon_rel = os.path.basename(root_icon_path)
                    icon_js_code = f"    icon: path.join(__dirname, {repr(icon_rel)}),\n"

                main_js = (
                        "const { app, BrowserWindow, Menu, ipcMain } = require('electron');\n"
                        "const path = require('path');\n"
                        "const fs = require('fs').promises;\n"
                        "const http = require('http');\n"
                        "\n"
                        "function createWindow() {\n"
                        f"  const win = new BrowserWindow({{\n"
                        "    width: 1000, height: 700,\n"
                        + icon_js_code +
                        "    webPreferences: {\n"
                        "      contextIsolation: true,\n"
                        "      preload: path.join(__dirname, 'preload.js')\n"
                        "    }\n"
                        "  });\n"
                        "  Menu.setApplicationMenu(null);\n"
                        "  win.loadFile(path.join(__dirname, 'app', 'index.html'));\n"
                        "  // Open DevTools in development mode if enabled\n"
                        "  if (process.env.DARS_DEV === '1' && process.env.DARS_DEVTOOLS !== '0') {\n"
                        "    win.webContents.openDevTools();\n"
                        "  }\n"
                        "}\n"
                        "\n"
                        "app.whenReady().then(() => {\n"
                        "  createWindow();\n"
                        "  app.on('activate', function () {\n"
                        "    if (BrowserWindow.getAllWindows().length === 0) createWindow();\n"
                        "  });\n"
                        "});\n"
                        "\n"
                        "// Utility to resolve paths: absolute paths are used as-is; relative paths resolve against process.cwd()\n"
                        "function resolvePath(p) {\n"
                        "  if (!p || typeof p !== 'string') throw new Error('filePath must be a string');\n"
                        "  if (path.isAbsolute(p)) return p;\n"
                        "  return path.resolve(process.cwd(), p);\n"
                        "}\n"
                        "\n"
                        "function closeAllAndExit() {\n"
                        "  try {\n"
                        "    const wins = BrowserWindow.getAllWindows();\n"
                        "    wins.forEach(w => { try { w.close(); } catch(e) {} });\n"
                        "  } catch (e) {}\n"
                        "  setTimeout(() => { try { app.quit(); } catch(e) {} }, 300);\n"
                        "}\n"
                        "\n"
                        "ipcMain.handle('dars::dev::shutdown', async () => {\n"
                        "  closeAllAndExit();\n"
                        "  return true;\n"
                        "});\n"
                        "\n"
                        "const controlPort = process.env.DARS_CONTROL_PORT;\n"
                        "if (controlPort) {\n"
                        "  try {\n"
                        "    const server = http.createServer((req, res) => {\n"
                        "      if (req.method === 'POST' && req.url === '/__dars_shutdown') {\n"
                        "        closeAllAndExit();\n"
                        "        res.writeHead(200); res.end('ok');\n"
                        "        return;\n"
                        "      }\n"
                        "      res.writeHead(404); res.end('not-found');\n"
                        "    });\n"
                        "    server.listen(Number(controlPort), '127.0.0.1');\n"
                        "  } catch (e) { /* ignore */ }\n"
                        "}\n"
                        "\n"
                        "// IPC handlers for Dars desktop API\n"
                        "ipcMain.handle('dars::FileSystem::read_text', async (_e, filePath, encoding = 'utf-8') => {\n"
                        "  const resolved = resolvePath(filePath);\n"
                        "  const content = await fs.readFile(resolved, { encoding });\n"
                        "  return content;\n"
                        "});\n"
                        "\n"
                        "ipcMain.handle('dars::FileSystem::write_text', async (_e, filePath, data, encoding = 'utf-8') => {\n"
                        "  const resolved = resolvePath(filePath);\n"
                        "  if (typeof data !== 'string') data = String(data ?? '');\n"
                        "  await fs.mkdir(path.dirname(resolved), { recursive: true });\n"
                        "  await fs.writeFile(resolved, data, { encoding });\n"
                        "  return true;\n"
                        "});\n"
                        "\n"
                        "ipcMain.handle('dars::FileSystem::read_file', async (_e, filePath) => {\n"
                        "  const resolved = resolvePath(filePath);\n"
                        "  try {\n"
                        "    const data = await fs.readFile(resolved);\n"
                        "    // Convert to array for JSON serialization\n"
                        "    return { data: Array.from(data) };\n"
                        "  } catch (error) {\n"
                        "    console.error('Error reading file:', error);\n"
                        "    throw error;\n"
                        "  }\n"
                        "});\n"
                        "\n"
                        "ipcMain.handle('dars::FileSystem::write_file', async (_e, filePath, data) => {\n"
                        "  const resolved = resolvePath(filePath);\n"
                        "  try {\n"
                        "    await fs.mkdir(path.dirname(resolved), { recursive: true });\n"
                        "    await fs.writeFile(resolved, Buffer.from(data));\n"
                        "    return true;\n"
                        "  } catch (error) {\n"
                        "    console.error('Error writing file:', error);\n"
                        "    throw error;\n"
                        "  }\n"
                        "});\n"
                        "\n"
                        "ipcMain.handle('dars::FileSystem::list_directory', async (_e, dirPath, pattern = '*', includeSize = false) => {\n"
                        "  const resolved = resolvePath(dirPath);\n"
                        "  try {\n"
                        "    const entries = await fs.readdir(resolved, { withFileTypes: true });\n"
                        "    const result = [];\n"
                        "    for (const entry of entries) {\n"
                        "      // Simple pattern matching (supports * wildcard)\n"
                        "      if (pattern !== '*') {\n"
                        "        const regex = new RegExp('^' + pattern.replace(/\\*/g, '.*') + '$');\n"
                        "        if (!regex.test(entry.name)) continue;\n"
                        "      }\n"
                        "      const obj = {\n"
                        "        name: entry.name,\n"
                        "        isDirectory: entry.isDirectory()\n"
                        "      };\n"
                        "      if (includeSize) {\n"
                        "        const stats = await fs.stat(path.join(resolved, entry.name));\n"
                        "        obj.size = stats.size;\n"
                        "      }\n"
                        "      result.push(obj);\n"
                        "    }\n"
                        "    return result;\n"
                        "  } catch (error) {\n"
                        "    console.error('Error listing directory:', error);\n"
                        "    throw error;\n"
                        "  }\n"
                        "});\n"
                        "\n"
                        "app.on('window-all-closed', function () {\n"
                        "  if (process.platform !== 'darwin') app.quit();\n"
                        "});\n"
                )
                with open(os.path.join(base_out, 'main.js'), 'w', encoding='utf-8') as f:
                    f.write(main_js)

            return True
        except Exception:
            return False

    # Not used directly here
    def render_component(self, component: 'Component') -> str:
        return ""