# Dars Framework - Arquitectura y Diseño

## Visión General

Dars es un framework de interfaz de usuario multiplataforma que permite a los desarrolladores escribir interfaces de usuario en Python puro y exportarlas a múltiples tecnologías y plataformas. El framework está diseñado con los siguientes principios fundamentales:

### Principios de Diseño

1. **Simplicidad de Uso**: El código debe ser legible y fácil de escribir, manteniendo la expresividad de Python.
2. **Modularidad**: Cada componente y exportador debe ser independiente y extensible.
3. **Multiplataforma**: Soporte nativo para exportar a tecnologías web, móviles y de escritorio.
4. **Declarativo**: Los componentes se definen de manera declarativa, similar a frameworks modernos como React.
5. **Tipado Fuerte**: Uso de type hints para mejor experiencia de desarrollo.

## Arquitectura del Framework

### Estructura de Directorios

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

### Componentes Principales

#### 1. Clase Base Component

La clase `Component` es la base de todos los elementos UI del framework:

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

#### 2. Sistema de Propiedades

Las propiedades se definen usando un sistema tipado que permite validación y autocompletado:

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
```

#### 3. Clase App

La clase principal que contiene toda la aplicación:

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

### Sistema de Scripts

Los scripts permiten agregar lógica interactiva a las aplicaciones:

```python
from abc import ABC, abstractmethod
from typing import Optional

class Script(ABC):
    def __init__(self):
        pass
        
    @abstractmethod
    def get_code(self) -> str:
        """Retorna el código del script"""
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

### Sistema de Exportadores

Cada exportador implementa la interfaz base `Exporter`:

```python
from abc import ABC, abstractmethod

class Exporter(ABC):
    def __init__(self):
        self.templates_path = "templates/"
        
    @abstractmethod
    def export(self, app: App, output_path: str) -> bool:
        """Exporta la aplicación al formato específico"""
        pass
        
    @abstractmethod
    def render_component(self, component: Component) -> str:
        """Renderiza un componente individual"""
        pass
        
    def load_template(self, template_name: str) -> str:
        """Carga una plantilla desde el directorio de templates"""
        template_path = f"{self.templates_path}{self.get_platform()}/{template_name}"
        with open(template_path, "r") as f:
            return f.read()
            
    @abstractmethod
    def get_platform(self) -> str:
        """Retorna el nombre de la plataforma (html, react, etc.)"""
        pass
```

## Flujo de Trabajo

1. **Desarrollo**: El usuario escribe su aplicación usando los componentes de Dars
2. **Exportación**: Se ejecuta el CLI `dars export` especificando el formato de salida
3. **Generación**: El exportador correspondiente procesa la aplicación y genera el código
4. **Preview**: Opcionalmente se puede previsualizar el resultado en el navegador con `dars preview`

## Ejemplo de Uso

```python
from dars.core.app import App
from dars.components.basic.button import Button
from dars.components.basic.text import Text
from dars.components.basic.container import Container
from dars.components.basic.page import Page
from dars.scripts.script import InlineScript

# Crear la aplicación
app = App(title="Mi Primera App")

# Crear componentes
page = Page(title="Página principal")

container = Container(
    style={
        "display": "flex",
        "flex-direction": "column",
        "align-items": "center",
        "padding": "20px"
    }
)

title = Text(
    text="¡Hola Dars!",
    style={
        "font-size": "24px",
        "color": "#333",
        "margin-bottom": "20px"
    }
)

button = Button(
    text="Hacer clic",
    style={
        "background-color": "#007bff",
        "color": "white",
        "padding": "10px 20px",
        "border": "none",
        "border-radius": "5px"
    }
)

# Agregar script
script = InlineScript("""
function handleClick() {
    alert("¡Botón presionado!");
}
""")

# Ensamblar la aplicación
container.add_child(title)
container.add_child(button)
app.set_root(container)
app.add_script(script)

# El archivo se guarda como app.py y se ejecuta con:
# dars export app.py --format html --output ./dist
# dars preview ./dist/index.html
```

Esta arquitectura proporciona una base sólida y extensible para el framework Dars, permitiendo agregar nuevos componentes y exportadores de manera modular.


