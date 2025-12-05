# Dars Framework - Core Source File
#
# This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0.
# If a copy of the MPL was not distributed with this file, You can obtain one at
# https://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2025 ZtaDev
"""
setVRef Hook - Direct value setting with V() selector access

This module implements the setVRef() hook for setting values that can be
accessed via V() selectors without creating State objects.
"""

from typing import Any
import uuid

# Global registry for VRef values
_VREF_VALUES_REGISTRY = {}


class VRefValue:
    """
    Represents a value accessible via V() selector.
    
    This allows setting values that can be read by V() expressions
    without creating State objects.
    
    Attributes:
        value: The actual value (number, string, bool, etc.)
        selector: CSS selector for V() access
        marker: Unique marker for template replacement
        marker_id: Unique ID for this value
    """
    
    def __init__(self, value: Any, selector: str):
        """
        Initialize a VRef value.
        
        Args:
            value: The value to set
            selector: CSS selector (class or ID) for V() access
            
        Raises:
            ValueError: If selector format is invalid
        """
        # Validate selector format
        if not selector or (not selector.startswith('.') and not selector.startswith('#')):
            raise ValueError(
                f"Invalid selector '{selector}'. "
                "Selector must start with '.' (class) or '#' (ID)."
            )
        
        self.value = value
        self.selector = selector
        
        # Generate unique marker
        self.marker_id = str(uuid.uuid4()).replace('-', '_')
        self.marker = f"__DARS_VREF_VALUE_{self.marker_id}__"
        
        # Register globally
        _VREF_VALUES_REGISTRY[self.marker_id] = self
    
    def __str__(self):
        """Return marker for template replacement."""
        return self.marker
    
    def get_initial_value(self) -> Any:
        """
        Return the stored value.
        
        Returns:
            The initial value
        """
        return str(self.value) if not isinstance(self.value, (int, float, bool)) else self.value
    
    def generate_registry_js(self) -> str:
        """
        Generate JavaScript to register value in window.__DARS_VREF_VALUES__.
        
        Returns:
            JavaScript code for value registration
        """
        # Format value for JavaScript
        if isinstance(self.value, bool):
            js_value = "true" if self.value else "false"
        elif isinstance(self.value, str):
            js_value = f"'{self.value}'"
        else:
            js_value = str(self.value)
        
        js_code = f"""
// VRef value: {self.selector}
(function() {{
    if (!window.__DARS_VREF_VALUES__) {{
        window.__DARS_VREF_VALUES__ = {{}};
    }}
    window.__DARS_VREF_VALUES__['{self.selector}'] = {js_value};
}})();
        """.strip()
        
        return js_code


def setVRef(value: Any, selector: str) -> VRefValue:
    """
    Set a value accessible via V() selector.
    
    This hook allows you to set values that can be read by V() expressions
    without creating State objects. Perfect for component-level state.
    
    Args:
        value: The value to set (number, string, bool, etc.)
        selector: CSS selector for V() access (must start with '.' or '#')
        
    Returns:
        VRefValue object for use in component props or FunctionComponent templates
        
    Raises:
        ValueError: If selector format is invalid
        
    Examples:
        # Set a value with selector
        price = setVRef(value=99.99, selector=".product-price")
        
        # Use in component prop
        Text(text=price)  # Displays: 99.99
        
        # Or in FunctionComponent template
        @FunctionComponent
        def ProductPrice(**props):
            price = setVRef(value=99.99, selector=".product-price")
            return f'''
            <div>
                <span>{price}</span>
            </div>
            '''
        
        # Access from another component using V()
        total = useVRef(V(".product-price").float() * V(".quantity").int())
        Text(text=total)
        
        # Update via updateVRef() function
        Button(on_click=updateVRef(".product-price", 149.99))
    """
    return VRefValue(value, selector)
