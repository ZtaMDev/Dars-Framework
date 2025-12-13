from dars.core.component import Component
from typing import Optional, Dict, Any

class Image(Component):
    """Component to display images."""
    def __init__(
        self,
        src: str,
        alt: str = "",
        width: Optional[str] = None,
        height: Optional[str] = None,
        class_name: Optional[str] = None,
        style: Optional[Dict[str, Any]] = None,
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




