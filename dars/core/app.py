from typing import Optional, List, Dict, Any
from .component import Component
from .events import EventManager

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

    def rTimeCompile(self, exporter=None, port=None, add_file_types=None):
        """
        Generates a quick preview of the app on a local server using an exporter  
        (default: HTMLCSSJSExporter) and serving the files from a temporary directory.  
        Does not open the browser automatically. The server stops with Ctrl+C.  
        You can pass the port as a command-line argument: python main.py --port 8080  
        """
        import threading
        import time
        import sys
        import os
        import inspect
        import importlib.util
        from pathlib import Path
        from contextlib import contextmanager
        import shutil
        import traceback

        @contextmanager
        def pushd(path):
            """Cambia temporalmente el cwd y lo restaura al salir."""
            old = os.getcwd()
            os.chdir(path)
            try:
                yield
            finally:
                os.chdir(old)

        # Rich para mensajes bonitos
        try:
            from rich.console import Console
            from rich.panel import Panel
            from rich.text import Text
        except ImportError:
            Console = None
        console = Console() if 'Console' in locals() else None

        # Leer puerto de sys.argv si no se pasa explícito
        if port is None:
            port = 8000
            for i, arg in enumerate(sys.argv):
                if arg in ('--port', '-p') and i + 1 < len(sys.argv):
                    try:
                        port = int(sys.argv[i + 1])
                    except Exception:
                        pass
            # --- Normalizar add_file_types => lista de extensiones que empiezan con '.' ---
        def _normalize_exts(exts):
            if not exts:
                return ['.py']
            # aceptar string con comas
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
            # siempre incluir .py (comportamiento: .py + los adicionales)
            if '.py' not in normalized:
                normalized.insert(0, '.py')
            # eliminar duplicados preservando orden
            seen = set()
            result = []
            for e in normalized:
                if e not in seen:
                    seen.add(e)
                    result.append(e)
            return result

        # Lista final de extensiones a vigilar (ej: ['.py', '.js', '.css'])
        watch_exts = _normalize_exts(add_file_types)
               
        # Importar exportador por defecto si no se pasa
        if exporter is None:
            try:
                from dars.exporters.web.html_css_js import HTMLCSSJSExporter
            except ImportError:
                print("Could not import HTMLCSSJSExporter")
                return
            exporter = HTMLCSSJSExporter()

        # Importar PreviewServer
        try:
            from dars.cli.preview import PreviewServer
        except ImportError:
            print("Could not import PreviewServer")
            return

        shutdown_event = threading.Event()
        watchers = []  # aquí guardaremos todos los watchers

        # Debounce / lock para evitar reloads concurrentes
        reload_lock = threading.Lock()
        last_reload_at = 0.0
        MIN_RELOAD_INTERVAL = 0.4  # segundos

        try:
            # Detectar archivo principal de la app (el que ejecutaste con `python archivo.py`)
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

            preview_dir = os.path.join(project_root, "dars_preview")
            cwd_original = os.getcwd()

            # limpiar preview anterior
            if os.path.exists(preview_dir):
                try:
                    shutil.rmtree(preview_dir)
                except Exception as e:
                    msg = f"Warning: Could not clean previous preview directory: {e}"
                    console.print(f"[yellow]{msg}[/yellow]") if console else print(msg)

            os.makedirs(preview_dir, exist_ok=True)

            # export inicial desde el root usando la instancia actual (self)
            with pushd(project_root):
                exporter.export(self, preview_dir)

            url = f"http://localhost:{port}"
            app_title = getattr(self, 'title', 'Dars App')
            if console:
                panel = Panel(
                    Text(f"✔ App running successfully\n\nName: {app_title}\nPreview available at: {url}\n\nPress Ctrl+C to stop the server.",
                        style="bold green", justify="center"),
                    title="Dars Preview", border_style="cyan")
                console.print(panel)
            else:
                print(f"[Dars] App '{app_title}' running. Preview at {url}")

            server = PreviewServer(preview_dir, port)
            try:
                if not server.start():
                    (console.print("[red]Could not start preview server.[/red]")
                    if console else print("Could not start preview server."))
                    return

                # --- HOT RELOAD ---
                from dars.cli.hot_reload import FileWatcher

                def _collect_project_files_by_ext(root, exts):
                    files = []
                    for dirpath, dirnames, filenames in os.walk(root):
                        # excluir preview_dir, .git y __pycache__
                        if os.path.abspath(dirpath).startswith(os.path.abspath(preview_dir)):
                            continue
                        if '.git' in dirpath or '__pycache__' in dirpath:
                            continue
                        for fname in filenames:
                            for ext in exts:
                                if fname.lower().endswith(ext):
                                    files.append(os.path.join(dirpath, fname))
                                    break
                    return files


                def reload_and_export(changed_file=None):
                    nonlocal last_reload_at
                    now = time.time()
                    # debounce rápido
                    if now - last_reload_at < MIN_RELOAD_INTERVAL:
                        return
                    with reload_lock:
                        last_reload_at = time.time()
                        if console:
                            console.print(f"[yellow]Detected change in {changed_file}. Reloading...[/yellow]")
                        else:
                            print(f"[Dars] Detected change in {changed_file}. Reloading...")

                        try:
                            if project_root not in sys.path:
                                sys.path.insert(0, project_root)

                            with pushd(project_root):
                                # --- Limpiar del cache todos los módulos que pertenecen al proyecto ---
                                to_remove = []
                                for name, mod in list(sys.modules.items()):
                                    try:
                                        mod_file = getattr(mod, '__file__', None)
                                        if not mod_file:
                                            continue
                                        # normalizar paths
                                        mod_file_abs = os.path.abspath(mod_file)
                                        if mod_file_abs.startswith(os.path.abspath(project_root)):
                                            to_remove.append(name)
                                    except Exception:
                                        continue

                                for name in to_remove:
                                    try:
                                        del sys.modules[name]
                                    except Exception:
                                        pass

                                # también borrar cualquier nombre temporal 'dars_app' si existiese
                                sys.modules.pop("dars_app", None)

                                # Importar el archivo principal en un nombre único (para limpieza segura)
                                unique_name = f"dars_app_reload_{int(time.time()*1000)}"
                                spec = importlib.util.spec_from_file_location(unique_name, app_file)
                                module = importlib.util.module_from_spec(spec)
                                spec.loader.exec_module(module)

                                # Buscar nueva instancia App en el módulo recargado
                                new_app = None
                                for v in vars(module).values():
                                    try:
                                        if isinstance(v, App):
                                            new_app = v
                                            break
                                    except Exception:
                                        # si isinstance falla por alguna razón, ignorar
                                        pass

                                # fallback por nombre de clase (por si App es distinto objeto)
                                if not new_app:
                                    for v in vars(module).values():
                                        try:
                                            if hasattr(v, '__class__') and v.__class__.__name__ == 'App':
                                                new_app = v
                                                break
                                        except Exception:
                                            pass

                                if not new_app:
                                    (console.print("[red]No App instance found after reload.[/red]")
                                    if console else print("[Dars] No App instance found after reload."))
                                    return

                                # Exportar la nueva instancia
                                exporter.export(new_app, preview_dir)

                            (console.print("[green]App reloaded and re-exported successfully.[/green]")
                            if console else print("[Dars] App reloaded and re-exported successfully."))

                        except Exception as e:
                            tb = traceback.format_exc()
                            (console.print(f"[red]Hot reload failed: {e}\n{tb}[/red]")
                            if console else print(f"[Dars] Hot reload failed: {e}\n{tb}"))

                # --- Crear watchers para todos los archivos .py dentro del proyecto (recursivo) ---
                files_to_watch = _collect_project_files_by_ext(project_root, watch_exts)


                # Si no hay archivos detectados (raro), al menos mirar app_file
                if not files_to_watch:
                    files_to_watch = [app_file]

                for f in files_to_watch:
                    try:
                        # FileWatcher espera una función sin argumentos; usamos lambda que captura f
                        w = FileWatcher(f, lambda f=f: reload_and_export(f))
                        w.start()
                        watchers.append(w)
                    except Exception as e:
                        if console:
                            console.print(f"[yellow]Warning: could not watch {f}: {e}[/yellow]")
                        else:
                            print(f"[Dars] Warning: could not watch {f}: {e}")
                
                if console:
                    # Mostrar rutas relativas para que no sea tan largo
                    rel_paths = [os.path.relpath(f, project_root) for f in files_to_watch]
                    max_show = 80  # número máximo de líneas a mostrar
                    if len(rel_paths) > max_show:
                        shown = rel_paths[:max_show]
                        shown.append(f"... (+{len(rel_paths)-max_show} más)")
                    else:
                        shown = rel_paths or ["(ninguno)"]

                    from rich.table import Table
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
                else:
                    print(f"[Dars] Watching {len(files_to_watch)} files in {project_root}:")
                    for f in files_to_watch:
                        print("  -", os.path.relpath(f, project_root))

                # Loop principal: espera a Ctrl+C
                while not shutdown_event.is_set():
                    shutdown_event.wait(timeout=1)  # Espera sin consumir CPU

            except KeyboardInterrupt:
                shutdown_event.set()
                for w in watchers:
                    try:
                        w.stop()
                    except Exception:
                        pass
                (console.print("\n[cyan]Stopping preview and watcher...[/cyan]")
                if console else print("\n[Dars] Stopping preview and watcher..."))
            finally:
                # Detener watchers y servidor
                try:
                    server.stop()
                except Exception:
                    pass
                for w in watchers:
                    try:
                        w.stop()
                    except Exception:
                        pass
                (console.print("[green]Preview stopped.[/green]")
                if console else print("[Dars] Preview stopped."))

        except PermissionError as e:
            msg = f"Warning: Could not clean temp directory due to permissions: {e}"
            console.print(f"[yellow]{msg}[/yellow]") if console else print(msg)
        except Exception as e:
            msg = f"Unexpected error in fast preview: {e}\n{traceback.format_exc()}"
            console.print(f"[red]{msg}[/red]") if console else print(msg)
        finally:
            # Restaurar cwd y limpiar preview
            try:
                os.chdir(cwd_original)
            except Exception:
                pass
            try:
                shutil.rmtree(preview_dir)
                (console.print("[yellow]Preview files deleted.[/yellow]")
                if console else print("Preview files deleted."))
            except Exception as e:
                msg = f"Could not delete preview directory: {e}"
                console.print(f"[red]{msg}[/red]") if console else print(msg)

    
    def __init__(
        self, 
        title: str = "Dars App",
        description: str = "",
        author: str = "",
        keywords: List[str] = None,
        language: str = "en",
        favicon: str = "",
        icon: str = "",
        apple_touch_icon: str = "",
        manifest: str = "",
        theme_color: str = "#000000",
        background_color: str = "#ffffff",
        **config
    ):
        # Propiedades básicas de la aplicación
        self.title = title
        self.description = description
        self.author = author
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
        
    def add_global_style(self, selector: str, styles: Dict[str, Any]):
        """Adds a global style to the app"""
        self.global_styles[selector] = styles
        
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


