from typing import Dict, Any, List, Optional, Callable
from abc import ABC, abstractmethod

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
        
    @abstractmethod
    def render(self, exporter: 'Exporter') -> str:
        pass


