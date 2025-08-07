# Installation Guide - Dars Framework

## System Requirements

### Minimum Requirements

- **Python**: 3.8 or higher
- **Operating System**: Windows, macOS, Linux
- **RAM**: 512 MB minimum (2 GB recommended)
- **Disk Space**: 100 MB for the framework

## Quick Installation

To install Dars, simply use pip:

```bash
pip install dars-framework
```

This will install Dars and all its dependencies automatically.

## CLI Usage

- [Dars CLI](dars/docs/cli.md)

Once installed, the `dars` command will be available in your terminal. You can use it to:

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
# Basic project with Hello World
dars init my_new_project

# Project with a specific template
dars init my_project -t demo/complete_app
```

### View Application Information

```bash
dars info my_app.py
```

### View Supported Formats

```bash
dars formats
```

## Post-Installation Verification

To verify that Dars has been installed correctly, open your terminal and run:

```bash
dars --help
```

You should see the help for the `dars` command, indicating that the installation was successful.

## First Steps After Installation

### 1. Create Your First Application (my_first_app.py)

```python
from dars.core.app import App
from dars.components.basic.text import Text
from dars.components.basic.container import Container

app = App(title="My First App")
container = Container(style={'padding': '20px'}) # Use ' to escape quotes
text = Text(text="Hello Dars!", style={'font-size': '24px'}) # Use ' to escape quotes

container.add_child(text)
app.set_root(container)
```

### 2. Export the Application

Save the code above as `my_first_app.py` and then run:

```bash
dars export my_first_app.py --format html --output ./my_app
```

### 3. Preview

```bash
dars preview ./my_app
```

## Additional Resources

### Documentation

- [Main README](README.md)
- [Quick Start Guide](dars/docs/getting_started.md)
- [Components Documentation](dars/docs/components.md)
- [Script System](dars/docs/scripts.md)
- [Exporters Guide](dars/docs/exporters.md)

### Examples

- [Basic Examples](dars/templates/examples/basic/)
- [Advanced Examples](dars/templates/examples/advanced/)
- [Demo Application](dars/templates/examples/demo/)

### Useful Commands

```bash
# General help
dars --help

# Application information
dars info my_app.py

# Available formats
dars formats

# Preview application
dars preview ./output_directory
```

## Post-Installation Checklist

- [x] Python 3.8+ installed
- [x] Dars Framework installed via `pip install dars-framework`
- [x] CLI `dars` works correctly (`dars --help`)
- [x] Basic test run successfully
- [x] Example exported and previewed correctly
- [x] Documentation reviewed

Congratulations! Dars is ready to use.

---

**Next Step:** [Quick Start Guide](dars/docs/getting_started.md)
