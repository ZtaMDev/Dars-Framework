from __future__ import annotations
from typing import Any, Union
import json

from dars.scripts.dscript import dScript

# VDOM builder to serialize Component -> vdom dict
try:
    from dars.exporters.web.vdom import VDomBuilder
    from dars.core.component import Component
except Exception:
    VDomBuilder = None  # type: ignore
    Component = object  # type: ignore


def deleteComp(id: str) -> dScript:
    """Return a dScript that deletes a component on the client by DOM id.
    Calls: Dars.runtime.deleteComponent(id)
    """
    code = f"Dars.runtime && Dars.runtime.deleteComponent && Dars.runtime.deleteComponent({json.dumps(id)});"
    return dScript(code=code)


def createComp(target: Union[Component, Any], root: Union[str, Component], position: str = "append") -> dScript:
    """Return a dScript that creates a new component on the client.
    Calls: Dars.runtime.createComponent(root_id, vdom_data, position)

    - target: Component instance (or callable returning one)
    - root: parent DOM id (or Component with .id)
    - position: "append" | "prepend" | "before:id" | "after:id"
    """
    # Normalize root id
    if isinstance(root, Component):  # type: ignore
        root_id = getattr(root, 'id', None)
    else:
        root_id = str(root)
    if not root_id:
        # Still return a no-op script to avoid crashes client-side
        return dScript(code="/* Dars.createComp: invalid root id */")

    # Normalize/create component VDOM
    comp = target
    try:
        if callable(target) and not isinstance(target, Component):  # type: ignore
            comp = target()
    except Exception:
        pass

    vdom_data: dict[str, Any] = {}
    events_map: dict[str, Any] = {}
    if VDomBuilder is not None and isinstance(comp, Component):  # type: ignore
        try:
            builder = VDomBuilder()
            vdom_data = builder.build(comp)  # type: ignore
            if getattr(builder, 'events_map', None):
                events_map = dict(builder.events_map)  # type: ignore
        except Exception:
            # Fallback: minimal payload
            vdom_data = {
                "type": getattr(comp, '__class__', type('X', (), {})).__name__,
                "id": getattr(comp, 'id', None),
                "props": getattr(comp, 'props', {}) or {},
                "children": [],
            }
    else:
        # Fallback for non-Component targets
        vdom_data = {
            "type": "Div",
            "id": None,
            "props": {"text": str(comp)},
            "children": [],
        }

    # Attach events map into vdom payload for runtime to hydrate
    if events_map:
        vdom_data["_events"] = events_map

    code = (
        "try{ (function(){\n"
        f"  const rootId = {json.dumps(root_id)};\n"
        f"  const vdom = {json.dumps(vdom_data)};\n"
        f"  const pos = {json.dumps(position)};\n"
        "  if (globalThis.Dars && Dars.runtime && typeof Dars.runtime.createComponent==='function') {\n"
        "    Dars.runtime.createComponent(rootId, vdom, pos);\n"
        "  } else { console.warn('[Dars] runtime.createComponent not available'); }\n"
        "})(); }catch(e){ console.error(e); }"
    )
    return dScript(code=code)
