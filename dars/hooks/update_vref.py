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
        ```python
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
        ```
    """
    
    
    def _to_structure(val):
        if hasattr(val, '_to_structure'):
            return val._to_structure()
        elif hasattr(val, 'data') and isinstance(val.data, dict):
            # If it's a dScript with data (action), we might treat it as a value?
            # Actions usually return void. But if it's an expression action (like get_dom_value), it returns value.
            # My current dScript logic differentiates actions vs values only by OP context.
            # Here we expect a VALUE.
            return val.data
        elif hasattr(val, 'get_action'): # dScript
             # If dScript has an action, assume it returns a value?
             act = val.get_action()
             if act: return act
             # If inline code, we can't use it easily in DAP unless we wrap in 'inline' op that returns value?
             # But we want to avoid inline.
             # If user passes dScript(code="..."), we fallback to legacy?
             # Ideally avoid.
             return getattr(val, 'code', str(val))
        return val

    # Handle batch updates (dict)
    if isinstance(selector, dict):
        actions = []
        for sel, val in selector.items():
            actions.append({
                "op": "vref_update", 
                "args": {
                    "selector": sel, 
                    "value": _to_structure(val)
                }
            })
        from dars.actionProtocol import Action
        return dScript(data=Action.sequence(actions))
    
    # Handle single update
    if value is None:
        raise ValueError("value parameter is required when selector is a string")
    
    return dScript(data={
        "op": "vref_update",
        "args": {
            "selector": selector,
            "value": _to_structure(value)
        }
    })
