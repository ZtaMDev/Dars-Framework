from dars.core.component import Component
from typing import Optional, Dict, Any, List

class Navbar(Component):
    """
    Navigation bar component for page headers, supporting branding and navigation links.
    
    Props:
    - ***children** (Component): Positional arguments for navigation links or other components.
    - **brand** (str): Text or logo component for the site branding area.
    - **id** (str): Unique identifier for the component.
    - **class_name** (str): String containing regular CSS class names.
    - **style** (dict): Optional dictionary for CSS utility classes (prefer `style`).
    - **children** (list): List of child components.
    - **Events**: Handlers like `on_click`, `on_mouse_enter`, etc.
    
    Example:
    ```python
    Navbar(
        Link("Home", href="/", class_name="px-4 py-2 hover:text-indigo-600"),
        Link("Services", href="/services", class_name="px-4 py-2 hover:text-indigo-600"),
        brand="Dars Framework",
        class_name="px-8 py-4 shadow-sm flex items-center justify-between"
    )
    ```
    """
    def __init__(
        self,
        *children,
        brand: Optional[str] = None,
        class_name: Optional[str] = None,
        style: Optional[Dict[str, Any]] = None,
        **kwargs
    ):
        # Compatibilidad retro: si 'children' está en kwargs, lo usamos; si no, usamos los posicionales
        children_kwarg = kwargs.pop('children', None)
        from dars.core.component import Component
        if children_kwarg is not None:
            children_final = children_kwarg
        elif len(children) == 1 and isinstance(children[0], list):
            children_final = children[0]
        else:
            children_final = list(children)
        # Filtro: solo instancias válidas de Component
        children_final = [c for c in children_final if isinstance(c, Component)]
        super().__init__(class_name=class_name, style=style, **kwargs)
        self.brand = brand
        for child in children_final:
            self.add_child(child)

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
        
        if self.id:
            attrs.append(f'id="{self.id}"')
        
        return f'<nav {" ".join(attrs)}>{brand_html}<div class="dars-navbar-nav">{children_html}</div></nav>'

