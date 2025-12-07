# Dars Framework - Core Source File
#
# This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0.
# If a copy of the MPL was not distributed with this file, You can obtain one at
# https://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2025 ZtaDev
"""
useDynamic Hook

Enables reactive binding to external State objects in FunctionComponents.
When the state changes, the DOM automatically updates.
"""

# Global registry to track all dynamic bindings
_DYNAMIC_BINDINGS_REGISTRY = {}


class DynamicBinding:
    """
    Represents a reactive binding to a state property.
    
    This object acts as a placeholder in the HTML template that will be
    replaced with a reactive span element during rendering.
    """
    
    _counter = 0
    
    def __init__(self, state_path: str):
        """
        Initialize a dynamic binding.
        
        Args:
            state_path: Dot-notation path to state property (e.g., "userCard.name")
        """
        self.state_path = state_path
        DynamicBinding._counter += 1
        self.marker = f"__DARS_DYNAMIC_{DynamicBinding._counter}_{id(self)}__"
        self._initial_value = None
        
        # Register this binding globally
        _DYNAMIC_BINDINGS_REGISTRY[self.marker] = self.state_path
    
    def __str__(self):
        """Return the marker string that will be replaced during rendering"""
        return self.marker
    
    def __repr__(self):
        return f"DynamicBinding({self.state_path!r})"

    def get_initial_value(self):
        """
        Resolve the current value from the state registry.
        Returns None if state or property not found.
        """
        try:
            from dars.core.state_v2 import STATE_V2_REGISTRY
            
            parts = self.state_path.split('.')
            if len(parts) < 2:
                return None
                
            state_id = parts[0]
            prop_name = parts[1]
            
            # Find state by ID (search in reverse to get the latest instance during hot reload)
            state = next((s for s in reversed(STATE_V2_REGISTRY) if s.component.id == state_id), None)
            if state:
                # Get property value
                prop = getattr(state, prop_name, None)
                if prop:
                    return prop.value
            return None
        except Exception:
            return None


def useDynamic(state_path: str) -> DynamicBinding:
    """
    Create a reactive binding to a state property.
    
    This hook allows FunctionComponents and built-in components props to reactively bind to external State objects.
    When the state value changes, the DOM element will automatically update.
    
    Args:
        state_path: Dot-notation path to the state property (e.g., "userCard.name")
    
    Returns:
        DynamicBinding object that will be replaced with reactive HTML
    
    Example:
    ```python
        userState = State("user", name="John", email="john@example.com")
        
        @FunctionComponent
        def UserCard(**props):
            return f'''
            <div {Props.id} {Props.class_name} {Props.style}>
                <h3>{useDynamic("user.name")}</h3>
                <p>{useDynamic("user.email")}</p>
            </div>
            '''
        
        # Later, when state changes:
        userState.name.set("Jane")  # DOM automatically updates
    ```
    
    Example 2:

    ```python
    userState = State("user", name="John", email="john@example.com")
        
    Text(text=useDynamic("user.name"))
    ```
    
    Notes:
        - The state_path must reference a registered State object
        - The binding is one-way: state → DOM
        - Multiple components can bind to the same state property
        - Nested paths are supported (e.g., "user.profile.name")
    """
    return DynamicBinding(state_path)


def get_bindings_registry():
    """Get the global bindings registry"""
    return _DYNAMIC_BINDINGS_REGISTRY


def clear_bindings_registry():
    """Clear the global bindings registry (useful for testing/resets)"""
    global _DYNAMIC_BINDINGS_REGISTRY
    _DYNAMIC_BINDINGS_REGISTRY = {}
