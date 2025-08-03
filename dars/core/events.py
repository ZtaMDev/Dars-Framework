from typing import Callable, Dict, Any, Optional
from abc import ABC, abstractmethod

class EventHandler:
    """Manejador de eventos para componentes"""
    
    def __init__(self, handler: Callable, event_type: str):
        self.handler = handler
        self.event_type = event_type
        self.id = f"event_{id(self)}"
    
    def __call__(self, *args, **kwargs):
        return self.handler(*args, **kwargs)

class EventManager:
    """Gestor de eventos para la aplicación"""
    
    def __init__(self):
        self.handlers: Dict[str, EventHandler] = {}
        self.component_events: Dict[str, Dict[str, EventHandler]] = {}
    
    def register_event(self, component_id: str, event_type: str, handler: Callable) -> str:
        """Registra un evento para un componente"""
        event_handler = EventHandler(handler, event_type)
        
        if component_id not in self.component_events:
            self.component_events[component_id] = {}
        
        self.component_events[component_id][event_type] = event_handler
        self.handlers[event_handler.id] = event_handler
        
        return event_handler.id
    
    def get_event_handler(self, handler_id: str) -> Optional[EventHandler]:
        """Obtiene un manejador de eventos por su ID"""
        return self.handlers.get(handler_id)
    
    def get_component_events(self, component_id: str) -> Dict[str, EventHandler]:
        """Obtiene todos los eventos de un componente"""
        return self.component_events.get(component_id, {})
    
    def remove_event(self, component_id: str, event_type: str):
        """Elimina un evento de un componente"""
        if component_id in self.component_events:
            if event_type in self.component_events[component_id]:
                handler = self.component_events[component_id][event_type]
                del self.handlers[handler.id]
                del self.component_events[component_id][event_type]

class EventEmitter(ABC):
    """Clase base para componentes que pueden emitir eventos"""
    
    def __init__(self):
        self.event_manager = EventManager()
    
    def on(self, event_type: str, handler: Callable) -> str:
        """Registra un manejador de eventos"""
        component_id = getattr(self, 'id', str(id(self)))
        return self.event_manager.register_event(component_id, event_type, handler)
    
    def off(self, event_type: str):
        """Elimina un manejador de eventos"""
        component_id = getattr(self, 'id', str(id(self)))
        self.event_manager.remove_event(component_id, event_type)
    
    @abstractmethod
    def emit(self, event_type: str, *args, **kwargs):
        """Emite un evento"""
        pass

# Tipos de eventos estándar
class EventTypes:
    # Eventos de mouse
    CLICK = "click"
    DOUBLE_CLICK = "dblclick"
    MOUSE_DOWN = "mousedown"
    MOUSE_UP = "mouseup"
    MOUSE_ENTER = "mouseenter"
    MOUSE_LEAVE = "mouseleave"
    MOUSE_MOVE = "mousemove"
    
    # Eventos de teclado
    KEY_DOWN = "keydown"
    KEY_UP = "keyup"
    KEY_PRESS = "keypress"
    
    # Eventos de formulario
    CHANGE = "change"
    INPUT = "input"
    SUBMIT = "submit"
    FOCUS = "focus"
    BLUR = "blur"
    
    # Eventos de carga
    LOAD = "load"
    ERROR = "error"
    RESIZE = "resize"
    
    # Eventos personalizados
    CUSTOM = "custom"

