# Dars Framework - Core Source File
#
# This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0.
# If a copy of the MPL was not distributed with this file, You can obtain one at
# https://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2025 ZtaDev
from typing import Any, Dict, List, Optional
from dars.scripts.dscript import dScript, RawJS
from dars.core.utilities import parse_utility_string
import json
import warnings

# Global registry collected at authoring time (Python)
STATE_BOOTSTRAP: List[Dict[str, Any]] = []

# Global registry for compile-time validation: {component_id: (state_name, states_list)}
_COMPONENT_TO_STATE_MAP: Dict[str, tuple] = {}

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

    # state.py - Modificar el método state de DarsState
    def state(self, idx: Optional[int] = None, cComp: bool = False, render: Optional[Any] = None, goto: Optional[Any] = None, **kwargs) -> dScript:
        """
        Convenience: returns an InlineScript that, when added to a page/app,
        triggers a state change via the JS runtime. Intended for quick prototyping.

        - idx: target state index/value
        - cComp: if True, performs a full HTML replace (custom component flow)
        - render: HTML string to inject when cComp=True
        - kwargs: dynamic state updates (text, style, etc.)
        """
        target_id = self.id or ""

        def _escape_js_str(s: str) -> str:
            # Escapar para JavaScript, incluyendo saltos de línea
            return s.replace("\\", "\\\\").replace("'", "\\'").replace("\n", "\\n").replace("\r", "\\r")

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
            
        # Dynamic updates
        if kwargs:
            parts.append("dynamic: true")
            for k, v in kwargs.items():
                if isinstance(v, RawJS):
                    parts.append(f"{k}: {v.code}")
                elif k == 'style':
                    val = v
                    if isinstance(val, str):
                        val = parse_utility_string(val)
                    if isinstance(val, dict):
                        parts.append(f"style: {json.dumps(val)}")
                elif k == 'attrs' and isinstance(v, dict):
                    parts.append(f"attrs: {json.dumps(v)}")
                elif k == 'classes' and isinstance(v, dict):
                    parts.append(f"classes: {json.dumps(v)}")
                else:
                    parts.append(f"{k}: {json.dumps(v)}")

        payload = ", ".join(parts)

        # Generar código JavaScript en una sola línea para compatibilidad con el nuevo sistema de eventos
        code = (
            "(async () => {"
            "  try {"
            "    let ch = window.__DARS_CHANGE_FN;"
            "    if (!ch) {"
            "      if (window.Dars && typeof window.Dars.change === 'function') {"
            "        ch = window.Dars.change.bind(window.Dars);"
            "      } else {"
            "        const m = await import('/lib/dars.min.js');"
            "        ch = (m.change || (m.default && m.default.change));"
            "      }"
            "      if (typeof ch === 'function') window.__DARS_CHANGE_FN = ch;"
            "    }"
            f"    if (typeof ch === 'function') ch({{{payload}}});"
            "  } catch (e) { console.error('[Dars] State error:', e); }"
            "})();"
        )
        
        # Minificar el código removiendo espacios extra (pero manteniendo la estructura básica)
        code = ' '.join(code.split())
        return dScript(code)  # Changed to dScript for .then() chaining support

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
        if 'style' in attrs and isinstance(attrs['style'], str):
            attrs['style'] = parse_utility_string(attrs['style'])
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
        
        # Register in compile-time validation map
        if target_id:
            _COMPONENT_TO_STATE_MAP[target_id] = (name, states or [])
    except Exception:
        pass
    return st


class ThisProxy:
    """
    Helper class to generate dynamic state changes for 'this' component.
    """
    def state(self, **kwargs) -> dScript:
        """
        Generate JS to update 'this' component's state dynamically.
        """
        parts = ["dynamic: true", "id: (this && this.id) ? this.id : (event && event.target && event.target.id) ? event.target.id : null"]
        
        for k, v in kwargs.items():
            if isinstance(v, RawJS):
                parts.append(f"{k}: {v.code}")
            elif k == 'style':
                val = v
                if isinstance(val, str):
                    val = parse_utility_string(val)
                if isinstance(val, dict):
                    parts.append(f"style: {json.dumps(val)}")
            elif k == 'attrs' and isinstance(v, dict):
                parts.append(f"attrs: {json.dumps(v)}")
            elif k == 'classes' and isinstance(v, dict):
                parts.append(f"classes: {json.dumps(v)}")
            else:
                parts.append(f"{k}: {json.dumps(v)}")
                
        payload = ", ".join(parts)
        
        code = (
            "(async () => {"
            "  try {"
            "    let ch = window.__DARS_CHANGE_FN;"
            "    if (!ch) {"
            "      if (window.Dars && typeof window.Dars.change === 'function') {"
            "        ch = window.Dars.change.bind(window.Dars);"
            "      } else {"
            "        const m = await import('/lib/dars.min.js');"
            "        ch = (m.change || (m.default && m.default.change));"
            "      }"
            "      if (typeof ch === 'function') window.__DARS_CHANGE_FN = ch;"
            "    }"
            f"    if (typeof ch === 'function') ch({{{payload}}});"
            "  } catch (e) { console.error('[Dars] State error:', e); }"
            "})();"
        )
        return dScript(' '.join(code.split()))  # Changed to dScript for .then() chaining support

    def goto(self, idx: int, _component_id: Optional[str] = None) -> dScript:
        """
        Navigate to a specific state index for this component.
        Requires a dState to be defined for the component.
        
        Args:
            idx: The state index to navigate to (must exist in the component's dState)
            _component_id: Internal - component ID for compile-time validation
            
        Raises:
            ValueError: At compile-time if validation fails
            JavaScript Error: At runtime if no dState is registered for the component
            JavaScript Error: At runtime if the index is out of bounds
        
        Note: Compile-time validation is advisory only. Full validation happens at runtime.
        """
        # Check if component ID was set via this_for() or passed directly
        cid = _component_id or getattr(self, '_cid', None)
        
        # Compile-time validation (when component ID is known)
        if cid and cid in _COMPONENT_TO_STATE_MAP:
            state_name, states_list = _COMPONENT_TO_STATE_MAP[cid]
            # Validate index is within bounds
            if not isinstance(states_list, list) or len(states_list) == 0:
                raise ValueError(
                    f"[Dars Compile Error] Component '{cid}' has dState '{state_name}' "
                    f"but no states list defined. Define states parameter in dState()."
                )
            if idx < 0 or idx >= len(states_list):
                raise ValueError(
                    f"[Dars Compile Error] this().goto({idx}) - Index {idx} out of bounds for component '{cid}'. "
                    f"State '{state_name}' has {len(states_list)} states (valid indices: 0-{len(states_list)-1})."
                )
        elif cid and cid not in _COMPONENT_TO_STATE_MAP:
            # Component ID is known but no dState registered
            raise ValueError(
                f"[Dars Compile Error] this().goto({idx}) used on component '{cid}' "
                f"but no dState is defined for this component. "
                f"You must create a dState for this component before using goto().\n"
                f"Example: my_state = dState('state_name', component=your_component, states=[0, 1, 2])"
            )
        
        # Generate JavaScript code (runtime validation)
        code = (
            "(async () => {"
            "  try {"
            "    const compId = (this && this.id) ? this.id : "
            "                    (event && event.target && event.target.id) ? event.target.id : null;"
            "    if (!compId) throw new Error('[Dars.goto] Cannot resolve component ID');"
            "    "
            "    let ch = window.__DARS_CHANGE_FN;"
            "    if (!ch) {"
            "      if (window.Dars && typeof window.Dars.change === 'function') {"
            "        ch = window.Dars.change.bind(window.Dars);"
            "      } else {"
            "        const m = await import('/lib/dars.min.js');"
            "        ch = (m.change || (m.default && m.default.change));"
            "      }"
            "      if (typeof ch === 'function') window.__DARS_CHANGE_FN = ch;"
            "    }"
            "    "
            "    const registry = (window.Dars && window.Dars._stateRegistry) || {};"
            "    let stateName = null;"
            "    for (const [name, stateObj] of Object.entries(registry)) {"
            "      if (stateObj.id === compId) {"
            "        stateName = name;"
            "        break;"
            "      }"
            "    }"
            "    "
            "    if (!stateName) {"
            "      throw new Error(`[Dars.goto] No dState found for component ${compId}. Define a dState for this component first.`);"
            "    }"
            "    "
            "    const stateObj = registry[stateName];"
            f"    const targetIdx = {idx};"
            "    "
            "    if (!stateObj.states || !Array.isArray(stateObj.states)) {"
            "      throw new Error(`[Dars.goto] State '${stateName}' has no states array`);"
            "    }"
            "    if (targetIdx < 0 || targetIdx >= stateObj.states.length) {"
            "      throw new Error(`[Dars.goto] Index " + str(idx) + " out of bounds for state '${stateName}' (valid: 0-${stateObj.states.length - 1})`);"
            "    }"
            "    "
            "    if (typeof ch === 'function') {"
            f"      ch({{id: compId, name: stateName, state: {idx}}});"
            "    }"
            "  } catch (e) {"
            "    console.error('[Dars.goto]', e);"
            "    throw e;"
            "  }"
            "})();"
        )
        return dScript(' '.join(code.split()), module=True)  # Changed to dScript for .then() chaining support

def this() -> ThisProxy:
    """
    Returns a proxy object that refers to the current component in an event handler.
    Usage: this().state(text="New Text")
    Note: For compile-time validation with goto(), prefer using direct assignment like:
    component.on_click = this().goto(idx) after defining dState for that component
    """
    return ThisProxy()

def this_for(component_id: str) -> ThisProxy:
    """
    Returns a ThisProxy bound to a specific component ID for compile-time validation.
    
    This is primarily used internally by the framework when components assign event handlers.
    For manual use, prefer direct assignment after dState definition.
    
    Args:
        component_id: The ID of the component this refers to
        
    Returns:
        ThisProxy instance that will validate goto() calls at compile-time
    """
    proxy = ThisProxy()
    # Store the component ID for validation in goto()
    proxy._cid = component_id  # type: ignore
    return proxy
