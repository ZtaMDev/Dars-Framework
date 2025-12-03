# Installation Guide - Dars Framework

## Quick Installation

To install Dars, simply use pip:

```bash
pip install dars-framework
```

This will install Dars and all its dependencies automatically.

## CLI Usage

- [Dars CLI](#dars-cli-reference)

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
dars init my_project -t basic/Forms
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

if __name__ == "__main__":
    app.rTimeCompile()
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

## Desktop (BETA)

You can build native desktop apps from Dars projects. This capability is in **BETA** and is not recommended for production yet, but it is usable for testing.

### Quickstart

```bash
# Scaffold or update a desktop-capable project
dars init --type desktop
# or
dars init --update

# Verify optional tooling (Node/Bun and packager)
dars doctor --all --yes

# Ensure your config sets the desktop format and target
# dars.config.json
{
  "entry": "main.py",
  "format": "desktop",
  "outdir": "dist",
  "targetPlatform": "auto"
}

# Build desktop artifacts
dars build
```

Notes:
- Desktop support is under active development; configuration keys and defaults may change.
- Some platform targets (like macOS) require building on that OS for signing.
