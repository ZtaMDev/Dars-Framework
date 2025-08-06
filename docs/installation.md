# Installation Guide

## System Requirements

- **Python:** 3.8+
- **Operating System:** Windows, macOS, Linux
- **RAM:** 512 MB (2 GB recommended)
- **Disk Space:** 100 MB for the framework

## Quick Installation

Install Dars with pip:
```bash
pip install dars-framework
```
All dependencies will be installed automatically.

## CLI Usage

After installation, use the `dars` command in your terminal:

### Export Applications
```bash
dars export my_app.py --format html --output ./my_app_web
```

### Preview Applications
```bash
dars preview ./my_app_web
```

### Initialize a New Project
```bash
# Basic Hello World project
dars init my_new_project

# With a specific template
dars init my_new_project -t demo/complete_app
```

### App Info
```bash
dars info my_app.py
```

### Supported Formats
```bash
dars formats
```

## Installation Check

Verify your installation:
```bash
dars --help
```
You should see the help message, confirming Dars is installed.

## First Steps After Installation

### 1. Create Your First App (`my_first_app.py`)
```python
from dars.core.app import App
from dars.components.basic.text import Text
from dars.components.basic.container import Container

app = App(title="My First App")
container = Container(style={'padding': '20px'})
text = Text(text="Hello Dars!", style={'font-size': '24px'})

container.add_child(text)
app.set_root(container)
```

### 2. Export the App
Save as `my_first_app.py` and run:
```bash
dars export my_first_app.py --format html --output ./my_app
```

### 3. Preview
```bash
dars preview ./my_app
```

## Additional Resources
- [Quickstart Guide](getting_started.md)
- [Component Documentation](components.md)
- [Scripts System](scripts.md)
- [Exporter Guide](exporters.md)
- [Basic Examples](../templates/examples/basic/)
- [Advanced Examples](../templates/examples/advanced/)

## 🗂️ System Requirements

### Minimum Requirements

- **Python**: 3.8+
- **OS**: Windows, macOS, Linux
- **RAM**: 512 MB (2 GB recommended)
- **Disk Space**: 100 MB for the framework

## 🚀 Quick Installation

Install Dars with pip:

```bash
pip install dars-framework
```

All dependencies will be installed automatically.

## 🛠️ CLI Usage

Once installed, the `dars` command is available in your terminal:

### Export Applications
```bash
dars export my_app.py --format html --output ./my_app_web
```

### Preview Applications
```bash
dars preview ./my_app_web
```

### Initialize a New Project
```bash
# Basic Hello World project
dars init my_new_project

# With a specific template
dars init my_new_project -t demo/complete_app
```

### App Info
```bash
dars info my_app.py
```

### Supported Formats
```bash
dars formats
```

## ✅ Installation Check

Verify your installation:
```bash
dars --help
```

You should see the help message, confirming Dars is installed.

## 🚀 First Steps After Installation

### 1. Create Your First App (my_first_app.py)
```python
from dars.core.app import App
from dars.components.basic.text import Text
from dars.components.basic.container import Container

app = App(title="My First App")
container = Container(style={'padding': '20px'})
text = Text(text="Hello Dars!", style={'font-size': '24px'})

container.add_child(text)
app.set_root(container)
```

### 2. Export the App
Save as `my_first_app.py` and run:
```bash
dars export my_first_app.py --format html --output ./my_app
```

### 3. Preview
```bash
dars preview ./my_app
```

## 📚 Additional Resources

- [Quickstart Guide](getting_started.md)
- [Component Documentation](components.md)
- [Scripts System](scripts.md)
- [Exporter Guide](exporters.md)

### Examples
- [Basic Examples](../templates/examples/basic/)
- [Advanced Examples](../templates/examples/advanced/)
- [Demo App](../templates/examples/demo/)

### Useful Commands
```bash
dars --help
dars info my_app.py
dars formats
dars preview ./output_directory
```

## ✅ Post-Installation Checklist

- [x] Python 3.8+ installed
- [x] Dars Framework installed via `pip install dars-framework`
- [x] CLI `dars` works (`dars --help`)
- [x] Basic test run successfully
- [x] Example exported and previewed
- [x] Docs reviewed

Congratulations! Dars is ready to use. 🎉

---

**Next step:** [Quickstart Guide](getting_started.md)
