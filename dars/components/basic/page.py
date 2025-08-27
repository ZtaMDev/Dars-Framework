from dars.core.component import Component
from typing import Optional, Dict, Any, List

class Page(Component):
    """Root component for pages in Dars multipage apps. Allows passing children as positional arguments and scripts per page."""
    def __init__(self, *children: Component, id: Optional[str] = None, class_name: Optional[str] = None, style: Optional[Dict[str, Any]] = None):
        super().__init__(id=id, class_name=class_name, style=style)
        self.scripts = []
        for child in children:
            self.add_child(child)

    def add_script(self, script):
        self.scripts.append(script)

    def get_scripts(self):
        return self.scripts

    def render(self, exporter: Any) -> str:
        # El método render será implementado por el exporter
        raise NotImplementedError("El método render debe ser implementado por el exporter")
