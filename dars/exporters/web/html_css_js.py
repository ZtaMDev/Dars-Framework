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
            # Initialize obfuscation context for this export
            # Keep original IDs to avoid breaking CSS/anchors. We still obfuscate types and events.
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
            try:
                resolved = resolve_paths(cfg if cfg else {}, project_root)
            except Exception:
                resolved = {"public_abs": None, "include": [], "exclude": []}

            # Copiar public/assets completos al output (tanto en preview como en bundle)
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
            # NOTA: No copiar ejecutables ni nada fuera del proyecto

            base_css_content = self.generate_base_css()  # Nuevo método para estilos base
            custom_css_content = self.generate_custom_css(app)  # Nuevo método para estilos personalizados

            self.write_file(os.path.join(output_path, "runtime_css.css"), base_css_content)
            self.write_file(os.path.join(output_path, "styles.css"), custom_css_content)

            # Multipágina: exportar un HTML, CSS y JS por cada página registrada
            if hasattr(app, "is_multipage") and app.is_multipage():
                import copy
                index_page = None
                if hasattr(app, 'get_index_page'):
                    index_page = app.get_index_page()
                
                # Exportar cada página
                for slug, page in app.pages.items():
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
                    
                    # Generar runtime específico para esta página
                    runtime_js = self.generate_javascript(page_app, page.root)
                    runtime_name = f"runtime_dars_{slug}.js" if slug != "index" else "runtime_dars.js"
                    self.write_file(os.path.join(output_path, runtime_name), runtime_js)
                    # Generar VDOM Tree JS (externo)
                    vdom_name = None
                    try:
                        vdom_dict = VDomBuilder(id_provider=self.get_component_id).build(page_app.root)
                        if bundle:
                            vdom_dict = self._obfuscate_vdom(vdom_dict)
                        import json
                        vdom_js = "window.__DARS_VDOM__ = " + json.dumps(vdom_dict, ensure_ascii=False, separators=(",", ":")) + ";\n"
                    except Exception:
                        vdom_js = "window.__DARS_VDOM__ = { };\n"
                    vdom_name = f"vdom_tree_{slug}.js" if slug != "index" else "vdom_tree.js"
                    self.write_file(os.path.join(output_path, vdom_name), vdom_js)
                    # Fase 2: escribir snapshot/version por página (solo en dev, no bundle)
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
                    
                    # Generar scripts específicos de esta página
                    page_scripts = []
                    
                    # Scripts globales de la app
                    page_scripts.extend(getattr(app, 'scripts', []))
                    
                    # Scripts específicos de esta página
                    if hasattr(page, 'scripts'):
                        page_scripts.extend(page.scripts)
                    
                    # Scripts de componentes dentro de la página
                    if hasattr(page_app.root, 'get_scripts'):
                        page_scripts.extend(page_app.root.get_scripts())
                    
                    # Generar script.js específico para esta página
                    # Preparar y copiar scripts: combinados + externos
                    combined_js, external_srcs, combined_is_module = self._prepare_page_scripts(page_scripts, output_path, project_root)

                    if index_page is not None and page is index_page:
                        # Página index
                        self.write_file(os.path.join(output_path, "script.js"), combined_js)
                        html_content = self.generate_html(page_app, css_file="styles.css",
                                                        script_file="script.js",
                                                        runtime_file="runtime_dars.js",
                                                        extra_script_srcs=external_srcs, bundle=bundle, vdom_script=vdom_name,
                                                        script_is_module=combined_is_module)
                        filename = "index.html"
                    else:
                        # Otras páginas
                        script_name = f"script_{slug}.js"
                        self.write_file(os.path.join(output_path, script_name), combined_js)
                        html_content = self.generate_html(page_app, css_file="styles.css",
                                                        script_file=script_name,
                                                        runtime_file=runtime_name,
                                                        extra_script_srcs=external_srcs, bundle=bundle, vdom_script=vdom_name,
                                                        script_is_module=combined_is_module)
                        filename = f"{slug}.html"
                    
                    # Mejorar formato HTML si es posible
                    try:
                        soup = BeautifulSoup(html_content, "html.parser")
                        html_content = soup.prettify()
                    except ImportError:
                        pass
                    
                    self.write_file(os.path.join(output_path, filename), html_content)
            else:
                # Single-page clásico (mantener comportamiento existente)
                runtime_js = self.generate_javascript(app, app.root)
                self.write_file(os.path.join(output_path, "runtime_dars.js"), runtime_js)
                
                user_scripts = list(getattr(app, 'scripts', []))
                combined_js, external_srcs, combined_is_module = self._prepare_page_scripts(user_scripts, output_path, project_root)
                self.write_file(os.path.join(output_path, "script.js"), combined_js)
                # Generar VDOM Tree JS (externo)
                vdom_name = None
                try:
                    vdom_dict = VDomBuilder(id_provider=self.get_component_id).build(app.root)
                    if bundle:
                        vdom_dict = self._obfuscate_vdom(vdom_dict)
                    import json
                    vdom_js = "window.__DARS_VDOM__ = " + json.dumps(vdom_dict, ensure_ascii=False, separators=(",", ":")) + ";\n"
                except Exception:
                    vdom_js = "window.__DARS_VDOM__ = { };\n"
                vdom_name = "vdom_tree.js"
                self.write_file(os.path.join(output_path, vdom_name), vdom_js)

                html_content = self.generate_html(app, css_file="styles.css",
                                                script_file="script.js",
                                                runtime_file="runtime_dars.js",
                                                extra_script_srcs=external_srcs, bundle=bundle, vdom_script=vdom_name,
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

            return True
        except Exception as e:
            print(f"Error al exportar: {e}")
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
                 script_file: str = "script.js", runtime_file: str = "runtime_dars.js", extra_script_srcs: list = None, bundle: bool = False, vdom_script: str = "vdom_tree.js", script_is_module: bool = False) -> str:
        """Genera el contenido HTML con todas las propiedades de la aplicación"""
        body_content = ""
        from dars.components.basic.container import Container
        root_component = app.root
        # Protección: si root es lista, envolver en Container correctamente
        if isinstance(root_component, list):
            root_component = Container(*root_component)
        if root_component:
            body_content = self.render_component(root_component)
        
        # VDOM snapshot ahora se sirve desde un archivo externo (vdom_script)
        
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
                        "    const m = await import('./lib/dars.min.js');\n"
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
                        "    const m = await import('./lib/dars.min.js');\n"
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

        vdom_script_tag = ''
        if vdom_script:
            vdom_script_tag = f'<script src="{vdom_script}"></script>'

        html_template = f"""<!DOCTYPE html>
<html lang="{app.language}">
<head>
    <meta charset="{app.config.get('charset', 'UTF-8')}">
    {meta_tags_html}
    <title>{app.title}</title>
    {links_html}
    {og_tags_html}
    {twitter_tags_html}
    <link rel=\"stylesheet\" href=\"https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css\">\n    <link rel=\"stylesheet\" href=\"runtime_css.css\">\n    <link rel=\"stylesheet\" href=\"{css_file}\">
</head>
<body>
    {body_content}
    {vdom_script_tag}
    {version_vars_html}
    {bootstrap_json_tag}
    {dars_lib_tag}
    {bootstrap_init_tag}
    <script src=\"{runtime_file}\"{' type=\"module\"' if script_is_module else ''} defer></script>\n{extra_scripts_html}    <script src=\"{script_file}\"{' type=\"module\"' if script_is_module else ''}></script>
</body>
</html>"""

        return html_template

    def _obfuscate_vdom(self, vnode: dict) -> dict:
        """Produce a minimal VDOM structure keeping events but hiding code.
        - Keeps: type, id, key, class, text, children, events
        - Events: { evName: {t:'i', b:'<base64>'} }
        - Strips: style, props, any other keys
        Recurses through children.
        """
        if not isinstance(vnode, dict):
            return vnode
        import base64
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
        # text retained (non-sensitive content remains visible by choice)
        if 'text' in vnode:
            kept['text'] = vnode.get('text')
        # Obfuscate events
        evs = vnode.get('events') or None
        if isinstance(evs, dict) and evs:
            obf = {}
            for ev, spec in evs.items():
                try:
                    code = None
                    if isinstance(spec, dict):
                        # existing shapes: {type:'inline', code:'...'} or short-forms
                        code = spec.get('code') or spec.get('value')
                    elif isinstance(spec, str):
                        code = spec
                    if code:
                        b64 = base64.b64encode(code.encode('utf-8')).decode('ascii')
                        obf[ev] = {'t': 'i', 'b': b64}
                except Exception:
                    # if anything fails, skip this event
                    pass
            kept['events'] = obf if obf else None
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

    
    def _generate_meta_tags(self, app: App) -> str:
        """Genera todos los meta tags de la aplicación"""
        meta_tags = app.get_meta_tags()
        meta_html = []
        
        for name, content in meta_tags.items():
            if content:
                meta_html.append(f'    <meta name="{name}" content="{content}">')
        
        # Añadir canonical URL si está configurado
        if app.canonical_url:
            meta_html.append(f'    <link rel="canonical" href="{app.canonical_url}">')
        
        return '\n'.join(meta_html)
    
    def _generate_links(self, app: App) -> str:
        """Genera los enlaces en el head del HTML"""
        links = []
        
        # Favicon
        if hasattr(app, 'favicon'):
            links.append(f'<link rel="icon" href="{app.favicon}" type="image/x-icon">')
        
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
    def generate_custom_css(self, app: App) -> str:
        """Genera solo los estilos personalizados de la aplicación"""
        css_content = ""
        
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
        """Genera el contenido CSS base"""
        return """/* Estilos base de Dars */
* {
    box-sizing: border-box;
}

body {
    margin: 0;
    padding: 0;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
}

/* Estilos de componentes Dars */
.dars-container {
    display: block;
}

.dars-text {
    display: inline-block;
}

.dars-button {
    display: inline-block;
    padding: 8px 16px;
    border: 1px solid #ccc;
    background-color: #f8f9fa;
    color: #333;
    cursor: pointer;
    border-radius: 4px;
    font-size: 14px;
}

.dars-button:hover {
    background-color: #e9ecef;
}

.dars-button:disabled {
    opacity: 0.6;
    cursor: not-allowed;
}

.dars-input {
    display: inline-block;
    padding: 8px 12px;
    border: 1px solid #ccc;
    border-radius: 4px;
    font-size: 14px;
}

.dars-input:focus {
    outline: none;
    border-color: #007bff;
    box-shadow: 0 0 0 2px rgba(0, 123, 255, 0.25);
}

.dars-image {
    max-width: 100%;
    height: auto;
}

.dars-link {
    color: #007bff;
    text-decoration: none;
}

.dars-link:hover {
    text-decoration: underline;
}

.dars-textarea {
    width: 100%;
    padding: 8px 12px;
    border: 1px solid #ccc;
    border-radius: 4px;
    font-size: 14px;
}

.dars-textarea:focus {
    outline: none;
    border-color: #007bff;
    box-shadow: 0 0 0 2px rgba(0, 123, 255, 0.25);
}

.dars-card {
    background-color: white;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    padding: 20px;
    margin-bottom: 20px;
}

.dars-card h2 {
    margin-top: 0;
    margin-bottom: 15px;
    font-size: 24px;
    color: #333;
}

/* Table */
.dars-table {
    width: 100%;
    border-collapse: collapse;
    margin-bottom: 20px;
    background: white;
}
.dars-table th, .dars-table td {
    border: 1px solid #ddd;
    padding: 8px 12px;
    text-align: left;
}
.dars-table th {
    background: #f5f5f5;
    font-weight: bold;
}
.dars-table tr:nth-child(even) {
    background: #fafbfc;
}

/* Tabs */
.dars-tabs {
    margin-bottom: 20px;
}
.dars-tabs-header {
    display: flex;
    border-bottom: 2px solid #eee;
    margin-bottom: 10px;
}
.dars-tab {
    background: none;
    border: none;
    padding: 10px 20px;
    cursor: pointer;
    font-size: 16px;
    color: #555;
    border-bottom: 2px solid transparent;
    transition: border 0.2s, color 0.2s;
}
.dars-tab-active {
    color: #007bff;
    border-bottom: 2px solid #007bff;
    font-weight: bold;
}
.dars-tab-panel {
    display: none;
    padding: 16px 0;
}
.dars-tab-panel-active {
    display: block;
}

/* Accordion */
.dars-accordion {
    border-radius: 8px;
    overflow: hidden;
    background: #fff;
    margin-bottom: 20px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.06);
}
.dars-accordion-section {
    border-bottom: 1px solid #eee;
}
.dars-accordion-title {
    padding: 14px 20px;
    background: #f7f7f7;
    cursor: pointer;
    font-weight: 500;
    transition: background 0.2s;
}
.dars-accordion-section.dars-accordion-open .dars-accordion-title {
    background: #e9ecef;
}
.dars-accordion-content {
    display: none;
    padding: 16px 20px;
    background: #fafbfc;
}
.dars-accordion-section.dars-accordion-open .dars-accordion-content {
    display: block;
}

/* ProgressBar */
.dars-progressbar {
    width: 100%;
    background: #e9ecef;
    border-radius: 8px;
    overflow: hidden;
    height: 20px;
    margin-bottom: 20px;
}
.dars-progressbar-bar {
    height: 100%;
    background: linear-gradient(90deg, #007bff, #4a90e2);
    transition: width 0.3s;
}

/* Spinner */
.dars-spinner {
    border: 4px solid #e9ecef;
    border-top: 4px solid #007bff;
    border-radius: 50%;
    width: 36px;
    height: 36px;
    animation: dars-spin 1s linear infinite;
    margin: 10px auto;
}
@keyframes dars-spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

/* Tooltip */
.dars-tooltip {
    position: relative;
    display: inline-block;
    cursor: pointer;
}
.dars-tooltip .dars-tooltip-text {
    visibility: hidden;
    width: max-content;
    background: #333;
    color: #fff;
    text-align: center;
    border-radius: 4px;
    padding: 6px 10px;
    position: absolute;
    z-index: 10;
    opacity: 0;
    transition: opacity 0.2s;
    font-size: 13px;
    pointer-events: none;
}
.dars-tooltip:hover .dars-tooltip-text,
.dars-tooltip:focus .dars-tooltip-text {
    visibility: visible;
    opacity: 1;
}
.dars-tooltip-top .dars-tooltip-text {
    bottom: 125%;
    left: 50%;
    transform: translateX(-50%);
    margin-bottom: 6px;
}
.dars-tooltip-bottom .dars-tooltip-text {
    top: 125%;
    left: 50%;
    transform: translateX(-50%);
    margin-top: 6px;
}
.dars-tooltip-left .dars-tooltip-text {
    right: 125%;
    top: 50%;
    transform: translateY(-50%);
    margin-right: 6px;
}
.dars-tooltip-right .dars-tooltip-text {
    left: 125%;
    display: none; /* Hidden by default */
    position: fixed; /* Stay in place */
    z-index: 1; /* Sit on top */
    left: 0;
    top: 0;
    width: 100%; /* Full width */
    height: 100%; /* Full height */
    overflow: auto; /* Enable scroll if needed */
    background-color: rgba(0,0,0,0.4); /* Black w/ opacity */
    justify-content: center;
    align-items: center;
}
.dars-modal-hidden {
    display: none !important;
}

.dars-modal-content {
    background-color: #fefefe;
    margin: auto;
    padding: 20px;
    border: 1px solid #888;
    width: 80%;
    max-width: 500px;
    border-radius: 8px;
    box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2), 0 6px 20px 0 rgba(0,0,0,0.19);
}

.dars-navbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1rem;
    background-color: #f8f9fa;
    border-bottom: 1px solid #dee2e6;
}

.dars-navbar-brand {
    font-weight: bold;
    font-size: 1.25rem;
    color: #333;
}

.dars-navbar-nav {
    display: flex;
    gap: 1rem;
}

.dars-navbar-nav a {
    color: #007bff;
    text-decoration: none;
    padding: 0.5rem 1rem;
}

.dars-navbar-nav a:hover {
    background-color: #e9ecef;
    border-radius: 4px;
}

/* Estilos para nuevos componentes básicos */

/* Checkbox */
.dars-checkbox-wrapper {
    display: flex;
    align-items: center;
    gap: 8px;
    margin: 4px 0;
}

.dars-checkbox {
    width: 16px;
    height: 16px;
    cursor: pointer;
}

.dars-checkbox:disabled {
    opacity: 0.6;
    cursor: not-allowed;
}

.dars-checkbox-wrapper label {
    cursor: pointer;
    user-select: none;
}

/* RadioButton */
.dars-radio-wrapper {
    display: flex;
    align-items: center;
    gap: 8px;
    margin: 4px 0;
}

.dars-radio {
    width: 16px;
    height: 16px;
    cursor: pointer;
}

.dars-radio:disabled {
    opacity: 0.6;
    cursor: not-allowed;
}

.dars-radio-wrapper label {
    cursor: pointer;
    user-select: none;
}

/* Select */
.dars-select {
    display: inline-block;
    padding: 8px 12px;
    border: 1px solid #ccc;
    border-radius: 4px;
    font-size: 14px;
    background-color: white;
    cursor: pointer;
    min-width: 120px;
}

.dars-select:focus {
    outline: none;
    border-color: #007bff;
    box-shadow: 0 0 0 2px rgba(0, 123, 255, 0.25);
}

.dars-select:disabled {
    opacity: 0.6;
    cursor: not-allowed;
    background-color: #f8f9fa;
}

.dars-select option:disabled {
    color: #6c757d;
}

/* Slider */
.dars-slider-wrapper {
    display: flex;
    align-items: center;
    gap: 12px;
    margin: 8px 0;
}

.dars-slider-wrapper.dars-slider-vertical {
    flex-direction: column;
    align-items: stretch;
}

.dars-slider {
    flex: 1;
    cursor: pointer;
}

.dars-slider-horizontal .dars-slider {
    width: 100%;
    height: 6px;
}

.dars-slider-vertical input[type="range"] {
  width: 8px;
  height: 160px;
  writing-mode: vertical-lr;
  direction: rtl;
}

.dars-slider:disabled {
    opacity: 0.6;
    cursor: not-allowed;
}

.dars-slider-value {
    font-weight: bold;
    min-width: 40px;
    text-align: center;
    padding: 4px 8px;
    background-color: #f8f9fa;
    border-radius: 4px;
    font-size: 12px;
}

.dars-slider-wrapper label {
    font-weight: 500;
    margin-bottom: 4px;
}

/* DatePicker */
.dars-datepicker {
    display: inline-block;
    padding: 8px 12px;
    border: 1px solid #ccc;
    border-radius: 4px;
    font-size: 14px;
    background-color: white;
    cursor: pointer;
}

.dars-datepicker:focus {
    outline: none;
    border-color: #007bff;
    box-shadow: 0 0 0 2px rgba(0, 123, 255, 0.25);
}

.dars-datepicker:disabled {
    opacity: 0.6;
    cursor: not-allowed;
    background-color: #f8f9fa;
}

.dars-datepicker:readonly {
    background-color: #f8f9fa;
    cursor: default;
}

.dars-datepicker-inline {
    display: inline-block;
    border: 1px solid #ccc;
    border-radius: 4px;
    padding: 12px;
    background-color: white;
}

.dars-datepicker-inline .dars-datepicker {
    border: none;
    padding: 0;
}
/* Markdown Styles */
.dars-markdown {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
    line-height: 1.6;
    color: #333;
    background-color: #ffffff;
    padding: 20px;
    border-radius: 8px;
    transition: all 0.3s ease;
}

/* Dark Theme */
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

.dars-markdown-dark p {
    color: #cccccc;
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

.dars-markdown-dark ul,
.dars-markdown-dark ol {
    color: #cccccc;
}

.dars-markdown li {
    margin-bottom: 0.5em;
}

.dars-markdown code {
    background-color: #f6f8fa;
    padding: 0.2em 0.4em;
    border-radius: 3px;
    font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
    font-size: 0.85em;
    color: #333;
}

.dars-markdown-dark code {
    background-color: #2d2d2d;
    color: #e0e0e0;
}

.dars-markdown pre {
    background-color: #f6f8fa;
    padding: 1em;
    border-radius: 3px;
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
}

.dars-markdown blockquote {
    border-left: 4px solid #ddd;
    padding-left: 1em;
    margin-left: 0;
    color: #666;
    font-style: italic;
    background-color: #f9f9f9;
    padding: 10px 15px;
    border-radius: 4px;
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

.dars-markdown-dark table {
    border-color: #444;
}

.dars-markdown th,
.dars-markdown td {
    border: 1px solid #ddd;
    padding: 0.5em;
    text-align: left;
}

.dars-markdown-dark th,
.dars-markdown-dark td {
    border-color: #444;
    color: #e0e0e0;
}

.dars-markdown th {
    background-color: #f6f8fa;
    font-weight: 600;
}

.dars-markdown-dark th {
    background-color: #333;
}

.dars-markdown a {
    color: #0366d6;
    text-decoration: none;
}

.dars-markdown-dark a {
    color: #4da6ff;
}

.dars-markdown a:hover {
    text-decoration: underline;
}

.dars-markdown-dark a:hover {
    color: #66b3ff;
}

.dars-markdown img {
    max-width: 100%;
    height: auto;
    border-radius: 4px;
}

.dars-markdown-dark img {
    filter: brightness(0.9);
}

/* Horizontal Rule */
.dars-markdown hr {
    border: none;
    height: 1px;
    background-color: #ddd;
    margin: 2em 0;
}

.dars-markdown-dark hr {
    background-color: #444;
}
"""

    def build_vdom_tree(self, component: Component) -> dict:
        """Serializa un componente Dars a un VNode (snapshot VDOM para hidratación)."""
        try:
            comp_type = component.__class__.__name__
        except Exception:
            comp_type = 'Component'

        comp_id = self.get_component_id(component)

        # Serializar eventos (solo inline ejecutable en cliente)
        events_payload = {}
        try:
            events = getattr(component, 'events', {}) or {}
            for ev_name, handler in events.items():
                code = None
                try:
                    if hasattr(handler, 'get_code'):
                        code = handler.get_code()
                    elif hasattr(handler, 'code'):
                        code = getattr(handler, 'code')
                    elif hasattr(handler, 'to_js'):
                        code = handler.to_js()
                    elif isinstance(handler, str):
                        code = handler
                except Exception:
                    code = None
                if code:
                    try:
                        code_str = str(code)
                    except Exception:
                        code_str = ''
                    if code_str:
                        events_payload[ev_name] = { 'type': 'inline', 'code': code_str }
        except Exception:
            events_payload = {}

        # Props seguros (evitar funciones y objetos no serializables)
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
            'events': events_payload if events_payload else None,
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

    def generate_javascript(self, app: App, page_root: Component) -> str:
        """Genera un runtime modular: hidratación + delegación de eventos + diff/patch + hot-reload incremental (polling)."""
        runtime = r"""// Dars Runtime (Hydration + Delegated Events + Diff/Patch + Hot Reload)
(function(){
  const eventMap = new Map(); // id -> {ev: fn}
  let currentSnapshot = null;
  let currentVersion = null;

  // Registro de componentes (skeleton). En siguientes iteraciones añadiremos create/patch por tipo built-in
  const registry = {
    // Implementación mínima segura para crear nodos cuando se agregan hijos
    'Text': {
      create(v){
        if(!v || v.isIsland) return null;
        const el = document.createElement('span');
        if(v.id) el.id = v.id;
        if(v.class) el.className = v.class;
        if(v.style){ for(const k in v.style){ try{ el.style.setProperty(k.replace(/_/g,'-'), String(v.style[k])); }catch{} } }
        if(Object.prototype.hasOwnProperty.call(v,'text')){ el.textContent = String(v.text||''); }
        // props
        if(v.props){ for(const k in v.props){ const val=v.props[k]; try{ if(val===false||val===null||typeof val==='undefined'){ el.removeAttribute(k);} else { el.setAttribute(k, String(val)); } }catch{} } }
        return el;
      }
    },
    'Container': {
      create(v){
        if(!v || v.isIsland) return null;
        const el = document.createElement('div');
        if(v.id) el.id = v.id;
        const base = 'dars-container';
        el.className = (v.class ? (base + ' ' + v.class) : base);
        if(v.style){ for(const k in v.style){ try{ el.style.setProperty(k.replace(/_/g,'-'), String(v.style[k])); }catch{} } }
        // props
        if(v.props){ for(const k in v.props){ const val=v.props[k]; try{ if(val===false||val===null||typeof val==='undefined'){ el.removeAttribute(k);} else { el.setAttribute(k, String(val)); } }catch{} } }
        return el;
      }
    },
  };

  function walk(v, fn){
    if(!v) return;
    fn(v);
    const ch = v.children || [];
    for(let i=0;i<ch.length;i++){ walk(ch[i], fn); }
  }

  function _decodeCodeB64(b64){
    try {
      if (typeof atob === 'function') return atob(b64);
      if (typeof Buffer !== 'undefined') { return Buffer.from(b64, 'base64').toString('utf8'); }
    } catch(_){ }
    return '';
  }

  function _compileHandlerFromSpec(spec){
    try {
      if (!spec) return null;
      if (spec && spec.type === 'inline' && spec.code) {
        return new Function('event', spec.code);
      }
      const b64 = (spec && (spec.b || spec.code_b64)) || null;
      if (b64){
        const code = _decodeCodeB64(b64);
        if (code) return new Function('event', code);
      }
    } catch(_){ }
    return null;
  }

  function bindEventsFromVNode(snapshot){
    // Construir tabla de eventos a partir del snapshot
    walk(snapshot, (v)=>{
      if(v && v.id && v.events){
        const handlers = {};
        for(const ev in v.events){
          const spec = v.events[ev];
          const fn = _compileHandlerFromSpec(spec);
          if (fn) { handlers[ev] = fn; }
        }
        if(Object.keys(handlers).length){ eventMap.set(v.id, handlers); } else { eventMap.delete(v.id); }
      }
    });
  }

  // Utilities
  function setProps(el, props){
    if(!el || !props) return;
    for(const [k,v] of Object.entries(props)){
      try {
        if(v === false || v === null || typeof v === 'undefined'){
          el.removeAttribute(k);
        } else {
          el.setAttribute(k, String(v));
        }
      } catch(err) { /* ignore */ }
    }
  }
  function diffProps(el, oldP={}, newP={}){
    // remove
    for(const k in oldP){ if(!(k in newP)){ try{ el.removeAttribute(k); }catch{} } }
    // add/update
    for(const k in newP){ const v=newP[k]; try{ if(v===false||v===null||typeof v==='undefined'){ el.removeAttribute(k);} else { el.setAttribute(k, String(v)); } }catch{} }
  }
  function diffStyles(el, oldS={}, newS={}){
    for(const k in oldS){ if(!(k in newS)){ try{ el.style.removeProperty(k.replace(/_/g,'-')); }catch{} } }
    for(const k in newS){ const v=newS[k]; try{ el.style.setProperty(k.replace(/_/g,'-'), String(v)); }catch{} }
  }

  // Event delegation helper (restored)
  function delegate(eventName, root){
    (root||document).addEventListener(eventName, function(e){
      let node = e.target;
      const boundary = root||document;
      while(node && node !== boundary){
        const id = node.id;
        if(id && eventMap.has(id)){
          const handlers = eventMap.get(id);
          const h = handlers[eventName];
          // If there is a dynamic handler attached on this node for the same event, let it handle and skip default
          if(node && node.__darsEv && node.__darsEv[eventName]){
            return;
          }
          if(typeof h === 'function'){
            try { h.call(node, e); } catch(err){ console.error('[Dars] handler error', err); }
            return;
          }
        }
        node = node.parentNode;
      }
    }, true);
  }

  function typesDiffer(a,b){ return (a && b) ? a.type !== b.type : a!==b; }

  // Elimina un subárbol del DOM (y del mapa de eventos) usando los ids del VDOM
  function removeSubtree(v){
    if(!v) return;
    // eliminar hijos primero (postorden)
    const ch = (v.children||[]);
    for(let i=0;i<ch.length;i++){ removeSubtree(ch[i]); }
    // limpiar handlers
    if(v.id){ eventMap.delete(v.id); }
    // quitar elemento del DOM
    if(v.id){ const el = document.getElementById(v.id); if(el && el.parentNode){ try{ el.parentNode.removeChild(el); }catch(_){} }}
  }

  function updateNode(oldV, newV){
    if(!newV || !newV.id){ return { ok:false, reason:'missing-new' }; }
    let el = document.getElementById(newV.id);
    if(!el){
      // Fallback: si cambió el id entre snapshots pero es el mismo nodo lógico, reasignamos id
      const oldEl = (oldV && oldV.id) ? document.getElementById(oldV.id) : null;
      if(oldEl){ try { oldEl.id = newV.id; el = oldEl; } catch(_){} }
    }
    if(!el){ return { ok:false, reason:'missing-el' }; }

    // Si cambia el tipo, estructura u orden de hijos, pedimos reload completo (fase 2 simplificada)
    if(typesDiffer(oldV, newV)){
      return { ok:false, reason:'type-changed' };
    }

    const isIsland = !!newV.isIsland;

    // class -> atributo className
    if(!isIsland && newV.class){ el.className = newV.class; }

    // props
    if(!isIsland){ diffProps(el, (oldV&&oldV.props)||{}, newV.props||{}); }

    // styles
    if(!isIsland){ diffStyles(el, (oldV&&oldV.style)||{}, newV.style||{}); }

    // text
    if(!isIsland && Object.prototype.hasOwnProperty.call(newV, 'text')){
      if(el.textContent !== String(newV.text||'')){
        el.textContent = String(newV.text||'');
      }
    }

    // events
    if(newV.events){
      const handlers = {};
      for(const ev in newV.events){
        const spec = newV.events[ev];
        const fn = _compileHandlerFromSpec(spec);
        if (fn) { handlers[ev] = fn; }
      }
      if(Object.keys(handlers).length){ eventMap.set(newV.id, handlers); } else { eventMap.delete(newV.id); }
    } else {
      eventMap.delete(newV.id);
    }

    // hijos (reconciliación por id/key). Para islas, tratamos el subárbol como opaco.
    if(isIsland){ return { ok:true }; }

    // Permitimos REMOCIONES sin recarga.
    const oldC = (oldV && oldV.children) ? oldV.children : [];
    const newC = (newV.children) ? newV.children : [];

    // Construir índice de hijos viejos por id o key
    const oldIndex = new Map(); // clave -> vnode viejo
    for(let i=0;i<oldC.length;i++){
      const k = (oldC[i] && (oldC[i].id || oldC[i].key)) || null;
      if(k){ oldIndex.set(String(k), oldC[i]); }
    }

    // Seguimiento de cuáles viejos fueron actualizados
    const seenOld = new Set();

    // Actualizar/validar hijos nuevos
    for(let i=0;i<newC.length;i++){
      const newChild = newC[i];
      const k = (newChild && (newChild.id || newChild.key)) || null;
      if(!k){
        // sin id/key fiable: conservador => usar reconciliación por índice si existe par
        if(i < oldC.length){
          const r = updateNode(oldC[i], newChild);
          if(!r.ok){ return r; }
          seenOld.add(oldC[i]);
          continue;
        } else {
          // no podemos crear de forma segura
          return { ok:false, reason:'children-added' };
        }
      }
      const oldChild = oldIndex.get(String(k));
      if(oldChild){
        const r = updateNode(oldChild, newChild);
        if(!r.ok){ return r; }
        seenOld.add(oldChild);
      } else {
        // Fallback conservador: si hay viejo en la misma posición y el tipo coincide, lo reutilizamos
        if(i < oldC.length){
          const candidate = oldC[i];
          if(!typesDiffer(candidate, newChild)){
            const r = updateNode(candidate, newChild);
            if(!r.ok){ return r; }
            seenOld.add(candidate);
            continue;
          }
        }
        // Intentar crear subárbol si es un tipo soportado por el registry (no isla)
        const subtree = createSubtree(newChild);
        if(subtree){
          // insertar en la posición i dentro del DOM
          const refChildVNode = (i < oldC.length) ? oldC[i] : null;
          if(refChildVNode && refChildVNode.id){
            const refEl = document.getElementById(refChildVNode.id);
            if(refEl && refEl.parentNode){ refEl.parentNode.insertBefore(subtree, refEl); }
            else { el.appendChild(subtree); }
          } else {
            el.appendChild(subtree);
          }
          // marcar como visto (no había old), nada que añadir a seenOld
          continue;
        }
        // hijo nuevo de tipo no soportado => recarga por seguridad
        return { ok:false, reason:'children-added' };
      }
    }

    // Eliminar los viejos no vistos (removidos)
    for(let i=0;i<oldC.length;i++){
      const v = oldC[i];
      if(!seenOld.has(v)){
        removeSubtree(v);
      }
    }
    return { ok:true };
  }

  function schedule(fn){
    if(typeof requestAnimationFrame === 'function'){
      requestAnimationFrame(fn);
    } else { setTimeout(fn, 16); }
  }

  function update(newSnapshot){
    const old = currentSnapshot;
    if(!old){
      // primera vez: solo (re)hidratar eventos
      bindEventsFromVNode(newSnapshot);
      currentSnapshot = newSnapshot;
      try{ window.__DARS_VDOM__ = newSnapshot; }catch(_){ /* ignore */ }
      return;
    }
    schedule(()=>{
      const res = updateNode(old, newSnapshot);
      if(!res.ok){
        console.warn('[Dars] Structural change detected (', res.reason, '), reloading...');
        try { location.reload(); } catch(e) { /* ignore */ }
        return;
      }
      // Re-vincular mapa de eventos por si cambió
      bindEventsFromVNode(newSnapshot);
      currentSnapshot = newSnapshot;
      try{ window.__DARS_VDOM__ = newSnapshot; }catch(_){ /* ignore */ }
    });
  }

  function hydrate(snapshot){
    bindEventsFromVNode(snapshot);
    currentSnapshot = snapshot;
    try{ window.__DARS_VDOM__ = snapshot; }catch(_){ /* ignore */ }

    // Delegar eventos comunes (extendido)
    const delegated = [
      'click','dblclick',
      'mousedown','mouseup','mouseenter','mouseleave','mousemove',
      'keydown','keyup','keypress',
      'change','input','submit',
      'focus','blur'
    ];
    delegated.forEach(ev => delegate(ev, document));
  }

  function startHotReload(){
    const vurl = (window.__DARS_VERSION_URL || 'version.txt');
    let timer = null;
    let warnedVersionMissing = false;

    function httpGet(url, onSuccess, onError, responseType){
      try{
        const xhr = new XMLHttpRequest();
        if(responseType){ xhr.responseType = responseType; }
        xhr.open('GET', url, true);
        xhr.timeout = 5000;
        xhr.onreadystatechange = function(){
          if(xhr.readyState === 4){
            if(xhr.status >= 200 && xhr.status < 300){
              onSuccess(xhr.response);
            } else {
              onError();
            }
          }
        };
        xhr.onerror = onError;
        xhr.ontimeout = onError;
        xhr.setRequestHeader('Cache-Control', 'no-store');
        xhr.send();
      }catch(e){ onError(); }
    }

    function tick(){
      httpGet(vurl, function(text){
        let ver = (text || '').toString().trim();
        if(ver){ warnedVersionMissing = false; }
        if(!currentVersion){ currentVersion = ver; }
        if(ver && ver !== currentVersion){
          currentVersion = ver;
          // Política solicitada: siempre recargar por completo al detectar nueva versión
          try { location.reload(); } catch(_) {}
          return;
        }
        timer = setTimeout(tick, 600);
      }, function(){
        if(!warnedVersionMissing){ console.log('[Dars] waiting for version.txt'); warnedVersionMissing = true; }
        timer = setTimeout(tick, 600);
      }, 'text');
    }
    tick();
    return ()=>{ if(timer) clearTimeout(timer); };
  }

  document.addEventListener('DOMContentLoaded', function(){
    if(window.__DARS_VDOM__){
      hydrate(window.__DARS_VDOM__);
    } else {
      console.warn('[Dars] No VDOM snapshot found for hydration');
    }
    // Activar hot-reload incremental en dev si hay URLs definidas
    if(window.__DARS_VERSION_URL && window.__DARS_SNAPSHOT_URL){
      startHotReload();
    }
  });
})();
"""
        return runtime

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

    def render_component(self, component: Component) -> str:
        if not isinstance(component, Component):
            raise TypeError(f"render_component wait to recived an instance of Component, but recive an {component}")
        """Render an HTML component"""
        from dars.components.basic.page import Page
        from dars.components.layout.grid import GridLayout
        from dars.components.layout.flex import FlexLayout
        
        
        # Lista de componentes built-in de Dars que NO deben usar su propio método render()
        builtin_components = [
            Page, GridLayout, FlexLayout, Text, Button, Input, Container, Image, Link, 
            Textarea, Card, Modal, Navbar, Checkbox, RadioButton, Select, Slider, 
            DatePicker, Table, Tabs, Accordion, ProgressBar, Spinner, Tooltip, Markdown,
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
        
        return f'<span id="{component_id}" {class_attr} {style_attr}>{text.text}</span>'
        
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
        disabled_attr = "disabled" if button.disabled else ""
        
        return f'<button id="{component_id}" {class_attr} {style_attr} {type_attr} {disabled_attr}>{button.text}</button>'
        
    def render_input(self, input_comp: Input) -> str:
        """Renderiza un componente Input"""
        component_id = self.get_component_id(input_comp, prefix="input")
        class_attr = f'class="dars-input {input_comp.class_name or ""}"'
        style_attr = f'style="{self.render_styles(input_comp.style)}"' if input_comp.style else ""
        type_attr = f'type="{input_comp.input_type}"'
        value_attr = f'value="{input_comp.value}"' if input_comp.value else ""
        placeholder_attr = f'placeholder="{input_comp.placeholder}"' if input_comp.placeholder else ""
        disabled_attr = "disabled" if input_comp.disabled else ""
        readonly_attr = "readonly" if input_comp.readonly else ""
        required_attr = "required" if input_comp.required else ""
        
        attrs = [class_attr, style_attr, type_attr, value_attr, placeholder_attr, 
                disabled_attr, readonly_attr, required_attr]
        attrs_str = " ".join(attr for attr in attrs if attr)
        
        return f'<input id="{component_id}" {attrs_str} />'
        
    def render_container(self, container: Container) -> str:
        """Renderiza un componente Container"""
        component_id = self.get_component_id(container, prefix="container")
        class_attr = f'class="dars-container {container.class_name or ""}"'
        style_attr = f'style="{self.render_styles(container.style)}"' if container.style else ""

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

        return f'<div id="{component_id}" {class_attr} {style_attr}>{children_html}</div>'
        
    def render_image(self, image: Image) -> str:
        """Renderiza un componente Image"""
        component_id = self.get_component_id(image, prefix="image")
        class_attr = f'class="dars-image {image.class_name or ""}"'
        style_attr = f'style="{self.render_styles(image.style)}"' if image.style else ""
        width_attr = f'width="{image.width}"' if image.width else ""
        height_attr = f'height="{image.height}"' if image.height else ""

        return f'<img id="{component_id}" src="{image.src}" alt="{image.alt}" {width_attr} {height_attr} {class_attr} {style_attr} />'

    def render_link(self, link: Link) -> str:
        """Renderiza un componente Link"""
        component_id = self.get_component_id(link, prefix="link")
        class_attr = f'class="dars-link {link.class_name or ""}"'
        style_attr = f'style="{self.render_styles(link.style)}"' if link.style else ""
        target_attr = f'target="{link.target}"'

        return f'<a id="{component_id}" href="{link.href}" {target_attr} {class_attr} {style_attr}>{link.text}</a>'

    def render_textarea(self, textarea: Textarea) -> str:
        """Renderiza un componente Textarea"""
        component_id = self.get_component_id(textarea, prefix="textarea")
        class_attr = f'class="dars-textarea {textarea.class_name or ""}"'
        style_attr = f'style="{self.render_styles(textarea.style)}"' if textarea.style else ""
        rows_attr = f'rows="{textarea.rows}"'
        cols_attr = f'cols="{textarea.cols}"'
        placeholder_attr = f'placeholder="{textarea.placeholder}"' if textarea.placeholder else ""
        disabled_attr = "disabled" if textarea.disabled else ""
        readonly_attr = "readonly" if textarea.readonly else ""
        required_attr = "required" if textarea.required else ""
        maxlength_attr = f'maxlength="{textarea.max_length}"' if textarea.max_length else ""

        attrs = [class_attr, style_attr, rows_attr, cols_attr, placeholder_attr,
                 disabled_attr, readonly_attr, required_attr, maxlength_attr]
        attrs_str = " ".join(attr for attr in attrs if attr)

        return f'<textarea id="{component_id}" {attrs_str}>{textarea.value}</textarea>'

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
        checked_attr = "checked" if checkbox.checked else ""
        disabled_attr = "disabled" if checkbox.disabled else ""
        required_attr = "required" if checkbox.required else ""
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
        checked_attr = "checked" if radio.checked else ""
        disabled_attr = "disabled" if radio.disabled else ""
        required_attr = "required" if radio.required else ""
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
        disabled_attr = "disabled" if select.disabled else ""
        required_attr = "required" if select.required else ""
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
        disabled_attr = "disabled" if slider.disabled else ""
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
                extras=["fenced-code-blocks", "tables", "header-ids"]
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
        
        return f'<div id="{component_id}" {class_attr} {style_attr}>{html_content}</div>'

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
