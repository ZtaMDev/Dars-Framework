from dars.core.component import Component
from dars.core.properties import StyleProps
from dars.core.events import EventTypes
from typing import Optional, Union, Dict, Any, Callable

class RadioButton(Component):
    """
    Radio button component for selecting one option from a group.
    
    Props:
    - **label** (str): Text label to display next to the radio button.
    - **value** (str): Value associated with the radio button.
    - **name** (str): Name of the radio group (used to link related buttons).
    - **checked** (bool): Current state of the radio button.
    - **disabled** (bool): If True, the radio button is not interactive.
    - **required** (bool): If True, the radio button must be selected.
    - **id** (str): Unique identifier for the component.
    - **class_name** (str): String containing regular CSS class names.
    - **style** (dict): Optional dictionary for CSS utility classes (prefer `style`).
    - **children** (list): List of child components.
    - **Events**: Handlers like `on_change`, `on_click`, etc.
    
    Example:
    ```python
    RadioButton(
        label="Option A",
        name="my-group",
        value="a",
        checked=True,
        class_name="text-indigo-600 focus:ring-indigo-500"
    )
    ```
    """
    def __init__(
        self,
        label: Any = "",
        value: Any = "",
        name: Any = "radio_group",
        checked: bool = False,
        id: Any = None,
        class_name: Any = None,
        style: Optional[Dict[str, Any] | str] = None,
        disabled: bool = False,
        required: bool = False,
        on_change: Optional[Callable] = None,
        **props
    ):
        super().__init__(id=id, class_name=class_name, style=style, **props)
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
