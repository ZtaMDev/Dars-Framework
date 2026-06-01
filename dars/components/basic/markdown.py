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
        content: Any = None,
        file_path: Any = None,
        id: Any = None,
        class_name: Any = None,
        style: Optional[Dict[str, Any] | str] = None,
        dark_theme: bool = True,
        lazy: bool = False,
        prism_theme: Any = "prism-okaidia",
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
        self.prism_theme = prism_theme
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
    
    def update_content(self, new_content: Any = None, new_file_path: Any = None):
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
    
    def load_prism_theme(self) -> str:
        """Dynamically load the selected Prism.js theme."""
        
        theme_url = (
            f"https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/themes/"
            f"{self.prism_theme}.min.css"
        )

        html = f'<link href="{theme_url}" rel="stylesheet">'
        
        self.rendered_html += html
        
        return html

    def render(self, exporter: Any) -> str:
        """Render the Markdown component with the selected theme."""
        raise NotImplementedError("Exporter implements the component render")