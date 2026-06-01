from dars.core.component import Component
from dars.core.properties import StyleProps
from typing import Optional, Union, Dict, Any

class Text(Component):
    """
    Component for displaying text content.
    
    Props:
    - **text** (str): The text content to display.
    - **id** (str): Unique identifier for the component.
    - **class_name** (str): String containing regular CSS class names.
    - **style** (dict): Optional dictionary for CSS utility classes (prefer `style`).
    - **children** (list): List of child components.
    - **Events**: Handlers like `on_click`, `on_mouse_enter`, etc.
    
    Example:
    ```python
    Text("Welcome to Dars!", class_name="text-4xl font-extrabold text-indigo-600 mb-4")
    ```
    """
    def __init__(
        self, 
        text: Any = "", 
        id: Any = None, 
        class_name: Any = None, 
        style: Optional[Dict[str, Any] | str] = None,
        **props
    ):
        super().__init__(id=id, class_name=class_name, style=style, **props)
        self.text = text

    def render(self, exporter: Any) -> str:
        # El método render será implementado por cada exportador
        # para generar el código específico de la plataforma.
        raise NotImplementedError("El método render debe ser implementado por el exportador")


