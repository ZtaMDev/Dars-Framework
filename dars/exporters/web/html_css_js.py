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
from typing import Dict, Any
import os
from bs4 import BeautifulSoup

class HTMLCSSJSExporter(Exporter):
    """Exportador para HTML, CSS y JavaScript"""
    
    def get_platform(self) -> str:
        return "html"
        
    def export(self, app: App, output_path: str) -> bool:
        """Exporta la aplicación a HTML/CSS/JS (soporta multipágina)."""
        try:
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

            # Generar CSS global (compartido)
            css_content = self.generate_css(app)
            self.write_file(os.path.join(output_path, "styles.css"), css_content)

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
                    script_js = self._generate_combined_script_js(page_scripts)
                    
                    if index_page is not None and page is index_page:
                        # Página index
                        self.write_file(os.path.join(output_path, "script.js"), script_js)
                        html_content = self.generate_html(page_app, css_file="styles.css", 
                                                        script_file="script.js", 
                                                        runtime_file="runtime_dars.js")
                        filename = "index.html"
                    else:
                        # Otras páginas
                        script_name = f"script_{slug}.js"
                        self.write_file(os.path.join(output_path, script_name), script_js)
                        html_content = self.generate_html(page_app, css_file="styles.css", 
                                                        script_file=script_name, 
                                                        runtime_file=runtime_name)
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
                script_js = self._generate_combined_script_js(user_scripts)
                self.write_file(os.path.join(output_path, "script.js"), script_js)
                
                html_content = self.generate_html(app, css_file="styles.css", 
                                                script_file="script.js", 
                                                runtime_file="runtime_dars.js")
                try:
                    soup = BeautifulSoup(html_content, "html.parser")
                    html_content = soup.prettify()
                except ImportError:
                    pass
                
                self.write_file(os.path.join(output_path, "index.html"), html_content)

            # Generar archivos PWA si está habilitado
            if getattr(app, 'pwa_enabled', False):
                self._generate_pwa_files(app, output_path)

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
            # Si el usuario define iconos personalizados
            icons_manifest = []
            icons_dir = os.path.join(output_path, "icons")
            os.makedirs(icons_dir, exist_ok=True)
            for icon in user_icons:
                if isinstance(icon, dict):
                    src = icon.get("src")
                    if src and os.path.isfile(src):
                        # Copiamos el icono al output
                        dest_path = os.path.join(icons_dir, os.path.basename(src))
                        shutil.copy(src, dest_path)
                        icon["src"] = f"icons/{os.path.basename(src)}"
                    icons_manifest.append(icon)
                elif isinstance(icon, str):
                    # Si solo es una ruta, la copiamos y generamos el dict
                    if os.path.isfile(icon):
                        dest_path = os.path.join(icons_dir, os.path.basename(icon))
                        shutil.copy(icon, dest_path)
                        icons_manifest.append({
                            "src": f"icons/{os.path.basename(icon)}",
                            "sizes": "192x192",
                            "type": "image/png",
                            "purpose": "any maskable"
                        })
            return icons_manifest if icons_manifest else None
        # Si no hay icons definidos, ponemos por defecto
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

    def _generate_combined_script_js(self, scripts):
        """Combina y concatena el código de todos los scripts específicos de la página"""
        js = "// Scripts específicos de esta página\n"
        js += "document.addEventListener('DOMContentLoaded', function() {\n"
        
        for script in scripts:
            if hasattr(script, 'get_code'):
                js += f"    // Script: {script.__class__.__name__}\n"
                code = script.get_code().strip()
                # Asegurar que el código esté dentro del contexto DOMContentLoaded
                if not code.startswith('document.addEventListener'):
                    js += f"    {code}\n"
                else:
                    js += f"{code}\n"
                js += "\n"
        
        js += "});\n"
        return js

    def generate_html(self, app: App, css_file: str = "styles.css", 
                 script_file: str = "script.js", runtime_file: str = "runtime_dars.js") -> str:
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
        
        html_template = f"""<!DOCTYPE html>
<html lang="{app.language}">
<head>
    <meta charset="{app.config.get('charset', 'UTF-8')}">
    {meta_tags_html}
    <title>{app.title}</title>
    {links_html}
    {og_tags_html}
    {twitter_tags_html}
    <link rel=\"stylesheet\" href=\"https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css\">\n    <link rel=\"stylesheet\" href=\"{css_file}\">
</head>
<body>
    {body_content}
    <script src=\"{runtime_file}\"></script>
    <script src=\"{script_file}\"></script>
</body>
</html>"""

        return html_template

    
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
        
    def generate_css(self, app: App) -> str:
        """Genera el contenido CSS"""
        css_content = """/* Estilos base de Dars */
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

"""
        
        # Agregar estilos globales de la aplicación definidos por el usuario
        for selector, styles in app.global_styles.items():
            css_content += f"{selector} {{\n"
            css_content += f"    {self.render_styles(styles)}\n"
            css_content += "}\n\n"
            
        return css_content
        
    def generate_javascript(self, app: App, page_root: Component) -> str:
        """Genera el contenido JavaScript específico para una página"""
        js_content = """// Dars Runtime - Página específica
    document.addEventListener('DOMContentLoaded', function() {
        console.log('Dars App loaded');
        
        // Inicializar eventos de componentes
        initializeEvents();
    });

    function initializeEvents() {
        // Los eventos específicos se agregarán aquí
    """

        # Función para detectar componentes con lógica mínima
        def has_component_type_with_logic(component, cls):
            if isinstance(component, cls) and getattr(component, 'minimum_logic', True):
                return True
            
            # Recursión para buscar en hijos
            children = getattr(component, 'children', [])
            if not isinstance(children, list):
                children = []
            
            for child in children:
                if has_component_type_with_logic(child, cls):
                    return True
            return False

        # Verificar si la página contiene componentes específicos
        has_tabs_logic = has_component_type_with_logic(page_root, Tabs)
        has_accordion_logic = has_component_type_with_logic(page_root, Accordion)

        if has_tabs_logic:
            js_content += "    // Tabs interactivas\n"
            js_content += """    document.querySelectorAll('.dars-tabs').forEach(function(tabsEl) {
        const tabButtons = tabsEl.querySelectorAll('.dars-tab');
        const panels = tabsEl.querySelectorAll('.dars-tab-panel');
        tabButtons.forEach(function(btn, i) {
            btn.addEventListener('click', function() {
                tabButtons.forEach(b => b.classList.remove('dars-tab-active'));
                panels.forEach(p => p.classList.remove('dars-tab-panel-active'));
                btn.classList.add('dars-tab-active');
                if (panels[i]) panels[i].classList.add('dars-tab-panel-active');
            });
        });
    });\n"""
        
        if has_accordion_logic:
            js_content += "    // Accordion interactivo\n"
            js_content += """    document.querySelectorAll('.dars-accordion').forEach(function(accEl) {
        accEl.querySelectorAll('.dars-accordion-title').forEach(function(titleEl) {
            titleEl.addEventListener('click', function() {
                const section = titleEl.parentElement;
                const isOpen = section.classList.contains('dars-accordion-open');
                if (isOpen) {
                    section.classList.remove('dars-accordion-open');
                } else {
                    // Si es acordeón exclusivo, cerrar otros
                    accEl.querySelectorAll('.dars-accordion-section').forEach(function(sec) {
                        sec.classList.remove('dars-accordion-open');
                    });
                    section.classList.add('dars-accordion-open');
                }
            });
        });
    });\n"""
        
        js_content += "}\n\n"

        # Lógica para asociar eventos Script a componentes específicos de esta página
        js_content += "// Asociación automática de eventos Script para esta página\n"
        
        from dars.scripts.script import Script
        
        def traverse_and_bind_events(component, js_lines):
            comp_id = getattr(component, 'id', None)
            
            # Si no tiene ID pero tiene eventos, generamos uno temporal
            if not comp_id and hasattr(component, 'events') and component.events:
                import uuid
                comp_id = f"comp_{str(uuid.uuid4())[:8]}"
                component.id = comp_id
            
            if comp_id and hasattr(component, 'events') and component.events:
                events = getattr(component, 'events', {})
                
                for event_name, handler in events.items():
                    if isinstance(handler, Script):
                        dom_event = event_name.lower()
                        code = handler.get_code().strip()
                        import re
                        m = re.search(r"function\s+([a-zA-Z0-9_]+)\s*\(", code, re.DOTALL | re.MULTILINE)
                        if m:
                            func_name = m.group(1)
                            js_lines.append(code)
                            js_line = f"document.getElementById('{comp_id}').on{dom_event} = {func_name};"
                            js_lines.append(js_line)
                        else:
                            js_line = f"document.getElementById('{comp_id}').on{dom_event} = function(event) {{\n{code}\n}};"
                            js_lines.append(js_line)
            
            # Recursivo en hijos
            children = getattr(component, 'children', [])
            if children and isinstance(children, (list, tuple)):
                for child in children:
                    if child is not None:
                        traverse_and_bind_events(child, js_lines)
        
        # Recorrer el árbol de componentes de esta página
        js_lines = []
        traverse_and_bind_events(page_root, js_lines)
        js_content += "\n".join(js_lines) + "\n"
            
        return js_content
        
    def render_component(self, component: Component) -> str:
        """Renderiza un componente a HTML"""
        from dars.components.basic.page import Page
        from dars.components.layout.grid import GridLayout
        from dars.components.layout.flex import FlexLayout
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
        else:
            # Componente genérico
            return self.render_generic_component(component)

    def render_grid(self, grid):
        """Renderiza un GridLayout como un div con CSS grid."""
        component_id = self.generate_unique_id(grid)
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
        component_id = self.generate_unique_id(flex)
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
        component_id = self.generate_unique_id(text)
        class_attr = f'class="dars-text {text.class_name or ""}"'
        style_attr = f'style="{self.render_styles(text.style)}"' if text.style else ""
        
        return f'<span id="{component_id}" {class_attr} {style_attr}>{text.text}</span>'
        
    def render_button(self, button: Button) -> str:
        """Renderiza un componente Button"""
        # Asegurarse de que el botón tenga un ID
        if not hasattr(button, 'id') or not button.id:
            import uuid
            button.id = f"btn_{str(uuid.uuid4())[:8]}"
            
        component_id = self.generate_unique_id(button)
        class_attr = f'class="dars-button {button.class_name or ""}"'
        style_attr = f'style="{self.render_styles(button.style)}"' if button.style else ""
        type_attr = f'type="{button.button_type}"'
        disabled_attr = "disabled" if button.disabled else ""
        
        return f'<button id="{button.id}" {class_attr} {style_attr} {type_attr} {disabled_attr}>{button.text}</button>'
        
    def render_input(self, input_comp: Input) -> str:
        """Renderiza un componente Input"""
        component_id = self.generate_unique_id(input_comp)
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
        component_id = self.generate_unique_id(container)
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
        component_id = self.generate_unique_id(image)
        class_attr = f'class="dars-image {image.class_name or ""}"'
        style_attr = f'style="{self.render_styles(image.style)}"' if image.style else ""
        width_attr = f'width="{image.width}"' if image.width else ""
        height_attr = f'height="{image.height}"' if image.height else ""

        return f'<img id="{component_id}" src="{image.src}" alt="{image.alt}" {width_attr} {height_attr} {class_attr} {style_attr} />'

    def render_link(self, link: Link) -> str:
        """Renderiza un componente Link"""
        component_id = self.generate_unique_id(link)
        class_attr = f'class="dars-link {link.class_name or ""}"'
        style_attr = f'style="{self.render_styles(link.style)}"' if link.style else ""
        target_attr = f'target="{link.target}"'

        return f'<a id="{component_id}" href="{link.href}" {target_attr} {class_attr} {style_attr}>{link.text}</a>'

    def render_textarea(self, textarea: Textarea) -> str:
        """Renderiza un componente Textarea"""
        component_id = self.generate_unique_id(textarea)
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
        component_id = self.generate_unique_id(card)
        class_attr = f'class="dars-card {card.class_name or ""}"'
        style_attr = f'style="{self.render_styles(card.style)}"' if card.style else ""
        title_html = f'<h2>{card.title}</h2>' if card.title else ""
        children_html = ""
        for child in card.children:
            children_html += self.render_component(child)

        return f'<div id="{component_id}" {class_attr} {style_attr}>{title_html}{children_html}</div>'

    def render_modal(self, modal: Modal) -> str:
        """Renderiza un componente Modal"""
        component_id = self.generate_unique_id(modal)
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
        component_id = self.generate_unique_id(navbar)
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
        component_id = self.generate_unique_id(checkbox)
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
        component_id = self.generate_unique_id(radio)
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
        component_id = self.generate_unique_id(select)
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
        component_id = self.generate_unique_id(slider)
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
        component_id = self.generate_unique_id(datepicker)
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

    def render_generic_component(self, component: Component) -> str:
        """Renderiza un componente genérico"""
        component_id = self.generate_unique_id(component)
        class_attr = f'class="{component.class_name or ""}"'
        style_attr = f'style="{self.render_styles(component.style)}"' if component.style else ""
        
        # Renderizar hijos
        children_html = ""
        for child in component.children:
            children_html += self.render_component(child)
            
        return f'<div id="{component_id}" {class_attr} {style_attr}>{children_html}</div>'


