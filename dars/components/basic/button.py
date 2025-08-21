from dars.core.component import Component
from dars.core.properties import StyleProps
from dars.core.events import EventTypes
from dars.scripts.script import Script
from typing import Optional, Union, Dict, Any, Callable

class Button(Component):
    def __init__(
        self, 
        text: str = "Button", 
        id: Optional[str] = None, 
        class_name: Optional[str] = None, 
        style: Optional[Dict[str, Any]] = None,
        disabled: bool = False,
        button_type: str = "button",  # "button", "submit", "reset"
        on_click: Optional[Callable] = None,
        on_double_click: Optional[Callable] = None,
        on_mouse_enter: Optional[Callable] = None,
        on_mouse_leave: Optional[Callable] = None,
        on_mouse_down: Optional[Callable] = None,
        on_mouse_up: Optional[Callable] = None,
        on_key_down: Optional[Callable] = None,
        on_key_up: Optional[Callable] = None
    ):
        super().__init__(id=id, class_name=class_name, style=style)
        self.text = text
        self.disabled = disabled
        self.button_type = button_type
        
        # Soporte para presets JS editables con dScript u otros Script
        if on_click:
            # Convertir a Script si es necesario
            if not isinstance(on_click, Script) and callable(on_click):
                from dars.scripts.dscript import dScript
                on_click = dScript(on_click.__code__)
            self.set_event(EventTypes.CLICK, on_click)
        if on_double_click:
            self.set_event(EventTypes.DOUBLE_CLICK, on_double_click)
        if on_mouse_enter:
            self.set_event(EventTypes.MOUSE_ENTER, on_mouse_enter)
        if on_mouse_leave:
            self.set_event(EventTypes.MOUSE_LEAVE, on_mouse_leave)
        if on_mouse_down:
            self.set_event(EventTypes.MOUSE_DOWN, on_mouse_down)
        if on_mouse_up:
            self.set_event(EventTypes.MOUSE_UP, on_mouse_up)
        if on_key_down:
            self.set_event(EventTypes.KEY_DOWN, on_key_down)
        if on_key_up:
            self.set_event(EventTypes.KEY_UP, on_key_up)

    def render(self, exporter: Any) -> str:
        # El método render será implementado por cada exportador
        raise NotImplementedError("El método render debe ser implementado por el exportador")

