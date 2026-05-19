# Dars Framework - Core Source File
#
# This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0.
# If a copy of the MPL was not distributed with this file, You can obtain one at
# https://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2025 ZtaDev
"""
Route Types for Secure Routing and SSR

This module defines route types for the Dars Framework:
- PUBLIC: Routes that load immediately (no authentication required)
- SSR: Server-Side Rendered routes (rendered on backend, fetched on navigation)
"""

from enum import Enum
from typing import List, Optional, TYPE_CHECKING

from fastapi.middleware import Middleware



class RouteType(Enum):
    """
    Enumeration of route types for security and rendering strategies.
    
    - PUBLIC: Client-side rendered, included in initial bundle
    - SSR: Server-side rendered, fetched from backend on navigation
    """
    PUBLIC = "public"
    SSR = "ssr"  # Server-Side Rendering


class RouteMetadata:
    """
    Metadata for a route including security and loading configuration.
    
    Attributes:
        path: Route path (e.g., "/home", "/admin")
        route_type: Type of route (PUBLIC, SSR)
        requires_auth: Whether route requires authentication
        middleware: List of middleware to apply
        loader_endpoint: Backend endpoint to load route from
    """
    
    def __init__(
        self,
        path: str,
        route_type: RouteType = RouteType.PUBLIC,
        requires_auth: bool = False,
        middleware: Optional[List['Middleware']] = None,
        loader_endpoint: Optional[str] = None
    ):
        """
        Initialize route metadata.
        
        Args:
            path: Route path
            route_type: Type of route (default: PUBLIC)
            requires_auth: Whether authentication is required
            middleware: List of middleware classes/instances
            loader_endpoint: Custom loader endpoint (auto-generated if None)
        """
        self.path = path
        self.route_type = route_type
        self.requires_auth = requires_auth
        self.middleware = middleware or []
        
        # Auto-generate loader endpoint for SSR routes
        if loader_endpoint:
            self.loader_endpoint = loader_endpoint
        elif route_type == RouteType.SSR:
            # SSR routes use /api/ssr/ prefix
            route_name = path.strip('/').replace('/', '_') or 'index'
            self.loader_endpoint = f"/api/ssr/{route_name}"
        else:
            self.loader_endpoint = None
    
    def to_dict(self) -> dict:
        """
        Convert metadata to dictionary for export.
        
        Returns:
            Dictionary representation
        """
        return {
            'path': self.path,
            'type': self.route_type.value,
            'requires_auth': self.requires_auth,
            'loader': self.loader_endpoint,
            'middleware': [m.__class__.__name__ for m in self.middleware]
        }
    
    def __repr__(self):
        return f"RouteMetadata(path='{self.path}', type={self.route_type.value}, auth={self.requires_auth})"
