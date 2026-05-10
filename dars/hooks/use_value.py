# Dars Framework - Core Source File
#
# This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0.
# If a copy of the MPL was not distributed with this file, You can obtain one at
# https://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2025 ZtaDev
"""
useValue Hook

Enables non-reactive initial value binding with explicit selector-based DOM value extraction.
"""

from typing import Optional
from dars.scripts.dscript import dScript
import time


# Global registry for value markers
_VALUE_REGISTRY = {}


class ValueMarker:
    """
    Represents a non-reactive value binding with explicit selector.
    
    Unlike DynamicBinding (useDynamic), this does NOT create reactive bindings.
    It only sets the initial value from state, then allows the user to edit freely.
    """
    
    def __init__(self, state_path: str, selector: str = None):
        """
        Initialize a ValueMarker.
        
        Args:
            state_path: Dot-notation path to state property (e.g., "user.name")
            selector: CSS selector for DOM element (Optional)
        """
        self.state_path = state_path
        self.selector = selector
        self.marker_id = f"__DARS_VALUE_{id(self)}_{int(time.time()*1000)}__"
        
        # Always register in global registry to allow template resolution
        _VALUE_REGISTRY[self.marker_id] = self
    
    def __str__(self):
        """
        Return the marker ID string.
        This allows the exporter to detect and process the marker in FunctionComponent templates.
        """
        return self.marker_id
    
    def __repr__(self):
        return f"ValueMarker(state_path='{self.state_path}', selector='{self.selector}')"
    
    def get_initial_value(self):
        """
        Resolve initial value from State V2 registry.
        
        Returns:
            Initial value from state, or empty string if not found
        """
        try:
            from dars.core.state_v2 import STATE_V2_REGISTRY
            
            parts = self.state_path.split('.')
            if len(parts) < 2:
                return ""
            
            state_id = parts[0]
            prop_name = parts[1]
            
            # Find state in registry (search in reverse to get the latest instance)
            state = next((s for s in reversed(STATE_V2_REGISTRY) if s.component.id == state_id), None)
            if not state:
                return ""
            
            # Get property value
            prop = getattr(state, prop_name, None)
            if prop and hasattr(prop, 'value'):
                return prop.value
            
            return ""
        except Exception:
            return ""


class UseValueSelector:
    """Helper class for DOM value extraction"""
    
    @staticmethod
    def select(selector: str) -> dScript:
        """
        Generate dScript to get current value from DOM element.
        
        Returns dScript (not RawJS) to enable:
        - Chaining with .then()
        - Use in backend API calls (fetch, get, post)
        - Integration with State V2 updates
        
        Args:
            selector: CSS selector for target element
        
        Returns:
            dScript that resolves to the element's current value
        
        Example:
            # Basic usage
            value = useValue.select(".username-input")
            
            # In event handler
            Button(on_click=userState.name.set(useValue.select(".input")))
            
            # With chaining
            useValue.select(".email").then(
                dScript("console.log('Email:', value)")
            )
        """
        js_code = f"""
(async () => {{
    try {{
        const el = document.querySelector('{selector}');
        if (!el) {{
            console.warn('useValue.select: Element not found for selector: {selector}');
            return '';
        }}
        
        // Handle different element types
        if (el.tagName === 'INPUT' || el.tagName === 'TEXTAREA') {{
            return el.value || '';
        }}
        if (el.tagName === 'SELECT') {{
            return el.value || '';
        }}
        if (el.type === 'checkbox') {{
            return el.checked;
        }}
        // Fallback to textContent
        return el.textContent || '';
    }} catch (e) {{
        console.error('useValue.select error:', e);
        return '';
    }}
}})()
        """
        
        # return dScript(js_code.strip())
        # Use secure DAP action
        return dScript(data={
            "op": "get_dom_value",
            "args": {"selector": selector}
        })


def useValue(state_path: str, selector: str = None) -> ValueMarker:
    """
    Set initial value from state (non-reactive).
    
    This hook allows components to have their initial value set from state,
    but does NOT create a reactive binding. The user can then modify the value
    freely without it being overwritten by state changes.
    
    Args:
        state_path: Dot-notation path (e.g., "user.name")
        selector: CSS selector for DOM element (Optional, used for easy targeting)
    
    Returns:
        ValueMarker instance (resolves to initial value string in templates)
    
    Example:
        ```python
        In FunctionComponent template (resolves to string)
        <div>{useValue("user.name")}</div>
        
        In component props with selector
        Input(value=useValue("user.name", "input.name-field"))
        ```
    """
    return ValueMarker(state_path, selector)


# Attach selector helper to useValue function
useValue.select = UseValueSelector.select


def get_value_registry():
    """Get the global value registry"""
    return _VALUE_REGISTRY


def clear_value_registry():
    """Clear the global value registry (useful for testing/resets)"""
    global _VALUE_REGISTRY
    _VALUE_REGISTRY = {}
