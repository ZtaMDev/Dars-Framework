# Dars Framework - Core Source File
#
# This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0.
# If a copy of the MPL was not distributed with this file, You can obtain one at
# https://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2025 ZtaDev
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

import json
from copy import deepcopy
from typing import Any, Callable, Dict, List, Optional, Union

from dars.core.utilities import parse_utility_string
from dars.scripts.dscript import dScript

# Global registry for V2 states (similar to STATE_BOOTSTRAP in state.py)
STATE_V2_REGISTRY: List["State"] = []


def clear_state_registry():
    """Clear the global state registry. Used during hot reload."""
    global STATE_V2_REGISTRY
    STATE_V2_REGISTRY.clear()


class ReactiveProperty:
    """
    Represents a single reactive property of a component.

    Supports Pythonic operations like +=, -=, and methods like increment(), set(), etc.
    All mutations automatically sync to the client-side DOM via the change() function.
    """

    def __init__(self, state: "State", name: str, initial_value: Any):
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

    def _generate_change_action(self, **props) -> dict:
        """
        Generate DAP change action dictionary.
        """
        component_id = self._state.component.id

        args = {"id": component_id, "dynamic": True}

        for k, v in props.items():
            # Helper to get structural value
            def to_structure(val):
                if hasattr(val, "_to_structure"):
                    return val._to_structure()
                if hasattr(val, "to_dict"):
                    return val.to_dict()
                if isinstance(val, (list, tuple)):
                    return [to_structure(x) for x in val]
                if isinstance(val, dict):
                    return {sk: to_structure(sv) for sk, sv in val.items()}
                return val

            # Handle events (on_click, on_change, etc.)
            if k.startswith("on_"):
                # Events are essentially lists of actions or a single action
                # dScript.get_action() returns the action dict if available
                if hasattr(v, "get_action"):
                    action = v.get_action()
                    if action:
                        args[k] = action
                    else:
                        pass
                elif isinstance(v, list):
                    actions = []
                    for handler in v:
                        if hasattr(handler, "get_action"):
                            act = handler.get_action()
                            if act:
                                actions.append(act)
                    if actions:
                        args[k] = {"op": "sequence", "args": actions}
            # Handle regular properties
            elif k == "text":
                args["text"] = to_structure(v)
            elif k == "html":
                args["html"] = to_structure(v)
            elif k == "style":
                args["style"] = to_structure(v)
            elif k == "class_name":
                # Map class_name to class attribute or specialized 'classes' dict
                # If v is a string, it replaces the class attribute?
                # The runtime change() function handles 'classes' dict for granular updates,
                # or 'attrs.class' for full replacement.
                # Use attrs.class for simple string to match previous behavior
                if isinstance(v, str) or hasattr(v, "_to_structure"):
                    if "attrs" not in args:
                        args["attrs"] = {}
                    args["attrs"]["class"] = to_structure(v)
                elif isinstance(v, dict):
                    args["classes"] = to_structure(v)
            elif k == "attrs" and isinstance(v, dict):
                comp_attrs = args.get("attrs", {})
                comp_attrs.update(to_structure(v))
                args["attrs"] = comp_attrs
            elif k == "classes" and isinstance(v, dict):
                args["classes"] = to_structure(v)
            else:
                # Custom properties or unmapped attrs
                # Add directly to args, similar to previous behavior
                # But typically only text/html/style/attrs/classes are supported by change() runtime efficiently.
                # However, previous code allowed custom props.
                args[k] = to_structure(v)

        return {"op": "change", "args": args}

    def increment(self, by: int = 1) -> "dScript":
        """Increment value action"""
        from dars.scripts.dscript import dScript

        if not isinstance(self._value, (int, float)):
            # Allow if initial value is numeric string? No, enforce cleaner types.
            pass

        action = self._generate_change_action(
            **{
                self._name: {
                    "op": "math_expr",
                    "args": {
                        "left": {
                            "op": "get_state_value",
                            "args": {
                                "state_id": self._state.component.id,
                                "prop_name": self._name,
                            },
                        },
                        "operator": "+",
                        "right": by,
                    },
                }
            }
        )
        return dScript(data=action)

    def decrement(self, by: int = 1) -> "dScript":
        """Decrement value action"""
        return self.increment(by=-by)

    def set(self, value: Any) -> "dScript":
        """Set value action"""
        from dars.scripts.dscript import dScript

        # _generate_change_action handles MathExpression because of to_structure helper recursively calling _to_structure
        action = self._generate_change_action(**{self._name: value})
        return dScript(data=action)

    def auto_increment(
        self, by: int = 1, interval: int = 1000, max: Optional[int] = None
    ) -> "dScript":
        """Auto-increment loop action"""
        from dars.scripts.dscript import dScript

        config = {
            "type": "auto_increment",
            "property": self._name,
            "by": by,
            "interval": interval,
            "max": max,
        }
        self._loop_config = config

        action = {
            "op": "start_loop",
            "args": {"id": self._state.component.id, "config": config},
        }
        return dScript(data=action)

    def auto_decrement(
        self, by: int = 1, interval: int = 1000, min: Optional[int] = None
    ) -> "dScript":
        """Auto-decrement loop action"""
        from dars.scripts.dscript import dScript

        config = {
            "type": "auto_decrement",
            "property": self._name,
            "by": by,
            "interval": interval,
            "min": min,
        }
        self._loop_config = config

        action = {
            "op": "start_loop",
            "args": {"id": self._state.component.id, "config": config},
        }
        return dScript(data=action)

    def stop_auto(self) -> "dScript":
        """Stop loop action"""
        from dars.scripts.dscript import dScript

        action = {"op": "stop_loop", "args": {"id": self._state.component.id}}
        return dScript(data=action)

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

    def __init__(self, state: "State", condition: Callable):
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
            "condition": "lambda",  # We'll need to handle this specially
            "props": self.props,
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
        if hasattr(component, "bind_state") and not isinstance(component, str):
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
                if name.startswith("_"):
                    object.__setattr__(self, name, value)
                else:
                    raise AttributeError(
                        "Default state is immutable. Use .reset() to restore defaults."
                    )

        return DefaultSnapshot(self._default_snapshot)

    def reset(self) -> "dScript":
        """Reset state to default action"""
        from dars.scripts.dscript import dScript

        component_id = self.component.id
        args = {"id": component_id, "dynamic": True}

        # Helper to get structural value (allows list/dict recursion)
        def to_structure(val):
            if hasattr(val, "_to_structure"):
                return val._to_structure()
            if hasattr(val, "to_dict"):
                return val.to_dict()
            if isinstance(val, (list, tuple)):
                return [to_structure(x) for x in val]
            if isinstance(val, dict):
                return {sk: to_structure(sv) for sk, sv in val.items()}
            return val

        for k, v in self._default_snapshot.items():
            # Handle events
            if k.startswith("on_"):
                if hasattr(v, "get_action"):
                    act = v.get_action()
                    if act:
                        args[k] = act
                elif isinstance(v, list):
                    actions = []
                    for handler in v:
                        if hasattr(handler, "get_action"):
                            act = handler.get_action()
                            if act:
                                actions.append(act)
                    if actions:
                        args[k] = {"op": "sequence", "args": actions}
                continue

            # Handle properties logic (duplicated from ReactiveProperty for independence)
            if k == "text":
                args["text"] = to_structure(v)
            elif k == "html":
                args["html"] = to_structure(v)
            elif k == "style":
                args["style"] = to_structure(v)
            elif k == "class_name":
                if isinstance(v, str) or hasattr(v, "_to_structure"):
                    if "attrs" not in args:
                        args["attrs"] = {}
                    args["attrs"]["class"] = to_structure(v)
                elif isinstance(v, dict):
                    args["classes"] = to_structure(v)
            elif k == "attrs" and isinstance(v, dict):
                comp_attrs = args.get("attrs", {})
                comp_attrs.update(to_structure(v))
                args["attrs"] = comp_attrs
            elif k == "classes" and isinstance(v, dict):
                args["classes"] = to_structure(v)
            else:
                args[k] = to_structure(v)

        return dScript(data={"op": "change", "args": args})

    def update(self, **props) -> "dScript":
        """Update multiple properties action"""
        from dars.scripts.dscript import dScript

        component_id = self.component.id
        args = {"id": component_id, "dynamic": True}

        # Helper to get structural value
        def to_structure(val):
            if hasattr(val, "_to_structure"):
                return val._to_structure()
            if hasattr(val, "to_dict"):
                return val.to_dict()
            if isinstance(val, (list, tuple)):
                return [to_structure(x) for x in val]
            if isinstance(val, dict):
                return {sk: to_structure(sv) for sk, sv in val.items()}
            return val

        for k, v in props.items():
            if k.startswith("on_"):
                if hasattr(v, "get_action"):
                    act = v.get_action()
                    if act:
                        args[k] = act
                elif isinstance(v, list):
                    actions = []
                    for handler in v:
                        if hasattr(handler, "get_action"):
                            act = handler.get_action()
                            if act:
                                actions.append(act)
                    if actions:
                        args[k] = {"op": "sequence", "args": actions}
                continue

            if k == "text":
                args["text"] = to_structure(v)
            elif k == "html":
                args["html"] = to_structure(v)
            elif k == "style":
                args["style"] = to_structure(v)
            elif k == "class_name":
                if isinstance(v, str) or hasattr(v, "_to_structure"):
                    if "attrs" not in args:
                        args["attrs"] = {}
                    args["attrs"]["class"] = to_structure(v)
                elif isinstance(v, dict):
                    args["classes"] = to_structure(v)
            elif k == "attrs" and isinstance(v, dict):
                comp_attrs = args.get("attrs", {})
                comp_attrs.update(to_structure(v))
                args["attrs"] = comp_attrs
            elif k == "classes" and isinstance(v, dict):
                args["classes"] = to_structure(v)
            else:
                args[k] = to_structure(v)

        return dScript(data={"op": "change", "args": args})

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
                "id": self.component.id,
                "type": "custom",
                "interval": interval,
                "function": func,  # We'll need to serialize this
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
            "id": self.component.id if hasattr(self.component, "id") else None,
            "name": self.component.id if hasattr(self.component, "id") else None,
            "defaultProps": self._default_snapshot,
            "loops": self._loops,
            "transitions": [t.to_dict() for t in self._transitions],
        }

    def __getattr__(self, name: str) -> ReactiveProperty:
        """Resolve dynamically-declared state properties for type checkers/runtime.

        This allows patterns like:
            counter = State("counter", count=0)
            counter.count.increment(1)

        even though `count` is provided dynamically via ``**initial_props``.
        """
        props = self.__dict__.get("_props", {})
        if name in props:
            return props[name]
        raise AttributeError(f"State has no property '{name}'")

    def __repr__(self):
        props_str = ", ".join(f"{k}={v.value}" for k, v in self._props.items())
        return f"State(component={self.component.id}, {props_str})"
