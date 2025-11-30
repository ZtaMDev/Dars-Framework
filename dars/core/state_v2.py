"""
Dars Framework State Management V2

This module provides a modern state management system that replaces
the verbose dState/cState/Mod API with a cleaner, more intuitive interface.

Key Features:
- Direct property modification: state.text = "value"
- Reactive operations: state.text.increment(), state.text.auto_increment()
- Immutable default state with .reset()
- Clean transitions without Mod/cState verbosity
- Full integration with component system
"""

from typing import Any, Dict, List, Optional, Callable, Union
from copy import deepcopy
import json

# Global registry for V2 states (similar to STATE_BOOTSTRAP in state.py)
STATE_V2_REGISTRY: List['State'] = []


class ReactiveProperty:
    """
    Represents a single reactive property of a component.
    
    Supports Pythonic operations like +=, -=, and methods like increment(), set(), etc.
    All mutations automatically sync to the client-side DOM via the change() function.
    """
    
    def __init__(self, state: 'State', name: str, initial_value: Any):
        self._state = state
        self._name = name
        self._value = initial_value
        self._default = deepcopy(initial_value)
        self._loop_config = None  # For auto_increment/auto_decrement
    
    @property
    def value(self) -> Any:
        """Get the current value of this property"""
        return self._value
    
    @value.setter
    def value(self, new_value: Any):
        """Set the value and sync to client"""
        self._value = new_value
        self._sync_to_client()
    
    def _sync_to_client(self):
        """
        Generate JavaScript code to sync this property change to the client.
        This is called internally when the property is modified.
        """
        # This will be collected during export and injected as event handlers
        pass
    
    def _generate_change_call(self, **props) -> str:
        """
        Generate JS code to call window.Dars.change() with proper payload.
        This handles all property types including events (dScript objects).
        """
        from dars.scripts.dscript import dScript, RawJS
        
        component_id = self._state.component.id
        
        # Build payload parts
        parts = [f"id: '{component_id}'", "dynamic: true"]
        
        for k, v in props.items():
            # Helper to get JS code or JSON string
            def to_js_value(val):
                # Import DataAccessor locally to avoid circular imports
                try:
                    from dars.backend.data import DataAccessor
                    if isinstance(val, DataAccessor):
                        return val.code
                except ImportError:
                    pass
                
                if isinstance(val, (dScript, RawJS)):
                    return val.code if hasattr(val, 'code') else str(val)
                return json.dumps(val)

            # Handle events (on_click, on_change, etc.)
            if k.startswith('on_'):
                if isinstance(v, dScript):
                    # Extract JS code from dScript object
                    event_code = v.code if hasattr(v, 'code') else str(v)
                    parts.append(f"{k}: {json.dumps(event_code)}")
                elif isinstance(v, (list, tuple)):
                    # Handle array of event handlers
                    codes = []
                    for handler in v:
                        if isinstance(handler, dScript):
                            codes.append(handler.code if hasattr(handler, 'code') else str(handler))
                        elif isinstance(handler, str):
                            codes.append(handler)
                    parts.append(f"{k}: {json.dumps(codes)}")
                elif isinstance(v, str):
                    # Raw JS string
                    parts.append(f"{k}: {json.dumps(v)}")
                else:
                    # Skip unsupported event types
                    continue
            # Handle regular properties
            elif k == 'text':
                parts.append(f"text: {to_js_value(v)}")
            elif k == 'html':
                parts.append(f"html: {to_js_value(v)}")
            elif k == 'style' and isinstance(v, dict):
                # Handle style dict where values might be RawJS
                style_parts = []
                for sk, sv in v.items():
                    style_parts.append(f"{json.dumps(sk)}: {to_js_value(sv)}")
                parts.append(f"style: {{{', '.join(style_parts)}}}")
            elif k == 'class_name':
                # Map class_name to classes object
                if isinstance(v, str):
                    # Setting a single class - we should replace all classes
                    parts.append(f"attrs: {{class: {json.dumps(v)}}}")
                elif isinstance(v, (dScript, RawJS)):
                     parts.append(f"attrs: {{class: {v.code}}}")
                elif isinstance(v, dict):
                    # Advanced class manipulation
                    parts.append(f"classes: {json.dumps(v)}")
            elif k == 'attrs' and isinstance(v, dict):
                attrs_parts = []
                for ak, av in v.items():
                    attrs_parts.append(f"{json.dumps(ak)}: {to_js_value(av)}")
                parts.append(f"attrs: {{{', '.join(attrs_parts)}}}")
            elif k == 'classes' and isinstance(v, dict):
                parts.append(f"classes: {json.dumps(v)}")
            else:
                # Generic attribute
                try:
                    parts.append(f"attrs: {{{json.dumps(k)}: {to_js_value(v)}}}")
                except (TypeError, ValueError):
                    # Skip non-JSON-serializable values
                    continue
        
        payload = "{" +  ", ".join(parts) + "}"
        
        code = f"""
(async () => {{
    try {{
        let ch = window.__DARS_CHANGE_FN;
        if (!ch) {{
            if (window.Dars && typeof window.Dars.change === 'function') {{
                ch = window.Dars.change.bind(window.Dars);
            }} else {{
                const m = await import('/lib/dars.min.js');
                ch = (m.change || (m.default && m.default.change));
            }}
            if (typeof ch === 'function') window.__DARS_CHANGE_FN = ch;
        }}
        if (typeof ch === 'function') ch({payload});
    }} catch (e) {{ console.error('[Dars] State error:', e); }}
}})();
""".strip()
        
        return code

    
    def increment(self, by: int = 1) -> Callable:
        """
        Returns an event handler function that increments this property.
        
        Args:
            by: Amount to increment (default: 1)
            
        Example:
            button.on_click = counter_state.text.increment(by=1)
        """
        from dars.scripts.dscript import dScript
        
        # Only numeric properties can be incremented
        if self._name not in ('text',):
            raise ValueError(f"Cannot increment non-numeric property '{self._name}'. Use .set() instead.")
        
        component_id = self._state.component.id
        
        code = f"""
(async () => {{
const el = document.getElementById('{component_id}');
if (el) {{
    const current = parseFloat(el.textContent || '0') || 0;
    const newValue = current + {by};
    el.textContent = String(newValue);
    
    // Dispatch state update event
    const ev = new CustomEvent('dars:state-update', {{
        detail: {{ id: '{component_id}', property: 'text', value: newValue }}
    }});
    el.dispatchEvent(ev);
}}
}})();
""".strip()
        
        return dScript(code)
    
    def decrement(self, by: int = 1) -> Callable:
        """
        Returns an event handler that decrements this property.
        
        Args:
            by: Amount to decrement (default: 1)
            
        Example:
            button.on_click = counter_state.text.decrement(by=1)
        """
        return self.increment(by=-by)
    
    def set(self, value: Any) -> Callable:
        """
        Returns an event handler that sets this property to a specific value.
        
        Works with any property type: text, html, style, class_name, attrs, etc.
        
        Args:
            value: The value to set
            
        Example:
            button.on_click = status_state.text.set("Loading...")
            button.on_click = state.class_name.set("active")
            button.on_click = state.style.set({"color": "red"})
        """
        from dars.scripts.dscript import dScript
        
        # Use the change() function to properly handle different property types
        code = self._generate_change_call(**{self._name: value})
        return dScript(code)
    
    def auto_increment(self, by: int = 1, interval: int = 1000, max: Optional[int] = None) -> Callable:
        """
        Start continuous auto-increment operation.
        
        Args:
            by: Amount to increment each interval
            interval: Time between increments in milliseconds
            max: Maximum value (stops when reached)
            
        Example:
            timer_state.text.auto_increment(by=1, interval=1000)
        """
        from dars.scripts.dscript import dScript
        import json
        
        config = {
            'type': 'auto_increment',
            'property': self._name,
            'by': by,
            'interval': interval,
            'max': max
        }
        self._loop_config = config
        
        component_id = self._state.component.id
        config_json = json.dumps(config)
        
        code = f"""
(async () => {{
if (window.Dars && window.Dars.startLoop) {{
    window.Dars.startLoop('{component_id}', {config_json});
}}
}})();
""".strip()
        return dScript(code)
    
    def auto_decrement(self, by: int = 1, interval: int = 1000, min: Optional[int] = None) -> Callable:
        """
        Start continuous auto-decrement operation.
        
        Args:
            by: Amount to decrement each interval
            interval: Time between decrements in milliseconds
            min: Minimum value (stops when reached)
            
        Example:
            countdown_state.text.auto_decrement(by=1, interval=1000, min=0)
        """
        from dars.scripts.dscript import dScript
        import json
        
        config = {
            'type': 'auto_decrement',
            'property': self._name,
            'by': by,
            'interval': interval,
            'min': min
        }
        self._loop_config = config
        
        component_id = self._state.component.id
        config_json = json.dumps(config)
        
        code = f"""
(async () => {{
if (window.Dars && window.Dars.startLoop) {{
    window.Dars.startLoop('{component_id}', {config_json});
}}
}})();
""".strip()
        return dScript(code)
    
    def stop_auto(self) -> Callable:
        """
        Returns an event handler that stops any auto-increment/decrement loop.
        
        Example:
            stop_btn.on_click = timer_state.text.stop_auto()
        """
        from dars.scripts.dscript import dScript
        
        component_id = self._state.component.id
        
        code = f"""
(async () => {{
if (window.Dars && window.Dars.stopLoop) {{
    window.Dars.stopLoop('{component_id}');
}}
}})();
""".strip()
        
        return dScript(code)
    
    # Magic methods for Pythonic operations
    def __iadd__(self, other):
        """Support for += operator"""
        self._value += other
        self._sync_to_client()
        return self
    
    def __isub__(self, other):
        """Support for -= operator"""
        self._value -= other
        self._sync_to_client()
        return self
    
    def __imul__(self, other):
        """Support for *= operator"""
        self._value *= other
        self._sync_to_client()
        return self
    
    def __itruediv__(self, other):
        """Support for /= operator"""
        self._value /= other
        self._sync_to_client()
        return self
    
    def __repr__(self):
        return f"ReactiveProperty(name='{self._name}', value={self._value})"



class StateTransition:
    """
    Represents a conditional state transition.
    
    Used with State.when() to create declarative state machines.
    """
    
    def __init__(self, state: 'State', condition: Callable):
        self._state = state
        self.condition = condition
        self.props = {}
    
    def apply(self, **props):
        """
        Apply properties when condition is met.
        
        Args:
            **props: Properties to update
            
        Example:
            state.when(lambda s: s.text > 10).apply(text="MAX!", style={'color': 'red'})
        """
        self.props = props
        self._state._transitions.append(self)
        return self
    
    def to_dict(self) -> Dict[str, Any]:
        """Serialize transition for JS runtime"""
        return {
            'condition': 'lambda',  # We'll need to handle this specially
            'props': self.props
        }


class State:
    """
    Main state management class for Dars V2.
    
    Provides Pythonic, reactive state management with direct property modification,
    continuous operations, and clean transitions.
    
    Example:
        counter_text = Text("0", id="counter")
        counter = State(counter_text, text=0)
        
        button.on_click = counter.text.increment(by=1)
        counter.text.auto_increment(by=1, interval=1000)
    """
    
    def __init__(self, component, **initial_props):
        """
        Initialize a new State bound to a component.
        
        Args:
            component: The Dars component to bind this state to, or a string ID
            **initial_props: Initial property values (e.g., text=0, style={...})
        """
        # Handle both component objects and string IDs
        if isinstance(component, str):
            # Create a mock component object with just the ID
            class MockComponent:
                def __init__(self, component_id):
                    self.id = component_id
            self.component = MockComponent(component)
        else:
            self.component = component
            
        self._props: Dict[str, ReactiveProperty] = {}
        self._default_snapshot = deepcopy(initial_props)
        self._transitions: List[StateTransition] = []
        self._loops: List[Dict] = []
        
        # Create ReactiveProperty for each initial prop
        for key, value in initial_props.items():
            reactive_prop = ReactiveProperty(self, key, value)
            self._props[key] = reactive_prop
            # Make it accessible as state.text, state.style, etc.
            setattr(self, key, reactive_prop)
        
        # Register in global registry
        STATE_V2_REGISTRY.append(self)
        
        # Bind to component if it has bind_state method (only for real components)
        if hasattr(component, 'bind_state') and not isinstance(component, str):
            component.bind_state(self)
    
    @property
    def default(self):
        """
        Access to immutable default state snapshot.
        
        Returns a read-only view of the initial state configuration.
        """
        class DefaultSnapshot:
            def __init__(self, snapshot):
                self._snapshot = snapshot
            
            def __getattr__(self, name):
                return self._snapshot.get(name)
            
            def __setattr__(self, name, value):
                if name.startswith('_'):
                    object.__setattr__(self, name, value)
                else:
                    raise AttributeError("Default state is immutable. Use .reset() to restore defaults.")
        
        return DefaultSnapshot(self._default_snapshot)
    
    def reset(self) -> Callable:
        """
        Returns an event handler that resets all properties to their default values.
        
        Example:
            reset_btn.on_click = counter_state.reset()
        """
        from dars.scripts.dscript import dScript
        
        component_id = self.component.id
        
        # Build payload with all default properties
        parts = [f"id: '{component_id}'", "dynamic: true"]
        attrs_dict = {}  # Collect all attrs in a single object
        
        for k, v in self._default_snapshot.items():
            # Handle events (on_click, on_change, etc.)
            if k.startswith('on_'):
                if isinstance(v, dScript):
                    # Extract JS code from dScript object
                    event_code = v.code if hasattr(v, 'code') else str(v)
                    parts.append(f"{k}: {json.dumps(event_code)}")
                elif isinstance(v, (list, tuple)):
                    # Handle array of event handlers
                    codes = []
                    for handler in v:
                        if isinstance(handler, dScript):
                            codes.append(handler.code if hasattr(handler, 'code') else str(handler))
                        elif isinstance(handler, str):
                            codes.append(handler)
                    parts.append(f"{k}: {json.dumps(codes)}")
                elif isinstance(v, str):
                    # Raw JS string
                    parts.append(f"{k}: {json.dumps(v)}")
                else:
                    # Skip unsupported event types
                    continue
            elif k == 'text':
                parts.append(f"text: {json.dumps(v)}")
            elif k == 'html':
                parts.append(f"html: {json.dumps(v)}")
            elif k == 'style' and isinstance(v, dict):
                parts.append(f"style: {json.dumps(v)}")
            elif k == 'class_name':
                if isinstance(v, str):
                    attrs_dict['class'] = v
                elif isinstance(v, dict):
                    parts.append(f"classes: {json.dumps(v)}")
            elif k == 'attrs' and isinstance(v, dict):
                # Merge attrs dict
                attrs_dict.update(v)
            else:
                # Add to attrs dict
                try:
                    attrs_dict[k] = v
                except (TypeError, ValueError):
                    continue
        
        # Add attrs as a single object if there are any
        if attrs_dict:
            parts.append(f"attrs: {json.dumps(attrs_dict)}")
        
        payload = "{" + ", ".join(parts) + "}"
        
        code = f"""
(async () => {{
    try {{
        let ch = window.__DARS_CHANGE_FN;
        if (!ch) {{
            if (window.Dars && typeof window.Dars.change === 'function') {{
                ch = window.Dars.change.bind(window.Dars);
            }} else {{
                const m = await import('/lib/dars.min.js');
                ch = (m.change || (m.default && m.default.change));
            }}
            if (typeof ch === 'function') window.__DARS_CHANGE_FN = ch;
        }}
        if (typeof ch === 'function') ch({payload});
    }} catch (e) {{ console.error('[Dars] State reset error:', e); }}
}})();
""".strip()
        
        return dScript(code)
    
    def update(self, **props) -> Callable:
        """
        Returns an event handler that updates multiple properties at once.
        
        Supports all property types: text, html, style, class_name, attrs, etc.
        
        Args:
            **props: Properties to update
            
        Example:
            button.on_click = state.update(text="New", style={'color': 'red'})
            button.on_click = state.update(class_name="active", style={'opacity': '1'})
        """
        from dars.scripts.dscript import dScript
        
        component_id = self.component.id
        
        # Build payload with proper property mapping
        parts = [f"id: '{component_id}'", "dynamic: true"]
        
        for k, v in props.items():
            # Handle events (on_click, on_change, etc.)
            if k.startswith('on_'):
                if isinstance(v, dScript):
                    # Extract JS code from dScript object
                    event_code = v.code if hasattr(v, 'code') else str(v)
                    parts.append(f"{k}: {json.dumps(event_code)}")
                elif isinstance(v, (list, tuple)):
                    # Handle array of event handlers
                    codes = []
                    for handler in v:
                        if isinstance(handler, dScript):
                            codes.append(handler.code if hasattr(handler, 'code') else str(handler))
                        elif isinstance(handler, str):
                            codes.append(handler)
                    parts.append(f"{k}: {json.dumps(codes)}")
                elif isinstance(v, str):
                    # Raw JS string
                    parts.append(f"{k}: {json.dumps(v)}")
                else:
                    # Skip unsupported event types
                    continue
            elif k == 'text':
                parts.append(f"text: {json.dumps(v)}")
            elif k == 'html':
                parts.append(f"html: {json.dumps(v)}")
            elif k == 'style' and isinstance(v, dict):
                parts.append(f"style: {json.dumps(v)}")
            elif k == 'class_name':
                if isinstance(v, str):
                    parts.append(f"attrs: {{class: {json.dumps(v)}}}")
                elif isinstance(v, dict):
                    parts.append(f"classes: {json.dumps(v)}")
            elif k == 'attrs' and isinstance(v, dict):
                parts.append(f"attrs: {json.dumps(v)}")
            elif k == 'classes' and isinstance(v, dict):
                parts.append(f"classes: {json.dumps(v)}")
            else:
                try:
                    parts.append(f"attrs: {{{json.dumps(k)}: {json.dumps(v)}}}")
                except (TypeError, ValueError):
                    continue
        
        payload = "{" + ", ".join(parts) + "}"
        
        code = f"""
(async () => {{
    try {{
        let ch = window.__DARS_CHANGE_FN;
        if (!ch) {{
            if (window.Dars && typeof window.Dars.change === 'function') {{
                ch = window.Dars.change.bind(window.Dars);
            }} else {{
                const m = await import('/lib/dars.min.js');
                ch = (m.change || (m.default && m.default.change));
            }}
            if (typeof ch === 'function') window.__DARS_CHANGE_FN = ch;
        }}
        if (typeof ch === 'function') ch({payload});
    }} catch (e) {{ console.error('[Dars] State update error:', e); }}
}})();
""".strip()
        
        return dScript(code)
    
    def when(self, condition: Callable) -> StateTransition:
        """
        Create a conditional transition.
        
        Args:
            condition: Lambda or callable that returns bool when evaluated with state
            
        Example:
            state.when(lambda s: s.text > 10).apply(text="MAX!", style={'color': 'red'})
        """
        return StateTransition(self, condition)
    
    def loop(self, interval: int = 1000):
        """
        Decorator for creating custom reactive loops.
        
        Args:
            interval: Loop interval in milliseconds
            
        Example:
            @state.loop(interval=500)
            def animate():
                state.text = int(state.text.value) * 2
                return int(state.text.value) < 100  # Continue condition
        """
        def decorator(func: Callable):
            # Store loop configuration
            loop_config = {
                'id': self.component.id,
                'type': 'custom',
                'interval': interval,
                'function': func  # We'll need to serialize this
            }
            self._loops.append(loop_config)
            return func
        return decorator
    
    def _register_loop(self, loop_config: Dict):
        """Internal method to register a loop configuration"""
        self._loops.append(loop_config)
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Serialize state for bootstrap injection.
        
        Returns a dictionary that can be JSON-serialized and sent to the client.
        """
        return {
            'id': self.component.id if hasattr(self.component, 'id') else None,
            'defaultProps': self._default_snapshot,
            'loops': self._loops,
            'transitions': [t.to_dict() for t in self._transitions]
        }
    
    def __repr__(self):
        props_str = ", ".join(f"{k}={v.value}" for k, v in self._props.items())
        return f"State(component={self.component.id}, {props_str})"
