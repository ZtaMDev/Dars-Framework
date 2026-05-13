
from dars.core.component import Component
from dars.core.events import EventTypes
from typing import Optional, Dict, Any, Callable, Union

class FileUpload(Component):
    """
    Component for selecting and uploading files with support for filters and size limits.
    
    Props:
    - **accept** (str): Allowed file types (e.g., `"image/*"`, `".pdf"`, `"audio/*"`).
    - **multiple** (bool): If True, allows selecting multiple files.
    - **disabled** (bool): If True, the component is not interactive.
    - **required** (bool): If True, a file must be selected.
    - **max_size** (int): Maximum file size allowed in bytes.
    - **label** (str): Text label for the upload button (defaults to "Choose File").
    - **id** (str): Unique identifier for the component.
    - **class_name** (str): String containing CSS utility classes (e.g., `"bg-slate-100 border-2 border-dashed p-8 text-center rounded-xl"`).
    - **style** (dict): Optional dictionary for direct inline styles (prefer `class_name`).
    - **children** (list): List of child components.
    - **Events**: Handlers like `on_change` (triggered when files are selected).
    
    Example:
    ```python
    FileUpload(
        accept="image/*",
        multiple=True,
        label="Upload Images",
        class_name="bg-indigo-600 text-white px-6 py-3 rounded-full cursor-pointer hover:bg-indigo-700 transition-all shadow-lg"
    )
    ```
    """
    def __init__(
        self,
        accept: Optional[str] = None,
        multiple: bool = False,
        disabled: bool = False,
        required: bool = False,
        max_size: Optional[int] = None,  # In bytes
        id: Optional[str] = None,
        class_name: Optional[str] = None,
        style: Optional[Dict[str, Any]] = None,
        on_change: Optional[Callable] = None,
        label: Optional[str] = "Choose File",
        **props
    ):
        super().__init__(id=id, class_name=class_name, style=style, **props)
        self.accept = accept
        self.multiple = multiple
        self.disabled = disabled
        self.required = required
        self.max_size = max_size
        self.label = label
        
        if on_change:
            self.set_event(EventTypes.CHANGE, on_change)

    def render(self, exporter: Any) -> str:
        raise NotImplementedError("render method must be implemented by exporter")
