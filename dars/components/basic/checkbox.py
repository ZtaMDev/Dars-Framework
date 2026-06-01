from dars.core.component import Component
from dars.core.properties import StyleProps
from dars.core.events import EventTypes
from typing import Optional, Union, Dict, Any, Callable

class Checkbox(Component):
    """
    Interactive checkbox component for boolean input.
    
    Props:
    - **label** (str): Text label to display next to the checkbox.
    - **checked** (bool): Current state of the checkbox.
    - **value** (str): Value associated with the checkbox.
    - **name** (str): Name attribute for form submission.
    - **disabled** (bool): If True, the checkbox is not interactive.
    - **required** (bool): If True, the checkbox must be checked.
    - **id** (str): Unique identifier for the component.
    - **class_name** (str): String containing regular CSS class names.
    - **style** (dict): Optional dictionary for CSS utility classes (prefer `style`).
    - **children** (list): List of child components.
    - **Events**: Handlers like `on_change`, `on_click`, etc.
    
    Example:
    ```python
    Checkbox(
        label="Accept terms and conditions",
        on_change=lambda val: print(f"Checked: {val}"),
        class_name="text-slate-700 font-medium cursor-pointer"
    )
    ```
    """
    def __init__(
        self,
        label: Any = "",
        checked: bool = False,
        value: Any = "",
        name: Any = None,
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
        self.checked = checked
        self.value = value or label  # Si no se proporciona value, usar label
        self.name = name
        self.disabled = disabled
        self.required = required
        
        # Registrar evento de cambio si se proporciona
        if on_change:
            self.set_event(EventTypes.CHANGE, on_change)

    def render(self, exporter: Any) -> str:
        # El método render será implementado por cada exportador
        raise NotImplementedError("El método render debe ser implementado por el exportador")
