# Dars Framework - Core Source File
#
# This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0.
# If a copy of the MPL was not distributed with this file, You can obtain one at
# https://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2025 ZtaDev
"""
Show — visibility-toggle rendering component.

Unlike :class:`If_Component`, ``Show`` **always** renders its children into
the DOM.  A falsy condition simply hides the wrapper with ``display:none``.
"""

import json
from typing import Any, Optional

from dars.core.component import Component


class Show_Component(Component):
    """
    Render children but toggle their visibility based on *condition*.

    The children are always present in the DOM.  When *condition* is a
    compile-time ``False`` the wrapper receives ``style="display:none"``.
    When *condition* is a runtime VRef expression the exporter emits a
    ``data-dap-show`` attribute and the browser runtime calls
    ``dom_show`` / ``dom_hide`` accordingly.

    The **initial** display state is derived from the VRefValue's ``.value``
    so the element is correctly hidden/shown before JavaScript runs.

    Args:
        condition: ``bool``, VRef expression, or DAP-compatible structure.
        *children: Child components to render inside the wrapper.
        id: HTML ``id`` attribute.
        class_name: CSS class names.
        style: Inline style dict.
    """

    def __init__(
        self,
        condition: Any,
        *children: Component,
        id: Optional[str] = None,
        class_name: Optional[str] = None,
        style: Optional[dict] = None,
        **props,
    ) -> None:
        super().__init__(id=id, class_name=class_name, style=style, **props)
        self._condition = condition
        for child in children:
            self.add_child(child)

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _is_runtime_condition(condition: Any) -> bool:
        if isinstance(condition, bool):
            return False
        # VRefValue (from setVRef) — runtime-driven
        if hasattr(condition, 'selector') and hasattr(condition, 'generate_registry_js'):
            return True
        if hasattr(condition, '_to_structure') or hasattr(condition, 'op'):
            return True
        if isinstance(condition, dict) and 'op' in condition:
            return True
        return False

    @staticmethod
    def _condition_to_json(condition: Any) -> str:
        # VRefValue — emit a vref_get DAP op
        if hasattr(condition, 'selector') and hasattr(condition, 'generate_registry_js'):
            return json.dumps({"op": "vref_get", "args": {"selector": condition.selector}})
        if hasattr(condition, '_to_structure'):
            return json.dumps(condition._to_structure())
        if isinstance(condition, dict):
            return json.dumps(condition)
        return json.dumps(str(condition))

    # ------------------------------------------------------------------
    # Render
    # ------------------------------------------------------------------

    def render(self, exporter: Any) -> str:
        comp_id = exporter.get_component_id(self, prefix="show")
        class_attr = f'class="{self.class_name or ""}"'
        base_style = exporter.render_styles(self.style) if self.style else ""

        children_html = "".join(
            exporter.render_component(child) for child in self.children
        )

        if not self._is_runtime_condition(self._condition):
            # ── Compile-time bool ─────────────────────────────────────────
            hidden = not self._condition
            display = f"display:none; {base_style}" if hidden else base_style
            style_attr = f'style="{display}"' if display else ""
            return (
                f'<div id="{comp_id}" {class_attr} {style_attr}>'
                f'{children_html}</div>'
            )

        # ── Runtime VRef condition ────────────────────────────────────────
        # Use the VRefValue's initial value to set the correct initial display
        # so the element is hidden/shown correctly before JS runs.
        condition_json = self._condition_to_json(self._condition)
        # Escape double quotes for safe embedding in an HTML attribute value
        condition_attr = condition_json.replace('"', '&quot;')

        initial_hidden = False
        if hasattr(self._condition, 'value'):
            initial_hidden = not bool(self._condition.value)

        initial_display = f"display:none; {base_style}" if initial_hidden else base_style
        style_attr = f'style="{initial_display}"' if initial_display else ""

        return (
            f'<div id="{comp_id}" {class_attr} {style_attr}'
            f' data-dap-show="{condition_attr}">'
            f'{children_html}</div>'
        )
