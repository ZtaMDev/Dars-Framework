from dars.core.component import Component
from typing import Optional, Dict, Any

class Link(Component):
    """Component to create links."""
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



