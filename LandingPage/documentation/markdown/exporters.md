# Dars - Exporter Documentation

## Introduction

Exporters are the heart of Dars that allow transforming applications written in Python to different technologies and platforms. Each exporter translates Dars components, styles, and scripts to the native code of the target platform.

## Exporter Architecture

### Base Exporter Class

All exporters inherit from the base `Exporter` class:

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
        
    @abstractmethod
    def get_platform(self) -> str:
        """Returns the name of the platform"""
        pass
```

### Exportation Flow

1. **Validation**: Verify that the application is valid
2. **Preparation**: Create directory structure
3. **Rendering**: Convert components to the target format
4. **Generation**: Create configuration and dependency files
5. **Finalization**: Write files to the system

## Web Exporters

### HTML/CSS/JavaScript

The HTML exporter generates standard web applications that can run in any browser.

#### Features

- **Compatibility**: Works in all modern browsers
- **Simplicity**: No requires build tools
- **Performance**: Fast loading and efficient execution
- **SEO**: Content indexable by search engines

#### Usage

```bash
dars export my_app.py --format html --output ./dist
```

#### Generated Structure

```
dist/
├── index.html      # Main page
├── styles.css      # CSS styles
└── script.js       # JavaScript logic
```

#### Example Output

**index.html**
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>My Application</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <div id="container_123" class="dars-container" style="display: flex; flex-direction: column; padding: 20px;">
        <span id="text_456" class="dars-text" style="font-size: 24px; color: #333;">Hello Dars!</span>
        <button id="button_789" class="dars-button" style="background-color: #007bff; color: white;">Click</button>
    </div>
    <script src="script.js"></script>
</body>
</html>
```

**styles.css**
```css
/* Base Dars styles */
* {
    box-sizing: border-box;
}

body {
    margin: 0;
    padding: 0;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
}

.dars-button {
    display: inline-block;
    padding: 8px 16px;
    border: 1px solid #ccc;
    background-color: #f8f9fa;
    color: #333;
    cursor: pointer;
    border-radius: 4px;
    font-size: 14px;
}

.dars-button:hover {
    background-color: #e9ecef;
}
```

#### Advantages

- **Universality**: Works in any web server
- **Debugging**: Easy to debug with browser tools
- **Personalization**: CSS and JavaScript completely modifiable
- **Hosting**: Can be hosted on any static hosting service

#### Use Cases

- Corporate websites
- Landing pages
- Simple web applications
- Quick prototypes
- Interactive documentation

## Exporter Personalization

### Extending Existing Exporters

```python
from dars.exporters.base import Exporter

class MyCustomExporter(Exporter):
    def get_platform(self):
        return "my_custom_platform"
    
    def export(self, app, output_path):
        # Implement custom export logic
        return True
    
    def render_component(self, component):
        # Implement custom component rendering
        return "generated_code"
```

## Desktop Export (BETA)

The desktop exporter allows you to package your Dars app as a native desktop application. This feature is currently in BETA: usable for testing and internal tooling, but not recommended for production deployments yet.

### Status and Scope

- BETA: Many options and integrations are still evolving (advanced packaging, signing, etc.).
- Cross‑platform targets supported: Windows, Linux, macOS (host restrictions apply for macOS signing, and linux if you don't have docker).
- Underlying tech: Electron is used to deliver a native desktop container for your web UI.
- Hot Reload: `dars dev` with desktop apps is fully supported, but for now it closes and reopen the electron dev app when a file change is detected.
### Quickstart desktop Export

1. Initialize or update your project for desktop:

   ```bash
   dars init --type desktop
   # or if you already have a project
   dars init --update
   ```

2. Ensure your project config has desktop format:

   ```json
   {
     "entry": "main.py",
     "format": "desktop",
     "outdir": "dist",
     "targetPlatform": "auto"
   }
   ```

3. Verify optional tooling (Node/Bun, Electron, electron‑builder):

   ```bash
   dars doctor --all --yes
   ```

4. Build your desktop app:

   ```bash
   dars build
   ```

Artifacts will be placed in `dist/`. The desktop source (used for packaging) is emitted to `dist/source-electron/`.

### Native Functions

You can acces native functions via `dars.desktop` module:

```python
from dars.desktop import *
```

With this module you can acces for now 2 main functions:

```python 
write_text("./app/lib/hello.txt", "Hello Text")
```
and

```python
read_text("./app/lib/hello.txt")
```

This two functions allows you to read and write text files in your desktop application filesystem, both returns an dScript() with the code to be executed in the desktop app.
also you can use dScripts to run custom javascript code in the desktop app. and for now 'dars dev' is supported but python main.py with rTimeCompile() is not supported because it have issues with relative paths and also it can be used in events of any component.

### Platform Targeting

- `targetPlatform`: `auto` | `windows` | `linux` | `macos`.
- On non‑mac hosts, building for macOS is not supported.

### Metadata and Packaging Notes

- App metadata is taken from your `App` instance when available: title, description, author, version.
- If version is not set, a default `0.1.0` is used and a warning is shown.
- Package manager and Electron version are pinned by the exporter to make builds predictable.

### Caveats (BETA)

- Not yet recommended for production.
- Some advanced packaging and signing options may require manual configuration.
- Expect changes to configuration keys and defaults as the feature matures.
