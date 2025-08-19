from dars.core.component import Component
from typing import Optional, Dict, Any, List

class Modal(Component):
    """Componente para mostrar contenido en un modal."""
    def __init__(
        self,
        children: Optional[List[Component]] = None,
        title: Optional[str] = None,
        is_open: bool = False,
        class_name: Optional[str] = None,
        style: Optional[Dict[str, Any]] = None,
        minimum_logic: bool = True,
        **kwargs
    ):
        super().__init__(class_name=class_name, style=style, **kwargs)
        self.title = title
        self.is_open = is_open
        self.minimum_logic = minimum_logic
        if children:
            for child in children:
                self.add_child(child)

    def render(self) -> str:
        title_html = f'<h2>{self.title}</h2>' if self.title else ''
        children_html = ''.join([child.render() for child in self.children])
        
        display_style = 'display: flex' if self.is_open else 'display: none'
        
        attrs = []
        if self.class_name: attrs.append(f'class="dars-modal {self.class_name}"')
        else: attrs.append('class="dars-modal"')
        
        modal_style = f'{display_style}; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background-color: rgba(0,0,0,0.5); justify-content: center; align-items: center; z-index: 1000'
        if self.style:
            modal_style += f'; {self.render_styles(self.style)}'
        attrs.append(f'style="{modal_style}"')
        
        return f'''<div {" ".join(attrs)}>
            <div class="dars-modal-content" style="background: white; padding: 20px; border-radius: 8px; max-width: 500px; width: 90%;">
                {title_html}
                {children_html}
            </div>
        </div>'''

