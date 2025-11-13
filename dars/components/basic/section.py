from typing import Optional, Dict, Any, List

from dars.core.component import Component

class Section(Component):
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

