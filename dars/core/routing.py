# Dars Framework - Core Source File
#
# This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0.
# If a copy of the MPL was not distributed with this file, You can obtain one at
# https://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2026 ZtaDev
"""
SPA Routing System for Dars Framework

This module provides:
- ``@route`` decorator for defining routes with security guards
- ``@guard`` decorator for attaching route guards to components
- :class:`SPARoute` class for route configuration with parameter support
- :class:`RouteNode` class for nested route tree structure
"""

from __future__ import annotations

import re
from typing import Any, Callable, Dict, List, Optional, Sequence, TYPE_CHECKING

from dars.core.route_types import RouteType, RouteMetadata, RouteGuard

if TYPE_CHECKING:
    from dars.core.component import Component

# Global registry for route metadata from decorators
_ROUTE_REGISTRY: Dict[int, str] = {}


def route(
    path: str,
    route_type: Optional[RouteType] = None,
    requires_auth: bool = False,
    roles: Optional[List[str]] = None,
    guard: Optional[RouteGuard] = None,
    redirect: Optional[str] = None,
    middleware: Optional[List] = None,
    loader_endpoint: Optional[str] = None,
):
    """
    Decorator to define a route for a page with security and rendering options.

    Usage::

        # Public route (default)
        @route("/home")
        def homepage():
            return Page(...)

        # SSR route
        @route("/dashboard", route_type=RouteType.SSR)
        def dashboard():
            return Page(...)

        # Private route (requires authentication)
        @route("/account", route_type=RouteType.PRIVATE)
        def account():
            return Page(...)

        # Protected route (requires auth + admin role)
        @route("/admin", route_type=RouteType.PROTECTED, roles=["admin"])
        def admin_panel():
            return Page(...)

        # With custom guard
        @route("/premium", guard=RouteGuard(requires_auth=True, roles=["premium"]))
        def premium():
            return Page(...)

    Args:
        path: Route path (e.g., ``"/home"``, ``"/user/:id"``).
        route_type: Type of route (PUBLIC, SSR, PRIVATE, PROTECTED).
        requires_auth: Shorthand to require authentication.
        roles: List of roles permitted (for PROTECTED routes).
        guard: :class:`RouteGuard` instance for fine-grained access control.
        redirect: Path to redirect unauthorized users (default ``"/login"``).
        middleware: List of middleware to apply.
        loader_endpoint: Custom loader endpoint.

    Returns:
        Decorator function.
    """
    from dars.core.route_types import RouteType, RouteMetadata, RouteGuard

    if route_type is None:
        if requires_auth or roles:
            route_type = RouteType.PROTECTED if roles else RouteType.PRIVATE
        else:
            route_type = RouteType.PUBLIC

    if guard is None:
        guard_kwargs = dict(
            requires_auth=requires_auth or route_type in (RouteType.PRIVATE, RouteType.PROTECTED),
            roles=roles or [],
        )
        if redirect is not None:
            guard_kwargs["redirect"] = redirect
        guard = RouteGuard(**guard_kwargs)

    metadata = RouteMetadata(
        path=path,
        route_type=route_type,
        requires_auth=requires_auth or route_type in (RouteType.PRIVATE, RouteType.PROTECTED),
        guard=guard,
        middleware=middleware or [],
        loader_endpoint=loader_endpoint,
        roles=roles or [],
    )

    def decorator(func):
        req_auth = getattr(func, "__requires_auth__", False) or requires_auth
        auth_id = getattr(func, "__auth_id__", None)

        if req_auth:
            metadata.requires_auth = True
        if auth_id:
            metadata.auth_id = auth_id

        func.__dars_route__ = path
        func.__dars_route_metadata__ = metadata
        _ROUTE_REGISTRY[id(func)] = path

        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            if result is not None:
                result.__dars_route__ = path
                if hasattr(result, "_auth_id") and result._auth_id:
                    metadata.requires_auth = True
                    metadata.auth_id = result._auth_id
                result.__dars_route_metadata__ = metadata
                result.__source_func__ = func
            return result

        wrapper.__dars_route__ = path
        wrapper.__dars_route_metadata__ = metadata
        wrapper.__name__ = func.__name__
        wrapper.__doc__ = func.__doc__

        return wrapper

    return decorator


def guard(
    requires_auth: bool = True,
    roles: Optional[List[str]] = None,
    redirect: str = "/login",
    custom_check: Optional[Callable[[Dict[str, Any]], bool]] = None,
):
    """
    Decorator to attach a route guard to a page function.

    This is an alternative to specifying ``guard=`` in ``@route``::

        @route("/admin")
        @guard(requires_auth=True, roles=["admin"])
        def admin_panel():
            return Page(...)

    Args:
        requires_auth: Whether authentication is required.
        roles: List of permitted roles.
        redirect: Redirect path for unauthorized users.
        custom_check: Optional callable for custom access logic.

    Returns:
        Decorator function.
    """
    def decorator(func):
        guard_obj = RouteGuard(
            requires_auth=requires_auth,
            roles=roles or [],
            redirect=redirect,
            custom_check=custom_check,
        )
        func.__dars_guard__ = guard_obj
        return func
    return decorator


def get_route(func_or_page) -> Optional[str]:
    """
    Extract route from function or page if defined via ``@route`` decorator.

    Args:
        func_or_page: Function or Page instance.

    Returns:
        Route path string or ``None`` if not defined.
    """
    if hasattr(func_or_page, "__dars_route__"):
        return func_or_page.__dars_route__

    if hasattr(func_or_page, "__source_func__"):
        source = func_or_page.__source_func__
        if hasattr(source, "__dars_route__"):
            return source.__dars_route__

    return None


def get_route_metadata(func_or_page) -> Optional[RouteMetadata]:
    """
    Extract route metadata from function or page.

    Args:
        func_or_page: Function or Page instance.

    Returns:
        :class:`RouteMetadata` or ``None``.
    """
    if hasattr(func_or_page, "__dars_route_metadata__"):
        return func_or_page.__dars_route_metadata__

    if hasattr(func_or_page, "__source_func__"):
        source = func_or_page.__source_func__
        if hasattr(source, "__dars_route_metadata__"):
            return source.__dars_route_metadata__

    return None


class SPARoute:
    """
    Represents a SPA route with client-side routing support.

    Features:
    - Route parameter extraction (``/user/:id``)
    - Pattern-based matching with regex
    - Nested route support via parent reference
    - Preloading configuration
    - Route guard support for private/protected routes
    """

    def __init__(
        self,
        name: str,
        root: Component,
        route: str,
        title: str = None,
        meta: dict = None,
        preload: List[str] = None,
        index: bool = False,
        parent: str = None,
        outlet_id: str = "main",
    ):
        self.name = name
        self.root = root
        self.route = route
        self.title = title
        self.meta = meta or {}
        self.preload = preload or []
        self.index = index
        self.parent = parent
        try:
            self.outlet_id = str(outlet_id or "main")
        except Exception:
            self.outlet_id = "main"

        self.params = self._extract_params(route)
        self.pattern = self._build_pattern(route)

    def _extract_params(self, route: str) -> List[str]:
        return re.findall(r":([a-zA-Z_][a-zA-Z0-9_]*)", route)

    def _build_pattern(self, route: str) -> str:
        pattern = re.sub(r":([a-zA-Z_][a-zA-Z0-9_]*)", r"(?P<\1>[^/]+)", route)
        return f"^{pattern}$"

    def matches(self, path: str) -> Optional[Dict[str, str]]:
        match = re.match(self.pattern, path)
        if match:
            return match.groupdict()
        return None

    def __repr__(self):
        return f"SPARoute(name='{self.name}', route='{self.route}', params={self.params})"


class RouteNode:
    """
    Node in the nested route tree structure.

    Used to build a hierarchy of routes for nested routing::

        /docs (parent)
        ├── /docs/getting-started (child)
        └── /docs/api (child)
    """

    def __init__(self, route: SPARoute = None):
        self.route = route
        self.children: List[RouteNode] = []

    def add_child(self, child_node: RouteNode):
        self.children.append(child_node)

    def find_route(self, path: str) -> Optional[tuple]:
        if self.route:
            params = self.route.matches(path)
            if params is not None:
                return (self.route, params)

        for child in self.children:
            result = child.find_route(path)
            if result:
                return result

        return None

    def __repr__(self):
        route_str = f"'{self.route.route}'" if self.route else "ROOT"
        return f"RouteNode({route_str}, children={len(self.children)})"
