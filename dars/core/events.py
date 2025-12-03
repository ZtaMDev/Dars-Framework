# Dars Framework - Core Source File
#
# This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0.
# If a copy of the MPL was not distributed with this file, You can obtain one at
# https://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2025 ZtaDev
from typing import Callable, Dict, Any, Optional
from abc import ABC, abstractmethod

class EventHandler:
    """Event handler for components"""
    
    def __init__(self, handler: Callable, event_type: str):
        self.handler = handler
        self.event_type = event_type
        self.id = f"event_{id(self)}"
    
    def __call__(self, *args, **kwargs):
        return self.handler(*args, **kwargs)

class EventManager:
    """Event manager for the application"""
    
    def __init__(self):
        self.handlers: Dict[str, EventHandler] = {}
        self.component_events: Dict[str, Dict[str, EventHandler]] = {}
    
    def register_event(self, component_id: str, event_type: str, handler: Callable) -> str:
        """Registers an event for a component"""
        event_handler = EventHandler(handler, event_type)
        
        if component_id not in self.component_events:
            self.component_events[component_id] = {}
        
        self.component_events[component_id][event_type] = event_handler
        self.handlers[event_handler.id] = event_handler
        
        return event_handler.id
    
    def get_event_handler(self, handler_id: str) -> Optional[EventHandler]:
        """Gets all events of a component by ID"""

        return self.handlers.get(handler_id)
    
    def get_component_events(self, component_id: str) -> Dict[str, EventHandler]:
        """Gets all events of a component"""
        return self.component_events.get(component_id, {})
    
    def remove_event(self, component_id: str, event_type: str):
        """Removes an event from a component"""
        if component_id in self.component_events:
            if event_type in self.component_events[component_id]:
                handler = self.component_events[component_id][event_type]
                del self.handlers[handler.id]
                del self.component_events[component_id][event_type]

class EventEmitter(ABC):
    """Base class for components that can emit events"""
    
    def __init__(self):
        self.event_manager = EventManager()
    
    def on(self, event_type: str, handler: Callable) -> str:
        """Registers an event handler"""
        component_id = getattr(self, 'id', str(id(self)))
        return self.event_manager.register_event(component_id, event_type, handler)
    
    def off(self, event_type: str):
        """Removes an event handler"""
        component_id = getattr(self, 'id', str(id(self)))
        self.event_manager.remove_event(component_id, event_type)
    
    @abstractmethod
    def emit(self, event_type: str, *args, **kwargs):
        """Emits an event"""
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
    
    # Eventos de teclado específicos (key-filtered)
    # Enter
    KEY_DOWN_ENTER = "keydown.Enter"
    KEY_UP_ENTER = "keyup.Enter"
    KEY_PRESS_ENTER = "keypress.Enter"
    
    # Escape
    KEY_DOWN_ESCAPE = "keydown.Escape"
    KEY_UP_ESCAPE = "keyup.Escape"
    
    # Tab
    KEY_DOWN_TAB = "keydown.Tab"
    KEY_UP_TAB = "keyup.Tab"
    
    # Space
    KEY_DOWN_SPACE = "keydown.Space"
    KEY_UP_SPACE = "keyup.Space"
    
    # Arrows
    KEY_DOWN_ARROW_UP = "keydown.ArrowUp"
    KEY_DOWN_ARROW_DOWN = "keydown.ArrowDown"
    KEY_DOWN_ARROW_LEFT = "keydown.ArrowLeft"
    KEY_DOWN_ARROW_RIGHT = "keydown.ArrowRight"
    KEY_UP_ARROW_UP = "keyup.ArrowUp"
    KEY_UP_ARROW_DOWN = "keyup.ArrowDown"
    KEY_UP_ARROW_LEFT = "keyup.ArrowLeft"
    KEY_UP_ARROW_RIGHT = "keyup.ArrowRight"
    
    # Backspace and Delete
    KEY_DOWN_BACKSPACE = "keydown.Backspace"
    KEY_DOWN_DELETE = "keydown.Delete"
    
    # Control keys
    KEY_DOWN_CTRL = "keydown.Control"
    KEY_UP_CTRL = "keyup.Control"
    KEY_DOWN_ALT = "keydown.Alt"
    KEY_UP_ALT = "keyup.Alt"
    KEY_DOWN_SHIFT = "keydown.Shift"
    KEY_UP_SHIFT = "keyup.Shift"
    
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

