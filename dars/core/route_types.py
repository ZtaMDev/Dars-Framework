# Dars Framework - Core Source File
#
# This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0.
# If a copy of the MPL was not distributed with this file, You can obtain one at
# https://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2025 ZtaDev
"""
Route Types for Secure Routing

This module defines route types for the Dars Framework security system:
- PUBLIC: Routes that load immediately (no authentication required)
- PRIVATE: Routes that require authentication (lazy loaded from backend)
- PROTECTED: Routes with custom middleware (lazy loaded with middleware check)
"""

from enum import Enum
from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from dars.middleware.base import Middleware


class RouteType(Enum):
    """
    Route type enum for security and lazy loading.
    
    Attributes:
        PUBLIC: Route loads immediately, no authentication required
        PRIVATE: Route requires authentication, lazy loaded from backend
        PROTECTED: Route with custom middleware, lazy loaded with checks
    """
    PUBLIC = "public"
    PRIVATE = "private"
    PROTECTED = "protected"


class RouteMetadata:
    """
    Metadata for a route including security and loading configuration.
    
    Attributes:
        path: Route path (e.g., "/home", "/admin")
        route_type: Type of route (PUBLIC, PRIVATE, PROTECTED)
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
        
        # Auto-generate loader endpoint for private/protected routes
        if loader_endpoint:
            self.loader_endpoint = loader_endpoint
        elif route_type in (RouteType.PRIVATE, RouteType.PROTECTED):
            # Extract route name from path
            route_name = path.strip('/').replace('/', '_') or 'index'
            self.loader_endpoint = f"/api/routes/{route_name}"
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
