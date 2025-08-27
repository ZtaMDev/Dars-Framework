from typing import Dict, Any, List, Optional, Callable, Union, Type
from abc import ABC, abstractmethod

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
        self.class_name: Optional[str] = props.get('class_name')
        self.style: Dict[str, Any] = props.get('style', {})
        self.events: Dict[str, Callable] = {}
        
    def add_child(self, child: 'Component'):
        child.parent = self
        self.children.append(child)
        
    def set_event(self, event_name: str, handler: Callable):
        self.events[event_name] = handler
        
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
            for key, value in attrs.items():
                if key == 'style':
                    self.style.update(value)
                    continue
                elif key == 'class_name':
                    self.class_name = value
                    continue
                elif key == 'events':
                    self.events.update(value)
                    continue
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
        d['events'] = self.events
        return d

    def render_children(self, exporter: 'Exporter') -> str:
        """Render all children of the component using the exporter."""
        children_html = ""
        for child in self.children:
            children_html += exporter.render_component(child)
        return children_html
    
    @abstractmethod
    def render(self, exporter: 'Exporter') -> str:
        pass


