from dars.core.component import Component

class Spinner(Component):
    """
    Animated circular loading indicator (spinner) for indicating background processes.
    
    Props:
    - **id** (str): Unique identifier for the component.
    - **class_name** (str): String containing regular CSS class names.
    - **style** (dict): Optional dictionary for CSS utility classes (prefer `style`).
    - **children** (list): List of child components.
    - **Events**: Handlers like `on_click`, `on_mouse_enter`, etc.
    
    Example:
    ```python
    Spinner(class_name="w-6 h-6 border-2 border-indigo-600 border-t-transparent rounded-full animate-spin")
    ```
    """

    def __init__(self, **props):
        super().__init__(**props)

    def render(self) -> str:
        return '<div class="dars-spinner"></div>'
