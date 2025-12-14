# Dars Framework - Core Source File
#
# This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0.
# If a copy of the MPL was not distributed with this file, You can obtain one at
# https://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2025 ZtaDev
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

    def useWatch(self, state_path: str, *js_helpers):
        """Adds a watcher to this page."""
        from dars.hooks.use_watch import useWatch
        watcher = useWatch(state_path, *js_helpers)
        self.add_script(watcher)
        return self

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

    def __init__(
        self,
        title: str = "Dars App",
        meta: dict = None,
        description: str = "",
        author: str = "",
        version: str = "",
        keywords: List[str] = None,
        language: str = "en",
        favicon: str = "",
        icon: str = "",
        apple_touch_icon: str = "",
        apple_mobile_web_app_capable: bool = False,
        apple_mobile_web_app_status_bar_style: str = "default",  # "default", "black", "black-translucent"
        apple_mobile_web_app_title: str = "",
        manifest: str = "",
        theme_color: str = "#000000",
        background_color: str = "#ffffff",
        service_worker_path: str = "",
        service_worker_enabled: bool = False,
        desktop: bool = False,
        devtools: bool = True,  # Auto-open DevTools in desktop dev mode
        ssr_url: str = None,  # URL for SSR backend fetching
        **config
    ):

        # Propiedades básicas de la aplicación
        self.title = title
        self.meta = meta or {}
        self._pages = {}
        self.ssr_url = ssr_url  # URL for SSR backend fetching
        self._spa_routes = {}
        self._spa_404_page = None
        self._spa_403_page = None
        self._spa_loading_page = None
        self._spa_error_page = None
        
        # Initialize default meta tags
        if "viewport" not in self.meta:
            self.meta["viewport"] = "width=device-width, initial-scale=1.0"
        if "charset" not in self.meta:
            self.meta["charset"] = "utf-8"
        self.description = description
        self.author = author
        # Optional app version (used for desktop package.json if present)
        self.version = version
        self.keywords = keywords or []
        self.language = language
        self.desktop = desktop
        # Iconos y favicon
        self.favicon = favicon
        self.icon = icon  # Para PWA y meta tags
        self.apple_touch_icon = apple_touch_icon
        # Apple mobile web app properties
        self.apple_mobile_web_app_capable = apple_mobile_web_app_capable
        self.apple_mobile_web_app_status_bar_style = apple_mobile_web_app_status_bar_style
        self.apple_mobile_web_app_title = apple_mobile_web_app_title or title
        self.manifest = manifest  # Para PWA manifest.json
        
        # Colores para PWA y tema
        self.icons = config.get('icons', [])
        self.theme_color = theme_color
        self.background_color = background_color
        self.service_worker_path = service_worker_path
        self.service_worker_enabled = service_worker_enabled
        
        # Desktop configuration
        self.devtools = devtools  # Control DevTools auto-open in dev mode
        self.ssr_url = ssr_url
        
        # Load project configuration and register custom utilities
        try:
            from dars.config import load_config
            from dars.core.utilities import register_custom_utilities
            
            # Detect project root (similar to rTimeCompile)
            import inspect
            import sys
            import os
            
            app_file = None
            for frame in inspect.stack():
                if frame.function == "<module>":
                    app_file = frame.filename
                    break
            if not app_file:
                app_file = sys.argv[0]
            
            project_root = os.path.dirname(os.path.abspath(app_file))
            cfg, cfg_found = load_config(project_root)
            
            if cfg_found and 'utility_styles' in cfg:
                register_custom_utilities(cfg['utility_styles'])
                
        except Exception:
            # Fail silently if config loading fails during init
            pass
        
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
        self._pages: Dict[str, Page] = {}      # Traditional multipage mode
        self._index_page: str = None           # Nombre de la página principal (si existe)
        
        # SPA Routing properties
        self._spa_routes: Dict[str, 'SPARoute'] = {}  # SPA routes by name
        self._spa_route_tree: Optional['RouteNode'] = None  # Tree structure for nested routes
        self._spa_index_route: str = None      # Main SPA route
        self._spa_404_page: Optional[Page] = None  # Custom 404 page
        self._spa_403_page: Optional[Page] = None  # Custom 403 Forbidden page
        self._spa_loading_page: Optional[Any] = None
        self._spa_error_page: Optional[Any] = None
        
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


    def add_page(
        self, 
        name: str, 
        root: 'Component', 
        title: str = None, 
        meta: dict = None, 
        index: bool = False,
        route: str = None,
        preload: List[str] = None,
        parent: str = None,
        outlet_id: str = "main"
    ):
        """
        Adds a page to the app. Can be traditional multipage or SPA route.
        
        Args:
            name: Page identifier/slug
            root: Root component for the page
            title: Page title
            meta: Metadata dict
            index: If True, this is the main/index page
            route: SPA route path (e.g., "/home", "/user/:id"). If provided, page becomes SPA route
            preload: List of route paths to preload (only valid with route parameter)
            parent: Parent route name for nested routes (only valid with route parameter)
        
        Raises:
            ValueError: If route is defined both via decorator and parameter
            ValueError: If preload is used without route
            ValueError: If parent is used without route
            ValueError: If page name already exists
        
        Examples:
            # Traditional multipage
            app.add_page("about", about_page)
            
            # SPA route
            app.add_page("home", home_page, route="/")
            
            # SPA route with parameters
            app.add_page("user", user_page, route="/user/:id")
            
            # Nested SPA route
            app.add_page("docs", docs_layout, route="/docs")
            app.add_page("docs_start", getting_started, route="/docs/getting-started", parent="docs")
        """
        from dars.core.routing import get_route, SPARoute, RouteNode
        
        # Check for route from decorator
        decorator_route = get_route(root)
        
        # Validate route definition (can't define in both places)
        if decorator_route and route:
            raise ValueError(
                f"Route for page '{name}' is defined in both @route decorator "
                f"('{decorator_route}') and route parameter ('{route}'). "
                "Please use only one method."
            )
        
        # Determine final route
        final_route = route or decorator_route
        
        # Validate preload usage
        if preload and not final_route:
            raise ValueError(
                f"preload parameter cannot be used without route definition for page '{name}'"
            )
        
        # Validate parent usage
        if parent and not final_route:
            raise ValueError(
                f"parent parameter cannot be used without route definition for page '{name}'"
            )
        
        # Check if page already exists
        if name in self._pages or name in self._spa_routes:
            raise ValueError(f"Page already exists with this name: '{name}'")
        
        # Create SPA route or traditional page
        if final_route:
            # Validate parent exists if specified
            if parent and parent not in self._spa_routes:
                raise ValueError(
                    f"Parent route '{parent}' does not exist for page '{name}'. "
                    f"Add parent route before child routes."
                )
            
            # Initialize route tree if needed
            if self._spa_route_tree is None:
                self._spa_route_tree = RouteNode()
            
            # Create SPA route
            spa_route = SPARoute(
                name=name,
                root=root,
                route=final_route,
                title=title,
                meta=meta,
                preload=preload,
                index=index,
                parent=parent,
                outlet_id=outlet_id
            )
            self._spa_routes[name] = spa_route
            
            # Build route tree
            route_node = RouteNode(spa_route)
            if parent:
                # Add as child of parent
                parent_node = self._find_route_node(self._spa_route_tree, parent)
                if parent_node:
                    parent_node.add_child(route_node)
            else:
                # Add as top-level route
                self._spa_route_tree.add_child(route_node)
            
            if index:
                self._spa_index_route = name
        else:
            # Traditional multipage
            self._pages[name] = Page(name, root, title, meta, index=index)
            if index:
                self._index_page = name


    def _find_route_node(self, node: 'RouteNode', route_name: str) -> Optional['RouteNode']:
        """Helper to find a RouteNode by its route name in the SPA route tree."""
        if node.route and node.route.name == route_name:
            return node
        for child in node.children:
            found = self._find_route_node(child, route_name)
            if found:
                return found
        return None

    def get_page(self, name: str) -> 'Page':
        """Obtain one registered page by name."""
        return self._pages.get(name)

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

        # ---- PREVIEW DIR CLEANUP (OPTIMIZED) ----
        preview_dir = os.path.join(project_root, "dars_preview")
        
        # Optimization: Rename and delete in background to avoid blocking startup
        if os.path.exists(preview_dir):
            try:
                # Create a unique trash name
                trash_name = f"dars_preview_trash_{int(time.time()*1000)}"
                trash_path = os.path.join(project_root, trash_name)
                os.rename(preview_dir, trash_path)
                
                # Delete in background thread
                def _bg_cleanup(path):
                    try:
                        shutil.rmtree(path, ignore_errors=True)
                    except: pass
                    
                threading.Thread(target=_bg_cleanup, args=(trash_path,), daemon=True).start()
            except Exception:
                # Fallback to blocking delete if rename fails (e.g. open files)
                try:
                    shutil.rmtree(preview_dir, ignore_errors=True)
                except: pass
                
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
        # Fix logic: Use self.desktop attribute if available, regardless of config
        is_desktop = bool(getattr(self, 'desktop', False) or fmt == 'desktop')

        # ---- STARTUP SPINNER ----
        startup_status = None
        if console:
            startup_status = console.status("[bold cyan]Starting preview...[/bold cyan]", spinner="dots")
            startup_status.start()

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

                        # Clear state registry to prevent duplicates
                        try:
                            from dars.core.state_v2 import clear_state_registry
                            clear_state_registry()
                        except ImportError:
                            pass

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
                        if is_desktop:
                            # In desktop mode, index.html is inside 'app' folder
                            index_path = os.path.join(preview_dir, "app", "index.html")
                        
                        if os.path.exists(index_path):
                            if console:
                                console.print("[green]App reloaded and re-exported successfully.[/green]")
                        else:
                            if console:
                                console.print(f"[red]Export failed: {os.path.basename(index_path)} not created[/red]")
                        
                        return True # Indicate success
                            
                except Exception as e:
                    tb = traceback.format_exc()
                    if console:
                        console.print(f"[red]Hot reload failed: {e}\n{tb}[/red]")
                    else:
                        print(f"[Dars] Hot reload failed: {e}\n{tb}")
                    return False # Indicate failure
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
                    env['DARS_DEV'] = '1'
                    env['DARS_DEVTOOLS'] = '1' if getattr(self, 'devtools', True) else '0'
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
                                
                                # Filter out harmless DevTools warnings
                                if "Autofill.enable" in text or "Autofill.setAddresses" in text:
                                    continue
                                if "wasn't found" in text and ("Autofill" in text or "protocol_client" in text):
                                    continue
                                
                                # Only show actual errors, not all stderr
                                if is_err and (("Error" in text and ("occurred in handler" in text or "ENOENT" in text or "TypeError" in text or "ReferenceError" in text)) or "Uncaught" in text):
                                    if console:
                                        console.print(f"[red][Electron Error][/red] {text}")
                                    else:
                                        print(f"[Electron Error] {text}")
                                elif not is_err and text.strip():  # Only show non-empty stdout
                                    # Skip empty lines and unnecessary output
                                    if console:
                                        console.print(f"[dim][Electron][/dim] {text}")
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
                    # Prevent concurrent restarts
                    if restart_triggered:
                        return
                    
                    reloaded = handle_file_change(f"File changed: {os.path.relpath(changed_file, project_root)}" if changed_file else "Change detected")
                    if reloaded:
                        restart_triggered = True
                        time.sleep(0.3)  # Small delay to consolidate multiple file change events
                        stop_electron()
                        time.sleep(0.2)  # Ensure process fully stopped
                        if not shutdown_event.is_set():  # Only restart if not shutting down
                            start_electron()
                            restart_triggered = False


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

                # Stop startup spinner once Electron dev process is running
                if startup_status:
                    try:
                        startup_status.stop()
                    except Exception:
                        pass

                try:
                    while not shutdown_event.is_set():
                        if electron_proc and electron_proc.poll() is not None:
                            code = electron_proc.returncode
                            # Only restart if it wasn't a deliberate restart from file change
                            if restart_triggered:
                                # Already being handled by reload_and_restart
                                if console:
                                    console.print(f"[dim][Electron restarting after file change...][/dim]")
                                # Wait for the restart to complete
                                time.sleep(1)
                                continue
                            else:
                                if console:
                                    console.print(f"[cyan]Electron closed by user (code {code}). Stopping dev mode...[/cyan]")
                                else:
                                    print(f"[Dars] Electron closed by user (code {code}). Stopping dev mode...")
                                shutdown_event.set()
                                break
                        time.sleep(0.5)
  # Faster polling
                except KeyboardInterrupt:
                    shutdown_event.set()
                finally:
                    # Show stopped message IMMEDIATELY
                    if console:
                        console.print("[green]OK Preview stopped.[/green]")
                    else:
                        print("OK Preview stopped.")
                    
                    # All cleanup in background thread
                    def _background_cleanup():
                        # Stop Electron
                        stop_electron()
                        
                        # Stop watchers
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
                    
                    # Start background cleanup
                    cleanup_bg_thread = threading.Thread(target=_background_cleanup, daemon=True)
                    cleanup_bg_thread.start()
                    
                    cleanup_done_event.set()
                    
                    # Clean up preview directory with spinner
                    def _cleanup_preview():
                        try:
                            shutil.rmtree(preview_dir, ignore_errors=True)
                        except Exception:
                            pass
                    
                    # Show spinner while cleaning up (max 2 seconds)
                    if console:
                        with console.status("[yellow]Cleaning up preview files...[/yellow]", spinner="dots"):
                            cleanup_thread = threading.Thread(target=_cleanup_preview, daemon=True)
                            cleanup_thread.start()
                            cleanup_thread.join(timeout=2.0)
                        console.print("[green]OK Preview files deleted.[/green]")
                    else:
                        cleanup_thread = threading.Thread(target=_cleanup_preview, daemon=True)
                        cleanup_thread.start()
                        cleanup_thread.join(timeout=2.0)
                        print("Preview files deleted.")
                    
                    # Restore original directory
                    try:
                        os.chdir(cwd_original)
                    except Exception:
                        pass
                    


            except Exception as e:
                import traceback
                traceback.print_exc()
                initialization_complete.set()
                raise

            # Desktop mode should never fall through into the web preview flow.
            # Once the Electron dev loop finishes (normally or via Ctrl+C), exit rTimeCompile.
            return

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

        # Stop spinner before showing success
        if startup_status:
            startup_status.stop()

        # Mensaje inicial bonito con Panel
        try:
            if console and Panel and Text:
                panel = Panel(
                    Text(
                        f"App running successfully\n\nName: {app_title}\nPreview available at: {url}\n\nPress Ctrl+C to stop the server.",
                        style="bold green", justify="center"),
                    title="Dars Preview", border_style="bold blue", expand=False)
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

        # Initialize watchers in background for faster startup
        def _init_watchers():
            # Crear EnhancedFileWatchers para archivos individuales
            for f in files_to_watch:
                if shutdown_event.is_set():
                    break
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
            if not shutdown_event.is_set():
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
        
        # Start watcher initialization in background
        watcher_init_thread = threading.Thread(target=_init_watchers, daemon=True)
        watcher_init_thread.start()

        # Mark initialization as complete (don't wait for watchers)
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
            
            # Show stopped message IMMEDIATELY (before any cleanup)
            if console:
                console.print("[green]OK Preview stopped.[/green]")
            else:
                print("OK Preview stopped.")
            
            # All cleanup in background thread
            def _background_cleanup():
                # Stop watchers
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
                
                # Server shutdown
                try:
                    if server and hasattr(server, "httpd"):
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
            
            # Start background cleanup
            cleanup_bg_thread = threading.Thread(target=_background_cleanup, daemon=True)
            cleanup_bg_thread.start()
            
            cleanup_done_event.set()

            # Restore original directory
            try:
                os.chdir(cwd_original)
            except Exception:
                pass

            # Fast preview directory cleanup in background
            def _cleanup_preview():
                try:
                    shutil.rmtree(preview_dir, ignore_errors=True)
                except Exception:
                    pass
            
            # Show spinner while cleaning up (max 2 seconds)
            if console:
                with console.status("[yellow]Cleaning up preview files...[/yellow]", spinner="dots"):
                    cleanup_thread = threading.Thread(target=_cleanup_preview, daemon=True)
                    cleanup_thread.start()
                    cleanup_thread.join(timeout=2.0)
                console.print("[green]✔ Preview files deleted.[/green]")
            else:
                cleanup_thread = threading.Thread(target=_cleanup_preview, daemon=True)
                cleanup_thread.start()
                cleanup_thread.join(timeout=2.0)
                print("Preview files deleted.")
    
    def get_index_page(self) -> 'Page':
        """
        Returns the index page from multipage, or None if none has index=True.
        Does NOT return first page as fallback if SPA has an index route.
        """
        # Check if index is explicitly defined in multipage
        if hasattr(self, '_index_page') and self._index_page and self._index_page in self._pages:
            return self._pages[self._index_page]
        
        # Look for a page with index=True
        for page in self._pages.values():
            if getattr(page, 'index', False):
                return page
        
        # Only return first page as fallback if there are NO SPA routes
        # If SPA routes exist, return None to avoid conflicts
        if hasattr(self, '_spa_routes') and self._spa_routes:
            return None
        
        # Fallback: return first page only if no SPA exists
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
    
    def has_spa_routes(self) -> bool:
        """Indicate if the app has any SPA routes."""
        return bool(self._spa_routes)
    
    def get_spa_index(self) -> Optional['SPARoute']:
        """Get the index SPA route if exists."""
        if self._spa_index_route and self._spa_index_route in self._spa_routes:
            return self._spa_routes[self._spa_index_route]
        return None
    
    def set_404_page(self, page: 'Page'):
        """
        Set custom 404 page for SPA routing.
        
        Args:
            page: Page instance to display when route not found
        
        Example:
            not_found_page = Page(Container(Text("404 - Page Not Found")))
            app.set_404_page(not_found_page)
        """
        self._spa_404_page = page
    
    def set_403_page(self, page: 'Page'):
        """
        Set custom 403 Forbidden page for SPA routing.
        
        Args:
            page: Page instance to display when access is forbidden
        
        Example:
            forbidden_page = Page(Container(Text("403 - Access Forbidden")))
            app.set_403_page(forbidden_page)
        """
        self._spa_403_page = page

    def set_loading_state(self, loadingComp: Any = None, onErrorComp: Any = None):
        """Set custom loading and error components for SSR lazy-load in SPA.

        This is rendered by exporters as static HTML (like 404/403 pages), and does
        not register states or events.
        """
        self._spa_loading_page = loadingComp
        self._spa_error_page = onErrorComp
        
    def add_script(self, script: 'Script'):
        """Adds a script to the app"""
        self.scripts.append(script)

    def useWatch(self, state_path: str, *js_helpers):
        """
        Watch a state property and execute callback when it changes.
        
        Usage with app.add_script():
            app.add_script(useWatch("user.name", log("Name changed!")))
        
        Usage with page.add_script():
            page.add_script(useWatch("user.name", log("Name changed!")))
            
        Usage with app.useWatch() (convenience):
            app.useWatch("user.name", log("Name changed!"))
            
        Usage with page.useWatch() (convenience):
            page.useWatch("user.name", log("Name changed!"))
        
        The returned WatchMarker has a get_code() method that generates the JavaScript.
        """
        from dars.hooks.use_watch import useWatch
        watcher = useWatch(state_path, *js_helpers)
        self.add_script(watcher)
        return self
        
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

        # Validación SPA, multipage y single-page
        if self.has_spa_routes():
            # SPA mode - validate SPA routes
            if not self._spa_routes:
                errors.append("The app has SPA routing enabled but there are no routes registered.")
            for name, spa_route in self._spa_routes.items():
                if not spa_route.root:
                    errors.append(f"The SPA route '{name}' hasn't a root component.")
                else:
                    errors.extend(self._validate_component(spa_route.root, path=f"spa_routes['{name}']"))
        elif self.is_multipage():
            # Traditional multipage mode
            if not self._pages:
                errors.append("The app is on multipage mode but there are no pages registered.")
            for name, page in self._pages.items():
                if not page.root:
                    errors.append(f"The page '{name}' hasn't a root component.")
                else:
                    errors.extend(self._validate_component(page.root, path=f"pages['{name}']"))
        else:
            # Single-page mode
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
    
    def delete(self, id: str) -> 'App':
        """Remove a component by id from the tree before export (compile-time)."""
        def _find_parent_and_index(node: Component, target_id: str):
            for idx, ch in enumerate(getattr(node, 'children', [])[:] ):
                if getattr(ch, 'id', None) == target_id:
                    return node, idx
                res = _find_parent_and_index(ch, target_id)
                if res:
                    return res
            return None

        if self.is_multipage():
            for name, page in self._pages.items():
                if not page.root:
                    continue
                res = _find_parent_and_index(page.root, id)
                if res:
                    parent, idx = res
                    child = parent.children.pop(idx)
                    try:
                        child.parent = None
                    except Exception:
                        pass
                    return self
            print(f"[Dars] Warning: component id '{id}' not found for deletion.")
            return self
        if not self.root:
            print("[Dars] Warning: no root component defined.")
            return self
        res = _find_parent_and_index(self.root, id)
        if res:
            parent, idx = res
            child = parent.children.pop(idx)
            try:
                child.parent = None
            except Exception:
                pass
            return self
        print(f"[Dars] Warning: component id '{id}' not found for deletion.")
        return self

    def create(self, target, root: Optional["Component"] = None, on_top_of=None, on_bottom_of=None) -> 'App':
        """Create/insert a component in the tree before export (compile-time)."""
        if on_top_of is not None and on_bottom_of is not None:
            raise ValueError("Provide only one of on_top_of or on_bottom_of")

        # Permitir target como callable, instancia o id (str) de un componente existente
        if isinstance(target, str):
            # Mover componente existente por id
            comp = self.find_component_by_id(target)
            if not comp:
                print(f"[Dars] Warning: target id '{target}' not found; create() skipped.")
                return self
            # Desanclar del padre anterior si existe
            try:
                if getattr(comp, 'parent', None) and comp in comp.parent.children:
                    comp.parent.children.remove(comp)
                    comp.parent = None
            except Exception:
                pass
        else:
            comp = target() if callable(target) and not isinstance(target, Component) else target
        if isinstance(comp, type) and issubclass(comp, Component):
            raise TypeError("A Component class was provided; pass an instance or a callable returning one.")
        if not isinstance(comp, Component):
            raise TypeError("target must be a Component instance or a callable returning one")

        def _resolve_root(root_arg):
            if root_arg is None:
                if self.is_multipage():
                    page = self.get_index_page()
                    return page.root if page else None
                return self.root
            if isinstance(root_arg, Component):
                return root_arg
            if isinstance(root_arg, str):
                # Priorizar id de componente sobre nombre de página
                found = self.find_component_by_id(root_arg)
                if found:
                    return found
                if root_arg in self._pages:
                    p = self._pages[root_arg]
                    return p.root
            return None

        root_comp = _resolve_root(root)
        if not root_comp:
            print("[Dars] Warning: invalid root for create(); operation skipped.")
            return self

        def _resolve_ref(ref):
            if ref is None:
                return None
            if isinstance(ref, Component):
                for i, ch in enumerate(root_comp.children):
                    if ch is ref:
                        return i
                return None
            if isinstance(ref, str):
                for i, ch in enumerate(root_comp.children):
                    if getattr(ch, 'id', None) == ref:
                        return i
                return None
            return None

        def _find_parent_and_index_in_subtree(node: Component, ref) -> Optional[tuple]:
            """Busca en profundidad la referencia y devuelve (parent, index) si la referencia es hijo de 'parent'."""
            for idx, ch in enumerate(getattr(node, 'children', [])[:] ):
                if (ref is ch) or (isinstance(ref, str) and getattr(ch, 'id', None) == ref):
                    return node, idx
                res = _find_parent_and_index_in_subtree(ch, ref)
                if res:
                    return res
            return None

        insert_idx = None
        if on_top_of is not None:
            idx = _resolve_ref(on_top_of)
            if idx is None:
                # Intentar localizar en el subárbol y ajustar root si es necesario
                res = _find_parent_and_index_in_subtree(root_comp, on_top_of)
                if res:
                    root_comp, idx = res
                    insert_idx = idx
                else:
                    print("[Dars] Warning: on_top_of reference not found; appending.")
                    insert_idx = None
            else:
                insert_idx = idx
        elif on_bottom_of is not None:
            idx = _resolve_ref(on_bottom_of)
            if idx is None:
                res = _find_parent_and_index_in_subtree(root_comp, on_bottom_of)
                if res:
                    root_comp, idx = res
                    insert_idx = idx + 1
                else:
                    print("[Dars] Warning: on_bottom_of reference not found; appending.")
                    insert_idx = None
            else:
                insert_idx = idx + 1

        comp.parent = root_comp
        if insert_idx is None or insert_idx >= len(root_comp.children):
            root_comp.children.append(comp)
        else:
            root_comp.children.insert(insert_idx, comp)
        return self
        
    def get_stats(self) -> Dict[str, Any]:
        """Return application stadistics (single-page and multipage)"""
        # Multipage mode (classic pages)
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

        # SPA / SSR mode (routes stored in _spa_routes)
        if self.has_spa_routes():
            total_components = 0
            max_depth = 0
            for spa_route in self._spa_routes.values():
                root = getattr(spa_route, 'root', None)
                if root:
                    total_components += self._count_components(root)
                    depth = self._calculate_max_depth(root)
                    max_depth = max(max_depth, depth)
            return {
                'total_components': total_components,
                'max_depth': max_depth,
                'scripts_count': len(self.scripts),
                'global_styles_count': len(self.global_styles),
                'total_pages': len(self._spa_routes) or 0,
            }

        # Single-page mode
        if self.root:
            return {
                'total_components': self._count_components(self.root),
                'max_depth': self._calculate_max_depth(self.root),
                'scripts_count': len(self.scripts),
                'global_styles_count': len(self.global_styles),
                'total_pages': 1
            }

        # No root defined
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

        if self.has_spa_routes():
            return max((self._calculate_max_depth(getattr(route, 'root', None))
                        for route in self._spa_routes.values() if getattr(route, 'root', None)), default=0)

        if self.root:
            return self._calculate_max_depth(self.root)

        return 0

    def _calculate_max_depth(self, component: Component, current_depth: int = 0) -> int:
        """Calculates the maximun depth of a component tree (internal use)"""
        if not component or not getattr(component, 'children', []):
            return current_depth
        return max(self._calculate_max_depth(child, current_depth + 1) for child in component.children)


