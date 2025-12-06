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
                        # Cannot inject efficiently, maybe allow client to load?
                        # For now, we only handle local files as requested "backend collects JS"
                        # But we can't inject remote JS easily due to CORS/Security.
                        # We will append a loader for it in the combined JS?
                        # Better to append as a dynamic import or script injection in JS.
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
            # In Dars, raw strings in scripts list are usually paths if they look like paths, or code if not?
            # actually usually strings are paths in some old version, but newer dScript uses objects.
            # safe assumption: if it has newlines or lacks extension, it's code. 
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
            Dictionary containing rendered HTML, scripts, events, and VDOM
        
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
        
        # Create a copy of the app for this render
        route_app = copy.copy(self.app)
        route_app.root = route.root
        if route.title:
            route_app.title = route.title
            
        # Create a fresh exporter instance for this render to ensure clean state (IDs)
        exporter = HTMLCSSJSExporter()
        
        # Render component to HTML
        html = exporter.render_component(route.root)
        
        # Build VDOM and events
        try:
            vdom_builder = VDomBuilder(id_provider=exporter.get_component_id)
            route_vdom = vdom_builder.build(route.root)
            route_events_map = vdom_builder.events_map
        except Exception as e:
            print(f"[SSR] Warning: VDOM build failed: {e}")
            import traceback
            traceback.print_exc()
            route_vdom = {}
            route_events_map = {}
        
        # Generate VDOM JavaScript
        vdom_json = json.dumps(route_vdom, ensure_ascii=False, separators=(",", ":"), cls=DarsJSONEncoder)
        vdom_js = f"window.__ROUTE_VDOM__ = {vdom_json};"

        # Only inject VDOM snapshot AND the bundled script for this page.
        # This matches the behavior of static HTML export where app_{slug}.js is included.
        script_fn = "app.js" if route_name == "index" else f"app_{route_name}.js"
        
        return {
            "name": route_name,
            "html": html,
            "scripts": [
                {"type": "core", "code": vdom_js},
                {"type": "user", "src": f"/{script_fn}", "module": True}
            ],
            "events": route_events_map,
            "vdom": route_vdom,
            "states": []
        }


def create_ssr_app(dars_app: App, prefix: str = "/api/ssr") -> FastAPI:
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
    
    # Find all SSR routes
    ssr_routes = []
    for name, route in dars_app._spa_routes.items():
        metadata = getattr(route.root, '__dars_route_metadata__', None)
        if metadata and metadata.route_type == RouteType.SSR:
            ssr_routes.append((name, route))
    
    # Create endpoints for each SSR route
    for route_name, route in ssr_routes:
        # Create endpoint dynamically
        def create_endpoint(name: str):
            async def endpoint(request: Request):
                try:
                    # Extract route params from query string
                    params = dict(request.query_params)
                    
                    # Render route
                    result = renderer.render_route(name, params)
                    return result
                except ValueError as e:
                    raise HTTPException(status_code=404, detail=str(e))
                except Exception as e:
                    raise HTTPException(status_code=500, detail=f"SSR render error: {str(e)}")
            
            return endpoint
        
        # Register endpoint
        endpoint_path = f"{prefix}/{route_name}"
        fastapi_app.get(endpoint_path)(create_endpoint(route_name))
        print(f"[SSR] Registered endpoint: {endpoint_path}")
    
    # Health check endpoint
    @fastapi_app.get("/")
    async def root():
        return {
            "message": f"{dars_app.title} - SSR Backend",
            "ssr_routes": [name for name, _ in ssr_routes],
            "endpoints": [f"{prefix}/{name}" for name, _ in ssr_routes]
        }
    
    return fastapi_app
