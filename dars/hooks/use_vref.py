# Dars Framework - Core Source File
#
# This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0.
# If a copy of the MPL was not distributed with this file, You can obtain one at
# https://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2025 ZtaDev
"""
useVRef Hook - Reactive V() expressions without State dependencies

This module implements the useVRef() hook for creating reactive bindings
from V() expressions, enabling component-level reactivity.
"""

from typing import Union, List, Any, Optional
from dars.scripts.dscript import dScript
from dars.hooks.value_helpers import ValueRef, MathExpression, BooleanExpression, ConditionalExpression, LogicalExpression
import uuid

# Global registry for VRef bindings
_VREF_BINDINGS_REGISTRY = {}


class VRefBinding:
    """
    Represents a reactive V() expression binding.
    
    This creates a reactive span that automatically updates when dependencies change.
    
    Attributes:
        vexpr: Single V() expression, list of V() expressions, or direct value
        dependencies: Optional list of V() selectors to watch for changes
        callbacks: Optional list of dScript callbacks to execute on change
        marker: Unique marker for template replacement
        marker_id: Unique ID for this binding
    """
    
    def __init__(
        self,
        vexpr: Union[ValueRef, MathExpression, BooleanExpression, ConditionalExpression, LogicalExpression, List, Any],
        dependencies: Optional[List[ValueRef]] = None,
        callbacks: Optional[List[Union[dScript, str]]] = None
    ):
        """
        Initialize a VRef binding.
        
        Args:
            vexpr: V() expression(s) or direct value
            dependencies: Optional V() selectors to watch
            callbacks: Optional callbacks to execute on change
        """
        self.vexpr = vexpr
        self.dependencies = dependencies or []
        self.callbacks = callbacks or []
        
        # Generate unique marker
        self.marker_id = str(uuid.uuid4()).replace('-', '_')
        self.marker = f"__DARS_VREF_{self.marker_id}__"
        
        # Register globally
        _VREF_BINDINGS_REGISTRY[self.marker_id] = self
    
    def __str__(self):
        """Return marker for template replacement."""
        return self.marker
    
    def get_initial_value(self) -> Any:
        """
        Resolve V() expression to initial value.
        
        For V() expressions, this returns a placeholder since actual
        evaluation happens client-side. For direct values, returns the value.
        
        Returns:
            Initial value or placeholder
        """
        # Check if it's a direct value (not a V() expression)
        if not isinstance(self.vexpr, (ValueRef, MathExpression, BooleanExpression, ConditionalExpression, LogicalExpression, list)):
            return str(self.vexpr)
        
        # For V() expressions, return empty placeholder
        # Actual value will be resolved client-side
        return ""
    
    def generate_reactive_js(self, component_id: str) -> str:
        """
        Generate JavaScript for reactive binding.
        
        Args:
            component_id: ID of the component containing this binding
            
        Returns:
            JavaScript code for reactive updates
        """
        # Generate V() expression code
        if isinstance(self.vexpr, (ValueRef, MathExpression, BooleanExpression, ConditionalExpression, LogicalExpression)):
            vexpr_code = self.vexpr._get_code()
        elif isinstance(self.vexpr, list):
            # Array of expressions
            vexpr_code = "[" + ", ".join(
                expr._get_code() if isinstance(expr, (ValueRef, MathExpression, BooleanExpression, ConditionalExpression, LogicalExpression))
                else f"'{expr}'"
                for expr in self.vexpr
            ) + "]"
        else:
            # Direct value
            if isinstance(self.vexpr, str):
                vexpr_code = f"'{self.vexpr}'"
            else:
                vexpr_code = str(self.vexpr)
        
        # Generate dependency selectors
        dep_selectors = []
        for dep in self.dependencies:
            if isinstance(dep, ValueRef):
                dep_selectors.append(f"'{dep.selector}'")
        
        # Generate callback code
        callback_code = ""
        if self.callbacks:
            callback_lines = []
            for cb in self.callbacks:
                if isinstance(cb, dScript):
                    callback_lines.append(cb.code)
                else:
                    callback_lines.append(str(cb))
            callback_code = "\n".join(callback_lines)
        
        js_code = f"""
// VRef binding: {self.marker_id}
(function() {{
    const marker = '{self.marker}';
    const vexprCode = async () => {{ return await ({vexpr_code}); }};
    const dependencies = [{', '.join(dep_selectors)}];
    const callbacks = function() {{
        {callback_code}
    }};
    
    // Register binding
    if (!window.__DARS_VREF_BINDINGS__) {{
        window.__DARS_VREF_BINDINGS__ = [];
    }}
    
    window.__DARS_VREF_BINDINGS__.push({{
        marker: marker,
        vexpr: vexprCode,
        dependencies: dependencies,
        callbacks: callbacks,
        elements: []
    }});
    
    // Find and store elements with this marker
    document.addEventListener('DOMContentLoaded', async function() {{
        const binding = window.__DARS_VREF_BINDINGS__.find(b => b.marker === marker);
        if (binding) {{
            binding.elements = Array.from(document.querySelectorAll(`[data-vref="${{marker}}"]`));
            
            // Initial evaluation
            try {{
                const value = await binding.vexpr();
                binding.elements.forEach(el => {{
                    el.textContent = value !== null && value !== undefined ? value : '';
                }});
            }} catch (e) {{
                console.error('[Dars VRef] Error evaluating expression:', e);
            }}
        }}
    }});
}})();
        """.strip()
        
        return js_code


def useVRef(
    vexpr: Union[ValueRef, MathExpression, BooleanExpression, ConditionalExpression, LogicalExpression, List, Any],
    dependencies: Optional[List[ValueRef]] = None,
    callbacks: Optional[List[Union[dScript, str]]] = None
) -> VRefBinding:
    """
    Create a reactive binding from V() expression(s).
    
    This hook enables component-level reactivity using V() expressions without
    requiring State objects. The binding automatically updates when dependencies change.
    
    Args:
        vexpr: V() expression, list of V() expressions, or direct value
        dependencies: Optional list of V() selectors to watch for changes
        callbacks: Optional list of dScript callbacks to execute on change
        
    Returns:
        VRefBinding object for use in component props or FunctionComponent templates
        
    Examples:
        # Single V() expression
        Text(text=useVRef(V("#price").float() * 1.21))
        
        # With dependencies (re-evaluate when cart.total changes)
        Text(text=useVRef(
            V("cart.total").float() + 10,
            dependencies=[V("cart.total")]
        ))
        
        # With callbacks
        Input(value=useVRef(
            V("#input"),
            callbacks=[log("Value changed")]
        ))
        
        # Direct value (static)
        Text(text=useVRef(42))
        Text(text=useVRef("Hello"))
        
        # Boolean expression
        Text(text=useVRef(
            (V("#age").int() >= 18).then("Adult", "Minor"),
            dependencies=[V("#age")]
        ))
    """
    return VRefBinding(vexpr, dependencies, callbacks)
