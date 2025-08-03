from dars.core.component import Component
from dars.core.properties import StyleProps
from dars.core.events import EventTypes
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
        on_click: Optional[Callable] = None
    ):
        super().__init__(id=id, class_name=class_name, style=style)
        self.text = text
        self.disabled = disabled
        self.button_type = button_type
        
        # Registrar evento de click si se proporciona
        if on_click:
            self.set_event(EventTypes.CLICK, on_click)

    def render(self, exporter: Any) -> str:
        # El método render será implementado por cada exportador
        raise NotImplementedError("El método render debe ser implementado por el exportador")

