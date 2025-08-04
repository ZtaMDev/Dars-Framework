from dars.core.component import Component
from dars.core.properties import StyleProps
from dars.core.events import EventTypes
from typing import Optional, Union, Dict, Any, Callable, List

class SelectOption:
    """Clase para representar una opción del select"""
    def __init__(self, value: str, label: str, disabled: bool = False):
        self.value = value
        self.label = label
        self.disabled = disabled

class Select(Component):
    def __init__(
        self,
        options: List[Union[SelectOption, Dict[str, Any], str]] = None,
        value: Optional[str] = None,
        placeholder: str = "Seleccionar...",
        multiple: bool = False,
        size: Optional[int] = None,
        id: Optional[str] = None,
        class_name: Optional[str] = None,
        style: Optional[Dict[str, Any]] = None,
        disabled: bool = False,
        required: bool = False,
        on_change: Optional[Callable] = None
    ):
        super().__init__(id=id, class_name=class_name, style=style)
        self.options = self._process_options(options or [])
        self.value = value
        self.placeholder = placeholder
        self.multiple = multiple
        self.size = size  # Número de opciones visibles (para select múltiple)
        self.disabled = disabled
        self.required = required
        
        # Registrar evento de cambio si se proporciona
        if on_change:
            self.set_event(EventTypes.CHANGE, on_change)
    
    def _process_options(self, options: List[Union[SelectOption, Dict[str, Any], str]]) -> List[SelectOption]:
        """Procesa las opciones y las convierte a objetos SelectOption"""
        processed_options = []
        
        for option in options:
            if isinstance(option, SelectOption):
                processed_options.append(option)
            elif isinstance(option, dict):
                processed_options.append(SelectOption(
                    value=option.get('value', ''),
                    label=option.get('label', option.get('value', '')),
                    disabled=option.get('disabled', False)
                ))
            elif isinstance(option, str):
                processed_options.append(SelectOption(value=option, label=option))
        
        return processed_options
    
    def add_option(self, value: str, label: str = None, disabled: bool = False):
        """Añade una nueva opción al select"""
        self.options.append(SelectOption(
            value=value,
            label=label or value,
            disabled=disabled
        ))
    
    def remove_option(self, value: str):
        """Elimina una opción por su valor"""
        self.options = [opt for opt in self.options if opt.value != value]
    
    def get_selected_option(self) -> Optional[SelectOption]:
        """Obtiene la opción seleccionada actualmente"""
        if self.value:
            for option in self.options:
                if option.value == self.value:
                    return option
        return None

    def render(self, exporter: Any) -> str:
        # El método render será implementado por cada exportador
        raise NotImplementedError("El método render debe ser implementado por el exportador")
