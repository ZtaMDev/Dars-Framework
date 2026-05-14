from dars.core.component import Component
from typing import Optional, Dict, Any

class Textarea(Component):
    """
    Multiline text input component for longer messages or data entry.
    
    Props:
    - **value** (str): Initial text content.
    - **placeholder** (str): Hint text displayed when empty.
    - **rows** (int): Number of visible text lines (defaults to 4).
    - **cols** (int): Visible width in characters (defaults to 50).
    - **disabled** (bool): If True, the textarea is not interactive.
    - **readonly** (bool): If True, the content cannot be modified.
    - **required** (bool): If True, the field must be filled.
    - **max_length** (int): Maximum number of characters allowed.
    - **id** (str): Unique identifier for the component.
    - **class_name** (str): String containing regular CSS class names.
    - **style** (dict): Optional dictionary for CSS utility classes (prefer `style`).
    - **children** (list): List of child components.
    - **Events**: Handlers like `on_change`, `on_input`, `on_focus`, `on_blur`.
    
    Example:
    ```python
    Textarea(
        placeholder="Tell us about yourself...",
        rows=5,
        class_name="w-full bg-slate-50 border-slate-200 rounded-lg p-3 outline-none focus:border-indigo-500 transition-all"
    )
    ```
    """
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



