# Dars Framework - Backend Module
#
# This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0.
# If a copy of the MPL was not distributed with this file, You can obtain one at
# https://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2025 ZtaDev
"""
Route Loader for Lazy Loading Private Routes

This module provides backend endpoints for loading private/protected routes
that are not included in the initial client-side bundle for security.
"""

from typing import Optional, Dict, Any
from fastapi import HTTPException, Header


class RouteLoader:
    """
    Handles loading of private/protected routes from backend.
    
    This class provides endpoints for:
    - Loading route HTML, scripts, and events
    - Verifying authentication tokens
    - Checking permissions
    """
    
    def __init__(self, dars_app):
        """
        Initialize route loader with Dars app.
        
        Args:
            dars_app: Dars App instance with routes
        """
        self.dars_app = dars_app
        self.routes_cache = {}
    
    def get_route_data(self, route_name: str) -> Optional[Dict[str, Any]]:
        """
        Get route data by name.
        
        Args:
            route_name: Name of the route
        
        Returns:
            Dict with route data (html, scripts, events, vdom) or None
        """
        # Check cache first
        if route_name in self.routes_cache:
            return self.routes_cache[route_name]
        
        # Find route in app
        for page_name, page in self.dars_app.pages.items():
            if page_name == route_name:
                # Get route metadata
                metadata = getattr(page, '__dars_route_metadata__', None)
                if not metadata:
                    continue
                
                # Export route data
                from dars.exporters.web.html_css_js import HTMLCSSJSExporter
                exporter = HTMLCSSJSExporter()
                
                # Render component
                html = exporter._render_component(page)
                
                # Get scripts and events
                # TODO: Extract scripts and events from exporter
                
                route_data = {
                    'name': route_name,
                    'path': metadata.path,
                    'html': html,
                    'scripts': [],
                    'events': {},
                    'vdom': {}
                }
                
                # Cache for future requests
                self.routes_cache[route_name] = route_data
                return route_data
        
        return None
    
    async def load_route(
        self,
        route_name: str,
        authorization: Optional[str] = Header(None)
    ) -> Dict[str, Any]:
        """
        FastAPI endpoint to load a private/protected route.
        
        Args:
            route_name: Name of the route to load
            authorization: Authorization header with Bearer token
        
        Returns:
            Route data dict
        
        Raises:
            HTTPException: If unauthorized or route not found
        """
        # Extract token from Authorization header
        token = None
        if authorization and authorization.startswith('Bearer '):
            token = authorization[7:]  # Remove 'Bearer ' prefix
        
        # Get route data
        route_data = self.get_route_data(route_name)
        if not route_data:
            raise HTTPException(status_code=404, detail="Route not found")
        
        # Get route metadata
        for page_name, page in self.dars_app.pages.items():
            if page_name == route_name:
                metadata = getattr(page, '__dars_route_metadata__', None)
                if metadata:
                    # Check if authentication is required
                    if metadata.requires_auth:
                        if not token:
                            raise HTTPException(
                                status_code=401,
                                detail="Authentication required"
                            )
                        
                        # TODO: Verify token
                        # For now, just check if token exists
                        # In v1.7.2, we'll implement proper JWT verification
                    
                    break
        
        return route_data


def create_route_loader_endpoint(app, dars_app):
    """
    Create FastAPI endpoint for route loading.
    
    Usage:
        from fastapi import FastAPI
        from dars.backend.route_loader import create_route_loader_endpoint
        
        fastapi_app = FastAPI()
        create_route_loader_endpoint(fastapi_app, dars_app)
    
    Args:
        app: FastAPI app instance
        dars_app: Dars App instance
    """
    loader = RouteLoader(dars_app)
    
    @app.get("/api/routes/{route_name}")
    async def load_route(
        route_name: str,
        authorization: Optional[str] = Header(None)
    ):
        """Load a private/protected route."""
        return await loader.load_route(route_name, authorization)
    
    return loader
