
from dars.core.component import Component
from dars.core.events import EventTypes
from typing import Optional, Dict, Any, Callable, Union

class FileUpload(Component):
    def __init__(
        self,
        accept: Optional[str] = None,
        multiple: bool = False,
        disabled: bool = False,
        required: bool = False,
        max_size: Optional[int] = None,  # In bytes
        id: Optional[str] = None,
        class_name: Optional[str] = None,
        style: Optional[Dict[str, Any]] = None,
        on_change: Optional[Callable] = None,
        label: Optional[str] = "Choose File",
        **props
    ):
        super().__init__(id=id, class_name=class_name, style=style, **props)
        self.accept = accept
        self.multiple = multiple
        self.disabled = disabled
        self.required = required
        self.max_size = max_size
        self.label = label
        
        if on_change:
            self.set_event(EventTypes.CHANGE, on_change)

    def render(self, exporter: Any) -> str:
        raise NotImplementedError("render method must be implemented by exporter")
