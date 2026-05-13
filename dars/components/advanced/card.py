from dars.core.component import Component
from typing import Optional, Dict, Any, List

class Card(Component):
    """
    Card component for grouping related information in a visually distinct container.
    
    Props:
    - **children** (list): List of child components to render inside the card.
    - **title** (str): Optional title displayed at the top of the card.
    - **id** (str): Unique identifier for the component.
    - **class_name** (str): String containing CSS utility classes (e.g., `"p-6 bg-white rounded-2xl shadow-xl hover:shadow-2xl transition-shadow"`).
    - **style** (dict): Optional dictionary for direct inline styles (prefer `class_name`).
    - **Events**: Handlers like `on_click`, `on_mouse_enter`, etc.
    
    Example:
    ```python
    Card(
        Text("Card content goes here..."),
        title="Featured Post",
        class_name="max-w-sm border border-slate-100 bg-gradient-to-br from-white to-slate-50"
    )
    ```
    """
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
        
        if self.id:
            attrs.append(f'id="{self.id}"')
        
        return f'<div {" ".join(attrs)}>{title_html}{children_html}</div>'


