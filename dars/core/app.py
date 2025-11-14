from typing import Optional, List, Dict, Any

from dars.exporters.base import Exporter
from dars.scripts.script import Script
from .component import Component
from .events import EventManager
import os, shutil, sys, platform
class Page:
    """Represents an individual page in the Dars app (multipage)."""
    def __init__(self, name: str, root: 'Component', title: str = None, meta: dict = None, index: bool = False, scripts: Optional[List[Any]] = None):
        self.name = name  # slug o nombre de la página
        self.root = root  # componente raíz de la página
        self.title = title
        self.meta = meta or {}
        self.index = index  # ¿Es la página principal?
        self.scripts: List[Any] = list(scripts) if scripts else []

    def attr(self, **attrs):
        """Setter/getter for Page attributes, similar to Component.attr().  
        If kwargs are provided, sets attributes; otherwise, returns a dict with the editable attributes."""  

        if attrs:
            for key, value in attrs.items():
                if hasattr(self, key):
                    setattr(self, key, value)
                else:
                    self.meta[key] = value
            return self
        # Getter
        d = dict(self.meta)
        d['name'] = self.name
        d['root'] = self.root
        d['title'] = self.title
        d['index'] = self.index
        d['scripts'] = list(self.scripts)
        return d
    # -----------------------------
    # Métodos para manejar scripts
    # -----------------------------
    def add_script(self, script: Any):
        """Adds a script to this page.  
        - If 'script' is an instance (e.g., InlineScript/FileScript/DScript), it is added as is.  
        - If 'script' is a string, it is interpreted as an InlineScript (code).  
        - If 'script' is a dict, it is added as is (fallback).  
        Returns self to allow call chaining."""  

        # si es str => interpretarlo como inline
        if isinstance(script, str):
            created = self._make_inline_script(script)
            self.scripts.append(created)
            return self

        # si es dict => fallback, guardarlo
        if isinstance(script, dict):
            self.scripts.append(script)
            return self

        # si ya es una instancia de "Script" (no podemos verificar tipo concreto sin dependencia),
        # asumimos que es un script válido y lo añadimos.
        self.scripts.append(script)
        return self

    # alias corto (pedido)
    def addscript(self, script: Any):
        return self.add_script(script)

    def add_inline_script(self, code: str, **kwargs):
        """Convenience: adds an InlineScript to the page (code = JS or similar)."""
        s = self._make_inline_script(code, **kwargs)
        self.scripts.append(s)
        return self

    def add_file_script(self, path: str, **kwargs):
        """Convenience: adds a FileScript (reference to a .js/.ts/etc. file)."""
        s = self._make_file_script(path, **kwargs)
        self.scripts.append(s)
        return self

    def add_dscript(self, obj: Any, **kwargs):
        """Convenience: attempts to create/add a DScript (if the class exists)."""
        s = self._make_dscript(obj, **kwargs)
        self.scripts.append(s)
        return self

    def get_scripts(self) -> List[Any]:
        """Returns the list of scripts added to the page."""
        return list(self.scripts)

    # -----------------------------
    # Helpers para construcción segura
    # -----------------------------
    def _make_inline_script(self, code: str, **kwargs) -> Any:
        """Attempts to create an InlineScript instance if it exists in dars.scripts.*.  
            Otherwise, returns a fallback dict: {'type': 'inline', 'code': ..., **kwargs}"""

        try:
            # intentamos import común (ajusta según tu layout de módulos si hace falta)
            from dars.scripts.script import InlineScript  # type: ignore
            return InlineScript(code, **kwargs)
        except Exception:
            try:
                from dars.scripts.script import InlineScript  # type: ignore
                return InlineScript(code, **kwargs)
            except Exception:
                # fallback: dict simple que contiene lo mínimo
                return {'type': 'inline', 'code': code, **kwargs}

    def _make_file_script(self, path: str, **kwargs) -> Any:
        """Attempts to create a FileScript instance if it exists. Otherwise, returns a fallback dict."""

        try:
            from dars.scripts.script import FileScript  # type: ignore
            return FileScript(path, **kwargs)
        except Exception:
            try:
                from dars.scripts.script import FileScript  # type: ignore
                return FileScript(path, **kwargs)
            except Exception:
                return {'type': 'file', 'path': path, **kwargs}

    def _make_dscript(self, obj: Any, **kwargs) -> Any:
        """Attempts to create a DScript instance if it exists. Otherwise, stores the object with a marker."""
        try:
            from dars.scripts.dscript import dScript  # type: ignore
            return dScript(obj, **kwargs)
        except Exception:
            # si ya es dict o similar, solo anotamos el tipo
            return {'type': 'dscript', 'value': obj, **kwargs}

class App:
    """Main class that represents a Dars application"""

    def rTimeCompile(self, exporter=None, port=None, add_file_types=".py, .js, .css", watchfiledialog=False):
        """
        Optimized Real-Time Compile with fast Ctrl+C exit
        Shows a colored spinner ("Exiting server...") when user presses Ctrl+C.
        Supports both web and desktop modes with configuration respect.
        """

        import threading
        import time
        import sys
        import os
        import inspect
        import importlib.util
        import signal
        import subprocess
        from pathlib import Path
        from contextlib import contextmanager
        import shutil
        import traceback

        self.watchfiledialog = watchfiledialog

        @contextmanager
        def pushd(path):
            old = os.getcwd()
            os.chdir(path)
            try:
                yield
            finally:
                os.chdir(old)
        try:
            from dars.cli.main import console as global_console
        except Exception:
            global_console = None

        # Importar componentes de Rich
        try:
            from rich.panel import Panel
            from rich.text import Text
            from rich.live import Live
            from rich.spinner import Spinner
            from rich.align import Align
            from rich.table import Table
        except Exception:
            Panel = Text = Live = Spinner = Align = Table = None

        # Si no existe una consola global, creamos una local segura
        if global_console:
            console = global_console
        else:
            try:
                from rich.console import Console as _Console
                console = _Console()
            except Exception:
                console = None

        # ---- PORT ----
        if port is None:
            port = 8000
            for i, arg in enumerate(sys.argv):
                if arg in ('--port', '-p') and i + 1 < len(sys.argv):
                    try:
                        port = int(sys.argv[i + 1])
                    except:
                        pass

        # ---- NORMALIZE EXTENSIONS ----
        def _normalize_exts(exts):
            if not exts:
                return ['.py']
            if isinstance(exts, str):
                parts = [p.strip() for p in exts.split(',') if p.strip()]
            elif isinstance(exts, (list, tuple, set)):
                parts = [str(p).strip() for p in exts if p]
            else:
                parts = [str(exts).strip()]

            normalized = []
            for p in parts:
                if not p:
                    continue
                if not p.startswith('.'):
                    p = '.' + p
                normalized.append(p.lower())

            if '.py' not in normalized:
                normalized.insert(0, '.py')

            seen, result = set(), []
            for e in normalized:
                if e not in seen:
                    seen.add(e)
                    result.append(e)
            return result

        watch_exts = _normalize_exts(add_file_types)

        # ---- EXPORTER ----
        if exporter is None:
            try:
                from dars.exporters.web.html_css_js import HTMLCSSJSExporter
            except ImportError:
                if console:
                    console.print("[red]Could not import HTMLCSSJSExporter[/red]")
                else:
                    print("Could not import HTMLCSSJSExporter")
                return
            exporter = HTMLCSSJSExporter()

        # ---- PREVIEW SERVER ----
        try:
            from dars.cli.preview import PreviewServer
        except Exception:
            PreviewServer = None

        shutdown_event = threading.Event()
        cleanup_done_event = threading.Event()
        watchers = []
        directory_watchers = []

        reload_lock = threading.Lock()
        last_reload_at = 0.0
        MIN_RELOAD_INTERVAL = 0.4

        # ---- IMPROVED Ctrl+C HANDLER ----
        shutting_down = False
        spinner_thread = None
        initialization_complete = threading.Event()

        def fast_exit_handler(sig, frame):
            nonlocal shutting_down, spinner_thread
            if shutting_down:
                return
            shutting_down = True
            shutdown_event.set()

            if console:
                def _spinner():
                    try:
                        # Wait for initialization to complete if we're still starting up
                        if not initialization_complete.is_set():
                            with console.status("[bold yellow] Waiting for initialization to complete...[/bold yellow]", spinner="dots"):
                                initialization_complete.wait(timeout=5.0)
                        
                        with console.status("[bold magenta] Exiting server...[/bold magenta]", spinner="dots"):
                            cleanup_done_event.wait(timeout=3.0)
                    except Exception:
                        pass

                spinner_thread = threading.Thread(target=_spinner, daemon=True)
                spinner_thread.start()
            else:
                print("Exiting...")

        try:
            signal.signal(signal.SIGINT, fast_exit_handler)
        except Exception:
            pass

        # ---- DETECT APP FILE AND PROJECT ROOT ----
        app_file = None
        for frame in inspect.stack():
            if frame.function == "<module>":
                app_file = frame.filename
                break
        if not app_file:
            app_file = sys.argv[0]

        project_root = os.path.dirname(os.path.abspath(app_file))
        if project_root not in sys.path:
            sys.path.insert(0, project_root)

        cwd_original = os.getcwd()

        # ---- PREVIEW DIR ----
        preview_dir = os.path.join(project_root, "dars_preview")
        try:
            shutil.rmtree(preview_dir, ignore_errors=True)
        except:
            pass
        os.makedirs(preview_dir, exist_ok=True)

        # ---- LOAD CONFIG AND DETECT MODE ----
        try:
            from dars.config import load_config
            cfg, cfg_found = load_config(project_root)
        except Exception:
            cfg, cfg_found = ({}, False)

        if not cfg_found:
            warn_msg = "[Dars] Warning: dars.config.json not found. Run 'dars init --update' to create it in existing projects."
            if console:
                console.print(f"[yellow]{warn_msg}[/yellow]")
            else:
                print(warn_msg)

        # Detect desktop mode from config or attribute
        fmt = str(cfg.get('format', '')).lower() if cfg else ''
        is_desktop = bool(getattr(self, 'desktop', False) or fmt == 'desktop')

        # ---- ENHANCED FILE WATCHING SYSTEM ----
        class EnhancedFileWatcher:
            """Watches a file for changes and triggers a callback when it changes."""
            def __init__(self, path, on_change, poll_interval=0.5):
                self.path = path
                self.on_change = on_change
                self.poll_interval = poll_interval
                self._last_mtime = None
                self._stop_event = threading.Event()
                self._thread = threading.Thread(target=self._watch, daemon=True)

            def start(self):
                try:
                    self._last_mtime = os.path.getmtime(self.path)
                except OSError:
                    # File might not exist yet, we'll check in the watch loop
                    self._last_mtime = None
                self._thread.start()

            def stop(self):
                self._stop_event.set()
                self._thread.join(timeout=1.0)

            def _watch(self):
                while not self._stop_event.is_set():
                    try:
                        if os.path.exists(self.path):
                            mtime = os.path.getmtime(self.path)
                            if mtime != self._last_mtime:
                                self._last_mtime = mtime
                                self.on_change()
                        else:
                            # File was deleted, reset last_mtime so we detect when it's recreated
                            if self._last_mtime is not None:
                                self._last_mtime = None
                    except Exception:
                        pass
                    time.sleep(self.poll_interval)

        class DirectoryWatcher:
            """Watches a directory for file changes and new files."""
            def __init__(self, directory, extensions, on_change, poll_interval=2.0):
                self.directory = directory
                self.extensions = extensions
                self.on_change = on_change
                self.poll_interval = poll_interval
                self._stop_event = threading.Event()
                self._thread = threading.Thread(target=self._watch, daemon=True)
                self._known_files = self._get_current_files()

            def start(self):
                self._thread.start()

            def stop(self):
                self._stop_event.set()
                self._thread.join(timeout=1.0)

            def _get_current_files(self):
                """Get current files matching extensions in directory."""
                files = set()
                try:
                    for ext in self.extensions:
                        for file_path in Path(self.directory).rglob(f"*{ext}"):
                            if self._should_watch_file(file_path):
                                files.add(str(file_path))
                except Exception:
                    pass
                return files

            def _should_watch_file(self, file_path):
                """Check if file should be watched based on exclusion rules."""
                skip_dirs = {"__pycache__", ".git", "dars_preview", ".pytest_cache", "venv", "env", "node_modules"}
                file_str = str(file_path)
                return not any(skip_dir in file_str for skip_dir in skip_dirs)

            def _watch(self):
                while not self._stop_event.is_set():
                    try:
                        current_files = self._get_current_files()
                        
                        # Check for new files
                        new_files = current_files - self._known_files
                        if new_files:
                            if len(new_files) == 1:
                                file = next(iter(new_files))
                                self.on_change(f"New file created: {os.path.relpath(file, self.directory)}")
                            else:
                                self.on_change(f"New files detected: {len(new_files)} files")
                            self._known_files = current_files
                        
                        # Check for deleted files (optional, but good for tracking)
                        deleted_files = self._known_files - current_files
                        if deleted_files:
                            self._known_files = current_files
                            
                    except Exception as e:
                        # Log error but continue watching
                        pass
                        
                    time.sleep(self.poll_interval)

        def _collect_project_files_by_ext(root, exts):
            """Collect files with given extensions, excluding certain directories."""
            files = []
            skip_dirs = {"__pycache__", ".git", "dars_preview", ".pytest_cache", "venv", "env", "node_modules"}
            
            try:
                for dirpath, dirnames, filenames in os.walk(root):
                    # Remove skipped directories from dirnames to prevent walking into them
                    dirnames[:] = [d for d in dirnames if d not in skip_dirs]
                    
                    for fname in filenames:
                        file_path = os.path.join(dirpath, fname)
                        file_ext = os.path.splitext(fname)[1].lower()
                        
                        if file_ext in exts:
                            files.append(file_path)
            except Exception as e:
                # If there's any error walking the directory, at least return the main app file
                if console:
                    console.print(f"[yellow]Warning: Error scanning directory {root}: {e}[/yellow]")
            
            return files

        # Función mejorada para manejar cambios
        def handle_file_change(change_description=None):
            nonlocal last_reload_at, files_to_watch
            now = time.time()
            if now - last_reload_at < MIN_RELOAD_INTERVAL:
                return
            with reload_lock:
                last_reload_at = time.time()
                
                if change_description:
                    change_msg = change_description
                else:
                    change_msg = "File change detected"
                    
                if console:
                    console.print(f"[yellow]{change_msg}. Reloading...[/yellow]")
                else:
                    print(f"[Dars] {change_msg}. Reloading...")

                try:
                    # Actualizar la lista de archivos vigilados si es necesario
                    current_files = _collect_project_files_by_ext(project_root, watch_exts)
                    if len(current_files) != len(files_to_watch):
                        files_to_watch.clear()
                        files_to_watch.extend(current_files)
                        if console:
                            console.print(f"[cyan]Updated file watch list: {len(files_to_watch)} files[/cyan]")
                    
                    if project_root not in sys.path:
                        sys.path.insert(0, project_root)
                    with pushd(project_root):
                        to_remove = []
                        root_abs = os.path.abspath(project_root)
                        for name, mod in list(sys.modules.items()):
                            mod_file = getattr(mod, '__file__', None)
                            if not mod_file:
                                continue
                            mod_file_abs = os.path.abspath(mod_file)
                            if mod_file_abs.startswith(root_abs):
                                to_remove.append(name)
                        for name in to_remove:
                            sys.modules.pop(name, None)
                        sys.modules.pop("dars_app", None)

                        unique_name = f"dars_app_reload_{int(time.time()*1000)}"
                        spec = importlib.util.spec_from_file_location(unique_name, app_file)
                        module = importlib.util.module_from_spec(spec)
                        spec.loader.exec_module(module)

                        new_app = None
                        for v in vars(module).values():
                            if getattr(v, "__class__", None) and v.__class__.__name__ == "App":
                                new_app = v
                                break

                        if not new_app:
                            if console:
                                console.print("[red]No App instance found after reload.[/red]")
                            return

                        # Escribir version.txt ANTES de exportar
                        version_file = os.path.join(preview_dir, "version.txt")
                        new_version = str(int(time.time() * 1000))
                        with open(version_file, 'w') as f:
                            f.write(new_version)
                        
                        # Exportar la aplicación
                        if is_desktop:
                            elec_exporter.export(new_app, preview_dir, bundle=False)
                        else:
                            exporter.export(new_app, preview_dir, bundle=False)
                        
                        # Verificar que la exportación fue exitosa
                        index_path = os.path.join(preview_dir, "index.html")
                        if os.path.exists(index_path):
                            if console:
                                console.print("[green]App reloaded and re-exported successfully.[/green]")
                        else:
                            if console:
                                console.print("[red]Export failed: index.html not created[/red]")
                            
                except Exception as e:
                    tb = traceback.format_exc()
                    if console:
                        console.print(f"[red]Hot reload failed: {e}\n{tb}[/red]")
                    else:
                        print(f"[Dars] Hot reload failed: {e}\n{tb}")

        # ---- DESKTOP MODE ----
        if is_desktop:
            try:
                from dars.exporters.desktop.electron import ElectronExporter
                from dars.core import js_bridge as jsb
            except Exception as e:
                if console:
                    console.print(f"[red]Desktop dev setup failed: {e}[/red]")
                else:
                    print(f"[Dars] Desktop dev setup failed: {e}")
                return

            # Mark initialization as in progress
            initialization_complete.clear()

            try:
                with pushd(project_root):
                    elec_exporter = ElectronExporter()
                    ok = elec_exporter.export(self, preview_dir, bundle=False)
                    if not ok:
                        if console:
                            console.print("[red]Electron export failed.[/red]")
                        else:
                            print("[Dars] Electron export failed.")
                        return

                if not jsb.electron_available():
                    if console:
                        console.print("[yellow]⚠ Electron not found. Run: dars doctor --all --yes[/yellow]")
                    else:
                        print("[Dars] Electron not found. Run: dars doctor --all --yes")
                    return

                run_msg = f"Running dev: {app_file}\nLaunching Electron (dev)..."
                if console:
                    console.print(f"[cyan]{run_msg}[/cyan]")
                else:
                    print(run_msg)

                files_to_watch = _collect_project_files_by_ext(project_root, watch_exts)
                if not files_to_watch:
                    files_to_watch = [app_file]

                electron_proc = None
                stream_threads = []
                control_port = None
                restart_triggered = False

                def start_electron():
                    nonlocal electron_proc, stream_threads, control_port, restart_triggered
                    try:
                        import socket as _socket
                        s = _socket.socket()
                        s.bind(('127.0.0.1', 0))
                        picked = s.getsockname()[1]
                        s.close()
                    except Exception:
                        picked = None
                        
                    env = os.environ.copy()
                    if picked:
                        env['DARS_CONTROL_PORT'] = str(picked)
                        
                    p, cmd = jsb.electron_dev_spawn(cwd=preview_dir, env=env)
                    if p and picked:
                        control_port = picked
                        
                    if not p:
                        msg = f"Could not start Electron (cmd: {cmd}). Ensure Electron is installed."
                        if console:
                            console.print(f"[red]{msg}[/red]")
                        else:
                            print(msg)
                        return False

                    def _stream_output(pipe, is_err=False):
                        try:
                            for line in iter(pipe.readline, ''):
                                if not line:
                                    break
                                text = line.rstrip('\n')
                                if is_err and ("Uncaught" in text or "Error" in text or "TypeError" in text or "ReferenceError" in text):
                                    if console:
                                        console.print(f"[red][Electron STDERR][/red] {text}")
                                    else:
                                        print(f"[Electron STDERR] {text}")
                                else:
                                    if console:
                                        console.print(f"[Electron] {text}")
                                    else:
                                        print(f"[Electron] {text}")
                        except Exception:
                            pass

                    t_out = threading.Thread(target=_stream_output, args=(p.stdout, False), daemon=True)
                    t_err = threading.Thread(target=_stream_output, args=(p.stderr, True), daemon=True)
                    t_out.start()
                    t_err.start()
                    stream_threads = [t_out, t_err]
                    electron_proc = p
                    
                    try:
                        if console:
                            console.print(f"[magenta]Electron PID: {p.pid}[/magenta]")
                        else:
                            print(f"[Dars] Electron PID: {p.pid}")
                    except Exception:
                        pass
                    
                    restart_triggered = False
                    return True

                def stop_electron():
                    nonlocal electron_proc
                    if electron_proc:
                        # Fast shutdown - use terminate immediately for faster exit
                        try:
                            if control_port:
                                try:
                                    import urllib.request as _ur
                                    url = f"http://127.0.0.1:{control_port}/__dars_shutdown"
                                    req = _ur.Request(url, method='POST')
                                    _ur.urlopen(req, timeout=0.5)  # Reduced timeout
                                except Exception:
                                    pass
                        except Exception:
                            pass

                        # Fast kill process
                        try:
                            pid = electron_proc.pid
                            if os.name == 'nt':
                                subprocess.run(["taskkill", "/F", "/T", "/PID", str(pid)], 
                                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=2)
                            else:
                                try:
                                    os.killpg(os.getpgid(pid), signal.SIGTERM)
                                    electron_proc.wait(timeout=1)
                                except:
                                    try:
                                        electron_proc.terminate()
                                        electron_proc.wait(timeout=1)
                                    except:
                                        try:
                                            electron_proc.kill()
                                        except:
                                            pass
                        except Exception:
                            try:
                                electron_proc.terminate()
                            except:
                                pass
                        finally:
                            electron_proc = None

                def reload_and_restart(changed_file=None):
                    nonlocal restart_triggered
                    handle_file_change(f"File changed: {os.path.relpath(changed_file, project_root)}" if changed_file else "Change detected")
                    restart_triggered = True
                    stop_electron()
                    start_electron()

                # Crear EnhancedFileWatchers para archivos individuales
                for f in files_to_watch:
                    try:
                        w = EnhancedFileWatcher(f, lambda f=f: reload_and_restart(f))
                        w.start()
                        watchers.append(w)
                    except Exception as e:
                        if console:
                            console.print(f"[yellow]Warning: could not watch {f}: {e}[/yellow]")
                        else:
                            print(f"[Dars] Warning: could not watch {f}: {e}")

                # Crear DirectoryWatcher para detectar nuevos archivos
                try:
                    dir_watcher = DirectoryWatcher(
                        project_root, 
                        watch_exts, 
                        lambda msg: reload_and_restart(),
                        poll_interval=2.0  # Check for new files every 2 seconds
                    )
                    dir_watcher.start()
                    directory_watchers.append(dir_watcher)
                    
                except Exception as e:
                    if console:
                        console.print(f"[yellow]Warning: could not start directory watcher: {e}[/yellow]")

                # Mark initialization as complete
                initialization_complete.set()

                # Check if shutdown was requested during initialization
                if shutdown_event.is_set():
                    if console:
                        console.print("[yellow]Shutdown requested during initialization. Stopping...[/yellow]")
                    # Clean up and return
                    for w in watchers:
                        try:
                            w.stop()
                        except Exception:
                            pass
                    for dw in directory_watchers:
                        try:
                            dw.stop()
                        except Exception:
                            pass
                    return

                if not start_electron():
                    for w in watchers:
                        try:
                            w.stop()
                        except Exception:
                            pass
                    for dw in directory_watchers:
                        try:
                            dw.stop()
                        except Exception:
                            pass
                    return

                try:
                    while not shutdown_event.is_set():
                        if electron_proc and electron_proc.poll() is not None:
                            code = electron_proc.returncode
                            if restart_triggered:
                                if console:
                                    console.print(f"[red]Electron exited with code {code}. Restarting...[/red]")
                                else:
                                    print(f"[Dars] Electron exited with code {code}. Restarting...")
                                restart_triggered = False
                                stop_electron()
                                start_electron()
                            else:
                                if console:
                                    console.print(f"[cyan]Electron closed by user (code {code}). Stopping dev mode...[/cyan]")
                                else:
                                    print(f"[Dars] Electron closed by user (code {code}). Stopping dev mode...")
                                shutdown_event.set()
                                break
                        time.sleep(0.1)  # Faster polling
                except KeyboardInterrupt:
                    shutdown_event.set()
                finally:
                    # Fast cleanup for desktop mode
                    stop_electron()
                    for w in watchers:
                        try:
                            w.stop()
                        except Exception:
                            pass
                    for dw in directory_watchers:
                        try:
                            dw.stop()
                        except Exception:
                            pass
                    cleanup_done_event.set()
                    time.sleep(0.1)  # Minimal delay
                    return

            except Exception as e:
                initialization_complete.set()
                raise

        # ---- WEB MODE ----
        # Mark initialization as in progress
        initialization_complete.clear()

        try:
            with pushd(project_root):
                exporter.export(self, preview_dir, bundle=False)
        except Exception as e:
            if console:
                console.print(f"[red]Export failed: {e}[/red]")
            else:
                print(f"Export failed: {e}")
            initialization_complete.set()
            return

        if not PreviewServer:
            if console:
                console.print("[red]Preview server module not available.[/red]")
            else:
                print("[Dars] Preview server module not available.")
            initialization_complete.set()
            return

        url = f"http://localhost:{port}"
        app_title = getattr(self, 'title', 'Dars App')

        # Mensaje inicial bonito con Panel
        try:
            if console and Panel and Text:
                panel = Panel(
                    Text(
                        f"✔ App running successfully\n\nName: {app_title}\nPreview available at: {url}\n\nPress Ctrl+C to stop the server.",
                        style="bold green", justify="center"),
                    title="Dars Preview", border_style="cyan")
                console.print(panel)
            else:
                print(f"[Dars] App '{app_title}' running. Preview at {url}")
        except Exception:
            print(f"[Dars] App '{app_title}' running. Preview at {url}")

        server = PreviewServer(preview_dir, port)
        server_exception = {"exc": None}

        def _server_thread_fn():
            try:
                started = server.start()
                if not started:
                    if console:
                        console.print("[red]Could not start preview server.[/red]")
                    else:
                        print("Could not start preview server.")
                    return
            except Exception as e:
                server_exception["exc"] = e
                if console:
                    console.print(f"[red]Server thread exception: {e}[/red]")
                else:
                    print(f"Server thread exception: {e}\n{traceback.format_exc()}")

        srv_thread = threading.Thread(target=_server_thread_fn, daemon=True)
        srv_thread.start()

        files_to_watch = _collect_project_files_by_ext(project_root, watch_exts)
        if not files_to_watch:
            files_to_watch = [app_file]

        # Crear EnhancedFileWatchers para archivos individuales
        for f in files_to_watch:
            try:
                w = EnhancedFileWatcher(f, lambda f=f: handle_file_change(f"File changed: {os.path.relpath(f, project_root)}"))
                w.start()
                watchers.append(w)
            except Exception as e:
                if console:
                    console.print(f"[yellow]Warning: could not watch {f}: {e}[/yellow]")
                else:
                    print(f"[Dars] Warning: could not watch {f}: {e}")

        # Crear DirectoryWatcher para detectar nuevos archivos
        try:
            dir_watcher = DirectoryWatcher(
                project_root, 
                watch_exts, 
                lambda msg: handle_file_change(msg),
                poll_interval=2.0
            )
            dir_watcher.start()
            directory_watchers.append(dir_watcher)
        except Exception as e:
            if console:
                console.print(f"[yellow]Warning: could not start directory watcher: {e}[/yellow]")

        # Mark initialization as complete
        initialization_complete.set()

        # Check if shutdown was requested during initialization
        if shutdown_event.is_set():
            if console:
                console.print("[yellow]Shutdown requested during initialization. Stopping...[/yellow]")
            # Clean up and return
            for w in watchers:
                try:
                    w.stop()
                except Exception:
                    pass
            for dw in directory_watchers:
                try:
                    dw.stop()
                except Exception:
                    pass
            try:
                server.stop()
            except Exception:
                pass
            cleanup_done_event.set()
            return

        # Show watched files if enabled
        if self.watchfiledialog and console and Table:
            rel_paths = [os.path.relpath(f, project_root) for f in files_to_watch]
            max_show = 80
            if len(rel_paths) > max_show:
                shown = rel_paths[:max_show]
                shown.append(f"... (+{len(rel_paths)-max_show} more)")
            else:
                shown = rel_paths or ["(none)"]

            table = Table(show_header=False, box=None, padding=0)
            table.add_column("Files", style="bold")
            for p in shown:
                table.add_row(p)

            panel = Panel(
                table,
                title=f"Watching {len(files_to_watch)} files · Exts: {', '.join(watch_exts)}",
                subtitle=f"Project root: {os.path.basename(project_root)}",
                border_style="magenta"
            )
            console.print(panel)
        elif self.watchfiledialog:
            print(f"[Dars] Watching {len(files_to_watch)} files in {project_root}:")
            for f in files_to_watch:
                print("  -", os.path.relpath(f, project_root))

        # ---- IMPROVED MAIN LOOP ----
        try:
            while not shutdown_event.is_set():
                if server_exception.get("exc"):
                    if console:
                        console.print(f"[red]Server failed during startup: {server_exception['exc']}[/red]")
                    else:
                        print("Server failed during startup:", server_exception["exc"])
                    break
                time.sleep(0.1)  # Faster polling
        except Exception as e:
            if console:
                console.print(f"[red]Main loop exception: {e}[/red]")
            else:
                print("Main loop exception:", e)
        finally:
            # FAST CLEANUP - New version style
            shutdown_event.set()
            
            # Stop watchers first (fast)
            for w in watchers:
                try:
                    w.stop()
                except Exception:
                    pass
            
            # Stop directory watchers
            for dw in directory_watchers:
                try:
                    dw.stop()
                except Exception:
                    pass

            # Fast server shutdown
            try:
                if server and hasattr(server, "httpd"):
                    # Fast shutdown without graceful waiting
                    try:
                        server.httpd.shutdown()
                    except Exception:
                        pass
                    try:
                        server.httpd.server_close()
                    except Exception:
                        pass
            except Exception:
                pass

            cleanup_done_event.set()
            time.sleep(0.15)  # Minimal delay for cleanup

            if console:
                console.print("[green]✔ Preview stopped.[/green]")
            else:
                print("✔ Preview stopped.")

            # Restore original directory
            try:
                os.chdir(cwd_original)
            except Exception:
                pass

            # Fast preview directory cleanup
            try:
                shutil.rmtree(preview_dir, ignore_errors=True)
                if console:
                    console.print("[yellow]Preview files deleted.[/yellow]")
                else:
                    print("Preview files deleted.")
            except Exception as e:
                if console:
                    console.print(f"[yellow]Note: Could not delete preview directory: {e}[/yellow]")

    
    def __init__(
        self,
        title: str = "Dars App",
        description: str = "",
        author: str = "",
        version: str = "",
        keywords: List[str] = None,
        language: str = "en",
        favicon: str = "",
        icon: str = "",
        apple_touch_icon: str = "",
        manifest: str = "",
        theme_color: str = "#000000",
        background_color: str = "#ffffff",
        service_worker_path: str = "",
        service_worker_enabled: bool = False,
        **config
    ):
        # Propiedades básicas de la aplicación
        self.title = title
        self.description = description
        self.author = author
        # Optional app version (used for desktop package.json if present)
        self.version = version
        self.keywords = keywords or []
        self.language = language
        
        # Iconos y favicon
        self.favicon = favicon
        self.icon = icon  # Para PWA y meta tags
        self.apple_touch_icon = apple_touch_icon
        self.manifest = manifest  # Para PWA manifest.json
        
        # Colores para PWA y tema
        self.icons = config.get('icons', [])
        self.theme_color = theme_color
        self.background_color = background_color
        self.service_worker_path = service_worker_path
        self.service_worker_enabled = service_worker_enabled
        
        # Propiedades Open Graph (para redes sociales)

        #
        # [RECOMENDACIÓN DARS]
        # Para lanzar la compilación/preview rápido de tu app, añade al final de tu archivo principal:
        #   if __name__ == "__main__":
        #       app.rTimeCompile()  # o app.timeCompile()
        # Así tendrás preview instantáneo y control explícito, sin efectos colaterales.
        #
        self.og_title = config.get('og_title', title)
        self.og_description = config.get('og_description', description)
        self.og_image = config.get('og_image', '')
        self.og_url = config.get('og_url', '')
        self.og_type = config.get('og_type', 'website')
        self.og_site_name = config.get('og_site_name', '')
        
        # Twitter Cards
        self.twitter_card = config.get('twitter_card', 'summary')
        self.twitter_site = config.get('twitter_site', '')
        self.twitter_creator = config.get('twitter_creator', '')
        
        # SEO y robots
        self.robots = config.get('robots', 'index, follow')
        self.canonical_url = config.get('canonical_url', '')
        
        # PWA configuración
        self.pwa_enabled = config.get('pwa_enabled', False)
        self.pwa_name = config.get('pwa_name', title)
        self.pwa_short_name = config.get('pwa_short_name', title[:12])
        self.pwa_display = config.get('pwa_display', 'standalone')
        self.pwa_orientation = config.get('pwa_orientation', 'portrait')
        
        # Propiedades del framework
        self.root: Optional[Component] = None  # Single-page mode
        self._pages: Dict[str, Page] = {}      # Multipage mode
        self._index_page: str = None           # Nombre de la página principal (si existe)
        self.scripts: List['Script'] = []
        self.global_styles: Dict[str, Any] = {}
        self.global_style_files: List[str] = []
        self.event_manager = EventManager()
        self.config = config
        
        # Configuración por defecto
        self.config.setdefault('viewport', {
            'width': 'device-width',
            'initial_scale': 1.0,
            'user_scalable': 'yes'
        })
        self.config.setdefault('theme', 'light')
        self.config.setdefault('responsive', True)
        self.config.setdefault('charset', 'UTF-8')
        
    def set_root(self, component: Component):
        """Sets the root component of the application (backward-compatible single-page mode)."""
        self.root = component

    def add_page(self, name: str, root: 'Component', title: str = None, meta: dict = None, index: bool = False):
        """
        Adds a multipage page to the app.  
        `name` is the slug/key, `root` the root component.  
        If `index=True`, this page will be the main one (exported as index.html).  
        If multiple pages have `index=True`, the last registered one will be the main page.  
        """
        if name in self._pages:
            raise ValueError(f"Page already exists with this name: '{name}'")
        self._pages[name] = Page(name, root, title, meta, index=index)
        if index:
            self._index_page = name


    def get_page(self, name: str) -> 'Page':
        """Obtain one registered page by name."""
        return self._pages.get(name)

    def get_index_page(self) -> 'Page':
        """
        Returns the index page, or the first one if none has index=True.
        """
        # Prioridad: explícita, luego la primera
        if hasattr(self, '_index_page') and self._index_page and self._index_page in self._pages:
            return self._pages[self._index_page]
        for page in self._pages.values():
            if getattr(page, 'index', False):
                return page
        # Si ninguna marcada, devolver la primera
        if self._pages:
            return list(self._pages.values())[0]
        return None


    @property
    def pages(self) -> Dict[str, 'Page']:
        """Returns the registered pages dictionary (multipage)."""
        return self._pages

    def is_multipage(self) -> bool:
        """Indicate if the app is in multipage mode."""
        return bool(self._pages)
        
    def add_script(self, script: 'Script'):
        """Adds a script to the app"""
        self.scripts.append(script)
        
    def add_global_style(self, selector: str = None, styles: Dict[str, Any] = None, file_path: str = None):
        """
        Adds a global style to the app.
        
        - If file_path is provided, the CSS file is read and stored.
        - If selector and styles are provided, they are stored as inline CSS rules.
        - It is invalid to mix file_path with selector/styles.
        """
        if file_path:
            if selector or styles:
                raise ValueError("Cannot use selector/styles when file_path is provided.")
            if file_path not in self.global_style_files:
                self.global_style_files.append(file_path)
            return self

        if not selector or not styles:
            raise ValueError("Must provide selector and styles when file_path is not used.")
        
        self.global_styles[selector] = styles
        return self
        
    def set_theme(self, theme: str):
        """Set the theme for the app"""
        self.config['theme'] = theme
        
    def set_favicon(self, favicon_path: str):
        """Set the favicon for the app"""
        self.favicon = favicon_path
    
    def set_icon(self, icon_path: str):
        """Set the principal icon for the app"""
        self.icon = icon_path
    
    def set_apple_touch_icon(self, icon_path: str):
        """Set de icon for apple devices"""
        self.apple_touch_icon = icon_path
    
    def set_manifest(self, manifest_path: str):
        """Set the manifes for PWA"""
        self.manifest = manifest_path
    
    def add_keyword(self, keyword: str):
        """Add a keyword for SEO"""
        if keyword not in self.keywords:
            self.keywords.append(keyword)
    
    def add_keywords(self, keywords: List[str]):
        """Add multiple keywords for SEO"""
        for keyword in keywords:
            self.add_keyword(keyword)
    
    def set_open_graph(self, **og_data):
        """Configure properties of Open Graph for social media sharing"""
        if 'title' in og_data:
            self.og_title = og_data['title']
        if 'description' in og_data:
            self.og_description = og_data['description']
        if 'image' in og_data:
            self.og_image = og_data['image']
        if 'url' in og_data:
            self.og_url = og_data['url']
        if 'type' in og_data:
            self.og_type = og_data['type']
        if 'site_name' in og_data:
            self.og_site_name = og_data['site_name']
    
    def set_twitter_card(self, card_type: str = 'summary', site: str = '', creator: str = ''):
        """Set the Twitter Card meta tags"""
        self.twitter_card = card_type
        if site:
            self.twitter_site = site
        if creator:
            self.twitter_creator = creator
    
    def enable_pwa(self, name: str = None, short_name: str = None, display: str = 'standalone'):
        """Enable PWA settings (Progressive Web App)"""
        self.pwa_enabled = True
        if name:
            self.pwa_name = name
        if short_name:
            self.pwa_short_name = short_name
        self.pwa_display = display
    
    def set_theme_colors(self, theme_color: str, background_color: str = None):
        """Select the theme color of the PWA theme and browsers themes """
        self.theme_color = theme_color
        if background_color:
            self.background_color = background_color
    
    def get_meta_tags(self) -> Dict[str, str]:
        """Obtain all tags of as a dictionary"""
        meta_tags = {}
        
        # Meta tags básicos
        if self.description:
            meta_tags['description'] = self.description
        if self.author:
            meta_tags['author'] = self.author
        if self.keywords:
            meta_tags['keywords'] = ', '.join(self.keywords)
        if self.robots:
            meta_tags['robots'] = self.robots
        
        # Viewport
        viewport_parts = []
        for key, value in self.config['viewport'].items():
            if key == 'initial_scale':
                viewport_parts.append(f'initial-scale={value}')
            elif key == 'user_scalable':
                viewport_parts.append(f'user-scalable={value}')
            else:
                viewport_parts.append(f'{key.replace("_", "-")}={value}')
        meta_tags['viewport'] = ', '.join(viewport_parts)
        
        # PWA y tema
        meta_tags['theme-color'] = self.theme_color
        if self.pwa_enabled:
            meta_tags['mobile-web-app-capable'] = 'yes'
            meta_tags['apple-mobile-web-app-capable'] = 'yes'
            meta_tags['apple-mobile-web-app-status-bar-style'] = 'default'
            meta_tags['apple-mobile-web-app-title'] = self.pwa_short_name
        
        return meta_tags
    
    def get_open_graph_tags(self) -> Dict[str, str]:
        """ Obtain all tags of Open Graph"""
        og_tags = {}
        
        if self.og_title:
            og_tags['og:title'] = self.og_title
        if self.og_description:
            og_tags['og:description'] = self.og_description
        if self.og_image:
            og_tags['og:image'] = self.og_image
        if self.og_url:
            og_tags['og:url'] = self.og_url
        if self.og_type:
            og_tags['og:type'] = self.og_type
        if self.og_site_name:
            og_tags['og:site_name'] = self.og_site_name
        
        return og_tags
    
    def get_twitter_tags(self) -> Dict[str, str]:
        """Obtain all tags of Twitter Cards"""
        twitter_tags = {}
        
        if self.twitter_card:
            twitter_tags['twitter:card'] = self.twitter_card
        if self.twitter_site:
            twitter_tags['twitter:site'] = self.twitter_site
        if self.twitter_creator:
            twitter_tags['twitter:creator'] = self.twitter_creator
        
        return twitter_tags
        
    def export(self, exporter: 'Exporter', output_path: str) -> bool:
        """Exports the application to the specified path using the exporter"""
        if not self.root:
            raise ValueError("No se ha establecido un componente raíz")
        
        return exporter.export(self, output_path)
        
    def validate(self) -> List[str]:
        """Validate the applicatiob and return a error lines"""
        errors = []

        # Validar título
        if not self.title:
            errors.append("The application title can't be empty.")

        # Validación single-page y multipage
        if self.is_multipage():
            if not self._pages:
                errors.append("The app is on multipage mode but there are no pages registered.")
            for name, page in self._pages.items():
                if not page.root:
                    errors.append(f"The page '{name}' hasn't a root component.")
                else:
                    errors.extend(self._validate_component(page.root, path=f"pages['{name}']"))
        else:
            if not self.root:
                errors.append("Can't find a root component (single-page mode)")
            else:
                errors.extend(self._validate_component(self.root))

        return errors
        
    def _validate_component(self, component: Component, path: str = "root") -> List[str]:
        """Validate a component and its children recursively"""
        errors = []

        # Validar que el componente tenga un método render
        if not hasattr(component, 'render'):
            errors.append(f"The component in {path} doesn't have render method")
            
        # Validar hijos
        for i, child in enumerate(component.children):
            child_path = f"{path}.children[{i}]"
            errors.extend(self._validate_component(child, child_path))
            
        return errors

    def _count_components(self, component: Component) -> int:
        """Count the total number of components in the app"""
        count = 1
        for child in component.children:
            count += self._count_components(child)
        return count
    def get_component_tree(self) -> str:
        """
        Returns a legible representation of the component tree.
        """
        def tree_str(component, indent=0):
            pad = '  ' * indent
            s = f"{pad}- {component.__class__.__name__} (id={getattr(component, 'id', None)})"
            for child in getattr(component, 'children', []):
                s += '\n' + tree_str(child, indent + 1)
            return s

        if self.is_multipage():
            if not self._pages:
                return "[Dars] No pages registered."
            result = []
            for name, page in self._pages.items():
                result.append(f"Página: {name} (title={page.title})\n" + tree_str(page.root))
            return '\n\n'.join(result)
        elif self.root:
            return tree_str(self.root)
        else:
            return "[Dars] No root component defined."
        
    def _component_to_dict(self, component: Component) -> Dict[str, Any]:
        """Convert a component to a dictionary for inspection"""
        return {
            'type': component.__class__.__name__,
            'id': component.id,
            'class_name': component.class_name,
            'props': component.props,
            'style': component.style,
            'children': [self._component_to_dict(child) for child in component.children]
        }
        
    def find_component_by_id(self, component_id: str) -> Optional[Component]:
        """Find a component by its ID (soporta multipage y single-page)"""
        if self.is_multipage():
            for page in self._pages.values():
                result = self._find_component_recursive(page.root, component_id)
                if result:
                    return result
            return None
        elif self.root:
            return self._find_component_recursive(self.root, component_id)
        else:
            return None

    def _find_component_recursive(self, component: Component, target_id: str) -> Optional[Component]:
        """Search components recursively by ID"""
        if component.id == target_id:
            return component
        for child in getattr(component, 'children', []):
            result = self._find_component_recursive(child, target_id)
            if result:
                return result
        return None
        
    def get_stats(self) -> Dict[str, Any]:
        """Return application stadistics (single-page and multipage)"""
        if self.is_multipage():
            total_components = 0
            max_depth = 0
            for page in self._pages.values():
                if page.root:
                    total_components += self._count_components(page.root)
                    depth = self._calculate_max_depth(page.root)
                    max_depth = max(max_depth, depth)
            return {
                'total_components': total_components,
                'max_depth': max_depth,
                'scripts_count': len(self.scripts),
                'global_styles_count': len(self.global_styles),
                'total_pages': len(self._pages)
            }
        elif self.root:
            return {
                'total_components': self._count_components(self.root),
                'max_depth': self._calculate_max_depth(self.root),
                'scripts_count': len(self.scripts),
                'global_styles_count': len(self.global_styles),
                'total_pages': 1
            }
        else:
            return {
                'total_components': 0,
                'max_depth': 0,
                'scripts_count': len(self.scripts),
                'global_styles_count': len(self.global_styles),
                'total_pages': 0
            }

    def calculate_max_depth(self) -> int:
        """Calculates the maximun depth of a component tree (single page and multipage)"""
        if self.is_multipage():
            return max((self._calculate_max_depth(page.root) for page in self._pages.values() if page.root), default=0)
        elif self.root:
            return self._calculate_max_depth(self.root)
        else:
            return 0

    def _calculate_max_depth(self, component: Component, current_depth: int = 0) -> int:
        """Calculates the maximun depth of a component tree (internal use)"""
        if not component or not getattr(component, 'children', []):
            return current_depth
        return max(self._calculate_max_depth(child, current_depth + 1) for child in component.children)


