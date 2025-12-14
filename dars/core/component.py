# Dars Framework - Core Source File
#
# This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0.
# If a copy of the MPL was not distributed with this file, You can obtain one at
# https://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2025 ZtaDev
from typing import Dict, Any, List, Optional, Callable, Union, Type
from threading import Thread
import inspect
import hashlib
import os
from abc import ABC, abstractmethod
from dars.core.events import EventTypes
from dars.exporters.base import Exporter
from dars.core.utilities import parse_utility_string

class ComponentQuery:
    def __init__(self, components: List['Component']):
        self.components = components

    def find(self, 
             id: Optional[str] = None,
             class_name: Optional[str] = None,
             type: Optional[Union[Type['Component'], str]] = None,
             predicate: Optional[Callable[['Component'], bool]] = None) -> 'ComponentQuery':
        
        """Searches for components within the currently selected components."""  
        results: List['Component'] = []
        
        def match_component(comp: Component) -> bool:
            if id is not None and comp.id != id:
                return False
            if class_name is not None and comp.class_name != class_name:
                return False
            if type is not None:
                if isinstance(type, str):
                    if comp.__class__.__name__ != type:
                        return False
                elif not isinstance(comp, type):
                    return False
            if predicate is not None and not predicate(comp):
                return False
            return True
        
        # Buscar en los hijos de todos los componentes actuales
        for component in self.components:
            for child in component.children:
                if match_component(child):
                    results.append(child)
                # Buscar recursivamente en los hijos del hijo
                for descendant in ComponentQuery([child]).find().get():
                    if match_component(descendant):
                        results.append(descendant)
        
        return ComponentQuery(results)

    def attr(self, **attrs) -> 'ComponentQuery':
        """Modifies the attributes of all found components."""  
        for component in self.components:
            for key, value in attrs.items():
                # Manejo especial para atributos comunes
                if key == 'style':
                    if isinstance(value, str):
                        component.style.update(parse_utility_string(value))
                    else:
                        component.style.update(value)
                    continue
                elif key == 'class_name':
                    component.class_name = value
                    continue
                elif key == 'events':
                    component.events.update(value)
                    continue
                
                # Intenta establecer el atributo directamente si existe
                if hasattr(component, key):
                    setattr(component, key, value)
                # Si no existe como atributo directo, guárdalo en props
                else:
                    component.props[key] = value
        return self

    def get(self) -> List['Component']:
        """Returns the list of found components."""  
        return self.components

    def first(self) -> Optional['Component']:
        """Returns the first found component, or None if there is none."""  
        return self.components[0] if self.components else None

class Component(ABC):
    def __init__(self, **props):
        self.props = props
        self.children: List[Component] = []
        self.parent: Optional[Component] = None
        self.id: Optional[str] = props.get('id')
        self.class_name: str = props.get("class_name", self.__class__.__name__)
        
        # Server Component Configuration
        self.use_server: bool = props.get('use_server', False)
        
        # Automatic Deterministic ID for Server Components (if no ID provided)
        # This ensures IDs match between the Exporter process (frontend build) 
        # and the SSR process (backend), even if they run separately.
        if self.use_server and not self.id:
            try:
                # Get caller frame to identify where the component is instantiated
                # We skip frames inside dars core to find user code
                frame = inspect.currentframe()
                while frame:
                    if 'dars' in frame.f_code.co_filename and 'core' in frame.f_code.co_filename:
                         frame = frame.f_back
                         continue
                    break
                
                if frame:
                    finfo = inspect.getframeinfo(frame)
                    # Create a stable hash based on filename (basename) and line number
                    # We use basename because absolute paths might differ slightly in docker/env
                    # but usually safest to include some path context if possible.
                    # For local dev, basename + line is good enough collision resistance for typical pages.
                    fname = os.path.basename(finfo.filename)
                    seed = f"{fname}:{finfo.lineno}:{self.__class__.__name__}"
                    h = hashlib.md5(seed.encode()).hexdigest()[:8]
                    self.id = f"{self.__class__.__name__.lower()}_{h}"
            except Exception:
                pass

        self._loading_component: Optional['Component'] = props.get('loading_comp')
        self._error_component: Optional['Component'] = props.get('on_error_comp')
        
        # Handle style parsing (str -> dict)
        _style = props.get('style', {})
        self.style: Dict[str, Any] = parse_utility_string(_style) if isinstance(_style, str) else _style
        
        _hover = props.get('hover_style', {})
        self.hover_style: Dict[str, Any] = parse_utility_string(_hover) if isinstance(_hover, str) else _hover
        
        _active = props.get('active_style', {})
        self.active_style: Dict[str, Any] = parse_utility_string(_active) if isinstance(_active, str) else _active

        self.events: Dict[str, Callable] = {}
        self.key: Optional[str] = props.get('key')
        
        
        if props:
            on_map = {
                'on_click': EventTypes.CLICK,
                'on_double_click': EventTypes.DOUBLE_CLICK,
                'on_mouse_down': EventTypes.MOUSE_DOWN,
                'on_mouse_up': EventTypes.MOUSE_UP,
                'on_mouse_enter': EventTypes.MOUSE_ENTER,
                'on_mouse_leave': EventTypes.MOUSE_LEAVE,
                'on_mouse_move': EventTypes.MOUSE_MOVE,
                # Deprecated
                'on_key_down': EventTypes.KEY_DOWN,
                'on_key_up': EventTypes.KEY_UP,
                # Simpler
                'on_key_press': EventTypes.KEY_PRESS,
                'on_keydown_enter': EventTypes.KEY_DOWN_ENTER,
                'on_keyup_enter': EventTypes.KEY_UP_ENTER,
                'on_keypress_enter': EventTypes.KEY_PRESS_ENTER,
                'on_keydown_escape': EventTypes.KEY_DOWN_ESCAPE,
                'on_keyup_escape': EventTypes.KEY_UP_ESCAPE,
                'on_keydown_tab': EventTypes.KEY_DOWN_TAB,
                'on_keyup_tab': EventTypes.KEY_UP_TAB,
                'on_keydown_space': EventTypes.KEY_DOWN_SPACE,
                'on_keyup_space': EventTypes.KEY_UP_SPACE,
                'on_keydown_arrow_up': EventTypes.KEY_DOWN_ARROW_UP,
                'on_keydown_arrow_down': EventTypes.KEY_DOWN_ARROW_DOWN,
                'on_keydown_arrow_left': EventTypes.KEY_DOWN_ARROW_LEFT,
                'on_keydown_arrow_right': EventTypes.KEY_DOWN_ARROW_RIGHT,
                'on_keyup_arrow_up': EventTypes.KEY_UP_ARROW_UP,
                'on_keyup_arrow_down': EventTypes.KEY_UP_ARROW_DOWN,
                'on_keyup_arrow_left': EventTypes.KEY_UP_ARROW_LEFT,
                'on_keyup_arrow_right': EventTypes.KEY_UP_ARROW_RIGHT,
                'on_keydown_backspace': EventTypes.KEY_DOWN_BACKSPACE,
                'on_keydown_delete': EventTypes.KEY_DOWN_DELETE,
                'on_keydown_ctrl': EventTypes.KEY_DOWN_CTRL,
                'on_keyup_ctrl': EventTypes.KEY_UP_CTRL,
                'on_keydown_alt': EventTypes.KEY_DOWN_ALT,
                'on_keyup_alt': EventTypes.KEY_UP_ALT,
                'on_keydown_shift': EventTypes.KEY_DOWN_SHIFT,
                'on_keyup_shift': EventTypes.KEY_UP_SHIFT,
                'on_change': EventTypes.CHANGE,
                'on_input': EventTypes.INPUT,
                'on_submit': EventTypes.SUBMIT,
                'on_focus': EventTypes.FOCUS,
                'on_blur': EventTypes.BLUR,
                'on_load': EventTypes.LOAD,
                'on_error': EventTypes.ERROR,
                'on_resize': EventTypes.RESIZE,
            }
            for k, v in list(props.items()):
                if k in on_map and v is not None:
                    if isinstance(v, (list, tuple)):
                        handlers = []
                        for handler_item in v:
                            handler = self._normalize_handler(handler_item)
                            if handler:
                                handlers.append(handler)
                        if handlers:
                            self.set_event(on_map[k], handlers)
                    else:
                        # Comportamiento original para handlers únicos
                        handler = self._normalize_handler(v)
                        if handler:
                            self.set_event(on_map[k], handler)
    
    def __setattr__(self, name: str, value: Any) -> None:
        """Intercept attribute assignments to handle on_* event properties."""
        # Allow normal attribute setting for non-event properties
        if not name.startswith('on_'):
            object.__setattr__(self, name, value)
            return
        
        # Handle on_* event property assignments
        event_map = {
            'on_click': EventTypes.CLICK,
            'on_double_click': EventTypes.DOUBLE_CLICK,
            'on_mouse_down': EventTypes.MOUSE_DOWN,
            'on_mouse_up': EventTypes.MOUSE_UP,
            'on_mouse_enter': EventTypes.MOUSE_ENTER,
            'on_mouse_leave': EventTypes.MOUSE_LEAVE,
            'on_mouse_move': EventTypes.MOUSE_MOVE,
            'on_key_down': EventTypes.KEY_DOWN,
            'on_key_up': EventTypes.KEY_UP,
            'on_key_press': EventTypes.KEY_PRESS,
            # Key-specific events
            'on_keydown_enter': EventTypes.KEY_DOWN_ENTER,
            'on_keyup_enter': EventTypes.KEY_UP_ENTER,
            'on_keypress_enter': EventTypes.KEY_PRESS_ENTER,
            'on_keydown_escape': EventTypes.KEY_DOWN_ESCAPE,
            'on_keyup_escape': EventTypes.KEY_UP_ESCAPE,
            'on_keydown_tab': EventTypes.KEY_DOWN_TAB,
            'on_keyup_tab': EventTypes.KEY_UP_TAB,
            'on_keydown_space': EventTypes.KEY_DOWN_SPACE,
            'on_keyup_space': EventTypes.KEY_UP_SPACE,
            'on_keydown_arrow_up': EventTypes.KEY_DOWN_ARROW_UP,
            'on_keydown_arrow_down': EventTypes.KEY_DOWN_ARROW_DOWN,
            'on_keydown_arrow_left': EventTypes.KEY_DOWN_ARROW_LEFT,
            'on_keydown_arrow_right': EventTypes.KEY_DOWN_ARROW_RIGHT,
            'on_keyup_arrow_up': EventTypes.KEY_UP_ARROW_UP,
            'on_keyup_arrow_down': EventTypes.KEY_UP_ARROW_DOWN,
            'on_keyup_arrow_left': EventTypes.KEY_UP_ARROW_LEFT,
            'on_keyup_arrow_right': EventTypes.KEY_UP_ARROW_RIGHT,
            'on_keydown_backspace': EventTypes.KEY_DOWN_BACKSPACE,
            'on_keydown_delete': EventTypes.KEY_DOWN_DELETE,
            'on_keydown_ctrl': EventTypes.KEY_DOWN_CTRL,
            'on_keyup_ctrl': EventTypes.KEY_UP_CTRL,
            'on_keydown_alt': EventTypes.KEY_DOWN_ALT,
            'on_keyup_alt': EventTypes.KEY_UP_ALT,
            'on_keydown_shift': EventTypes.KEY_DOWN_SHIFT,
            'on_keyup_shift': EventTypes.KEY_UP_SHIFT,
            'on_change': EventTypes.CHANGE,
            'on_input': EventTypes.INPUT,
            'on_submit': EventTypes.SUBMIT,
            'on_focus': EventTypes.FOCUS,
            'on_blur': EventTypes.BLUR,
            'on_load': EventTypes.LOAD,
            'on_error': EventTypes.ERROR,
            'on_resize': EventTypes.RESIZE,
        }
        
        event_name = event_map.get(name)
        if event_name and value is not None:
            # Clear existing handlers for this event
            if event_name in self.events:
                self.events[event_name] = []
            
            # Add new handler(s)
            if isinstance(value, (list, tuple)):
                handlers = []
                for handler_item in value:
                    handler = self._normalize_handler(handler_item)
                    if handler:
                        handlers.append(handler)
                if handlers:
                    self.set_event(event_name, handlers)
            else:
                handler = self._normalize_handler(value)
                if handler:
                    self.set_event(event_name, handler)
        
        # Still set the attribute for backward compatibility
        object.__setattr__(self, name, value)
    
    def _normalize_handler(self, handler):
        """Normaliza un handler individual a formato Script"""
        try:
            from dars.scripts.script import Script
            if not isinstance(handler, Script):
                if callable(handler):
                    from dars.scripts.dscript import dScript
                    handler = dScript(handler.__code__)
        except Exception:
            # Best-effort: mantener como está (string o callable)
            pass
        return handler

    def set_event(self, event_name: str, handler):
        """Ahora soporta handler individual o lista de handlers"""
        if event_name not in self.events:
            self.events[event_name] = []
        
        if isinstance(handler, (list, tuple)):
            self.events[event_name].extend(handler)
        else:
            self.events[event_name].append(handler)
        
    def add_child(self, child: 'Component'):
        if isinstance(child, type) and issubclass(child, Component):
            raise TypeError(f"The class {child.__name__} was passed instead of an instance. You should use {child.__name__}(...).")
        child.parent = self
        self.children.append(child)

        
    def find(self, 
             id: Optional[str] = None,
             class_name: Optional[str] = None,
             type: Optional[Union[Type['Component'], str]] = None,
             predicate: Optional[Callable[['Component'], bool]] = None) -> ComponentQuery:
        """Searches for components that match the specified criteria.

            Args:
                id: Search by component ID
                class_name: Search by CSS class name
                type: Search by component type (class or class name)
                predicate: Custom filter function that takes a component and returns bool

            Returns:
                ComponentQuery that allows chaining operations and modifying attributes
        """

        results: List[Component] = []
        
        def match_component(comp: Component) -> bool:
            if id is not None and comp.id != id:
                return False
            if class_name is not None and comp.class_name != class_name:
                return False
            if type is not None:
                if isinstance(type, str):
                    if comp.__class__.__name__ != type:
                        return False
                elif not isinstance(comp, type):
                    return False
            if predicate is not None and not predicate(comp):
                return False
            return True
        
        def search_recursive(component: Component):
            if match_component(component):
                results.append(component)
            for child in component.children:
                search_recursive(child)
        
        search_recursive(self)
        return ComponentQuery(results)

    def attr(self, **attrs) -> Union['Component', dict]:
        """If kwargs are provided, sets attributes on the component (chained setter).  
        If no kwargs are provided, returns a dict with all editable component attributes (getter).  
        Example:
                c.attr(id='new', style={'color': 'red'})
                c.attr()['id']  # getter
        """

        if attrs:
            if 'defer' in attrs:
                try:
                    d = attrs.pop('defer')
                    if d:
                        return DeferredAttr(self, attrs)
                except Exception:
                    pass
            for key, value in attrs.items():
                if key == 'style':
                    if isinstance(value, str):
                        self.style.update(parse_utility_string(value))
                    else:
                        self.style.update(value)
                    continue
                elif key == 'hover_style':
                    if isinstance(value, str):
                        self.hover_style.update(parse_utility_string(value))
                    else:
                        self.hover_style.update(value)
                    continue
                elif key == 'active_style':
                    if isinstance(value, str):
                        self.active_style.update(parse_utility_string(value))
                    else:
                        self.active_style.update(value)
                    continue
                elif key == 'class_name':
                    self.class_name = value
                    continue
                elif key == 'events':
                    self.events.update(value)
                    continue
                # Allow setting on_* event properties via attr()
                if key.startswith('on_') and value is not None:
                    try:
                        event_name = {
                            'on_click': EventTypes.CLICK,
                            'on_double_click': EventTypes.DOUBLE_CLICK,
                            'on_mouse_down': EventTypes.MOUSE_DOWN,
                            'on_mouse_up': EventTypes.MOUSE_UP,
                            'on_mouse_enter': EventTypes.MOUSE_ENTER,
                            'on_mouse_leave': EventTypes.MOUSE_LEAVE,
                            'on_mouse_move': EventTypes.MOUSE_MOVE,
                            'on_key_down': EventTypes.KEY_DOWN,
                            'on_key_up': EventTypes.KEY_UP,
                            'on_key_press': EventTypes.KEY_PRESS,
                            'on_change': EventTypes.CHANGE,
                            'on_input': EventTypes.INPUT,
                            'on_submit': EventTypes.SUBMIT,
                            'on_focus': EventTypes.FOCUS,
                            'on_blur': EventTypes.BLUR,
                            'on_load': EventTypes.LOAD,
                            'on_error': EventTypes.ERROR,
                            'on_resize': EventTypes.RESIZE,
                        }.get(key)
                        if event_name:
                            # Soporte para arrays
                            if isinstance(value, (list, tuple)):
                                handlers = []
                                for handler_item in value:
                                    handler = self._normalize_handler(handler_item)
                                    if handler:
                                        handlers.append(handler)
                                if handlers:
                                    self.set_event(event_name, handlers)
                            else:
                                handler = self._normalize_handler(value)
                                if handler:
                                    self.set_event(event_name, handler)
                            continue
                    except Exception:
                        pass
                if hasattr(self, key):
                    setattr(self, key, value)
                else:
                    self.props[key] = value
            return self
        # Getter: devolver todos los atributos editables
        d = dict(self.props)
        d['id'] = self.id
        d['class_name'] = self.class_name
        d['style'] = self.style
        d['hover_style'] = self.hover_style
        d['active_style'] = self.active_style
        d['events'] = self.events
        return d

    def mod(self, **attrs):
        return DeferredAttr(self, attrs)
    
    def set_loading_state(self, loading_comp: Optional['Component'] = None, 
                          on_error_comp: Optional['Component'] = None) -> 'Component':
        """
        Configure loading and error placeholders for server components.
        
        When use_server=True, the component is rendered by the backend.
        This method allows configuring what to show while loading and on error.
        
        Args:
            loading_comp: Component to show while loading (e.g., Spinner())
            on_error_comp: Component to show if loading fails (e.g., Text("Error"))
            
        Returns:
            self for method chaining
            
        Example:
            chart = Chart(data=data, use_server=True, id="my-chart").set_loading_state(
                loading_comp=Container(Spinner(), Text("Loading chart...")),
                on_error_comp=Text("Failed to load chart", style="color:red")
            )
        """
        if loading_comp is not None:
            self._loading_component = loading_comp
        if on_error_comp is not None:
            self._error_component = on_error_comp
        return self
    
    def render_children(self, exporter: 'Exporter') -> str:
        """Render all children of the component using the exporter."""
        children_html = ""
        for child in self.children:
            children_html += exporter.render_component(child)
        return children_html


class DeferredAttr:
    def __init__(self, component: 'Component', attrs: Dict[str, Any]):
        self.component = component
        self.attrs = attrs or {}

    def clone_with(self) -> 'Component':
        try:
            import copy
            clone = copy.copy(self.component)
        except Exception:
            clone = self.component
        try:
            if hasattr(clone, 'attr') and callable(getattr(clone, 'attr')):
                clone.attr(**self.attrs)
        except Exception:
            pass
        return clone

    def render_children(self, exporter: 'Exporter') -> str:
        """Render all children of the component using the exporter."""
        children_html = ""
        for child in self.children:
            children_html += exporter.render_component(child)
        return children_html
    
    @abstractmethod
    def render(self, exporter: 'Exporter') -> str:
        pass



import inspect

class Props:
    """Helper class with placeholders for Function Components to avoid linter errors."""
    id = "{id}"
    class_name = "{class_name}"
    style = "{style}"
    children = "{children}"
    events = "" # Events are handled separately

def FunctionComponent(func: Callable) -> type:
    """
    Decorator to create a component from a function that returns an f-string template.
    
    You can access framework properties in two ways:
    1. Import `Props` and use `Props.id`, `Props.class_name`, etc.
    2. Declare arguments `id`, `class_name`, `style`, `children` in your function.
    
    Example 1 (Props object):

        @FunctionComponent
        def Card(title, **props):
            return f'''
            <div {Props.id} {Props.class_name} {Props.style}>
                {title}
                {Props.children}
            </div>
            '''
            
    Example 2 (Arguments):
    
        @FunctionComponent
        def Card(title, id, class_name, style, children, **props):
            return f'''
            <div {id} {class_name} {style}>
                {title}
                {children}
            </div>
            '''
    """
    
    # Extract function signature
    sig = inspect.signature(func)
    func_name = func.__name__
    
    # Create dynamic Component subclass
    class DynamicFunctionComponent(Component):
        _template_func = staticmethod(func)
        _func_name = func_name
        _is_function_component = True
        
        def __init__(self, *args, **kwargs):
            # Extract function parameters
            bound_args = sig.bind_partial(*args, **kwargs)
            bound_args.apply_defaults()
            
            # Separate component props from template props
            component_props = {}
            template_props = {}
            
            # Props that belong to the Component base class
            # Note: lifecycle hooks (onMount/onUpdate/onUnmount) are treated as
            # component-level props so they are available in component.props
            # and can be serialized into VDOM lifecycle metadata.
            component_keys = [
                'id', 'class_name', 'style', 'hover_style',
                'active_style', 'key', 'children',
                'onMount', 'onUpdate', 'onUnmount',
            ]
            
            for key, value in kwargs.items():
                if key in component_keys or key.startswith('on_'):
                    component_props[key] = value
                else:
                    template_props[key] = value
            
            # Initialize Component base
            super().__init__(**component_props)
            
            # Prepare arguments for the template function
            # We need to inject placeholders for framework props if they are expected arguments
            
            func_args = bound_args.arguments
            
            # Inject placeholders if arguments exist in signature
            placeholders = {
                'id': '{id}',
                'class_name': '{class_name}',
                'style': '{style}',
                'children': '{children}'
            }
            
            for name, placeholder in placeholders.items():
                if name in sig.parameters:
                    # Only inject if not already provided (though usually they shouldn't be provided manually)
                    if name not in func_args or func_args[name] is None:
                         # We can't modify bound_args easily, so we'll handle it in get_template
                         pass
            
            self.template_props = template_props
            self.template_args = args
            self.template_kwargs = kwargs # Store original kwargs to check for overrides
            
            # Handle children population
            # We need to populate self.children so the exporter can render them
            _children = component_props.get('children')
            
            # If not in component_props (kwargs), check bound arguments if 'children' is a parameter
            if _children is None and 'children' in bound_args.arguments:
                _children = bound_args.arguments['children']
            
            if _children:
                # Import Text to wrap strings if needed
                try:
                    from dars.components.basic.text import Text
                except ImportError:
                    # Fallback if circular import, though unlikely
                    Text = None

                items = _children if isinstance(_children, (list, tuple)) else [_children]
                
                for item in items:
                    if isinstance(item, Component):
                        self.add_child(item)
                    elif isinstance(item, str) and Text:
                        self.add_child(Text(item))
        
        def get_template(self) -> str:
            """Get the template string from the function"""
            
            # Prepare arguments
            # We need to reconstruct the arguments to pass to the function
            # mixing user-provided args and our placeholders
            
            placeholders = {
                'id': '{id}',
                'class_name': '{class_name}',
                'style': '{style}',
                'children': '{children}'
            }
            
            # Get bound arguments again
            bound = sig.bind_partial(*self.template_args, **self.template_props)
            bound.apply_defaults()
            args_dict = bound.arguments
            
            # Inject placeholders for missing arguments that are in signature
            for name, placeholder in placeholders.items():
                if name in sig.parameters:
                    # Always inject placeholder so the function returns a string with {id}
                    # which the exporter will then format.
                    # We override whatever might have been bound (though usually these are consumed by __init__)
                    args_dict[name] = placeholder
            
            # Call function to get template
            template = self._template_func(**args_dict)
            
            # Process DynamicBinding objects
            # Import here to avoid circular dependency
            try:
                from dars.hooks.use_dynamic import DynamicBinding
                
                # Store dynamic bindings for exporter
                if not hasattr(self, '_dynamic_bindings'):
                    self._dynamic_bindings = []
                
                # Find all DynamicBinding markers in the template
                import re
                marker_pattern = r'__DARS_DYNAMIC_\d+_\d+__'
                markers = re.findall(marker_pattern, template)
                
                # Replace markers with reactive span elements
                for marker in markers:
                    # Find the DynamicBinding object (it's in the template string)
                    # We need to track these bindings for the exporter
                    # For now, we'll replace with a data attribute that the exporter can process
                    # The actual state path is embedded in the marker, but we need to extract it
                    # Since we can't easily get the original DynamicBinding object here,
                    # we'll use a different approach: store bindings during function call
                    pass
                
            except ImportError:
                pass
            
            return template
            
        def render(self, exporter) -> str:
            """
            Render the function component using the provided exporter.
            This is required when the component is nested in other components that call .render() on their children.
            """
            if hasattr(exporter, 'render_function_component'):
                return exporter.render_function_component(self)
            return exporter.render_component(self)
    
    # Set class name to function name
    DynamicFunctionComponent.__name__ = func_name
    DynamicFunctionComponent.__qualname__ = func_name
    
    return DynamicFunctionComponent
