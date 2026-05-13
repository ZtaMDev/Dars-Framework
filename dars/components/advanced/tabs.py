from dars.core.component import Component
from typing import List, Optional

class Tabs(Component):
    """
    Tabbed navigation component for switching between multiple content panels in the same space.
    
    Props:
    - **tabs** (list): List of strings for the tab headers.
    - **panels** (list): List of components or strings representing the content of each tab.
    - **selected** (int): Index of the initially active tab (defaults to 0).
    - **id** (str): Unique identifier for the component.
    - **class_name** (str): String containing CSS utility classes (e.g., `"flex flex-col w-full"`).
    - **style** (dict): Optional dictionary for direct inline styles (prefer `class_name`).
    - **children** (list): List of child components.
    - **Events**: Handlers like `on_change` when the active tab is switched.
    
    Example:
    ```python
    Tabs(
        tabs=["General", "Security", "Notifications"],
        panels=[
            Container(Text("General settings...")),
            Container(Text("Security settings...")),
            Container(Text("Notification settings..."))
        ],
        selected=0,
        class_name="bg-white rounded-xl shadow-sm border border-slate-100"
    )
    ```
    """

    def __init__(self, tabs: List[str], panels: List[Component], selected: Optional[int]=0, minimum_logic: bool = True, **props):
        super().__init__(**props)
        self.tabs = tabs
        self.panels = panels
        self.selected = selected or 0
        self.minimum_logic = minimum_logic
        for panel in panels:
            if hasattr(panel, 'render'):
                self.add_child(panel)

    def render(self) -> str:
        tab_headers = ''.join(
            f'<button class="dars-tab{ " dars-tab-active" if i == self.selected else "" }" data-tab="{i}">{title}</button>'
            for i, title in enumerate(self.tabs)
        )
        panels_html = ''.join(
            f'<div class="dars-tab-panel{ " dars-tab-panel-active" if i == self.selected else "" }">{panel.render() if hasattr(panel, "render") else panel}</div>'
            for i, panel in enumerate(self.panels)
        )
        return f'<div class="dars-tabs"><div class="dars-tabs-header">{tab_headers}</div><div class="dars-tabs-panels">{panels_html}</div></div>'
