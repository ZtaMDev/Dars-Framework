# Dars Framework - Core Source File
#
# This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0.
# If a copy of the MPL was not distributed with this file, You can obtain one at
# https://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2025 ZtaDev
"""
SPA Routing System for Dars Framework

This module provides:
- @route decorator for defining routes
- SPARoute class for route configuration with parameter support
- RouteNode class for nested route tree structure
"""

import re
from typing import List, Optional, Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from dars.core.component import Component

# Global registry for route metadata from decorators
_ROUTE_REGISTRY: Dict[int, str] = {}


def route(
    path: str,
    route_type: 'RouteType' = None,
    requires_auth: bool = False,
    middleware: Optional[List] = None,
    loader_endpoint: Optional[str] = None
):
    """
    Decorator to define a route for a page function with security options.
    
    Usage:
        # Public route (default)
        @route("/home")
        def homepage():
            return Page(...)
        
        # Private route (requires authentication)
        @route("/admin", route_type=RouteType.PRIVATE, requires_auth=True)
        def admin():
            return Page(...)
        
        # Protected route (custom middleware)
        @route("/dashboard", route_type=RouteType.PROTECTED, middleware=[AuthMiddleware()])
        def dashboard():
            return Page(...)
    
    Args:
        path: Route path (e.g., "/home", "/user/:id")
        route_type: Type of route (PUBLIC, PRIVATE, PROTECTED)
        requires_auth: Whether route requires authentication
        middleware: List of middleware to apply
        loader_endpoint: Custom backend loader endpoint
    
    Returns:
        Decorator function
    """
    # Import here to avoid circular imports
    from dars.core.route_types import RouteType, RouteMetadata
    
    # Default to PUBLIC if not specified
    if route_type is None:
        route_type = RouteType.PUBLIC
    
    # Create route metadata
    metadata = RouteMetadata(
        path=path,
        route_type=route_type,
        requires_auth=requires_auth,
        middleware=middleware,
        loader_endpoint=loader_endpoint
    )
    
    def decorator(func):
        # Store route metadata on the function
        func.__dars_route__ = path
        func.__dars_route_metadata__ = metadata
        _ROUTE_REGISTRY[id(func)] = path
        
        # Create wrapper that also adds route to returned Page
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            # If result is a Page, attach route info
            if result is not None:
                result.__dars_route__ = path
                result.__dars_route_metadata__ = metadata
                result.__source_func__ = func
            return result
        
        # Preserve function metadata
        wrapper.__dars_route__ = path
        wrapper.__dars_route_metadata__ = metadata
        wrapper.__name__ = func.__name__
        wrapper.__doc__ = func.__doc__
        
        return wrapper
    return decorator



def get_route(func_or_page) -> Optional[str]:
    """
    Extract route from function or page if defined via @route decorator.
    
    Args:
        func_or_page: Function or Page instance
    
    Returns:
        Route path string or None if not defined
    """
    # Check if it's a function with __dars_route__
    if hasattr(func_or_page, '__dars_route__'):
        return func_or_page.__dars_route__
    
    # Check if it's a page from a decorated function
    if hasattr(func_or_page, '__source_func__'):
        source = func_or_page.__source_func__
        if hasattr(source, '__dars_route__'):
            return source.__dars_route__
    
    return None


class SPARoute:
    """
    Represents a SPA route with client-side routing support.
    
    Features:
    - Route parameter extraction (/user/:id)
    - Pattern-based matching with regex
    - Nested route support via parent reference
    - Preloading configuration
    """
    
    def __init__(
        self, 
        name: str, 
        root: 'Component', 
        route: str,
        title: str = None, 
        meta: dict = None, 
        preload: List[str] = None,
        index: bool = False,
        parent: str = None
    ):
        """
        Initialize SPA route.
        
        Args:
            name: Internal route name (identifier)
            root: Root component for this route
            route: URL path (e.g., "/home", "/user/:id", "/post/:slug/edit")
            title: Page title
            meta: Metadata dict
            preload: List of route paths to preload
            index: Whether this is the index/main route
            parent: Parent route name for nested routes
        """
        self.name = name
        self.root = root
        self.route = route
        self.title = title
        self.meta = meta or {}
        self.preload = preload or []
        self.index = index
        self.parent = parent
        
        # Parse route parameters and build pattern
        self.params = self._extract_params(route)
        self.pattern = self._build_pattern(route)
    
    def _extract_params(self, route: str) -> List[str]:
        """
        Extract parameter names from route.
        
        Example:
            "/user/:id" -> ["id"]
            "/post/:slug/edit" -> ["slug"]
            "/user/:id/post/:postId" -> ["id", "postId"]
        
        Args:
            route: Route path with parameters
        
        Returns:
            List of parameter names
        """
        return re.findall(r':([a-zA-Z_][a-zA-Z0-9_]*)', route)
    
    def _build_pattern(self, route: str) -> str:
        """
        Build regex pattern for route matching.
        
        Converts route with parameters to regex:
            "/user/:id" -> "^/user/(?P<id>[^/]+)$"
            "/post/:slug/edit" -> "^/post/(?P<slug>[^/]+)/edit$"
        
        Args:
            route: Route path with parameters
        
        Returns:
            Regex pattern string
        """
        # Convert :param to named regex group
        pattern = re.sub(
            r':([a-zA-Z_][a-zA-Z0-9_]*)', 
            r'(?P<\1>[^/]+)', 
            route
        )
        return f"^{pattern}$"
    
    def matches(self, path: str) -> Optional[Dict[str, str]]:
        """
        Check if a path matches this route pattern.
        
        Args:
            path: URL path to match
        
        Returns:
            Dict of extracted parameters if match, None otherwise
            
        Example:
            route = SPARoute(..., route="/user/:id")
            route.matches("/user/123")  # Returns {"id": "123"}
            route.matches("/other")     # Returns None
        """
        match = re.match(self.pattern, path)
        if match:
            return match.groupdict()
        return None
    
    def __repr__(self):
        return f"SPARoute(name='{self.name}', route='{self.route}', params={self.params})"


class RouteNode:
    """
    Node in the nested route tree structure.
    
    Used to build a hierarchy of routes for nested routing:
        /docs (parent)
        ├── /docs/getting-started (child)
        └── /docs/api (child)
    """
    
    def __init__(self, route: SPARoute = None):
        """
        Initialize route node.
        
        Args:
            route: SPARoute instance (None for root node)
        """
        self.route = route
        self.children: List['RouteNode'] = []
    
    def add_child(self, child_node: 'RouteNode'):
        """
        Add a child route node.
        
        Args:
            child_node: Child RouteNode to add
        """
        self.children.append(child_node)
    
    def find_route(self, path: str) -> Optional[tuple]:
        """
        Find matching route in tree, returns (route, params) or None.
        
        Searches this node and all children recursively.
        
        Args:
            path: URL path to match
        
        Returns:
            Tuple of (SPARoute, params_dict) if found, None otherwise
        """
        # Check this node
        if self.route:
            params = self.route.matches(path)
            if params is not None:
                return (self.route, params)
        
        # Check children
        for child in self.children:
            result = child.find_route(path)
            if result:
                return result
        
        return None
    
    def __repr__(self):
        route_str = f"'{self.route.route}'" if self.route else "ROOT"
        return f"RouteNode({route_str}, children={len(self.children)})"
