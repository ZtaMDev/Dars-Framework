# Dars Project Structure

## 📁 General Structure

```
dars-framework/
├── README.md                    # Main documentation (project overview and usage guide)
├── INSTALL.md                   # Installation instructions and requirements
├── STRUCTURE.md                 # Project structure reference (this file)
├── dars_architecture.md         # Internal architecture and design documentation
├── pyproject.toml               # Python project configuration (dependencies, metadata)
│
├── dars/                        # Main framework package
│   ├── __init__.py
│   ├── core/                    # Core logic and base classes
│   ├── components/              # User interface components
│   ├── scripts/                 # Script system and integrations
│   ├── exporters/               # Exporters for different platforms
│   ├── templates/               # Templates used for export
│   ├── cli/                     # Command-line interface tools
│   └── docs/                    # Detailed documentation and guides
│
└── dars/templates/examples/     # Example applications and templates
    ├── README.md
    ├── basic/                   # Basic usage examples
    ├── advanced/                # Advanced usage examples
    └── demo/                    # Complete demo application
```

## 🏗️ Framework Core (`dars/core/`)

```
core/
├── __init__.py
├── app.py                      # Main App class
├── component.py                # Base Component class
├── properties.py               # Property and style system
└── events.py                   # Event handling system
```

### Descripción de Archivos

- **`app.py`**: Main class representing a Dars application
- **`component.py`**: Abstract base class for all components
- **`properties.py`**: Defines style properties and events
- **`events.py`**: Event handling system

## 🧩 Componentes (`dars/components/`)

```
components/
├── __init__.py
├── basic/                      # Basic components
│   ├── __init__.py
│   ├── text.py                 # Text component
│   ├── button.py               # Button component
│   ├── input.py                # Input component
│   ├── container.py            # Container component
│   ├── image.py                # Image component
│   ├── link.py                 # Link component
│   └── textarea.py             # Text componentarea
├── advanced/                   # Advanced components
│   ├── __init__.py
│   ├── card.py                 # Card component
│   ├── modal.py                # Modal component
│   └── navbar.py               # Navbar component
└── layout/                     # Layout components (future)
    └── __init__.py
```

### Componentes Implementados

- **Text**: Display static or dynamic text
- **Button**: Interactive buttons
- **Input**: Input fields
- **Container**: Containers for organizing layout
- **Image**: Display images
- **Link**: Create navigation links
- **Textarea**: Multiline text areas
- **Card**: Styled container for grouping content
- **Modal**: Overlay modal window
- **Navbar**: Navigation bar

## 📜 Script System (`dars/scripts/`)

```
scripts/
├── __init__.py
└── script.py                   # InlineScript and FileScript classes
```

### Tipos de Scripts

- **InlineScript**: JavaScript code defined in Python
- **FileScript**: Code loaded from external files

## 🔄 Exportadores (`dars/exporters/`)

```
exporters/
├── __init__.py
├── base.py                     # Base Exporter class
└── web/                        # Web exporters
    ├── __init__.py
    └── html_css_js.py          # HTML/CSS/JS exporter
```

### Exportadores Disponibles

#### Web
- **HTML/CSS/JS**: Standard web applications

## 📋 Templates (`dars/templates/`)

```
templates/
├── __init__.py
├── examples/                   # Application examples
│   ├── README.md
│   ├── basic/                  # Basic examples
│   ├── advanced/               # Advanced examples
│   └── demo/                   # Complete demo application
└── html/                       # HTML templates
    └── __init__.py
```

## 🛠️ CLI Tools (`dars/cli/`)

```
cli/
├── __init__.py
├── main.py                     # Main CLI with Rich
└── preview.py                  # Preview system
```

### Available Tools

- **main.py**: Main CLI to export applications
- **preview.py**: Preview system para aplicaciones exportadas

## 📚 Documentación (`dars/docs/`)

```
docs/
├── __init__.py
├── getting_started.md          # Quick Start Guide
├── components.md               # Components documentation
├── scripts.md                  # Script system
└── exporters.md                # Exporters guide
```

## 🎯 Ejemplos (`dars/templates/examples/`)

```
examples/
├── README.md                   # Examples guide
├── basic/                      # Basic examples
│   ├── hello_world.py          # Hello World example
│   └── simple_form.py          # Simple form
├── advanced/                   # Advanced examples
│   └── dashboard.py            # Business dashboard
└── demo/                       # Complete demonstration
    └── complete_app.py         # Complete application
```

### Tipos de Ejemplos

#### Basic
- **Hello World**: Simple app with text and button
- **Simple Form**: Form with validation

#### Advanced
- **Dashboard**: Dashboard with navigation and statistics

#### Demostración
- **Complete App**: App showcasing all features

## 🔧 Configuration Files

### `pyproject.toml`
Configuration file for the Python project, including metadata and dependencies for PyPI.

### `__init__.py`
Initialization files for Python modules in each directory.

## 📊 Data Flow

```
Python Application (*.py)
         ↓
    Dars Core
         ↓
    Validation
         ↓
    Specific Exporter
         ↓
    Output Code (HTML/CSS/JS)
```

## 🎨 Design Patterns Used

### Factory Pattern
- Exporters are created dynamically according to the requested format

### Component Pattern
- All UI elements inherit from the base Component class

### Strategy Pattern
- Different export strategies for each platform

### Template Method Pattern
- Common export process with platform-specific steps

## 🔍 Extension Points

### New Components

```python
# dars/components/basic/mi_componente.py
from dars.core.component import Component

class MiComponente(Component):
    def __init__(self, **props):
        super().__init__(**props)
        # Specific implementation
```

### New Exporters

```python
# dars/exporters/mi_plataforma/mi_exportador.py
from dars.exporters.base import Exporter

class MiExportador(Exporter):
    def get_platform(self):
        return "mi_plataforma"
    
    def export(self, app, output_path):
        # Export logic
        return True
```

### New Scripts

```python
# Extend script functionality
from dars.scripts.script import Script

class MiTipoScript(Script):
    def get_code(self):
        # Generate specific code
        return "código_generado"
```

## 📈 Project Metrics

### Lines of Code (Approximate)

- **Core**: ~800 lines
- **Components**: ~1000 lines (updated with new components)
- **Exporters**: ~500 lines (HTML/CSS/JS only)
- **CLI**: ~400 lines
- **Scripts**: ~200 lines
- **Examples**: ~800 lines
- **Documentation**: ~3000 lines (updated with new documentation)

### Total: ~7000 lines of code and documentation

## 🚀 Development Roadmap

### Implemented

- [x] Framework core
- [x] Basic components (Text, Button, Input, Container, Page [supports add_script for per-page scripts in multipage], Checkbox, RadioButton, Select, Slider, DatePicker, etc)
- [x] Advanced components (Card, Modal, Navbar)
- [x] Script system
- [x] HTML/CSS/JS exporter
- [x] CLI with Rich
- [x] Preview system
- [x] Complete documentation
- [x] Functional examples

### Future Improvements 🔮

- [ ] More components (Video, Table, Chart, etc.)
- [ ] Advanced theme system
- [ ] Hot reloading in development
- [ ] Plugin system
- [ ] Automatic code generator
- [ ] Integrated testing framework
- [ ] Exporters for other platforms (React, React Native, Desktop)

## 🛡️ Security Considerations

### Scripts
- Scripts run in the context of the browser/application
- Input validation in forms
- Data sanitization

### Export
- Output path validation
- Write permissions verification
- Special character escaping

## 📝 Code Conventions

### Python
- PEP 8 for code style
- Type hints where appropriate
- Docstrings for public classes and methods

### JavaScript
- ES6+ features
- Descriptive comments
- Error handling

### File Structure
- One component per file
- Descriptive names
- Logical organization by functionality

---

This structure provides a solid and extensible foundation for the Dars framework, allowing for easy maintenance and future expansion.
This structure provides a solid and extensible foundation for the Dars framework, allowing for easy maintenance and future expansion.


