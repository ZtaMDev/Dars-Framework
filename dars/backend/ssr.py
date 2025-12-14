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

            # Index route
            if getattr(spa_route, "index", False):
                spa_config["index"] = name

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

        spa_config_json = json.dumps(spa_config, ensure_ascii=False, separators=(",", ":"), cls=DarsJSONEncoder)

        # Expose SPA config, VDOM and state snapshots on the window object so
        # js_lib can hydrate without re-creating the DOM from scratch.
        vdom_js = (
            f"window.__DARS_SPA_CONFIG__ = {spa_config_json};\n"
            f"window.__ROUTE_VDOM__ = {vdom_json};\n"
            f"window.__DARS_STATE__ = {states_json};\n"
            f"window.__DARS_STATE_V2__ = {states_v2_json};"
        )

        # Only inject VDOM snapshot AND the bundled script for this page.
        # This matches the behavior of static HTML export where app_{slug}.js is included.
        script_fn = "app.js" if route_name == "index" else f"app_{route_name}.js"
        
        # Extract head metadata if Head component was used
        head_metadata = getattr(exporter, '_page_head_metadata', {})
        
        # Generate meta tags HTML for SSR
        if head_metadata:
            # Use the exporter's method to generate meta tags
            meta_tags_html = exporter._generate_page_meta_tags(head_metadata, route_app)
            page_title = head_metadata.get('title', route_app.title)
        else:

            # No Head component - use minimal meta tags
            meta_tags_html = f'<meta name="description" content="{route_app.description}">' if hasattr(route_app, 'description') and route_app.description else ''
            page_title = route_app.title
        
        # Construct full HTML document with meta tags.
        #
        # IMPORTANT: wrap the rendered body inside the __dars_spa_root__
        # container so that the SPA router in dars.min.js can detect and
        # hydrate the already-rendered content instead of re-rendering it
        # from scratch on first load.
        # Generate CSS for style registry for this SSR render (use early snapshot)
        registry_css = _registry_css_snapshot
        # Robust fallback: if still empty, extract from rendered HTML's inline styles
        if not registry_css and body_html:
            try:
                from bs4 import BeautifulSoup
                soup = BeautifulSoup(body_html, 'html.parser')
                rules = {}

                def parse_inline_style(s: str):
                    out = {}
                    for decl in s.split(';'):
                        decl = decl.strip()
                        if not decl:
                            continue
                        if ':' not in decl:
                            continue
                        k, v = decl.split(':', 1)
                        k = k.strip()
                        v = v.strip()
                        if k and v:
                            out[k] = v
                    return out

                # Find all elements with inline style
                for el in soup.select('[style]'):
                    style_text = el.get('style') or ''
                    style_dict = parse_inline_style(style_text)
                    if not style_dict:
                        continue
                    # Compute class via exporter helper
                    try:
                        class_name = exporter._style_fingerprint(style_dict)  # type: ignore[attr-defined]
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
                        # Serialize like exporter.render_styles (simple serializer)
                        lines = []
                        for k, v in sdict.items():
                            lines.append(f"{k}: {v};")
                        css_body = '\n    '.join(lines)
                        blocks.append(f".{cname} {{\n    {css_body}\n}}")
                    registry_css = '\n\n'.join(blocks)
            except Exception:
                registry_css = registry_css

        # Always include the style tag (even if empty) so presence can be verified and updated later
        registry_style_tag = f"\n    <style id=\"dars-style-registry\">\n{registry_css}\n    </style>\n    "
        
        full_html = f"""<!DOCTYPE html>
<html lang="{route_app.language if hasattr(route_app, 'language') else 'en'}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    {meta_tags_html}
    <title>{page_title}</title>
    <link rel="stylesheet" href="/runtime_css.css">{registry_style_tag}<link rel="stylesheet" href="/styles.css">
</head>
<body>
    <div id="__dars_spa_root__">
        {body_html}
    </div>
    <script type="module" src="/lib/dars.min.js" defer></script>
    <script>{vdom_js}</script>
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

        return {
            "name": route_name,
            "html": body_html,  # Body HTML for SPA hydration
            "fullHtml": full_html,  # Complete HTML document with <head>
            "styles": registry_css,
            "scripts": [
                {"type": "core", "code": vdom_js},
                {"type": "user", "src": f"/{script_fn}", "module": True}
            ],
            "events": route_events_map,
            "vdom": route_vdom,
            # Provide initial state snapshot for dynamic loading/hydration.
            "states": initial_states,
            "statesV2": initial_states_v2,
            "spaConfig": spa_config,
            "headMetadata": head_metadata  # Include for client hydration
        }


def _register_server_components_from_app(dars_app: App) -> int:
    """
    Scan the entire Dars app component tree and register all server components.
    
    This ensures SERVER_COMPONENT_REGISTRY is populated when the backend starts,
    allowing server component endpoints to find and render the components.
    
    Args:
        dars_app: The Dars App instance to scan
        
    Returns:
        Number of server components registered
    """
    from dars.core.server_components import register_server_component, clear_server_component_registry
    from dars.core.component import Component
    
    # Clear existing registry to avoid duplicates on hot reload
    clear_server_component_registry()
    
    count = 0
    visited = set()
    
    def scan_component(comp):
        nonlocal count
        if comp is None or not isinstance(comp, Component):
            return
        
        # Avoid cycles
        comp_id_check = id(comp)
        if comp_id_check in visited:
            return
        visited.add(comp_id_check)
        
        # Register if use_server=True
        if getattr(comp, 'use_server', False):
            # Ensure component has an ID
            if not comp.id:
                import uuid
                comp.id = f"sc_{uuid.uuid4().hex[:8]}"
            register_server_component(comp)
            count += 1
            print(f"[SSR] Registered server component: {comp.id} ({type(comp).__name__})")
        
        # Scan children
        for child in getattr(comp, 'children', []) or []:
            scan_component(child)
        
        # Scan loading/error components too
        if hasattr(comp, '_loading_component') and comp._loading_component:
            scan_component(comp._loading_component)
        if hasattr(comp, '_error_component') and comp._error_component:
            scan_component(comp._error_component)
    
    # Scan multipage pages
    if hasattr(dars_app, 'pages'):
        for page in dars_app.pages.values():
            if hasattr(page, 'root'):
                scan_component(page.root)
    
    # Scan SPA routes
    if hasattr(dars_app, '_spa_routes'):
        for route in dars_app._spa_routes.values():
            if hasattr(route, 'root'):
                scan_component(route.root)
    
    # Scan app root
    if dars_app.root:
        scan_component(dars_app.root)
    
    print(f"[SSR] Total server components registered: {count}")
    return count


def create_ssr_app(dars_app: App, prefix: str = "/api/ssr", streaming: bool = False) -> FastAPI:
    """
    Create a FastAPI app with automatic SSR endpoints for all SSR routes.
    
    This function scans the Dars app for routes with RouteType.SSR and
    automatically creates FastAPI endpoints to render them server-side.
    
    Args:
        dars_app: Dars App instance
        prefix: URL prefix for SSR endpoints (default: "/api/ssr")
    
    Returns:
        FastAPI app with SSR endpoints
    
    Example:
        ```python
        from dars.all import *
        from dars.backend.ssr import create_ssr_app
        
        # Define Dars app with SSR routes
        app = App("My App")
        
        @route("/dashboard", route_type=RouteType.SSR)
        def dashboard():
            return Page(Text("Dashboard"))
        
        app.add_page("dashboard", dashboard())
        
        # Create FastAPI app
        fastapi_app = create_ssr_app(app)
        
        # Run with: uvicorn server:fastapi_app --reload
        ```
    """
    fastapi_app = FastAPI(title=f"{dars_app.title} - SSR Backend")
    
    renderer = SSRRenderer(dars_app)
    
    # IMPORTANT: Scan and register all server components from the app tree
    # This populates SERVER_COMPONENT_REGISTRY so component endpoints work
    _register_server_components_from_app(dars_app)
    
    # Find all SSR routes
    ssr_routes = []
    for name, route in dars_app._spa_routes.items():
        metadata = getattr(route.root, '__dars_route_metadata__', None)
        if metadata and metadata.route_type == RouteType.SSR:
            ssr_routes.append((name, route))
    
    from fastapi.responses import HTMLResponse, JSONResponse, StreamingResponse

    # Create endpoints for each SSR route
    for route_name, route in ssr_routes:
        # 1. API Endpoint (JSON) - used by SPA hydration
        def create_api_endpoint(name: str):
            async def endpoint(request: Request):
                try:
                    params = dict(request.query_params)
                    result = renderer.render_route(name, params)
                    return JSONResponse(result)
                except ValueError as e:
                    raise HTTPException(status_code=404, detail=str(e))
                except Exception as e:
                    raise HTTPException(status_code=500, detail=f"SSR render error: {str(e)}")
            return endpoint
        
        # Register API endpoint
        api_path = f"{prefix}/{route_name}"
        fastapi_app.get(api_path)(create_api_endpoint(route_name))
        print(f"[SSR] Registered API endpoint: {api_path}")

        # 2. HTML Endpoint - used by browser/crawlers (SEO)
        # Only if the route has a defined path
        if hasattr(route, 'route') and route.route:
            def create_html_endpoint(name: str):
                async def html_endpoint(request: Request):
                    try:
                        params = dict(request.query_params)
                        result = renderer.render_route(name, params)
                        full_html = result['fullHtml']

                        if not streaming:
                            # Classic non-streaming response
                            return HTMLResponse(content=full_html, status_code=200)

                        # Streaming mode: try to send <head> first, then body.
                        # We do a simple split on the <body> tag; if it fails,
                        # we fall back to a single-chunk streaming response.
                        lower_html = full_html.lower()
                        body_idx = lower_html.find("<body")
                        if body_idx == -1:
                            async def iter_single():
                                yield full_html.encode("utf-8")
                            return StreamingResponse(iter_single(), media_type="text/html")

                        # Find the end of the opening <body> tag
                        body_tag_end = lower_html.find('>', body_idx)
                        if body_tag_end == -1:
                            async def iter_single():
                                yield full_html.encode("utf-8")
                            return StreamingResponse(iter_single(), media_type="text/html")

                        head_part = full_html[:body_tag_end + 1]
                        body_part = full_html[body_tag_end + 1:]

                        async def iter_html():
                            # Send <html> + <head> + opening <body> first
                            yield head_part.encode("utf-8")
                            # Then the rest of the document
                            yield body_part.encode("utf-8")

                        return StreamingResponse(iter_html(), media_type="text/html")
                    except ValueError as e:
                         # Fallback to 404
                        raise HTTPException(status_code=404, detail=str(e))
                    except Exception as e:
                         # In dev, show error. In prod, maybe fallback to SPA?
                        raise HTTPException(status_code=500, detail=str(e))
                return html_endpoint

            # Register HTML endpoint
            # We use the actual route path (e.g., "/" or "/blog")
            fastapi_app.get(route.route)(create_html_endpoint(route_name))
            print(f"[SSR] Registered HTML endpoint: {route.route} -> {route_name}")
    
    # Add server component routes for lazy hydration
    create_server_component_routes(fastapi_app)
    
    # Health check endpoint (only if root is not taken)
    root_taken = any(r.route == "/" for _, r in ssr_routes if hasattr(r, 'route'))
    if not root_taken:
        @fastapi_app.get("/")
        async def root():
            return {
                "message": f"{dars_app.title} - SSR Backend",
                "ssr_routes": [name for name, _ in ssr_routes],
            }
    
    return fastapi_app


def create_server_component_routes(fastapi_app: FastAPI, prefix: str = "/api/server-component") -> None:
    """
    Add endpoints for rendering individual server components.
    
    This enables the lazy hydration pattern where components with use_server=True
    are initially rendered as placeholders, then fetched and hydrated on the client.
    
    Args:
        fastapi_app: The FastAPI application to add routes to
        prefix: URL prefix for server component endpoints (default: /api/server-component)
    """
    from dars.core.server_components import SERVER_COMPONENT_REGISTRY, get_server_component
    from dars.exporters.web.vdom import VDomBuilder
    from dars.exporters.web.html_css_js import HTMLCSSJSExporter, DarsJSONEncoder
    from starlette.requests import Request
    from starlette.responses import JSONResponse
    import json
    
    @fastapi_app.get(f"{prefix}/{{component_id}}")
    async def render_server_component(component_id: str, request: Request):
        """
        Render a registered server component and return HTML + VDOM for hydration.
        
        Response format:
        {
            "html": "<div>...</div>",
            "vdom": {...},
            "events": {...},
            "componentId": "..."
        }
        """
        component = get_server_component(component_id)
        if component is None:
            raise HTTPException(status_code=404, detail=f"Server component '{component_id}' not found")
        
        try:
            # Create exporter instance
            exporter = HTMLCSSJSExporter()
            
            # Temporarily disable use_server to render actual content
            original_use_server = getattr(component, 'use_server', False)
            component.use_server = False
            
            try:
                # Render component to HTML
                html = exporter.render_component(component)
                
                # Build VDOM
                vdom_builder = VDomBuilder(id_provider=exporter.get_component_id)
                vdom = vdom_builder.build(component)
                events_map = vdom_builder.events_map
            finally:
                # Restore use_server
                component.use_server = original_use_server
            
            return JSONResponse({
                "html": html,
                "vdom": vdom,
                "events": events_map,
                "componentId": component_id,
            })
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error rendering component: {str(e)}")
    
    @fastapi_app.get(f"{prefix}")
    async def list_server_components():
        """List all registered server components (for debugging)."""
        return {
            "components": list(SERVER_COMPONENT_REGISTRY.keys()),
            "count": len(SERVER_COMPONENT_REGISTRY),
        }
    
    print(f"[SSR] Registered server component endpoints at {prefix}/{{id}}")

