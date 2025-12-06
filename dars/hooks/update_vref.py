# Dars Framework - Core Source File
#
# This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0.
# If a copy of the MPL was not distributed with this file, You can obtain one at
# https://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2025 ZtaDev
"""
updateVRef Function - Pythonic VRef value updates

This module implements the updateVRef() function for updating VRef values
and triggering dependent bindings without inline JavaScript.
"""

from typing import Any, Union, Dict
from dars.scripts.dscript import dScript
from dars.hooks.value_helpers import ValueRef, MathExpression, BooleanExpression, ConditionalExpression, LogicalExpression


def updateVRef(
    selector: Union[str, Dict[str, Any]], 
    value: Any = None
) -> dScript:
    """
    Update a VRef value or DOM element and trigger dependent bindings.
    
    This function provides a Pythonic way to update values without writing
    inline JavaScript. It works with both VRef values (set via setVRef) and
    regular DOM elements.
    
    Args:
        selector: CSS selector string or dict of {selector: value} pairs
        value: Value to set (string, number, bool, ValueRef, or expression)
               Ignored if selector is a dict
        
    Returns:
        dScript object for use in event handlers
        
    Examples:
        # Single update
        Button(on_click=updateVRef("#name", "John"))
        
        # With ValueRef
        Button(on_click=updateVRef("#target", V("#source")))
        
        # With expression
        Button(on_click=updateVRef("#result", V("#a").int() + V("#b").int()))
        
        # With boolean expression
        Button(on_click=updateVRef("#status",
            (V("#age").int() >= 18).then("Adult", "Minor")
        ))
        
        # Batch update
        Button(on_click=updateVRef({
            "#name": "John",
            "#email": "john@example.com",
            "#age": 25
        }))
        
        # Update VRef value (set via setVRef)
        Button(on_click=updateVRef(".product-price", 149.99))
    """
    
    def _generate_value_code(val: Any) -> str:
        """Generate JavaScript code for a value."""
        if isinstance(val, (ValueRef, MathExpression, BooleanExpression, ConditionalExpression, LogicalExpression)):
            return f"await ({val._get_code()})"
        elif isinstance(val, bool):
            return "true" if val else "false"
        elif isinstance(val, str):
            # Check if it's already a V() expression code
            if val.startswith("await ("):
                return val
            return f"'{val}'"
        elif isinstance(val, (int, float)):
            return str(val)
        else:
            return f"'{str(val)}'"
    
    def _generate_update_code(sel: str, val: Any) -> str:
        """Generate JavaScript code to update one or more elements."""
        value_code = _generate_value_code(val)
        
        return f"""
    // Update {sel}
    (async () => {{
        const selector = '{sel}';
        const value = {value_code};
        
        // Update VRef value if exists
        if (window.__DARS_VREF_VALUES__ && selector in window.__DARS_VREF_VALUES__) {{
            window.__DARS_VREF_VALUES__[selector] = value;
        }}
        
        // Update DOM elements
        const elements = document.querySelectorAll(selector);
        elements.forEach(el => {{
            // Handle different element types
            if (el.tagName === 'INPUT' || el.tagName === 'TEXTAREA') {{
                if (el.type === 'checkbox' || el.type === 'radio') {{
                    el.checked = Boolean(value);
                }} else {{
                    el.value = value;
                }}
            }} else if (el.tagName === 'SELECT') {{
                el.value = value;
            }} else {{
                el.textContent = value;
            }}
        }});
        
        // Trigger VRef bindings update
        if (window.Dars && window.Dars.updateVRef) {{
            window.Dars.updateVRef(selector);
        }}
    }})();
        """.strip()
    
    # Handle batch updates (dict)
    if isinstance(selector, dict):
        update_codes = []
        for sel, val in selector.items():
            update_codes.append(_generate_update_code(sel, val))
        
        js_code = "\n".join(update_codes)
        return dScript(js_code)
    
    # Handle single update
    if value is None:
        raise ValueError("value parameter is required when selector is a string")
    
    js_code = _generate_update_code(selector, value)
    return dScript(js_code)
