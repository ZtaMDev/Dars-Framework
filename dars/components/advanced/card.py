from dars.core.component import Component
from typing import Optional, Dict, Any, List

class Card(Component):
    """Componente para mostrar contenido en una tarjeta."""
    def __init__(
        self,
        children: Optional[List[Component]] = None,
        title: Optional[str] = None,
        class_name: Optional[str] = None,
        style: Optional[Dict[str, Any]] = None,
        minimum_logic: bool = True,
        **kwargs
    ):
        super().__init__(class_name=class_name, style=style, **kwargs)
        self.title = title
        self.minimum_logic = minimum_logic
        if children:
            for child in children:
                self.add_child(child)

    def render(self) -> str:
        title_html = f'<h2>{self.title}</h2>' if self.title else ''
        children_html = ''.join([child.render() for child in self.children])
        
        attrs = []
        if self.class_name: attrs.append(f'class="dars-card {self.class_name}"')
        else: attrs.append('class="dars-card"')
        if self.style: attrs.append(f'style="{self.render_styles(self.style)}"')
        
        return f'<div {" ".join(attrs)}>{title_html}{children_html}</div>'


