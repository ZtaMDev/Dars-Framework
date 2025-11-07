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
        self.rules: Dict[str, Dict[str, Any]] = {}
        self._bootstrap_ref: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        d = {
            "name": self.name,
            "id": self.id,
            "states": self.states,
            "isCustom": self.is_custom,
        }
        try:
            d["defaultIndex"] = 0
            d["defaultValue"] = (self.states[0] if isinstance(self.states, list) and len(self.states) > 0 else None)
        except Exception:
            d["defaultIndex"] = 0
            d["defaultValue"] = None
        if self.rules:
            d["rules"] = self.rules
        return d

    def state(self, idx: Optional[int] = None, cComp: bool = False, render: Optional[Any] = None, goto: Optional[Any] = None) -> InlineScript:
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

        # Build payload
        parts = [f"id: '{_escape_js_str(target_id)}'", f"name: '{_escape_js_str(self.name)}'"]
        if idx is not None:
            parts.append(f"state: {idx}")
        if goto is not None:
            if isinstance(goto, str):
                parts.append(f"goto: '{_escape_js_str(goto)}'")
            else:
                parts.append(f"goto: {goto}")
        if cComp:
            html_str = _escape_js_str(html_val or "")
            parts.append("useCustomRender: true")
            parts.append(f"html: '{html_str}'")
        payload = ", ".join(parts)

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

    # --- cState: define rules/mods for a given state index ---
    def cState(self, idx: int, mods: Optional[List[Dict[str, Any]]] = None) -> 'CStateRuleBuilder':
        key = str(idx)
        if idx == 0:
            raise ValueError(
                "Default state (index 0) is immutable. Do not define cState(0). "
                "Configure the component's default directly on the instance instead."
            )
        if key not in self.rules:
            self.rules[key] = {}
        if mods:
            existing = list(self.rules[key].get('mods', []))
            existing.extend(mods)
            self.rules[key]['mods'] = existing
            # mirror into bootstrap ref if exists
            if self._bootstrap_ref is not None:
                self._bootstrap_ref.setdefault('rules', {})
                self._bootstrap_ref['rules'][key] = self.rules[key]
        return CStateRuleBuilder(self, key)

    # sugar: direct goto builder for rules
    def goto(self, value: Any) -> 'CStateRuleBuilder':
        # attach as default rule for current state if exists, else for state 0
        key = str(0)
        if key not in self.rules:
            self.rules[key] = {}
        self.rules[key]['goto'] = value
        if self._bootstrap_ref is not None:
            self._bootstrap_ref.setdefault('rules', {})
            self._bootstrap_ref['rules'][key] = self.rules[key]
        return CStateRuleBuilder(self, key)


class Mod:
    @staticmethod
    def inc(target: Any, prop: str = 'text', by: int = 1) -> Dict[str, Any]:
        tid = getattr(target, 'id', None) or str(target)
        return {"op": "inc", "target": tid, "prop": prop, "by": by}

    @staticmethod
    def dec(target: Any, prop: str = 'text', by: int = 1) -> Dict[str, Any]:
        return Mod.inc(target, prop=prop, by=(-abs(by)))

    @staticmethod
    def set(target: Any, **attrs) -> Dict[str, Any]:
        tid = getattr(target, 'id', None) or str(target)
        return {"op": "set", "target": tid, "attrs": attrs}

    @staticmethod
    def toggle_class(target: Any, name: str, on: Optional[bool] = None) -> Dict[str, Any]:
        tid = getattr(target, 'id', None) or str(target)
        d: Dict[str, Any] = {"op": "toggleClass", "target": tid, "name": name}
        if on is not None:
            d['on'] = bool(on)
        return d

    @staticmethod
    def append_text(target: Any, value: str) -> Dict[str, Any]:
        tid = getattr(target, 'id', None) or str(target)
        return {"op": "appendText", "target": tid, "value": value}

    @staticmethod
    def prepend_text(target: Any, value: str) -> Dict[str, Any]:
        tid = getattr(target, 'id', None) or str(target)
        return {"op": "prependText", "target": tid, "value": value}

    @staticmethod
    def call(target: Any, state: Any = None, goto: Any = None) -> Dict[str, Any]:
        """Invoke another dState's state change.
        - target: DarsState instance or state name string; if a component is passed, use its id.
        - state: target state index/value.
        - goto: relative/absolute goto directive (e.g., '+1').
        The runtime will resolve the state by name first (registry), falling back to id.
        """
        name: Optional[str] = None
        sid: Optional[str] = None
        try:
            # DarsState instance
            if hasattr(target, 'name') and hasattr(target, 'id'):
                name = getattr(target, 'name', None)
                sid = getattr(target, 'id', None)
            elif isinstance(target, str):
                name = target
            else:
                # Maybe a component; try id
                sid = getattr(target, 'id', None) or str(target)
        except Exception:
            name = None
            sid = None
        d: Dict[str, Any] = {"op": "call"}
        if name:
            d['name'] = name
        if sid:
            d['id'] = sid
        if state is not None:
            d['state'] = state
        if goto is not None:
            d['goto'] = goto
        return d


class CStateRuleBuilder:
    def __init__(self, st: DarsState, key: str):
        self.st = st
        self.key = key

    def _ensure(self):
        if self.key not in self.st.rules:
            self.st.rules[self.key] = {}
        if 'mods' not in self.st.rules[self.key]:
            self.st.rules[self.key]['mods'] = []

    def inc(self, target: Any, prop: str = 'text', by: int = 1) -> 'CStateRuleBuilder':
        self._ensure()
        self.st.rules[self.key]['mods'].append(Mod.inc(target, prop, by))
        if self.st._bootstrap_ref is not None:
            self.st._bootstrap_ref.setdefault('rules', {})
            self.st._bootstrap_ref['rules'][self.key] = self.st.rules[self.key]
        return self

    def dec(self, target: Any, prop: str = 'text', by: int = 1) -> 'CStateRuleBuilder':
        self._ensure()
        self.st.rules[self.key]['mods'].append(Mod.dec(target, prop, by))
        if self.st._bootstrap_ref is not None:
            self.st._bootstrap_ref.setdefault('rules', {})
            self.st._bootstrap_ref['rules'][self.key] = self.st.rules[self.key]
        return self

    def set(self, target: Any, **attrs) -> 'CStateRuleBuilder':
        self._ensure()
        self.st.rules[self.key]['mods'].append(Mod.set(target, **attrs))
        if self.st._bootstrap_ref is not None:
            self.st._bootstrap_ref.setdefault('rules', {})
            self.st._bootstrap_ref['rules'][self.key] = self.st.rules[self.key]
        return self

    def toggle_class(self, target: Any, name: str, on: Optional[bool] = None) -> 'CStateRuleBuilder':
        self._ensure()
        self.st.rules[self.key]['mods'].append(Mod.toggle_class(target, name, on))
        if self.st._bootstrap_ref is not None:
            self.st._bootstrap_ref.setdefault('rules', {})
            self.st._bootstrap_ref['rules'][self.key] = self.st.rules[self.key]
        return self

    def append_text(self, target: Any, value: str) -> 'CStateRuleBuilder':
        self._ensure()
        self.st.rules[self.key]['mods'].append(Mod.append_text(target, value))
        if self.st._bootstrap_ref is not None:
            self.st._bootstrap_ref.setdefault('rules', {})
            self.st._bootstrap_ref['rules'][self.key] = self.st.rules[self.key]
        return self

    def prepend_text(self, target: Any, value: str) -> 'CStateRuleBuilder':
        self._ensure()
        self.st.rules[self.key]['mods'].append(Mod.prepend_text(target, value))
        if self.st._bootstrap_ref is not None:
            self.st._bootstrap_ref.setdefault('rules', {})
            self.st._bootstrap_ref['rules'][self.key] = self.st.rules[self.key]
        return self

    def call(self, target: Any, state: Any = None, goto: Any = None) -> 'CStateRuleBuilder':
        """Append a cross-state call op to this rule."""
        self._ensure()
        self.st.rules[self.key]['mods'].append(Mod.call(target, state=state, goto=goto))
        if self.st._bootstrap_ref is not None:
            self.st._bootstrap_ref.setdefault('rules', {})
            self.st._bootstrap_ref['rules'][self.key] = self.st.rules[self.key]
        return self

    def goto(self, value: Any) -> 'CStateRuleBuilder':
        if self.key not in self.st.rules:
            self.st.rules[self.key] = {}
        self.st.rules[self.key]['goto'] = value
        if self.st._bootstrap_ref is not None:
            self.st._bootstrap_ref.setdefault('rules', {})
            self.st._bootstrap_ref['rules'][self.key] = self.st.rules[self.key]
        return self


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
        d = st.to_dict()
        STATE_BOOTSTRAP.append(d)
        st._bootstrap_ref = d
    except Exception:
        pass
    return st
