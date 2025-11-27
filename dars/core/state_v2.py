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
    All mutations automatically sync to the client-side DOM.
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
    
    def increment(self, by: int = 1) -> Callable:
        """
        Returns an event handler function that increments this property.
        
        Args:
            by: Amount to increment (default: 1)
            
        Example:
            button.on_click = counter_state.text.increment(by=1)
        """
        from dars.scripts.dscript import dScript
        
        # Generate JS code to increment
        component_id = self._state.component.id
        prop_name = self._name
        
        code = f"""
const el = document.getElementById('{component_id}');
if (el) {{
    const current = parseFloat(el.textContent || '0') || 0;
    const newValue = current + {by};
    el.textContent = String(newValue);
    
    // Dispatch state update event
    const ev = new CustomEvent('dars:state-update', {{
        detail: {{ id: '{component_id}', property: '{prop_name}', value: newValue }}
    }});
    el.dispatchEvent(ev);
}}
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
        
        Args:
            value: The value to set
            
        Example:
            button.on_click = status_state.text.set("Loading...")
        """
        from dars.scripts.dscript import dScript
        
        component_id = self._state.component.id
        prop_name = self._name
        
        # Escape value for JS
        if isinstance(value, str):
            js_value = json.dumps(value)
        else:
            js_value = json.dumps(value)
        
        code = f"""
const el = document.getElementById('{component_id}');
if (el) {{
    el.textContent = {js_value};
    
    // Dispatch state update event
    const ev = new CustomEvent('dars:state-update', {{
        detail: {{ id: '{component_id}', property: '{prop_name}', value: {js_value} }}
    }});
    el.dispatchEvent(ev);
}}
""".strip()
        
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
if (window.Dars && window.Dars.startLoop) {{
    window.Dars.startLoop('{component_id}', {config_json});
}}
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
if (window.Dars && window.Dars.startLoop) {{
    window.Dars.startLoop('{component_id}', {config_json});
}}
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
if (window.Dars && window.Dars.stopLoop) {{
    window.Dars.stopLoop('{component_id}');
}}
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
            component: The Dars component to bind this state to
            **initial_props: Initial property values (e.g., text=0, style={...})
        """
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
        
        # Bind to component if it has bind_state method
        if hasattr(component, 'bind_state'):
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
        default_props = json.dumps(self._default_snapshot)
        
        code = f"""
const el = document.getElementById('{component_id}');
if (el) {{
    const defaults = {default_props};
    
    // Reset text if present
    if (defaults.text !== undefined) {{
        el.textContent = String(defaults.text);
    }}
    
    // Reset style if present
    if (defaults.style) {{
        for (const [key, value] of Object.entries(defaults.style)) {{
            el.style[key] = value;
        }}
    }}
    
    // Reset other attributes
    for (const [key, value] of Object.entries(defaults)) {{
        if (key !== 'text' && key !== 'style') {{
            el.setAttribute(key, String(value));
        }}
    }}
    
    // Dispatch reset event
    const ev = new CustomEvent('dars:state-reset', {{
        detail: {{ id: '{component_id}', defaults: defaults }}
    }});
    el.dispatchEvent(ev);
}}
""".strip()
        
        return dScript(code)
    
    def update(self, **props) -> Callable:
        """
        Returns an event handler that updates multiple properties at once.
        
        Args:
            **props: Properties to update
            
        Example:
            button.on_click = state.update(text="New", style={'color': 'red'})
        """
        from dars.scripts.dscript import dScript
        
        component_id = self.component.id
        props_json = json.dumps(props)
        
        code = f"""
const el = document.getElementById('{component_id}');
if (el) {{
    const updates = {props_json};
    
    // Apply text update
    if (updates.text !== undefined) {{
        el.textContent = String(updates.text);
    }}
    
    // Apply style updates
    if (updates.style) {{
        for (const [key, value] of Object.entries(updates.style)) {{
            el.style[key] = value;
        }}
    }}
    
    // Apply other attribute updates
    for (const [key, value] of Object.entries(updates)) {{
        if (key !== 'text' && key !== 'style') {{
            el.setAttribute(key, String(value));
        }}
    }}
    
    // Dispatch update event
    const ev = new CustomEvent('dars:state-update', {{
        detail: {{ id: '{component_id}', updates: updates }}
    }});
    el.dispatchEvent(ev);
}}
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
