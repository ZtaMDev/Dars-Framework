from dars.core.component import Component
from dars.core.properties import StyleProps
from typing import Optional, Union, Dict, Any, List

class Container(Component):
    """
    Versatile container component (div) to wrap and organize other components.
    
    Props:
    - ***children** (Component): Positional arguments for child components.
    - **additional_children** (list): Optional list of additional child components.
    - **id** (str): Unique identifier for the component.
    - **class_name** (str): String containing regular CSS class names.
    - **style** (dict): Optional dictionary for CSS utility classes (prefer `style`).
    - **Events**: Handlers like `on_click`, `on_mouse_enter`, etc.
    
    Example:
    ```python
    Container(
        Text("Title"),
        Button("Click me"),
        class_name="flex flex-col gap-4 p-6 bg-slate-50 rounded-2xl"
    )
    ```
    """
    def __init__(
        self,
        *children: Component,
        id: Any = None, 
        class_name: Any = None, 
        style: Optional[Dict[str, Any] | str] = None,
        additional_children: Optional[List[Component]] = None,
        **props
    ):
        super().__init__(id=id, class_name=class_name, style=style, **props)
        
        # Agregar hijos pasados como argumentos posicionales
        for child in children:
            self.add_child(child)
            
        # Agregar hijos adicionales si se proporcionan
        if additional_children:
            for child in additional_children:
                self.add_child(child)

    def render(self, exporter: Any) -> str:
        # El metodo render será implementado por cada exportador
        raise NotImplementedError("El método render debe ser implementado por el exportador")

