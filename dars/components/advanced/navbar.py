from dars.core.component import Component
from typing import Optional, Dict, Any, List

class Navbar(Component):
    """Componente para crear barras de navegación."""
    def __init__(
        self,
        children: Optional[List[Component]] = None,
        brand: Optional[str] = None,
        class_name: Optional[str] = None,
        style: Optional[Dict[str, Any]] = None,
        **kwargs
    ):
        super().__init__(children=children, class_name=class_name, style=style, **kwargs)
        self.brand = brand

    def render(self) -> str:
        brand_html = f'<div class="dars-navbar-brand">{self.brand}</div>' if self.brand else ''
        children_html = ''.join([child.render() for child in self.children])
        
        attrs = []
        if self.class_name: attrs.append(f'class="dars-navbar {self.class_name}"')
        else: attrs.append('class="dars-navbar"')
        
        navbar_style = 'display: flex; justify-content: space-between; align-items: center; padding: 1rem; background-color: #f8f9fa; border-bottom: 1px solid #dee2e6'
        if self.style:
            navbar_style += f'; {self.render_styles(self.style)}'
        attrs.append(f'style="{navbar_style}"')
        
        return f'<nav {" ".join(attrs)}>{brand_html}<div class="dars-navbar-nav">{children_html}</div></nav>'

