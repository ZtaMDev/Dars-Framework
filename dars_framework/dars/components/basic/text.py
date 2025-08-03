from dars.core.component import Component
from dars.core.properties import StyleProps
from typing import Optional, Union, Dict, Any

class Text(Component):
    def __init__(
        self, 
        text: str = "", 
        id: Optional[str] = None, 
        class_name: Optional[str] = None, 
        style: Optional[Dict[str, Any]] = None
    ):
        super().__init__(id=id, class_name=class_name, style=style)
        self.text = text

    def render(self, exporter: Any) -> str:
        # El método render será implementado por cada exportador
        # para generar el código específico de la plataforma.
        # Por ahora, solo definimos la interfaz.
        raise NotImplementedError("El método render debe ser implementado por el exportador")


