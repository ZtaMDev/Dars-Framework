from dars.components.basic.section import Section
from dars.exporters.base import Exporter
from dars.scripts.dscript import dScript
from dars.core.app import App
from dars.core.component import Component
from dars.components.basic.text import Text
from dars.components.basic.button import Button
from dars.components.basic.input import Input
from dars.components.basic.container import Container
from dars.components.basic.image import Image
from dars.components.basic.link import Link
from dars.components.basic.textarea import Textarea
from dars.components.basic.checkbox import Checkbox
from dars.components.basic.radiobutton import RadioButton
from dars.components.basic.select import Select
from dars.components.basic.slider import Slider
from dars.components.basic.datepicker import DatePicker
from dars.components.advanced.card import Card
from dars.components.advanced.modal import Modal
from dars.components.advanced.navbar import Navbar
from dars.components.advanced.table import Table
from dars.components.advanced.tabs import Tabs
from dars.components.advanced.accordion import Accordion
from dars.components.basic.progressbar import ProgressBar
from dars.components.basic.spinner import Spinner
from dars.components.basic.tooltip import Tooltip
from dars.components.basic.markdown import Markdown
from dars.components.basic.section import Section
from typing import Dict, Any
import os
from bs4 import BeautifulSoup
from dars.exporters.web.vdom import VDomBuilder
from dars.config import load_config, resolve_paths, copy_public_dir

class HTMLCSSJSExporter(Exporter):
    """Exportador para HTML, CSS y JavaScript"""
    
    def get_platform(self) -> str:
        return "html"
        
    def export(self, app: App, output_path: str, bundle: bool = False) -> bool:
        """Exporta la aplicación a HTML/CSS/JS (soporta multipágina)."""
        try:
            # Initialize watch scripts list for this export
            self._watch_scripts = []
            # Initialize obfuscation context for this export
            self._hash_ids = False
            self._id_hash_map = {}
            self._type_obfuscation = bool(bundle)
            self._type_map = {}
            self._type_seq = 0
            self.create_output_directory(output_path)

            # --- Copiar recursos adicionales desde la carpeta del proyecto ---
            import inspect, shutil
            import sys
            # Determinar la raíz del proyecto desde el archivo fuente de la app
            app_source = getattr(app, '__source__', None)
            if app_source is None and hasattr(app, 'source_file'):
                app_source = app.source_file
            if app_source is None:
                # Fallback: usar root del componente, pero esto no es robusto
                project_root = os.getcwd()
            else:
                project_root = os.path.dirname(os.path.abspath(app_source))

            # --- Escribir librería de reactividad (dars.min.js) embebida ---
            try:
                lib_dir = os.path.join(output_path, 'lib')
                os.makedirs(lib_dir, exist_ok=True)
                dest_js = os.path.join(lib_dir, 'dars.min.js')
                from dars.js_lib import DARS_MIN_JS
                with open(dest_js, 'w', encoding='utf-8') as f:
                    f.write(DARS_MIN_JS)
            except Exception:
                pass

            # --- Cargar configuración si existe y copiar public/assets ---
            try:
                cfg, cfg_found = load_config(project_root)
            except Exception:
                cfg, cfg_found = ({}, False)
            
            # Obtener configuración de viteMinify
            vite_minify = cfg.get('viteMinify', True) if cfg else True
            
            try:
                resolved = resolve_paths(cfg if cfg else {}, project_root)
            except Exception:
                resolved = {"public_abs": None, "include": [], "exclude": []}

            # Copiar public/assets completos al output
            try:
                public_abs = resolved.get("public_abs")
                include = cfg.get("include", []) if cfg else []
                exclude = cfg.get("exclude", []) if cfg else []
                if not public_abs:
                    # autodetect simple si no viene en config
                    cand_public = os.path.join(project_root, "public")
                    cand_assets = os.path.join(project_root, "assets")
                    if os.path.isdir(cand_public):
                        public_abs = cand_public
                    elif os.path.isdir(cand_assets):
                        public_abs = cand_assets
                if public_abs and os.path.isdir(public_abs):
                    copy_public_dir(public_abs, output_path, include=include, exclude=exclude)
            except Exception:
                # Mejor esfuerzo, no romper export
                pass

            os.makedirs(output_path, exist_ok=True)

            # Copiar solo recursos explícitos usados por la app
            # 1) Favicon
            favicon = getattr(app, 'favicon', None)
            if favicon and os.path.isfile(os.path.join(project_root, favicon)):
                shutil.copy2(os.path.join(project_root, favicon), os.path.join(output_path, os.path.basename(favicon)))
            # 2) Iconos PWA
            icons = getattr(app, 'icons', None)
            if icons:
                icons_dir = os.path.join(output_path, 'icons')
                os.makedirs(icons_dir, exist_ok=True)
                for icon in icons:
                    src = icon.get('src') if isinstance(icon, dict) else icon
                    if src and os.path.isfile(os.path.join(project_root, src)):
                        shutil.copy2(os.path.join(project_root, src), os.path.join(icons_dir, os.path.basename(src)))
            # 3) Service Worker
            sw_path = getattr(app, 'service_worker_path', None)
            if sw_path and os.path.isfile(os.path.join(project_root, sw_path)):
                shutil.copy2(os.path.join(project_root, sw_path), os.path.join(output_path, 'sw.js'))
            # 4) Archivos estáticos definidos por el usuario
            static_files = getattr(app, 'static_files', [])
            for static in static_files:
                src = static.get('src') if isinstance(static, dict) else static
                if src and os.path.isfile(os.path.join(project_root, src)):
                    shutil.copy2(os.path.join(project_root, src), os.path.join(output_path, os.path.basename(src)))

            base_css_content = self.generate_base_css()
            custom_css_content = self.generate_custom_css(app)

            self.write_file(os.path.join(output_path, "runtime_css.css"), base_css_content)
            self.write_file(os.path.join(output_path, "styles.css"), custom_css_content)

            # Verificar si debemos combinar archivos JS
            should_combine_js = bundle and vite_minify

            # SPA Routing: exportar SPA routes si existen (no retornar, permitir multipage también)
            if hasattr(app, "has_spa_routes") and app.has_spa_routes():
                self._export_spa(app, output_path, bundle, should_combine_js, project_root)
            
            # Multipágina: exportar un HTML, CSS y JS por cada página registrada
            if hasattr(app, "is_multipage") and app.is_multipage():
                import copy
                index_page = None
                if hasattr(app, 'get_index_page'):
                    index_page = app.get_index_page()
                
                # Check if SPA already has an index route
                spa_has_index = False
                if hasattr(app, "has_spa_routes") and app.has_spa_routes():
                    spa_has_index = app.get_spa_index() is not None
                
                # Exportar cada página
                for slug, page in app.pages.items():
                    # Track current page for per-page markdown highlight injection
                    self._current_page_id = slug
                    
                    # Si es la página index y ya tenemos SPA index, saltar exportación multipage para esta página
                    if index_page is not None and page is index_page and spa_has_index:
                        continue
                    
                    # Si la página tiene parent (es ruta SPA hija), saltar exportación multipage
                    if hasattr(page, 'parent') and page.parent:
                        continue
                        
                    page_app = copy.copy(app)
                    page_app.root = page.root
                    if page.title:
                        page_app.title = page.title
                    if page.meta:
                        for k, v in page.meta.items():
                            setattr(page_app, k, v)
                    
                    # Asegurar que root sea Container si es lista
                    from dars.components.basic.container import Container
                    if isinstance(page_app.root, list):
                        page_app.root = Container(children=page_app.root)
                    
                    # Generar VDOM y obtener eventos
                    page_events_map = {}
                    try:
                        vdom_builder = VDomBuilder(id_provider=self.get_component_id)
                        vdom_dict = vdom_builder.build(page_app.root)
                        page_events_map = vdom_builder.events_map
                        
                        if bundle:
                            vdom_dict = self._obfuscate_vdom(vdom_dict)
                        import json
                        vdom_js = "window.__DARS_VDOM__ = " + json.dumps(vdom_dict, ensure_ascii=False, separators=(",", ":")) + ";\n"
                    except Exception:
                        vdom_js = "window.__DARS_VDOM__ = { };\n"
                        page_events_map = {}
                    
                    # Collect bindings by traversing component tree (without rendering)
                    # This avoids breaking Markdown script injection and other side effects
                    self._collect_bindings_from_tree(page_app.root)
                    
                    # Generar runtime JS con eventos
                    runtime_js = self.generate_javascript(page_app, page.root, page_events_map)
                    
                    # Scripts específicos de esta página
                    page_scripts = []
                    
                    # Scripts globales de la app
                    page_scripts.extend(getattr(app, 'scripts', []))
                    
                    # Scripts específicos de esta página
                    if hasattr(page, 'scripts'):
                        page_scripts.extend(page.scripts)
                    
                    # Scripts de componentes dentro de la página
                    if hasattr(page_app.root, 'get_scripts'):
                        page_scripts.extend(page_app.root.get_scripts())

                    # Incluir scripts automáticos generados por helpers de escritorio
                    try:
                        import dars.desktop as _dars_desktop
                        auto = getattr(_dars_desktop, '_auto_scripts', None)
                        if auto:
                            page_scripts.extend(auto)
                    except Exception:
                        pass
                    
                    # Preparar scripts
                    combined_js, external_srcs, combined_is_module = self._prepare_page_scripts(page_scripts, output_path, project_root)

                    if should_combine_js:
                        # Combinar runtime + VDOM + scripts en un solo archivo
                        combined_all_js = f"""// Combined JavaScript for {slug}
    // VDOM
    {vdom_js}

    // Runtime
    {runtime_js}

    // Page Scripts
    {combined_js}
    """
                        app_js_filename = f"app_{slug}.js" if slug != "index" else "app.js"
                        self.write_file(os.path.join(output_path, app_js_filename), combined_all_js)
                        
                        # Generar HTML con solo el archivo combinado
                        # Solo usar index.html si es multipage index Y no hay SPA index
                        if index_page is not None and page is index_page and not spa_has_index:
                            html_content = self.generate_html(page_app, css_file="styles.css",
                                                            script_file=app_js_filename,
                                                            runtime_file="",  # Vacío porque está combinado
                                                            extra_script_srcs=external_srcs, 
                                                            bundle=bundle, 
                                                            vdom_script="",  # Vacío porque está combinado
                                                            script_is_module=combined_is_module,
                                                            combined_js=True)
                            filename = "index.html"
                        else:
                            html_content = self.generate_html(page_app, css_file="styles.css",
                                                            script_file=app_js_filename,
                                                            runtime_file="",  # Vacío porque está combinado
                                                            extra_script_srcs=external_srcs, 
                                                            bundle=bundle, 
                                                            vdom_script="",  # Vacío porque está combinado
                                                            script_is_module=combined_is_module,
                                                            combined_js=True)
                            filename = f"{slug}.html"
                    else:
                        # Comportamiento original: archivos separados
                        vdom_filename = f"vdom_tree_{slug}.js" if slug != "index" else "vdom_tree.js"
                        self.write_file(os.path.join(output_path, vdom_filename), vdom_js)
                        
                        runtime_filename = f"runtime_dars_{slug}.js" if slug != "index" else "runtime_dars.js"
                        self.write_file(os.path.join(output_path, runtime_filename), runtime_js)
                        
                        script_filename = f"script_{slug}.js" if slug != "index" else "script.js"
                        self.write_file(os.path.join(output_path, script_filename), combined_js)
                        
                        # Solo usar index.html si es multipage index Y no hay SPA index
                        if index_page is not None and page is index_page and not spa_has_index:
                            html_content = self.generate_html(page_app, css_file="styles.css",
                                                            script_file=script_filename,
                                                            runtime_file=runtime_filename,
                                                            extra_script_srcs=external_srcs, 
                                                            bundle=bundle, 
                                                            vdom_script=vdom_filename,
                                                            script_is_module=combined_is_module)
                            filename = "index.html"
                        else:
                            html_content = self.generate_html(page_app, css_file="styles.css",
                                                            script_file=script_filename,
                                                            runtime_file=runtime_filename,
                                                            extra_script_srcs=external_srcs, 
                                                            bundle=bundle, 
                                                            vdom_script=vdom_filename,
                                                            script_is_module=combined_is_module)
                            filename = f"{slug}.html"
                    
                    # Mejorar formato HTML
                    try:
                        soup = BeautifulSoup(html_content, "html.parser")
                        html_content = soup.prettify()
                    except ImportError:
                        pass
                    
                    self.write_file(os.path.join(output_path, filename), html_content)
                    
                    # Fase 2: snapshot/version por página (solo en dev, no bundle)
                    if not bundle:
                        try:
                            vdom_json = self.generate_vdom_snapshot(page_app.root)
                        except Exception:
                            vdom_json = '{}'
                        if slug != 'index':
                            snapshot_name = f"snapshot_{slug}.json"
                            version_name = f"version_{slug}.txt"
                        else:
                            snapshot_name = "snapshot.json"
                            version_name = "version.txt"
                        self.write_file(os.path.join(output_path, snapshot_name), vdom_json)
                        try:
                            import time
                            version_val = str(int(time.time()*1000))
                        except Exception:
                            version_val = "1"
                        self.write_file(os.path.join(output_path, version_name), version_val)
            elif not (hasattr(app, "has_spa_routes") and app.has_spa_routes()):
                # Single-page clásico (solo si NO hay SPA routes)
                # Generar VDOM y obtener eventos
                page_events_map = {}
                try:
                    vdom_builder = VDomBuilder(id_provider=self.get_component_id)
                    vdom_dict = vdom_builder.build(app.root)
                    page_events_map = vdom_builder.events_map
                    
                    if bundle:
                        vdom_dict = self._obfuscate_vdom(vdom_dict)
                    import json
                    vdom_js = "window.__DARS_VDOM__ = " + json.dumps(vdom_dict, ensure_ascii=False, separators=(",", ":")) + ";\n"
                except Exception:
                    vdom_js = "window.__DARS_VDOM__ = { };\n"
                    page_events_map = {}

                # Pre-render components to populate bindings (useDynamic, etc.)
                # This is critical so that _generate_reactive_bindings_js has data
                self.render_component(app.root)

                # Generar runtime JS con eventos
                runtime_js = self.generate_javascript(app, app.root, page_events_map)

                user_scripts = list(getattr(app, 'scripts', []))
                # Incluir scripts automáticos generados por helpers de escritorio
                try:
                    import dars.desktop as _dars_desktop
                    auto = getattr(_dars_desktop, '_auto_scripts', None)
                    if auto:
                        user_scripts.extend(auto)
                except Exception:
                    pass
                combined_js, external_srcs, combined_is_module = self._prepare_page_scripts(user_scripts, output_path, project_root)

                if should_combine_js:
                    # Combinar runtime + VDOM + scripts en un solo archivo
                    combined_all_js = f"""// Combined JavaScript for Single Page App
    // VDOM
    {vdom_js}

    // Runtime
    {runtime_js}

    // Page Scripts
    {combined_js}
    """
                    app_js_filename = "app.js"
                    self.write_file(os.path.join(output_path, app_js_filename), combined_all_js)
                    
                    html_content = self.generate_html(app, css_file="styles.css",
                                                    script_file=app_js_filename,
                                                    runtime_file="",  # Vacío porque está combinado
                                                    extra_script_srcs=external_srcs, 
                                                    bundle=bundle, 
                                                    vdom_script="",  # Vacío porque está combinado
                                                    script_is_module=combined_is_module,
                                                    combined_js=True)
                else:
                    # Comportamiento original: archivos separados
                    vdom_filename = "vdom_tree.js"
                    self.write_file(os.path.join(output_path, vdom_filename), vdom_js)

                    runtime_filename = "runtime_dars.js"
                    self.write_file(os.path.join(output_path, runtime_filename), runtime_js)
                    
                    script_filename = "script.js"
                    self.write_file(os.path.join(output_path, script_filename), combined_js)

                    html_content = self.generate_html(app, css_file="styles.css",
                                                    script_file=script_filename,
                                                    runtime_file=runtime_filename,
                                                    extra_script_srcs=external_srcs, 
                                                    bundle=bundle, 
                                                    vdom_script=vdom_filename,
                                                    script_is_module=combined_is_module)

                soup = BeautifulSoup(html_content, "html.parser")
                html_content = soup.prettify()
                
                self.write_file(os.path.join(output_path, "index.html"), html_content)
                
                # Fase 2: snapshot/version para single-page (solo en dev, no bundle)
                if not bundle:
                    try:
                        vdom_json = self.generate_vdom_snapshot(app.root)
                    except Exception:
                        vdom_json = '{}'
                    self.write_file(os.path.join(output_path, "snapshot.json"), vdom_json)
                    try:
                        import time
                        version_val = str(int(time.time()*1000))
                    except Exception:
                        version_val = "1"
                    self.write_file(os.path.join(output_path, "version.txt"), version_val)

            # Generar archivos PWA si está habilitado
            if getattr(app, 'pwa_enabled', False):
                self._generate_pwa_files(app, output_path)

            # Limpiar bootstrap de estado para evitar duplicados en siguientes exports
            try:
                from dars.core.state import STATE_BOOTSTRAP
                if isinstance(STATE_BOOTSTRAP, list):
                    STATE_BOOTSTRAP.clear()
            except Exception:
                pass

            # Limpiar scripts automáticos generados por dars.desktop helpers
            try:
                import dars.desktop as _dars_desktop
                auto = getattr(_dars_desktop, '_auto_scripts', None)
                if isinstance(auto, list):
                    auto.clear()
            except Exception:
                pass

            return True
        except Exception as e:
            print(f"Error at export time: {e}")
            return False

            
    def _generate_pwa_files(self, app: 'App', output_path: str) -> None:
        """Genera manifest.json, iconos y service worker para PWA"""
        import json, os
        # Manifest
        self._generate_manifest_json(app, output_path)
        # Iconos por defecto (placeholder, puedes mejorar esto)
        self._generate_default_icons(output_path)
        # Service worker
        sw_path = getattr(app, 'service_worker_path', None)
        sw_enabled = getattr(app, 'service_worker_enabled', True)
        if sw_enabled:
            if sw_path:
                # Copiar el personalizado
                import shutil
                shutil.copy(sw_path, os.path.join(output_path, 'sw.js'))
            else:
                self._generate_basic_service_worker(output_path)

    def _generate_manifest_json(self, app: 'App', output_path: str) -> None:
        import json, os, shutil
        manifest = {
            "name": getattr(app, 'pwa_name', getattr(app, 'title', 'Dars App')),
            "short_name": getattr(app, 'pwa_short_name', 'Dars'),
            "description": getattr(app, 'description', 'Aplicación web progresiva creada con Dars'),
            "start_url": ".",
            "display": getattr(app, 'pwa_display', 'standalone'),
            "background_color": getattr(app, 'background_color', '#ffffff'),
            "theme_color": getattr(app, 'theme_color', '#4a90e2'),
            "orientation": getattr(app, 'pwa_orientation', 'portrait')
        }
        icons = self._get_icons_manifest(app, output_path)
        if icons is not None:
            manifest["icons"] = icons
        manifest_path = os.path.join(output_path, "manifest.json")
        with open(manifest_path, 'w', encoding='utf-8') as f:
            json.dump(manifest, f, indent=2)

    def _get_icons_manifest(self, app: 'App', output_path: str) -> list:
        import os, shutil
        user_icons = getattr(app, 'icons', None)
        if user_icons is not None:
            # Si el usuario define icons=[] explícito, no ponemos icons
            if isinstance(user_icons, list) and len(user_icons) == 0:
                return None
            
            # Obtener project_root para rutas relativas
            app_source = getattr(app, '__source__', None)
            if app_source is None and hasattr(app, 'source_file'):
                app_source = app.source_file
            if app_source is None:
                project_root = os.getcwd()
            else:
                project_root = os.path.dirname(os.path.abspath(app_source))
            
            # Si el usuario define iconos personalizados
            icons_manifest = []
            icons_dir = os.path.join(output_path, "icons")
            os.makedirs(icons_dir, exist_ok=True)
            
            for icon in user_icons:
                if isinstance(icon, dict):
                    src = icon.get("src")
                    if src:
                        # Resolver ruta relativa a project_root
                        src_path = os.path.join(project_root, src) if not os.path.isabs(src) else src
                        if os.path.isfile(src_path):
                            # Copiamos el icono al output
                            dest_path = os.path.join(icons_dir, os.path.basename(src))
                            shutil.copy(src_path, dest_path)
                            icon_copy = icon.copy()  # No modificar el original
                            icon_copy["src"] = f"/icons/{os.path.basename(src)}"
                            icons_manifest.append(icon_copy)
                        else:
                            # Si no existe, usar la ruta tal cual (podría ser URL)
                            icons_manifest.append(icon)
                    else:
                        icons_manifest.append(icon)
                elif isinstance(icon, str):
                    # Si solo es una ruta, la copiamos y generamos el dict
                    src_path = os.path.join(project_root, icon) if not os.path.isabs(icon) else icon
                    if os.path.isfile(src_path):
                        dest_path = os.path.join(icons_dir, os.path.basename(icon))
                        shutil.copy(src_path, dest_path)
                        icons_manifest.append({
                            "src": f"icons/{os.path.basename(icon)}",
                            "sizes": "192x192",
                            "type": "image/png",
                            "purpose": "any maskable"
                        })
                    else:
                        # Si no existe, asumir que es URL
                        icons_manifest.append({
                            "src": icon,
                            "sizes": "192x192",
                            "type": "image/png"
                        })
            return icons_manifest if icons_manifest else None
        
        # Si no hay icons definidos, poner por defecto
        return [
            {
                "src": "icons/icon-192x192.png",
                "sizes": "192x192",
                "type": "image/png",
                "purpose": "any maskable"
            },
            {
                "src": "icons/icon-512x512.png",
                "sizes": "512x512",
                "type": "image/png"
            }
        ]

    def _generate_default_icons(self, output_path: str) -> None:
        import os, shutil
        # Ruta de los iconos PWA por defecto incluidos en el framework
        base_dir = os.path.dirname(os.path.abspath(__file__))
        default_icons_dir = os.path.join(base_dir, "icons", "pwa")
        icons_dir = os.path.join(output_path, "icons")
        os.makedirs(icons_dir, exist_ok=True)
        # Copiar icon-192x192.png y icon-512x512.png si existen
        for fname in ["icon-192x192.png", "icon-512x512.png"]:
            src = os.path.join(default_icons_dir, fname)
            dst = os.path.join(icons_dir, fname)
            if os.path.isfile(src):
                shutil.copy(src, dst)


    def _generate_basic_service_worker(self, output_path: str) -> None:
        sw_content = '''// Service Worker básico para Dars PWA
const CACHE_NAME = 'dars-pwa-cache-v1';
const urlsToCache = [
  '/',
  '/index.html',
  '/styles.css',
  '/script.js'
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        console.log('Cache abierto');
        return cache.addAll(urlsToCache);
      })
  );
});

self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request)
      .then(response => {
        if (response) {
          return response;
        }
        return fetch(event.request);
      })
  );
});
'''
        sw_path = os.path.join(output_path, "sw.js")
        with open(sw_path, 'w', encoding='utf-8') as f:
            f.write(sw_content)

    def _prepare_page_scripts(self, scripts, output_path: str, project_root: str):
        """
        Toma la lista mixta `scripts` y:
        - concatena todo el JS inline en un único string (combined_js)
        - copia los file scripts al output_path y devuelve la lista de src relativos (external_srcs)
        Compatibilidades:
        - objetos con get_code()
        - dicts {'type':'inline','code':...} o {'type':'file','path':...}
        - objetos con attribute 'path' o 'src' (se interpretan como file script)
        - strings -> treated as inline code
        """
        combined_lines = []
        external_srcs = []  # list of tuples (src, is_module)
        combined_is_module = False
        import shutil

        for script in scripts or []:
            # Instancia con get_code()
            try:
                if hasattr(script, 'get_code'):
                    code = script.get_code()
                    if code:
                        combined_lines.append(f"// Script: {getattr(script, '__class__', type(script)).__name__}\n{code.strip()}\n")
                        try:
                            if getattr(script, 'module', False):
                                combined_is_module = True
                        except Exception:
                            pass
                    continue
            except Exception:
                pass

            # Dict fallback
            if isinstance(script, dict):
                stype = script.get('type', '').lower()
                is_module = bool(script.get('module'))
                if stype == 'inline' or ('code' in script and not stype):
                    code = script.get('code') or script.get('value') or ''
                    if code:
                        combined_lines.append(f"// Inline dict script\n{code.strip()}\n")
                        if is_module:
                            combined_is_module = True
                    continue
                if stype == 'file' or 'path' in script:
                    path = script.get('path') or script.get('src') or script.get('value')
                    if path:
                        # Resolver ruta relativa a project_root
                        src_path = os.path.join(project_root, path) if not os.path.isabs(path) else path
                        if os.path.isfile(src_path):
                            dest_name = os.path.basename(src_path)
                            dest_path = os.path.join(output_path, dest_name)
                            try:
                                shutil.copy2(src_path, dest_path)
                                external_srcs.append((dest_name, is_module))
                            except Exception:
                                pass
                        else:
                            # si no existe en disco, asumimos que es una URL o ya accesible: usar tal cual
                            external_srcs.append((path, is_module))
                    continue
                # Otros dicts con code
                if 'code' in script:
                    code = script.get('code')
                    if code:
                        combined_lines.append(f"// Inline dict script\n{code.strip()}\n")
                        if is_module:
                            combined_is_module = True
                    continue

            # String -> inline code
            if isinstance(script, str):
                combined_lines.append(f"// Inline string script\n{script.strip()}\n")
                continue

            # Objetos con .path o .src (file scripts)
            path_attr = None
            for candidate in ('path', 'src', 'file'):
                if hasattr(script, candidate):
                    try:
                        path_attr = getattr(script, candidate)
                        break
                    except Exception:
                        continue
            if path_attr:
                path = path_attr
                src_path = os.path.join(project_root, path) if not os.path.isabs(path) else path
                if os.path.isfile(src_path):
                    dest_name = os.path.basename(src_path)
                    dest_path = os.path.join(output_path, dest_name)
                    try:
                        shutil.copy2(src_path, dest_path)
                        is_module = False
                        try:
                            if getattr(script, 'module', False):
                                is_module = True
                        except Exception:
                            pass
                        external_srcs.append((dest_name, is_module))
                    except Exception:
                        pass
                else:
                    is_module = False
                    try:
                        if getattr(script, 'module', False):
                            is_module = True
                    except Exception:
                        pass
                    external_srcs.append((path, is_module))
                continue

            # Si no sabemos qué es, intentar str() y añadir como inline (fallback)
            try:
                s = str(script)
                if s:
                    combined_lines.append(f"// Fallback script: {type(script).__name__}\n{s}\n")
            except Exception:
                pass

        combined_js = "// Scripts específicos de esta página (combinados)\n" + "\n".join(combined_lines)

        return combined_js, external_srcs, combined_is_module
    def _generate_combined_script_js(self, scripts):
        """Deprecated internal wrapper: usa _prepare_page_scripts sin copiar archivos.
           Conserva compatibilidad devolviendo solo el combined JS (sin external refs)."""
        combined_js, external_srcs = self._prepare_page_scripts(scripts, output_path=os.getcwd(), project_root=os.getcwd())
        return combined_js

    def generate_html(self, app: App, css_file: str = "styles.css", 
                 script_file: str = "script.js", runtime_file: str = "runtime_dars.js", 
                 extra_script_srcs: list = None, bundle: bool = False, 
                 vdom_script: str = "vdom_tree.js", script_is_module: bool = False,
                 combined_js: bool = False) -> str:
        """Genera el contenido HTML con todas las propiedades de la aplicación"""
        body_content = ""
        from dars.components.basic.container import Container
        root_component = app.root
        # Protección: si root es lista, envolver en Container correctamente
        if isinstance(root_component, list):
            root_component = Container(*root_component)
        if root_component:
            body_content = self.render_component(root_component)
        
        # Generar meta tags
        meta_tags_html = self._generate_meta_tags(app)
        
        # Generar links (favicon, manifest, etc.)
        links_html = self._generate_links(app)
        
        # Generar Open Graph tags
        og_tags_html = self._generate_open_graph_tags(app)
        
        # Generar Twitter Card tags
        twitter_tags_html = self._generate_twitter_tags(app)
        
        # Construir string de scripts externos (extra_script_srcs)
        extra_scripts_html = ""
        if extra_script_srcs:
            for item in extra_script_srcs:
                # item can be string (backward compat) or tuple (src, is_module)
                if isinstance(item, tuple):
                    src, is_module = item
                else:
                    src, is_module = item, False
                type_attr = ' type="module"' if is_module else ''
                extra_scripts_html += f'    <script src="{src}"{type_attr}></script>\n'
        
        # Incluir dars.min.js (ESM) antes de runtime/script
        dars_lib_tag = '<script type="module" src="lib/dars.min.js" defer data-dars-lib></script>'

        # State bootstrap: emit JSON (+ obfuscation in bundle) + module to register states
        bootstrap_json_tag = ""
        bootstrap_init_tag = ""
        try:
            from dars.core.state import STATE_BOOTSTRAP
            if STATE_BOOTSTRAP:
                import json as _json
                from copy import deepcopy as _deepcopy
                try:
                    from dars.scripts.script import Script as _Script
                except Exception:
                    _Script = None

                def _ser(v):
                    try:
                        if _Script and isinstance(v, _Script):
                            return {"code": v.get_code()}
                        if isinstance(v, dict):
                            return {k: _ser(val) for k, val in v.items()}
                        if isinstance(v, list):
                            return [_ser(x) for x in v]
                        return v
                    except Exception:
                        return v

                _clean = _ser(_deepcopy(STATE_BOOTSTRAP))
                bootstrap_json = _json.dumps(_clean, ensure_ascii=False)
                if bundle:
                    # Obfuscate: base64-encode the bootstrap JSON
                    import base64 as _b64
                    _b64data = _b64.b64encode(bootstrap_json.encode('utf-8')).decode('ascii')
                    bootstrap_json_tag = f'<script type="application/octet-stream" id="dars-state-bootstrap-b64">{_b64data}</script>'
                    bootstrap_init_tag = (
                        "<script type=\"module\">\n"
                        "(async () => {\n"
                        "  if (window.__DARS_STATE_BOOTSTRAPPED__) return;\n"
                        "  const el = document.getElementById('dars-state-bootstrap-b64');\n"
                        "  if (!el) { window.__DARS_STATE_BOOTSTRAPPED__ = true; return; }\n"
                        "  let arr = [];\n"
                        "  try {\n"
                        "    const b64 = el.textContent || '';\n"
                        "    let json = '';\n"
                        "    if (typeof atob === 'function') json = atob(b64);\n"
                        "    else if (typeof Buffer !== 'undefined') json = Buffer.from(b64, 'base64').toString('utf8');\n"
                        "    arr = JSON.parse(json||'[]');\n"
                        "  } catch(_) { arr = []; }\n"
                        "  try {\n"
                        "    const m = await import('/lib/dars.min.js');\n"
                        "    const reg = m.registerState || (m.default && m.default.registerState);\n"
                        "    if (typeof reg === 'function') { arr.forEach(s => reg(s.name, s)); }\n"
                        "  } catch (e) {\n"
                        "    const D = window.Dars; if (D && typeof D.registerState==='function') { arr.forEach(s => D.registerState(s.name, s)); }\n"
                        "  }\n"
                        "  window.__DARS_STATE_BOOTSTRAPPED__ = true;\n"
                        "})();\n"
                        "</script>"
                    )
                else:
                    # Dev: keep readable JSON
                    bootstrap_json_tag = f'<script type="application/json" id="dars-state-bootstrap">{bootstrap_json}</script>'
                    bootstrap_init_tag = (
                        "<script type=\"module\">\n"
                        "(async () => {\n"
                        "  if (window.__DARS_STATE_BOOTSTRAPPED__) return;\n"
                        "  const el = document.getElementById('dars-state-bootstrap');\n"
                        "  if (!el) { window.__DARS_STATE_BOOTSTRAPPED__ = true; return; }\n"
                        "  const arr = JSON.parse(el.textContent||'[]');\n"
                        "  try {\n"
                        "    const m = await import('/lib/dars.min.js');\n"
                        "    const reg = m.registerState || (m.default && m.default.registerState);\n"
                        "    if (typeof reg === 'function') { arr.forEach(s => reg(s.name, s)); }\n"
                        "  } catch (e) {\n"
                        "    const D = window.Dars; if (D && typeof D.registerState==='function') { arr.forEach(s => D.registerState(s.name, s)); }\n"
                        "  }\n"
                        "  window.__DARS_STATE_BOOTSTRAPPED__ = true;\n"
                        "})();\n"
                        "</script>"
                    )
        except Exception:
            pass

        # Derivar nombres para hot-reload incremental (opcional)
        def _derive_snapshot_and_version(runtime_name: str):
            if runtime_name == 'runtime_dars.js':
                return ('snapshot.json', 'version.txt')
            if runtime_name.startswith('runtime_dars_') and runtime_name.endswith('.js'):
                slug = runtime_name[len('runtime_dars_'):-3]
                return (f'snapshot_{slug}.json', f'version_{slug}.txt')
            return ('snapshot.json', 'version.txt')

        snapshot_name, version_name = _derive_snapshot_and_version(runtime_file)
        # Incluir variables de hot-reload solo en modo dev (no bundle)
        version_vars_html = ""
        if not bundle:
            version_vars_html = f"<script>window.__DARS_SNAPSHOT_URL = '{snapshot_name}'; window.__DARS_VERSION_URL = '{version_name}';</script>"

        # NUEVO: Manejar archivos combinados vs separados
        if combined_js:
            # Cuando está combinado, solo necesitamos el script_file principal
            main_script_tag = f'<script src="{script_file}"{" type=\"module\"" if script_is_module else ""} defer></script>'
            vdom_script_tag = ''
            runtime_script_tag = ''
        else:
            # Comportamiento original: archivos separados
            vdom_script_tag = f'<script src="{vdom_script}"></script>' if vdom_script else ''
            runtime_script_tag = f'<script src="{runtime_file}"{" type=\"module\"" if script_is_module else ""} defer></script>' if runtime_file else ''
            main_script_tag = f'<script src="{script_file}"{" type=\"module\"" if script_is_module else ""}></script>' if script_file else ''

        html_template = f"""<!DOCTYPE html>
    <html lang="{app.language}">
    <head>
        <meta charset="{app.config.get('charset', 'UTF-8')}">
        {meta_tags_html}
        <title>{app.title}</title>
        {links_html}
        {og_tags_html}
        {twitter_tags_html}
    <link rel=\"stylesheet\" href=\"runtime_css.css\">\n    <link rel=\"stylesheet\" href=\"{css_file}\">
    </head>
    <body>
        {body_content}
        {vdom_script_tag}
        {version_vars_html}
        {dars_lib_tag}
        {runtime_script_tag}
    {extra_scripts_html}    {main_script_tag}
    </body>
    </html>"""

        return html_template

    def _obfuscate_vdom(self, vnode: dict) -> dict:
        """Produce un VDOM mínimo SIN eventos"""
        if not isinstance(vnode, dict):
            return vnode
        
        kept = {}
        # type (obfuscated when enabled)
        t = vnode.get('type')
        if t is not None:
            kept['type'] = self._obf_type(t) if getattr(self, '_type_obfuscation', False) else t
        # id and key
        if 'id' in vnode and vnode['id']:
            kept['id'] = self._hash_id(str(vnode['id'])) if getattr(self, '_hash_ids', False) else vnode['id']
        if 'key' in vnode and vnode['key']:
            kept['key'] = str(vnode['key'])
        # class: drop in obfuscated VDOM to avoid leaking names
        if not getattr(self, '_type_obfuscation', False):
            if 'class' in vnode:
                kept['class'] = vnode.get('class')
        # text retained
        if 'text' in vnode:
            kept['text'] = vnode.get('text')
        
        
        # Recurse children
        ch = vnode.get('children') or []
        if ch:
            kept['children'] = [self._obfuscate_vdom(c) for c in ch]
        return kept

    def _obf_type(self, name: str) -> str:
        m = getattr(self, '_type_map', None)
        if m is None:
            self._type_map = {}
            self._type_seq = 0
            m = self._type_map
        if name in m:
            return m[name]
        self._type_seq += 1
        obf = f"T{self._type_seq}"
        m[name] = obf
        return obf

    def generate_custom_css(self, app: App) -> str:
        """Genera solo los estilos personalizados de la aplicación"""
        css_content = ""
        
        # Generar estilos hover PRIMERO para que tengan prioridad
        css_content += self._generate_hover_styles(app)
        css_content += self._generate_active_styles(app)
        
        # Agregar estilos globales de la aplicación definidos por el usuario
        for selector, styles in app.global_styles.items():
            css_content += f"{selector} {{\n"
            css_content += f"    {self.render_styles(styles)}\n"
            css_content += "}\n\n"

        # Agregar contenido de archivos CSS globales
        for file_path in app.global_style_files:
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    css_content += f.read() + "\n\n"
            except Exception as e:
                print(f"[Dars] Warning: could not read CSS file '{file_path}': {e}")
                    
        return css_content

    def _generate_hover_styles(self, app: App) -> str:
        """Genera estilos CSS para hover_style de todos los componentes con mayor especificidad"""
        hover_css = ""
        
        def process_component(component):
            nonlocal hover_css
            # Verificar si el componente tiene hover_style y no está vacío
            if hasattr(component, 'hover_style') and component.hover_style:
                comp_id = self.get_component_id(component)
                if comp_id and component.hover_style:
                    styles_str = self.render_styles(component.hover_style)
                    if styles_str and styles_str.strip():
                        # Aumentar la especificidad usando !important
                        important_styles = []
                        for style_line in styles_str.split(';'):
                            if style_line.strip():
                                important_styles.append(f"{style_line.strip()} !important")
                        
                        important_styles_str = ";\n    ".join(important_styles)
                        
                        hover_css += f"#{comp_id}:hover {{\n"
                        hover_css += f"    {important_styles_str};\n"
                        hover_css += "}\n\n"
            
            # Procesar hijos recursivamente
            for child in getattr(component, 'children', []):
                process_component(child)
        
        # Procesar todos los componentes en la aplicación
        if app.is_multipage():
            for page in app.pages.values():
                if page.root:
                    process_component(page.root)
        elif app.root:
            process_component(app.root)
        
        return hover_css
    
    def _generate_active_styles(self, app: App) -> str:
        """Genera estilos CSS para active_style de todos los componentes con mayor especificidad"""
        active_css = ""
        
        def process_component(component):
            nonlocal active_css
            # Verificar si el componente tiene active_style y no está vacío
            if hasattr(component, 'active_style') and component.active_style:
                comp_id = self.get_component_id(component)
                if comp_id and component.active_style:
                    styles_str = self.render_styles(component.active_style)
                    if styles_str and styles_str.strip():
                        # Aumentar la especificidad usando !important
                        important_styles = []
                        for style_line in styles_str.split(';'):
                            if style_line.strip():
                                important_styles.append(f"{style_line.strip()} !important")
                        
                        important_styles_str = ";\n    ".join(important_styles)
                        
                        active_css += f"#{comp_id}:active {{\n"
                        active_css += f"    {important_styles_str};\n"
                        active_css += "}\n\n"
            
            # Procesar hijos recursivamente
            for child in getattr(component, 'children', []):
                process_component(child)
        
        # Procesar todos los componentes en la aplicación
        if app.is_multipage():
            for page in app.pages.values():
                if page.root:
                    process_component(page.root)
        elif app.root:
            process_component(app.root)
        
        return active_css

    def render_styles(self, styles: Dict[str, Any]) -> str:
        """Convierte un diccionario de estilos a string CSS"""
        if not styles:
            return ""
        
        css_lines = []
        for prop, value in styles.items():
            # Convertir nombres de propiedades de Python a CSS
            css_prop = prop.replace('_', '-')
            
            # Manejar valores especiales
            if value is None:
                continue
                
            # Si el valor es un diccionario, podría ser una regla anidada (como en media queries)
            if isinstance(value, dict):
                # Por ahora, ignoramos reglas anidadas en hover_style
                continue
                
            css_lines.append(f"{css_prop}: {value};")
        
        return "\n    ".join(css_lines)

    
    def _generate_meta_tags(self, app: App) -> str:
        """Genera todos los meta tags de la aplicación"""
        meta_tags = app.get_meta_tags()
        meta_html = []
        
        for name, content in meta_tags.items():
            if content:
                meta_html.append(f'    <meta name="{name}" content="{content}">')
        
        # Apple Mobile Web App meta tags
        if hasattr(app, 'apple_mobile_web_app_capable') and app.apple_mobile_web_app_capable:
            # Modern standard meta tag (prevents deprecation warning)
            meta_html.append('    <meta name="mobile-web-app-capable" content="yes">')
            # Apple-specific meta tag (for older iOS compatibility)
            meta_html.append('    <meta name="apple-mobile-web-app-capable" content="yes">')
        
        if hasattr(app, 'apple_mobile_web_app_status_bar_style') and app.apple_mobile_web_app_status_bar_style:
            style = app.apple_mobile_web_app_status_bar_style
            # Validate style value
            if style in ['default', 'black', 'black-translucent']:
                meta_html.append(f'    <meta name="apple-mobile-web-app-status-bar-style" content="{style}">')
        
        if hasattr(app, 'apple_mobile_web_app_title') and app.apple_mobile_web_app_title:
            meta_html.append(f'    <meta name="apple-mobile-web-app-title" content="{app.apple_mobile_web_app_title}">')
        
        # Enhanced theme-color for Safari 15+ (with media queries for light/dark mode)
        if hasattr(app, 'theme_color') and app.theme_color:
            # Standard theme-color
            meta_html.append(f'    <meta name="theme-color" content="{app.theme_color}">')
            # Safari 15+ with prefers-color-scheme support
            meta_html.append(f'    <meta name="theme-color" media="(prefers-color-scheme: light)" content="{app.theme_color}">')
            meta_html.append(f'    <meta name="theme-color" media="(prefers-color-scheme: dark)" content="{app.theme_color}">')
        
        # Añadir canonical URL si está configurado
        if app.canonical_url:
            meta_html.append(f'    <link rel="canonical" href="{app.canonical_url}">')
        
        return '\n'.join(meta_html)
    
    def _detect_icon_mime_type(self, icon_path: str) -> str:
        """Detect MIME type for icon based on file extension"""
        import os
        ext = os.path.splitext(icon_path)[1].lower()
        mime_types = {
            '.png': 'image/png',
            '.ico': 'image/x-icon',
            '.svg': 'image/svg+xml',
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.webp': 'image/webp',
            '.gif': 'image/gif'
        }
        return mime_types.get(ext, 'image/x-icon')  # Default fallback
    
    def _generate_links(self, app: App) -> str:
        """Genera los enlaces en el head del HTML"""
        links = []
        
        # Favicon - with automatic MIME type detection
        if hasattr(app, 'favicon') and app.favicon:
            mime_type = self._detect_icon_mime_type(app.favicon)
            links.append(f'<link rel="icon" href="{app.favicon}" type="{mime_type}">')
        
        # Icon (for PWA) - with automatic MIME type detection
        if hasattr(app, 'icon') and app.icon:
            mime_type = self._detect_icon_mime_type(app.icon)
            links.append(f'<link rel="icon" href="{app.icon}" type="{mime_type}">')
        
        # Apple Touch Icon - with multiple sizes for better iOS support
        if hasattr(app, 'apple_touch_icon') and app.apple_touch_icon:
            links.append(f'<link rel="apple-touch-icon" href="{app.apple_touch_icon}">')
            links.append(f'<link rel="apple-touch-icon" sizes="180x180" href="{app.apple_touch_icon}">')
        
        # Manifest
        if getattr(app, 'pwa_enabled', False):
            links.append('<link rel="manifest" href="manifest.json">')
            # Registrar service worker si está habilitado
            if getattr(app, 'service_worker_enabled', True):
                links.append("""
<script>
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        navigator.serviceWorker.register('sw.js')
            .then(registration => {
                console.log('ServiceWorker registration successful');
            })
            .catch(err => {
                console.log('ServiceWorker registration failed: ', err);
            });
    });
}
</script>
""")
        return "\n    ".join(links)

    def _generate_open_graph_tags(self, app: App) -> str:
        """Genera todos los tags Open Graph para redes sociales"""
        og_tags = app.get_open_graph_tags()
        og_html = []
        
        for property_name, content in og_tags.items():
            if content:
                og_html.append(f'    <meta property="{property_name}" content="{content}">')
        
        return '\n'.join(og_html)
    
    def _generate_twitter_tags(self, app: App) -> str:
        """Genera todos los tags de Twitter Card"""
        twitter_tags = app.get_twitter_tags()
        twitter_html = []
        
        for name, content in twitter_tags.items():
            if content:
                twitter_html.append(f'    <meta name="{name}" content="{content}">')
        
        return '\n'.join(twitter_html)
        
    def generate_base_css(self) -> str:
        """Genera el contenido CSS base con variables y estilos modernos."""
        base_css = """/* Dars Framework Base Styles */
:root {
    /* Colors */
    --dars-primary: #007bff;
    --dars-primary-hover: #0056b3;
    --dars-secondary: #6c757d;
    --dars-success: #28a745;
    --dars-danger: #dc3545;
    --dars-warning: #ffc107;
    --dars-info: #17a2b8;
    --dars-light: #f8f9fa;
    --dars-dark: #343a40;
    --dars-white: #ffffff;
    
    /* Text */
    --dars-text-color: #212529;
    --dars-text-muted: #6c757d;
    --dars-font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    
    /* Borders & Spacing */
    --dars-border-color: #dee2e6;
    --dars-border-radius: 0.25rem;
    --dars-border-radius-lg: 0.5rem;
    --dars-spacing-xs: 0.25rem;
    --dars-spacing-sm: 0.5rem;
    --dars-spacing-md: 1rem;
    --dars-spacing-lg: 1.5rem;
    
    /* Shadows */
    --dars-shadow-sm: 0 .125rem .25rem rgba(0,0,0,.075);
    --dars-shadow: 0 .5rem 1rem rgba(0,0,0,.15);
}

* {
    box-sizing: border-box;
}

body {
    margin: 0;
    padding: 0;
    font-family: var(--dars-font-family);
    color: var(--dars-text-color);
    background-color: var(--dars-white);
    line-height: 1.5;
}

/* --- Components --- */

/* Container */
.dars-container {
    /* Default is block, no need to specify unless overriding */
}

/* Text */
.dars-text {
    /* Allow natural flow (inline inside block, etc.) */
    margin: 0;
}

/* Button */
.dars-button {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    font-weight: 400;
    text-align: center;
    vertical-align: middle;
    user-select: none;
    background-color: var(--dars-light);
    border: 1px solid var(--dars-border-color);
    padding: 0.375rem 0.75rem;
    font-size: 1rem;
    line-height: 1.5;
    border-radius: var(--dars-border-radius);
    color: var(--dars-text-color);
    cursor: pointer;
    transition: color 0.15s ease-in-out, background-color 0.15s ease-in-out, border-color 0.15s ease-in-out, box-shadow 0.15s ease-in-out;
}

.dars-button:hover {
    background-color: #e2e6ea;
    border-color: #dae0e5;
}

.dars-button:focus {
    outline: 0;
    box-shadow: 0 0 0 0.2rem rgba(0, 123, 255, 0.25);
}

.dars-button:disabled {
    opacity: 0.65;
    cursor: not-allowed;
}

/* Input */
.dars-input {
    display: block;
    width: 100%;
    padding: 0.375rem 0.75rem;
    font-size: 1rem;
    font-weight: 400;
    line-height: 1.5;
    color: var(--dars-text-color);
    background-color: var(--dars-white);
    background-clip: padding-box;
    border: 1px solid var(--dars-border-color);
    border-radius: var(--dars-border-radius);
    transition: border-color 0.15s ease-in-out, box-shadow 0.15s ease-in-out;
}

.dars-input:focus {
    color: var(--dars-text-color);
    background-color: var(--dars-white);
    border-color: #80bdff;
    outline: 0;
    box-shadow: 0 0 0 0.2rem rgba(0, 123, 255, 0.25);
}

/* Textarea */
.dars-textarea {
    display: block;
    width: 100%;
    padding: 0.375rem 0.75rem;
    font-size: 1rem;
    font-weight: 400;
    line-height: 1.5;
    color: var(--dars-text-color);
    background-color: var(--dars-white);
    background-clip: padding-box;
    border: 1px solid var(--dars-border-color);
    border-radius: var(--dars-border-radius);
    transition: border-color 0.15s ease-in-out, box-shadow 0.15s ease-in-out;
    resize: vertical;
}

.dars-textarea:focus {
    border-color: #80bdff;
    outline: 0;
    box-shadow: 0 0 0 0.2rem rgba(0, 123, 255, 0.25);
}

/* Image */
.dars-image {
    max-width: 100%;
    height: auto;
    vertical-align: middle;
}

/* Link */
.dars-link {
    color: var(--dars-primary);
    text-decoration: none;
    background-color: transparent;
}

.dars-link:hover {
    color: var(--dars-primary-hover);
    text-decoration: underline;
}

/* Card */
.dars-card {
    position: relative;
    display: flex;
    flex-direction: column;
    min-width: 0;
    word-wrap: break-word;
    background-color: var(--dars-white);
    background-clip: border-box;
    border: 1px solid rgba(0,0,0,.125);
    border-radius: var(--dars-border-radius-lg);
    padding: var(--dars-spacing-lg);
    box-shadow: var(--dars-shadow-sm);
    margin-bottom: var(--dars-spacing-md);
}

.dars-card h2 {
    margin-top: 0;
    margin-bottom: var(--dars-spacing-md);
    font-size: 1.5rem;
    font-weight: 500;
}

/* Table */
.dars-table {
    width: 100%;
    margin-bottom: 1rem;
    color: var(--dars-text-color);
    border-collapse: collapse;
}

.dars-table th,
.dars-table td {
    padding: 0.75rem;
    vertical-align: top;
    border-top: 1px solid var(--dars-border-color);
    text-align: left;
}

.dars-table thead th {
    vertical-align: bottom;
    border-bottom: 2px solid var(--dars-border-color);
    background-color: var(--dars-light);
    font-weight: 600;
}

.dars-table tbody + tbody {
    border-top: 2px solid var(--dars-border-color);
}

/* Tabs */
.dars-tabs {
    margin-bottom: var(--dars-spacing-md);
}

.dars-tabs-header {
    display: flex;
    flex-wrap: wrap;
    padding-left: 0;
    margin-bottom: 0;
    list-style: none;
    border-bottom: 1px solid var(--dars-border-color);
}

.dars-tab {
    display: block;
    padding: 0.5rem 1rem;
    text-decoration: none;
    background: none;
    border: 1px solid transparent;
    border-top-left-radius: var(--dars-border-radius);
    border-top-right-radius: var(--dars-border-radius);
    cursor: pointer;
    margin-bottom: -1px;
    color: var(--dars-primary);
    transition: color 0.15s ease-in-out, background-color 0.15s ease-in-out, border-color 0.15s ease-in-out;
}

.dars-tab:hover {
    border-color: #e9ecef #e9ecef #dee2e6;
    color: var(--dars-primary-hover);
}

.dars-tab-active {
    color: var(--dars-text-color);
    background-color: var(--dars-white);
    border-color: var(--dars-border-color) var(--dars-border-color) var(--dars-white);
    cursor: default;
}

.dars-tab-panel {
    display: none;
    padding: var(--dars-spacing-md) 0;
}

.dars-tab-panel-active {
    display: block;
}

/* Accordion */
.dars-accordion {
    border: 1px solid rgba(0,0,0,.125);
    border-radius: var(--dars-border-radius);
    overflow: hidden;
}

.dars-accordion-section {
    border-bottom: 1px solid rgba(0,0,0,.125);
}

.dars-accordion-section:last-child {
    border-bottom: 0;
}

.dars-accordion-title {
    position: relative;
    display: block;
    padding: 0.75rem 1.25rem;
    margin-bottom: 0;
    background-color: var(--dars-white);
    border: 0;
    width: 100%;
    text-align: left;
    cursor: pointer;
    font-weight: 500;
    transition: background-color 0.15s ease;
}

.dars-accordion-title:hover {
    background-color: var(--dars-light);
}

.dars-accordion-content {
    display: none;
    padding: 1.25rem;
    background-color: var(--dars-white);
    border-top: 1px solid rgba(0,0,0,.125);
}

.dars-accordion-section.dars-accordion-open .dars-accordion-content {
    display: block;
}

/* Modal */
.dars-modal {
    position: fixed;
    top: 0;
    left: 0;
    z-index: 1050;
    display: none;
    width: 100%;
    height: 100%;
    overflow: hidden;
    outline: 0;
    background-color: rgba(0,0,0,0.5);
    justify-content: center;
    align-items: center;
}

.dars-modal:not(.dars-modal-hidden) {
    display: flex;
}

.dars-modal-content {
    position: relative;
    display: flex;
    flex-direction: column;
    width: 100%;
    max-width: 500px;
    pointer-events: auto;
    background-color: var(--dars-white);
    background-clip: padding-box;
    border: 1px solid rgba(0,0,0,.2);
    border-radius: var(--dars-border-radius-lg);
    outline: 0;
    box-shadow: var(--dars-shadow);
    margin: 1.75rem auto;
}

/* ProgressBar */
.dars-progressbar {
    display: flex;
    height: 1rem;
    overflow: hidden;
    line-height: 0;
    font-size: 0.75rem;
    background-color: #e9ecef;
    border-radius: var(--dars-border-radius);
    margin-bottom: var(--dars-spacing-md);
}

.dars-progressbar-bar {
    display: flex;
    flex-direction: column;
    justify-content: center;
    overflow: hidden;
    color: var(--dars-white);
    text-align: center;
    white-space: nowrap;
    background-color: var(--dars-primary);
    transition: width 0.6s ease;
}

/* Spinner */
.dars-spinner {
    display: inline-block;
    width: 2rem;
    height: 2rem;
    vertical-align: text-bottom;
    border: 0.25em solid currentColor;
    border-right-color: transparent;
    border-radius: 50%;
    animation: dars-spinner-border .75s linear infinite;
    color: var(--dars-primary);
}

@keyframes dars-spinner-border {
    100% { transform: rotate(360deg); }
}

/* Tooltip */
.dars-tooltip {
    position: relative;
    display: inline-block;
}

.dars-tooltip .dars-tooltip-text {
    visibility: hidden;
    background-color: black;
    color: #fff;
    text-align: center;
    border-radius: 6px;
    padding: 5px 10px;
    position: absolute;
    z-index: 1;
    opacity: 0;
    transition: opacity 0.3s;
    font-size: 0.875rem;
    white-space: nowrap;
}

.dars-tooltip:hover .dars-tooltip-text {
    visibility: visible;
    opacity: 1;
}

.dars-tooltip-top .dars-tooltip-text {
    bottom: 125%;
    left: 50%;
    transform: translateX(-50%);
}

.dars-tooltip-bottom .dars-tooltip-text {
    top: 125%;
    left: 50%;
    transform: translateX(-50%);
}

.dars-tooltip-left .dars-tooltip-text {
    top: 50%;
    right: 105%;
    transform: translateY(-50%);
}

.dars-tooltip-right .dars-tooltip-text {
    top: 50%;
    left: 105%;
    transform: translateY(-50%);
}

/* Navbar */
.dars-navbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: var(--dars-spacing-md);
    background-color: var(--dars-white);
    border-bottom: 1px solid var(--dars-border-color);
    box-shadow: var(--dars-shadow-sm);
}

.dars-navbar-brand {
    font-weight: 600;
    font-size: 1.25rem;
    color: var(--dars-text-color);
    text-decoration: none;
}

.dars-navbar-nav {
    display: flex;
    gap: var(--dars-spacing-sm);
    list-style: none;
    margin: 0;
    padding: 0;
}

.dars-navbar-nav a {
    color: var(--dars-primary);
    text-decoration: none;
    padding: var(--dars-spacing-sm) var(--dars-spacing-md);
    border-radius: var(--dars-border-radius);
    transition: background-color 0.15s ease, color 0.15s ease;
}

.dars-navbar-nav a:hover {
    background-color: var(--dars-light);
    color: var(--dars-primary-hover);
}

/* Checkbox */
.dars-checkbox-wrapper {
    display: inline-flex;
    align-items: center;
    gap: var(--dars-spacing-sm);
    margin: var(--dars-spacing-xs) 0;
}

.dars-checkbox {
    width: 1rem;
    height: 1rem;
    cursor: pointer;
    accent-color: var(--dars-primary);
}

.dars-checkbox:disabled {
    opacity: 0.65;
    cursor: not-allowed;
}

.dars-checkbox-wrapper label {
    cursor: pointer;
    user-select: none;
    color: var(--dars-text-color);
}

/* RadioButton */
.dars-radio-wrapper {
    display: inline-flex;
    align-items: center;
    gap: var(--dars-spacing-sm);
    margin: var(--dars-spacing-xs) 0;
}

.dars-radio {
    width: 1rem;
    height: 1rem;
    cursor: pointer;
    accent-color: var(--dars-primary);
}

.dars-radio:disabled {
    opacity: 0.65;
    cursor: not-allowed;
}

.dars-radio-wrapper label {
    cursor: pointer;
    user-select: none;
    color: var(--dars-text-color);
}

/* Select */
.dars-select {
    display: block;
    width: 100%;
    padding: 0.375rem 0.75rem;
    font-size: 1rem;
    font-weight: 400;
    line-height: 1.5;
    color: var(--dars-text-color);
    background-color: var(--dars-white);
    background-clip: padding-box;
    border: 1px solid var(--dars-border-color);
    border-radius: var(--dars-border-radius);
    transition: border-color 0.15s ease-in-out, box-shadow 0.15s ease-in-out;
    cursor: pointer;
}

.dars-select:focus {
    color: var(--dars-text-color);
    background-color: var(--dars-white);
    border-color: #80bdff;
    outline: 0;
    box-shadow: 0 0 0 0.2rem rgba(0, 123, 255, 0.25);
}

.dars-select:disabled {
    opacity: 0.65;
    cursor: not-allowed;
    background-color: var(--dars-light);
}

.dars-select option:disabled {
    color: var(--dars-text-muted);
}

/* Slider */
.dars-slider-wrapper {
    display: flex;
    align-items: center;
    gap: var(--dars-spacing-md);
    margin: var(--dars-spacing-sm) 0;
}

.dars-slider-wrapper.dars-slider-vertical {
    flex-direction: column;
    align-items: stretch;
}

.dars-slider {
    flex: 1;
    cursor: pointer;
    accent-color: var(--dars-primary);
}

.dars-slider:disabled {
    opacity: 0.65;
    cursor: not-allowed;
}

.dars-slider-value {
    font-weight: 600;
    min-width: 2.5rem;
    text-align: center;
    padding: var(--dars-spacing-xs) var(--dars-spacing-sm);
    background-color: var(--dars-light);
    border-radius: var(--dars-border-radius);
    font-size: 0.875rem;
    color: var(--dars-text-color);
}

.dars-slider-wrapper label {
    font-weight: 500;
    color: var(--dars-text-color);
}

/* DatePicker */
.dars-datepicker {
    display: block;
    width: 100%;
    padding: 0.375rem 0.75rem;
    font-size: 1rem;
    font-weight: 400;
    line-height: 1.5;
    color: var(--dars-text-color);
    background-color: var(--dars-white);
    background-clip: padding-box;
    border: 1px solid var(--dars-border-color);
    border-radius: var(--dars-border-radius);
    transition: border-color 0.15s ease-in-out, box-shadow 0.15s ease-in-out;
    cursor: pointer;
}

.dars-datepicker:focus {
    color: var(--dars-text-color);
    background-color: var(--dars-white);
    border-color: #80bdff;
    outline: 0;
    box-shadow: 0 0 0 0.2rem rgba(0, 123, 255, 0.25);
}

.dars-datepicker:disabled {
    opacity: 0.65;
    cursor: not-allowed;
    background-color: var(--dars-light);
}

.dars-datepicker:readonly {
    background-color: var(--dars-light);
    cursor: default;
}

.dars-datepicker-inline {
    display: inline-block;
    border: 1px solid var(--dars-border-color);
    border-radius: var(--dars-border-radius);
    padding: var(--dars-spacing-md);
    background-color: var(--dars-white);
}

.dars-datepicker-inline .dars-datepicker {
    border: none;
    padding: 0;
}

/* Markdown */
.dars-markdown {
    font-family: var(--dars-font-family);
    line-height: 1.6;
    color: var(--dars-text-color);
    background-color: var(--dars-white);
    padding: var(--dars-spacing-lg);
    border-radius: var(--dars-border-radius-lg);
}

.dars-markdown-dark {
    color: #e0e0e0;
    background-color: #1e1e1e;
}

.dars-markdown h1,
.dars-markdown h2,
.dars-markdown h3,
.dars-markdown h4,
.dars-markdown h5,
.dars-markdown h6 {
    margin-top: 1.5em;
    margin-bottom: 0.5em;
    font-weight: 600;
    line-height: 1.25;
    color: var(--dars-text-color);
}

.dars-markdown-dark h1,
.dars-markdown-dark h2,
.dars-markdown-dark h3,
.dars-markdown-dark h4,
.dars-markdown-dark h5,
.dars-markdown-dark h6 {
    color: #ffffff;
}

.dars-markdown h1 { font-size: 2em; }
.dars-markdown h2 { font-size: 1.5em; }
.dars-markdown h3 { font-size: 1.25em; }
.dars-markdown h4 { font-size: 1em; }
.dars-markdown h5 { font-size: 0.875em; }
.dars-markdown h6 { font-size: 0.85em; }

.dars-markdown p {
    margin-bottom: 1em;
}

.dars-markdown strong {
    font-weight: 600;
}

.dars-markdown em {
    font-style: italic;
}

.dars-markdown ul,
.dars-markdown ol {
    margin-bottom: 1em;
    padding-left: 2em;
}

.dars-markdown li {
    margin-bottom: 0.5em;
}

.dars-markdown code {
    background-color: var(--dars-light);
    padding: 0.2em 0.4em;
    border-radius: var(--dars-border-radius);
    font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
    font-size: 0.875em;
    color: var(--dars-danger);
}

.dars-markdown-dark code {
    background-color: #2d2d2d;
    color: #e0e0e0;
}

.dars-markdown pre {
    background-color: var(--dars-light);
    padding: var(--dars-spacing-md);
    border-radius: var(--dars-border-radius);
    overflow: auto;
    margin-bottom: 1em;
}

.dars-markdown-dark pre {
    background-color: #2d2d2d;
    border: 1px solid #404040;
}

.dars-markdown pre code {
    background: none;
    padding: 0;
    color: inherit;
}

.dars-markdown blockquote {
    border-left: 4px solid var(--dars-border-color);
    padding-left: 1em;
    margin-left: 0;
    color: var(--dars-text-muted);
    font-style: italic;
    background-color: var(--dars-light);
    padding: var(--dars-spacing-sm) var(--dars-spacing-md);
    border-radius: var(--dars-border-radius);
}

.dars-markdown-dark blockquote {
    border-left-color: #555;
    color: #bbb;
    background-color: #2a2a2a;
}

.dars-markdown table {
    border-collapse: collapse;
    width: 100%;
    margin-bottom: 1em;
}

.dars-markdown th,
.dars-markdown td {
    border: 1px solid var(--dars-border-color);
    padding: 0.5em;
    text-align: left;
}

.dars-markdown-dark th,
.dars-markdown-dark td {
    border-color: #444;
    color: #e0e0e0;
}

.dars-markdown th {
    background-color: var(--dars-light);
    font-weight: 600;
}

.dars-markdown-dark th {
    background-color: #333;
}

.dars-markdown a {
    color: var(--dars-primary);
    text-decoration: none;
    transition: color 0.15s ease;
}

.dars-markdown-dark a {
    color: #4da6ff;
}

.dars-markdown a:hover {
    text-decoration: underline;
    color: var(--dars-primary-hover);
}

.dars-markdown-dark a:hover {
    color: #66b3ff;
}

.dars-markdown img {
    max-width: 100%;
    height: auto;
    border-radius: var(--dars-border-radius);
}

.dars-markdown-dark img {
    filter: brightness(0.9);
}

.dars-markdown hr {
    border: none;
    height: 1px;
    background-color: var(--dars-border-color);
    margin: 2em 0;
}

.dars-markdown-dark hr {
    background-color: #444;
}
"""
        return base_css

    def build_vdom_tree(self, component: Component) -> dict:
        """Serializa componente SIN eventos"""
        try:
            comp_type = component.__class__.__name__
        except Exception:
            comp_type = 'Component'

        comp_id = self.get_component_id(component)

        # NUEVO: NO serializar eventos aquí
        
        # Props seguros
        safe_props = {}
        try:
            for k, v in (getattr(component, 'props', {}) or {}).items():
                if callable(v):
                    continue
                if isinstance(v, (str, int, float, bool)) or v is None:
                    safe_props[k] = v
        except Exception:
            pass

        # Soporte para componentes de texto
        text_value = None
        try:
            if comp_type == 'Text' and hasattr(component, 'text'):
                text_value = component.text
        except Exception:
            pass

        # Hijos
        children_nodes = []
        try:
            for child in getattr(component, 'children', []) or []:
                if child is None:
                    continue
                children_nodes.append(self.build_vdom_tree(child))
        except Exception:
            children_nodes = []

        vnode = {
            'type': comp_type,
            'id': comp_id,
            'key': getattr(component, 'key', None),
            'class': getattr(component, 'class_name', None),
            'style': getattr(component, 'style', {}) or {},
            'props': safe_props,
            # NUEVO: REMOVER eventos del VDOM
            'children': children_nodes if children_nodes else []
        }
        if text_value is not None:
            vnode['text'] = text_value
        return vnode

    def generate_vdom_snapshot(self, root_component: Component) -> str:
        """Genera el snapshot VDOM (JSON) a partir del componente raíz.
        Usa VDomBuilder para mantener consistencia con el vdom_tree.js externo.
        """
        import json
        try:
            vdom_dict = VDomBuilder(id_provider=self.get_component_id).build(root_component)
        except Exception:
            vdom_dict = {'type': 'Root', 'id': None, 'children': []}
        return json.dumps(vdom_dict, ensure_ascii=False)

    def _collect_component_types(self, component: Component, types_set: set):
        """Recursively collect all component types used in the tree"""
        if not component:
            return
        
        # Add current component type
        types_set.add(component.__class__.__name__)
        
        # Recurse children
        if hasattr(component, 'children') and component.children:
            for child in component.children:
                self._collect_component_types(child, types_set)

    def generate_javascript(self, app: App, page_root: Component, events_map: Dict[str, Dict[str, Any]] = None) -> str:
        """Genera un runtime modular con eventos integrados directamente en JS"""
        
        # Convertir events_map a código JS
        events_js_code = ""
        if events_map:
            events_js_code = self._generate_events_js(events_map)
            
        states_js_code = self._generate_states_js()
        
        # Collect used component types for conditional logic injection
        used_types = set()
        self._collect_component_types(page_root, used_types)
        
        # Conditional Default Logic
        default_logic_js = ""
        
        # Tabs Logic
        if 'Tabs' in used_types:
            default_logic_js += """
    // Tabs
    document.addEventListener('click', function(e) {
        if (e.target && e.target.matches && e.target.matches('.dars-tab')) {
            const tabsContainer = e.target.closest('.dars-tabs');
            if (!tabsContainer) return;
            const tabIndex = e.target.getAttribute('data-tab');
            tabsContainer.querySelectorAll('.dars-tab').forEach(t => t.classList.remove('dars-tab-active'));
            e.target.classList.add('dars-tab-active');
            tabsContainer.querySelectorAll('.dars-tab-panel').forEach((p, i) => {
                if (i == tabIndex) p.classList.add('dars-tab-panel-active');
                else p.classList.remove('dars-tab-panel-active');
            });
        }
    });
"""

        # Accordion Logic
        if 'Accordion' in used_types:
            default_logic_js += """
    // Accordion
    document.addEventListener('click', function(e) {
        if (e.target && e.target.matches && e.target.matches('.dars-accordion-title')) {
            const section = e.target.closest('.dars-accordion-section');
            if (section) {
                section.classList.toggle('dars-accordion-open');
            }
        }
    });
"""

        # Modal Logic (Close on overlay click)
        if 'Modal' in used_types:
            default_logic_js += """
    // Modal (Close on overlay click)
    document.addEventListener('click', function(e) {
        if (e.target && e.target.matches && e.target.matches('.dars-modal')) {
            // Only close if clicking the overlay itself, not the content
            // Check if the modal is currently visible (flex/block)
            const style = window.getComputedStyle(e.target);
            if (style.display !== 'none') {
                e.target.style.display = 'none';
            }
        }
    });
"""

        # Slider Logic (Update displayed value)
        if 'Slider' in used_types:
            default_logic_js += """
    // Slider (Update displayed value)
    document.addEventListener('input', function(e) {
        if (e.target && e.target.type === 'range') {
            const wrapper = e.target.closest('.dars-slider-wrapper');
            if (wrapper) {
                const valueDisplay = wrapper.querySelector('.dars-slider-value');
                if (valueDisplay) {
                    valueDisplay.textContent = e.target.value;
                }
            }
        }
    });
"""
        
        runtime = f"""// Dars Runtime
    (function(){{
    const eventMap = new Map();
    let currentSnapshot = null;
    let currentVersion = null;

    function initializeEvents() {{
    {events_js_code}
    
    // --- Default Logic for Advanced Components ---
    {default_logic_js}
    }}
    
    function initializeStates() {{
    {states_js_code}
    }}

    function walk(v, fn){{
        if(!v) return;
        fn(v);
        const ch = v.children || [];
        for(let i=0;i<ch.length;i++){{ walk(ch[i], fn); }}
    }}

    // Utilities
    function setProps(el, props){{
        if(!el || !props) return;
        for(const [k,v] of Object.entries(props)){{
        try {{
            if(v === false || v === null || typeof v === 'undefined'){{
            el.removeAttribute(k);
            }} else {{
            el.setAttribute(k, String(v));
            }}
        }} catch(err) {{ /* ignore */ }}
        }}
    }}
    function diffProps(el, oldP={{}}, newP={{}}){{
        // remove
        for(const k in oldP){{ if(!(k in newP)){{ try{{ el.removeAttribute(k); }}catch{{}} }} }}
        // add/update
        for(const k in newP){{ const v=newP[k]; try{{ if(v===false||v===null||typeof v==='undefined'){{ el.removeAttribute(k);}} else {{ el.setAttribute(k, String(v)); }} }}catch{{}} }}
    }}
    function diffStyles(el, oldS={{}}, newS={{}}){{
        for(const k in oldS){{ if(!(k in newS)){{ try{{ el.style.removeProperty(k.replace(/_/g,'-')); }}catch{{}} }} }}
        for(const k in newS){{ const v=newS[k]; try{{ el.style.setProperty(k.replace(/_/g,'-'), String(v)); }}catch{{}} }}
    }}

    function delegate(eventName, root){{
        (root||document).addEventListener(eventName, function(e){{
        let node = e.target;
        const boundary = root||document;
        while(node && node !== boundary){{
            const id = node.id;
            if(id && eventMap.has(id)){{
            const handlers = eventMap.get(id);
            
            // Check __darsEv first (these are from js_lib.py event attachment)
            if(node && node.__darsEv && node.__darsEv[eventName]){{
                return;
            }}
            
            // Try exact match first
            let h = handlers[eventName];
            
            // For keyboard events, also check for key-filtered version
            if(!h && (eventName === 'keydown' || eventName === 'keyup' || eventName === 'keypress')){{
                // Check if there's a filtered handler for this specific key
                const key = e.key || e.code;
                if(key){{
                const filteredEvent = eventName + '.' + key;
                h = handlers[filteredEvent];
                }}
            }}
            
            if(typeof h === 'function'){{
                try {{ h.call(node, e); }} catch(err){{ console.error('[Dars] handler error', err); }}
                return;
            }}
            }}
            node = node.parentNode;
        }}
        }}, true);
    }}

    function typesDiffer(a,b){{ return (a && b) ? a.type !== b.type : a!==b; }}

    function removeSubtree(v){{
        if(!v) return;
        // eliminar hijos primero (postorden)
        const ch = (v.children||[]);
        for(let i=0;i<ch.length;i++){{ removeSubtree(ch[i]); }}
        // limpiar handlers
        if(v.id){{ eventMap.delete(v.id); }}
        // quitar elemento del DOM
        if(v.id){{ const el = document.getElementById(v.id); if(el && el.parentNode){{ try{{ el.parentNode.removeChild(el); }}catch(_){{}} }} }}
    }}

    function updateNode(oldV, newV){{
        if(!newV || !newV.id){{ return {{ ok:false, reason:'missing-new' }}; }}
        let el = document.getElementById(newV.id);
        if(!el){{
        const oldEl = (oldV && oldV.id) ? document.getElementById(oldV.id) : null;
        if(oldEl){{ try {{ oldEl.id = newV.id; el = oldEl; }} catch(_){{}} }}
        }}
        if(!el){{ return {{ ok:false, reason:'missing-el' }}; }}

        if(typesDiffer(oldV, newV)){{
        return {{ ok:false, reason:'type-changed' }};
        }}

        const isIsland = !!newV.isIsland;

        // class -> atributo className
        if(!isIsland && newV.class){{ el.className = newV.class; }}

        // props
        if(!isIsland){{ diffProps(el, (oldV&&oldV.props)||{{}}, newV.props||{{}}); }}

        // styles
        if(!isIsland){{ diffStyles(el, (oldV&&oldV.style)||{{}}, newV.style||{{}}); }}

        // text
        if(!isIsland && Object.prototype.hasOwnProperty.call(newV, 'text')){{
        if(el.textContent !== String(newV.text||'')){{
            el.textContent = String(newV.text||'');
        }}
        }}

        if(isIsland){{ return {{ ok:true }}; }}

        const oldC = (oldV && oldV.children) ? oldV.children : [];
        const newC = (newV.children) ? newV.children : [];

        const oldIndex = new Map(); // clave -> vnode viejo
        for(let i=0;i<oldC.length;i++){{
        const k = (oldC[i] && (oldC[i].id || oldC[i].key)) || null;
        if(k){{ oldIndex.set(String(k), oldC[i]); }}
        }}

        const seenOld = new Set();

        for(let i=0;i<newC.length;i++){{
        const newChild = newC[i];
        const k = (newChild && (newChild.id || newChild.key)) || null;
        if(!k){{
            if(i < oldC.length){{
            const r = updateNode(oldC[i], newChild);
            if(!r.ok){{ return r; }}
            seenOld.add(oldC[i]);
            continue;
            }} else {{
            return {{ ok:false, reason:'children-added' }};
            }}
        }}
        const oldChild = oldIndex.get(String(k));
        if(oldChild){{
            const r = updateNode(oldChild, newChild);
            if(!r.ok){{ return r; }}
            seenOld.add(oldChild);
        }} else {{
            if(i < oldC.length){{
            const candidate = oldC[i];
            if(!typesDiffer(candidate, newChild)){{
                const r = updateNode(candidate, newChild);
                if(!r.ok){{ return r; }}
                seenOld.add(candidate);
                continue;
            }}
            }}
            const subtree = createSubtree(newChild);
            if(subtree){{
            const refChildVNode = (i < oldC.length) ? oldC[i] : null;
            if(refChildVNode && refChildVNode.id){{
                const refEl = document.getElementById(refChildVNode.id);
                if(refEl && refEl.parentNode){{ refEl.parentNode.insertBefore(subtree, refEl); }}
                else {{ el.appendChild(subtree); }}
            }} else {{
                el.appendChild(subtree);
            }}
            continue;
            }}
            return {{ ok:false, reason:'children-added' }};
        }}
        }}

        for(let i=0;i<oldC.length;i++){{
        const v = oldC[i];
        if(!seenOld.has(v)){{
            removeSubtree(v);
        }}
        }}
        return {{ ok:true }};
    }}

    function schedule(fn){{
        if(typeof requestAnimationFrame === 'function'){{
        requestAnimationFrame(fn);
        }} else {{ setTimeout(fn, 16); }}
    }}

    function update(newSnapshot){{
        const old = currentSnapshot;
        if(!old){{
        currentSnapshot = newSnapshot;
        try{{ window.__DARS_VDOM__ = newSnapshot; }}catch(_){{ /* ignore */ }}
        return;
        }}
        schedule(()=>{{
        const res = updateNode(old, newSnapshot);
        if(!res.ok){{
            console.warn('[Dars] Structural change detected (', res.reason, '), reloading...');
            try {{ location.reload(); }} catch(e) {{ /* ignore */ }}
            return;
        }}
        currentSnapshot = newSnapshot;
        try{{ window.__DARS_VDOM__ = newSnapshot; }}catch(_){{ /* ignore */ }}
        }});
    }}

    function hydrate(snapshot){{
        currentSnapshot = snapshot;
        try{{ window.__DARS_VDOM__ = snapshot; }}catch(_){{ /* ignore */ }}
        const delegated = [
        'click','dblclick',
        'mousedown','mouseup','mouseenter','mouseleave','mousemove',
        'keydown','keyup','keypress',
        'change','input','submit',
        'focus','blur'
        ];
        delegated.forEach(ev => delegate(ev, document));
    }}

    function startHotReload(){{
        try{{ if (window.__DARS_HOTRELOAD_DISABLED__) return ()=>{{}}; }}catch(_ ){{ }}
        const vurl = (window.__DARS_VERSION_URL || 'version.txt');
        let timer = null;
        let warnedVersionMissing = false;
        let failCount = 0;
        const maxFails = 10;
        let stopped = false;

        function httpGet(url, onSuccess, onError, responseType){{
        try{{
            const xhr = new XMLHttpRequest();
            if(responseType){{ xhr.responseType = responseType; }}
            xhr.open('GET', url, true);
            xhr.timeout = 5000;
            xhr.onreadystatechange = function(){{
            if(xhr.readyState === 4){{
                if(xhr.status >= 200 && xhr.status < 300){{
                onSuccess(xhr.response);
                }} else {{
                onError();
                }}
            }}
            }};
            xhr.onerror = onError;
            xhr.ontimeout = onError;
            xhr.setRequestHeader('Cache-Control', 'no-store');
            xhr.send();
        }}catch(e){{ onError(); }}
        }}

        function tick(){{
        if(stopped) return;
        httpGet(vurl, function(text){{
            let ver = (text || '').toString().trim();
            // Treat '0' or empty as missing
            if(!ver || ver === '0'){{
            failCount += 1;
            if(failCount >= maxFails){{
                console.warn('[Dars] version file not found after', maxFails, 'attempts. Hot reload disabled for this session.');
                stopped = true;
                try{{ window.__DARS_HOTRELOAD_DISABLED__ = true; window.__DARS_STOP_HOTRELOAD = null; }}catch(_ ){{ }}
                if(timer) try{{ clearTimeout(timer); }}catch(_ ){{ }}
                return;
            }}
            if(!warnedVersionMissing){{ console.warn('[Dars] waiting for version file...'); warnedVersionMissing = true; }}
            timer = setTimeout(tick, 600);
            return;
            }}
            // Reset fail counter on valid version
            failCount = 0;
            warnedVersionMissing = false;
            if(!currentVersion){{ currentVersion = ver; }}
            if(ver && ver !== currentVersion){{
            currentVersion = ver;
            try {{ location.reload(); }} catch(_) {{}}
            return;
            }}
            timer = setTimeout(tick, 600);
        }}, function(){{
            failCount += 1;
            if(failCount >= maxFails){{
            console.warn('[Dars] version file not reachable after', maxFails, 'attempts. Hot reload disabled for this session.');
            stopped = true;
            try{{ window.__DARS_HOTRELOAD_DISABLED__ = true; window.__DARS_STOP_HOTRELOAD = null; }}catch(_ ){{ }}
            if(timer) try{{ clearTimeout(timer); }}catch(_ ){{ }}
            return;
            }}
            if(!warnedVersionMissing){{ console.warn('[Dars] waiting for version file...'); warnedVersionMissing = true; }}
            timer = setTimeout(tick, 600);
        }}, 'text');
        }}
        tick();
        return ()=>{{ try{{ stopped = true; if(timer) clearTimeout(timer); window.__DARS_STOP_HOTRELOAD = null; }}catch(_ ){{ }} }};
    }}

document.addEventListener('DOMContentLoaded', function(){{
initializeStates();
//Inicializar eventos antes de la hidratación
initializeEvents();
        
if(window.__DARS_VDOM__){{
hydrate(window.__DARS_VDOM__);
}} else {{
console.warn('[Dars] No VDOM snapshot found for hydration');
}}
// Activar hot-reload incremental en dev si hay URLs definidas (evitar múltiples pollers)
if(window.__DARS_VERSION_URL && window.__DARS_SNAPSHOT_URL){{
try{{ if (typeof window.__DARS_STOP_HOTRELOAD === 'function') {{ window.__DARS_STOP_HOTRELOAD(); }} }}catch(_){{ }}
try{{ window.__DARS_STOP_HOTRELOAD = startHotReload(); }}catch(_){{ }}
}}

// Initialize reactive bindings for useDynamic
{self._generate_reactive_bindings_js()}
}});
}})();
"""
        return runtime

    def _generate_states_js(self) -> str:
        """Genera código JS puro para inicializar todos los estados directamente en el runtime"""
        try:
            from dars.core.state import STATE_BOOTSTRAP
            from dars.core.state_v2 import STATE_V2_REGISTRY
            
            if not STATE_BOOTSTRAP and not STATE_V2_REGISTRY:
                return "    // No hay estados para inicializar"

            lines = []
            lines.append('    // Inicializar estados')
            lines.append('    try {')
            lines.append('        const statesConfig = [')

            # 1. Generar estados V1 (STATE_BOOTSTRAP)
            if STATE_BOOTSTRAP:
                for i, state in enumerate(STATE_BOOTSTRAP):
                    state_js = self._state_to_js(state)
                    lines.append(f'            {state_js},')

            # 2. Generar estados V2 (STATE_V2_REGISTRY)
            if STATE_V2_REGISTRY:
                for state in STATE_V2_REGISTRY:
                    # Crear objeto de configuración para V2
                    # Necesitamos serializar el snapshot por defecto
                    default_vals = {}
                    if hasattr(state, '_default_snapshot'):
                        default_vals = state._default_snapshot
                    
                    # Convertir valores a JS safe
                    js_defaults = []
                    for k, v in default_vals.items():
                        js_defaults.append(f'"{k}": {self._value_to_js(v)}')
                    
                    defaults_str = '{ ' + ', '.join(js_defaults) + ' }'
                    
                    # ID del componente o nombre del estado
                    state_id = state.component.id if hasattr(state.component, 'id') else str(state.component)
                    
                    state_config = f'''{{
                        "name": "{state_id}",
                        "id": "{state_id}",
                        "defaultValue": {defaults_str},
                        "isV2": true
                    }}'''
                    lines.append(f'            {state_config},')

            lines.append('        ];')
            lines.append('        if (window.Dars && typeof window.Dars.registerStates === "function") {')
            lines.append('            window.Dars.registerStates(statesConfig);')
            lines.append('        } else if (window.__DARS_STATES_FN) {')
            lines.append('            window.__DARS_STATES_FN(statesConfig);')
            lines.append('        } else {')
            lines.append('            // Fallback: cargar runtime y luego registrar estados')
            lines.append('            (async () => {')
            lines.append('                try {')
            lines.append('                    const m = await import("./lib/dars.min.js");')
            lines.append('                    const registerStates = m.registerStates || (m.default && m.default.registerStates);')
            lines.append('                    if (typeof registerStates === "function") {')
            lines.append('                        registerStates(statesConfig);')
            lines.append('                        window.__DARS_STATES_FN = registerStates;')
            lines.append('                    }')
            lines.append('                } catch (e) {')
            lines.append('                    console.error("[Dars] Failed to initialize states", e);')
            lines.append('                }')
            lines.append('            })();')
            lines.append('        }')
            lines.append('    } catch (e) {')
            lines.append('        console.error("[Dars] State initialization error", e);')
            lines.append('    }')

            return '\n'.join(lines)

        except Exception as e:
            return f'    console.error("[Dars] State bootstrap failed: {str(e)}");'

    def _state_to_js(self, state):
        """Convierte un estado a código JavaScript literal"""
        if not isinstance(state, dict):
            return '{}'

        parts = []
        for key, value in state.items():
            js_key = f'"{key}"'
            js_value = self._value_to_js(value)
            parts.append(f'{js_key}: {js_value}')

        return '{ ' + ', '.join(parts) + ' }'

    def _value_to_js(self, value):
        """Convierte cualquier valor a su representación JavaScript"""
        if value is None:
            return 'null'
        elif isinstance(value, bool):
            return 'true' if value else 'false'
        elif isinstance(value, (int, float)):
            return str(value)
        elif isinstance(value, str):
            # Escapar para JavaScript
            escaped = (value.replace('\\', '\\\\')
                       .replace('"', '\\"')
                       .replace("'", "\\'")
                       .replace('\n', '\\n')
                       .replace('\r', '\\r')
                       .replace('\t', '\\t'))
            return f'"{escaped}"'
        elif isinstance(value, list):
            items = [self._value_to_js(item) for item in value]
            return '[' + ', '.join(items) + ']'
        elif isinstance(value, dict):
            parts = []
            for k, v in value.items():
                js_key = f'"{k}"' if isinstance(k, str) else str(k)
                js_value = self._value_to_js(v)
                parts.append(f'{js_key}: {js_value}')
            return '{' + ', '.join(parts) + '}'
        else:
            # Para objetos InlineScript y otros tipos especiales
            try:
                if hasattr(value, 'get_code'):
                    code = value.get_code()
                    # Escapar el código para JS
                    escaped_code = (code.replace('\\', '\\\\')
                                    .replace('"', '\\"')
                                    .replace("'", "\\'")
                                    .replace('\n', '\\n')
                                    .replace('\r', '\\r')
                                    .replace('\t', '\\t'))
                    return f'"{escaped_code}"'
            except Exception:
                pass

            # Fallback: convertir a string
            return f'"{str(value)}"'
    
    def _process_dynamic_props(self, component: Component) -> dict:
        """
        Process component props to detect and handle DynamicBinding objects.
        
        Returns dict with:
        - 'bindings': List of {prop, state_path, component_id}
        - 'initial_values': Dict of {prop: initial_value}
        """
        from dars.hooks.use_dynamic import DynamicBinding, get_bindings_registry
        import re
        
        bindings = []
        initial_values = {}
        registry = get_bindings_registry()
        marker_pattern = r'__DARS_DYNAMIC_\d+_\d+__'
        
        # Check common props (expanded to include disabled, checked)
        props_to_check = ['text', 'html', 'value', 'placeholder', 'src', 'alt', 'href', 'disabled', 'checked', 'style', 'class_name']
        
        for prop_name in props_to_check:
            prop_value = getattr(component, prop_name, None)
            
            state_path = None
            initial_val = None
            
            if isinstance(prop_value, DynamicBinding):
                state_path = prop_value.state_path
                initial_val = prop_value.get_initial_value()
            elif isinstance(prop_value, str):
                # Check if it's a marker string
                match = re.match(marker_pattern, prop_value)
                if match and prop_value in registry:
                    state_path = registry[prop_value]
                    # We need to resolve initial value manually since we don't have the object
                    # But we can create a temp binding to resolve it or use a helper
                    # For now, let's try to resolve it using the same logic as DynamicBinding.get_initial_value
                    try:
                        from dars.core.state_v2 import STATE_V2_REGISTRY
                        parts = state_path.split('.')
                        if len(parts) >= 2:
                            state_id = parts[0]
                            p_name = parts[1]
                            state = next((s for s in STATE_V2_REGISTRY if s.component.id == state_id), None)
                            if state:
                                prop = getattr(state, p_name, None)
                                if prop:
                                    initial_val = prop.value
                    except Exception:
                        pass

            if state_path:
                comp_id = self.get_component_id(component)
                
                bindings.append({
                    'component_id': comp_id,
                    'property': prop_name,
                    'state_path': state_path
                })
                
                # Get initial value from state registry
                initial_values[prop_name] = initial_val
                
                # CRITICAL: Update the component's property with the resolved initial value
                # This ensures that when component.render() is called, it uses the actual value
                # instead of the marker string
                if initial_val is not None:
                    setattr(component, prop_name, initial_val)
        
        return {'bindings': bindings, 'initial_values': initial_values}

    def _process_value_props(self, component: Component) -> dict:
        """
        Process component props to detect and handle ValueMarker objects (useValue).
        
        Unlike _process_dynamic_props, this does NOT create reactive bindings.
        It only resolves and sets the initial value from state.
        
        Returns dict with:
        - 'initial_values': Dict of {prop: initial_value}
        - 'selectors': Dict of {prop: selector} for CSS class addition
        """
        from dars.hooks.use_value import ValueMarker, get_value_registry
        import re
        
        initial_values = {}
        selectors = {}
        registry = get_value_registry()
        marker_pattern = r'__DARS_VALUE_\d+_\d+__'
        
        # Check common props
        props_to_check = ['value', 'placeholder', 'text', 'html', 'checked']
        
        for prop_name in props_to_check:
            prop_value = getattr(component, prop_name, None)
            
            selector = None
            initial_val = None
            
            if isinstance(prop_value, ValueMarker):
                selector = prop_value.selector
                initial_val = prop_value.get_initial_value()
            elif isinstance(prop_value, str):
                # Check if it's a marker string
                match = re.match(marker_pattern, prop_value)
                if match and prop_value in registry:
                    marker = registry[prop_value]
                    selector = marker.selector
                    initial_val = marker.get_initial_value()
            
            if selector:
                selectors[prop_name] = selector
                initial_values[prop_name] = initial_val
                
                # CRITICAL: Update the component's property with the resolved initial value
                # This ensures that when component.render() is called, it uses the actual value
                if initial_val is not None:
                    setattr(component, prop_name, initial_val)
                
                # Add selector as CSS class if it's a class selector
                if selector.startswith('.'):
                    class_name = selector[1:]  # Remove the leading dot
                    if hasattr(component, 'class_name'):
                        existing_classes = component.class_name or ""
                        if class_name not in existing_classes:
                            component.class_name = f"{existing_classes} {class_name}".strip()
        
        return {'initial_values': initial_values, 'selectors': selectors}
    
    def _collect_bindings_from_tree(self, component):
        """
        Recursively traverse component tree to collect dynamic bindings.
        This avoids rendering components (which can have side effects like script injection).
        """
        if not hasattr(self, '_built_in_bindings'):
            self._built_in_bindings = []
        
        # Process this component's dynamic props
        result = self._process_dynamic_props(component)
        if result['bindings']:
            self._built_in_bindings.extend(result['bindings'])
        
        # Recursively process children
        if hasattr(component, 'children') and component.children:
            for child in component.children:
                if child is not None:
                    self._collect_bindings_from_tree(child)


    def _generate_reactive_bindings_js(self) -> str:
        """Generate JavaScript for reactive bindings from useDynamic"""
        # Collect all bindings: FunctionComponent spans (self._dynamic_bindings) AND built-in props (self._built_in_bindings)
        
        has_fc_bindings = hasattr(self, '_dynamic_bindings') and self._dynamic_bindings
        has_builtin_bindings = hasattr(self, '_built_in_bindings') and self._built_in_bindings
        
        if not has_fc_bindings and not has_builtin_bindings:
            return "    // No reactive bindings"
        
        lines = []
        lines.append("    // Reactive bindings for useDynamic")
        lines.append("    try {")
        lines.append("        // Hook into window.Dars.change to update reactive elements")
        lines.append("        const originalChange = window.Dars && window.Dars.change;")
        lines.append("        if (originalChange) {")
        lines.append("            window.Dars.change = function(payload) {")
        lines.append("                // Call original change")
        lines.append("                const result = originalChange.call(this, payload);")
        lines.append("                ")
        lines.append("                // Update reactive elements if this is a dynamic change")
        lines.append("                if (payload && payload.dynamic && payload.id) {")
        
        # 1. Handle FunctionComponent spans (data-dynamic="{state_path}")
        if has_fc_bindings:
            # Group by component ID (state ID)
            bindings_by_component = {}
            for state_path, component_ids in self._dynamic_bindings.items():
                parts = state_path.split('.')
                if len(parts) >= 2:
                    component_id = parts[0]
                    property_name = parts[1]
                    if component_id not in bindings_by_component:
                        bindings_by_component[component_id] = {}
                    bindings_by_component[component_id][property_name] = state_path
            
            for component_id, properties in bindings_by_component.items():
                lines.append(f"                    // FunctionComponent bindings for {component_id}")
                lines.append(f"                    if (payload.id === '{component_id}') {{")
                for property_name, state_path in properties.items():
                    lines.append(f"                        if (payload.attrs && payload.attrs.{property_name} !== undefined) {{")
                    lines.append(f"                            document.querySelectorAll('[data-dynamic=\"{state_path}\"]').forEach(function(el) {{")
                    lines.append(f"                                el.textContent = payload.attrs.{property_name};")
                    lines.append("                            });")
                    lines.append(f"                        }} else if (payload.{property_name} !== undefined) {{")
                    lines.append(f"                            document.querySelectorAll('[data-dynamic=\"{state_path}\"]').forEach(function(el) {{")
                    lines.append(f"                                el.textContent = payload.{property_name};")
                    lines.append("                            });")
                    lines.append("                        }")
                lines.append("                    }")

        # 2. Handle Built-in Component bindings (direct ID update)
        if has_builtin_bindings:
            # Group bindings by State ID
            # self._built_in_bindings is list of {component_id, property, state_path}
            bindings_by_state = {}
            for binding in self._built_in_bindings:
                state_path = binding['state_path']
                parts = state_path.split('.')
                if len(parts) >= 2:
                    state_id = parts[0]
                    state_prop = parts[1]
                    
                    if state_id not in bindings_by_state:
                        bindings_by_state[state_id] = {}
                    if state_prop not in bindings_by_state[state_id]:
                        bindings_by_state[state_id][state_prop] = []
                    
                    bindings_by_state[state_id][state_prop].append({
                        'target_id': binding['component_id'],
                        'target_prop': binding['property']
                    })

            for state_id, props in bindings_by_state.items():
                lines.append(f"                    // Built-in bindings for state '{state_id}'")
                lines.append(f"                    if (payload.id === '{state_id}') {{")
                for state_prop, targets in props.items():
                    # Check if this property changed
                    lines.append(f"                        let val_{state_prop} = undefined;")
                    lines.append(f"                        if (payload.attrs && payload.attrs.{state_prop} !== undefined) val_{state_prop} = payload.attrs.{state_prop};")
                    lines.append(f"                        else if (payload.{state_prop} !== undefined) val_{state_prop} = payload.{state_prop};")
                    
                    lines.append(f"                        if (val_{state_prop} !== undefined) {{")
                    # Group targets by ID to avoid duplicate declarations
                    targets_by_id = {}
                    for target in targets:
                        tid = target['target_id']
                        if tid not in targets_by_id:
                            targets_by_id[tid] = []
                        targets_by_id[tid].append(target['target_prop'])
                    
                    for target_id, target_props in targets_by_id.items():
                        lines.append(f"                            const el_{target_id} = document.getElementById('{target_id}');")
                        lines.append(f"                            if (el_{target_id}) {{")
                        for target_prop in target_props:
                            if target_prop == 'text':
                                lines.append(f"                                el_{target_id}.textContent = String(val_{state_prop});")
                            elif target_prop == 'html':
                                lines.append(f"                                el_{target_id}.innerHTML = String(val_{state_prop});")
                            elif target_prop == 'value':
                                lines.append(f"                                el_{target_id}.value = String(val_{state_prop});")
                            elif target_prop == 'placeholder':
                                lines.append(f"                                el_{target_id}.setAttribute('placeholder', String(val_{state_prop}));")
                            else:
                                lines.append(f"                                el_{target_id}.setAttribute('{target_prop}', String(val_{state_prop}));")
                        lines.append("                            }")
                    lines.append("                        }")
                lines.append("                    }")

        lines.append("                }")
        lines.append("                return result;")
        lines.append("            };")
        lines.append("        }")
        lines.append("    } catch(e) {")
        lines.append("        console.error('[Dars] Failed to initialize reactive bindings', e);")
        lines.append("    }")
        
        return '\n'.join(lines)
    
    def _generate_events_js(self, events_map: Dict[str, Dict[str, Any]]) -> str:
        """Genera código JS para inicializar todos los eventos directamente en el runtime"""
        lines = []

        for comp_id, events in events_map.items():
            for event_name, event_handlers in events.items():
                # Soporte para arrays de handlers
                handlers_list = event_handlers if isinstance(event_handlers, list) else [event_handlers]
                
                valid_handlers = []
                for handler_spec in handlers_list:
                    code = None
                    
                    # Extraer código del handler de manera más robusta
                    if hasattr(handler_spec, 'get_code'):
                        # Para objetos dScript, InlineScript, etc.
                        try:
                            code = handler_spec.get_code()
                        except Exception:
                            continue
                    elif isinstance(handler_spec, dict):
                        # Para diccionarios con código
                        code = handler_spec.get('code') or handler_spec.get('value')
                    elif isinstance(handler_spec, str):
                        # Para strings directos
                        code = handler_spec
                    
                    if code and isinstance(code, str) and code.strip():
                        valid_handlers.append(code.strip())

                if valid_handlers:
                    lines.append(f'    // Evento {event_name} para componente {comp_id}')
                    lines.append(f'    if (!eventMap.has("{comp_id}")) eventMap.set("{comp_id}", {{}});')
                    
                    # NUEVO: Ejecutar cada handler en su propio contexto
                    if len(valid_handlers) == 1:
                        # Caso único handler - mantener compatibilidad
                        lines.append(f'    eventMap.get("{comp_id}")["{event_name}"] = async function(event) {{')
                        lines.append(f'        try {{ {valid_handlers[0]} }} catch(e) {{ console.error("Error en handler:", e); }}')
                        lines.append(f'    }};')
                    else:
                        # Múltiples handlers - ejecutar cada uno individualmente
                        lines.append(f'    eventMap.get("{comp_id}")["{event_name}"] = async function(event) {{')
                        for i, handler_code in enumerate(valid_handlers):
                            lines.append(f'        // Handler {i+1}')
                            lines.append(f'        try {{ {handler_code} }} catch(e) {{ console.error("Error en handler {i+1}:", e); }}')
                        lines.append(f'    }};')
                    
                    lines.append('')

        return '\n'.join(lines) if lines else '    // No hay eventos para esta página'

    def get_component_id(self, component, prefix="comp"):
        """
        Devuelve el id del componente.
        - Si el componente ya tiene id definido, se respeta.
        - Si no tiene, se genera uno único y se asigna al objeto (para consistencia).
        """
        comp_id = getattr(component, "id", None)
        if not comp_id:
            comp_id = self.generate_unique_id(component, prefix=prefix)
            try:
                component.id = comp_id
            except Exception:
                # si el objeto no permite asignar, seguimos usando comp_id local
                pass
        # Hash IDs in bundle mode consistently
        if getattr(self, '_hash_ids', False) and comp_id:
            hid = self._hash_id(comp_id)
            try:
                component.id = hid
            except Exception:
                pass
            return hid
        return comp_id

    def _hash_id(self, original: str) -> str:
        import hashlib
        m = getattr(self, '_id_hash_map', None)
        if m is None:
            self._id_hash_map = {}
            m = self._id_hash_map
        if original in m:
            return m[original]
        h = hashlib.sha256(original.encode('utf-8')).hexdigest()[:12]
        obf = 'd' + h
        m[original] = obf
        return obf
    def render_function_component(self, component: Component) -> str:
        """
        Render a function component with automatic property injection.
        
        Validates and injects:
        - {id} -> id="component-id" or empty
        - {class_name} -> class="..." with framework classes
        - {style} -> style="..." 
        - {children} -> rendered children HTML
        
        Note: Events are handled separately by the exporter using the component ID.
        """
        
        # Ensure component has an ID (required for events and state)
        if not component.id:
            import uuid
            component.id = f"fc_{str(uuid.uuid4())[:8]}"
        
        # Get template from component
        template = component.get_template()
        
        # Process DynamicBinding markers before formatting
        try:
            from dars.hooks.use_dynamic import get_bindings_registry
            from dars.core.state_v2 import STATE_V2_REGISTRY
            import re
            
            bindings_registry = get_bindings_registry()
            marker_pattern = r'__DARS_DYNAMIC_\d+_\d+__'
            markers = re.findall(marker_pattern, template)
            
            # Track bindings for this component for JavaScript generation
            if not hasattr(self, '_dynamic_bindings'):
                self._dynamic_bindings = {}
            
            # Replace each marker with a reactive span element
            for marker in markers:
                if marker in bindings_registry:
                    state_path = bindings_registry[marker]
                    
                    # Track this binding
                    if state_path not in self._dynamic_bindings:
                        self._dynamic_bindings[state_path] = []
                    self._dynamic_bindings[state_path].append(component.id)
                    
                    # Get initial value from component props
                    initial_value = ""
                    try:
                        # Parse state path (e.g., "userCard.name")
                        parts = state_path.split('.')
                        if len(parts) >= 2:
                            property_name = parts[1]  # e.g., "name" from "userCard.name"
                            
                            # Try to get from template_props
                            if hasattr(component, 'template_props'):
                                template_props = component.template_props
                                if isinstance(template_props, dict) and property_name in template_props:
                                    initial_value = str(template_props[property_name])
                            
                            # Also try template_kwargs as fallback
                            if not initial_value and hasattr(component, 'template_kwargs'):
                                template_kwargs = component.template_kwargs
                                if isinstance(template_kwargs, dict) and property_name in template_kwargs:
                                    initial_value = str(template_kwargs[property_name])
                    except Exception:
                        pass
                    
                    # Create reactive span with initial value
                    reactive_span = f'<span data-dynamic="{state_path}" data-component-id="{component.id}">{initial_value}</span>'
                    template = template.replace(marker, reactive_span)
        except ImportError:
            # useDynamic not available, skip processing
            pass
        
        # Build framework properties
        framework_props = {}
        
        # 1. ID (required placeholder)
        framework_props['id'] = f'id="{component.id}"'
        
        # 2. Class name (required placeholder)
        classes = []
        if component.class_name:
            classes.append(component.class_name)
        
        # Add event classes if has events
        if component.events:
            for event_type in component.events.keys():
                classes.append(f"dars-ev-{event_type}")
        
        if classes:
            framework_props['class_name'] = f'class="{" ".join(classes)}"'
        else:
            framework_props['class_name'] = ''
        
        # 3. Style (required placeholder)
        if component.style:
            style_str = self.render_styles(component.style)
            framework_props['style'] = f'style="{style_str}"'
        else:
            framework_props['style'] = ''
        
        # 4. Children (optional)
        if component.children:
            children_html = ''
            for child in component.children:
                children_html += self.render_component(child)
            framework_props['children'] = children_html
        else:
            framework_props['children'] = ''
        
        # Validate required placeholders
        required = ['id', 'class_name', 'style']
        for req in required:
            if f'{{{req}}}' not in template:
                raise ValueError(
                    f"Function component '{component._func_name}' template "
                    f"must include {{{req}}} placeholder"
                )
        
        # Inject framework properties into template
        try:
            rendered = template.format(**framework_props)
        except KeyError as e:
            raise ValueError(
                f"Function component '{component._func_name}' template "
                f"has undefined placeholder: {e}"
            )
            
        # Process ValueMarker IDs (useValue) using BeautifulSoup
        # This allows us to find where the value was used (attribute or text) and apply selectors
        try:
            from dars.hooks.use_value import get_value_registry
            from bs4 import BeautifulSoup
            import re
            
            value_registry = get_value_registry()
            marker_pattern = r'__DARS_VALUE_\d+_\d+__'
            
            # Check if there are any markers in the rendered HTML
            if re.search(marker_pattern, rendered):
                soup = BeautifulSoup(rendered, 'html.parser')
                modified = False
                
                # 1. Find markers in text content
                # We need to find text nodes containing the marker
                # Since BS4 doesn't give easy access to text nodes, we iterate over all elements
                for element in soup.find_all(string=re.compile(marker_pattern)):
                    text = element.string
                    matches = re.findall(marker_pattern, text)
                    
                    # Save parent reference BEFORE replacing
                    parent = element.parent
                    
                    for marker_id in matches:
                        if marker_id in value_registry:
                            marker = value_registry[marker_id]
                            initial_val = str(marker.get_initial_value())
                            
                            # Replace marker with initial value
                            new_text = text.replace(marker_id, initial_val)
                            element.replace_with(new_text)
                            text = new_text # Update for next iteration
                            modified = True
                            
                            # Apply selector to parent element if present
                            if marker.selector and parent:
                                if marker.selector.startswith('.'):
                                    # Class selector
                                    class_name = marker.selector[1:]
                                    existing_classes = parent.get('class', [])
                                    if class_name not in existing_classes:
                                        existing_classes.append(class_name)
                                        parent['class'] = existing_classes
                                elif marker.selector.startswith('#'):
                                    # ID selector
                                    id_value = marker.selector[1:]
                                    parent['id'] = id_value
                
                # 2. Find markers in attributes
                for tag in soup.find_all(True):  # True finds all tags
                    for attr_name, attr_value in list(tag.attrs.items()):
                        # Attributes can be string or list (like class)
                        if isinstance(attr_value, str):
                            matches = re.findall(marker_pattern, attr_value)
                            for marker_id in matches:
                                if marker_id in value_registry:
                                    marker = value_registry[marker_id]
                                    initial_val = str(marker.get_initial_value())
                                    
                                    # Replace marker with initial value
                                    tag[attr_name] = tag[attr_name].replace(marker_id, initial_val)
                                    modified = True
                                    
                                    # Apply selector to this element
                                    if marker.selector:
                                        if marker.selector.startswith('.'):
                                            # Class selector
                                            class_name = marker.selector[1:]
                                            existing_classes = tag.get('class', [])
                                            if class_name not in existing_classes:
                                                existing_classes.append(class_name)
                                                tag['class'] = existing_classes
                                        elif marker.selector.startswith('#'):
                                            # ID selector
                                            id_value = marker.selector[1:]
                                            tag['id'] = id_value
                        
                        elif isinstance(attr_value, list):
                            # Handle list attributes (like class)
                            new_list = []
                            list_modified = False
                            for item in attr_value:
                                if isinstance(item, str) and re.search(marker_pattern, item):
                                    matches = re.findall(marker_pattern, item)
                                    new_item = item
                                    for marker_id in matches:
                                        if marker_id in value_registry:
                                            marker = value_registry[marker_id]
                                            initial_val = str(marker.get_initial_value())
                                            new_item = new_item.replace(marker_id, initial_val)
                                            
                                            # Apply selector
                                            if marker.selector:
                                                if marker.selector.startswith('.'):
                                                    class_name = marker.selector[1:]
                                                    # We'll add it to the list later to avoid modifying while iterating
                                                    # But since we are rebuilding the list, we can just ensure it's added
                                                    # However, tag['class'] is the list we are iterating (indirectly via attr_value copy)
                                                    # Let's handle selector addition after loop
                                                    pass 
                                                    # Note: Adding to class list while processing class list is tricky
                                                    # Ideally useValue isn't used INSIDE a class name string often, but if it is:
                                                    # We should add the selector class as a separate item
                                    
                                    new_list.append(new_item)
                                    list_modified = True
                                else:
                                    new_list.append(item)
                            
                            if list_modified:
                                tag[attr_name] = new_list
                                modified = True
                                
                                # Re-scan for selectors to add (simpler approach)
                                # If any marker in the original list had a selector, add it now
                                for item in attr_value:
                                    if isinstance(item, str):
                                        matches = re.findall(marker_pattern, item)
                                        for marker_id in matches:
                                            if marker_id in value_registry:
                                                marker = value_registry[marker_id]
                                                if marker.selector and marker.selector.startswith('.'):
                                                    class_name = marker.selector[1:]
                                                    current_classes = tag.get('class', [])
                                                    if class_name not in current_classes:
                                                        current_classes.append(class_name)
                                                        tag['class'] = current_classes

                if modified:
                    # Use prettify() or just str() depending on need. 
                    # str(soup) might add <html><body> if it parsed a fragment as full doc, 
                    # but for fragments BeautifulSoup usually behaves well if created from fragment.
                    # However, to be safe with fragments, we can output the body contents if it added body
                    # But since we passed a fragment, soup usually is the fragment.
                    # Let's check if it wrapped it.
                    rendered = str(soup)
                    
        except ImportError:
            pass
        except Exception as e:
            print(f"Warning: Error processing useValue markers in FunctionComponent: {e}")
        
        return rendered


    def render_component(self, component: Component) -> str:
        if not isinstance(component, Component):
            raise TypeError(f"render_component wait to recived an instance of Component, but recive an {component}")
        """Render an HTML component"""
        
        # Check if it's a function component
        if hasattr(component, '_is_function_component') and component._is_function_component:
            return self.render_function_component(component)
            
        from dars.components.basic.page import Page
        from dars.components.layout.grid import GridLayout
        from dars.components.layout.flex import FlexLayout
        
        
        # Lista de componentes built-in de Dars que NO deben usar su propio metodo render()
        builtin_components = [
            Page, GridLayout, FlexLayout, Text, Button, Input, Container, Image, Link, 
            Textarea, Card, Modal, Navbar, Checkbox, RadioButton, Select, Slider, 
            DatePicker, Table, Tabs, Accordion, ProgressBar, Spinner, Tooltip, Markdown, Section
        ]
        
        # Verificar si es un componente personalizado (no built-in)
        is_custom_component = True
        for builtin_type in builtin_components:
            if isinstance(component, builtin_type):
                is_custom_component = False
                break
        
        if isinstance(component, Component) and is_custom_component:
            if hasattr(component, 'render') and callable(component.render):
                try:
                    return component.render(self) 
                except Exception as e:
                    print(f"Error at rendering component {component.__class__.__name__}: {e}")

        
        if isinstance(component, Page):
            return self.render_page(component)
        if isinstance(component, GridLayout):
            return self.render_grid(component)
        if isinstance(component, FlexLayout):
            return self.render_flex(component)
        if isinstance(component, Text):
            return self.render_text(component)
        elif isinstance(component, Button):
            return self.render_button(component)
        elif isinstance(component, Input):
            return self.render_input(component)
        elif isinstance(component, Container):
            return self.render_container(component)
        elif isinstance(component, Section):
            return self.render_section(component)
        elif isinstance(component, Image):
            return self.render_image(component)
        elif isinstance(component, Link):
            return self.render_link(component)
        elif isinstance(component, Textarea):
            return self.render_textarea(component)
        elif isinstance(component, Card):
            return self.render_card(component)
        elif isinstance(component, Modal):
            return self.render_modal(component)
        elif isinstance(component, Navbar):
            return self.render_navbar(component)
        elif isinstance(component, Checkbox):
            return self.render_checkbox(component)
        elif isinstance(component, RadioButton):
            return self.render_radiobutton(component)
        elif isinstance(component, Select):
            return self.render_select(component)
        elif isinstance(component, Slider):
            return self.render_slider(component)
        elif isinstance(component, DatePicker):
            return self.render_datepicker(component)
        elif isinstance(component, Table):
            return self.render_table(component)
        elif isinstance(component, Tabs):
            return self.render_tabs(component)
        elif isinstance(component, Accordion):
            return self.render_accordion(component)
        elif isinstance(component, ProgressBar):
            return self.render_progressbar(component)
        elif isinstance(component, Spinner):
            return self.render_spinner(component)
        elif isinstance(component, Tooltip):
            return self.render_tooltip(component)
        elif isinstance(component, Markdown):
            return self.render_markdown(component)
        else:
            # Componente genérico
            return self.render_generic_component(component)

    def render_grid(self, grid):
        """Renderiza un GridLayout como un div con CSS grid."""
        component_id = self.get_component_id(grid, prefix="grid")
        class_attr = f'class="dars-grid {grid.class_name or ""}"'
        style = f'display: grid; grid-template-rows: repeat({grid.rows}, 1fr); grid-template-columns: repeat({grid.cols}, 1fr); gap: {getattr(grid, "gap", "16px")};'
        # Render anchors/positions
        children_html = ""
        layout_info = getattr(grid, 'get_child_layout', lambda: [])()
        for child_info in layout_info:
            child = child_info['child']
            row = child_info.get('row', 0) + 1
            col = child_info.get('col', 0) + 1
            row_span = child_info.get('row_span', 1)
            col_span = child_info.get('col_span', 1)
            anchor = child_info.get('anchor')
            anchor_style = ''
            if anchor:
                if isinstance(anchor, str):
                    anchor_map = {
                        'top-left': 'justify-self: start; align-self: start;',
                        'top': 'justify-self: center; align-self: start;',
                        'top-right': 'justify-self: end; align-self: start;',
                        'left': 'justify-self: start; align-self: center;',
                        'center': 'justify-self: center; align-self: center;',
                        'right': 'justify-self: end; align-self: center;',
                        'bottom-left': 'justify-self: start; align-self: end;',
                        'bottom': 'justify-self: center; align-self: end;',
                        'bottom-right': 'justify-self: end; align-self: end;'
                    }
                    anchor_style = anchor_map.get(anchor, '')
                elif hasattr(anchor, 'x') or hasattr(anchor, 'y'):
                    # AnchorPoint object
                    if getattr(anchor, 'x', None):
                        if anchor.x == 'left': anchor_style += 'justify-self: start;'
                        elif anchor.x == 'center': anchor_style += 'justify-self: center;'
                        elif anchor.x == 'right': anchor_style += 'justify-self: end;'
                        elif '%' in anchor.x or 'px' in anchor.x: anchor_style += f'left: {anchor.x}; position: relative;'
                    if getattr(anchor, 'y', None):
                        if anchor.y == 'top': anchor_style += 'align-self: start;'
                        elif anchor.y == 'center': anchor_style += 'align-self: center;'
                        elif anchor.y == 'bottom': anchor_style += 'align-self: end;'
                        elif '%' in anchor.y or 'px' in anchor.y: anchor_style += f'top: {anchor.y}; position: relative;'
            grid_item_style = f'grid-row: {row} / span {row_span}; grid-column: {col} / span {col_span}; {anchor_style}'
            children_html += f'<div style="{grid_item_style}">{self.render_component(child)}</div>'
        return f'<div id="{component_id}" {class_attr} style="{style}">{children_html}</div>'

    def render_flex(self, flex):
        """Renderiza un FlexLayout como un div con CSS flexbox."""
        component_id = self.get_component_id(flex, prefix="flex")
        class_attr = f'class="dars-flex {flex.class_name or ""}"'
        style = f'display: flex; flex-direction: {getattr(flex, "direction", "row")}; flex-wrap: {getattr(flex, "wrap", "wrap")}; justify-content: {getattr(flex, "justify", "flex-start")}; align-items: {getattr(flex, "align", "stretch")}; gap: {getattr(flex, "gap", "16px")};'
        children_html = ""
        for child in flex.children:
            anchor = getattr(child, 'anchor', None)
            anchor_style = ''
            if anchor:
                if isinstance(anchor, str):
                    anchor_map = {
                        'top-left': 'align-self: flex-start; justify-self: flex-start;',
                        'top': 'align-self: flex-start; margin-left: auto; margin-right: auto;',
                        'top-right': 'align-self: flex-start; margin-left: auto;',
                        'left': 'align-self: center;',
                        'center': 'align-self: center; margin-left: auto; margin-right: auto;',
                        'right': 'align-self: center; margin-left: auto;',
                        'bottom-left': 'align-self: flex-end;',
                        'bottom': 'align-self: flex-end; margin-left: auto; margin-right: auto;',
                        'bottom-right': 'align-self: flex-end; margin-left: auto;'
                    }
                    anchor_style = anchor_map.get(anchor, '')
                elif hasattr(anchor, 'x') or hasattr(anchor, 'y'):
                    if getattr(anchor, 'x', None):
                        if anchor.x == 'left': anchor_style += 'margin-right: auto;'
                        elif anchor.x == 'center': anchor_style += 'margin-left: auto; margin-right: auto;'
                        elif anchor.x == 'right': anchor_style += 'margin-left: auto;'
                        elif '%' in anchor.x or 'px' in anchor.x: anchor_style += f'left: {anchor.x}; position: relative;'
                    if getattr(anchor, 'y', None):
                        if anchor.y == 'top': anchor_style += 'align-self: flex-start;'
                        elif anchor.y == 'center': anchor_style += 'align-self: center;'
                        elif anchor.y == 'bottom': anchor_style += 'align-self: flex-end;'
                        elif '%' in anchor.y or 'px' in anchor.y: anchor_style += f'top: {anchor.y}; position: relative;'
            children_html += f'<div style="{anchor_style}">{self.render_component(child)}</div>'
        return f'<div id="{component_id}" {class_attr} style="{style}">{children_html}</div>'

    def render_page(self, page):
        """Renderiza un componente Page como root de una página multipage"""
        component_id = self.generate_unique_id(page)
        class_attr = f'class="dars-page {page.class_name or ""}"'
        style_attr = f'style="{self.render_styles(page.style)}"' if page.style else ""
        # Renderizar hijos
        children_html = ""
        children = getattr(page, 'children', [])
        if not isinstance(children, list):
            children = []
        for child in children:
            if hasattr(child, 'render'):
                children_html += self.render_component(child)
        return f'<div id="{component_id}" {class_attr} {style_attr}>{children_html}</div>'


            
    def render_text(self, text: Text) -> str:
        """Renderiza un componente Text"""
        component_id = self.get_component_id(text, prefix="text")
        class_attr = f'class="dars-text {text.class_name or ""}"'
        style_attr = f'style="{self.render_styles(text.style)}"' if text.style else ""
        
        # Process useValue props FIRST (non-reactive initial values)
        value_info = self._process_value_props(text)
        
        # Then process dynamic props (reactive bindings)
        dynamic_info = self._process_dynamic_props(text)
        
        if dynamic_info['bindings']:
            # Store bindings for runtime processing
            if not hasattr(self, '_built_in_bindings'):
                self._built_in_bindings = []
            self._built_in_bindings.extend(dynamic_info['bindings'])
            
            # Use initial value from state if available
            text_value = dynamic_info['initial_values'].get('text', text.text)
            if text_value is None:
                text_value = text.text
        else:
            text_value = text.text
            
        return f'<span id="{component_id}" {class_attr} {style_attr}>{text_value}</span>'
        
    def render_button(self, button: Button) -> str:
        """Renderiza un componente Button"""
        # Asegurarse de que el botón tenga un ID
        if not hasattr(button, 'id') or not button.id:
            import uuid
            button.id = f"btn_{str(uuid.uuid4())[:8]}"
            
        component_id =  self.get_component_id(button, prefix="btn")
        class_attr = f'class="dars-button {button.class_name or ""}"'
        style_attr = f'style="{self.render_styles(button.style)}"' if button.style else ""
        type_attr = f'type="{button.button_type}"'
        
        # Process useValue props FIRST (non-reactive initial values)
        value_info = self._process_value_props(button)
        
        # Then process dynamic props (reactive bindings)
        dynamic_info = self._process_dynamic_props(button)
        
        if dynamic_info['bindings']:
            if not hasattr(self, '_built_in_bindings'):
                self._built_in_bindings = []
            self._built_in_bindings.extend(dynamic_info['bindings'])
            
        # Handle text
        text_value = dynamic_info['initial_values'].get('text', button.text)
        if hasattr(text_value, 'marker'): text_value = ""
        if text_value is None: text_value = button.text

        # Handle disabled
        disabled_val = dynamic_info['initial_values'].get('disabled', button.disabled)
        if hasattr(disabled_val, 'marker'): disabled_val = False
        
        disabled_attr = "disabled" if disabled_val else ""
        
        return f'<button id="{component_id}" {class_attr} {style_attr} {type_attr} {disabled_attr}>{text_value}</button>'
        
    def render_input(self, input_comp: Input) -> str:
        """Renderiza un componente Input"""
        component_id = self.get_component_id(input_comp, prefix="input")
        class_attr = f'class="dars-input {input_comp.class_name or ""}"'
        style_attr = f'style="{self.render_styles(input_comp.style)}"' if input_comp.style else ""
        type_attr = f'type="{input_comp.input_type}"'
        
        # Process useValue props FIRST (non-reactive initial values)
        value_info = self._process_value_props(input_comp)
        
        # Then process dynamic props (reactive bindings)
        dynamic_info = self._process_dynamic_props(input_comp)
        
        if dynamic_info['bindings']:
            # Store bindings for runtime processing
            if not hasattr(self, '_built_in_bindings'):
                self._built_in_bindings = []
            self._built_in_bindings.extend(dynamic_info['bindings'])
        
        # Handle value
        if 'value' in dynamic_info['initial_values'] and dynamic_info['initial_values']['value'] is not None:
            value_val = dynamic_info['initial_values']['value']
        else:
            value_val = input_comp.value
            
        # Handle placeholder
        if 'placeholder' in dynamic_info['initial_values'] and dynamic_info['initial_values']['placeholder'] is not None:
            placeholder_val = dynamic_info['initial_values']['placeholder']
        else:
            placeholder_val = input_comp.placeholder

        value_attr = f'value="{value_val}"' if value_val else ""
        placeholder_attr = f'placeholder="{placeholder_val}"' if placeholder_val else ""
        
        # Handle disabled
        disabled_val = dynamic_info['initial_values'].get('disabled', input_comp.disabled)
        if hasattr(disabled_val, 'marker'): disabled_val = False
        disabled_attr = "disabled" if disabled_val else ""
        
        # Handle readonly
        readonly_val = dynamic_info['initial_values'].get('readonly', input_comp.readonly)
        if hasattr(readonly_val, 'marker'): readonly_val = False
        readonly_attr = "readonly" if readonly_val else ""
        
        # Handle required
        required_val = dynamic_info['initial_values'].get('required', input_comp.required)
        if hasattr(required_val, 'marker'): required_val = False
        required_attr = "required" if required_val else ""
        
        return f'<input id="{component_id}" {class_attr} {style_attr} {type_attr} {value_attr} {placeholder_attr} {disabled_attr} {readonly_attr} {required_attr} />'
        
    def render_container(self, container: Container) -> str:
        """Renderiza un componente Container"""
        component_id = self.get_component_id(container, prefix="container")
        class_attr = f'class="dars-container {container.class_name or ""}"'
        style_attr = f'style="{self.render_styles(container.style)}"' if container.style else ""

        # Renderizar atributos data-* de props
        data_attrs = ""
        if hasattr(container, 'props') and container.props:
            for key, value in container.props.items():
                if key.startswith('data-'):
                    # Escapar el valor para HTML
                    escaped_value = str(value).replace('"', '&quot;')
                    data_attrs += f' {key}="{escaped_value}"'

        # Protección: asegurar que children es lista de Component
        children_html = ""
        children = container.children
        if not isinstance(children, list):
            children = []
        # Aplanar si hay listas anidadas
        flat_children = []
        for child in children:
            if isinstance(child, list):
                flat_children.extend([c for c in child if hasattr(c, 'render')])
            elif hasattr(child, 'render'):
                flat_children.append(child)
        for child in flat_children:
            children_html += self.render_component(child)

        return f'<div id="{component_id}" {class_attr} {style_attr}{data_attrs}>{children_html}</div>'

    def render_section(self, section: Section):
        """Renderiza un componente Section"""
        component_id = self.get_component_id(section, prefix="section")
        class_attr = f'class="dars-section {section.class_name or ""}"'
        style_attr = f'style="{self.render_styles(section.style)}"' if section.style else ""

        children_html = ""
        children = section.children
        if not isinstance(children, list):
            children = []
        flat_children = []
        for child in children:
            if isinstance(child, list):
                flat_children.extend([c for c in child if hasattr(c, 'render')])
            elif hasattr(child, 'render'):
                flat_children.append(child)
        for child in flat_children:
            children_html += self.render_component(child)

        return f'<section id="{component_id}" {class_attr} {style_attr}>{children_html}</section>'
        
    def render_image(self, image: Image) -> str:
        """Renderiza un componente Image"""
        component_id = self.get_component_id(image, prefix="image")
        class_attr = f'class="dars-image {image.class_name or ""}"'
        style_attr = f'style="{self.render_styles(image.style)}"' if image.style else ""
        width_attr = f'width="{image.width}"' if image.width else ""
        height_attr = f'height="{image.height}"' if image.height else ""

        # Process useValue props FIRST (non-reactive initial values)
        value_info = self._process_value_props(image)
        
        # Then process dynamic props (reactive bindings)
        dynamic_info = self._process_dynamic_props(image)
        
        if dynamic_info['bindings']:
            if not hasattr(self, '_built_in_bindings'):
                self._built_in_bindings = []
            self._built_in_bindings.extend(dynamic_info['bindings'])
            
        # Handle src
        src_val = dynamic_info['initial_values'].get('src', image.src)
        # If unresolved binding, use empty string to avoid 404s
        if hasattr(src_val, 'marker'): src_val = ""
        
        # Handle alt
        alt_val = dynamic_info['initial_values'].get('alt', image.alt)
        if hasattr(alt_val, 'marker'): alt_val = ""

        return f'<img id="{component_id}" src="{src_val}" alt="{alt_val}" {width_attr} {height_attr} {class_attr} {style_attr} />'

    def render_link(self, link: Link) -> str:
        """Renderiza un componente Link"""
        component_id = self.get_component_id(link, prefix="link")
        class_attr = f'class="dars-link {link.class_name or ""}"'
        style_attr = f'style="{self.render_styles(link.style)}"' if link.style else ""
        target_attr = f'target="{link.target}"'
        
        # Process useValue props FIRST (non-reactive initial values)
        value_info = self._process_value_props(link)
        
        # Then process dynamic props (reactive bindings)
        dynamic_info = self._process_dynamic_props(link)
        
        if dynamic_info['bindings']:
            if not hasattr(self, '_built_in_bindings'):
                self._built_in_bindings = []
            self._built_in_bindings.extend(dynamic_info['bindings'])
            
        # Handle href
        href_val = dynamic_info['initial_values'].get('href', link.href)
        if hasattr(href_val, 'marker'): href_val = "#"
        
        # Handle text
        text_val = dynamic_info['initial_values'].get('text', link.text)
        if hasattr(text_val, 'marker'): text_val = ""

        return f'<a id="{component_id}" href="{href_val}" {target_attr} {class_attr} {style_attr}>{text_val}</a>'

    def render_textarea(self, textarea: Textarea) -> str:
        """Renderiza un componente Textarea"""
        component_id = self.get_component_id(textarea, prefix="textarea")
        class_attr = f'class="dars-textarea {textarea.class_name or ""}"'
        style_attr = f'style="{self.render_styles(textarea.style)}"' if textarea.style else ""
        rows_attr = f'rows="{textarea.rows}"'
        cols_attr = f'cols="{textarea.cols}"'
        
        # Process useValue props FIRST (non-reactive initial values)
        value_info = self._process_value_props(textarea)
        
        # Then process dynamic props (reactive bindings)
        dynamic_info = self._process_dynamic_props(textarea)
        
        if dynamic_info['bindings']:
            # Store bindings for runtime processing
            if not hasattr(self, '_built_in_bindings'):
                self._built_in_bindings = []
            self._built_in_bindings.extend(dynamic_info['bindings'])
        
        # Handle value
        if 'value' in dynamic_info['initial_values'] and dynamic_info['initial_values']['value'] is not None:
            value_val = dynamic_info['initial_values']['value']
        else:
            value_val = textarea.value
            
        # Handle placeholder
        if 'placeholder' in dynamic_info['initial_values'] and dynamic_info['initial_values']['placeholder'] is not None:
            placeholder_val = dynamic_info['initial_values']['placeholder']
        else:
            placeholder_val = textarea.placeholder
            
        placeholder_attr = f'placeholder="{placeholder_val}"' if placeholder_val else ""
        
        # Handle disabled
        disabled_val = dynamic_info['initial_values'].get('disabled', textarea.disabled)
        if hasattr(disabled_val, 'marker'): disabled_val = False
        disabled_attr = "disabled" if disabled_val else ""
        
        # Handle readonly
        readonly_val = dynamic_info['initial_values'].get('readonly', textarea.readonly)
        if hasattr(readonly_val, 'marker'): readonly_val = False
        readonly_attr = "readonly" if readonly_val else ""
        
        # Handle required
        required_val = dynamic_info['initial_values'].get('required', textarea.required)
        if hasattr(required_val, 'marker'): required_val = False
        required_attr = "required" if required_val else ""
        
        # Handle maxlength
        maxlength_val = dynamic_info['initial_values'].get('max_length', textarea.max_length)
        if hasattr(maxlength_val, 'marker'): maxlength_val = None # Or some default if needed
        maxlength_attr = f'maxlength="{maxlength_val}"' if maxlength_val is not None else ""

        attrs = [class_attr, style_attr, rows_attr, cols_attr, placeholder_attr,
                 disabled_attr, readonly_attr, required_attr, maxlength_attr]
        attrs_str = " ".join(attr for attr in attrs if attr)
        
        return f'<textarea id="{component_id}" {attrs_str}>{value_val or ""}</textarea>'

    def render_card(self, card: Card) -> str:
        """Renderiza un componente Card"""
        component_id = self.get_component_id(card, prefix="card")
        class_attr = f'class="dars-card {card.class_name or ""}"'
        style_attr = f'style="{self.render_styles(card.style)}"' if card.style else ""
        title_html = f'<h2>{card.title}</h2>' if card.title else ""
        children_html = ""
        for child in card.children:
            children_html += self.render_component(child)

        return f'<div id="{component_id}" {class_attr} {style_attr}>{title_html}{children_html}</div>'

    def render_modal(self, modal: Modal) -> str:
        """Renderiza un componente Modal"""
        component_id = self.get_component_id(modal, prefix="modal")
        class_list = "dars-modal"
        if not modal.is_open:
            class_list += " dars-modal-hidden"
        if modal.class_name:
            class_list += f" {modal.class_name}"
        hidden_attr = " hidden" if not modal.is_open else ""
        display_style = "display: flex;" if modal.is_open else "display: none;"
        modal_style = f'{display_style} position: fixed; top: 0; left: 0; width: 100%; height: 100%; background-color: rgba(0,0,0,0.5); justify-content: center; align-items: center; z-index: 1000;'
        if modal.style:
            modal_style += f' {self.render_styles(modal.style)}'
        data_enabled = f'data-enabled="{str(getattr(modal, "is_enabled", True)).lower()}"'
        title_html = f'<h2>{modal.title}</h2>' if modal.title else ""
        children_html = ""
        for child in modal.children:
            children_html += self.render_component(child)
        return (
            f'<div id="{component_id}" class="{class_list}" {data_enabled}{hidden_attr} style="{modal_style}">\n'
            f'    <div class="dars-modal-content" style="background: white; padding: 20px; border-radius: 8px; max-width: 500px; width: 90%;">\n'
            f'        {title_html}\n'
            f'        {children_html}\n'
            f'    </div>\n'
            f'</div>'
        )

    def render_navbar(self, navbar: Navbar) -> str:
        """Renderiza un componente Navbar"""
        component_id = self.get_component_id(navbar, prefix="navbar")
        class_attr = f'class="dars-navbar {navbar.class_name or ""}"'
        style_attr = f'style="{self.render_styles(navbar.style)}"' if navbar.style else ""
        brand_html = f'<div class="dars-navbar-brand">{navbar.brand}</div>' if navbar.brand else ""
        # Soporta hijos como lista o *args (igual que Container)
        children = getattr(navbar, 'children', [])
        if callable(children):
            children = children()
        if children is None:
            children = []
        if not isinstance(children, (list, tuple)):
            children = [children]
        children_html = ""
        for child in children:
            children_html += self.render_component(child)

        return f'<nav id="{component_id}" {class_attr} {style_attr}>{brand_html}<div class="dars-navbar-nav">{children_html}</div></nav>'

    def render_checkbox(self, checkbox: Checkbox) -> str:
        """Renderiza un componente Checkbox"""
        component_id = self.get_component_id(checkbox, prefix="checkbox")
        class_attr = f'class="dars-checkbox {checkbox.class_name or ""}"'
        style_attr = f'style="{self.render_styles(checkbox.style)}"' if checkbox.style else ""
        
        # Process useValue props FIRST (non-reactive initial values)
        value_info = self._process_value_props(checkbox)
        
        # Then process dynamic props (reactive bindings)
        dynamic_info = self._process_dynamic_props(checkbox)
        
        if dynamic_info['bindings']:
            if not hasattr(self, '_built_in_bindings'):
                self._built_in_bindings = []
            self._built_in_bindings.extend(dynamic_info['bindings'])
            
        # Handle checked
        checked_val = dynamic_info['initial_values'].get('checked', checkbox.checked)
        if hasattr(checked_val, 'marker'): checked_val = False
        checked_attr = "checked" if checked_val else ""
        
        # Handle disabled
        disabled_val = dynamic_info['initial_values'].get('disabled', checkbox.disabled)
        if hasattr(disabled_val, 'marker'): disabled_val = False
        disabled_attr = "disabled" if disabled_val else ""
        
        # Handle required
        required_val = dynamic_info['initial_values'].get('required', checkbox.required)
        if hasattr(required_val, 'marker'): required_val = False
        required_attr = "required" if required_val else ""
        
        name_attr = f'name="{checkbox.name}"' if checkbox.name else ""
        value_attr = f'value="{checkbox.value}"' if checkbox.value else ""
        
        attrs = [class_attr, style_attr, checked_attr, disabled_attr, required_attr, name_attr, value_attr]
        attrs_str = " ".join(attr for attr in attrs if attr)
        
        label_html = f'<label for="{component_id}">{checkbox.label}</label>' if checkbox.label else ""
        
        return f'<div class="dars-checkbox-wrapper"><input type="checkbox" id="{component_id}" {attrs_str}>{label_html}</div>'

    def render_radiobutton(self, radio: RadioButton) -> str:
        """Renderiza un componente RadioButton"""
        component_id = self.get_component_id(radio, prefix="radiobutton")
        class_attr = f'class="dars-radio {radio.class_name or ""}"'
        style_attr = f'style="{self.render_styles(radio.style)}"' if radio.style else ""
        
        # Process useValue props FIRST (non-reactive initial values)
        value_info = self._process_value_props(radio)
        
        # Then process dynamic props (reactive bindings)
        dynamic_info = self._process_dynamic_props(radio)
        
        if dynamic_info['bindings']:
            if not hasattr(self, '_built_in_bindings'):
                self._built_in_bindings = []
            self._built_in_bindings.extend(dynamic_info['bindings'])
            
        # Handle checked
        checked_val = dynamic_info['initial_values'].get('checked', radio.checked)
        if hasattr(checked_val, 'marker'): checked_val = False
        checked_attr = "checked" if checked_val else ""
        
        # Handle disabled
        disabled_val = dynamic_info['initial_values'].get('disabled', radio.disabled)
        if hasattr(disabled_val, 'marker'): disabled_val = False
        disabled_attr = "disabled" if disabled_val else ""
        
        # Handle required
        required_val = dynamic_info['initial_values'].get('required', radio.required)
        if hasattr(required_val, 'marker'): required_val = False
        required_attr = "required" if required_val else ""
        
        name_attr = f'name="{radio.name}"'
        value_attr = f'value="{radio.value}"'
        
        attrs = [class_attr, style_attr, checked_attr, disabled_attr, required_attr, name_attr, value_attr]
        attrs_str = " ".join(attr for attr in attrs if attr)
        
        label_html = f'<label for="{component_id}">{radio.label}</label>' if radio.label else ""
        
        return f'<div class="dars-radio-wrapper"><input type="radio" id="{component_id}" {attrs_str}>{label_html}</div>'

    def render_select(self, select: Select) -> str:
        """Renderiza un componente Select"""
        component_id = self.get_component_id(select, prefix="select")
        class_attr = f'class="dars-select {select.class_name or ""}"'
        style_attr = f'style="{self.render_styles(select.style)}"' if select.style else ""
        
        # Process useValue props FIRST (non-reactive initial values)
        value_info = self._process_value_props(select)
        
        # Then process dynamic props (reactive bindings)
        dynamic_info = self._process_dynamic_props(select)
        
        if dynamic_info['bindings']:
            if not hasattr(self, '_built_in_bindings'):
                self._built_in_bindings = []
            self._built_in_bindings.extend(dynamic_info['bindings'])
            
        # Handle disabled
        disabled_val = dynamic_info['initial_values'].get('disabled', select.disabled)
        if hasattr(disabled_val, 'marker'): disabled_val = False
        disabled_attr = "disabled" if disabled_val else ""
        
        # Handle required
        required_val = dynamic_info['initial_values'].get('required', select.required)
        if hasattr(required_val, 'marker'): required_val = False
        required_attr = "required" if required_val else ""
        
        multiple_attr = "multiple" if select.multiple else ""
        size_attr = f'size="{select.size}"' if select.size else ""
        
        attrs = [class_attr, style_attr, disabled_attr, required_attr, multiple_attr, size_attr]
        attrs_str = " ".join(attr for attr in attrs if attr)
        
        # Generar opciones
        options_html = ""
        if select.placeholder and not select.multiple:
            selected = "selected" if not select.value else ""
            options_html += f'<option value="" disabled {selected}>{select.placeholder}</option>'
        
        for option in select.options:
            selected = "selected" if option.value == select.value else ""
            disabled = "disabled" if option.disabled else ""
            options_html += f'<option value="{option.value}" {selected} {disabled}>{option.label}</option>'
        
        return f'<select id="{component_id}" {attrs_str}>{options_html}</select>'

    def render_slider(self, slider: Slider) -> str:
        """Renderiza un componente Slider"""
        component_id = self.get_component_id(slider, prefix="slider")
        class_attr = f'class="dars-slider {slider.class_name or ""}"'
        style_attr = f'style="{self.render_styles(slider.style)}"' if slider.style else ""
        
        # Process useValue props FIRST (non-reactive initial values)
        value_info = self._process_value_props(slider)
        
        # Then process dynamic props (reactive bindings)
        dynamic_info = self._process_dynamic_props(slider)
        
        if dynamic_info['bindings']:
            if not hasattr(self, '_built_in_bindings'):
                self._built_in_bindings = []
            self._built_in_bindings.extend(dynamic_info['bindings'])
            
        # Handle disabled
        disabled_val = dynamic_info['initial_values'].get('disabled', slider.disabled)
        if hasattr(disabled_val, 'marker'): disabled_val = False
        disabled_attr = "disabled" if disabled_val else ""
        min_attr = f'min="{slider.min_value}"'
        max_attr = f'max="{slider.max_value}"'
        value_attr = f'value="{slider.value}"'
        step_attr = f'step="{slider.step}"'
        
        attrs = [class_attr, style_attr, disabled_attr, min_attr, max_attr, value_attr, step_attr]
        attrs_str = " ".join(attr for attr in attrs if attr)
        
        label_html = f'<label for="{component_id}">{slider.label}</label>' if slider.label else ""
        value_display = f'<span class="dars-slider-value">{slider.value}</span>' if slider.show_value else ""
        
        wrapper_class = "dars-slider-vertical" if slider.orientation == "vertical" else "dars-slider-horizontal"
        
        return f'<div class="dars-slider-wrapper {wrapper_class}">{label_html}<input type="range" id="{component_id}" {attrs_str}>{value_display}</div>'

    def render_datepicker(self, datepicker: DatePicker) -> str:
        """Renderiza un componente DatePicker"""
        component_id = self.get_component_id(datepicker, prefix="datepicker")
        class_attr = f'class="dars-datepicker {datepicker.class_name or ""}"'
        style_attr = f'style="{self.render_styles(datepicker.style)}"' if datepicker.style else ""
        disabled_attr = "disabled" if datepicker.disabled else ""
        required_attr = "required" if datepicker.required else ""
        readonly_attr = "readonly" if datepicker.readonly else ""
        value_attr = f'value="{datepicker.value}"' if datepicker.value else ""
        placeholder_attr = f'placeholder="{datepicker.placeholder}"' if datepicker.placeholder else ""
        min_attr = f'min="{datepicker.min_date}"' if datepicker.min_date else ""
        max_attr = f'max="{datepicker.max_date}"' if datepicker.max_date else ""
        
        # Determinar el tipo de input según si incluye tiempo
        input_type = "datetime-local" if datepicker.show_time else "date"
        
        attrs = [class_attr, style_attr, disabled_attr, required_attr, readonly_attr, 
                value_attr, placeholder_attr, min_attr, max_attr]
        attrs_str = " ".join(attr for attr in attrs if attr)
        
        # Si es inline, usar un div contenedor adicional
        if datepicker.inline:
            return f'<div class="dars-datepicker-inline"><input type="{input_type}" id="{component_id}" {attrs_str}></div>'
        else:
            return f'<input type="{input_type}" id="{component_id}" {attrs_str}>'

    def render_table(self, table: Table) -> str:
        # Renderizado HTML para Table
        thead = '<thead><tr>' + ''.join(f'<th>{col["title"]}</th>' for col in table.columns) + '</tr></thead>'
        rows = table.data[:table.page_size] if table.page_size else table.data
        tbody = '<tbody>' + ''.join(
            '<tr>' + ''.join(f'<td>{row.get(col["field"], "")}</td>' for col in table.columns) + '</tr>'
            for row in rows) + '</tbody>'
        return f'<table class="dars-table">{thead}{tbody}</table>'

    def render_tabs(self, tabs: Tabs) -> str:
        tab_headers = ''.join(
            f'<button class="dars-tab{ " dars-tab-active" if i == tabs.selected else "" }" data-tab="{i}">{title}</button>'
            for i, title in enumerate(tabs.tabs)
        )
        panels_html = ''.join(
            f'<div class="dars-tab-panel{ " dars-tab-panel-active" if i == tabs.selected else "" }">{self.render_component(panel) if hasattr(panel, "render") else panel}</div>'
            for i, panel in enumerate(tabs.panels)
        )
        return f'<div class="dars-tabs"><div class="dars-tabs-header">{tab_headers}</div><div class="dars-tabs-panels">{panels_html}</div></div>'

    def render_accordion(self, accordion: Accordion) -> str:
        html = '<div class="dars-accordion">'
        for i, (title, content) in enumerate(accordion.sections):
            opened = ' dars-accordion-open' if i in accordion.open_indices else ''
            html += f'<div class="dars-accordion-section{opened}"><div class="dars-accordion-title">{title}</div><div class="dars-accordion-content">{self.render_component(content) if hasattr(content, "render") else content}</div></div>'
        html += '</div>'
        return html

    def render_progressbar(self, bar: ProgressBar) -> str:
        percent = min(max(bar.value / bar.max_value * 100, 0), 100)
        return f'<div class="dars-progressbar"><div class="dars-progressbar-bar" style="width: {percent}%;"></div></div>'

    def render_spinner(self, spinner: Spinner) -> str:
        return '<div class="dars-spinner"></div>'

    def render_tooltip(self, tooltip: Tooltip) -> str:
        return f'<div class="dars-tooltip dars-tooltip-{tooltip.position}">{self.render_component(tooltip.child) if hasattr(tooltip.child, "render") else tooltip.child}<span class="dars-tooltip-text">{tooltip.text}</span></div>'
    
    def render_markdown(self, markdown: 'Markdown') -> str:
        """Render a Markdown component"""
        try:
            import markdown2
            # Convert markdown to HTML
            html_content = markdown2.markdown(
                markdown.content,
                extras=[
                    "fenced-code-blocks",
                    "code-friendly",
                    "tables",
                    "header-ids",
                ],
            )
        except ImportError:
            # Fallback to basic conversion if markdown2 is not available
            html_content = self._basic_markdown_to_html(markdown.content)
        
        component_id = self.get_component_id(markdown, prefix="markdown")
        
        # Add dark theme class if enabled
        class_name = f"dars-markdown {markdown.class_name or ''}"
        if markdown.dark_theme:
            class_name += " dars-markdown-dark"
        
        class_attr = f'class="{class_name.strip()}"'
        style_attr = f'style="{self.render_styles(markdown.style)}"' if markdown.style else ""

        # Normalize code block classes for client highlighters (e.g., Prism)
        # markdown2 may emit <code class="lang-python">; convert to language-python
        import re
        html_content = re.sub(r'<code class="lang-([a-zA-Z0-9_+-]+)">', r'<code class="language-\1">', html_content)
        # If a <pre><code> lacks a class, add language-none for Prism to process
        html_content = re.sub(r'<pre([^>]*)>\s*<code(?![^>]*class=)([^>]*)>', r'<pre\1>\n<code class="language-none"\2>', html_content)
        # Ensure multiline code blocks render correctly even without extra CSS and allow absolute-positioned copy button
        html_content = html_content.replace(
            '<pre><code',
            '<pre style="white-space: pre; overflow:auto; position: relative;"><code'
        )

        # Auto-inject highlight.js (CSS + JS + init) once per page if enabled in config and not injected
        assets = ""
        cfg_hl = True
        hl_theme = "auto"
        try:
            # Try to read config for markdownHighlight; default True if missing/errors
            app_source = getattr(getattr(self, 'app', None), '__source__', None)
            project_root = os.getcwd() if not app_source else os.path.dirname(os.path.abspath(app_source))
            from dars.config import load_config
            cfg, _ = load_config(project_root)
            cfg_hl = bool(cfg.get('markdownHighlight', True))
            hl_theme = str(cfg.get('markdownHighlightTheme', 'auto')).lower()
        except Exception:
            cfg_hl = True
        
        # Track injection per-page for multipage apps (use a set to track page IDs)
        if not hasattr(self, "_hljs_injected_pages"):
            self._hljs_injected_pages = set()
        
        # Get current page identifier (try to determine which page we're rendering)
        current_page_id = getattr(self, '_current_page_id', 'default')
        
        if cfg_hl and current_page_id not in self._hljs_injected_pages:
            # Prism.js theme CSS selection
            css_links = ''
            if hl_theme == 'dark':
                css_links = '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/themes/prism-okaidia.min.css">\n'
            elif hl_theme == 'light':
                css_links = '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/themes/prism.min.css">\n'
            else:  # auto
                css_links = (
                    '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/themes/prism.min.css" media="(prefers-color-scheme: light)">\n'
                    '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/themes/prism-okaidia.min.css" media="(prefers-color-scheme: dark)">\n'
                )
            parts = []
            parts.append(css_links)
            parts.append('<style>.dars-code-copy{position:absolute;top:8px;right:8px;background:rgba(0,0,0,0.5);color:#fff;border:none;border-radius:6px;padding:4px 8px;font-size:12px;cursor:pointer;opacity:.0;transition:opacity .2s ease;}pre:hover .dars-code-copy{opacity:.9}.dars-code-copy.copied{background:#16a34a}</style>\n')
            parts.append('<script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/prism.min.js"></script>\n')
            parts.append('<script>window.Prism=window.Prism||{};Prism.plugins=Prism.plugins||{};Prism.plugins.autoloader=Prism.plugins.autoloader||{};Prism.plugins.autoloader.languages_path="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/";</script>\n')
            parts.append('<script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/plugins/autoloader/prism-autoloader.min.js"></script>\n')
            parts.append('<script>(function(){function addCopyButtons(){document.querySelectorAll("pre code").forEach(function(code){var pre=code.parentElement;if(!pre||pre.querySelector(".dars-code-copy"))return;var btn=document.createElement("button");btn.className="dars-code-copy";btn.type="button";btn.textContent="Copy";btn.addEventListener("click",async function(e){e.stopPropagation();try{await navigator.clipboard.writeText(code.innerText);btn.textContent="Copied";btn.classList.add("copied");setTimeout(function(){btn.textContent="Copy";btn.classList.remove("copied")},1200)}catch(err){btn.textContent="Error";setTimeout(function(){btn.textContent="Copy"},1200)}});pre.appendChild(btn);});}function guessLang(text){var t=text.trim();if(/^{[\\s\\S]*}$/.test(t)||/^\\[/.test(t))return "json";if(/^(pip |python |python3 |dars |#|\\$ )/m.test(t))return "bash";if(/\\b(def |class |import |from |print\\(|self\\b)/.test(t))return "python";return null;}function stripPygments(code){if(code && code.innerHTML && code.innerHTML.indexOf("<span")!==-1){code.textContent = code.innerText;}}function prepareAndHighlight(){document.querySelectorAll("pre code").forEach(function(code){stripPygments(code);if(!code.className||code.className.indexOf("language-")===-1){var g=guessLang(code.innerText);code.classList.add("language-"+(g||"none"));}if(window.Prism&&Prism.highlightElement){Prism.highlightElement(code);}});}document.addEventListener("DOMContentLoaded",function(){try{prepareAndHighlight();}catch(e){};try{addCopyButtons()}catch(e){}});})();</script>')
            assets = ''.join(parts)
            self._hljs_injected_pages.add(current_page_id)

        # Add stable theme class to container for easier overriding if needed
        theme_tag = hl_theme if hl_theme in ('light','dark') else 'auto'
        class_name = f"{class_name} dars-code-theme-{theme_tag}"
        class_attr = f'class="{class_name.strip()}"'

        return f'{assets}<div id="{component_id}" {class_attr} {style_attr}>{html_content}</div>'

    def _basic_markdown_to_html(self, markdown_text: str) -> str:
        """Basic markdown to HTML conversion as fallback"""
        if not markdown_text:
            return ""
        
        html = markdown_text
        
        # Basic replacements
        html = html.replace('**', '<strong>').replace('**', '</strong>')
        html = html.replace('*', '<em>').replace('*', '</em>')
        html = html.replace('__', '<strong>').replace('__', '</strong>')
        html = html.replace('_', '<em>').replace('_', '</em>')
        
        # Headers
        html = html.replace('# ', '<h1>').replace('\n# ', '</h1>\n<h1>')
        html = html.replace('## ', '<h2>').replace('\n## ', '</h2>\n<h2>')
        html = html.replace('### ', '<h3>').replace('\n### ', '</h3>\n<h3>')
        
        # Line breaks
        html = html.replace('\n\n', '<br><br>')
        
        return html
    def render_generic_component(self, component: Component) -> str:
        """Renderiza un componente genérico con estructura básica"""
        component_id = self.get_component_id(component, prefix="comp")
        class_attr = f'class="{component.class_name or ""}"'
        style_attr = f'style="{self.render_styles(component.style)}"' if component.style else ""
        
        # Renderizar hijos usando el exporter
        children_html = ""
        for child in component.children:
            children_html += self.render_component(child)
            
        # Agregar eventos como data attributes para referencia
        events_attr = ""
        if component.events:
            for event_name in component.events:
                events_attr += f' data-event-{event_name}="true"'
        
        return f'<div id="{component_id}" {class_attr} {style_attr}{events_attr}>{children_html}</div>'
    
    def _export_spa(self, app: App, output_path: str, bundle: bool, should_combine_js: bool, project_root: str) -> bool:
        """Export SPA with client-side routing."""
        import json, copy
        from dars.components.basic.container import Container
        spa_config = {'routes': [], 'index': None, 'notFound': None}
        for route_name, spa_route in app._spa_routes.items():
            route_app = copy.copy(app)
            route_app.root = spa_route.root
            if spa_route.title: route_app.title = spa_route.title
            if isinstance(route_app.root, list): route_app.root = Container(children=route_app.root)
            route_html = self.render_component(route_app.root)
            route_vdom, route_events_map = {}, {}
            try:
                vdom_builder = VDomBuilder(id_provider=self.get_component_id)
                route_vdom, route_events_map = vdom_builder.build(route_app.root), vdom_builder.events_map
                if bundle: route_vdom = self._obfuscate_vdom(route_vdom)
            except: pass
            
            # Generate runtime JS with events/states for this route
            runtime_js = self.generate_javascript(route_app, route_app.root, route_events_map)
            
            # Write runtime file for this route
            runtime_filename = f"runtime_dars_{route_name}.js"
            self.write_file(os.path.join(output_path, runtime_filename), runtime_js)
            
            # Write VDOM file for this route  
            vdom_json = json.dumps(route_vdom, ensure_ascii=False, separators=(",", ":"))
            vdom_filename = f"vdom_tree_{route_name}.js"
            vdom_js_content = f"window.__DARS_VDOM__ = {vdom_json};\n"
            self.write_file(os.path.join(output_path, vdom_filename), vdom_js_content)
            
            # Collect and write scripts for this route (app scripts + page scripts)
            route_scripts = []
            route_scripts.extend(getattr(app, 'scripts', []))
            if hasattr(route_app.root, 'get_scripts'):
                route_scripts.extend(route_app.root.get_scripts())
            
            # Process scripts using _prepare_page_scripts
            combined_js, external_srcs, is_module = self._prepare_page_scripts(
                route_scripts, output_path, project_root
            )
            
            # Write combined scripts to file
            script_filename = f"script_{route_name}.js"
            if combined_js:
                self.write_file(os.path.join(output_path, script_filename), combined_js)
            # Build scripts array: vdom, runtime, then page scripts (use absolute paths)
            scripts_array = [f"/{vdom_filename}", f"/{runtime_filename}"]
            if combined_js:
                scripts_array.append(f"/{script_filename}")
            
            route_config = {
                'name': route_name, 'path': spa_route.route, 'title': spa_route.title or app.title,
                'html': route_html, 'styles': '',
                'scripts': scripts_array, 'events': route_events_map, 'vdom': route_vdom, 'states': [], 'preload': spa_route.preload or [],
                'parent': spa_route.parent
            }
            spa_config['routes'].append(route_config)
            if spa_route.index: spa_config['index'] = route_name
        if app._spa_404_page:
            not_found_app = copy.copy(app)
            
            # Handle both component (Page from dars.components) and wrapper (Page from dars.core.app)
            if hasattr(app._spa_404_page, 'root'):
                # It's a Page wrapper from dars.core.app
                not_found_app.root = app._spa_404_page.root
            else:
                # It's a component directly (Page component or any other component)
                not_found_app.root = app._spa_404_page
            
            if isinstance(not_found_app.root, list): 
                not_found_app.root = Container(children=not_found_app.root)
            
            route_404 = {
                'name': '__404__', 'path': '/404', 'title': '404 Not Found', 
                'html': self.render_component(not_found_app.root),
                'styles': '', 'scripts': [], 'events': {}, 'vdom': {}, 'states': [], 'preload': []
            }
            spa_config['routes'].append(route_404)
            spa_config['notFoundPath'] = '/404'
        else:
            # Default 404 page
            from dars.components.basic.text import Text
            
            default_404_root = Container(
                Text("404 Page Not Found", style={"fontSize": "48px", "fontWeight": "bold", "marginBottom": "20px", "color": "#333"}),
                Text(" The page you are looking for does not exist.", style={"fontSize": "18px", "color": "#666"}),
                style={
                    "display": "flex", "flexDirection": "column", "alignItems": "center", 
                    "justifyContent": "center", "height": "100vh", "fontFamily": "system-ui, -apple-system, sans-serif",
                    "backgroundColor": "#f9f9f9", "margin": "0", "padding": "20px", "textAlign": "center"
                }
            )
            
            route_404 = {
                'name': '__404__', 'path': '/404', 'title': '404 Not Found', 
                'html': self.render_component(default_404_root),
                'styles': '', 'scripts': [], 'events': {}, 'vdom': {}, 'states': [], 'preload': []
            }
            spa_config['routes'].append(route_404)
            spa_config['notFoundPath'] = '/404'
        # Hot reload script for dev mode (only if not bundle)
        hot_reload_script = ""
        if not bundle:
            hot_reload_script = """
<script>
(function() {
    let lastVersion = null;
    const versionUrl = '/version.txt';
    let errorCount = 0;
    const MAX_ERRORS = 10;
    let intervalId = null;
    
    async function checkForUpdates() {
        try {
            const response = await fetch(versionUrl + '?t=' + Date.now(), {
                cache: 'no-store',
                headers: { 'Cache-Control': 'no-cache' }
            });
            
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            
            // Reset error count on success
            errorCount = 0;
            
            const currentVersion = await response.text();
            if (lastVersion === null) {
                lastVersion = currentVersion;
            } else if (lastVersion !== currentVersion) {
                console.log('[Dars Hot Reload] Change detected, reloading...');
                window.location.reload();
            }
        } catch (e) {
            errorCount++;
            if (errorCount >= MAX_ERRORS) {
                console.warn('[Dars Hot Reload] Too many errors (' + errorCount + '), stopping hot reload.');
                if (intervalId) clearInterval(intervalId);
            }
        }
    }
    
    // Check every 500ms for changes
    intervalId = setInterval(checkForUpdates, 500);
    checkForUpdates();
})();
</script>"""
        
        spa_html = f'''<!DOCTYPE html><html lang="{getattr(app, "language", "en")}"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>{app.title}</title><link rel="stylesheet" href="/runtime_css.css"><link rel="stylesheet" href="/styles.css"></head><body><div id="__dars_spa_root__"></div><script type="module" src="/lib/dars.min.js"></script><script>const __DARS_SPA_CONFIG__ = {json.dumps(spa_config, ensure_ascii=False, separators=(",", ":"))};window.addEventListener("DOMContentLoaded", function() {{ if (window.Dars && window.Dars.router) window.Dars.router.registerConfig(__DARS_SPA_CONFIG__);else console.error("[Dars SPA] Router not available");}});\u003c/script\u003e{hot_reload_script}</body></html>'''
        try:
            soup = BeautifulSoup(spa_html, "html.parser")
            spa_html = soup.prettify()
        except: pass
        self.write_file(os.path.join(output_path, "index.html"), spa_html)
        return True


