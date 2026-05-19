# Dars Framework - Core Source File
#
# This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0.
# If a copy of the MPL was not distributed with this file, You can obtain one at
# https://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2025 ZtaDev
"""LEGACY USE STATEV2

import it with:

```python
from dars.core.state_v2.py import State
```
"""
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

    def state(self, idx: Optional[int] = None, cComp: bool = False, render: Optional[Any] = None, goto: Optional[Any] = None, **kwargs) -> RawJS:
        """
        Convenience: returns a dScript containing a DAP 'change' action.
        The client-side DAP dispatcher will handle the logic securely without eval().
        """
        target_id = self.id or ""

        # Construct basic action payload
        action_args = {
            "id": target_id,
            "name": self.name
        }

        if idx is not None:
            action_args["state"] = idx
            
        if goto is not None:
            action_args["goto"] = goto

        # Handle Custom Component Rendering (cComp)
        if cComp:
            action_args["useCustomRender"] = True
            html_val = None
            if render is not None:
                # Resolve deferred attributes first
                if hasattr(render, 'clone_with') and callable(getattr(render, 'clone_with')):
                    render = render.clone_with()
                    
                # Try to render fully if it's a Dars Component
                try:
                    from dars.core.component import Component as _DarsComponent
                    if isinstance(render, _DarsComponent):
                        from dars.exporters.web.html_css_js import HTMLCSSJSExporter
                        _exp = HTMLCSSJSExporter()
                        # NOTE: We create a temporary exporter instance. 
                        # Ideally this should reuse a shared context if possible, but for static generation it's fine.
                        html_val = _exp.render_component(render)
                except Exception:
                    html_val = None
                
                # Fallback if it's just a string or couldn't be rendered
                if html_val is None:
                    html_val = str(render)
            
            action_args["html"] = html_val or ""

        # Handle Dynamic Props (kwargs)
        if kwargs:
            action_args["dynamic"] = True
            for k, v in kwargs.items():
                if k == 'style':
                    val = v
                    if isinstance(val, str):
                        val = parse_utility_string(val)
                    action_args[k] = val
                elif k == 'attrs' and isinstance(v, dict):
                    action_args[k] = v
                elif k == 'classes' and isinstance(v, dict):
                    action_args[k] = v
                else:
                    action_args[k] = v

        # Return RawJS
        import json
        payload_js = json.dumps(action_args)
        return RawJS(code=f"if (window.Dars && typeof window.Dars.change === 'function') window.Dars.change({payload_js}); else if (typeof change === 'function') change({payload_js});")

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
        if prop == 'text':
            return {"$code": f"function() {{ var el = document.getElementById('{tid}'); if(el) el.textContent = String((parseFloat(el.textContent||'0')||0) + {by}); }}"}
        else:
            return {"$code": f"function() {{ var el = document.getElementById('{tid}'); if(el) el.setAttribute('{prop}', String((parseFloat(el.getAttribute('{prop}')||'0')||0) + {by})); }}"}

    @staticmethod
    def dec(target: Any, prop: str = 'text', by: int = 1) -> Dict[str, Any]:
        return Mod.inc(target, prop=prop, by=(-abs(by)))

    @staticmethod
    def set(target: Any, **attrs) -> Dict[str, Any]:
        tid = getattr(target, 'id', None) or str(target)
        import json
        lines = [f"function() {{ var _el = document.getElementById('{tid}');", "if(_el) {"]
        for k, v in attrs.items():
            if k == 'style':
                if isinstance(v, str): v = parse_utility_string(v)
                for sk, sv in v.items():
                    lines.append(f"  _el.style[{json.dumps(sk)}] = {json.dumps(sv)};")
            elif k == 'text':
                lines.append(f"  _el.textContent = {json.dumps(v)};")
            elif k == 'html':
                # No DOMPurify check needed for static generation if trusted or simple? Let's use simple assignment.
                lines.append(f"  _el.innerHTML = typeof _sanitize === 'function' ? _sanitize({json.dumps(v)}) : {json.dumps(v)};")
            elif k == 'value':
                lines.append(f"  _el.value = {json.dumps(v)};")
            elif k in ['checked', 'disabled', 'readonly', 'required', 'selected', 'autofocus', 'autoplay', 'controls', 'loop', 'muted']:
                # Boolean attributes
                if v is True or str(v).lower() == 'true':
                    lines.append(f"  _el.setAttribute('{k}', ''); if('{k}' in _el) _el['{k}'] = true;")
                else:
                    lines.append(f"  _el.removeAttribute('{k}'); if('{k}' in _el) _el['{k}'] = false;")
            else:
                lines.append(f"  _el.setAttribute({json.dumps(k)}, {json.dumps(v)});")
        lines.append("} }")
        return {"$code": " ".join(lines)}

    @staticmethod
    def toggle_class(target: Any, name: str, on: Optional[bool] = None) -> Dict[str, Any]:
        tid = getattr(target, 'id', None) or str(target)
        import json
        name_js = json.dumps(name)
        if on is None:
            return {"$code": f"function() {{ var el = document.getElementById('{tid}'); if(el) el.classList.toggle({name_js}); }}"}
        elif on is True:
            return {"$code": f"function() {{ var el = document.getElementById('{tid}'); if(el) el.classList.add({name_js}); }}"}
        else:
            return {"$code": f"function() {{ var el = document.getElementById('{tid}'); if(el) el.classList.remove({name_js}); }}"}

    @staticmethod
    def append_text(target: Any, value: str) -> Dict[str, Any]:
        tid = getattr(target, 'id', None) or str(target)
        import json
        return {"$code": f"function() {{ var el = document.getElementById('{tid}'); if(el) el.textContent = String(el.textContent||'') + {json.dumps(value)}; }}"}

    @staticmethod
    def prepend_text(target: Any, value: str) -> Dict[str, Any]:
        tid = getattr(target, 'id', None) or str(target)
        import json
        return {"$code": f"function() {{ var el = document.getElementById('{tid}'); if(el) el.textContent = {json.dumps(value)} + String(el.textContent||''); }}"}

    @staticmethod
    def call(target: Any, state: Any = None, goto: Any = None) -> Dict[str, Any]:
        """Invoke another dState's state change via the JS change() endpoint."""
        name: Optional[str] = None
        sid: Optional[str] = None
        try:
            if hasattr(target, 'name') and hasattr(target, 'id'):
                name = getattr(target, 'name', None)
                sid = getattr(target, 'id', None)
            elif isinstance(target, str):
                name = target
            else:
                sid = getattr(target, 'id', None) or str(target)
        except Exception:
            pass
        
        args = {}
        if name: args['name'] = name
        if sid: args['id'] = sid
        if state is not None: args['state'] = state
        if goto is not None: args['goto'] = goto
        
        import json
        payload_js = json.dumps(args)
        return {"$code": f"function() {{ if (window.Dars && typeof window.Dars.change === 'function') window.Dars.change({payload_js}); else if (typeof change === 'function') change({payload_js}); }}"}


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
    def state(self, **kwargs) -> RawJS:
        """
        Generate DAP action to update 'this' component's state dynamically.
        """
        import json
        action_args = { "dynamic": True }
        for k, v in kwargs.items():
            if k == 'style':
                val = v
                if isinstance(val, str): val = parse_utility_string(val)
                action_args[k] = val
            elif k == 'attrs' and isinstance(v, dict):
                action_args[k] = v
            elif k == 'classes' and isinstance(v, dict):
                action_args[k] = v
            else:
                action_args[k] = v
                
        payload_js = json.dumps(action_args)
        code = f"var _opts = {payload_js}; _opts.id = event.currentTarget ? event.currentTarget.id : (event.target ? event.target.id : ''); if (window.Dars && typeof window.Dars.change === 'function') window.Dars.change(_opts); else if (typeof change === 'function') change(_opts);"
        return RawJS(code=code)

    def goto(self, idx: int, _component_id: Optional[str] = None) -> RawJS:
        """
        Navigate to a specific state index for this component.
        """
        # Check if component ID was set via this_for() or passed directly
        cid = _component_id or getattr(self, '_cid', None)
        
        # Compile-time validation (when component ID is known)
        if cid and cid in _COMPONENT_TO_STATE_MAP:
            state_name, states_list = _COMPONENT_TO_STATE_MAP[cid]
            if not isinstance(states_list, list) or len(states_list) == 0:
                raise ValueError(
                    f"[Dars Compile Error] Component '{cid}' has dState '{state_name}' "
                    f"but no states list defined."
                )
            if idx < 0 or idx >= len(states_list):
                raise ValueError(
                    f"[Dars Compile Error] this().goto({idx}) - Index {idx} out of bounds for component '{cid}'. "
                    f"Valid indices: 0-{len(states_list)-1}."
                )
        elif cid and cid not in _COMPONENT_TO_STATE_MAP:
             raise ValueError(
                f"[Dars Compile Error] this().goto({idx}) used on component '{cid}' "
                f"but no dState is defined for this component."
            )
        
        code = f"var _opts = {{ state: {idx} }}; _opts.id = event.currentTarget ? event.currentTarget.id : (event.target ? event.target.id : ''); if (window.Dars && typeof window.Dars.change === 'function') window.Dars.change(_opts); else if (typeof change === 'function') change(_opts);"
        return RawJS(code=code)

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
