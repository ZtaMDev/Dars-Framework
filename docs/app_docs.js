window.__DARS_VDOM__={type:"T1",id:"page_93",children:[{type:"T2",id:"container_94",children:[{type:"T3",id:"dars-navbar",children:[{type:"T2",id:"navbar-left",children:[{type:"T4",id:"image_95"},{type:"T5",id:"text_96",text:"Dars Framework"}]},{type:"T2",id:"container_97",children:[{type:"T2",id:"navbar-right",children:[{type:"T6",id:"link_98",text:"Home"},{type:"T6",id:"link_99",text:"Documentation"},{type:"T6",id:"link_100",text:"Releases"},{type:"T6",id:"link_101",text:"PlayGround"},{type:"T6",id:"link_102",text:"GitHub"}]},{type:"T2",id:"hamburger-menu",children:[{type:"T2",id:"hamburger-btn",children:[{type:"T2",id:"container_103",children:[{type:"T2",id:"container_104"},{type:"T2",id:"container_105"},{type:"T2",id:"container_106"}]}]},{type:"T2",id:"mobile-menu",children:[{type:"T6",id:"link_107",text:"Home"},{type:"T6",id:"link_108",text:"Documentation"},{type:"T6",id:"link_109",text:"Releases"},{type:"T6",id:"link_110",text:"PlayGround"},{type:"T6",id:"link_111",text:"GitHub"}]}]}]}]}]},{type:"T8",id:"documentation-sidebar"},{type:"T2",id:"container_112",children:[{type:"T2",id:"markdown-content-container",children:[{type:"T9",id:"markdown_113",text:`# Dars Framework Documentation

Welcome to the official Dars Framework documentation. Here you will find detailed guides and references to help you build modern web applications with Python.

## Main Guides

- [Getting Started with Dars](#getting-started-with-dars)
- [App class](#app-class-and-pwa-features-in-dars-framework)
- [State Management](#state-management-in-dars-dstate-cstate-goto-mods)
- [Components](#dars-components-documentation)
- [Custom Components](#custom-components-in-dars-framework)
- [Event Handling](#events-in-dars)
- [Exporters](#dars-exporter-documentation)
  - See Desktop Export (BETA) in Exporters
- [Scripts System](#dars-script-system)
- [CLI Usage and Commands](#dars-cli-reference)

`},{type:"T9",id:"markdown_114",text:`# Installation Guide - Dars Framework

## System Requirements

### Minimum Requirements

- **Python**: 3.8 or higher
- **Operating System**: Windows, macOS, Linux
- **RAM**: 512 MB minimum (2 GB recommended)
- **Disk Space**: 100 MB for the framework

## Quick Installation

To install Dars, simply use pip:

\`\`\`bash
pip install dars-framework
\`\`\`

This will install Dars and all its dependencies automatically.

## CLI Usage

- [Dars CLI](#dars-cli-reference)

Once installed, the \`dars\` command will be available in your terminal. You can use it to:

### Export Applications

\`\`\`bash
dars export my_app.py --format html --output ./my_app_web
\`\`\`

### Preview Applications

\`\`\`bash
dars preview ./my_app_web
\`\`\`

### Initialize a New Project

\`\`\`bash
# Basic project with Hello World
dars init my_new_project

# Project with a specific template
dars init my_project -t basic/Forms
\`\`\`

### View Application Information

\`\`\`bash
dars info my_app.py
\`\`\`

### View Supported Formats

\`\`\`bash
dars formats
\`\`\`

## Post-Installation Verification

To verify that Dars has been installed correctly, open your terminal and run:

\`\`\`bash
dars --help
\`\`\`

You should see the help for the \`dars\` command, indicating that the installation was successful.

## First Steps After Installation

### 1. Create Your First Application (my_first_app.py)

\`\`\`python
from dars.core.app import App
from dars.components.basic.text import Text
from dars.components.basic.container import Container

app = App(title="My First App")
container = Container(style={'padding': '20px'}) # Use ' to escape quotes
text = Text(text="Hello Dars!", style={'font-size': '24px'}) # Use ' to escape quotes

container.add_child(text)
app.set_root(container)
\`\`\`

### 2. Export the Application

Save the code above as \`my_first_app.py\` and then run:

\`\`\`bash
dars export my_first_app.py --format html --output ./my_app
\`\`\`

### 3. Preview

\`\`\`bash
dars preview ./my_app
\`\`\`


### Useful Commands

\`\`\`bash
# General help
dars --help

# Application information
dars info my_app.py

# Available formats
dars formats

# Preview application
dars preview ./output_directory
\`\`\`

## Post-Installation Checklist

- [x] Python 3.8+ installed
- [x] Dars Framework installed via \`pip install dars-framework\`
- [x] CLI \`dars\` works correctly (\`dars --help\`)
- [x] Basic test run successfully
- [x] Example exported and previewed correctly
- [x] Documentation reviewed

Congratulations! Dars is ready to use.

---

## Desktop (BETA)

You can build native desktop apps from Dars projects. This capability is in **BETA** and is not recommended for production yet, but it is usable for testing.

### Quickstart

\`\`\`bash
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
\`\`\`

Notes:
- Desktop support is under active development; configuration keys and defaults may change.
- Some platform targets (like macOS) require building on that OS for signing.
`},{type:"T9",id:"markdown_115",text:`# Getting Started with Dars

Welcome to Dars, a modern Python framework for building web applications with reusable UI components.

## Quick Start

1. **Install Dars**  
   See INSTALL section for installation instructions.

2. **Explore Components**  
   Discover all available UI components in [components.md](#dars-components-documentation).

3. **Command-Line Usage**  
   Find CLI commands, options, and workflows in [cli.md](#dars-cli-reference).

4. **App Class**
   Learn how to create an app class in [App Documentation](#app-class-and-pwa-features-in-dars-framework).

5. **Component Search and Modification**
   All components in Dars now support a powerful search and modification system:

\`\`\`python

   from dars.all import *

   app = App(title="Search Demo")

   # Create a page with nested components
   page = Page(
       Container(
           Text(text="Welcome!", id="welcome-text"),
           Container(
               Button(text="Click me", class_name="action-btn"),
               Button(text="Cancel", class_name="action-btn"),
               id="buttons-container"
           ),
           id="main-container"
       )
   )

   # Find and modify components
   page.find(id="welcome-text")\\
       .attr(text="Welcome to Dars!", style={"color": "blue"})

   # Chain searches to find nested components
   page.find(id="buttons-container")\\
       .find(class_name="action-btn")\\
       .attr(style={"padding": "10px"})

   app.add_page(name="main", root=page)

\`\`\`

7.  **Adding Custom File Types**

\`\`\`python

app.rTimeCompile().add_file_types = ".js,.css"

\`\`\`

* Include any extension your project uses beyond default Python files.

## Need More Help?

- For advanced topics, see the full documentation and examples in the referenced files above.
- If you have questions or need support, check the official repository or community channels.

Start building with Dars...
`},{type:"T9",id:"markdown_116",text:'# Dars Project Configuration\n\nThe file (dars.config.json) configures how Dars exports and builds your project. It is created by `dars init <name>` for new projects and can be merged/updated in existing projects with `dars init --update`.\n\n## Example\n\n```json\n{\n  "entry": "main.py",\n  "format": "html",\n  "outdir": "dist",\n  "publicDir": null,\n  "include": [],\n  "exclude": ["**/__pycache__", ".git", ".venv", "node_modules"],\n  "bundle": false,\n  "defaultMinify": true,\n  "viteMinify": true,\n  "markdownHighlight": true\n}\n```\n\n## Fields\n\n- entry\n  Python entry file for your app. Used by `dars build` and by `dars export config`.\n\n- format\n  Export format. Supported: `html` and `desktop` (BETA). When set to `desktop`, the build command will produce native desktop artifacts.\n\n- outdir\n  Directory where the exported files are written.\n\n- publicDir\n  Directory whose contents are copied as-is into the output (e.g. `public/` or `assets/`). If `null`, Dars will try to autodetect common locations.\n\n- include / exclude\n  Simple filters (by substring) applied when copying from `publicDir`.\n\n- bundle\n  Reserved for future use. Current exporters already produce a bundled output.\n\n- defaultMinify\n  Toggle the built-in Python minifier (safe and conservative). Controls HTML minification and provides JS/CSS fallback when advanced tools are unavailable.\n  - `true` (default): run the default Python-side minifier.\n  - `false`: skip the default minifier. You can still use Vite/esbuild via `viteMinify`.\n\n- viteMinify\n  Toggle the advanced JS minifier.\n  - `true` (default): prefer the advanced minifier; fall back to the secondary minifier; if neither is available, a conservative built-in fallback is used.\n  - `false`: skip the advanced minifier and use the secondary minifier directly; fall back to the conservative built-in if not available.\n\n- markdownHighlight\n  Auto-inject a client-side syntax highlighter for fenced code blocks in Markdown.\n  - `true` (default): injects Prism.js assets once per page and highlights `pre code` blocks.\n  - `false`: no assets injected; you can include your own highlighter or none at all.\n\n## Desktop-specific (BETA)\n\n- targetPlatform\n  Desktop build target. Only effective when `format` is `desktop`.\n  - Values: `auto` (default), `windows`, `linux`, `macos`.\n  - Note: macOS targets must be built on macOS for signing.\n\n> Desktop export is BETA: suitable for testing, not recommended for production yet. Configuration keys and defaults may change.\n\n## Behavior and defaults\n\n- `dars init --update` merges your existing config with Dars defaults and writes the result back, adding any new keys (like `defaultMinify`, `viteMinify`) without removing your current settings.\n- During `dars export` and `dars build`, Dars reads this file and configures the minification pipeline accordingly.\n- If advanced minifiers are not available, builds still complete with a conservative fallback. On `dars build`, a small notice may appear indicating that a less powerful minifier was used.\n- You can force-skip the default Python minifier per run with `--no-minify` (does not affect `viteMinify`).\n\n## Tips\n\n- To add or refresh the config in an existing project:\n  ```bash\n  dars init --update\n  ```\n- To review optional tooling that can enhance bundling/minification, run:\n  ```bash\n  dars doctor\n  ```\n- If you want to force using only the secondary minifier, set `"viteMinify": false`.\n - To disable the default minifier by config, set `"defaultMinify": false`; to disable it per-run use `--no-minify`.\n'},{type:"T9",id:"markdown_117",text:`# App Class and PWA Features in Dars Framework

## Overview

The \`App\` class is the core of any Dars Framework application. It represents the complete application and manages all configuration, components, pages, and functionalities, including Progressive Web App (PWA) support.

## Basic Structure

\`\`\`python
class App:
    def __init__(
        self, 
        title: str = "Dars App",
        description: str = "",
        author: str = "",
        keywords: List[str] = None,
        language: str = "en",
        favicon: str = "",
        icon: str = "",
        apple_touch_icon: str = "",
        manifest: str = "",
        theme_color: str = "#000000",
        background_color: str = "#ffffff",
        service_worker_path: str = "",
        service_worker_enabled: bool = False,
        **config
    ):
\`\`\`

## Global Styles Management

### Enhanced add_global_style() Method

The \`App\` class now includes an enhanced \`add_global_style()\` method that supports both inline style definitions and external CSS file imports.


#### Usage Examples

**1. Inline Style Definition (Traditional)**
\`\`\`python
app.add_global_style(
    selector=".my-button",
    styles={
        "background-color": "#4CAF50",
        "color": "white",
        "padding": "10px 20px",
        "border-radius": "5px"
    }
)
\`\`\`

**2. External CSS File Import (New in v1.1.2)**
\`\`\`python
app.add_global_style(file_path="styles.css")
\`\`\`

**3. Combined Usage**
\`\`\`python
# Add inline styles
app.add_global_style(
    selector=".primary-btn",
    styles={
        "background-color": "#007bff",
        "color": "white"
    }
)

# Import external CSS file
app.add_global_style(file_path="components.css")
\`\`\`

#### Practical Example with External CSS

**main.py:**
\`\`\`python
from dars.all import *

app = App(title="Dars Styling Test")

index = Page(
    Container(
        Button("Styled Button", class_name="button-styling-test"),
        id="page_sub_container"
    )
)

app.add_page(name="index", root=index, title="index", index=True)
app.add_global_style(file_path="styles.css")

if __name__ == "__main__":
    app.rTimeCompile(add_file_types=".py, .css")
\`\`\`

**styles.css:**
\`\`\`css
.button-styling-test {
    background-color: rgb(51, 255, 0);
    padding: 15px 30px;
    border-radius: 8px;
    border: none;
    font-weight: bold;
    cursor: pointer;
}

.button-styling-test:hover {
    background-color: rgb(30, 200, 0);
    transform: scale(1.05);
}

#page_sub_container {
    padding: 20px;
    background-color: #f5f5f5;
    min-height: 100vh;
}
\`\`\`

### Hot Reload for CSS Files

When using \`app.rTimeCompile()\` with the \`add_file_types=".css"\` parameter, the development server automatically watches for changes in CSS files and reloads the application when modifications are detected.

\`\`\`python
# Watch for both Python and CSS file changes
app.rTimeCompile(add_file_types=".py, .css")

# Or watch for CSS files only
app.rTimeCompile(add_file_types=".css")
\`\`\`

### Benefits of External CSS Import

1. **Separation of Concerns**: Keep styles separate from application logic
2. **Better Organization**: Maintain complex stylesheets in dedicated files
3. **Team Collaboration**: Designers and developers can work simultaneously
4. **CSS Preprocessors**: Use SASS, LESS, or other preprocessors
5. **Performance**: Browser caching for external CSS files

### Backward Compatibility

The enhanced method maintains full backward compatibility - existing code using \`add_global_style(selector, styles)\` will continue to work without modification.


## PWA Configuration Properties

The App class includes these PWA-specific properties:

\`\`\`python
# Icons and visual resources
self.favicon = favicon  # Path to traditional favicon
self.icon = icon  # Main icon for PWA (multiple sizes)
self.apple_touch_icon = apple_touch_icon  # Icon for Apple devices
self.manifest = manifest  # Path to manifest.json file

# Colors and theme
self.theme_color = theme_color  # Theme color (#RRGGBB)
self.background_color = background_color  # Background color for splash screens

# Service Worker
self.service_worker_path = service_worker_path  # Path to service worker file
self.service_worker_enabled = service_worker_enabled  # Enable/disable

# Additional PWA configuration
self.pwa_enabled = config.get('pwa_enabled', False)
self.pwa_name = config.get('pwa_name', title)
self.pwa_short_name = config.get('pwa_short_name', title[:12])
self.pwa_display = config.get('pwa_display', 'standalone')
self.pwa_orientation = config.get('pwa_orientation', 'portrait')
\`\`\`

## Meta Tag Generation for PWA

The App class provides methods to generate PWA meta tags:

\`\`\`python
def get_meta_tags(self) -> Dict[str, str]:
    """Returns all meta tags as a dictionary"""
    meta_tags = {}
    
    # Viewport configured for responsiveness
    viewport_parts = []
    for key, value in self.config['viewport'].items():
        if key == 'initial_scale':
            viewport_parts.append(f'initial-scale={value}')
        elif key == 'user_scalable':
            viewport_parts.append(f'user-scalable={value}')
        else:
            viewport_parts.append(f'{key.replace("_", "-")}={value}')
    meta_tags['viewport'] = ', '.join(viewport_parts)
    
    # Specific tags for PWA
    meta_tags['theme-color'] = self.theme_color
    if self.pwa_enabled:
        meta_tags['mobile-web-app-capable'] = 'yes'
        meta_tags['apple-mobile-web-app-capable'] = 'yes'
        meta_tags['apple-mobile-web-app-status-bar-style'] = 'default'
        meta_tags['apple-mobile-web-app-title'] = self.pwa_short_name
    
    return meta_tags
\`\`\`

## Integration with HTML/CSS/JS Exporter

The \`HTMLCSSJSExporter\` uses the PWA configuration from the App class to generate:

1. **manifest.json file** - Progressive web app configuration
2. **Meta tags** - To indicate PWA capabilities in different browsers
3. **Icon references** - For multiple devices and sizes
4. **Service Worker registration** - For offline functionality

### Example of Generated Manifest.json

\`\`\`json
{
  "name": "App Name",
  "short_name": "Short Name",
  "description": "Application description",
  "start_url": "/",
  "display": "standalone",
  "background_color": "#ffffff",
  "theme_color": "#000000",
  "orientation": "portrait",
  "icons": [
    {
      "src": "icon-192x192.png",
      "sizes": "192x192",
      "type": "image/png"
    },
    {
      "src": "icon-512x512.png",
      "sizes": "512x512",
      "type": "image/png"
    }
  ]
}
\`\`\`

### Service Worker Registration Script

The exporter automatically generates code to register the service worker:

\`\`\`javascript
if ('serviceWorker' in navigator && '{service_worker_path}') {
  window.addEventListener('load', function() {
    navigator.serviceWorker.register('{service_worker_path}')
      .then(function(registration) {
        console.log('ServiceWorker registration successful');
      })
      .catch(function(error) {
        console.log('ServiceWorker registration failed: ', error);
      });
  });
}
\`\`\`

## Complete PWA App Configuration Example

\`\`\`python
# Create a complete PWA application
app = App(
    title="My PWA App",
    description="An amazing progressive application",
    author="My Company",
    keywords=["pwa", "webapp", "productivity"],
    language="en",
    favicon="assets/favicon.ico",
    icon="assets/icon-192x192.png",
    apple_touch_icon="assets/apple-touch-icon.png",
    theme_color="#4A90E2",
    background_color="#FFFFFF",
    service_worker_path="sw.js",
    service_worker_enabled=True,
    pwa_enabled=True,
    pwa_name="My App",
    pwa_short_name="MyApp",
    pwa_display="standalone"
)

# Add pages and components
app.add_page("home", HomeComponent(), title="Home", index=True)
app.add_page("about", AboutComponent(), title="About")
\`\`\`

## Implementation Considerations

### Browser Compatibility

Dars Framework's PWA implementation is compatible with:
- Chrome/Chromium (full support)
- Firefox (basic support)
- Safari (limited support on iOS)
- Edge (full support)`},{type:"T9",id:"markdown_118",text:`# State management in Dars (dState, cState, goto, mods)

This document describes the new state system available in Dars 1.1.9.

- dState(name, component|id, states): declares a state tied to a DOM target (component id).
- state(idx=None, goto=None, cComp=False, render=None): triggers a state change from Python by producing a JS inline script.
- cState(idx, mods=[...]): declares rules to execute when entering a state.
- Mod helpers: inc, dec, set, toggle_class, append_text, prepend_text.
- goto: absolute (e.g. 2) or relative ("+1", "-1") state jumps.


## Quick start with states

\`\`\`python
from dars.all import *
from dars.core.state import dState, Mod

app = App(title="State Demo")
label = Text("0", id="Counter")
st = dState("counter", component=label, states=[0,1,2,3])

# Rules on state entry
st.cState(1, mods=[Mod.inc(label, prop='text', by=1)])
st.cState(2, mods=[Mod.dec(label, prop='text', by=1)])
st.cState(3, mods=[Mod.toggle_class(label, name='highlight', on=None)])

# Buttons to navigate
next_btn = Button("Next", on_click=st.state(goto='+1'))
prev_btn = Button("Prev", on_click=st.state(goto='-1'))
\`\`\`

## Mod operations

- inc/dec(target, prop='text', by=1): increments or decrements a numeric value (textContent by default).
- set(target, **attrs): sets attributes; \`text\` sets textContent; \`html\` sets innerHTML; other keys map to element attributes.
- toggle_class(target, name, on=None): toggles a class; when \`on\` is True/False, forces add/remove.
- append_text / prepend_text: concatenates to textContent.

## Cross-state calls with Mod.call

- Use \`Mod.call(target, state=None, goto=None)\` inside a \`cState\` to trigger another \`dState\`.
- \`target\` can be the \`DarsState\` instance or its name (string). Example:

\`\`\`python
txt = dState("txt", id="txt1", states=[0,1])
btn = dState("btn", id="btn1", states=[0,1])

txt.cState(1, mods=[
    Mod.set("txt1", text="Bye"),
    Mod.call(btn, state=1)  # or Mod.call("btn", state=1)
])
\`\`\`

## Immutable default state (index 0)

- State \`0\` is the component's default configuration (as instantiated) and is immutable.
- Authoring-time: \`cState(0, ...)\` is forbidden and raises an error.
- Runtime: switching to state \`0\` restores the initial DOM snapshot (attributes except \`id\`, plus innerHTML) and ignores any rules for state \`0\`.
- This guarantees that returning to \`0\` reverts the UI to its original state.

## Mod.set now supports multiple attributes and event arrays

- You can set multiple properties in one call, e.g.:

\`\`\`python
Mod.set("btn1", text="Don't click it", class_name="warn")
\`\`\`

- Event attributes accept a single script or an array of scripts (executed sequentially). Valid values are:
  - InlineScript, FileScript, dScript, or plain JS strings

\`\`\`python
Mod.set("btn1", on_click=[txt.state(0), dScript(code="console.log('clicked')")])
\`\`\`

- The runtime ensures only one dynamic listener per event is active at a time and cleans it up when returning to state \`0\`.

## Full HTML replacement (custom components)

If you need full HTML replacement on state change:
\`\`\`python
swap_btn = Button(
    "Swap",
    on_click=st.state(2, cComp=True, render=label.mod(text="SWAPPED"))
)
\`\`\`

\`render\` accepts:
- A DeferredAttr produced by \`component.mod(...)\` or \`component.attr(..., defer=True)\`.
- A Component instance (will be rendered to HTML at event time).
- A raw HTML string.

## Runtime behavior

- At export time, state declarations are embedded in the page as a bootstrap JSON.
- The runtime (dars.min.js) registers states with: id, states, current index, and optional rules.
- \`change({...})\` resolves \`goto\`, updates \`current\`, applies \`rules[<state>].mods\` and optional \`rules[<state>].goto\` (single hop), then dispatches a \`CustomEvent('dars:state', ...)\`.

## Best practices

- Keep the label text purely numeric if you plan to use \`inc/dec\` on \`text\`.
- Use \`goto\` in rules to avoid infinite accumulation when staying at the same state.
- Prefer \`mods\` for small changes; use \`cComp=True\` only when you need full HTML replacement.

---`},{type:"T9",id:"markdown_119",text:`# Dars - Components Documentation

---

## Barrel Import

You can now import all main components and modules with a single line:

\`\`\`python
from dars.all import *
\`\`\`

This simplifies integration and improves the developer experience. 
> But if you crate your own components it can cause conflicts with names of your components and built in components if they have the same name.

---

## Introduction to Components

Components are the fundamental elements of Dars that represent UI elements. Each component encapsulates its appearance, behavior, and state, allowing you to create complex interfaces by composing simple elements.

To learn how to create your own custom components, refer to the documentation in [Custom Components](#custom-components-in-dars-framework).

## Event Handling with dScript

Dars provides a powerful way to handle user interactions through the \`dScript\` class. You can attach event handlers to interactive components like \`Button\` and \`Input\` to create dynamic and responsive user interfaces.

For a complete list of available event types and how to use them, refer to the documentation in [Events](#events-in-dars).

### dScript Basic Usage

\`\`\`python
from dars.scripts.dscript import dScript

# Button with click handler
button = Button(
    text="Click me",
    on_click=dScript("""
        function handleClick(event) {
            alert('Button was clicked!');
            // Access the button element
            const button = event.target;
            // Toggle a class on click
            button.classList.toggle('clicked');
        }
    """)
)

# Input with change handler
input_field = Input(
    placeholder="Type something...",
    on_change=dScript("""
        function handleChange(event) {
            console.log('Input value changed to:', event.target.value);
            // Add validation or other logic here
            if (event.target.value.length < 3) {
                event.target.style.borderColor = 'red';
            } else {
                event.target.style.borderColor = 'green';
            }
        }
    """
)
\`\`\`

### Available Events

| Component | Event | Description |
|-----------|-------|-------------|
| \`Button\` | \`on_click\` | Triggered when the button is clicked |
| \`Button\` | \`on_double_click\` | Triggered on double click |
| \`Button\` | \`on_mouse_enter\` | Triggered when mouse enters the button |
| \`Button\` | \`on_mouse_leave\` | Triggered when mouse leaves the button |
| \`Input\` | \`on_change\` | Triggered when input value changes |
| \`Input\` | \`on_key_up\` | Triggered when a key is released |
| \`Input\` | \`on_key_down\` | Triggered when a key is pressed |

### Events and dScriptBest Practices

1. **Use Named Functions**: Makes debugging easier and allows reusing the same function for multiple events.
2. **Keep Handlers Small**: Move complex logic to separate functions in your JavaScript code.
3. **Access Event Object**: The event object provides useful properties like \`target\`, \`keyCode\`, etc.
4. **Return \`false\`** to prevent default behavior when needed.

---

### Quick Access

- [Base Component Class](#base-component-class)
- [Component Search](#component-search-and-modification)
- [Page](#page)
- [Text](#text)
- [Button](#button)
- [Input](#input)
- [Container](#container)
- [Markdown](#markdown)
- [Image](#image)
- [Link](#link)
- [Textarea](#textarea)
- [Checkbox](#checkbox)
- [RadioButton](#radiobutton)
- [Select](#select)
- [Slider](#slider)
- [ProgressBar](#progressBar)
- [Tooltip](#tooltip)
- [DatePicker](#datepicker)
- [Card](#card)
- [Modal](#modal)
- [Navbar](#navbar)
- [Accordion](#accordion)
- [Tabs](#tabs)
- [Table](#table)
- [Layout Components](#layout-components)
  - [GridLayout](#gridlayout)
  - [FlexLayout](#flexlayout)
  - [LayoutBase](#layoutbase)
  - [AnchorPoint](#anchorpoint)

---

## Base Component Class

All components in Dars inherit from the base \`Component\` class, which provides common functionality:

\`\`\`python
from dars.core.component import Component

class Component(ABC):
    def __init__(self, **props):
        self.props = props
        self.children = []
        self.parent = None
        self.id = props.get("id")
        self.class_name = props.get("class_name")
        self.style = props.get("style", {})
        self.events = {}
\`\`\`

### Common Properties

All components support these basic properties:

- **id**: Unique component identifier
- **class_name**: CSS class for additional styles
- **style**: Dictionary of CSS styles
- **children**: List of child components (for containers)

### Component-Search-and-Modification

All components include a powerful search and modification system through the \`find()\` method. This allows you to search for components in the component tree and modify their attributes using a fluent interface.

#### Basic Search

\`\`\`python
# Find by ID
component.find(id="search-button")

# Find by CSS class
component.find(class_name="primary-button")

# Find by component type
component.find(type="Button")  # or type=Button

# Find using a custom predicate
component.find(predicate=lambda c: "welcome" in c.text.lower())
\`\`\`

#### Chained Searches

You can chain multiple \`find()\` calls to search within the results of previous searches:

\`\`\`python
# Find a container and then search within it
component.find(id="main-container")\\
        .find(type="Text")\\
        .attr(text="New text")

# Multiple levels of search
component.find(class_name="section")\\
        .find(type="Container")\\
        .find(id="special-text")\\
        .attr(text="Modified text")
\`\`\`

#### Modifying Components

Use the \`attr()\` method to modify the found components:

\`\`\`python
# Modify styles
component.find(type="Button").attr(
    style={"background-color": "red", "color": "white"}
)

# Modify class names
component.find(class_name="btn").attr(
    class_name="btn primary"
)

# Modify component-specific attributes
component.find(type="Text").attr(
    text="New content"
)

# Multiple modifications at once
component.find(type="Input").attr(
    placeholder="Type here...",
    style={"padding": "10px"},
    class_name="modern-input"
)
\`\`\`

#### Getting Results

\`\`\`python
# Get all matched components
components = component.find(type="Button").get()

# Get only the first match
first_button = component.find(type="Button").first()
\`\`\`

#### Search Parameters

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| \`id\` | str | Search by component ID | \`find(id="search-btn")\` |
| \`class_name\` | str | Search by CSS class | \`find(class_name="primary")\` |
| \`type\` | str/Type | Search by component type | \`find(type="Button")\` or \`find(type=Button)\` |
| \`predicate\` | Callable | Custom search function | \`find(predicate=lambda c: len(c.children) > 0)\` |

### Page

The \`Page\` component represents the root of a multipage app. It can contain other components and scripts specific to that page.

#### Page Syntax

\`\`\`python
from dars.components.basic import Page, Text, Button
from dars.scripts.script import InlineScript
page = Page(
    Text("Bienvenido!"),
    Button("Click aqu\xED", id="btn-demo")
)
# A\xF1adir script JS solo a esta p\xE1gina
page.add_script(InlineScript("""
document.addEventListener('DOMContentLoaded', function() {
    var btn = document.getElementById('btn-demo');
    if (btn) btn.onclick = () => alert('\xA1Bot\xF3n de esta p\xE1gina!');
});
"""))
\`\`\`

Use \`Page\` as the root of each page in the multipage system. Allows passing children directly as arguments and JS scripts per page.

#### Page Properties 

| Property    | Type   | Description                                         |
|-------------|--------|-----------------------------------------------------|
| \`children\`  | list   | List of child components                            |
| \`anchors\`   | dict   | Optional anchor points for child placement          |

#### Page Scripts System

The new page scripts system allows assigning scripts to specific pages instead of globally:

* **Adding Scripts**:
  Use the \`add_script()\` method on a page instance.

\`\`\`python
from dars.scripts.dscript import dScript

index.add_script(
    dScript(code="console.log('Hello world')")
)
\`\`\`

### Text

The \`Text\` component displays static or dynamic text.

#### Text Syntax

\`\`\`python
from dars.components.basic.text import Text

text = Text(
    text="Contenido del text",
    id="mi-text",
    class_name="text-principal",
    style={
        "font-size": "16px",
        "color": "#333",
        "font-weight": "bold"
    }
)
\`\`\`

#### Text Properties

| Property | Type | Description | Example |
|-----------|------|-------------|---------|
| \`text\` | str | Text content | \`"Hello world"\` |
| \`id\` | str | Unique identifier | \`"title-primary"\` |
| \`class_name\` | str | CSS class | \`"text-highlight"\` |
| \`style\` | dict | CSS styles | \`{"color": "red"}\` |

#### Text Common Styles

\`\`\`python
# T\xEDtulo principal
title = Text(
    text="T\xEDtulo Principal",
    style={
        "font-size": "32px",
        "font-weight": "bold",
        "color": "#2c3e50",
        "margin-bottom": "20px",
        "text-align": "center"
    }
)

# P\xE1rrafo de contenido
paragraph = Text(
    text="Este es un p\xE1rrafo de ejemplo con contenido descriptivo.",
    style={
        "font-size": "16px",
        "line-height": "1.6",
        "color": "#34495e",
        "margin-bottom": "15px"
    }
)

# Texto peque\xF1o
note = Text(
    text="Nota: Esta informaci\xF3n es importante.",
    style={
        "font-size": "12px",
        "color": "#7f8c8d",
        "font-style": "italic"
    }
)
\`\`\`

### Button

The \`Button\` component creates interactive buttons that can execute actions.

#### Button Syntax

\`\`\`python
from dars.components.basic.button import Button

boton = Button(
    text="Hacer clic",
    button_type="button",  # "button", "submit", "reset"
    disabled=False,
    on_click=dScript("""
        function handleClick() {
            alert('Button clicked!');
        }
    """)
    style={
        "background-color": "#3498db",
        "color": "white",
        "padding": "10px 20px",
        "border": "none",
        "border-radius": "4px"
    }
)
\`\`\`

#### Button Properties

| Property | Type | Description | Values |
|-----------|------|-------------|---------|
| \`text\` | str | Button text | \`"Enviar"\` |
| \`button_type\` | str | Button type | \`"button"\`, \`"submit"\`, \`"reset"\` |
| \`disabled\` | bool | Si est\xE1 deshabilitado | \`True\`, \`False\` |
| \`on_click\` | dScript | Click handler | \`dScript("function() { ... }")\` |
| \`on_double_click\` | dScript | Double click handler | \`dScript("function() { ... }")\` |
| \`on_mouse_enter\` | dScript | Mouse enter handler | \`dScript("function() { ... }")\` |
| \`on_mouse_leave\` | dScript | Mouse leave handler | \`dScript("function() { ... }")\` |
| \`on_key_up\` | dScript | Key up handler | \`dScript("function(e) { ... }")\` |
| \`on_key_down\` | dScript | Key down handler | \`dScript("function(e) { ... }")\` |

#### Button Examples

\`\`\`python
# Primary Button
primary_button = Button(
    text="Acci\xF3n Principal",
    style={
        "background-color": "#007bff",
        "color": "white",
        "padding": "12px 24px",
        "border": "none",
        "border-radius": "6px",
        "font-size": "16px",
        "font-weight": "500",
        "cursor": "pointer",
        "transition": "background-color 0.3s"
    }
)

# Secondary Button
secondary_button = Button(
    text="Cancelar",
    style={
        "background-color": "transparent",
        "color": "#6c757d",
        "padding": "12px 24px",
        "border": "1px solid #6c757d",
        "border-radius": "6px",
        "font-size": "16px",
        "cursor": "pointer"
    }
)

# Danger Button
delete_button = Button(
    text="Eliminar",
    style={
        "background-color": "#dc3545",
        "color": "white",
        "padding": "8px 16px",
        "border": "none",
        "border-radius": "4px",
        "font-size": "14px"
    }
)

# Disabled Button
disabled_button = Button(
    text="No disponible",
    disabled=True,
    style={
        "background-color": "#e9ecef",
        "color": "#6c757d",
        "padding": "10px 20px",
        "border": "none",
        "border-radius": "4px",
        "cursor": "not-allowed"
    }
)
\`\`\`

### Input

The \`Input\` component allows user data entry.

#### Input Syntax

\`\`\`python
from dars.components.basic.input import Input

entrada = Input(
    value="Valor inicial",
    placeholder="Escribe aqu\xED...",
    input_type="text",  # "text", "password", "email", "number", etc.
    disabled=False,
    readonly=False,
    required=False,
    max_length=100,
    on_change=dScript("""
        function handleChange(event) {
            console.log('Input changed:', event.target.value);
        }
    """)
    style={
        "width": "300px",
        "padding": "10px",
        "border": "1px solid #ddd",
        "border-radius": "4px"
    }
)
\`\`\`

#### Input Properties

| Property | Type | Description | Values |
|-----------|------|-------------|---------|
| \`value\` | str | Initial value | \`"text"\` |
| \`placeholder\` | str | Help text | \`"Ingresa tu name"\` |
| \`input_type\` | str | Tipo de entrada | \`"text"\`, \`"password"\`, \`"email"\`, \`"number"\` |
| \`disabled\` | bool | Si est\xE1 deshabilitado | \`True\`, \`False\` |
| \`readonly\` | bool | Solo lectura | \`True\`, \`False\` |
| \`required\` | bool | Campo obligatorio | \`True\`, \`False\` |
| \`on_change\` | dScript | Change handler | \`dScript("function(e) { ... }")\` |
| \`on_key_up\` | dScript | Key up handler | \`dScript("function(e) { ... }")\` |
| \`on_key_down\` | dScript | Key down handler | \`dScript("function(e) { ... }")\` |
| \`max_length\` | int | Longitud m\xE1xima | \`50\` |
| \`min_length\` | int | Longitud m\xEDnima | \`3\` |
| \`pattern\` | str | Validation pattern | \`"[0-9]+"\` |

#### Input Types

\`\`\`python
# Basic text input
name = Input(
    placeholder="Ingresa tu name",
    input_type="text",
    required=True,
    style={
        "width": "100%",
        "padding": "12px",
        "border": "2px solid #e1e5e9",
        "border-radius": "8px",
        "font-size": "16px"
    }
)

# Email input
email = Input(
    placeholder="tu@email.com",
    input_type="email",
    required=True,
    style={
        "width": "100%",
        "padding": "12px",
        "border": "2px solid #e1e5e9",
        "border-radius": "8px"
    }
)

# Password input
password = Input(
    placeholder="Contrase\xF1a",
    input_type="password",
    required=True,
    min_length=8,
    style={
        "width": "100%",
        "padding": "12px",
        "border": "2px solid #e1e5e9",
        "border-radius": "8px"
    }
)

# Numeric input
edad = Input(
    placeholder="Edad",
    input_type="number",
    style={
        "width": "100px",
        "padding": "8px",
        "border": "1px solid #ccc",
        "border-radius": "4px",
        "text-align": "center"
    }
)

# Search input
busqueda = Input(
    placeholder="Buscar...",
    input_type="search",
    style={
        "width": "300px",
        "padding": "10px 15px",
        "border": "1px solid #ddd",
        "border-radius": "20px",
        "background-color": "#f8f9fa"
    }
)
\`\`\`

### Container

The \`Container\` component is a container that can hold other components. It supports multiple ways to add child components.

#### Container Syntax

\`\`\`python
from dars.components.basic.container import Container

# Method 1: Pass components as arguments
container = Container(
    Text("Hello"),
    Button("Click me"),
    style={
        "display": "flex",
        "flex-direction": "column",
        "padding": "20px",
        "background-color": "#f8f9fa"
    }
)

# Method 2: Use additional_children parameter
components = [Text("Hello"), Button("Click me")]
container = Container(
    additional_children=components,
    style={
        "display": "flex",
        "flex-direction": "column",
        "padding": "20px",
        "background-color": "#f8f9fa"
    }
)

# Method 3: Add children after creation
container = Container(style={
    "display": "flex",
    "flex-direction": "column",
    "padding": "20px",
    "background-color": "#f8f9fa"
})
container.add_child(Text("Hello"))
container.add_child(Button("Click me"))
\`\`\`

#### Container Properties

| Property | Type | Description |
|-----------|------|-------------|
| \`children\` | tuple | Components passed as positional arguments |
| \`additional_children\` | list | Optional list of additional components |

#### Container Layouts

\`\`\`python
# Vertical layout (column)
columna = Container(
    style={
        "display": "flex",
        "flex-direction": "column",
        "gap": "15px",
        "padding": "20px"
    }
)

# Horizontal layout (row)
fila = Container(
    style={
        "display": "flex",
        "flex-direction": "row",
        "gap": "20px",
        "align-items": "center"
    }
)

# Layout centrado
centrado = Container(
    style={
        "display": "flex",
        "justify-content": "center",
        "align-items": "center",
        "min-height": "100vh",
        "background-color": "#f0f2f5"
    }
)

# Card/Tarjeta
tarjeta = Container(
    style={
        "background-color": "white",
        "border-radius": "12px",
        "padding": "24px",
        "box-shadow": "0 2px 10px rgba(0,0,0,0.1)",
        "max-width": "400px",
        "margin": "20px auto"
    }
)

# Sidebar
sidebar = Container(
    style={
        "width": "250px",
        "height": "100vh",
        "background-color": "#2c3e50",
        "padding": "20px",
        "position": "fixed",
        "left": "0",
        "top": "0"
    }
)
\`\`\`

### Markdown

The \`Markdown\` component allows you to render markdown content directly in your Dars applications, converting markdown syntax to beautiful HTML with proper styling.

#### Markdown Syntax

\`\`\`python
from dars.components.basic.markdown import Markdown

# From string content
markdown_component = Markdown(
    content="# Welcome\\nThis is **markdown** content",
    id="my-markdown",
    class_name="custom-markdown",
    style={"padding": "20px"}
)

# From file
markdown_from_file = Markdown(
    file_path="README.md",
    id="documentation",
    dark_theme=True
)
\`\`\`

#### Markdown Properties

| Property | Type | Description | Example |
|-----------|------|-------------|---------|
| \`content\` | str | Markdown content as string | \`"# Heading"\` |
| \`file_path\` | str | Path to a markdown file | \`"docs/intro.md"\` |
| \`dark_theme\` | bool | Enable dark theme styling | \`True\` |
| \`id\` | str | Component ID | \`"markdown-content"\` |
| \`class_name\` | str | CSS class | \`"markdown-body"\` |
| \`style\` | dict | CSS styles | \`{"fontSize": "16px"}\` |

#### Markdown Methods

| Method | Description | Example |
|--------|-------------|---------|
| \`update_content(new_content=None, new_file_path=None)\` | Update markdown content | \`markdown_component.update_content(new_content="# New")\` |
| \`set_dark_theme(enabled=True)\` | Enable/disable dark theme | \`markdown_component.set_dark_theme(True)\` |

#### Markdown Examples

\`\`\`python
# Simple markdown from string
simple_md = Markdown(
    content="# Hello\\nThis is a **markdown** example",
    style={"maxWidth": "800px", "margin": "0 auto"}
)

# Load from file with dark theme
docs_md = Markdown(
    file_path="documentation.md",
    dark_theme=True,
    class_name="docs-content"
)

# Update content dynamically
simple_md.update_content(new_content="# Updated\\nNew content here")
\`\`\`

The Markdown renderer supports fenced code blocks and emits standard \`language-<lang>\` classes, e.g. \`language-python\`.

By default, the exporter auto-injects a client-side highlighter (highlight.js) once per page and highlights all \`pre code\` blocks. This is controlled by \`markdownHighlight\` in \`dars.config.json\`.

Config example:

\`\`\`json
{
  "markdownHighlight": true
}
\`\`\`

- When \`true\` (default), highlight.js CSS/JS + init are added automatically.
- When \`false\`, no assets are injected; include your own highlighter if you want colored code.

Fenced code example:

\`\`\`\`
\`\`\`python
import time
def hello():
    print("hi")
\`\`\`
\`\`\`\`

#### Markdown Dependencies

The Markdown component requires the \`markdown2\` library. Included with the framework.

#### Supported Markdown Features

- Headers (\`#\`, \`##\`, \`###\`)
- **Bold** and *italic* text
- Lists (ordered and unordered)
- [Links](https://github.com/ZtaMDev/Dars-Framework)
- \`Inline code\` and code blocks
- Tables
- Blockquotes
- Images
- Horizontal rules

#### Markdown Styling

The Markdown component includes comprehensive default styling for both light and dark themes:

\`\`\`python
# Light theme (default)
markdown_light = Markdown(content="# Light theme")

# Dark theme
markdown_dark = Markdown(
    content="# Dark theme", 
    dark_theme=True,
    style={"padding": "20px", "borderRadius": "8px"}
)
\`\`\`

#### Markdown Best Practices

1. Use file paths for large documentation content
2. Enable dark theme for better readability in low-light environments
3. Combine with layout components for responsive designs
4. Use the update methods for dynamic content changes

#### Markdown Integration Example

\`\`\`python
from dars.core.app import App
from dars.components.basic.markdown import Markdown
from dars.components.basic.container import Container

app = App(title="Documentation Viewer")

# Load documentation from file
docs = Markdown(
    file_path="README.md",
    dark_theme=True,
    class_name="documentation",
    style={
        "maxWidth": "800px",
        "margin": "0 auto",
        "padding": "40px",
        "lineHeight": "1.6"
    }
)

app.set_root(Container(children=[docs]))
\`\`\`

This component is perfect for creating documentation pages, blog posts, content management systems, and any application that needs to display formatted text content.

### Image

The \`Image\` component displays images.

#### Image Syntax

\`\`\`python
from dars.components.basic.image import Image

image = Image(
    src="path/to/your/image.jpg",
    alt="Descripci\xF3n de la image",
    width="300px",
    height="200px",
    class_name="responsive-img",
    style={
        "border-radius": "8px",
        "box-shadow": "0 4px 8px rgba(0,0,0,0.1)"
    }
)
\`\`\`

#### Image Properties

| Property | Type | Description | Example |
|-----------|------|-------------|---------|
| \`src\` | str | Image path | \`"images/logo.png"\` |
| \`alt\` | str | Alternative text | \`"Logo of the company"\` |
| \`width\` | str | Ancho de la image (CSS) | \`"100%"\`, \`"200px"\` |
| \`height\` | str | Alto de la image (CSS) | \`"auto"\`, \`"150px"\` |

### Link

The \`Link\` component creates navigation links.

#### Link Syntax

\`\`\`python
from dars.components.basic.link import Link

link = Link(
    text="Visitar Google",
    href="https://www.google.com",
    target="_blank", # Abre en una nueva pesta\xF1a
    class_name="external-link",
    style={
        "color": "#007bff",
        "text-decoration": "none",
        "font-weight": "bold"
    }
)
\`\`\`

#### Link Properties

| Property | Type | Description | Values |
|-----------|------|-------------|---------|
| \`text\` | str | Link text | \`"Ir a la p\xE1gina"\` |
| \`href\` | str | URL of destination | \`"/about"\`, \`"https://example.com"\` |
| \`target\` | str | D\xF3nde abrir el link | \`"_self"\` (misma pesta\xF1a), \`"_blank"\` (nueva pesta\xF1a) |

### Textarea

The \`Textarea\` component allows for multi-line text input.

#### Textarea Syntax

\`\`\`python
from dars.components.basic.textarea import Textarea

area_text = Textarea(
    value="Texto inicial",
    placeholder="Escribe tu mensaje aqu\xED...",
    rows=5,
    cols=40,
    disabled=False,
    readonly=False,
    required=True,
    max_length=500,
    class_name="comment-box",
    style={
        "width": "100%",
        "padding": "10px",
        "border": "1px solid #ccc",
        "border-radius": "5px"
    }
)
\`\`\`

#### Textarea Properties

| Property | Type | Description | Values |
|-----------|------|-------------|---------|
| \`value\` | str | Initial value | \`""\` |
| \`placeholder\` | str | Help text | \`"Escribe aqu\xED..."\` |
| \`rows\` | int | N\xFAmero de filas visibles | \`4\` |
| \`cols\` | int | N\xFAmero de columnas visibles | \`50\` |
| \`disabled\` | bool | Si est\xE1 deshabilitado | \`True\`, \`False\` |
| \`readonly\` | bool | Solo lectura | \`True\`, \`False\` |
| \`required\` | bool | Campo obligatorio | \`True\`, \`False\` |
| \`max_length\` | int | Longitud m\xE1xima | \`500\` |


---

### ProgressBar

The \`ProgressBar\` component visually displays progress for a task, such as loading or completion percentage.

#### ProgressBar Syntax

\`\`\`python
from dars.components.basic.progressbar import ProgressBar

progress = ProgressBar(value=40, max_value=100)
\`\`\`

#### ProgressBar Properties

| Property    | Type | Description                       |
|-------------|------|-----------------------------------|
| \`value\`     | int  | Current progress value            |
| \`max_value\` | int  | Maximum value (default: 100)      |

#### ProgressBar Example

\`\`\`python
progress = ProgressBar(value=75, max_value=100)
\`\`\`

---

### Tooltip

The \`Tooltip\` component displays a tooltip when hovering over a child component.

#### Tooltip Syntax

\`\`\`python
from dars.components.basic.tooltip import Tooltip
from dars.components.basic.button import Button

tooltip = Tooltip(
    text="More info",
    child=Button(text="Hover me")
)
\`\`\`

#### Tooltip Properties

| Property   | Type      | Description                             |
|------------|-----------|-----------------------------------------|
| \`text\`     | str       | Tooltip text                            |
| \`child\`    | Component | Component to wrap                       |
| \`position\` | str       | Tooltip position (e.g., "top")          |

#### Tooltip Example

\`\`\`python
tooltip = Tooltip(text="Help", child=Button(text="?"))
\`\`\`

---

### Accordion

The \`Accordion\` component creates a vertically stacked set of expandable/collapsible panels for organizing content.

#### Accordion Syntax

\`\`\`python
from dars.components.advanced.accordion import Accordion

accordion = Accordion(
    items=[
        {"title": "Section 1", "content": "Content for section 1"},
        {"title": "Section 2", "content": "Content for section 2"}
    ],
    allow_multiple=False
)
\`\`\`

#### Accordion Properties

| Property         | Type    | Description                                         |
|------------------|---------|-----------------------------------------------------|
| \`items\`          | list    | List of dicts with \`title\` and \`content\`            |
| \`allow_multiple\` | bool    | Allow multiple sections open at once                |

#### Accordion Example

\`\`\`python
accordion = Accordion(
    items=[
        {"title": "FAQ 1", "content": "Answer 1"},
        {"title": "FAQ 2", "content": "Answer 2"}
    ]
)
\`\`\`

---

### Tabs

The \`Tabs\` component allows navigation between different views or content panels.

> **New in 1.0.5:** The exporter now recursively detects Tabs at any nesting level (including inside containers, panels, or multipage apps) for \`minimum_logic\` and JS injection. You can safely nest Tabs in any structure and the export will work as expected.


#### Tabs Syntax

\`\`\`python
from dars.components.advanced.tabs import Tabs

tabs = Tabs(
    tabs=[
        {"label": "Tab 1", "content": "Content 1"},
        {"label": "Tab 2", "content": "Content 2"}
    ],
    default_index=0
)
\`\`\`

#### Tabs Properties

| Property        | Type | Description                              |
|-----------------|------|------------------------------------------|
| \`tabs\`          | list | List of dicts with \`label\` and \`content\` |
| \`default_index\` | int  | Index of the initially selected tab      |

#### Tabs Example

\`\`\`python
tabs = Tabs(
    tabs=[
        {"label": "Overview", "content": "Main content"},
        {"label": "Details", "content": "Detailed info"}
    ],
    default_index=0
)
\`\`\`

---

### Table

The \`Table\` component displays tabular data with rows and columns.

#### Table Syntax

\`\`\`python
from dars.components.advanced.table import Table

table = Table(
    columns=["Name", "Age", "Country"],
    data=[
        ["Alice", 30, "USA"],
        ["Bob", 25, "UK"]
    ]
)
\`\`\`

#### Table Properties

| Property   | Type   | Description                       |
|------------|--------|-----------------------------------|
| \`columns\`  | list   | List of column headers            |
| \`data\`     | list   | List of rows (each a list/tuple)  |

#### Table Example

\`\`\`python
table = Table(
    columns=["Product", "Price"],
    data=[
        ["Book", "$10"],
        ["Pen", "$2"]
    ]
)
\`\`\`

---

## Layout Components

### GridLayout

The \`GridLayout\` component provides a responsive grid-based layout with customizable rows, columns, gaps, and anchor points for precise positioning of children.

#### GridLayout Syntax

\`\`\`python
from dars.components.layout.grid import GridLayout
from dars.components.basic.text import Text

grid = GridLayout(
    rows=2,
    cols=2,
    gap="24px",
    children=[
        Text("Top Left"),
        Text("Top Right"),
        Text("Bottom Left"),
        Text("Bottom Right")
    ]
)
\`\`\`

#### GridLayout Properties

| Property   | Type   | Description                                 |
|------------|--------|---------------------------------------------|
| \`rows\`     | int    | Number of grid rows                         |
| \`cols\`     | int    | Number of grid columns                      |
| \`gap\`      | str    | Gap between grid cells (e.g., "16px")      |
| \`children\` | list   | List of child components                    |
| \`anchors\`  | dict   | Optional anchor points for child placement  |

#### GridLayout Example

\`\`\`python
grid = GridLayout(
    rows=3,
    cols=2,
    gap="16px",
    children=[Text(f"Cell {i}") for i in range(6)]
)
\`\`\`

---

### FlexLayout

The \`FlexLayout\` component provides a responsive flexbox layout, supporting direction, wrap, alignment, and gap between children. Useful for row/column layouts.

#### FlexLayout Syntax

\`\`\`python
from dars.components.layout.flex import FlexLayout
from dars.components.basic.button import Button

flex = FlexLayout(
    direction="row",
    justify="space-between",
    align="center",
    gap="12px",
    children=[Button("A"), Button("B"), Button("C")]
)
\`\`\`

#### FlexLayout Properties

| Property    | Type   | Description                                         |
|-------------|--------|-----------------------------------------------------|
| \`direction\` | str    | Flex direction: "row" or "column"                   |
| \`wrap\`      | str    | Flex wrap: "wrap" or "nowrap"                       |
| \`justify\`   | str    | Justify content: e.g., "flex-start", "center"      |
| \`align\`     | str    | Align items: e.g., "stretch", "center"             |
| \`gap\`       | str    | Gap between children (e.g., "16px")                |
| \`children\`  | list   | List of child components                            |
| \`anchors\`   | dict   | Optional anchor points for child placement          |

#### FlexLayout Example

\`\`\`python
flex = FlexLayout(
    direction="column",
    gap="24px",
    children=[Button("Save"), Button("Cancel")]
)
\`\`\`

---

### LayoutBase

The \`LayoutBase\` component is the base class for all layout components. It allows adding children and anchor/positioning info. You typically use \`FlexLayout\` or \`GridLayout\` directly.

#### LayoutBase Syntax

\`\`\`python
from dars.components.layout.grid import LayoutBase
from dars.components.basic.text import Text

layout = LayoutBase(
    children=[Text("Item 1"), Text("Item 2")],
    anchors={}
)
\`\`\`

#### LayoutBase Properties

| Property    | Type   | Description                    |
|-------------|--------|--------------------------------|
| \`children\`  | list   | List of child components       |
| \`anchors\`   | dict   | Anchor/positioning information |

---

### AnchorPoint

The \`AnchorPoint\` class represents an anchor or alignment point for a child in a layout (e.g., top, left, right, bottom, center, percent, or px).

#### AnchorPoint Syntax

\`\`\`python
from dars.components.layout.anchor import AnchorPoint

anchor = AnchorPoint(x="left", y="top", name="top-left")
\`\`\`

#### AnchorPoint Properties

| Property | Type | Description                                      |
|----------|------|--------------------------------------------------|
| \`x\`      | str  | Horizontal alignment (e.g., "left", "center")    |
| \`y\`      | str  | Vertical alignment (e.g., "top", "center")       |
| \`name\`   | str  | Optional semantic name for the anchor            |

#### AnchorPoint Example

\`\`\`python
anchor = AnchorPoint(x="50%", y="50%", name="center")
\`\`\`

---

### Card

The \`Card\` component is a styled container to group related content, such as a title and other components.

#### Card Syntax

\`\`\`python
from dars.components.basic.card import Card
from dars.components.basic.text import Text
from dars.components.basic.button import Button

my_card = Card(
    title="T\xEDtulo de la Tarjeta",
    children=[
        Text("Este es el contenido de la tarjeta."),
        Button("Ver m\xE1s")
    ],
    class_name="product-card",
    style={
        "background-color": "#ffffff",
        "border": "1px solid #e0e0e0",
        "border-radius": "10px",
        "padding": "20px",
        "box-shadow": "0 4px 8px rgba(0,0,0,0.05)"
    }
)
\`\`\`

#### Card Properties

| Property | Type | Description |
|-----------|------|-------------|
| \`title\` | str | Card title |
| \`children\` | list | List of child components |

#### Card Example

\`\`\`python
my_card = Card(
    title="T\xEDtulo de la Tarjeta",
    children=[
        Text("Este es el contenido de la tarjeta."),
        Button("Ver m\xE1s")
    ],
    class_name="product-card",
    style={
        "background-color": "#ffffff",
        "border": "1px solid #e0e0e0",
        "border-radius": "10px",
        "padding": "20px",
        "box-shadow": "0 4px 8px rgba(0,0,0,0.05)"
    }
)
\`\`\`

---

### Modal

The \`Modal\` component creates an overlay window that appears on top of the main page content.

> **New in 1.0.5:** Modal is now exported as hidden by default (\`hidden\` attribute and \`dars-modal-hidden\` class) if \`is_open=False\`, preventing any visual flicker on page load, even if CSS/JS loads slowly.

#### Modal Syntax

\`\`\`python
from dars.components.advanced.modal import Modal
from dars.components.basic.text import Text
from dars.components.basic.button import Button

my_modal = Modal(
    title="Welcome to the Modal",
    is_open=False, # Now hidden from the very first render
    children=[
        Text("This is your modal content."),
        Button("Close")
    ],
    class_name="welcome-modal",
    style={
        "background-color": "rgba(0, 0, 0, 0.7)" # Overlay style
    }
)
\`\`\`

#### Modal Properties

| Property   | Type | Description |
|------------|------|------------------------------------------------------------|
| \`title\`    | str  | Modal title |
| \`is_open\`  | bool | Controls modal visibility (\`True\` to show, \`False\` to hide). If \`False\`, modal is hidden from exported HTML. |
| \`children\` | list | List of child components |

#### Modal Updated Example

\`\`\`python
my_modal = Modal(
    title="Welcome to the Modal",
    is_open=False,  # Hidden from the very first render
    children=[
        Text("This is your modal content."),
        Button("Close")
    ],
    class_name="welcome-modal",
    style={
        "background-color": "rgba(0, 0, 0, 0.7)"
    }
)
\`\`\`

> **Note:** The exporter now recursively detects advanced components (Tabs, Accordion, Modal, Card) at any nesting level, including inside multipage apps, and applies \`minimum_logic\` robustly.

---

### Navbar

The \`Navbar\` component creates a navigation bar, commonly used at the top of pages.

#### Navbar Syntax

\`\`\`python
from dars.components.advanced.navbar import Navbar
from dars.components.basic.link import Link

my_navbar = Navbar(
    brand="Mi App",
    children=[
        Link("Inicio", "/"),
        Link("Acerca de", "/about"),
        Link("Contacto", "/contact")
    ],
    class_name="main-nav",
    style={
        "background-color": "#333",
        "color": "white",
        "padding": "15px 20px"
    }
)
\`\`\`

#### Navbar Properties

| Property | Type | Description |
|-----------|------|-------------|
| \`brand\` | str | Texto o componente para la marca/logo de la navegaci\xF3n |
| \`children\` | list | List of child components (navigation items, usually \`Link\`s) |

## Additional Components

### Checkbox

The \`Checkbox\` component allows users to select options.

#### Checkbox Syntax

\`\`\`python
from dars.components.basic.checkbox import Checkbox

mi_checkbox = Checkbox(
    label="Acepto t\xE9rminos",
    checked=True,
    style={
        "margin": "10px"
    }
)
\`\`\`

#### Checkbox Properties

| Property | Type | Description | Values |
|-----------|------|-------------|---------|
| \`label\` | str | Texto de la etiqueta | \`"Acepto t\xE9rminos"\` |
| \`checked\` | bool | Estado de selecci\xF3n | \`True\`, \`False\` |

### RadioButton

The \`RadioButton\` component allows users to select one option from a group of options.

#### RadioButton Syntax

\`\`\`python
from dars.components.basic.radio_button import RadioButton

mi_radio_button = RadioButton(
    label="Opci\xF3n A",
    name="grupo1",
    checked=False,
    style={
        "margin": "10px"
    }
)
\`\`\`

#### RadioButton Properties

| Property | Type | Description | Values |
|-----------|------|-------------|---------|
| \`label\` | str | Texto de la etiqueta | \`"Opci\xF3n A"\` |
| \`name\` | str | Nombre del grupo de radio buttons | \`"grupo1"\` |
| \`checked\` | bool | Estado de selecci\xF3n | \`True\`, \`False\` |

### Select

The \`Select\` component allows users to select one option from a group of options.

#### Select Syntax

\`\`\`python
from dars.components.basic.select import Select

mi_select = Select(
    options=["Uno", "Dos", "Tres"],
    value="Dos",
    style={
        "width": "200px",
        "padding": "10px",
        "border": "1px solid #ccc"
    }
)
\`\`\`

#### Select Properties

| Property | Type | Description | Values |
|-----------|------|-------------|---------|
| \`options\` | list | List of options | \`["Uno", "Dos", "Tres"]\` |
| \`value\` | str | Selected value | \`"Dos"\` |

### Slider

The \`Slider\` component allows users to select a value within a range.

#### Slider Syntax

\`\`\`python
from dars.components.basic.slider import Slider

mi_slider = Slider(
    min_value=0,
    max_value=100,
    value=50,
    show_value=True,
    style={
        "width": "200px",
        "padding": "10px"
    }
)
\`\`\`

#### Slider Properties

| Property | Type | Description | Values |
|-----------|------|-------------|---------|
| \`min_value\` | int | Minimum value | \`0\` |
| \`max_value\` | int | Maximum value | \`100\` |
| \`value\` | int | Valor selectado | \`50\` |
| \`show_value\` | bool | Mostrar el valor selectado | \`True\`, \`False\` |


### DatePicker

The \`DatePicker\` component allows users to select a date.

#### DatePicker Syntax

\`\`\`python
from dars.components.basic.date_picker import DatePicker

mi_date_picker = DatePicker(
    value="2025-08-06",
    style={
        "width": "200px",
        "padding": "10px",
        "border": "1px solid #ccc"
    }
)
\`\`\`

#### DatePickerProperties

| Property | Type | Description | Values |
|-----------|------|-------------|---------|
| \`value\` | str | Selected date | \`"2025-08-06"\` |

## Styling System

### Supported Style Properties

Dars supports most standard CSS properties:

#### Dimensions
- \`width\`, \`height\`
- \`min-width\`, \`min-height\`
- \`max-width\`, \`max-height\`

#### Spacing
- \`margin\`, \`margin-top\`, \`margin-right\`, \`margin-bottom\`, \`margin-left\`
- \`padding\`, \`padding-top\`, \`padding-right\`, \`padding-bottom\`, \`padding-left\`

#### Colors
- \`background-color\`
- \`color\`
- \`border-color\`

#### Typography
- \`font-size\`, \`font-family\`, \`font-weight\`, \`font-style\`
- \`text-align\`, \`text-decoration\`, \`line-height\`

#### Borders
- \`border\`, \`border-width\`, \`border-style\`, \`border-radius\`

#### Layout
- \`display\`, \`position\`
- \`top\`, \`right\`, \`bottom\`, \`left\`, \`z-index\`

#### Flexbox
- \`flex-direction\`, \`flex-wrap\`
- \`justify-content\`, \`align-items\`, \`align-content\`
- \`flex\`, \`flex-grow\`, \`flex-shrink\`, \`flex-basis\`

#### Grid
- \`grid-template-columns\`, \`grid-template-rows\`
- \`grid-gap\`, \`grid-column\`, \`grid-row\`

#### Effects
- \`opacity\`, \`box-shadow\`, \`transform\`, \`transition\`

### Advanced Style Examples

\`\`\`python
# Gradiente de fondo
gradiente = Container(
    style={
        "background": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
        "min-height": "100vh",
        "display": "flex",
        "align-items": "center",
        "justify-content": "center"
    }
)

# Animaci\xF3n de hover (para web)
boton_animado = Button(
    text="Hover me",
    style={
        "background-color": "#3498db",
        "color": "white",
        "padding": "15px 30px",
        "border": "none",
        "border-radius": "8px",
        "transition": "all 0.3s ease",
        "transform": "translateY(0)",
        "box-shadow": "0 4px 15px rgba(52, 152, 219, 0.3)"
    }
)

# Layout de grid
grid_container = Container(
    style={
        "display": "grid",
        "grid-template-columns": "repeat(auto-fit, minmax(250px, 1fr))",
        "grid-gap": "20px",
        "padding": "20px"
    }
)

# Responsive design
responsive_container = Container(
    style={
        "width": "100%",
        "max-width": "1200px",
        "margin": "0 auto",
        "padding": "0 20px"
    }
)
\`\`\`



## Best Practices Styling

### Component Organization

\`\`\`python
def create_header():
    return Container(
        children=[
            Text("My Application", style={"font-size": "24px", "font-weight": "bold"}),
            Text("Descriptive subtitle", style={"color": "#666"})
        ],
        style={
            "padding": "20px",
            "background-color": "#f8f9fa",
            "border-bottom": "1px solid #dee2e6"
        }
    )

def create_form():
    return Container(
        children=[
            Text("Contact Form", style={"font-size": "20px", "margin-bottom": "20px"}),
            Input(placeholder="Name", style={"margin-bottom": "10px"}),
            Input(placeholder="Email", input_type="email", style={"margin-bottom": "10px"}),
            Button("Send", style={"background-color": "#007bff", "color": "white"})
        ],
        style={
            "max-width": "400px",
            "margin": "20px auto",
            "padding": "20px"
        }
    )
\`\`\`

### Style Reuse

\`\`\`python
# Define common styles
BASE_BUTTON_STYLES = {
    "padding": "10px 20px",
    "border": "none",
    "border-radius": "4px",
    "font-size": "14px",
    "cursor": "pointer"
}

PRIMARY_BUTTON_STYLES = {
    **BASE_BUTTON_STYLES,
    "background-color": "#007bff",
    "color": "white"
}

SECONDARY_BUTTON_STYLES = {
    **BASE_BUTTON_STYLES,
    "background-color": "#6c757d",
    "color": "white"
}

# Use in components
cancel_button = Button("Cancelar", style=SECONDARY_BUTTON_STYLES)
save_button = Button("Guardar", style=PRIMARY_BUTTON_STYLES)
\`\`\`

Components provide a solid foundation for creating modern and responsive user interfaces that can be exported to multiple platforms while maintaining consistency and functionality.

`},{type:"T9",id:"markdown_120",text:`# Custom Components in Dars Framework

This is an example of how to create a custom component in Dars. The \`Button\` class inherits from \`Component\` and defines its own initialization and rendering logic. You can use \`self.set_event\` to attach event handlers to components.

> Note: when you instance a CustomComponent you need to do it like this CustomComponent(id="") <-- with parentesis

\`\`\`python
from dars.all import *
from dars.core.component import Component
from dars.exporters.web.html_css_js import *

class CustomComponent(Component):
    def __init__(self, title: str, id: str = None, **props):
        super().__init__(**props)
        
        self.title = title
        self.id = id
        self.set_event(EventTypes.CLICK, dScript("console.log('click')"))
    def render(self, exporter: 'Exporter') -> str:
        # Use the exporter to consistently render children
        children_html = self.render_children(exporter)
        return f'''
        <div class="my-component" id="{self.id}">
            <h2>{self.title}</h2>
            <div class="content">
                {children_html}
            </div>
        </div>
        '''
\`\`\`

`},{type:"T9",id:"markdown_121",text:`# Events in Dars

This is the documentation for the events in Dars.

## Event Calling System

Custom components in Dars can have events associated with them. You can set an event on a custom component using the \`set_event\` method.

\`\`\`python
self.set_event(EventTypes.CLICK, dScript("console.log('click')"))
\`\`\`

### Available Event Types

To use the event types, you need to import them from \`dars.core.events\`:

\`\`\`python
from dars.core.events import EventTypes
\`\`\`

Here are the different event types available:

- **Mouse Events:**
    - \`CLICK = "click"\`
    - \`DOUBLE_CLICK = "dblclick"\`
    - \`MOUSE_DOWN = "mousedown"\`
    - \`MOUSE_UP = "mouseup"\`
    - \`MOUSE_ENTER = "mouseenter"\`
    - \`MOUSE_LEAVE = "mouseleave"\`
    - \`MOUSE_MOVE = "mousemove"\`

- **Keyboard Events:**
    - \`KEY_DOWN = "keydown"\`
    - \`KEY_UP = "keyup"\`
    - \`KEY_PRESS = "keypress"\`

- **Form Events:**
    - \`CHANGE = "change"\`
    - \`INPUT = "input"\`
    - \`SUBMIT = "submit"\`
    - \`FOCUS = "focus"\`
    - \`BLUR = "blur"\`

- **Load Events:**
    - \`LOAD = "load"\`
    - \`ERROR = "error"\`
    - \`RESIZE = "resize"\`


---

## New in v1.2.2: Event arrays and dynamic handlers

- Any \`on_*\` attribute can now accept:
  - A single script (InlineScript, FileScript, dScript) or plain JS string
  - An array mixing any of the above (executed sequentially)

Example using \`Mod.set\`:

\`\`\`python
Mod.set("btn1", on_click=[st1.state(0), dScript(code="console.log('clicked')")])
\`\`\`

Runtime behavior:

- Only one dynamic listener per event is active at a time; subsequent \`Mod.set\` replaces the previous one.
- Dynamic handlers run in capture phase and stop propagation for the same event.
- Returning to the default state (index 0) removes any dynamic listeners from that element and restores its initial DOM.

`},{type:"T9",id:"markdown_122",text:`# Dars - Exporter Documentation

## Introduction

Exporters are the heart of Dars that allow transforming applications written in Python to different technologies and platforms. Each exporter translates Dars components, styles, and scripts to the native code of the target platform.

## Exporter Architecture

### Base Exporter Class

All exporters inherit from the base \`Exporter\` class:

\`\`\`python
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
\`\`\`

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

\`\`\`bash
dars export my_app.py --format html --output ./dist
\`\`\`

#### Generated Structure

\`\`\`
dist/
\u251C\u2500\u2500 index.html      # Main page
\u251C\u2500\u2500 styles.css      # CSS styles
\u2514\u2500\u2500 script.js       # JavaScript logic
\`\`\`

#### Example Output

**index.html**
\`\`\`html
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
    <script src="script.js"><\/script>
</body>
</html>
\`\`\`

**styles.css**
\`\`\`css
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
\`\`\`

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

\`\`\`python
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
\`\`\`

## Desktop Export (BETA)

The desktop exporter allows you to package your Dars app as a native desktop application. This feature is currently in BETA: usable for testing and internal tooling, but not recommended for production deployments yet.

### Status and Scope

- BETA: Many options and integrations are still evolving (advanced packaging, signing, etc.).
- Cross\u2011platform targets supported: Windows, Linux, macOS (host restrictions apply for macOS signing, and linux if you don't have docker).
- Underlying tech: Electron is used to deliver a native desktop container for your web UI.
- Hot Reload: \`dars dev\` with desktop apps is fully supported, but for now it closes and reopen the electron dev app when a file change is detected.
### Quickstart desktop Export

1. Initialize or update your project for desktop:

   \`\`\`bash
   dars init --type desktop
   # or if you already have a project
   dars init --update
   \`\`\`

2. Ensure your project config has desktop format:

   \`\`\`json
   {
     "entry": "main.py",
     "format": "desktop",
     "outdir": "dist",
     "targetPlatform": "auto"
   }
   \`\`\`

3. Verify optional tooling (Node/Bun, Electron, electron\u2011builder):

   \`\`\`bash
   dars doctor --all --yes
   \`\`\`

4. Build your desktop app:

   \`\`\`bash
   dars build
   \`\`\`

Artifacts will be placed in \`dist/\`. The desktop source (used for packaging) is emitted to \`dist/source-electron/\`.

### Native Functions

You can acces native functions via \`dars.desktop\` module:

\`\`\`python
from dars.desktop import *
\`\`\`

With this module you can acces for now 2 main functions:

\`\`\`python 
write_text("./app/lib/hello.txt", "Hello Text")
\`\`\`
and

\`\`\`python
read_text("./app/lib/hello.txt")
\`\`\`

This two functions allows you to read and write text files in your desktop application filesystem, both returns an dScript() with the code to be executed in the desktop app.
also you can use dScripts to run custom javascript code in the desktop app. and for now 'dars dev' is supported but python main.py with rTimeCompile() is not supported because it have issues with relative paths and also it can be used in events of any component.

### Platform Targeting

- \`targetPlatform\`: \`auto\` | \`windows\` | \`linux\` | \`macos\`.
- On non\u2011mac hosts, building for macOS is not supported.

### Metadata and Packaging Notes

- App metadata is taken from your \`App\` instance when available: title, description, author, version.
- If version is not set, a default \`0.1.0\` is used and a warning is shown.
- Package manager and Electron version are pinned by the exporter to make builds predictable.

### Caveats (BETA)

- Not yet recommended for production.
- Some advanced packaging and signing options may require manual configuration.
- Expect changes to configuration keys and defaults as the feature matures.
`},{type:"T9",id:"markdown_123",text:`# Dars - Script System

## Introduction to Scripts

The script system of Dars allows adding interactive logic and dynamic behaviors to applications. Scripts are written in JavaScript and seamlessly integrate with UI components.

## Fundamentals of Scripts

### What are Scripts?

Scripts in Dars are fragments of JavaScript code that:

- Handle user interface events
- Implement client-side business logic
- Provide advanced interactivity
- Run in the context of the exported application

### Types of Scripts

Dars supports three main types of scripts:

1. **InlineScript**: Code defined directly in Python
2. **FileScript**: Code loaded from external files
3. **dScript**: Flexible script that can be defined either inline (as a string) or as a reference to an external file. Only one mode is allowed at a time.

## Base Script Class

All scripts inherit from the base \`Script\` class:

\`\`\`python
from abc import ABC, abstractmethod

class Script(ABC):
    def __init__(self):
        pass
        
    @abstractmethod
    def get_code(self) -> str:
        """Retorna el c\xF3digo del script"""
        pass
\`\`\`

## dScript

### When to use dScript

dScript is a flexible class that allows you to define a script as either:
- Inline JavaScript (via the \`code\` argument)
- Or as a reference to an external file (via the \`file_path\` argument)

But **never both at the same time**. This is useful for presets, user-editable actions, and advanced integrations.

### Basic Syntax

\`\`\`python
from dars.scripts.dscript import dScript

# Inline JS
script_inline = dScript(code="""
function hello() { alert('Hello from dScript!'); }
document.addEventListener('DOMContentLoaded', hello);
""")

# External file
script_file = dScript(file_path="./scripts/my_script.js")
\`\`\`

### Example: Editable JS preset from Python

\`\`\`python
from dars.scripts.dscript import dScript

custom_action = dScript(code="""
function customClick() {
    alert('Custom action from preset!');
}
document.addEventListener('DOMContentLoaded', function() {
    var btn = document.getElementById('my-btn');
    if (btn) btn.onclick = customClick;
});
""")

app.add_script(custom_action)
\`\`\`

## InlineScript

### Basic Syntax InlineScript

\`\`\`python
from dars.scripts.script import InlineScript

script = InlineScript("""
function saludar() {
    alert('\xA1Hola desde Dars!');
}

document.addEventListener('DOMContentLoaded', function() {
    console.log('Aplicaci\xF3n cargada');
});
""")
\`\`\`

### Practical Examples

#### Button Event Handling

\`\`\`python
script_botones = InlineScript("""
// Function to handle button clicks
function manejarClickBoton(evento) {
    const boton = evento.target;
    const texto = boton.textContent;
    
    console.log(\`Button pressed: \${texto}\`);
    
    // Change text temporarily
    const textoOriginal = boton.textContent;
    boton.textContent = '\xA1Presionado!';
    boton.disabled = true;
    
    setTimeout(() => {
        boton.textContent = textoOriginal;
        boton.disabled = false;
    }, 1000);
}

// Add events to all buttons
document.addEventListener('DOMContentLoaded', function() {
    const botones = document.querySelectorAll('button');
    botones.forEach(boton => {
        boton.addEventListener('click', manejarClickBoton);
    });
});
""")
\`\`\`

#### Form Validation

\`\`\`python
script_validacion = InlineScript("""
// Form validation
function validarFormulario() {
    const inputs = document.querySelectorAll('input[required]');
    let esValido = true;
    
    inputs.forEach(input => {
        if (!input.value.trim()) {
            mostrarError(input, 'This field is required');
            esValido = false;
        } else {
            limpiarError(input);
        }
        
        // Specific type validation
        if (input.type === 'email' && input.value) {
            const emailRegex = /^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$/;
            if (!emailRegex.test(input.value)) {
                mostrarError(input, 'Email is invalid');
                esValido = false;
            }
        }
    });
    
    return esValido;
}

function mostrarError(input, mensaje) {
    //  Remove previous error
    limpiarError(input);
    
    // Create error element
    const error = document.createElement('div');
    error.className = 'error-mensaje';
    error.textContent = mensaje;
    error.style.color = '#dc3545';
    error.style.fontSize = '12px';
    error.style.marginTop = '5px';
    
    // Add after the input
    input.parentNode.insertBefore(error, input.nextSibling);
    
    // Change input style
    input.style.borderColor = '#dc3545';
}

function limpiarError(input) {
    const error = input.parentNode.querySelector('.error-mensaje');
    if (error) {
        error.remove();
    }
    input.style.borderColor = '';
}

// Configure real-time validation
document.addEventListener('DOMContentLoaded', function() {
    const inputs = document.querySelectorAll('input');
    inputs.forEach(input => {
        input.addEventListener('blur', function() {
            if (this.hasAttribute('required') && !this.value.trim()) {
                mostrarError(this, 'This field is required');
            } else {
                limpiarError(this);
            }
        });
        
        input.addEventListener('input', function() {
            limpiarError(this);
        });
    });
});
""")
\`\`\`

#### Visual Effects and Animations

\`\`\`python
script_animaciones = InlineScript("""
// Fade in effect for elements
function fadeIn(elemento, duracion = 500) {
    elemento.style.opacity = '0';
    elemento.style.display = 'block';
    
    const inicio = performance.now();
    
    function animar(tiempo) {
        const progreso = (tiempo - inicio) / duracion;
        
        if (progreso < 1) {
            elemento.style.opacity = progreso;
            requestAnimationFrame(animar);
        } else {
            elemento.style.opacity = '1';
        }
    }
    
    requestAnimationFrame(animar);
}

// Typing effect for text
function efectoTyping(elemento, texto, velocidad = 50) {
    elemento.textContent = '';
    let i = 0;
    
    function escribir() {
        if (i < texto.length) {
            elemento.textContent += texto.charAt(i);
            i++;
            setTimeout(escribir, velocidad);
        }
    }
    
    escribir();
}

// Parallax simple
function iniciarParallax() {
    window.addEventListener('scroll', function() {
        const scrolled = window.pageYOffset;
        const elementos = document.querySelectorAll('.parallax');
        
        elementos.forEach(elemento => {
            const velocidad = elemento.dataset.velocidad || 0.5;
            const yPos = -(scrolled * velocidad);
            elemento.style.transform = \`translateY(\${yPos}px)\`;
        });
    });
}

// Inicializar efectos
document.addEventListener('DOMContentLoaded', function() {
    // Fade in para todos los elementos con clase 'fade-in'
    const elementosFadeIn = document.querySelectorAll('.fade-in');
    elementosFadeIn.forEach((elemento, index) => {
        setTimeout(() => fadeIn(elemento), index * 200);
    });
    
    // Efecto typing para t\xEDtulos
    const titulos = document.querySelectorAll('.typing-effect');
    titulos.forEach(titulo => {
        const texto = titulo.textContent;
        efectoTyping(titulo, texto);
    });
    
    // Inicializar parallax
    iniciarParallax();
});
""")
\`\`\`

### Integration with Exporter

The exporter (\`html_css_js.py\`) automatically detects and exports all scripts of type \`dScript\`, \`InlineScript\`, and \`FileScript\`. You can safely mix and match them in your app, and all will be included in the generated JS.

New in v1.2.2:

- Script objects embedded in state bootstrap (e.g., inside \`Mod.set(..., on_*=...)\`) are serialized to a JSON-safe form as \`{ "code": "..." }\` and reconstituted at runtime.
- Event attributes (\`on_*\`) accept a single script or an array of scripts (any mix of InlineScript, FileScript, dScript, or raw JS strings). The runtime runs them sequentially and guarantees a single active dynamic listener per event.

---

## FileScript

### Basic Syntax for FileScript
\`\`\`python
from dars.scripts.script import FileScript

# Load script from file
script = FileScript("./scripts/mi_script.js")
\`\`\`

### File Organization

\`\`\`
mi_proyecto/
\u251C\u2500\u2500 app.py
\u251C\u2500\u2500 scripts/
\u2502   \u251C\u2500\u2500 utils.js
\u2502   \u251C\u2500\u2500 validaciones.js
\u2502   \u2514\u2500\u2500 animaciones.js
\u2514\u2500\u2500\u2500\u2500\u2500\u2500 api.js

\`\`\`

#### Example: utils.js

\`\`\`javascript
// scripts/utils.js

// General utilities
const Utils = {
    // Date formatting
    formatearFecha: function(fecha) {
        return new Intl.DateTimeFormat('es-ES', {
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        }).format(fecha);
    },
    
    // Debounce for event optimization
    debounce: function(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    },
    
    // Email validation
    esEmailValido: function(email) {
        const regex = /^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$/;
        return regex.test(email);
    },
    
    // Generate unique ID
    generarId: function() {
        return '_'+ Math.random().toString(36).substr(2, 9);
    },
    
    // Local storage
    guardarEnLocal: function(clave, valor) {
        try {
            localStorage.setItem(clave, JSON.stringify(valor));
            return true;
        } catch (e) {
            console.error('Error al guardar en localStorage:', e);
            return false;
        }
    },
    
    obtenerDeLocal: function(clave) {
        try {
            const item = localStorage.getItem(clave);
            return item ? JSON.parse(item) : null;
        } catch (e) {
            console.error('Error al leer de localStorage:', e);
            return null;
        }
    }
};

// Make available globally
window.Utils = Utils;
\`\`\`

#### Example: api.js

\`\`\`javascript
// scripts/api.js

// API client
class ApiClient {
    constructor(baseUrl) {
        this.baseUrl = baseUrl;
        this.headers = {
            'Content-Type': 'application/json'
        };
    }
    
    async request(endpoint, options = {}) {
        const url = \`\${this.baseUrl}\${endpoint}\`;
        const config = {
            headers: this.headers,
            ...options
        };
        
        try {
            const response = await fetch(url, config);
            
            if (!response.ok) {
                throw new Error(\`HTTP error! status: \${response.status}\`);
            }
            
            return await response.json();
        } catch (error) {
            console.error('Error en la petici\xF3n:', error);
            throw error;
        }
    }
    
    async get(endpoint) {
        return this.request(endpoint, { method: 'GET' });
    }
    
    async post(endpoint, data) {
        return this.request(endpoint, {
            method: 'POST',
            body: JSON.stringify(data)
        });
    }
    
    async put(endpoint, data) {
        return this.request(endpoint, {
            method: 'PUT',
            body: JSON.stringify(data)
        });
    }
    
    async delete(endpoint) {
        return this.request(endpoint, { method: 'DELETE' });
    }
}

// Global instance
window.api = new ApiClient('https://api.ejemplo.com');
\`\`\`

### Usage in the Application

#### Global and Page-specific Scripts (multipage)

In multipage applications, you can add global scripts to the App and page-specific scripts to each Page:

\`\`\`python
from dars.scripts.script import InlineScript
from dars.components.basic import Page, Button, Text

home = Page(
    Text("Inicio"),
    Button("Ir a About", id="btn-about")
)
home.add_script(InlineScript("""
document.addEventListener('DOMContentLoaded', function() {
    var btn = document.getElementById('btn-about');
    if (btn) btn.onclick = () => window.location.href = 'about.html';
});
"""))

about = Page(
    Text("Sobre Nosotros"),
    Button("Volver", id="btn-home")
)
about.add_script(InlineScript("""
document.addEventListener('DOMContentLoaded', function() {
    var btn = document.getElementById('btn-home');
    if (btn) btn.onclick = () => window.location.href = 'index.html';
});
"""))


app.add_script(InlineScript("console.log('Script global para todas las p\xE1ginas');"))
\`\`\`

When exporting, each page will have its own JS file combining global scripts and page-specific scripts.

\`\`\`python
from dars.scripts.script import FileScript

app.add_script(FileScript("./scripts/utils.js"))
app.add_script(FileScript("./scripts/api.js"))
app.add_script(FileScript("./scripts/validaciones.js"))
\`\`\`

## Component Integration

### Connecting Scripts to Components

\`\`\`python
from dars.core.app import App
from dars.components.basic.button import Button
from dars.components.basic.input import Input
from dars.components.basic.container import Container
from dars.scripts.script import InlineScript

formulario = Container(
    id="formulario-contacto",
    children=[
        Input(
            id="campo-nombre",
            placeholder="Nombre",
            required=True
        ),
        Input(
            id="campo-email",
            placeholder="Email",
            input_type="email",
            required=True
        ),
        Button(
            id="boton-enviar",
            text="Enviar"
        )
    ]
)

script_formulario = InlineScript("""
document.addEventListener(\\'DOMContentLoaded\\', function() {
    const formulario = document.getElementById(\\'formulario-contacto\\');
    const campoNombre = document.getElementById(\\'campo-nombre\\');
    const campoEmail = document.getElementById(\\'campo-email\\');
    const botonEnviar = document.getElementById(\\'boton-enviar\\');
    
    // Real-time validation
    campoNombre.addEventListener(\\'input\\', function() {
        validarNombre(this.value);
    });
    
    campoEmail.addEventListener(\\'input\\', function() {
        validarEmail(this.value);
    });
    
    // Handle form submission
    botonEnviar.addEventListener(\\'click\\', function(e) {
        e.preventDefault();
        enviarFormulario();
    });
    
    function validarNombre(nombre) {
        const esValido = nombre.length >= 2;
        campoNombre.style.borderColor = esValido ? \\'#28a745\\' : \\'#dc3545\\';
        return esValido;
    }
    
    function validarEmail(email) {
        const regex = /^[^\\\\s@]+@[^\\\\s@]+\\\\.[^\\\\s@]+$/;
        const esValido = regex.test(email);
        campoEmail.style.borderColor = esValido ? \\'#28a745\\' : \\'#dc3545\\';
        return esValido;
    }
    
    function enviarFormulario() {
        const nombre = campoNombre.value;
        const email = campoEmail.value;
        
        if (validarNombre(nombre) && validarEmail(email)) {
            // Simular env\xEDo
            botonEnviar.textContent = \\'Enviando...\\';
            botonEnviar.disabled = true;
            
            setTimeout(() => {
                alert(\\'Formulario enviado correctamente\\');
                campoNombre.value = \\'\\';
                campoEmail.value = \\'\\';
                botonEnviar.textContent = \\'Enviar\\';
                botonEnviar.disabled = false;
            }, 2000);
        } else {
            alert(\\'Por favor, corrige los errores en el formulario\\');
        }
    }
});
""")

app = App(title="Form with Script")
app.set_root(form)
app.add_script(form_script)


`},{type:"T9",id:"markdown_124",text:`# Dars CLI Reference

The Dars Command Line Interface (CLI) lets you manage your projects, export apps, and preview results quickly from the terminal.

## How to Use the CLI

Open your terminal in your project directory and use any of the following commands:

\`\`\`bash
# Show information about your app
 dars info my_app.py

# Export to different formats (web)
 dars export my_app.py --format html --output ./output
 # Skip default Python minifier for this run (does not affect viteMinify)
 dars export my_app.py --format html --output ./output --no-minify

# List supported export formats
 dars formats

# Initialize a new project
 dars init my_new_project

# Initialize a project with a specific template
 dars init my_new_project -t demo/complete_app

# Preview an exported app
 dars preview ./output_directory

# Build using project config (dars.config.json)
 dars build
 # Build desktop (BETA) when format is desktop in config
 dars build
 # Build without the default Python minifier
 dars build --no-minify

# Help
 dars --help

# Version
 dars -v
\`\`\`

## Main Commands Table
| Command                                 | What it does                               |
|-----------------------------------------|--------------------------------------------|
| \`dars export my_app.py --format html\`   | Export app to HTML/CSS/JS in \`./my_app_web\` |
| \`dars export my_app.py --format html --no-minify\` | Export skipping default Python minifier |
| \`dars preview ./my_app_web\`             | Preview exported app locally                |
| \`dars build\`                            | Build using dars.config.json                |
| \`dars init --type desktop\`              | Scaffold desktop-capable project (BETA)     |
| \`dars build\` (desktop config)           | Build desktop app artifacts (BETA)          |
| \`dars build --no-minify\`                | Build skipping default Python minifier      |
| \`dars init my_project\`                  | Create a new Dars project                   |
| \`dars info my_app.py\`                   | Show info about your app                    |
| \`dars formats\`                          | List supported export formats               |
| \`dars --help\`                           | Show help and all CLI options               |

## Using Official Templates

Dars provides official templates to help you start new projects quickly. Templates include ready-to-use apps for forms, layouts, dashboards, multipage, and more.

### How to Use a Template

1. **Initialize a new project with a template:**
   \`\`\`bash
   dars init my_new_project -t basic/HelloWorld
   # ...and more (see below)
   \`\`\`

You can see the templates available with

\`\`\`bash
dars init --list-templates
dars init  -L
\`\`\`

2. **Export the template to HTML/CSS/JS:**
   \`\`\`bash
   dars export main.py --format html --output ./hello_output
   dars export main.py --format html --output ./dashboard_output
   # ...etc
   \`\`\`
3. **Preview the exported app:**
   \`\`\`bash
   dars preview ./hello_output
   \`\`\`

## Tips CLI
- Use \`dars --help\` for a full list of commands and options.
- You can preview apps either live (with \`app.rTimeCompile()\`) or from exported files with \`dars preview\`.
- Templates are available for quick project setup: use \`dars init my_project -t <template>\`.

### Desktop (BETA) CLI

- Mark your project with \`"format": "desktop"\` in \`dars.config.json\`.
- Use \`dars init --type desktop\` (or \`--update\`) to scaffold backend files.
- Run \`dars doctor --all --yes\` to set up optional tooling.
- Build with \`dars build\`. This feature is in BETA: suitable for testing, not yet for production.

### Minification labels in output
- Applying minification (default): default Python-side minifier is active.
- Applying minification (vite): Vite/esbuild minification is active (JS/CSS) and default is disabled.
- Applying minification (default + vite): both are active.

For more, see the [Getting Started](#getting-started-with-dars) guide and the main documentation index.`}]},{type:"T2",id:"footer-section",children:[{type:"T2",id:"container_125",children:[{type:"T2",id:"container_126",children:[{type:"T2",id:"container_127",children:[{type:"T4",id:"image_128"},{type:"T2",id:"container_129",children:[{type:"T5",id:"text_130",text:"Dars Framework"}]}]},{type:"T2",id:"container_131",children:[{type:"T2",id:"container_132",children:[{type:"T5",id:"text_133",text:"Quick Links"},{type:"T6",id:"link_134",text:"Documentation"},{type:"T6",id:"link_135",text:"GitHub"},{type:"T6",id:"link_136",text:"Examples"}]},{type:"T2",id:"container_137",children:[{type:"T5",id:"text_138",text:"Resources"},{type:"T6",id:"link_139",text:"Getting Started"},{type:"T6",id:"link_140",text:"Releases"}]},{type:"T2",id:"container_141",children:[{type:"T5",id:"text_142",text:"Info: "},{type:"T5",id:"text_143",text:"A modern Python framework for web and desktop applications"}]}]},{type:"T2",id:"container_144",children:[{type:"T2",id:"container_145",children:[{type:"T5",id:"text_146",text:"\xA9 2024 Dars Framework."}]},{type:"T2",id:"container_147",children:[{type:"T5",id:"text_148",text:"Created with "},{type:"T6",id:"link_149",text:"Dars Framework"},{type:"T5",id:"text_150",text:" by "},{type:"T6",id:"link_151",text:"ZtaDev"}]}]}]}]}]}]}]},function(){const l=new Map;let r=null,d=null;function c(){}const b={Text:{create(n){if(!n||n.isIsland)return null;const e=document.createElement("span");if(n.id&&(e.id=n.id),n.class&&(e.className=n.class),n.style)for(const t in n.style)try{e.style.setProperty(t.replace(/_/g,"-"),String(n.style[t]))}catch{}if(Object.prototype.hasOwnProperty.call(n,"text")&&(e.textContent=String(n.text||"")),n.props)for(const t in n.props){const o=n.props[t];try{o===!1||o===null||typeof o>"u"?e.removeAttribute(t):e.setAttribute(t,String(o))}catch{}}return e}},Container:{create(n){if(!n||n.isIsland)return null;const e=document.createElement("div");n.id&&(e.id=n.id);const t="dars-container";if(e.className=n.class?t+" "+n.class:t,n.style)for(const o in n.style)try{e.style.setProperty(o.replace(/_/g,"-"),String(n.style[o]))}catch{}if(n.props)for(const o in n.props){const i=n.props[o];try{i===!1||i===null||typeof i>"u"?e.removeAttribute(o):e.setAttribute(o,String(i))}catch{}}return e}}};function h(n,e){if(!n)return;e(n);const t=n.children||[];for(let o=0;o<t.length;o++)h(t[o],e)}function _(n){try{if(typeof atob=="function")return atob(n);if(typeof Buffer<"u")return Buffer.from(n,"base64").toString("utf8")}catch{}return""}function T(n){try{if(!n)return null;if(n&&n.type==="inline"&&n.code)return new Function("event",n.code);const e=n&&(n.b||n.code_b64)||null;if(e){const t=_(e);if(t)return new Function("event",t)}}catch{}return null}function L(n){h(n,e=>{if(e&&e.id&&e.events&&!l.has(e.id)){const t={};for(const o in e.events){const i=e.events[o],p=T(i);p&&(t[o]=p)}Object.keys(t).length?l.set(e.id,t):l.delete(e.id)}})}function I(n,e){if(!(!n||!e))for(const[t,o]of Object.entries(e))try{o===!1||o===null||typeof o>"u"?n.removeAttribute(t):n.setAttribute(t,String(o))}catch{}}function C(n,e={},t={}){for(const o in e)if(!(o in t))try{n.removeAttribute(o)}catch{}for(const o in t){const i=t[o];try{i===!1||i===null||typeof i>"u"?n.removeAttribute(o):n.setAttribute(o,String(i))}catch{}}}function E(n,e={},t={}){for(const o in e)if(!(o in t))try{n.style.removeProperty(o.replace(/_/g,"-"))}catch{}for(const o in t){const i=t[o];try{n.style.setProperty(o.replace(/_/g,"-"),String(i))}catch{}}}function A(n,e){(e||document).addEventListener(n,function(t){let o=t.target;const i=e||document;for(;o&&o!==i;){const p=o.id;if(p&&l.has(p)){const m=l.get(p)[n];if(o&&o.__darsEv&&o.__darsEv[n])return;if(typeof m=="function"){try{m.call(o,t)}catch(a){console.error("[Dars] handler error",a)}return}}o=o.parentNode}},!0)}function v(n,e){return n&&e?n.type!==e.type:n!==e}function k(n){if(!n)return;const e=n.children||[];for(let t=0;t<e.length;t++)k(e[t]);if(n.id&&l.delete(n.id),n.id){const t=document.getElementById(n.id);if(t&&t.parentNode)try{t.parentNode.removeChild(t)}catch{}}}function x(n,e){if(!e||!e.id)return{ok:!1,reason:"missing-new"};let t=document.getElementById(e.id);if(!t){const a=n&&n.id?document.getElementById(n.id):null;if(a)try{a.id=e.id,t=a}catch{}}if(!t)return{ok:!1,reason:"missing-el"};if(v(n,e))return{ok:!1,reason:"type-changed"};const o=!!e.isIsland;if(!o&&e.class&&(t.className=e.class),o||C(t,n&&n.props||{},e.props||{}),o||E(t,n&&n.style||{},e.style||{}),!o&&Object.prototype.hasOwnProperty.call(e,"text")&&t.textContent!==String(e.text||"")&&(t.textContent=String(e.text||"")),o)return{ok:!0};const i=n&&n.children?n.children:[],p=e.children?e.children:[],u=new Map;for(let a=0;a<i.length;a++){const s=i[a]&&(i[a].id||i[a].key)||null;s&&u.set(String(s),i[a])}const m=new Set;for(let a=0;a<p.length;a++){const s=p[a],S=s&&(s.id||s.key)||null;if(!S)if(a<i.length){const f=x(i[a],s);if(!f.ok)return f;m.add(i[a]);continue}else return{ok:!1,reason:"children-added"};const w=u.get(String(S));if(w){const f=x(w,s);if(!f.ok)return f;m.add(w)}else{if(a<i.length){const y=i[a];if(!v(y,s)){const g=x(y,s);if(!g.ok)return g;m.add(y);continue}}const f=createSubtree(s);if(f){const y=a<i.length?i[a]:null;if(y&&y.id){const g=document.getElementById(y.id);g&&g.parentNode?g.parentNode.insertBefore(f,g):t.appendChild(f)}else t.appendChild(f);continue}return{ok:!1,reason:"children-added"}}}for(let a=0;a<i.length;a++){const s=i[a];m.has(s)||k(s)}return{ok:!0}}function B(n){typeof requestAnimationFrame=="function"?requestAnimationFrame(n):setTimeout(n,16)}function M(n){const e=r;if(!e){r=n;try{window.__DARS_VDOM__=n}catch{}return}B(()=>{const t=x(e,n);if(!t.ok){console.warn("[Dars] Structural change detected (",t.reason,"), reloading...");try{location.reload()}catch{}return}r=n;try{window.__DARS_VDOM__=n}catch{}})}function P(n){r=n;try{window.__DARS_VDOM__=n}catch{}["click","dblclick","mousedown","mouseup","mouseenter","mouseleave","mousemove","keydown","keyup","keypress","change","input","submit","focus","blur"].forEach(t=>A(t,document))}function D(){const n=window.__DARS_VERSION_URL||"version.txt";let e=null,t=!1;function o(p,u,m,a){try{const s=new XMLHttpRequest;a&&(s.responseType=a),s.open("GET",p,!0),s.timeout=5e3,s.onreadystatechange=function(){s.readyState===4&&(s.status>=200&&s.status<300?u(s.response):m())},s.onerror=m,s.ontimeout=m,s.setRequestHeader("Cache-Control","no-store"),s.send()}catch{m()}}function i(){o(n,function(p){let u=(p||"").toString().trim();if(u&&(t=!1),d||(d=u),u&&u!==d){d=u;try{location.reload()}catch{}return}e=setTimeout(i,600)},function(){t||(console.log("[Dars] waiting for version.txt"),t=!0),e=setTimeout(i,600)},"text")}return i(),()=>{e&&clearTimeout(e)}}document.addEventListener("DOMContentLoaded",function(){window.__DARS_VDOM__?P(window.__DARS_VDOM__):console.warn("[Dars] No VDOM snapshot found for hydration"),window.__DARS_VERSION_URL&&window.__DARS_SNAPSHOT_URL&&D()})}(),window.addEventListener("scroll",()=>{const l=document.getElementById("dars-navbar");window.scrollY>20?l.classList.add("scrolled"):l.classList.remove("scrolled");const r=document.getElementById("features-section");if(r&&!r.classList.contains("visible")){const d=r.getBoundingClientRect().top,c=window.innerHeight/1.5;d<c&&(r.classList.add("visible"),document.querySelectorAll('[id^="feature-card-"]').forEach((h,_)=>{setTimeout(()=>{h.style.opacity="1",h.style.transform="translateY(0)"},_*100)}))}}),document.addEventListener("DOMContentLoaded",()=>{const l=document.getElementById("hero-logo"),r=document.getElementById("hero-title"),d=document.getElementById("hero-description"),c=document.getElementById("pip-command"),b=document.getElementById("get-started-btn"),h=document.getElementById("scroll-text");l&&setTimeout(()=>l.classList.add("show"),5),r&&setTimeout(()=>r.classList.add("show"),350),d&&setTimeout(()=>d.classList.add("show"),650),c&&setTimeout(()=>c.classList.add("show"),950),b&&setTimeout(()=>b.classList.add("show"),1250),h&&setTimeout(()=>h.classList.add("show"),1500)});function F(){window.open("https://ztamdev.github.io/Dars-Framework/docs.html","_self")}function j(){navigator.clipboard.writeText("pip install dars framework").then(()=>{const r=document.querySelector("#copy-btn"),d=r.textContent;r.textContent="Copied!",r.style.background="linear-gradient(135deg, #38c49f 0%, #2a6b5b 100%) !important",setTimeout(()=>{r.textContent=d,r.style.background="linear-gradient(135deg, #1d4a3f 0%, #2a6b5b 100%) !important"},2e3)})}document.addEventListener("DOMContentLoaded",function(){const l=document.getElementById("hamburger-btn"),r=document.getElementById("mobile-menu"),d=document.body;l&&r&&(l.addEventListener("click",function(c){c.stopPropagation(),r.style.display==="flex"?(r.style.display="none",l.classList.remove("menu-open"),d.classList.remove("menu-open")):(r.style.display="flex",l.classList.add("menu-open"),d.classList.add("menu-open"))}),r.querySelectorAll("a").forEach(c=>{c.addEventListener("click",function(){r.style.display="none",l.classList.remove("menu-open"),d.classList.remove("menu-open")})}),document.addEventListener("click",function(c){!l.contains(c.target)&&!r.contains(c.target)&&(r.style.display="none",l.classList.remove("menu-open"),d.classList.remove("menu-open"))}),document.addEventListener("keydown",function(c){c.key==="Escape"&&r.style.display==="flex"&&(r.style.display="none",l.classList.remove("menu-open"),d.classList.remove("menu-open"))}))});
