from dars.core.component import Component
from dars.core.properties import StyleProps
from dars.core.events import EventTypes
from typing import Optional, Union, Dict, Any, Callable

class RadioButton(Component):
    def __init__(
        self,
        label: str = "",
        value: str = "",
        name: str = "radio_group",
        checked: bool = False,
        id: Optional[str] = None,
        class_name: Optional[str] = None,
        style: Optional[Dict[str, Any]] = None,
        disabled: bool = False,
        required: bool = False,
        on_change: Optional[Callable] = None
    ):
        super().__init__(id=id, class_name=class_name, style=style)
        self.label = label
        self.value = value or label  # Si no se proporciona value, usar label
        self.name = name  # Requerido para agrupar radio buttons
        self.checked = checked
        self.disabled = disabled
        self.required = required
        
        # Registrar evento de cambio si se proporciona
        if on_change:
            self.set_event(EventTypes.CHANGE, on_change)

    def render(self, exporter: Any) -> str:
        # El método render será implementado por cada exportador
        raise NotImplementedError("El método render debe ser implementado por el exportador")
