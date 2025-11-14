"""
VDOM utilities for Dars HTML exporter.

This module defines a minimal, modular Virtual DOM representation and a builder
that converts Dars Components (built-in or user-defined) to a serializable
VNode tree. It is intentionally patch-agnostic; it only focuses on building
an accurate snapshot that future patch systems can consume.
"""
from __future__ import annotations

from typing import Any, Callable, Dict, List, Optional

# We only use loose imports to avoid heavy coupling
try:
    from dars.core.component import Component
except Exception:  # pragma: no cover - defensive import
    Component = Any  # type: ignore


class VNode:
    def __init__(
        self,
        type_name: str,
        id: Optional[str],
        key: Optional[str],
        class_name: Optional[str],
        style: Dict[str, Any],
        hover_style: Dict[str, Any],
        active_style: Dict[str, Any],
        props: Dict[str, Any],
        children: Optional[List["VNode"]] = None,
        text: Optional[str] = None,
        is_island: bool = False,
    ) -> None:
        self.type = type_name
        self.id = id
        self.key = key
        self.class_name = class_name
        self.style = style or {}
        self.hover_style = hover_style or {}
        self.active_style = active_style or {} 
        self.props = props or {}
        self.children = children or []
        self.text = text
        self.isIsland = is_island

    def to_dict(self) -> Dict[str, Any]:
        d: Dict[str, Any] = {
            "type": self.type,
            "id": self.id,
            "key": self.key,
            "class": self.class_name,
            "style": self.style or {},
            "hover_style": self.hover_style or {},
            "active_style": self.active_style or {},
            "props": self.props or {},
            "children": [c.to_dict() for c in (self.children or [])],
        }
        if self.text is not None:
            d["text"] = self.text
        d["isIsland"] = bool(self.isIsland)
        return d


class VDomBuilder:
    """Builds a VNode tree from a Dars Component tree.

    Notes:
    - Works with built-in and user-defined components alike.
    - For user components that render HTML via `render(exporter)`, we still
      build a structural node capturing props/events. The future patch system
      may treat these as opaque islands unless more granular hooks are added.
    """

    def __init__(self, id_provider: Optional[Callable[[Component, str], str]] = None) -> None: # type: ignore
        self.id_provider = id_provider
        # Nuevo: recolector de eventos por página
        self.events_map: Dict[str, Dict[str, Any]] = {}

    def build(self, component: Component) -> Dict[str, Any]: # type: ignore
        vnode = self._build_vnode(component, path=["0"])  # raíz con path estable
        return vnode.to_dict()

    # --- internals ---
    def _safe_props(self, component: Component) -> Dict[str, Any]: # type: ignore
        """Extract props + public attributes into a single serializable mapping.

        Rules:
        - Start with component.props (if present), but filter out framework-managed fields
          like id, class_name, style, children, events to avoid duplication.
        - Augment with other public attributes from the component instance (e.g.,
          Markdown.dark_theme, Markdown.file_path, CustomComponent.title), skipping
          callables, private names (prefixed with '_'), Component instances and lists of Components.
        - Only include values that are JSON-serializable; otherwise, stringify as fallback.
        """
        import json

        result: Dict[str, Any] = {}
        EXCLUDE_KEYS = {
            'id', 'class_name', 'style', 'children', 'events', 'scripts', 'key',
            'props',  # avoid nesting component.props inside props
            'rendered_html','active_style', 'hover_style'  # avoid transporting heavy derived HTML payloads
        }

        # 1) Base props from component.props
        try:
            base_props = getattr(component, 'props', {}) or {}
            for k, v in base_props.items():
                if k in EXCLUDE_KEYS:
                    continue
                if callable(v):
                    continue
                try:
                    json.dumps(v)
                    result[k] = v
                except Exception:
                    result[k] = str(v)
        except Exception:
            pass

        # 2) Additional public attributes from the instance
        try:
            for k, v in vars(component).items():
                if k in EXCLUDE_KEYS:
                    continue
                if k in result:
                    continue
                if k.startswith('_'):
                    continue
                # Skip methods/callables
                if callable(v):
                    continue
                # Skip Component instances or lists/tuples of Components
                try:
                    if isinstance(v, Component):
                        continue
                    if isinstance(v, (list, tuple)) and any(isinstance(it, Component) for it in v):
                        continue
                except Exception:
                    pass

                try:
                    json.dumps(v)
                    result[k] = v
                except Exception:
                    result[k] = str(v)
        except Exception:
            pass

        return result

    def _serialize_events(self, component: Component) -> Optional[Dict[str, Any]]: # type: ignore
        events_payload: Dict[str, Any] = {}
        try:
            events = getattr(component, 'events', {}) or {}
            for ev_name, handlers in events.items():
                # Soporte para arrays de handlers
                handler_list = handlers if isinstance(handlers, (list, tuple)) else [handlers]
                
                serialized_handlers = []
                for handler in handler_list:
                    code = None
                    try:
                        # MEJORADO: Manejo más robusto de diferentes tipos de handlers
                        if hasattr(handler, 'get_code'):
                            code = handler.get_code()
                        elif isinstance(handler, dict):
                            code = handler.get('code') or handler.get('value')
                        elif isinstance(handler, str):
                            code = handler
                        else:
                            # fallback mejorado
                            code = str(handler) if handler else None
                    except Exception as e:
                        print(f"Warning: Error serializing event handler: {e}")
                        code = None
                    
                    # MEJORADO: Validar que el código no esté vacío
                    if code and (isinstance(code, str) and code.strip()):
                        serialized_handlers.append({
                            "type": "inline", 
                            "code": code.strip()
                        })
                
                if serialized_handlers:
                    events_payload[ev_name] = serialized_handlers
        except Exception as e:
            print(f"Warning: Error processing events: {e}")
        return events_payload or None

    def _text_value(self, component: Component) -> Optional[str]: # type: ignore
        # Try extracting a textual value if the component has a primary text prop
        try:
            for cand in ('text', 'content', 'value', 'label'):
                if hasattr(component, cand):
                    v = getattr(component, cand)
                    if isinstance(v, (str, int, float)):
                        return str(v)
        except Exception:
            pass
        return None

    def _build_vnode(self, component: Component, path: list) -> VNode: # type: ignore
        try:
            comp_type = component.__class__.__name__
        except Exception:
            comp_type = 'Component'

        # Prefer an injected id provider to keep IDs consistent with the HTML output
        comp_id = getattr(component, 'id', None)
        if self.id_provider is not None:
            try:
                # Choose a sensible prefix based on type name (lowercase)
                prefix = (component.__class__.__name__ or 'comp').lower()
                comp_id = self.id_provider(component, prefix=prefix)
            except Exception:
                # fallback to existing id attribute (may be None)
                comp_id = getattr(component, 'id', None)

        # Props
        safe_props = self._safe_props(component)

        # Events
        events_payload = self._serialize_events(component)
        
        comp_id = comp_id or stable_key  # usar stable_key como fallback
        if comp_id and events_payload:
            self.events_map[comp_id] = events_payload

        # Children
        children_nodes: List[VNode] = []
        try:
            for idx, child in enumerate(getattr(component, 'children', []) or []):
                if child is None:
                    continue
                child_path = path + [str(idx)]
                children_nodes.append(self._build_vnode(child, child_path))
        except Exception:
            children_nodes = []

        # Text (optional)
        text_value = self._text_value(component)

        # Heurística para saber si es componente "isla" (custom)
        is_island = False
        try:
            mod = getattr(component.__class__, '__module__', '') or ''
            # Si no pertenece al paquete de componentes built-in, lo tratamos como isla
            if not mod.startswith('dars.components.'):
                is_island = True
        except Exception:
            is_island = False

        # Clave estable: si no hay id ni key definidos, usamos el path del árbol
        stable_key = getattr(component, 'key', None)
        if not stable_key and not comp_id:
            stable_key = "/".join(path)

        vnode = VNode(
            type_name=comp_type,
            id=comp_id,
            key=stable_key,
            class_name=getattr(component, 'class_name', None),
            style=getattr(component, 'style', {}) or {},
            hover_style=getattr(component, 'hover_style', {}) or {},
            active_style=getattr(component, 'active_style', {}) or {},
            props=safe_props,
            children=children_nodes,
            text=text_value,
            is_island=is_island,
        )
        return vnode
