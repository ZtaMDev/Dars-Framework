"""
SSR (Server-Side Rendering) Backend Helper for Dars Framework

This module provides utilities to render Dars components server-side
and create FastAPI endpoints automatically for SSR routes.
"""

from typing import Dict, Any, Optional
import json
from fastapi import FastAPI, Request, HTTPException
from dars.core.app import App
from dars.core.route_types import RouteType
from dars.exporters.web.html_css_js import HTMLCSSJSExporter, DarsJSONEncoder
from dars.exporters.web.vdom import VDomBuilder
import copy


class SSRRenderer:
    """
    Renders Dars components server-side using the HTMLCSSJSExporter.
    """
    
    def __init__(self, app: App):
        """
        Initialize SSR renderer with a Dars App instance.
        
        Args:
            app: Dars App instance containing routes to render
        """
        self.app = app
    
    def _prepare_scripts_in_memory(self, scripts) -> str:
        """
        Process scripts in memory without writing to disk.
        - Inline code is concatenated.
        - Local files are read and interpreted as inline code (to be served by backend).
        - Remote URLs are kept as external scripts (to be loaded by client).
        """
        combined_js = []
        import os
        
        # Try to determine project root
        app_source = getattr(self.app, '__source__', None)
        project_root = os.getcwd() if not app_source else os.path.dirname(os.path.abspath(app_source))

        for script in scripts or []:
            # 1. Object with get_code() (e.g. dScript)
            try:
                if hasattr(script, 'get_code'):
                    code = script.get_code()
                    if code:
                        combined_js.append(f"// Script: {getattr(script, '__class__', type(script)).__name__}\n{code.strip()}")
                    continue
            except Exception:
                pass

            # 2. Dictionary definition
            if isinstance(script, dict):
                stype = script.get('type', '').lower()
                
                # Inline code
                if stype == 'inline' or ('code' in script and not stype):
                    code = script.get('code') or script.get('value')
                    if code:
                        combined_js.append(f"// Inline dict script\n{code.strip()}")
                    continue
                
                # File/Src
                path = script.get('path') or script.get('src') or script.get('value')
                if path:
                    # Remote URL?
                    if path.startswith('http://') or path.startswith('https://') or path.startswith('//'):
                        combined_js.append(f"// Remote script: {path}\n(function(){{ var s=document.createElement('script'); s.src='{path}'; s.className='dars-route-script'; document.head.appendChild(s); }})();")
                    else:
                        # Local file - read and inject
                        try:
                            src_path = os.path.join(project_root, path) if not os.path.isabs(path) else path
                            if os.path.isfile(src_path):
                                with open(src_path, 'r', encoding='utf-8') as f:
                                    content = f.read()
                                    combined_js.append(f"// File: {os.path.basename(path)}\n{content}")
                            else:
                                combined_js.append(f"// Warning: Script file not found: {path}")
                        except Exception as e:
                            combined_js.append(f"// Error reading script {path}: {str(e)}")
                    continue

            # 3. String (treated as inline code usually, but could be path in some contexts?)
            if isinstance(script, str):
                if script.endswith('.js') and '\n' not in script:
                     # Treat as file path
                    path = script
                    if path.startswith('http') or path.startswith('//'):
                         combined_js.append(f"(function(){{ var s=document.createElement('script'); s.src='{path}'; s.className='dars-route-script'; document.head.appendChild(s); }})();")
                    else:
                        try:
                            src_path = os.path.join(project_root, path) if not os.path.isabs(path) else path
                            if os.path.isfile(src_path):
                                with open(src_path, 'r', encoding='utf-8') as f:
                                     combined_js.append(f"// File: {os.path.basename(path)}\n{f.read()}")
                        except: pass
                else:
                    # Treat as code
                    combined_js.append(script)
                    
        return "\n\n".join(combined_js)

    def render_route(self, route_name: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Render a Dars route server-side.
        
        Args:
            route_name: Name of the route to render
            params: Optional route parameters (e.g., from URL path)
        
        Returns:
            Dictionary containing rendered HTML, scripts, events, VDOM, and head metadata
        
        Raises:
            ValueError: If route not found or not an SSR route
        """
        # Get route
        route = self.app._spa_routes.get(route_name)
        if not route:
            raise ValueError(f"Route '{route_name}' not found")
        
        # Verify it's an SSR route
        metadata = getattr(route.root, '__dars_route_metadata__', None)
        if not metadata or metadata.route_type != RouteType.SSR:
            raise ValueError(f"Route '{route_name}' is not an SSR route")
        
        # Create a shallow copy of the app for this render
        route_app = copy.copy(self.app)
        if route.title:
            route_app.title = route.title
            
        # Create a fresh exporter instance for this render to ensure clean state (IDs, style registry)
        exporter = HTMLCSSJSExporter()
        exporter._current_page_id = route_name
        # Ensure fresh style registry for this render
        try:
            exporter._style_registry = {}
        except Exception:
            pass

        # IMPORTANT: Work on a deep copy of route.root so we never mutate the original tree
        from dars.components.basic.container import Container
        try:
            import copy as _cpy
            working_root = _cpy.deepcopy(route.root)
        except Exception:
            working_root = route.root

        # Normalize root (wrap list in Container) on the working copy
        if isinstance(working_root, list):
            working_root = Container(children=working_root)
        route_app.root = working_root

        # Ensure deterministic IDs for this SSR render before any processing
        exporter.ensure_ids_assigned(working_root)

        # Phase 1 styles: collect static styles and replace inline with classes for SSR route
        try:
            exporter._collect_static_styles_from_tree(working_root)
        except Exception:
            pass

        # Snapshot registry CSS immediately after collection (before further steps mutate state)
        try:
            _registry_css_snapshot = exporter._generate_style_registry_css()
        except Exception:
            _registry_css_snapshot = ""

        # Render component to HTML (body content only)
        body_html = exporter.render_component(working_root)
        
        # Capture bindings generated during this specific SSR render
        # These will use the deterministic IDs generated for the SSR output
        reactive_bindings_js = exporter._generate_reactive_bindings_js()
        vref_bindings_js = exporter._generate_vref_bindings_js()
        
        # Collect scripts from Markdown components (populated during render_component)
        route_markdown_scripts = []
        md_scripts = getattr(exporter, '_markdown_scripts', {}).get(route_name, [])
        for script_obj in md_scripts:
            if not isinstance(script_obj, dict):
                route_markdown_scripts.append(str(script_obj))
                continue
                
            stype = script_obj.get('type')
            if stype == 'file' or 'path' in script_obj:
                path = script_obj.get('path') or script_obj.get('src')
                is_mod = ' type="module"' if script_obj.get('module') else ''
                route_markdown_scripts.append(f'<script src="{path}"{is_mod}></script>')
            elif 'code' in script_obj:
                code = script_obj['code']
                is_mod = ' type="module"' if script_obj.get('module') else ''
                route_markdown_scripts.append(f'<script{is_mod}>{code}</script>')
        
        markdown_scripts_html = "".join(route_markdown_scripts)
        
        print(f"[Dars:SSR] Rendering route: {route_name}")
        print(f"[Dars:SSR] Reactive bindings length: {len(reactive_bindings_js)}")
        print(f"[Dars:SSR] VRef bindings length: {len(vref_bindings_js)}")

        # Fallback: if snapshot was empty, attempt a second collection post-render
        if not _registry_css_snapshot:
            try:
                exporter._collect_static_styles_from_tree(working_root)
                _registry_css_snapshot = exporter._generate_style_registry_css()
            except Exception:
                _registry_css_snapshot = ""
        
        # Build VDOM and events
        try:
            vdom_builder = VDomBuilder(id_provider=exporter.get_component_id)
            route_vdom = vdom_builder.build(working_root)
            route_events_map = vdom_builder.events_map
        except Exception as e:
            print(f"[SSR] Warning: VDOM build failed: {e}")
            import traceback
            traceback.print_exc()
            route_vdom = {}
            route_events_map = {}

        # Generate VDOM JavaScript and initial state snapshot for hydration
        vdom_json = json.dumps(route_vdom, ensure_ascii=False, separators=(",", ":"), cls=DarsJSONEncoder)

        # Collect initial state configuration (V1 + V2) so the client can
        # register states without requiring a separate static export.
        try:
            from dars.core.state import STATE_BOOTSTRAP  # type: ignore
            initial_states = list(STATE_BOOTSTRAP) if STATE_BOOTSTRAP else []
        except Exception:
            initial_states = []

        # State V2 snapshot (if available)
        try:
            from dars.core.state_v2 import STATE_V2_REGISTRY  # type: ignore
            initial_states_v2 = [s.to_dict() for s in STATE_V2_REGISTRY] if STATE_V2_REGISTRY else []
        except Exception:
            initial_states_v2 = []

        states_json = json.dumps(initial_states, ensure_ascii=False, separators=(",", ":"), cls=DarsJSONEncoder)
        states_v2_json = json.dumps(initial_states_v2, ensure_ascii=False, separators=(",", ":"), cls=DarsJSONEncoder)

        # Build a minimal SPA config so the client router can resolve routes on
        # first load without requiring the static export pipeline. We keep this
        # intentionally light-weight and focused on routing.
        spa_config = {
            "routes": [],
            "index": None,
            "notFound": None,
            "notFoundPath": None,
        }

        # Optional backend URL for SSR fetches (mirrors App.ssr_url usage)
        if getattr(self.app, "ssr_url", None):
            spa_config["backendUrl"] = self.app.ssr_url

        # Loading/Error components for SSR lazy-load (static HTML placeholders)
        try:
            def _render_static_placeholder(comp):
                if not comp:
                    return ""
                # Allow Page wrapper or raw Component
                if hasattr(comp, 'root'):
                    root0 = comp.root
                else:
                    root0 = comp
                # If list, wrap without using children=
                if isinstance(root0, list):
                    from dars.components.basic.container import Container
                    root0 = Container(*root0)
                try:
                    return exporter.render_component(root0)
                except Exception:
                    return ""

            spa_config["loadingHtml"] = _render_static_placeholder(getattr(self.app, "_spa_loading_page", None))
            spa_config["errorHtml"] = _render_static_placeholder(getattr(self.app, "_spa_error_page", None))
        except Exception:
            spa_config["loadingHtml"] = ""
            spa_config["errorHtml"] = ""

        # Build per-route config based on the in-memory SPA routes
        for name, spa_route in self.app._spa_routes.items():  # type: ignore[attr-defined]
            r_meta = getattr(spa_route.root, "__dars_route_metadata__", None)
            r_type = getattr(r_meta, "route_type", RouteType.PUBLIC)

            route_type_str = "ssr" if r_type == RouteType.SSR else "public"
            rcfg = {
                "name": name,
                "path": getattr(spa_route, "route", None),
                "title": getattr(spa_route, "title", None) or self.app.title,
                "type": route_type_str,
                "parent": getattr(spa_route, "parent", None),
                "outletId": getattr(spa_route, "outlet_id", "main"),
            }

            if route_type_str == "ssr":
                # Use the same default pattern as the exporter
                loader_endpoint = getattr(r_meta, "loader_endpoint", None) or f"/api/ssr/{name}"
                rcfg["ssr_endpoint"] = loader_endpoint

            spa_config["routes"].append(rcfg)
            
            # Index route detection
            if getattr(spa_route, "index", False):
                spa_config["index"] = name

        # Add markdown scripts to the current route's config in the SPA config
        # so they can be loaded by the client router
        for r in spa_config["routes"]:
            if r["name"] == route_name:
                r["scripts"] = md_scripts

        # Derive a simple 404 route if the SPA app has one configured
        not_found_page = getattr(self.app, "_spa_404_page", None)
        if not_found_page is not None:
            spa_config["notFoundPath"] = "/404"
            spa_config["routes"].append({
                "name": "__404__",
                "path": "/404",
                "title": "404 Not Found",
                "type": "public",
                "parent": None,
            })

        # Only inject VDOM snapshot AND the bundled script for this page.
        # This matches the behavior of static HTML export where app_{slug}.js is included.
        script_fn = f"app_{route_name}.js"

        # ---------------------------------------------------------------------
        # CSS Registry Handling
        # ---------------------------------------------------------------------
        # Generate CSS for style registry for this SSR render (use early snapshot)
        registry_css = _registry_css_snapshot
        
        # Robust fallback: if still empty, extract from rendered HTML's inline styles
        # This handles styles added dynamically during render_component
        if not registry_css and body_html:
            try:
                from bs4 import BeautifulSoup
                # Parse body fragment
                soup = BeautifulSoup(body_html, 'html.parser')
                rules = {}

                def parse_inline_style(s: str):
                    out = {}
                    for decl in s.split(';'):
                        decl = decl.strip()
                        if not decl: continue
                        if ':' not in decl: continue
                        k, v = decl.split(':', 1)
                        if k.strip() and v.strip():
                            out[k.strip()] = v.strip()
                    return out

                # Find all elements with inline style
                for el in soup.select('[style]'):
                    style_text = el.get('style') or ''
                    style_dict = parse_inline_style(style_text)
                    if not style_dict: continue
                    
                    # Compute class via exporter helper
                    try:
                        # Access protected method if available, else skip
                        if hasattr(exporter, '_style_fingerprint'):
                             class_name = exporter._style_fingerprint(style_dict) 
                        else:
                             continue
                    except Exception:
                        continue
                        
                    rules[class_name] = style_dict
                    
                    # Prepend class and drop inline style
                    existing = (el.get('class') or [])
                    if class_name not in existing:
                        el['class'] = [class_name] + list(existing)
                    try:
                        del el['style']
                    except Exception:
                        pass

                # If we collected any rules, rebuild body_html and CSS
                if rules:
                    # Update body_html with classes
                    body_html = str(soup)
                    # Build CSS from rules
                    blocks = []
                    for cname, sdict in rules.items():
                        lines = []
                        for k, v in sdict.items():
                            lines.append(f"{k}: {v};")
                        css_body = '\n    '.join(lines)
                        blocks.append(f".{cname} {{\n    {css_body}\n}}")
                    registry_css = '\n\n'.join(blocks)
            except Exception as e:
                # If extraction fails, keep original registry_css
                print(f"[SSR] CSS extraction warning: {e}")
                pass

        # ---------------------------------------------------------------------
        # Head Metadata & Meta Tags
        # ---------------------------------------------------------------------
        # Extract head metadata if Head component was used
        head_metadata = getattr(exporter, '_page_head_metadata', {})
        
        # Generate meta tags HTML for SSR
        if head_metadata:
            try:
                # Use the exporter's method to generate meta tags
                meta_tags_html = exporter._generate_page_meta_tags(head_metadata, route_app)
                page_title = head_metadata.get('title', route_app.title)
            except Exception:
                meta_tags_html = ""
                page_title = route_app.title
        else:
            # No Head component - use minimal meta tags
            meta_tags_html = f'<meta name="description" content="{route_app.description}">' if hasattr(route_app, 'description') and route_app.description else ''
            page_title = route_app.title

        try:
            # Build DSP Payload (Hydration Data)
            dsp_payload = {
                "spaConfig": spa_config,
                "vdom": route_vdom,
                "states": initial_states,
                "statesV2": initial_states_v2,
                "metaTags": meta_tags_html,
                "styles": registry_css,
                # Removed events and bindings. Handled natively by app_{route}.js
                "events": {},
                "reactiveBindings": "",
                "vrefBindings": ""
            }
            
            dsp_json = json.dumps(dsp_payload, ensure_ascii=False, cls=DarsJSONEncoder)
        except Exception as e:
            print(f"[Dars:SSR] Error building DSP payload: {e}")
            import traceback
            traceback.print_exc()
            dsp_json = "{}"

        # Always include the style tag (even if empty) so presence can be verified and updated later
        registry_style_tag = f"\n    <style id=\"dars-style-registry\">\n{registry_css}\n    </style>\n    "

        # Collect additional HTML assets (like Prism CSS links)
        md_html_assets = getattr(exporter, '_markdown_html_assets', {}).get(route_name, [])
        markdown_head_assets = "".join(md_html_assets)

        full_html = f"""<!DOCTYPE html>
<html lang="{route_app.language if hasattr(route_app, 'language') else 'en'}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    {meta_tags_html}
    <title>{page_title}</title>
    <link rel="stylesheet" href="/runtime_css.css">{registry_style_tag}<link rel="stylesheet" href="/styles.css">{markdown_head_assets}
</head>
<body>
    <div id="__dars_spa_root__">
        <div data-dars-route-wrapper="{route_name}" style="height: 100%; width: 100%;">
            {body_html}
        </div>
    </div>
    {markdown_scripts_html}
    <script type="module" src="/lib/dars.min.js" defer></script>
    <script type="module" src="/app.js"></script>
    <script type="module" src="/{script_fn}"></script>
</body>
</html>"""
        
        # Also attach styles to spa_config for the current route so client can inject when using JSON API
        try:
            for i, rc in enumerate(spa_config.get('routes', [])):
                if rc and rc.get('name') == route_name:
                    rc['styles'] = registry_css
                elif rc and 'styles' not in rc:
                    rc['styles'] = ''
        except Exception:
            pass
        
        from bs4 import BeautifulSoup
        # Route rendered successfully
        html_sp = BeautifulSoup(full_html, "html.parser")
        html_content = html_sp.prettify()
        return {
            "name": route_name,
            "html": body_html,  # Body HTML for SPA hydration
            "fullHtml": html_content,  # Complete HTML document with <head>
            "styles": registry_css,
            "scripts": [
                {"type": "user", "src": f"/{script_fn}", "module": True}
            ],
            "events": {}, # Removed, using native JS
            "vdom": route_vdom,
            "states": initial_states,
            "statesV2": initial_states_v2,
            "spaConfig": spa_config,
            "headMetadata": head_metadata,
            "reactiveBindings": "",
            "vrefBindings": ""
        }


class SSRApp:
    """
    Wrapper around FastAPI to provide a dedicated Dars SSR Application.
    Allows customization of the underlying FastAPI instance before starting.
    """
    def __init__(self, dars_app: App, prefix: str = "/api/ssr", title: str = None):
        self.dars_app = dars_app
        self.prefix = prefix
        self.fastapi_app = FastAPI(title=title or f"{dars_app.title} - SSR Backend")
        self.renderer = SSRRenderer(dars_app)
        self._setup_core_routes()

    def _setup_core_routes(self):
        from fastapi.responses import HTMLResponse, JSONResponse

        # Health check
        @self.fastapi_app.get("/_dars/health")
        async def health_check():
            return {"status": "ok", "app": self.dars_app.title}

        # Register SSR routes
        ssr_routes = []
        for name, route in self.dars_app._spa_routes.items():
            metadata = getattr(route.root, '__dars_route_metadata__', None)
            if metadata and metadata.route_type == RouteType.SSR:
                ssr_routes.append((name, route))

        for route_name, route in ssr_routes:
            self._register_api_endpoint(route_name)
            if hasattr(route, 'route') and route.route:
                self._register_html_endpoint(route_name, route.route)

        print(f"[SSR] Initialized {len(ssr_routes)} server-side routes.")

    def _register_api_endpoint(self, route_name: str):
        from fastapi.responses import JSONResponse

        api_path = f"{self.prefix}/{route_name}"

        @self.fastapi_app.get(api_path)
        async def api_endpoint(request: Request):
            try:
                params = dict(request.query_params)
                result = self.renderer.render_route(route_name, params)
                return JSONResponse(result)
            except ValueError as e:
                raise HTTPException(status_code=404, detail=str(e))
            except Exception as e:
                import traceback
                traceback.print_exc()
                raise HTTPException(status_code=500, detail=f"SSR render error: {str(e)}")

    def _register_html_endpoint(self, route_name: str, route_path: str):
        from fastapi.responses import HTMLResponse

        @self.fastapi_app.get(route_path)
        async def html_endpoint(request: Request):
            try:
                params = dict(request.query_params)
                result = self.renderer.render_route(route_name, params)
                return HTMLResponse(content=result['fullHtml'], status_code=200)
            except ValueError as e:
                raise HTTPException(status_code=404, detail=str(e))
            except Exception as e:
                import traceback
                traceback.print_exc()
                raise HTTPException(status_code=500, detail="Internal Server Error")

    # ------------------------------------------------------------------
    # Middleware helpers
    # ------------------------------------------------------------------

    def use_security_headers(self, csp: str = None, hsts: bool = False):
        """Add :class:`~dars.backend.middleware.SecurityHeadersMiddleware`."""
        from dars.backend.middleware import SecurityHeadersMiddleware
        self.fastapi_app.add_middleware(SecurityHeadersMiddleware, csp=csp, hsts=hsts)
        return self

    def use_cors(self, origins=None, methods=None, headers=None, credentials: bool = True):
        """Add CORS middleware with Dars-friendly defaults."""
        from fastapi.middleware.cors import CORSMiddleware as _CORS
        self.fastapi_app.add_middleware(
            _CORS,
            allow_origins=origins or ["*"],
            allow_methods=methods or ["*"],
            allow_headers=headers or ["*"],
            allow_credentials=credentials,
        )
        return self

    def use_auth(self, secret: str, exclude_paths: list = None):
        """Add JWT :class:`~dars.backend.middleware.AuthMiddleware`."""
        from dars.backend.middleware import AuthMiddleware
        self.fastapi_app.add_middleware(AuthMiddleware, secret=secret, exclude_paths=exclude_paths or [])
        return self

    # ------------------------------------------------------------------
    # Upload pipeline helper
    # ------------------------------------------------------------------

    def use_upload(self, upload_dir: str = "uploads", allowed_types: list = None,
                   max_size_bytes: int = None, path: str = "/api/upload"):
        """Register a file upload endpoint via :class:`~dars.backend.upload.UploadPipeline`."""
        from dars.backend.upload import UploadPipeline
        pipeline = UploadPipeline(
            upload_dir=upload_dir,
            allowed_types=allowed_types,
            max_size_bytes=max_size_bytes,
        )
        pipeline.create_endpoint(self.fastapi_app, path=path)
        return self

    def use_spa_fallback(self, frontend_dir: str = None):
        """
        Mount the built frontend (dist/) as static files and add an SPA fallback
        middleware so that SPA routes like /about are served index.html instead
        of returning 404.

        This MUST be called after all API routes are registered and is the only
        approach that works when dist/404.html exists (StaticFiles html=True silently
        serves 404.html without raising, bypassing exception_handler approaches).

        Args:
            frontend_dir: Absolute path to the dist/ directory. When omitted the
                          path is resolved from dars.config.json or defaults to
                          <project_root>/dist.
        """
        import os
        from fastapi.staticfiles import StaticFiles
        from fastapi.responses import FileResponse
        from starlette.middleware.base import BaseHTTPMiddleware

        if frontend_dir is None:
            # Try to resolve from apiConfig
            try:
                import importlib, sys
                if '' not in sys.path:
                    sys.path.insert(0, '')
                api_cfg = importlib.import_module('backend.apiConfig')
                frontend_dir = api_cfg.DarsEnv.get_frontend_dist_dir()
            except Exception:
                frontend_dir = os.path.join(os.getcwd(), 'dist')

        frontend_dir = os.path.abspath(frontend_dir)
        index_html = os.path.join(frontend_dir, 'index.html')

        if not os.path.isdir(frontend_dir):
            import warnings
            warnings.warn(
                f"[Dars] use_spa_fallback: frontend dir not found at '{frontend_dir}'. "
                "Run 'dars build' first."
            )
            return self

        class SPAFallbackMiddleware(BaseHTTPMiddleware):
            """Return index.html for any 404 with no file extension (SPA routes)."""
            async def dispatch(self, request, call_next):
                response = await call_next(request)
                if response.status_code == 404:
                    path = request.url.path
                    if not os.path.splitext(path)[1] and os.path.isfile(index_html):
                        return FileResponse(index_html, media_type='text/html')
                return response

        self.fastapi_app.add_middleware(SPAFallbackMiddleware)

        lib_dir = os.path.join(frontend_dir, 'lib')
        if os.path.isdir(lib_dir):
            self.fastapi_app.mount('/lib', StaticFiles(directory=lib_dir), name='lib')

        self.fastapi_app.mount('/', StaticFiles(directory=frontend_dir, html=True), name='frontend')
        return self

    # ------------------------------------------------------------------
    # Store helper
    # ------------------------------------------------------------------

    def use_store(self, path: str = "dars_store.json", default: dict = None):
        """Create and return a :class:`~dars.backend.store.JsonStore` instance."""
        from dars.backend.store import JsonStore
        return JsonStore(path=path, default=default)

    # ------------------------------------------------------------------
    # Standard FastAPI delegation
    # ------------------------------------------------------------------

    def add_middleware(self, middleware_class, **options):
        self.fastapi_app.add_middleware(middleware_class, **options)

    def include_router(self, router, **kwargs):
        self.fastapi_app.include_router(router, **kwargs)

    def mount(self, path: str, app, name: str = None):
        self.fastapi_app.mount(path, app, name)

    def get(self, path: str, **kwargs):
        return self.fastapi_app.get(path, **kwargs)

    def post(self, path: str, **kwargs):
        return self.fastapi_app.post(path, **kwargs)

    def put(self, path: str, **kwargs):
        return self.fastapi_app.put(path, **kwargs)

    def delete(self, path: str, **kwargs):
        return self.fastapi_app.delete(path, **kwargs)

    def run(self, host="0.0.0.0", port=8000, reload=False):
        import uvicorn
        uvicorn.run(self.fastapi_app, host=host, port=port, reload=reload)


def create_ssr_app(dars_app: App, prefix: str = "/api/ssr", streaming: bool = False) -> Any:
    """
    Legacy factory function for backward compatibility.
    Returns the underlying FastAPI app instance from the new SSRApp class.
    """
    ssr_instance = SSRApp(dars_app, prefix=prefix)
    return ssr_instance.fastapi_app




