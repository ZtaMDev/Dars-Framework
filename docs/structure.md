# Project Structure

The Dars Framework repository is organized for clarity and scalability. Below is an overview of the main directories and files:

```text
dars-framework/
├── README.md                  # Main documentation
├── INSTALL.md                 # Installation guide
├── STRUCTURE.md               # This file (structure reference)
├── dars_architecture.md       # Architecture docs
├── pyproject.toml             # Python project config
│
├── dars/                      # Main framework code
│   ├── __init__.py
│   ├── core/                  # Core logic (App, Component, etc)
│   ├── components/            # All UI components
│   ├── scripts/               # JS scripts system
│   ├── exporters/             # Exporters (web, etc)
│   ├── templates/             # Export templates
│   ├── cli/                   # CLI tools
│   └── docs/                  # Detailed docs (source)
│
└── dars/templates/examples/   # Example apps
    ├── README.md
    ├── basic/                 # Basic examples
    ├── advanced/              # Advanced examples
    └── demo/                  # Demo app
```

## Folders

- **dars/core/**: Core logic (App, Component, properties, events)
- **dars/components/**: All UI components (basic, advanced, layout)
- **dars/scripts/**: Script system for JS integration
- **dars/exporters/**: Exporters for different platforms (web, etc)
- **dars/templates/**: Export and example templates
- **dars/cli/**: Command-line tools
- **dars/docs/**: Detailed markdown documentation (source)
- **dars/templates/examples/**: Example apps and templates for quick start

## Main Files
- **README.md**: Minimal intro and links
- **INSTALL.md**: Installation instructions
- **STRUCTURE.md**: This structure reference
- **dars_architecture.md**: Detailed architecture notes
- **pyproject.toml**: Python project configuration

For more details on each component, see [Components Reference](components.md). For installation, see [Installation Guide](installation.md).
## 🗂️ General Structure

```text
dars-framework/
├── README.md                  # Main documentation
├── INSTALL.md                 # Installation guide
├── STRUCTURE.md               # This file
├── dars_architecture.md       # Architecture docs
├── pyproject.toml             # Python project config
│
├── dars/                      # Main framework
│   ├── __init__.py
│   ├── core/                  # Core of the framework
│   ├── components/            # UI components
│   ├── scripts/               # JS scripts system
│   ├── exporters/             # Exporters
│   ├── templates/             # Export templates
│   ├── cli/                   # CLI tools
│   └── docs/                  # Detailed docs
│
└── dars/templates/examples/   # Example apps
    ├── README.md
    ├── basic/                 # Basic examples
    ├── advanced/              # Advanced examples
    └── demo/                  # Demo app
```

## 🏗️ Core (`dars/core/`)

```text
core/
├── __init__.py
├── app.py            # Main App class
├── component.py      # Base Component class
├── properties.py     # Style & property system
└── events.py         # Event handling system
```

### File Descriptions
- **`app.py`**: Main class for a Dars app
- **`component.py`**: Abstract base class for all UI components
- **`properties.py`**: Defines style and event properties
- **`events.py`**: Event system

## 🧩 Components (`dars/components/`)

```text
components/
├── __init__.py
├── basic/            # Basic components
│   ├── __init__.py
│   ├── text.py       # Text component
│   ├── button.py     # Button component
│   ├── input.py      # Input field
│   ├── container.py  # Container
│   ├── image.py      # Image
│   ├── link.py       # Link
│   └── textarea.py   # Textarea
├── advanced/         # Advanced components
│   ├── __init__.py
│   ├── card.py       # Card
│   ├── modal.py      # Modal
│   └── navbar.py     # Navbar
└── layout/           # Layout components
    └── __init__.py
```

### Implemented Components
- **Text**: Static/dynamic text
- **Button**: Interactive buttons
- **Input**: Data input fields
- **Container**: Layout grouping
- **Image**: Images
- **Link**: Navigation links
- **Textarea**: Multiline text area
- **Card**: Styled content group
- **Modal**: Overlay window
- **Navbar**: Navigation bar

## 📜 Scripts System (`dars/scripts/`)

```text
scripts/
├── __init__.py
└── script.py         # InlineScript and FileScript classes
```

- **InlineScript**: JS code defined in Python
- **FileScript**: Code loaded from external files

## 🔄 Exporters (`dars/exporters/`)

```text
exporters/
├── __init__.py
├── base.py           # Base Exporter class
└── web/              # Web exporters
    ├── __init__.py
    └── html_css_js.py # HTML/CSS/JS exporter
```

### Available Exporters
- **HTML/CSS/JS**: Standard web apps

## 📁 Templates (`dars/templates/`)

```text
templates/
├── __init__.py
├── examples/         # Example apps
│   ├── basic/
│   ├── advanced/
│   └── demo/
```

### Example Types
- **Basic**: Hello World, simple forms
- **Advanced**: Dashboards
- **Demo**: Complete app demo

## ⚙️ Config Files

- **pyproject.toml**: Python project metadata and dependencies
- **__init__.py**: Python module initializers

## 🔄 Data Flow

```text
Python App (*.py)
      ↓
  Dars Core
      ↓
  Validation
      ↓
  Specific Exporter
      ↓
  Output Code (HTML/CSS/JS)
```

## 🧠 Design Patterns Used
- **Factory**: Exporters created dynamically
- **Component**: All UI elements inherit from base Component
- **Strategy**: Different export strategies per platform
- **Template Method**: Common export process with platform-specific steps

## 🧩 Extension Points

### New Components
```python
# dars/components/basic/my_component.py
from dars.core.component import Component

class MyComponent(Component):
    def __init__(self, **props):
        super().__init__(**props)
        # Custom implementation
```

### New Exporters
```python
# dars/exporters/my_platform/my_exporter.py
from dars.exporters.base import Exporter

class MyExporter(Exporter):
    def get_platform(self):
        return "my_platform"
    
    def export(self, app, output_path):
        # Export logic
        return True
```

### New Scripts
```python
from dars.scripts.script import Script

class MyScriptType(Script):
    def get_code(self):
        # Generate code
        return "generated_code"
```

## 📈 Project Metrics (Approximate)
- **Core**: ~800 lines
- **Components**: ~1000 lines
- **Exporters**: ~500 lines
- **CLI**: ~400 lines
- **Scripts**: ~200 lines
- **Examples**: ~800 lines
- **Docs**: ~3000 lines
- **Total**: ~7000 lines

## 🚦 Roadmap
- [x] Core framework
- [x] Basic components
- [x] Advanced components
- [x] Script system
- [x] HTML/CSS/JS exporter
- [x] CLI with Rich
- [x] Preview system
- [x] Complete docs
- [x] Functional examples
- [ ] More components (Video, Table, Chart, etc.)
- [ ] Advanced theming
- [ ] Hot reloading
- [ ] Plugin system
- [ ] Code generator
- [ ] Integrated testing
- [ ] Exporters for other platforms (React, Desktop)

## 🦺 Security Considerations
- Scripts run in browser/app context
- Input validation in forms
- Data sanitization
- Output path validation
- Write permission checks
- Escape special characters

## 📝 Code Conventions
- **Python**: PEP 8, type hints, docstrings
- **JavaScript**: ES6+, comments, error handling
- One component per file, descriptive names, logical organization

---

This structure provides a solid, extensible base for Dars, enabling easy maintenance and future expansion.
