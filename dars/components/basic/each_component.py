# Dars Framework - Core Source File
#
# This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0.
# If a copy of the MPL was not distributed with this file, You can obtain one at
# https://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2025 ZtaDev
"""
Each — list rendering component.

Compile-time Python lists are unrolled at export time.
Runtime VRef selectors pointing to a JSON array emit a
``data-dap-each`` attribute and the browser runtime re-renders the list
when the VRef value changes.
"""

import json
from typing import Any, Callable, Optional, Union

from dars.core.component import Component


# Sentinel item used to generate a VDOM template from the render function.
# Fields are placeholder strings that dom_each_render substitutes at runtime.
# Boolean fields use False so conditional Python logic in the render fn
# produces the "default" (not-done) template; the runtime handles done state
# via the __item_done__ placeholder in CSS class names.
_TEMPLATE_SENTINEL = {
    "__dars_each_item__": True,
    "id": "__item_id__",
    "title": "__item_title__",
    "done": False,          # False so render fns produce the default style
    "value": "__item_value__",
    "label": "__item_label__",
    "name": "__item_name__",
    "text": "__item_text__",
}


class Each_Component(Component):
    """
    Render a list of items using a template function.

    When *items* is a plain Python ``list`` the exporter calls
    ``render(item)`` for every element and concatenates the resulting HTML.
    An empty list produces an empty wrapper element without raising.

    When *items* is a VRef expression (pointing to a JSON array) the
    exporter emits ``data-dap-each`` and ``data-each-template`` attributes;
    the browser runtime re-renders the container whenever the VRef changes.
    The render function is called with a sentinel dict to produce a VDOM
    template that the runtime uses to render each item.

    Args:
        items: Python ``list`` or VRef expression pointing to a JSON array.
        render: Callable ``(item) -> Component`` used to render each element.
        item_key: Optional key field name in each item dict (default ``"id"``).
        id: HTML ``id`` attribute.
        class_name: CSS class names.
        style: Inline style dict.

    Example::

        Each(items=users, render=lambda u: Text(u["name"]))

        # Runtime VRef list (API response stored in VRef)
        Each(items=tasks_vref, render=lambda t: Text(t["title"]))
    """

    def __init__(
        self,
        items: Union[list, Any],
        render: Callable[[Any], Component],
        item_key: str = "id",
        id: Optional[str] = None,
        class_name: Optional[str] = None,
        style: Optional[dict] = None,
        **props,
    ) -> None:
        super().__init__(id=id, class_name=class_name, style=style, **props)
        self._items = items
        self._render_fn = render
        self._item_key = item_key

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _is_runtime_items(items: Any) -> bool:
        """Return True when items must be resolved at runtime."""
        if isinstance(items, list):
            return False
        # VRefValue from setVRef — has selector + generate_registry_js
        if hasattr(items, 'selector') and hasattr(items, 'generate_registry_js'):
            return True
        if hasattr(items, '_to_structure') or hasattr(items, 'op'):
            return True
        if isinstance(items, dict) and 'op' in items:
            return True
        return False

    @staticmethod
    def _items_selector(items: Any) -> str:
        """Extract the CSS selector string from a VRef expression."""
        # VRefBinding / VRefValue expose a .selector attribute
        if hasattr(items, 'selector'):
            return items.selector
        if hasattr(items, '_to_structure'):
            struct = items._to_structure()
            return json.dumps(struct)
        if isinstance(items, dict):
            return json.dumps(items)
        return str(items)

    def _build_template_html(self, exporter: Any) -> str:
        """
        Call the render function with a sentinel to produce a template HTML string.
        Placeholder tokens like ``__item_title__`` are replaced by the runtime
        with actual item field values.
        """
        try:
            component = self._render_fn(_TEMPLATE_SENTINEL)
            if isinstance(component, Component):
                return exporter.render_component(component)
        except Exception:
            pass
        return '<span>__item_value__</span>'

    # ------------------------------------------------------------------
    # Render
    # ------------------------------------------------------------------

    def render(self, exporter: Any) -> str:
        comp_id = exporter.get_component_id(self, prefix="each")
        class_attr = f'class="{self.class_name or ""}"'
        style_attr = (
            f'style="{exporter.render_styles(self.style)}"' if self.style else ""
        )

        if not self._is_runtime_items(self._items):
            # ── Compile-time list ─────────────────────────────────────────
            children_html = ""
            for item in self._items:
                component = self._render_fn(item)
                if isinstance(component, Component):
                    children_html += exporter.render_component(component)
            return (
                f'<div id="{comp_id}" {class_attr} {style_attr}>'
                f'{children_html}</div>'
            )

        # ── Runtime VRef list ─────────────────────────────────────────────
        selector = self._items_selector(self._items)
        # Build a template HTML string with sentinel placeholders
        template_html = self._build_template_html(exporter)
        # Escape for embedding in a data attribute
        template_escaped = template_html.replace('&', '&amp;').replace('"', '&quot;').replace("'", '&#39;')

        return (
            f'<div id="{comp_id}" {class_attr} {style_attr}'
            f' data-dap-each="{selector}"'
            f' data-each-key="{self._item_key}"'
            f' data-each-template="{template_escaped}">'
            f'</div>'
        )
