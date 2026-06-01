# Dars Framework - Core Source File
#
# This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0.
# If a copy of the MPL was not distributed with this file, You can obtain one at
# https://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2026 ZtaDev
"""
Route Types for Secure Routing, SSR, and Privacy

This module defines route types for the Dars Framework:

- PUBLIC: Routes that load immediately, no authentication required.
- SSR: Server-Side Rendered routes (rendered on backend, fetched on navigation).
- PRIVATE: Routes that require authentication. Redirect to login if unauthenticated.
- PROTECTED: Routes that require authentication AND specific roles/permissions.

Route types support a guard system for client-side routing:

    @route("/dashboard", route_type=RouteType.PRIVATE)
    def dashboard():
        return Page(...)

    @route("/admin", route_type=RouteType.PROTECTED, roles=["admin"])
    def admin_panel():
        return Page(...)
"""

from __future__ import annotations

from enum import Enum
from typing import Any, Callable, Dict, List, Optional, TYPE_CHECKING

from pydantic import BaseModel, Field

if TYPE_CHECKING:
    from fastapi import Request
    from starlette.middleware.base import BaseHTTPMiddleware


class RouteType(Enum):
    """
    Enumeration of route types for security and rendering strategies.

    - PUBLIC: Client-side rendered, included in initial bundle. No auth required.
    - SSR: Server-side rendered, fetched from backend on navigation.
    - PRIVATE: Requires authentication. Not included in initial client bundle.
               Client-side router checks auth before loading. Redirects to login.
    - PROTECTED: Requires authentication AND specific role/permission.
    """
    PUBLIC = "public"
    SSR = "ssr"
    PRIVATE = "private"
    PROTECTED = "protected"


class RouteGuard(BaseModel):
    """
    A guard that protects a route from unauthorized access.

    Attributes:
        requires_auth: If True, the user must be authenticated.
        roles: List of roles permitted to access this route.
        redirect: Path to redirect unauthenticated users (default ``"/login"``).
        custom_check: Optional callable ``(user: dict) -> bool`` for custom logic.
    """
    requires_auth: bool = False
    roles: List[str] = Field(default_factory=list)
    redirect: Optional[str] = None
    custom_check: Optional[Callable[[Dict[str, Any]], bool]] = None

    class Config:
        arbitrary_types_allowed = True

    def check(self, user: Optional[Dict[str, Any]]) -> bool:
        """
        Check if a user passes this guard.

        Args:
            user: The user dict from ``request.state.user`` or ``None``.

        Returns:
            ``True`` if the user should be granted access.
        """
        if not self.requires_auth and not self.roles:
            return True

        if self.requires_auth and not user:
            return False

        if self.roles and user:
            user_roles = user.get("roles", [])
            if isinstance(user_roles, str):
                user_roles = [user_roles]
            if not any(r in user_roles for r in self.roles):
                return False

        if self.custom_check is not None and user is not None:
            try:
                return bool(self.custom_check(user))
            except Exception:
                return False

        return True

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to a dict for client-side router configuration."""
        d: Dict[str, Any] = {
            "requires_auth": self.requires_auth,
        }
        if self.redirect:
            d["redirect"] = self.redirect
        if self.roles:
            d["roles"] = self.roles
        return d


class RouteMetadata(BaseModel):
    """
    Metadata for a route including security, rendering, and guard configuration.

    Attributes:
        path: Route path (e.g., ``"/home"``, ``"/admin"``).
        route_type: Type of route (PUBLIC, SSR, PRIVATE, PROTECTED).
        requires_auth: Whether route requires authentication (shorthand).
        guard: Optional :class:`RouteGuard` for fine-grained access control.
        middleware: List of FastAPI middleware classes to apply.
        loader_endpoint: Backend endpoint to load route from.
        auth_id: Auth configuration ID for multi-auth support.
        roles: List of roles required (for PROTECTED routes).
    """
    path: str
    route_type: RouteType = RouteType.PUBLIC
    requires_auth: bool = False
    guard: Optional[RouteGuard] = None
    middleware: List[Any] = Field(default_factory=list)
    loader_endpoint: Optional[str] = None
    auth_id: Optional[str] = None
    roles: List[str] = Field(default_factory=list)

    class Config:
        arbitrary_types_allowed = True

    def __init__(self, **data: Any) -> None:
        super().__init__(**data)

        # Auto-derive guard from route_type and shorthand params
        if self.guard is None:
            if self.route_type == RouteType.PRIVATE or self.requires_auth:
                self.guard = RouteGuard(requires_auth=True, roles=self.roles)
            elif self.route_type == RouteType.PROTECTED:
                self.guard = RouteGuard(requires_auth=True, roles=self.roles or ["admin"])
            elif self.roles:
                self.guard = RouteGuard(requires_auth=True, roles=self.roles)

        # Auto-generate loader endpoint for SSR/PRIVATE routes
        if self.loader_endpoint is None:
            route_name = self.path.strip("/").replace("/", "_") or "index"
            if self.route_type in (RouteType.SSR, RouteType.PRIVATE, RouteType.PROTECTED):
                self.loader_endpoint = f"/api/ssr/{route_name}"

    def to_dict(self) -> Dict[str, Any]:
        """Convert metadata to dictionary for export (client-side config)."""
        d: Dict[str, Any] = {
            "path": self.path,
            "type": self.route_type.value,
            "requires_auth": self.requires_auth or self.route_type in (RouteType.PRIVATE, RouteType.PROTECTED),
            "auth_id": self.auth_id,
            "loader": self.loader_endpoint,
        }
        if self.guard is not None:
            d["guard"] = self.guard.to_dict()
        if self.roles:
            d["roles"] = self.roles
        try:
            d["middleware"] = [m.__class__.__name__ for m in self.middleware]
        except Exception:
            d["middleware"] = []
        return d

    def __repr__(self) -> str:
        return (
            f"RouteMetadata(path='{self.path}', "
            f"type={self.route_type.value}, "
            f"auth={self.requires_auth}, "
            f"guard={self.guard is not None})"
        )
