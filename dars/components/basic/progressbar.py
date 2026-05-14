from dars.core.component import Component
from typing import Optional

class ProgressBar(Component):
    """
    Visual progress bar component to indicate completion of a task.
    
    Props:
    - **value** (int): Current progress value (from 0 to `max_value`).
    - **max_value** (int): Maximum value representing 100% (defaults to 100).
    - **id** (str): Unique identifier for the component.
    - **class_name** (str): String containing regular CSS class names.
    - **style** (dict): Optional dictionary for CSS utility classes (prefer `style`).
    - **children** (list): List of child components.
    - **Events**: Handlers like `on_click`, `on_mouse_enter`, etc.
    
    Example:
    ```python
    ProgressBar(
        value=75,
        class_name="w-full bg-indigo-100 rounded-lg shadow-inner",
        id="loading-bar"
    )
    ```
    """

    def __init__(self, value: int, max_value: int = 100, **props):
        super().__init__(**props)
        self.value = value
        self.max_value = max_value

    def render(self) -> str:
        percent = min(max(self.value / self.max_value * 100, 0), 100)
        return f'<div class="dars-progressbar"><div class="dars-progressbar-bar" style="width: {percent}%;"></div></div>'
