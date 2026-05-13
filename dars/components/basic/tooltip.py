from dars.core.component import Component
from typing import Optional

class Tooltip(Component):
    """
    Information box that appears on hover, providing extra context for a component.
    
    Props:
    - **text** (str): The message to display in the tooltip box.
    - **child** (Component): The component that will trigger the tooltip.
    - **position** (str): Tooltip placement relative to the child (`"top"`, `"right"`, `"bottom"`, `"left"`).
    - **id** (str): Unique identifier for the component.
    - **class_name** (str): String containing CSS utility classes (e.g., `"bg-slate-800 text-white text-xs p-2 rounded"`).
    - **style** (dict): Optional dictionary for direct inline styles (prefer `class_name`).
    - **children** (list): List of child components.
    - **Events**: Handlers for mouse events.
    
    Example:
    ```python
    Tooltip(
        text="Click to download report",
        child=Button("Download"),
        position="bottom",
        class_name="bg-indigo-600 text-white font-medium p-2 rounded-lg shadow-md transition-opacity"
    )
    ```
    """

    def __init__(self, text: str, child: Component, position: Optional[str] = "top", **props):
        super().__init__(**props)
        self.text = text
        self.child = child
        self.position = position

    def render(self) -> str:
        return f'<div class="dars-tooltip dars-tooltip-{self.position}">{self.child.render() if hasattr(self.child, "render") else self.child}<span class="dars-tooltip-text">{self.text}</span></div>'
