# Dars Framework - Architecture and Design

## Overview

Dars is a cross-platform user interface framework that allows developers to write user interfaces in pure Python and export them to multiple technologies and platforms. The framework is designed with the following core principles:

### Design Principles

1. **Ease of Use**: Code should be readable and easy to write, maintaining Python's expressiveness.
2. **Modularity**: Each component and exporter should be independent and extensible.
3. **Cross-Platform**: Native support for exporting to web, mobile, and desktop technologies.
4. **Declarative**: Components are defined declaratively, similar to modern frameworks like React.
5. **Strong Typing**: Use of type hints for a better development experience.

## Framework Architecture

### Directory Structure

```
dars/
├── core/
│   ├── __init__.py
│   ├── component.py          # Clase base Component
│   ├── app.py               # Clase principal App
│   ├── properties.py        # Sistema de propiedades
│   └── events.py           # Sistema de eventos
├── components/
│   ├── __init__.py
│   ├── basic/
│   │   ├── __init__.py
│   │   ├── button.py
│   │   ├── text.py
│   │   ├── input.py
│   │   ├── container.py
│   │   ├── image.py
│   │   ├── link.py
│   │   └── textarea.py
│   ├── advanced/
│   │   ├── __init__.py
│   │   ├── card.py
│   │   ├── modal.py
│   │   └── navbar.py
│   └── layout/
│       ├── __init__.py
│       ├── flex.py
│       ├── grid.py
│       └── stack.py
├── scripts/
│   ├── __init__.py
│   └── script.py           # Clase base Script
├── exporters/
│   ├── __init__.py
│   ├── base.py             # Clase base Exporter
│   └── web/
│       ├── __init__.py
│       └── html_css_js.py
├── cli/
│   ├── __init__.py
│   ├── main.py             # Herramienta de consola
│   └── preview.py          # Sistema de preview
├── templates/
│   ├── html/
│   └── examples/
│       ├── README.md
│       ├── basic/
│       ├── advanced/
│       └── demo/
└── docs/
    ├── getting_started.md
    ├── components.md
    ├── scripts.md
    └── exporters.md
```

### Main Components

#### 1. Base Component Class

The `Component` class is the base for all UI elements in the framework:

```python
from typing import Dict, Any, List, Optional, Callable
from abc import ABC, abstractmethod

class Component(ABC):
    def __init__(self, **props):
        self.props = props
        self.children: List[Component] = []
        self.parent: Optional[Component] = None
        self.id: Optional[str] = props.get("id")
        self.class_name: Optional[str] = props.get("class_name")
        self.style: Dict[str, Any] = props.get("style", {})
        self.events: Dict[str, Callable] = {}
        
    def add_child(self, child: "Component"):
        child.parent = self
        self.children.append(child)
        
    def set_event(self, event_name: str, handler: Callable):
        self.events[event_name] = handler
        
    @abstractmethod
    def render(self) -> str:
        pass
```

#### 2. Property System

Properties are defined using a typed system that allows validation and autocompletion:

```python
from typing import Union, Optional
from dataclasses import dataclass

@dataclass
class StyleProps:
    width: Optional[Union[str, int]] = None
    height: Optional[Union[str, int]] = None
    margin: Optional[Union[str, int]] = None
    padding: Optional[Union[str, int]] = None
    background_color: Optional[str] = None
    color: Optional[str] = None
    font_size: Optional[Union[str, int]] = None
    border: Optional[str] = None
    border_radius: Optional[Union[str, int]] = None
    display: Optional[str] = None
    flex_direction: Optional[str] = None
    justify_content: Optional[str] = None
    align_items: Optional[str] = None
    ...
```

#### 3. App Class

The main class that contains the entire application:

```python
class App:
    def __init__(self, title: str = "Dars App"):
        self.title = title
        self.root: Optional[Component] = None
        self.scripts: List[Script] = []
        self.global_styles: Dict[str, Any] = {}
        
    def set_root(self, component: Component):
        self.root = component
        
    def add_script(self, script: "Script"):
        self.scripts.append(script)
        
    def export(self, exporter: "Exporter", output_path: str):
        return exporter.export(self, output_path)
```

### Script System

Scripts allow you to add interactive logic to applications:

```python
from abc import ABC, abstractmethod
from typing import Optional

class Script(ABC):
    def __init__(self):
        pass
        
    @abstractmethod
    def get_code(self) -> str:
        """Returns the script code"""
        pass
        
class InlineScript(Script):
    def __init__(self, code: str):
        super().__init__()
        self.code = code
        
    def get_code(self) -> str:
        return self.code
        
class FileScript(Script):
    def __init__(self, file_path: str):
        super().__init__()
        self.file_path = file_path
        
    def get_code(self) -> str:
        with open(self.file_path, "r") as f:
            return f.read()
```

### Exporter System

Each exporter implements the base `Exporter` interface:

```python
from abc import ABC, abstractmethod

class Exporter(ABC):
    def __init__(self):
        self.templates_path = "templates/"
        
    @abstractmethod
    def export(self, app: App, output_path: str) -> bool:
        """Exports the application to the specific format"""
        pass
        
    @abstractmethod
    def render_component(self, component: Component) -> str:
        """Renders an individual component"""
        pass
        
    def load_template(self, template_name: str) -> str:
        """Loads a template from the templates directory"""
        template_path = f"{self.templates_path}{self.get_platform()}/{template_name}"
        with open(template_path, "r") as f:
            return f.read()
            
    @abstractmethod
    def get_platform(self) -> str:
        """Returns the platform name (html, react, etc.)"""
        pass
```

## Workflow

1. **Development**: The user writes their application using Dars components
2. **Export**: The CLI `dars export` is run, specifying the output format
3. **Generation**: The corresponding exporter processes the application and generates the code
4. **Preview**: Optionally, the result can be previewed in the browser with `dars preview`

## Usage Example

```python
from dars.core.app import App
from dars.components.basic.button import Button
from dars.components.basic.text import Text
from dars.components.basic.container import Container
from dars.components.basic.page import Page
from dars.scripts.script import InlineScript

# Create the application
app = App(title="My First App")

# Create components
page = Page(title="Main Page")

container = Container(
    style={
        "display": "flex",
        "flex-direction": "column",
        "align-items": "center",
        "padding": "20px"
    }
)

title = Text(
    text="Hello Dars!",
    style={
        "font-size": "24px",
        "color": "#333",
        "margin-bottom": "20px"
    }
)

button = Button(
    text="Click",
    style={
        "background-color": "#007bff",
        "color": "white",
        "padding": "10px 20px",
        "border": "none",
        "border-radius": "5px"
    }
)

# Add script
script = InlineScript("""
function handleClick() {
    alert("Button pressed!");
}
""")

# Assemble the application
container.add_child(title)
container.add_child(button)
app.set_root(container)
app.add_script(script)

# Save the file as app.py and run with:
# dars export app.py --format html --output ./dist
# dars preview ./dist/index.html
```

This architecture provides a solid and extensible foundation for the Dars framework, allowing new components and exporters to be added in a modular way.
