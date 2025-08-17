from dars.core.component import Component
from dars.core.properties import StyleProps
from typing import Optional, Union, Dict, Any, List

class Container(Component):
    def __init__(
        self,
        *children: Component,
        id: Optional[str] = None, 
        class_name: Optional[str] = None, 
        style: Optional[Dict[str, Any]] = None,
        additional_children: Optional[List[Component]] = None
    ):
        super().__init__(id=id, class_name=class_name, style=style)
        
        # Agregar hijos pasados como argumentos posicionales
        for child in children:
            self.add_child(child)
            
        # Agregar hijos adicionales si se proporcionan
        if additional_children:
            for child in additional_children:
                self.add_child(child)

    def render(self, exporter: Any) -> str:
        # El método render será implementado por cada exportador
        raise NotImplementedError("El método render debe ser implementado por el exportador")

