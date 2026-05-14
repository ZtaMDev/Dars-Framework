from typing import Optional, Dict, Any, Callable, Union
import os
from dars.core.component import Component

class Markdown(Component):
    """
    Component for rendering Markdown content into HTML using the Dars engine.
    
    Props:
    - **content** (str): Raw markdown string to be rendered.
    - **file_path** (str): Path to a `.md` file to load content from (cannot be used with `content`).
    - **dark_theme** (bool): Whether to apply dark theme styles to the markdown container.
    - **lazy** (bool): Enable lazy loading for content that only fetches when visible.
    - **id** (str): Unique identifier for the component.
    - **class_name** (str): String containing regular CSS class names.
    - **style** (dict): Optional dictionary for CSS utility classes (prefer `style`).
    - **children** (list): List of child components (not typically used for Markdown).
    - **Events**: Handlers like `on_click`, `on_mouse_enter`, etc.
    
    Example:
    ```python
    Markdown(
        content="# Hello Dars\nThis is **markdown** content.",
        class_name="p-6 bg-white rounded-xl shadow-sm border border-slate-200"
    )
    ```
    """
    def __init__(
        self,
        content: Optional[str] = None,
        file_path: Optional[str] = None,
        id: Optional[str] = None,
        class_name: Optional[str] = None,
        style: Optional[Dict[str, Any]] = None,
        dark_theme: bool = False,
        lazy: bool = False,
        **kwargs
    ):
    
        super().__init__(id=id, class_name=class_name, style=style, **kwargs)
        
        if content and file_path:
            raise ValueError("Only content or file_path can be specified, not both")
        
        if not content and not file_path:
            raise ValueError("Either content or file_path must be specified")
        
        self.content = content
        self.file_path = file_path
        self.dark_theme = dark_theme
        self.lazy = lazy
        self.rendered_html = ""
        
        # Load and process markdown content
        self._load_and_process_content()
    
    def _load_and_process_content(self):
        """Load and process markdown content."""
        if self.file_path:
            if not os.path.exists(self.file_path):
                raise FileNotFoundError(f"File {self.file_path} does not exist")
            
            if not self.file_path.endswith('.md'):
                raise ValueError("File must have .md extension")
            
            with open(self.file_path, 'r', encoding='utf-8') as f:
                self.content = f.read()
    
    def update_content(self, new_content: Optional[str] = None, new_file_path: Optional[str] = None):
        """
        Update the markdown content of the component.
        
        Args:
            new_content: New markdown content as string
            new_file_path: New markdown file path
        """
        if new_content and new_file_path:
            raise ValueError("Only new_content or new_file_path can be specified, not both")
        
        if new_content:
            self.content = new_content
            self.file_path = None
        elif new_file_path:
            self.file_path = new_file_path
            self.content = None
        
        self._load_and_process_content()
    
    def set_dark_theme(self, enabled: bool = True):
        """Enable or disable dark theme"""
        self.dark_theme = enabled
        # Add dark theme class dynamically
        if enabled:
            self.class_name = f"{self.class_name or ''} dars-markdown-dark"
        else:
            self.class_name = self.class_name.replace("dars-markdown-dark", "") if self.class_name else ""
    
    def render(self, exporter: Any) -> str:
        # El método render será implementado por cada exportador
        raise NotImplementedError("El método render debe ser implementado por el exportador")