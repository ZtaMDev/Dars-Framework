# Dars Framework - Core Source File
#
# This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0.
# If a copy of the MPL was not distributed with this file, You can obtain one at
# https://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2025 ZtaDev
"""
If — conditional rendering component.

Compile-time ``bool`` conditions prune the tree at export time.
Runtime VRef / DAP-expression conditions emit a browser-side visibility toggle.
"""

import json
from typing import Any, Callable, Optional, Union

from dars.core.component import Component


class If_Component(Component):
    """
    Conditionally render one of two subtrees.

    When *condition* is a plain Python ``bool`` it is evaluated at compile
    time and only the matching branch is included in the exported HTML.

    When *condition* is a VRef expression or DAP-compatible structure the
    exporter emits both branches wrapped in a ``<div data-dap-if="…">``
    element; the browser runtime evaluates the condition and toggles
    visibility without a page reload.

    Args:
        condition: ``bool``, VRef expression, or DAP-compatible dict/object.
        then: Component (or zero-argument callable returning one) shown when
              the condition is truthy.
        else_: Optional component (or callable) shown when falsy.
        id: HTML ``id`` attribute for the wrapper element.
        class_name: CSS class names for the wrapper element.
        style: Inline style dict for the wrapper element.

    Example::

        If(condition=user.is_logged_in,
           then=Dashboard(),
           else_=LoginPage())

        # Runtime VRef condition
        If(condition=V(".is-admin"),
           then=AdminPanel())
    """

    def __init__(
        self,
        condition: Any,
        then: Union[Component, Callable[[], Component]],
        else_: Optional[Union[Component, Callable[[], Component]]] = None,
        id: Any = None,
        class_name: Any = None,
        style: Optional[dict | str] = None,
        **props,
    ) -> None:
        super().__init__(id=id, class_name=class_name, style=style, **props)
        self._condition = condition
        self._then = then() if callable(then) and not isinstance(then, Component) else then
        self._else = else_() if callable(else_) and not isinstance(else_, Component) else else_

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _is_runtime_condition(condition: Any) -> bool:
        """Return True when the condition must be evaluated at runtime."""
        if isinstance(condition, bool):
            return False
        # VRefValue (from setVRef) — has a selector, runtime-driven
        if hasattr(condition, 'selector') and hasattr(condition, 'generate_registry_js'):
            return True
        # VRef / DAP expression objects expose _to_structure or op
        if hasattr(condition, '_to_structure') or hasattr(condition, 'op'):
            return True
        if isinstance(condition, dict) and 'op' in condition:
            return True
        return False

    @staticmethod
    def _condition_to_json(condition: Any) -> str:
        """Serialise a runtime condition to a JSON string for data-dap-if."""
        # VRefValue — emit a vref_get DAP op
        if hasattr(condition, 'selector') and hasattr(condition, 'generate_registry_js'):
            import json
            return json.dumps({"op": "vref_get", "args": {"selector": condition.selector}})
        if hasattr(condition, '_to_structure'):
            import json
            return json.dumps(condition._to_structure())
        if isinstance(condition, dict):
            import json
            return json.dumps(condition)
        import json
        return json.dumps(str(condition))

    # ------------------------------------------------------------------
    # Render
    # ------------------------------------------------------------------

    def render(self, exporter: Any) -> str:
        comp_id = exporter.get_component_id(self, prefix="if")
        class_attr = f'class="{self.class_name or ""}"'
        style_attr = (
            f'style="{exporter.render_styles(self.style)}"' if self.style else ""
        )

        if not self._is_runtime_condition(self._condition):
            # ── Compile-time branch ──────────────────────────────────────
            if self._condition:
                inner = exporter.render_component(self._then) if self._then else ""
            else:
                inner = exporter.render_component(self._else) if self._else else ""
            return f'<div id="{comp_id}" {class_attr} {style_attr}>{inner}</div>'

        # ── Runtime branch ───────────────────────────────────────────────
        condition_json = self._condition_to_json(self._condition)
        # Escape double quotes for safe embedding in an HTML attribute value
        condition_attr = condition_json.replace('"', '&quot;')
        then_id = f"{comp_id}-then"
        else_id = f"{comp_id}-else"

        then_html = exporter.render_component(self._then) if self._then else ""
        else_html = exporter.render_component(self._else) if self._else else ""

        # Determine initial visibility from VRefValue.value
        initial_then_hidden = False
        initial_else_hidden = True
        if hasattr(self._condition, 'value'):
            cond_val = bool(self._condition.value)
            initial_then_hidden = not cond_val
            initial_else_hidden = cond_val

        then_style = ' style="display:none"' if initial_then_hidden else ""
        else_style = ' style="display:none"' if initial_else_hidden else ""

        return (
            f'<div id="{comp_id}" {class_attr} {style_attr}'
            f' data-dap-if="{condition_attr}"'
            f' data-if-then="{then_id}" data-if-else="{else_id}">'
            f'<div id="{then_id}" data-if-branch="then"{then_style}>{then_html}</div>'
            f'<div id="{else_id}" data-if-branch="else"{else_style}>{else_html}</div>'
            f'</div>'
        )
