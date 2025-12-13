from dars.core.component import Component
from typing import List, Optional

class Accordion(Component):
    """
    Accordion component to display collapsible sections.
    sections: List of tuples (title, content)
    open_indices: List of open indices (optional)
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
