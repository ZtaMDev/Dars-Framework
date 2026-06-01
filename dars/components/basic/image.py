from dars.core.component import Component
from typing import Optional, Dict, Any

class Image(Component):
    """
    Component for displaying images with support for dimensions and styling.
    
    Props:
    - **src** (str): URL or path to the image source.
    - **alt** (str): Alternative text for accessibility.
    - **width** (str): Width of the image (e.g., `"100px"`, `"50%"`).
    - **height** (str): Height of the image.
    - **id** (str): Unique identifier for the component.
    - **class_name** (str): String containing regular CSS class names.
    - **style** (dict): Optional dictionary for CSS utility classes (prefer `style`).
    - **children** (list): List of child components.
    - **Events**: Handlers like `on_click`, `on_load`, etc.
    
    Example:
    ```python
    Image(
        src="https://example.com/logo.png",
        alt="Dars Logo",
        class_name="w-32 h-32 rounded-xl"
    )
    ```
    """
    def __init__(
        self,
        src: Any,
        alt: Any = "",
        width: Any = None,
        height: Any = None,
        class_name: Any = None,
        style: Optional[Dict[str, Any] | str] = None,
        **kwargs
    ):
        super().__init__(class_name=class_name, style=style, **kwargs)
        self.src = src
        self.alt = alt
        self.width = width
        self.height = height

    def render(self) -> str:
        attrs = [
            f'src="{self.src}"',
            f'alt="{self.alt}"',
        ]
        if self.width: attrs.append(f'width="{self.width}"')
        if self.height: attrs.append(f'height="{self.height}"')
        if self.class_name: attrs.append(f'class="{self.class_name}"')
        if self.style: attrs.append(f'style="{self.render_styles(self.style)}"')
        
        return f'<img {" ".join(attrs)} />'




