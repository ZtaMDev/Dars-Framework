from dars.core.component import Component
from typing import Optional, Dict, Any

class Link(Component):
    """
    Hyperlink component for navigation between pages or external URLs.
    
    Props:
    - **text** (str): The clickable text to display.
    - **href** (str): The URL or path to navigate to.
    - **target** (str): Where to open the link (e.g., `"_self"`, `"_blank"`).
    - **id** (str): Unique identifier for the component.
    - **class_name** (str): String containing CSS utility classes (e.g., `"text-indigo-600 hover:underline font-medium"`).
    - **style** (dict): Optional dictionary for direct inline styles (prefer `class_name`).
    - **children** (list): List of child components.
    - **Events**: Handlers like `on_click`, `on_mouse_enter`, etc.
    
    Example:
    ```python
    Link(
        text="Visit Documentation",
        href="/docs",
        class_name="text-indigo-500 hover:text-indigo-700 font-semibold transition-colors"
    )
    ```
    """
    def __init__(
        self,
        text: str,
        href: str,
        target: str = "_self",
        class_name: Optional[str] = None,
        style: Optional[Dict[str, Any]] = None,
        **kwargs
    ):
        super().__init__(class_name=class_name, style=style, **kwargs)
        self.text = text
        self.href = href
        self.target = target

    def render(self) -> str:
        attrs = [
            f'href="{self.href}"',
            f'target="{self.target}"',
        ]
        if self.class_name: attrs.append(f'class="{self.class_name}"')
        if self.style: attrs.append(f'style="{self.render_styles(self.style)}"')
        
        return f'<a {" ".join(attrs)}>{self.text}</a>'



