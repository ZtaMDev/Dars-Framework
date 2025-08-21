from dars.core.component import Component
from dars.core.properties import StyleProps
from dars.core.events import EventTypes
from typing import Optional, Union, Dict, Any, Callable

class Input(Component):
    def __init__(
        self, 
        value: str = "", 
        placeholder: str = "",
        input_type: str = "text",  # "text", "password", "email", "number", etc.
        id: Optional[str] = None, 
        class_name: Optional[str] = None, 
        style: Optional[Dict[str, Any]] = None,
        disabled: bool = False,
        readonly: bool = False,
        required: bool = False,
        max_length: Optional[int] = None,
        min_length: Optional[int] = None,
        pattern: Optional[str] = None,
        on_change: Optional[Callable] = None,
        on_input: Optional[Callable] = None,
        on_focus: Optional[Callable] = None,
        on_blur: Optional[Callable] = None,
        on_key_down: Optional[Callable] = None,
        on_key_up: Optional[Callable] = None
    ):
        super().__init__(id=id, class_name=class_name, style=style)
        self.value = value
        self.placeholder = placeholder
        self.input_type = input_type
        self.disabled = disabled
        self.readonly = readonly
        self.required = required
        self.max_length = max_length
        self.min_length = min_length
        self.pattern = pattern
        
        # Soporte para presets JS editables con dScript u otros Script
        if on_change:
            self.set_event(EventTypes.CHANGE, on_change)
        if on_input:
            self.set_event(EventTypes.INPUT, on_input)
        if on_focus:
            self.set_event(EventTypes.FOCUS, on_focus)
        if on_blur:
            self.set_event(EventTypes.BLUR, on_blur)
        if on_key_down:
            self.set_event(EventTypes.KEY_DOWN, on_key_down)
        if on_key_up:
            self.set_event(EventTypes.KEY_UP, on_key_up)

    def render(self, exporter: Any) -> str:
        # El método render será implementado por cada exportador
        raise NotImplementedError("El método render debe ser implementado por el exportador")

