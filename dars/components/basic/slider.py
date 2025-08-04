from dars.core.component import Component
from dars.core.properties import StyleProps
from dars.core.events import EventTypes
from typing import Optional, Union, Dict, Any, Callable

class Slider(Component):
    def __init__(
        self,
        min_value: Union[int, float] = 0,
        max_value: Union[int, float] = 100,
        value: Union[int, float] = 50,
        step: Union[int, float] = 1,
        label: str = "",
        show_value: bool = True,
        orientation: str = "horizontal",  # "horizontal" o "vertical"
        id: Optional[str] = None,
        class_name: Optional[str] = None,
        style: Optional[Dict[str, Any]] = None,
        disabled: bool = False,
        on_change: Optional[Callable] = None,
        on_input: Optional[Callable] = None
    ):
        super().__init__(id=id, class_name=class_name, style=style)
        self.min_value = min_value
        self.max_value = max_value
        self.value = max(min_value, min(max_value, value))  # Asegurar que esté en rango
        self.step = step
        self.label = label
        self.show_value = show_value
        self.orientation = orientation
        self.disabled = disabled
        
        # Validar orientación
        if orientation not in ["horizontal", "vertical"]:
            raise ValueError("orientation debe ser 'horizontal' o 'vertical'")
        
        # Registrar eventos si se proporcionan
        if on_change:
            self.set_event(EventTypes.CHANGE, on_change)
        if on_input:
            self.set_event(EventTypes.INPUT, on_input)
    
    def set_value(self, value: Union[int, float]):
        """Establece el valor del slider asegurando que esté en rango"""
        self.value = max(self.min_value, min(self.max_value, value))
    
    def get_percentage(self) -> float:
        """Obtiene el porcentaje actual del slider (0-100)"""
        if self.max_value == self.min_value:
            return 0
        return ((self.value - self.min_value) / (self.max_value - self.min_value)) * 100
    
    def is_at_min(self) -> bool:
        """Verifica si el slider está en su valor mínimo"""
        return self.value == self.min_value
    
    def is_at_max(self) -> bool:
        """Verifica si el slider está en su valor máximo"""
        return self.value == self.max_value

    def render(self, exporter: Any) -> str:
        # El método render será implementado por cada exportador
        raise NotImplementedError("El método render debe ser implementado por el exportador")
