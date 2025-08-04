from dars.core.component import Component
from typing import Optional, Dict, Any

class Textarea(Component):
    """Componente para áreas de texto multilínea."""
    def __init__(
        self,
        value: str = "",
        placeholder: str = "",
        rows: int = 4,
        cols: int = 50,
        disabled: bool = False,
        readonly: bool = False,
        required: bool = False,
        max_length: Optional[int] = None,
        class_name: Optional[str] = None,
        style: Optional[Dict[str, Any]] = None,
        **kwargs
    ):
        super().__init__(class_name=class_name, style=style, **kwargs)
        self.value = value
        self.placeholder = placeholder
        self.rows = rows
        self.cols = cols
        self.disabled = disabled
        self.readonly = readonly
        self.required = required
        self.max_length = max_length

    def render(self) -> str:
        attrs = [
            f'rows="{self.rows}"',
            f'cols="{self.cols}"',
        ]
        if self.placeholder: attrs.append(f'placeholder="{self.placeholder}"')
        if self.disabled: attrs.append('disabled')
        if self.readonly: attrs.append('readonly')
        if self.required: attrs.append('required')
        if self.max_length: attrs.append(f'maxlength="{self.max_length}"')
        if self.class_name: attrs.append(f'class="{self.class_name}"')
        if self.style: attrs.append(f'style="{self.render_styles(self.style)}"')
        
        return f'<textarea {" ".join(attrs)}>{self.value}</textarea>'



