from typing import Any, Optional

from dars.core.component import Component


class Tooltip(Component):
    """
    Information box that appears on hover, providing extra context for a component.

    Props:
    - **text** (str): The message to display in the tooltip box.
    - **child** (Component): The component that will trigger the tooltip.
    - **position** (str): Tooltip placement relative to the child (`"top"`, `"right"`, `"bottom"`, `"left"`).
    - **id** (str): Unique identifier for the component.
    - **class_name** (str): String containing regular CSS class names.
    - **style** (dict): Optional dictionary for CSS utility classes (prefer `style`).
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

    def __init__(self, text: Any, child: Component, position: Any = "top", **props):
        super().__init__(**props)
        self.text = text
        self.child = child
        self.position = position

    def render(self) -> str:
        child_render = getattr(self.child, "render", None)
        child_content = child_render() if callable(child_render) else self.child
        return f'<div class="dars-tooltip dars-tooltip-{self.position}">{child_content}<span class="dars-tooltip-text">{self.text}</span></div>'
