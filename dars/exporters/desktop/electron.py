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

            # 4) Backend: use user-provided backend/ if present; else generate defaults
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
                            shutil.copy2(src, os.path.join(base_out, fname))
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
                            # prefer a pinned electron version if missing or not exact
                            if not devd.get('electron') or devd.get('electron').startswith(('^','~','latest')):
                                devd['electron'] = '39.1.1'
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
                    "devDependencies": {"electron": "39.1.1", "electron-builder": "latest"},
                    "packageManager": "npm@10",
                    "description": app_desc,
                    "author": app_author,
                    "version": default_version,
                    "build": {"directories": {"output": "../"}, "electronVersion": "39.1.1", "appId": "com.dars.TBD", "productName": "TBD"}
                }
                import json
                pkg['name'] = pkg_name
                pkg['build']['appId'] = f"com.dars.{pkg_name}"
                pkg['build']['productName'] = app_title
                with open(os.path.join(base_out, 'package.json'), 'w', encoding='utf-8') as f:
                    json.dump(pkg, f, indent=2)

                main_js = (
                    "const { app, BrowserWindow, ipcMain, Menu } = require('electron');\n" \
                    "const path = require('path');\n" \
                    "const fs = require('fs').promises;\n" \
                    "let META = { title: '" + app_title.replace("'", "\\'") + "', packageName: '" + pkg_name + "' };\n" \
                    "try { META = Object.assign(META, require('./dars.meta.json')); } catch(e){}\n" \
                    "\n" \
                    "function createWindow() {\n" \
                    f"  const win = new BrowserWindow({{\n" \
                    "    width: 1000, height: 700,\n" \
                    "    title: META.title,\n" \
                    "    webPreferences: {\n" \
                    "      contextIsolation: true,\n" \
                    "      preload: path.join(__dirname, 'preload.js')\n" \
                    "    }\n" \
                    "  });\n" \
                    "  win.loadFile(path.join(__dirname, 'app', 'index.html'));\n" \
                    "}\n" \
                    "\n" \
                    "// Remove default application menu\n" \
                    "Menu.setApplicationMenu(null);\n" \
                    "try { app.setName(META.packageName || META.title || 'dars-app'); } catch(e){}\n" \
                    "\n" \
                    "// Basic IPC wiring (Phase 3)\n" \
                    "ipcMain.handle('dars::FileSystem::read_text', async (_e, filePath, encoding='utf-8') => {\n" \
                    "  if (!filePath || typeof filePath !== 'string') throw new Error('filePath must be a string');\n" \
                    "  const content = await fs.readFile(filePath, { encoding });\n" \
                    "  return content;\n" \
                    "});\n" \
                    "ipcMain.handle('dars::FileSystem::write_text', async (_e, filePath, data, encoding='utf-8') => {\n" \
                    "  if (!filePath || typeof filePath !== 'string') throw new Error('filePath must be a string');\n" \
                    "  if (typeof data !== 'string') data = String(data ?? '');\n" \
                    "  await fs.writeFile(filePath, data, { encoding });\n" \
                    "  return true;\n" \
                    "});\n" \
                    "\n" \
                    "app.whenReady().then(() => {\n" \
                    "  createWindow();\n" \
                    "  app.on('activate', function () {\n" \
                    "    if (BrowserWindow.getAllWindows().length === 0) createWindow();\n" \
                    "  });\n" \
                    "});\n" \
                    "\n" \
                    "app.on('window-all-closed', function () {\n" \
                    "  if (process.platform !== 'darwin') app.quit();\n" \
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
