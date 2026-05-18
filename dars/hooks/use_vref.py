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
from dars.scripts.dscript import RawJS
from dars.hooks.value_helpers import ValueRef, MathExpression, BooleanExpression, ConditionalExpression, LogicalExpression
import uuid

# Global registry for VRef bindings
_VREF_BINDINGS_REGISTRY = {}


class VRefBinding:
    """
    Represents a reactive V() expression binding.
    
    This creates a reactive span that automatically updates when dependencies change.
    Dependencies are auto-detected from the V() expression tree, so you only need
    to specify them manually for edge cases.
    
    Attributes:
        vexpr: Single V() expression, list of V() expressions, or direct value
        dependencies: Optional explicit list of V() selectors to watch for changes
        callbacks: Optional list of dScript, RawJS, or str callbacks to execute on change
        marker: Unique marker for template replacement
        marker_id: Unique ID for this binding
    """
    
    def __init__(
        self,
        vexpr: Union[ValueRef, MathExpression, BooleanExpression, ConditionalExpression, LogicalExpression, List, Any],
        dependencies: Optional[List[ValueRef]] = None,
        callbacks: Optional[Union[dScript, RawJS, str, List[Union[dScript, RawJS, str]]]] = None
    ):
        """
        Initialize a VRef binding.
        
        Args:
            vexpr: V() expression(s) or direct value
            dependencies: Optional explicit V() selectors to watch.
                          If omitted, selectors are auto-detected from the expression tree.
            callbacks: Optional callback(s) to execute on change.
                       Accepts a single dScript, RawJS, or str, OR a list of those.
        """
        self.vexpr = vexpr
        self.dependencies = dependencies or []
        
        # Normalize callbacks: always store as a list
        if callbacks is None:
            self.callbacks = []
        elif isinstance(callbacks, list):
            self.callbacks = callbacks
        else:
            # Single callback (dScript, RawJS, or str) — wrap in list
            self.callbacks = [callbacks]
        
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
            
        # Check if it's a single ValueRef and we have its initial value in the registry
        if isinstance(self.vexpr, ValueRef):
            from dars.hooks.set_vref import _VREF_VALUES_REGISTRY
            for vref_val in _VREF_VALUES_REGISTRY.values():
                if getattr(vref_val, 'selector', None) == self.vexpr.selector:
                    return vref_val.get_initial_value()
        
        # For complex V() expressions or if not found, return empty placeholder
        # Actual value will be resolved client-side
        return ""
    
    def _extract_selectors(self, expr) -> list:
        """
        Recursively walk a V() expression tree and collect all CSS selectors.
        Used for auto-detecting which VRef values this binding depends on.
        """
        selectors = []
        if expr is None:
            return selectors
        if isinstance(expr, ValueRef):
            selectors.append(expr.selector)
        elif isinstance(expr, (MathExpression, BooleanExpression, LogicalExpression)):
            selectors.extend(self._extract_selectors(getattr(expr, 'left', None)))
            selectors.extend(self._extract_selectors(getattr(expr, 'right', None)))
            # DynamicOperator inside math expressions
            op = getattr(expr, 'operator', None)
            if op and hasattr(op, 'value_ref'):
                selectors.extend(self._extract_selectors(op.value_ref))
        elif isinstance(expr, ConditionalExpression):
            selectors.extend(self._extract_selectors(getattr(expr, 'condition', None)))
            selectors.extend(self._extract_selectors(getattr(expr, 'true_value', None)))
            selectors.extend(self._extract_selectors(getattr(expr, 'false_value', None)))
        elif isinstance(expr, list):
            for item in expr:
                selectors.extend(self._extract_selectors(item))
        # Deduplicate, preserve order, remove empty strings
        seen = set()
        result = []
        for s in selectors:
            if s and s not in seen:
                seen.add(s)
                result.append(s)
        return result

    def generate_reactive_js(self, component_id: str) -> str:
        """
        Generate JavaScript for reactive binding.
        
        Auto-detects dependency selectors from the V() expression tree so the
        runtime knows which vref_update calls should re-evaluate this binding.
        
        Args:
            component_id: ID of the component containing this binding
            
        Returns:
            JavaScript code for reactive updates
        """
        # Generate V() expression code
        if isinstance(self.vexpr, (ValueRef, MathExpression, BooleanExpression, ConditionalExpression, LogicalExpression)):
            vexpr_code = self.vexpr._get_code()
        elif isinstance(self.vexpr, list):
            vexpr_code = "[" + ", ".join(
                expr._get_code() if isinstance(expr, (ValueRef, MathExpression, BooleanExpression, ConditionalExpression, LogicalExpression))
                else f"'{expr}'"
                for expr in self.vexpr
            ) + "]"
        else:
            if isinstance(self.vexpr, str):
                vexpr_code = f"'{self.vexpr}'"
            else:
                vexpr_code = str(self.vexpr)
        
        # Build dependency selector list.
        # Explicit dependencies override auto-detection.
        if self.dependencies:
            dep_selectors = [f"'{dep.selector}'" for dep in self.dependencies if isinstance(dep, ValueRef)]
        else:
            dep_selectors = [f"'{s}'" for s in self._extract_selectors(self.vexpr)]
        
        # Generate callback code
        callback_code = ""
        if self.callbacks:
            callback_lines = []
            for cb in self.callbacks:
                if isinstance(cb, RawJS):
                    callback_lines.append(cb.code)
                elif isinstance(cb, dScript):
                    if cb.code is not None:
                        callback_lines.append(cb.code)
                    elif cb.data is not None:
                        import json
                        action_json = json.dumps(cb.data, ensure_ascii=False)
                        callback_lines.append(
                            f"(async () => {{ try {{ const _dap = await import('./lib/dap.js'); "
                            f"await _dap.dispatch({action_json}); }} catch(_e) {{}} }})();"
                        )
                else:
                    callback_lines.append(str(cb))
            callback_code = "\n        ".join(callback_lines)
        
        js_code = f"""
// VRef binding: {self.marker_id}
(function() {{
    const marker = '{self.marker}';
    const vexprFn = async () => {{ return await ({vexpr_code}); }};
    // Auto-detected selectors this binding reads from.
    // vref_update uses this list to know which bindings to re-evaluate.
    const dependencies = [{', '.join(dep_selectors)}];
    const callbacksFn = async function() {{
        {callback_code}
    }};
    
    if (!window.__DARS_VREF_BINDINGS__) {{
        window.__DARS_VREF_BINDINGS__ = [];
    }}
    
    window.__DARS_VREF_BINDINGS__.push({{
        marker: marker,
        vexpr: vexprFn,
        dependencies: dependencies,
        callbacks: callbacksFn,
        elements: []
    }});
    
    // Resolve elements and run initial evaluation.
    // Works whether DOMContentLoaded has already fired or not.
    function _initBinding() {{
        const binding = window.__DARS_VREF_BINDINGS__.find(b => b.marker === marker);
        if (!binding) return;
        binding.elements = Array.from(document.querySelectorAll('[data-vref="' + marker + '"]'));
        if (binding.elements.length === 0) return;
        (async () => {{
            try {{
                const value = await binding.vexpr();
                const strVal = (value !== null && value !== undefined) ? String(value) : '';
                binding.elements.forEach(el => {{ el.textContent = strVal; }});
            }} catch (e) {{
                console.error('[Dars VRef] Error evaluating expression:', e);
            }}
        }})();
    }}
    
    if (document.readyState === 'complete' || document.readyState === 'interactive') {{
        _initBinding();
    }} else {{
        document.addEventListener('DOMContentLoaded', _initBinding);
    }}
}})();
        """.strip()
        
        return js_code


def useVRef(
    vexpr: Union[ValueRef, MathExpression, BooleanExpression, ConditionalExpression, LogicalExpression, List, Any],
    dependencies: Optional[List[ValueRef]] = None,
    callbacks: Optional[Union[dScript, RawJS, str, List[Union[dScript, RawJS, str]]]] = None
) -> VRefBinding:
    """
    Create a reactive binding from V() expression(s).
    
    This hook enables component-level reactivity using V() expressions without
    requiring State objects. The binding automatically updates when any of the
    V() selectors it reads from are updated via updateVRef().
    
    Dependency selectors are auto-detected from the expression tree, so you
    rarely need to specify them manually.
    
    The initial value is pre-resolved at build time from the setVRef registry
    when possible, ensuring zero-flash SSR rendering.
    
    Args:
        vexpr: V() expression, list of V() expressions, or direct value
        dependencies: Optional explicit list of V() selectors to watch.
                      If omitted, selectors are auto-detected from the expression.
        callbacks: Optional callback(s) to execute whenever the binding re-evaluates.
                   Accepts a single dScript, RawJS, or str, OR a list of those.
        
    Returns:
        VRefBinding object for use in component props or FunctionComponent templates
        
    Examples:
        ```python
        from dars.all import *
        from dars.scripts.dscript import RawJS
        
        # Single V() expression — auto-detects .item-price as dependency
        price = setVRef(10.0, ".item-price")
        Text(text=useVRef(V(".item-price")))
        
        # Math expression — auto-detects both selectors
        Text(text=useVRef(V(".price").float() * V(".qty").int()))
        
        # With a RawJS callback fired on each re-evaluation
        Text(text=useVRef(
            V(".score").int(),
            callbacks=RawJS("console.log('score updated');")
        ))
        
        # With a dScript callback (single, no list needed)
        Text(text=useVRef(
            V(".total").float(),
            callbacks=log("total changed")
        ))
        
        # With multiple callbacks
        Text(text=useVRef(
            V(".total").float(),
            callbacks=[log("total changed"), RawJS("console.log('synced');")]
        ))
        
        # Direct value (static, no reactivity)
        Text(text=useVRef(42))
        
        # Boolean expression — auto-detects #age as dependency
        Text(text=useVRef(
            (V("#age").int() >= 18).then("Adult", "Minor")
        ))
        ```
    """
    return VRefBinding(vexpr, dependencies, callbacks)
