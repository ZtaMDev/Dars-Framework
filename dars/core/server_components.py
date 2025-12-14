# Dars Framework - Core Source File
#
# This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0.
# If a copy of the MPL was not distributed with this file, You can obtain one at
# https://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2025 ZtaDev
"""
Dars Server Components - Backend-rendered component system.

Enables components with use_server=True to be rendered by FastAPI backend,
providing a Next.js-like experience for Python developers.

Usage:
    # Mark a component for server-side rendering
    chart = Chart(data=my_data, use_server=True, id="my-chart")
    chart.set_loading_state(
        loading_comp=Spinner(),
        on_error_comp=Text("Failed to load")
    )
"""

from typing import Dict, Any, Optional, TYPE_CHECKING
import json

if TYPE_CHECKING:
    from dars.core.component import Component

# Global configuration for server components
SSR_BASE_URL: str = ""  # Set by exporter from app.ssr_url

# Global registry for server components
# Maps component ID -> Component instance for backend rendering
SERVER_COMPONENT_REGISTRY: Dict[str, 'Component'] = {}


def set_ssr_base_url(url: str) -> None:
    """Set the base URL for server component endpoints. Called by exporter."""
    global SSR_BASE_URL
    SSR_BASE_URL = (url or "").rstrip('/')


class ServerComponentMarker:
    """
    Marker class for server component placeholders.
    
    Used by the exporter to generate placeholder HTML that will be
    replaced by server-rendered content at runtime.
    """
    
    def __init__(self, component: 'Component', backend_url: str = ""):
        self.component = component
        self.component_id = component.id
        self.component_type = type(component).__name__
        # Use provided backend_url, or fall back to global SSR_BASE_URL
        self.backend_url = (backend_url.rstrip('/') if backend_url else SSR_BASE_URL) or ""
        self.endpoint = f"{self.backend_url}/api/server-component/{component.id}"
        
    def to_placeholder_html(self, loading_html: str = "", error_html: str = "") -> str:
        """
        Generate placeholder HTML with data attributes for hydration.
        
        The placeholder includes:
        - data-server-component: marker for JS runtime detection
        - data-sc-endpoint: backend URL to fetch rendered content
        - data-sc-type: component type for debugging
        - data-sc-error: error HTML to show on failure (optional)
        """
        error_attr = ""
        if error_html:
            # Escape for attribute embedding
            escaped_error = error_html.replace('"', '&quot;').replace('\n', ' ')
            error_attr = f' data-sc-error="{escaped_error}"'
        
        return f'''<div id="{self.component_id}" class="dars-server-component dars-sc-loading" data-server-component="true" data-sc-endpoint="{self.endpoint}" data-sc-type="{self.component_type}"{error_attr}>{loading_html}</div>'''


def register_server_component(component: 'Component') -> str:
    """
    Register a component for server-side rendering.
    
    This adds the component to the SERVER_COMPONENT_REGISTRY so that
    the backend SSR endpoint can look it up and render it.
    
    Args:
        component: The component instance to register
        
    Returns:
        The component's ID (generated if not set)
    """
    if not component.id:
        # Generate ID if not set
        import uuid
        component.id = f"sc_{uuid.uuid4().hex[:8]}"
    
    SERVER_COMPONENT_REGISTRY[component.id] = component
    return component.id


def clear_server_component_registry():
    """Clear the server component registry. Used for hot reload."""
    SERVER_COMPONENT_REGISTRY.clear()


def get_server_component(component_id: str) -> Optional['Component']:
    """
    Get a registered server component by ID.
    
    Args:
        component_id: The component's ID
        
    Returns:
        The component instance, or None if not found
    """
    return SERVER_COMPONENT_REGISTRY.get(component_id)
