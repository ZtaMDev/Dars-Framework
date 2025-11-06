from typing import Any, Dict, List, Optional
from dars.scripts.script import InlineScript

# Global registry collected at authoring time (Python)
STATE_BOOTSTRAP: List[Dict[str, Any]] = []

class DarsState:
    def __init__(self, name: str, id: Optional[str], states: Optional[List[Any]], is_custom: bool = False):
        self.name = name
        self.id = id
        self.states = states or []
        self.is_custom = is_custom

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "id": self.id,
            "states": self.states,
            "isCustom": self.is_custom,
        }

    def state(self, idx: int, cComp: bool = False, render: Optional[Any] = None) -> InlineScript:
        """
        Convenience: returns an InlineScript that, when added to a page/app,
        triggers a state change via the JS runtime. Intended for quick prototyping.

        - idx: target state index/value
        - cComp: if True, performs a full HTML replace (custom component flow)
        - render: HTML string to inject when cComp=True
        """
        target_id = self.id or ""

        def _escape_js_str(s: str) -> str:
            return s.replace("\\", "\\\\").replace("'", "\\'").replace("\n", "\\n").replace("\r", "")

        # Compute HTML if needed
        html_val = None
        if cComp and render is not None:
            try:
                # DeferredAttr -> clone component with attrs
                if hasattr(render, 'clone_with') and callable(getattr(render, 'clone_with')):
                    render = render.clone_with()
                # If it's a Component instance, render it to HTML
                try:
                    from dars.core.component import Component as _DarsComponent
                    if isinstance(render, _DarsComponent):
                        from dars.exporters.web.html_css_js import HTMLCSSJSExporter
                        _exp = HTMLCSSJSExporter()
                        html_val = _exp.render_component(render)
                except Exception:
                    html_val = None
                if html_val is None and isinstance(render, str):
                    html_val = render
            except Exception:
                html_val = None

        payload_parts = [f"id: '{_escape_js_str(target_id)}'", f"state: {idx}"]
        if cComp:
            html_str = _escape_js_str(html_val or "")
            payload_parts.append("useCustomRender: true")
            payload_parts.append(f"html: '{html_str}'")
        payload = ", ".join(payload_parts)

        code = (
            "(async () => {\n"
            "  try {\n"
            "    let ch = window.__DARS_CHANGE_FN;\n"
            "    if (!ch) {\n"
            "      if (window.Dars && typeof window.Dars.change === 'function') {\n"
            "        ch = window.Dars.change.bind(window.Dars);\n"
            "      } else {\n"
            "        const m = await import('./lib/dars.min.js');\n"
            "        ch = (m.change || (m.default && m.default.change));\n"
            "      }\n"
            "      if (typeof ch === 'function') window.__DARS_CHANGE_FN = ch;\n"
            "    }\n"
            f"    if (typeof ch === 'function') ch({{{payload}}});\n"
            "  } catch (e) { /* noop */ }\n"
            "})();\n"
        )
        return InlineScript(code, module=True)


def dState(name: str, component: Any = None, id: Optional[str] = None, states: Optional[List[Any]] = None, is_custom: bool = False) -> DarsState:
    """
    Declare a state associated with a component or an element id.
    - name: state name (unique enough per app).
    - component: a Dars component instance; if provided and has .id, it is used.
    - id: explicit target id when component is not provided.
    - states: optional list of possible state values (metadata).
    - is_custom: mark as custom component to indicate full HTML replace flows.

    Returns a DarsState object (for ergonomics), and records the state
    in a global bootstrap list consumed by the exporter.
    """
    target_id = None
    try:
        if component is not None and hasattr(component, 'id'):
            target_id = getattr(component, 'id')
    except Exception:
        target_id = None
    if not target_id:
        target_id = id

    st = DarsState(name=name, id=target_id, states=states, is_custom=is_custom)
    try:
        STATE_BOOTSTRAP.append(st.to_dict())
    except Exception:
        pass
    return st
