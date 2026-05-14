from typing import Optional, Dict, Any, List

from dars.core.component import Component

class Section(Component):
    """
    Semantic section component (`<section>`) for grouping related content and defining page structure.
    
    Props:
    - ***children** (Component): Positional arguments for child components.
    - **additional_children** (list): Optional list of additional child components.
    - **id** (str): Unique identifier for the component.
    - **class_name** (str): String containing regular CSS class names.
    - **style** (dict): Optional dictionary for CSS utility classes (prefer `style`).
    - **Events**: Handlers like `on_click`, `on_mouse_enter`, etc.
    
    Example:
    ```python
    Section(
        Text("Our Services", class_name="text-3xl font-bold mb-8 text-center"),
        Container(class_name="grid grid-cols-1 md:grid-cols-3 gap-8"),
        class_name="container mx-auto px-4 py-16"
    )
    ```
    """
    def __init__(
        self,
        *children: Component,
        id: Optional[str] = None, 
        class_name: Optional[str] = None, 
        style: Optional[Dict[str, Any]] = None,
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

