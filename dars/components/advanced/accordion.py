from dars.core.component import Component
from typing import List, Optional

class Accordion(Component):
    """
    Accordion component for displaying collapsible content sections.
    
    Props:
    - **sections** (list): List of tuples containing `(title, content)`.
    - **open_indices** (list): Optional list of indices that should be open by default.
    - **id** (str): Unique identifier for the component.
    - **class_name** (str): String containing CSS utility classes (e.g., `"divide-y divide-slate-200 border rounded-xl overflow-hidden"`).
    - **style** (dict): Optional dictionary for direct inline styles (prefer `class_name`).
    - **children** (list): List of child components.
    - **Events**: Handlers like `on_click`, etc.
    
    Example:
    ```python
    Accordion(
        sections=[
            ("Section 1", Text("Content for section 1")),
            ("Section 2", Text("Content for section 2")),
        ],
        open_indices=[0],
        class_name="bg-white shadow-sm"
    )
    ```
    """

    def __init__(self, sections: List[tuple], open_indices: Optional[List[int]]=None, minimum_logic: bool = True, **props):
        super().__init__(**props)
        self.sections = sections
        self.open_indices = open_indices or []
        self.minimum_logic = minimum_logic
        for _, content in sections:
            if hasattr(content, 'render'):
                self.add_child(content)

    def render(self) -> str:
        html = '<div class="dars-accordion">'
        for i, (title, content) in enumerate(self.sections):
            opened = ' dars-accordion-open' if i in self.open_indices else ''
            html += f'<div class="dars-accordion-section{opened}"><div class="dars-accordion-title">{title}</div><div class="dars-accordion-content">{content.render() if hasattr(content, "render") else content}</div></div>'
        html += '</div>'
        return html
