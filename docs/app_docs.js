window.__DARS_VDOM__={type:"T1",id:"page_91",key:"0",children:[{type:"T2",id:"container_92",key:"0/0",children:[{type:"T3",id:"dars-navbar",key:"0/0/0",children:[{type:"T2",id:"navbar-left",key:"0/0/0/0",children:[{type:"T4",id:"image_93",key:"0/0/0/0/0"},{type:"T5",id:"text_94",key:"0/0/0/0/1",text:"Dars Framework"}]},{type:"T2",id:"container_95",key:"0/0/0/1",children:[{type:"T2",id:"navbar-right",key:"0/0/0/1/0",children:[{type:"T6",id:"link_96",key:"0/0/0/1/0/0",text:"Home"},{type:"T6",id:"link_97",key:"0/0/0/1/0/1",text:"Documentation"},{type:"T6",id:"link_98",key:"0/0/0/1/0/2",text:"Releases"},{type:"T6",id:"link_99",key:"0/0/0/1/0/3",text:"PlayGround"},{type:"T6",id:"link_100",key:"0/0/0/1/0/4",text:"GitHub"}]},{type:"T2",id:"hamburger-menu",key:"0/0/0/1/1",children:[{type:"T2",id:"hamburger-btn",key:"0/0/0/1/1/0",children:[{type:"T2",id:"container_101",key:"0/0/0/1/1/0/0",children:[{type:"T2",id:"container_102",key:"0/0/0/1/1/0/0/0"},{type:"T2",id:"container_103",key:"0/0/0/1/1/0/0/1"},{type:"T2",id:"container_104",key:"0/0/0/1/1/0/0/2"}]}]},{type:"T2",id:"mobile-menu",key:"0/0/0/1/1/1",children:[{type:"T6",id:"link_105",key:"0/0/0/1/1/1/0",text:"Home"},{type:"T6",id:"link_106",key:"0/0/0/1/1/1/1",text:"Documentation"},{type:"T6",id:"link_107",key:"0/0/0/1/1/1/2",text:"Releases"},{type:"T6",id:"link_108",key:"0/0/0/1/1/1/3",text:"PlayGround"},{type:"T6",id:"link_109",key:"0/0/0/1/1/1/4",text:"GitHub"}]}]}]}]}]},{type:"T8",id:"documentation-sidebar",key:"0/1"},{type:"T2",id:"container_110",key:"0/2",children:[{type:"T2",id:"markdown-content-container",key:"0/2/0",children:[{type:"T9",id:"markdown_111",key:"0/2/0/0",text:`# Dars Framework Documentation

Welcome to the official Dars Framework documentation. Here you will find detailed guides and references to help you build modern web applications with Python.

## Main Guides

- [Getting Started with Dars](#getting-started-with-dars)
- [App class](#app-class-and-pwa-features-in-dars-framework)
- [SPA Routing](#spa-routing-in-dars-framework)
- [Backend HTTP Utilities & API Communication](#backend-http-utilities)
- [State Management](#state-management-in-dars)
- [Components](#dars-components-documentation)
- [Animation System](#dars-animation-system)
- [Custom Components](#custom-components-in-dars-framework)
- [Hooks](#hooks-system)
- [Key Events System](#keyboard-events-in-dars)
- [Event Handling](#events-in-dars)
- [Exporters](#dars-exporter-documentation)
- [Scripts System](#dars-script-system)
- [CLI Usage and Commands](#dars-cli-reference)

`},{type:"T9",id:"markdown_112",key:"0/2/0/1",text:`# Installation Guide - Dars Framework

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
`},{type:"T9",id:"markdown_113",key:"0/2/0/2",text:`# Getting Started with Dars

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
`},{type:"T9",id:"markdown_114",key:"0/2/0/3",text:'# Dars Project Configuration\n\nThe file (dars.config.json) configures how Dars exports and builds your project. It is created by `dars init <name>` for new projects and can be merged/updated in existing projects with `dars init --update`.\n\n## Example\n\n```json\n{\n  "entry": "main.py",\n  "format": "html",\n  "outdir": "dist",\n  "publicDir": null,\n  "include": [],\n  "exclude": ["**/__pycache__", ".git", ".venv", "node_modules"],\n  "bundle": false,\n  "defaultMinify": true,\n  "viteMinify": true,\n  "markdownHighlight": true\n}\n```\n\n## Fields\n\n- entry\n  Python entry file for your app. Used by `dars build` and by `dars export config`.\n\n- format\n  Export format. Supported: `html` and `desktop` (BETA). When set to `desktop`, the build command will produce native desktop artifacts.\n\n- outdir\n  Directory where the exported files are written.\n\n- publicDir\n  Directory whose contents are copied as-is into the output (e.g. `public/` or `assets/`). If `null`, Dars will try to autodetect common locations.\n\n- include / exclude\n  Simple filters (by substring) applied when copying from `publicDir`.\n\n- bundle\n  Reserved for future use. Current exporters already produce a bundled output.\n\n- defaultMinify\n  Toggle the built-in Python minifier (safe and conservative). Controls HTML minification and provides JS/CSS fallback when advanced tools are unavailable.\n  - `true` (default): run the default Python-side minifier.\n  - `false`: skip the default minifier. You can still use Vite/esbuild via `viteMinify`.\n\n- viteMinify\n  Toggle the advanced JS minifier.\n  - `true` (default): prefer the advanced minifier; fall back to the secondary minifier; if neither is available, a conservative built-in fallback is used.\n  - `false`: skip the advanced minifier and use the secondary minifier directly; fall back to the conservative built-in if not available.\n\n- markdownHighlight\n  Auto-inject a client-side syntax highlighter for fenced code blocks in Markdown.\n  - `true` (default): injects Prism.js assets once per page and highlights `pre code` blocks.\n  - `false`: no assets injected; you can include your own highlighter or none at all.\n\n## Desktop-specific (BETA)\n\n- targetPlatform\n  Desktop build target. Only effective when `format` is `desktop`.\n  - Values: `auto` (default), `windows`, `linux`, `macos`.\n  - Note: macOS targets must be built on macOS for signing.\n\n> Desktop export is BETA: suitable for testing, not recommended for production yet. Configuration keys and defaults may change.\n\n## Behavior and defaults\n\n- `dars init --update` merges your existing config with Dars defaults and writes the result back, adding any new keys (like `defaultMinify`, `viteMinify`) without removing your current settings.\n- During `dars export` and `dars build`, Dars reads this file and configures the minification pipeline accordingly.\n- If advanced minifiers are not available, builds still complete with a conservative fallback. On `dars build`, a small notice may appear indicating that a less powerful minifier was used.\n- You can force-skip the default Python minifier per run with `--no-minify` (does not affect `viteMinify`).\n\n## Tips\n\n- To add or refresh the config in an existing project:\n  ```bash\n  dars init --update\n  ```\n- To review optional tooling that can enhance bundling/minification, run:\n  ```bash\n  dars doctor\n  ```\n- If you want to force using only the secondary minifier, set `"viteMinify": false`.\n - To disable the default minifier by config, set `"defaultMinify": false`; to disable it per-run use `--no-minify`.\n'},{type:"T9",id:"markdown_115",key:"0/2/0/4",text:`# App Class and PWA Features in Dars Framework

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

## Compile-Time Component Manipulation (App.create / App.delete)

Dars lets you modify the component tree before export or preview. Use these methods on \`App\` to insert or remove components safely at compile time.

### App.create(target, root=None, on_top_of=None, on_bottom_of=None)

- **Purpose**: Insert a component into the tree.
- **\`target\`** can be:
  - A component instance (e.g., \`Button("OK", id="ok")\`).
  - A callable that returns an instance (called lazily).
  - A \`str\` id of an existing component in the app tree to move it.
- **\`root\`**: Where to insert. Accepts:
  - A component instance.
  - A component id (\`str\`).
  - A page name (\`str\`) in multipage apps.
- **\`on_top_of\` / \`on_bottom_of\`**: Reference sibling inside \`root\` to place the new node before/after. Can be an id (\`str\`) or a component instance found within \`root\` (deep search). If neither is provided, it appends to \`root\`.
- Works with both single-page (\`app.root\`) and multipage (\`app.add_page\`) setups.
- If anything can\u2019t be resolved, it fails gracefully without crashing.

#### Examples

\`\`\`python
from dars.all import *

app = App(title="Compile-time create/delete")

# Single-page usage
root = Container(Text("A" , id="a"), Text("C", id="c"), id="root")
app.set_root(root)

# Insert new Text before id="c"
app.create(Text("B", id="b"), root="root", on_top_of="c")

# Move existing component by id to bottom
app.create("a", root="root", on_bottom_of="c")

# Multipage usage (root by page name)
home = Page(Container(Text("Home"), id="home_root"))
app.add_page(name="home", root=home, index=True)
app.create(Text("Welcome", id="welcome"), root="home", on_bottom_of="home_root")
\`\`\`

### App.delete(id)

- **Purpose**: Remove a component from the tree by its \`id\`.
- If the id does not exist, it becomes a no-op (safe warning behavior).

\`\`\`python
# Remove a component by id before export/preview
app.delete("b")
\`\`\`

These operations run before export and affect the generated HTML/VDOM. For dynamic changes at runtime in the browser, see the runtime APIs in the Components documentation.

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
- Edge (full support)`},{type:"T9",id:"markdown_116",key:"0/2/0/5",text:`# SPA Routing in Dars Framework

Dars Framework 1.4.5 introduces a powerful SPA (Single Page Application) routing system that supports nested routes, layouts, and automatic 404 handling.

## Basic Routing

To create a basic SPA, you define pages and add them to your app. One page must be designated as the index.

\`\`\`python
from dars.all import *

app = App(title="My SPA App")

# Create pages
home = Page(Container(Text("Home Page")))
about = Page(Container(Text("About Us")))

# Add pages to app
app.add_page(name="home", root=home, route="/", title="Home", index=True)
app.add_page(name="about", root=about, route="/about", title="About")
\`\`\`

you can also use the \`@route\` decorator to add pages to your app.

\`\`\`python
from dars.all import *

app = App(title="My SPA App")

# Create pages
home = Page(Container(Text("Home Page")))
about = Page(Container(Text("About Us")))

# Add pages to app
@app.route("/")
def home():
    return Page(Container(Text("Home Page")))

@app.route("/about")
def about():
    return Page(Container(Text("About Us")))

app.add_page("home", home, title="Home", index=True)
app.add_page("about", about, title="About")
\`\`\`

> Note: If you use the \`@route\` decorator, you can't add the route of the page in \`app.add_page()\`.

## Nested Routes & Layouts

Nested routes allow you to create layouts that persist while child content changes. This is achieved using the \`parent\` parameter and the \`Outlet\` component.

### The Outlet Component

The \`Outlet\` component serves as a placeholder where child routes will be rendered within a parent layout.

\`\`\`python
from dars.components.advanced.outlet import Outlet

# Parent Layout (Dashboard)
dashboard_layout = Page(
    Container(
        Text("Dashboard Header"),
        # Child routes will render here:
        Outlet(),
        Text("Dashboard Footer")
    )
)

# Child Page (Settings)
settings_page = Page(
    Container(Text("Settings Content"))
)
\`\`\`

### Configuring Nested Routes

Use the \`parent\` parameter in \`add_page\` to define the hierarchy.

\`\`\`python
# 1. Add the parent route
app.add_page(
    name="dashboard", 
    root=dashboard_layout, 
    route="/dashboard", 
    title="Dashboard"
)

# 2. Add the child route, specifying the parent's name
app.add_page(
    name="settings", 
    root=settings_page, 
    route="/dashboard/settings", 
    title="Settings",
    parent="dashboard"  # This links it to the dashboard layout
)
\`\`\`

When you navigate to \`/dashboard/settings\`, Dars will render the \`dashboard\` layout and place the \`settings\` content inside the \`Outlet\`.

## 404 Handling

Dars provides robust handling for non-existent routes.

### Default 404 Page

If a user navigates to a route that doesn't exist, Dars automatically:
1. Redirects the user to \`/404\`.
2. Displays a built-in, clean "404 Page Not Found" error page.

### Custom 404 Page

You can customize the 404 page using \`app.set_404_page()\`.

\`\`\`python
# Create your custom 404 page
not_found_page = Page(
    Container(
        Text("Oops! Page not found \u{1F622}", style={"fontSize": "32px"}),
        Link("Go Home", href="/")
    )
)

# Register it
app.set_404_page(not_found_page)
\`\`\`

Now, when a 404 occurs, users will be redirected to \`/404\` but will see your custom design.

## Hot Reload

The development server (\`dars dev\`) includes an intelligent hot reload system for SPAs:

- **Automatic Detection**: The browser automatically detects changes to your Python code.
- **Smart Polling**: It checks for updates every 500ms without spamming your console logs.
- **Retry Limit**: If the server goes down, the client stops polling after 10 consecutive errors to prevent browser lag.
- **State Preservation**: When possible, navigation state is preserved across reloads.
`},{type:"T9",id:"markdown_117",key:"0/2/0/6",text:`# Backend HTTP Utilities 

Dars Framework provides a powerful, **Pythonic system** for handling HTTP requests and API communication without writing any JavaScript. The \`dars.backend\` module enables you to fetch data, bind it to components, and create reactive UIs entirely in Python.

## Table of Contents

- [Quick Start with HTTP UTILS](#quick-start-with-http-utils)
- [HTTP Functions](#http-functions)
- [Data Binding with useData()](#data-binding-with-usedata)
- [JSON Utilities](#json-utilities)
- [Component Management](#component-management)

---

## Quick Start with HTTP UTILS

\`\`\`python
from dars.all import *
from dars.backend import get, useData

app = App(title="API Demo")

# Create display component
user_display = Text("No data", id="user-name")
user_state = State(user_display, text="No data")

# Fetch and bind data - pure Python!
fetch_btn = Button(
    "Fetch User",
    on_click=get(
        id="userData",
        url="https://api.example.com/user/1",
        callback=user_state.text.set(useData('userData').name)
    )
)

app.set_root(Container(user_display, fetch_btn))
app.rTimeCompile()
\`\`\`

---

## HTTP Functions

The \`dars.backend\` module provides standard HTTP methods that return \`dScript\` objects:

### \`get(id, url, **options)\`

Performs a GET request.

\`\`\`python
from dars.backend import get

# Basic GET
get_user = get(
    id="userData",
    url="https://jsonplaceholder.typicode.com/users/1"
)

# With callback
get_user = get(
    id="userData",
    url="https://api.example.com/user/1",
    callback=status_state.text.set("\u2705 Loaded!"),
    on_error=status_state.text.set("\u274C Error!")
)
\`\`\`

### \`post(id, url, body, **options)\`

Performs a POST request.

\`\`\`python
from dars.backend import post

# POST with JSON body
create_user = post(
    id="createResult",
    url="https://api.example.com/users",
    body={"name": "John", "email": "john@example.com"},
    callback=status_state.text.set("User created!")
)
\`\`\`

### Other Methods

- **\`put(id, url, body, **options)\`** - Update resource
- **\`delete(id, url, **options)\`** - Delete resource
- **\`patch(id, url, body, **options)\`** - Partial update
- **\`fetch(id, url, method, **options)\`** - Generic fetch

### Common Options

All HTTP functions accept these options:

| Option | Type | Description |
|--------|------|-------------|
| \`id\` | \`str\` | **Required**. Operation ID (NOT HTML ID) for accessing data |
| \`url\` | \`str\` | **Required**. API endpoint URL |
| \`headers\` | \`dict\` | Custom HTTP headers |
| \`callback\` | \`dScript\` | Executed on success |
| \`on_error\` | \`dScript\` | Executed on error |
| \`parse_json\` | \`bool\` | Auto-parse JSON response (default: \`True\`) |
| \`timeout\` | \`int\` | Request timeout in milliseconds |

---

## Data Binding with useData()

The \`useData()\` function provides **Pythonic access** to fetched data using dot notation:

### Basic Usage

\`\`\`python
from dars.backend import useData

# Access fetched data by operation ID
user_data = useData('userData')

# Access nested properties with dot notation
user_name = useData('userData').name
user_email = useData('userData').email
user_address_city = useData('userData').address.city
\`\`\`

### How It Works

1. **Operation ID**: When you call \`get(id="userData", ...)\`, the response is stored in \`window.userData\`
2. **DataAccessor**: \`useData('userData')\` creates a \`DataAccessor\` object
3. **Dot Notation**: \`.name\` uses \`__getattr__\` to create \`window.userData?.name\`
4. **RawJS Generation**: The \`.code\` property generates the JavaScript expression

### Binding to StateV2

The most powerful feature is binding API data directly to component states:

\`\`\`python
from dars.all import *
from dars.backend import get, useData

# Create components and states
name_display = Text("", id="user-name")
email_display = Text("", id="user-email")

name_state = State(name_display, text="")
email_state = State(email_display, text="")

# Fetch and bind - pure Python!
fetch_button = Button(
    "Fetch User",
    on_click=get(
        id="userData",
        url="https://jsonplaceholder.typicode.com/users/1",
        # Chain multiple state updates with .then()
        callback=(
            name_state.text.set(useData('userData').name)
            .then(email_state.text.set(useData('userData').email))
        )
    )
)
\`\`\`

### Chaining with \`.then()\`

Chain multiple operations sequentially:

\`\`\`python
# Update multiple components
callback=(
    status_state.text.set("Loading...")
    .then(name_state.text.set(useData('userData').name))
    .then(email_state.text.set(useData('userData').email))
    .then(status_state.text.set("\u2705 Loaded!"))
)
\`\`\`

### Before vs After

**Before (Raw JavaScript):**

\`\`\`python
callback=dScript("""
    const user = window.userData;
    if (user) {
        window.Dars.change({
            id: 'user-name',
            dynamic: true,
            text: user.name || 'Unknown'
        });
        window.Dars.change({
            id: 'user-email',
            dynamic: true,
            text: user.email || 'N/A'
        });
    }
""")
\`\`\`

**After (Pure Python):**

\`\`\`python
callback=(
    name_state.text.set(useData('userData').name)
    .then(email_state.text.set(useData('userData').email))
)
\`\`\`

---

## JSON Utilities

Helper functions for working with JSON data:

### \`stringify(data, pretty=False)\`

Convert data to JSON string:

\`\`\`python
from dars.backend import stringify, useData

# Stringify fetched data
display_state.text.set(stringify(useData('userData'), pretty=True))

# Stringify Python objects
json_str = stringify({"name": "John", "age": 30})
\`\`\`

### \`parse(json_string)\`

Parse JSON string:

\`\`\`python
from dars.backend import parse

# Parse JSON string
data = parse('{"name": "John"}')
\`\`\`

### \`get_value(obj, path, default=None)\`

Safely access nested values:

\`\`\`python
from dars.backend import get_value, useData

# Safe nested access with default
city = get_value(useData('userData'), 'address.city', default='Unknown')
\`\`\`

---

## Component Management

Create, update, and delete components dynamically at runtime:

### \`createComp(target, root, position="append")\`

Create a new component in the DOM:

\`\`\`python
from dars.backend import createComp

# Create new component
new_text = Text("Hello!", id="new-item")
create_btn.on_click = createComp(
    target=new_text,
    root="container-id",
    position="append"  # or "prepend", "before:id", "after:id"
)
\`\`\`

**Tip:** You can create a \`State()\` for a component before it exists using a string ID:

\`\`\`python
# Create state with string ID
item_state = State("new-item", text="Hello!")

# Create component later
create_btn.on_click = createComp(
    target=Text("Hello!", id="new-item"),
    root="container-id"
)

# State works immediately!
update_btn.on_click = item_state.text.set("Updated!")
\`\`\`


### \`updateComp(target, **props)\`

Update component properties:

\`\`\`python
from dars.backend import updateComp

# Update component
update_btn.on_click = updateComp(
    "my-component-id",
    text="Updated!",
    style={"color": "red"}
)
\`\`\`

### \`deleteComp(id)\`

Remove a component from the DOM:

\`\`\`python
from dars.backend import deleteComp

# Delete component
delete_btn.on_click = deleteComp("component-id")
\`\`\`

---

## Best Practices

1. **Use Unique Operation IDs**: Each HTTP operation should have a unique \`id\` to avoid conflicts
2. **Chain Updates**: Use \`.then()\` to chain multiple state updates sequentially
3. **Handle Errors**: Always provide \`on_error\` callbacks for better UX
4. **Leverage useData()**: Use dot notation for clean, readable data access
5. **Combine with StateV2**: Bind API data directly to component states for reactive UIs

---

## API Reference Summary

### HTTP Functions
- \`get(id, url, **options)\` - GET request
- \`post(id, url, body, **options)\` - POST request
- \`put(id, url, body, **options)\` - PUT request
- \`delete(id, url, **options)\` - DELETE request
- \`patch(id, url, body, **options)\` - PATCH request
- \`fetch(id, url, method, **options)\` - Generic fetch

### Data Access
- \`useData(operation_id)\` - Access fetched data with dot notation
- \`stringify(data, pretty=False)\` - Convert to JSON string
- \`parse(json_string)\` - Parse JSON
- \`get_value(obj, path, default=None)\` - Safe nested access

### Component Management
- \`createComp(target, root, position)\` - Create component
- \`updateComp(target, **props)\` - Update component
- \`deleteComp(id)\` - Delete component

---

For more examples, see the test files in \`tst/proj/test_http_demo.py\` and \`tst/proj/test_http_utils.py\`.
`},{type:"T9",id:"markdown_118",key:"0/2/0/7",text:`# State Management in Dars

Dars Framework features **two powerful state management systems**, each designed for different use cases:

- **State V2** - Modern, dynamic state management for simple reactive updates
- **dState & cState** - Indexed state system for complex state machines and workflows

##Choose the Right System

| Feature | State V2 | dState/cState |
|---------|----------|---------------|
| **API Style** | Clean Pythonic | Verbose but explicit |
| **Setup** | Minimal | Requires registration |
| **State Tracking** | Dynamic | Indexed (0, 1, 2...) |
| **Auto Operations** | Built-in | Manual with Mod |
| **Event Updates** | Supported | Supported |
| **State Machines** | Limited |  Full support |
| **Cross-State Calls** | No |  Mod.call() |
| **Immutable Default** | No |  State 0 |
| **Best For** | Counters, timers, simple updates | Workflows, toggles, complex UI transitions |

---

# State V2 - Dynamic State Management

Modern, Pythonic state management for reactive UIs.

## Quick Start

\`\`\`python
from dars.all import *

# Create a component
display = Text("0", id="counter")

# Create state
counter = State(display, text=0)

# Use reactive properties
increment_btn = Button("Increment", on_click=counter.text.increment(by=1))
decrement_btn = Button("Decrement", on_click=counter.text.decrement(by=1))
reset_btn = Button("Reset", on_click=counter.reset())
\`\`\`

## Core Concepts

### State Class

The \`State\` class wraps a component and provides reactive property access.

\`\`\`python
from dars.all import State

display = Text("0", id="counter")
counter_state = State(display, text=0)
\`\`\`

**Constructor Parameters:**
- \`component\`: The component to manage (can be a component object or string ID)
- \`**default_props\`: Default property values (e.g., \`text=0\`, \`style={...}\`)

### State with String IDs (for Dynamic Components)

\`State()\` can accept either a component object or a string ID. This is useful for components created dynamically:

\`\`\`python
from dars.all import *
from dars.backend import createComp

# Traditional: State with component object
existing_text = Text("0", id="counter")
existing_state = State(existing_text, text=0)

# New: State with string ID (for components created later)
dynamic_state = State("dynamic-counter", text=0)

# Create the component later
create_btn.on_click = createComp(
    target=Text("0", id="dynamic-counter"),
    root="container-id"
)

# State works even though component was created after state!
increment_btn.on_click = dynamic_state.text.increment(by=1)
\`\`\`

**Use Cases:**
- Components created with \`createComp()\`
- Dynamically generated UIs
- Conditional component rendering
- Server-side rendered components


### Reactive Properties

Access component properties through the state object to get reactive operations:

\`\`\`python
# Increment/decrement numeric properties
counter.text.increment(by=1)
counter.text.decrement(by=2)

# Set property values
counter.text.set(value=100)

# Auto operations (continuous)
counter.text.auto_increment(by=1, interval=1000)  # +1 every second
counter.text.auto_decrement(by=1, interval=500)   # -1 every 500ms
counter.text.stop_auto()  # Stop auto operations
\`\`\`

### Reset to Defaults

The \`reset()\` method restores all properties to their initial values:

\`\`\`python
state = State(display, text=0, style={"color": "blue"})

# ... user modifies the component ...

# Reset everything back to initial state
reset_btn.on_click = state.reset()
\`\`\`

## Reactive Operations

### Increment and Decrement

\`\`\`python
# Increment by 1 (default)
button.on_click = counter.text.increment()

# Increment by custom amount
button.on_click = counter.text.increment(by=5)

# Decrement (negative increment)
button.on_click = counter.text.decrement(by=1)
# OR
button.on_click = counter.text.increment(by=-1)
\`\`\`

\`\`\`python
button.on_click = counter.text.set(value=0)
\`\`\`

### All Property Types Supported

State V2 supports updating **all component properties**, not just text:

**Text Content:**
\`\`\`python
state.text.set("New text")
\`\`\`

**HTML Content:**
\`\`\`python
state.html.set("<strong>Bold text</strong>")
\`\`\`

**CSS Styles:**
\`\`\`python
state.style.set({"color": "red", "fontSize": "24px"})
\`\`\`

**CSS Classes:**
\`\`\`python
# Set class name
state.class_name.set("active")
\`\`\`

**Event Handlers:**
\`\`\`python
# Update event handler dynamically
state.update(on_click=alert("New handler!"))

# Or with dScript
from dars.scripts.dscript import dScript
state.update(on_click=dScript("console.log('clicked')"))
\`\`\`

**Multiple Properties at Once:**
\`\`\`python
state.update(
    text="Updated!",
    class_name="success",
    style={"color": "green"},
    on_click=alert("Done!")
)
\`\`\`

### Auto Operations


Auto operations create continuous reactive updates:

\`\`\`python
# Auto-increment timer
timer = State(display, text=0)

start_btn.on_click = timer.text.auto_increment(by=1, interval=1000)
stop_btn.on_click = timer.text.stop_auto()
\`\`\`

**With Limits:**
\`\`\`python
# Auto-increment up to 100
timer.text.auto_increment(by=1, interval=1000, max=100)

# Auto-decrement down to 0
countdown.text.auto_decrement(by=1, interval=1000, min=0)
\`\`\`

## Backend Integration with useData()

State V2 integrates seamlessly with Dars backend HTTP utilities for reactive API-driven UIs:

\`\`\`python
from dars.all import *
from dars.backend import get, useData

# Create components
user_name = Text("", id="user-name")
user_email = Text("", id="user-email")

# Create states
name_state = State(user_name, text="")
email_state = State(user_email, text="")

# Fetch and bind API data - pure Python!
fetch_btn = Button(
    "Load User",
    on_click=get(
        id="userData",
        url="https://api.example.com/users/1",
        # Access nested data with dot notation
        callback=(
            name_state.text.set(useData('userData').name)
            .then(email_state.text.set(useData('userData').email))
        )
    )
)
\`\`\`

**Key Features:**
- **\`useData('id')\`** - Access fetched data by operation ID
- **Dot notation** - \`useData('userData').name\` accesses nested properties
- **\`.then()\` chaining** - Chain multiple state updates sequentially
- **No JavaScript** - Everything is pure Python

## Complete Example

\`\`\`python
from dars.all import *

app = App("State V2 Demo")

# Timer display
timer_display = Text("0", id="timer", style={"font-size": "36px"})
timer = State(timer_display, text=0)

# Status display
status = Text("Paused", id="status")
status_state = State(status, text="Paused", class_name="paused")

# Control buttons
start_btn = Button("Start",
    on_click=timer.text.auto_increment(by=1, interval=1000)
)
stop_btn = Button("Stop", 
    on_click=[
        timer.text.stop_auto(),
        status_state.update(text="Paused", class_name="paused")
    ]
)
reset_btn = Button("Reset",
    on_click=[
        timer.text.stop_auto(),
        timer.reset(),
        status_state.reset()
    ]
)

page = Page(Container(timer_display, status, start_btn, stop_btn, reset_btn))
app.add_page("index", page, index=True)
app.rTimeCompile()
\`\`\`

### When to Use State V2

** Good for:**
- Simple counters and timers
- Dynamic text/style updates
- Auto-incrementing values
- Quick prototypes
- Single-component state

** Not ideal for:**
- Complex state machines
- Multi-step workflows
- State history/undo
- Cross-component state coordination

For these cases, use **dState & cState** instead.

---

# dState & cState - Indexed State Management

Powerful indexed state system for complex UI transitions and state machines.

## Quick Start with dState

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

## Mod Operations

- \`inc/dec(target, prop='text', by=1)\`: increments or decrements a numeric value (textContent by default).
- \`set(target, **attrs)\`: sets attributes; \`text\` sets textContent; \`html\` sets innerHTML; other keys map to element attributes.
- \`toggle_class(target, name, on=None)\`: toggles a class; when \`on\` is True/False, forces add/remove.
- \`append_text / prepend_text\`: concatenates to textContent.

## Cross-State Calls with Mod.call

Use \`Mod.call(target, state=None, goto=None)\` inside a \`cState\` to trigger another \`dState\`.

\`target\` can be the \`DarsState\` instance or its name (string). Example:

\`\`\`python
txt = dState("txt", id="txt1", states=[0,1])
btn = dState("btn", id="btn1", states=[0,1])

txt.cState(1, mods=[
    Mod.set("txt1", text="Bye"),
    Mod.call(btn, state=1)  # or Mod.call("btn", state=1)
])
\`\`\`

## Immutable Default State (Index 0)

- State \`0\` is the component's default configuration (as instantiated) and is **immutable**.
- Authoring-time: \`cState(0, ...)\` is forbidden and raises an error.
- Runtime: switching to state \`0\` restores the initial DOM snapshot (attributes except \`id\`, plus innerHTML) and ignores any rules for state \`0\`.
- This guarantees that returning to \`0\` reverts the UI to its original state.

## Mod.set with Multiple Attributes

You can set multiple properties in one call:

\`\`\`python
Mod.set("btn1", text="Don't click it", class_name="warn")
\`\`\`

Event attributes accept a single script or an array of scripts (executed sequentially). Valid values are:
- InlineScript, FileScript, dScript, or plain JS strings

\`\`\`python
Mod.set("btn1", on_click=[txt.state(0), dScript(code="console.log('clicked')")])
\`\`\`

The runtime ensures only one dynamic listener per event is active at a time and cleans it up when returning to state \`0\`.

## Full HTML Replacement (Custom Components)

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

## State Navigation Patterns

There are two main ways to trigger state changes in Dars:

### 1. Using \`state.state(idx)\` - Recommended

The \`state.state(idx)\` method is the standard way to navigate to a specific state when you have a reference to the dState object:

\`\`\`python
from dars.all import *
from dars.core.state import dState

# Create a toggle button
btn = Button("Off", id="ToggleBtn")

# Define state with 2 options
toggle = dState("toggle", component=btn, states=[0, 1])

# Configure "On" state
toggle.cState(1, mods=[
    Mod.set(btn, 
        text="On",
        style={'background-color': 'green'},
        on_click=toggle.state(0)  # Use state.state() to go back
    )
])

# Initial click goes to state 1
btn.on_click = toggle.state(1)
\`\`\`

**Advantages:**
- Clean and straightforward syntax
- Compile-time safety (if state object doesn't exist, Python will error)
- No runtime lookups needed
- Works in all contexts

### 2. Multi-State Cycles

\`\`\`python
# Create a button that cycles through 4 states
cycle_btn = Button("State 0", id="StatusBtn")
status = dState("status", component=cycle_btn, states=[0, 1, 2, 3])

# Define each state to navigate to the next
status.cState(1, mods=[
    Mod.set(cycle_btn, text="State 1 - Loading...", on_click=status.state(2))
])
status.cState(2, mods=[
    Mod.set(cycle_btn, text="State 2 - Processing...", on_click=status.state(3))
])
status.cState(3, mods=[
    Mod.set(cycle_btn, text="State 3 - Complete!", on_click=status.state(0))
])

# Start the cycle
cycle_btn.on_click = status.state(1)
\`\`\`

## Complete Interactive Example

\`\`\`python
from dars.all import *
from dars.core.state import dState

app = App(title="Status Indicator")

# Create button and status text
status_btn = Button("Idle", id="StatusBtn", style={
    'padding': '12px 24px',
    'background': '#gray'
})
status_text = Text("Ready", id="StatusText")

# Define 4-state workflow
workflow = dState("workflow", component=status_btn, states=[0, 1, 2, 3])

# State 1: Loading
workflow.cState(1, mods=[
    Mod.set(status_btn, 
        text="Loading...",
        style={'background': '#blue'},
        on_click=workflow.state(2)
    ),
    Mod.set(status_text, text="Fetching data...")
])

# State 2: Processing
workflow.cState(2, mods=[
    Mod.set(status_btn,
        text="Processing...",
        style={'background': '#orange'},
        on_click=workflow.state(3)
    ),
    Mod.set(status_text, text="Analyzing results...")
])

# State 3: Complete
workflow.cState(3, mods=[
    Mod.set(status_btn,
        text="Complete!",
        style={'background': '#green'},
        on_click=workflow.state(0)  # Back to idle
    ),
    Mod.set(status_text, text="All done!")
])

# Start workflow on click
status_btn.on_click = workflow.state(1)

index = Page(Container(status_btn, status_text))
app.add_page("index", index, index=True)
\`\`\`

### When to Use dState/cState

**Good for:**
- Complex state machines
- Multi-step workflows (wizards, forms)
- UI toggles with multiple states
- State history and reversion
- Cross-component state coordination

**Overkill for:**
- Simple counters
- Single property updates
- Quick prototypes
- Auto operations

For these cases, **State V2** is simpler.

---

## Dynamic State Updates & \`this()\`

Dars introduces dynamic state updates, allowing you to modify component properties directly without pre-registering state indices.

### \`this()\` helper

The \`this()\` helper allows a component to refer to itself in an event handler and apply updates dynamically.

\`\`\`python
from dars.core.state import this

btn = Button("Click me", on_click=this().state(text="Clicked!", style={"color": "red"}))
\`\`\`

Supported dynamic properties:
- \`text\`: Update text content.
- \`html\`: Update inner HTML.
- \`style\`: Dictionary of CSS styles.
- \`attrs\`: Dictionary of attributes.
- \`classes\`: Dictionary with \`add\`, \`remove\`, or \`toggle\` (single string or list of strings).

\`\`\`python
this().state(
    text="Updated",
    style={"backgroundColor": "#f0f0f0"},
    classes={"add": ["active"], "remove": ["inactive"]}
)
\`\`\`

### Using Raw JavaScript Values (\`RawJS\`)

You can pass raw JavaScript variables to dynamic updates using \`RawJS\`. This is particularly useful when:
- Chaining scripts where a previous script returns a value
- Working with async operations like file reading
- Using \`dScript.ARG\` to reference values from previous scripts

\`\`\`python
from dars.scripts.dscript import RawJS, dScript

# Using dScript.ARG placeholder for chained values
this().state(text=RawJS(dScript.ARG))

# Using custom JavaScript expressions
this().state(text=RawJS("someVar + ' processed'"))
\`\`\`

---

## Best Practices

### Choose State V2 When:
- Building simple counters or timers
- Need auto-increment/decrement
- Want quick reactive updates
- Working with single components

### Choose dState/cState When:
- Building complex state machines
- Need immutable default state (state 0)
- Require cross-state calls
- Managing multi-step workflows

### Use \`this()\` When:
- Don't need state tracking
- Making one-off updates
- Working with async operations
- Targeting the clicked element`},{type:"T9",id:"markdown_119",key:"0/2/0/8",text:`# Dars - Components Documentation

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

## Runtime Component Manipulation (createComp / deleteComp)

You can create or delete components dynamically at runtime in the browser using \`createComp()\` and \`deleteComp()\`. These functions return \`dScript\` so you can attach them to events.

- \`from dars.all import *\` exposes \`createComp\` and \`deleteComp\`.
- The created subtree is serialized to VDOM, mounted into the DOM, and its events are rehydrated automatically.
- Every node that has an \`id\` also receives a CSS class \`dars-id-<id>\` to help target multiple instances when needed.

### API

\`\`\`python
createComp(target, root, position='append') -> dScript
deleteComp(id) -> dScript
\`\`\`

- **target**: a component instance or a callable returning one.
- **root**: id (string) of the DOM/container where to insert.
- **position**: where to place the new element inside \`root\`.
  - \`append\` (default)
  - \`prepend\`
  - \`before:<id>\` (insert before a reference sibling id)
  - \`after:<id>\` (insert after a reference sibling id)

### Examples

\`\`\`python
from dars.all import *

container = Container(id="root")

# Add a button that creates a new Text inside #root on click
add_btn = Button(
    text="Add",
    id="add",
    on_click=createComp(Text("Hi", id="msg"), root="root", position='append')
)

# Add another button that inserts before a specific sibling
insert_btn = Button(
    text="Insert Before",
    on_click=createComp(Text("Before", id="before"), root="root", position='before:msg')
)

# Button that deletes an element by id
delete_btn = Button(
    text="Delete msg",
    on_click=deleteComp("msg")
)
\`\`\`

### Event Rehydration

- When a subtree is created with \`createComp\`, all events defined in its Python components are attached at runtime.
- This includes nested children and multiple handlers per node.

### Multiple Instances and CSS Class

- Elements get a helper class \`dars-id-<id>\` in addition to the DOM \`id\`.
- This makes it easier to query duplicate instances when they exist.

### Notes

- These APIs are for dynamic changes in the browser. For compile-time changes (before export/preview), use \`App.create()\` and \`App.delete()\` described in the App documentation.

## dScript Basic Usage

\`\`\`python
from dars.all import *

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
| \`Input\` | \`on_key_press\` | Triggered when a key is pressed |

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
- [Chart](#chart)
- [DataTable](#datatable)
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
        self.children: List[Component] = []
        self.parent: Optional[Component] = None
        self.id: Optional[str] = props.get('id')
        self.class_name: str = props.get("class_name", self.__class__.__name__)
        self.style: Dict[str, Any] = props.get('style', {})
        self.hover_style: Dict[str, Any] = props.get('hover_style', {})
        self.active_style: Dict[str, Any] = props.get('active_style', {})
        self.events: Dict[str, Callable] = {}
        self.key: Optional[str] = props.get('key')
\`\`\`

### Global Properties

All components support these basic properties:

- **id**: Unique component identifier
- **class_name**: CSS class for additional styles
- **style**: Dictionary of CSS styles
- **hover_style**: Dictionary of CSS styles on hover
- **active_style**: Dictionary of CSS styles when active
- **set_event(event_name, handler)**: Attach event handlers
- **on_click** event handler receives a dScript object or a comp.state() function
- **on_double_click** event handler receives a dScript object or a comp.state() function
- **on_mouse_down** event handler receives a dScript object or a comp.state() function
- **on_mouse_up** event handler receives a dScript object or a comp.state() function
- **on_mouse_enter** event handler receives a dScript object or a comp.state() function
- **on_mouse_leave** event handler receives a dScript object or a comp.state() function
- **on_mouse_move** event handler receives a dScript object or a comp.state() function
- **on_key_press** event handler receives a dScript object or a comp.state() function
- **on_key_up** event handler receives a dScript object or a comp.state() function
- **on_key_press** event handler receives a dScript object or a comp.state() function
- **on_change** event handler receives a dScript object or a comp.state() function
- **on_input** event handler receives a dScript object or a comp.state() function
- **on_submit** event handler receives a dScript object or a comp.state() function
- **on_focus** event handler receives a dScript object or a comp.state() function
- **on_blur** event handler receives a dScript object or a comp.state() function
- **on_load** event handler receives a dScript object or a comp.state() function
- **on_error** event handler receives a dScript object or a comp.state() function
- **on_resize** event handler receives a dScript object or a comp.state() function

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
| \`on_key_press\` | dScript | Key press handler | \`onKey(KeyCode.ENTER, action)\` |

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
| \`on_key_press\` | dScript | Key press handler | \`onKey(KeyCode.ENTER, action)\` |
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

### Section

The \`Section\` component is a container that can hold other components. It supports multiple ways to add child components.
And also its like the [Container](#Container) component but instead of export a \`<div>\` to render it exports and \`<section>\`.

#### Section Syntax

\`\`\`python
from dars.all import *
# Method 1: Pass components as arguments
container = Section(
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
container = Section(
    additional_children=components,
    style={
        "display": "flex",
        "flex-direction": "column",
        "padding": "20px",
        "background-color": "#f8f9fa"
    }
)

# Method 3: Add children after creation
container = Section(style={
    "display": "flex",
    "flex-direction": "column",
    "padding": "20px",
    "background-color": "#f8f9fa"
})
container.add_child(Text("Hello"))
container.add_child(Button("Click me"))
\`\`\`

#### Section Properties

| Property | Type | Description |
|-----------|------|-------------|
| \`children\` | tuple | Components passed as positional arguments |
| \`additional_children\` | list | Optional list of additional components |


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

### Chart

The \`Chart\` component renders interactive charts using Plotly.js.

#### Chart Syntax

\`\`\`python
from dars.components.visualization.chart import Chart
import plotly.graph_objects as go

fig = go.Figure(data=[go.Bar(x=['A', 'B', 'C'], y=[10, 20, 15])])

chart = Chart(
    figure=fig,
    width=800,
    height=400,
    style={"margin": "20px auto"}
)
\`\`\`

#### Chart Properties

| Property | Type | Description |
|----------|------|-------------|
| \`figure\` | plotly.graph_objects.Figure | Plotly figure object |
| \`width\` | int/str | Width in pixels or CSS value |
| \`height\` | int/str | Height in pixels or CSS value |
| \`config\` | dict | Plotly configuration options |

### DataTable

The \`DataTable\` component displays tabular data with optional Pandas DataFrame support.

#### DataTable Syntax

\`\`\`python
from dars.components.visualization.table import DataTable

# Using list of dicts (recommended)
data = [
    {'Name': 'Alice', 'Age': 30, 'City': 'New York'},
    {'Name': 'Bob', 'Age': 25, 'City': 'London'}
]
table = DataTable(data, theme='dark')

# With custom columns and formatters
data = [{'price': 99.99, 'qty': 5}, {'price': 149.99, 'qty': 3}]
table = DataTable(
    data,
    columns=[
        {'key': 'price', 'label': 'Price', 'formatter': lambda x: f'\${x:.2f}'},
        {'key': 'qty', 'label': 'Quantity', 'align': 'center'}
    ],
    striped=True,
    hover=True
)
\`\`\`

#### DataTable Properties

| Property | Type | Description | Default |
|----------|------|-------------|---------|
| \`data\` | DataFrame/list | Data source | - |
| \`columns\` | list | Column definitions | Auto-inferred |
| \`index\` | bool | Show DataFrame index | \`False\` |
| \`header\` | bool | Show header row | \`True\` |
| \`striped\` | bool | Alternating row colors | \`True\` |
| \`hover\` | bool | Hover effects | \`True\` |
| \`bordered\` | bool | Cell borders | \`True\` |
| \`compact\` | bool | Compact spacing | \`False\` |
| \`theme\` | str/dict | 'light', 'dark', or custom | \`'light'\` |


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

Components provide a solid foundation for creating modern and responsive user interfaces that can be exported to multiple platforms while maintaining consistency and functionality.`},{type:"T9",id:"markdown_120",key:"0/2/0/9",text:`# Dars Animation System

Dars provides a powerful and easy-to-use animation system built on top of the Web Animations API. It allows you to add professional-grade animations to your components with simple Python function calls.

## Animation Overview

All animations in Dars are **dScript** objects. This means they:
- Run entirely on the client side (zero latency)
- Can be assigned to any event handler (\`on_click\`, \`on_mouseover\`, etc.)
- Can be chained together using \`.then()\` or the \`sequence()\` helper
- Return Promises, allowing for complex orchestration

## Animation Quick Start

\`\`\`python
from dars.all import *

# Simple fade in
button.on_click = fadeIn(id="my-element")

# Chain animations
button.on_click = sequence(
    fadeOut(id="old-panel"),
    fadeIn(id="new-panel")
)
\`\`\`

## Animation Reference

### Fade Animations

Control visibility with opacity transitions.

#### \`fadeIn(id, duration=300, easing="ease")\`
Fades an element in from opacity 0 to 1. Sets \`display: block\` automatically.

\`\`\`python
fadeIn(id="modal", duration=500)
\`\`\`

#### \`fadeOut(id, duration=300, easing="ease", hide=True)\`
Fades an element out from current opacity to 0.
- \`hide\`: If \`True\` (default), sets \`display: none\` after animation completes.

\`\`\`python
fadeOut(id="notification", duration=2000, hide=True)
\`\`\`

### Slide Animations

Move elements into or out of view.

#### \`slideIn(id, direction="down", duration=300, easing="ease")\`
Slides an element into its final position.
- \`direction\`: \`"up"\`, \`"down"\`, \`"left"\`, \`"right"\` (from where it enters)

\`\`\`python
slideIn(id="sidebar", direction="left", duration=400)
\`\`\`

#### \`slideOut(id, direction="up", duration=300, easing="ease", hide=True)\`
Slides an element out of view.
- \`direction\`: \`"up"\`, \`"down"\`, \`"left"\`, \`"right"\` (to where it exits)

\`\`\`python
slideOut(id="sidebar", direction="left", duration=400)
\`\`\`

### Scale Animations

Zoom elements in and out.

#### \`scaleIn(id, duration=300, easing="ease", from_scale=0.0)\`
Scales an element up to its natural size (scale 1).
- \`from_scale\`: Starting scale factor (0.0 to 1.0)

\`\`\`python
scaleIn(id="popup", from_scale=0.5)
\`\`\`

#### \`scaleOut(id, duration=300, easing="ease", to_scale=0.0, hide=True)\`
Scales an element down.
- \`to_scale\`: Ending scale factor (0.0 to 1.0)

\`\`\`python
scaleOut(id="popup", to_scale=0.0)
\`\`\`

### Attention Seekers

Draw user attention to elements.

#### \`shake(id, intensity=5, duration=500)\`
Shakes an element horizontally. Great for error feedback.
- \`intensity\`: Shake distance in pixels.

\`\`\`python
shake(id="login-form", intensity=10)
\`\`\`

#### \`bounce(id, distance=20, duration=600)\`
Bounces an element vertically.
- \`distance\`: Bounce height in pixels.

\`\`\`python
bounce(id="notification-icon", distance=15)
\`\`\`

#### \`pulse(id, scale=1.1, duration=400, iterations=1)\`
Pulses an element (scales up and down).
- \`scale\`: Max scale during pulse.
- \`iterations\`: Number of pulses. Use \`"infinite"\` for continuous pulsing.

\`\`\`python
# Single pulse
pulse(id="heart-icon")

# Continuous heartbeat
pulse(id="status-dot", iterations="infinite", duration=1000)
\`\`\`

### Transformations

Rotate and flip elements.

#### \`rotate(id, degrees=360, duration=500, easing="ease")\`
Rotates an element.

\`\`\`python
rotate(id="refresh-icon", degrees=180)
\`\`\`

#### \`flip(id, axis="y", duration=600)\`
Flips an element 180 degrees around an axis.
- \`axis\`: \`"x"\` (horizontal flip) or \`"y"\` (vertical flip).

\`\`\`python
flip(id="card", axis="y")
\`\`\`

### Property Transitions

Animate specific CSS properties.

#### \`colorChange(id, from_color, to_color, duration=500, property="background-color")\`
Smoothly transitions a color property.

\`\`\`python
colorChange(id="btn", from_color="#fff", to_color="#f00", property="background-color")
\`\`\`

#### \`morphSize(id, to_width, to_height, duration=500, easing="ease")\`
Changes the dimensions of an element.

\`\`\`python
morphSize(id="panel", to_width="100%", to_height="500px")
\`\`\`

## Chaining & Sequencing

You can run animations in sequence using the \`sequence()\` helper or the \`.then()\` method.

### Using \`sequence()\`

The easiest way to run animations one after another.

\`\`\`python
from dars.all import sequence, fadeIn, slideIn

button.on_click = sequence(
    fadeIn(id="header"),
    slideIn(id="content", direction="up"),
    fadeIn(id="footer")
)
\`\`\`

### Using \`.then()\`

For more granular control or branching logic.

\`\`\`python
anim1 = fadeIn(id="box1")
anim2 = slideIn(id="box2")

# Run anim1, then anim2
button.on_click = anim1.then(anim2)
\`\`\`

### Parallel Animations

To run animations simultaneously, simply trigger them in the same event handler (or use a list of handlers).

\`\`\`python
# Both start at the same time
button.on_click = [
    fadeIn(id="box1"),
    slideIn(id="box2")
]
\`\`\`
`},{type:"T9",id:"markdown_121",key:"0/2/0/10",text:`# Custom Components in Dars Framework

Dars offers two ways to create custom components: **Function Components** (Recommended) and **Class Components** (Legacy).

## Function Components (Recommended)

Function Components are the modern way to create reusable UI elements. They use simple functions with f-string templates and automatically handle framework features like IDs, styling, and events.

### Basic Syntax

Use the \`@FunctionComponent\` decorator. You can access framework properties (\`id\`, \`class_name\`, \`style\`, \`children\`) using the \`Props\` helper object or by declaring them as arguments.

#### Option 1: Using \`Props\` Object (Cleanest)

\`\`\`python
from dars.all import *

@FunctionComponent
def UserCard(name, email, **props):
    return f"""
    <div {Props.id} {Props.class_name} {Props.style}>
        <h3>{name}</h3>
        <p>{email}</p>
        <div class="card-body">
            {Props.children}
        </div>
    </div>
    """

# Usage
card = UserCard("John Doe", "john@example.com", id="user-1", style={"padding": "20px"})
\`\`\`

#### Option 2: Explicit Arguments

\`\`\`python
@FunctionComponent
def UserCard(name, email, id, class_name, style, children, **props):
    return f"""
    <div {id} {class_name} {style}>
        <h3>{name}</h3>
        <p>{email}</p>
        <div class="card-body">
            {children}
        </div>
    </div>
    """
\`\`\`

### Key Features

1.  **Automatic Property Injection**: The framework automatically injects the correct HTML attributes for \`{id}\`, \`{class_name}\`, and \`{style}\`.
2.  **State V2 Compatible**: Function components work seamlessly with \`State()\` and reactive updates.
3.  **Event Handling**: Events like \`on_click\` are handled automatically by the framework (passed via \`**props\`).
4.  **Children Support**: Use \`{Props.children}\` or \`{children}\` to render nested content.

### Example with State and Events

\`\`\`python
@FunctionComponent
def Counter(**props):
    return f"""
    <div {Props.id} {Props.class_name} {Props.style}>
        0 {Props.children}
    </div>
    """

# Create component with initial value "0"
counter = Counter(id="my-counter", children="0")

# Make it reactive controlling the 'text' property (textContent)
# Note: This replaces the entire content of the div with the new text
state = State(counter, text="0")

# Update it
Button("Increment", on_click=state.text.set("5"))
\`\`\`

---

## Using Hooks in FunctionComponents

FunctionComponents work seamlessly with all Dars hooks, enabling reactive and interactive behavior.

### useDynamic() - Reactive Bindings

Use \`useDynamic()\` to create reactive text that updates automatically when state changes:

\`\`\`python
from dars.all import *

userState = State("user", name="John Doe", status="Active")

@FunctionComponent
def UserCard(**props):
    return f'''
    <div {Props.id} {Props.class_name} {Props.style}>
        <h3>Name: {useDynamic("user.name")}</h3>
        <p>Status: {useDynamic("user.status")}</p>
        {Props.children}
    </div>
    '''

# The name and status will update automatically when state changes
card = UserCard(id="user-card")
Button("Update", on_click=userState.name.set("Jane Doe"))
\`\`\`

### useValue() - Initial Values with Selectors

Use \`useValue()\` with selectors to set initial values and enable value extraction:

\`\`\`python
from dars.all import *

app = App("Example of hooks")

userState = State("user", name="Jane Doe", email="jane@example.com", display="None")

@FunctionComponent
def UserForm(**props):
    return f'''
    <div {Props.id} {Props.class_name} {Props.style}>
        <input value="{useValue("user.name", ".name-input")}" />
        <input value="{useValue("user.email", "#email-field")}" />
        <span>{useValue("user.age", ".age-display")}</span>
        <span>{useDynamic("user.display")}</span>
    </div>
    '''


@route("/")
def index():
    return Page(
        UserForm(id="user-form"),
        # Extract values using V() helper with the selectors
        Button(
            "Get Name",
            on_click=userState.display.set(
                "Name: " + V(".name-input")  # Extract current value
            )
        ),

        Button(
            "Combine Values",
            on_click=userState.display.set(
                V(".name-input") + " (" + V("#email-field") + ")"
            )
        )
    )

app.add_page("index", index(), title="hooks", index=True)

if __name__ == "__main__":
    app.rTimeCompile()
\`\`\`

### useWatch() - Side Effects

Use \`useWatch()\` to monitor state changes and execute side effects:

\`\`\`python
from dars.all import *

app = App("Example of hooks")

cartState = State("cart", total=0.0)

@FunctionComponent
def CartSummary(total=0,**props):
    return f'''
    <div {Props.id} {Props.class_name} {Props.style}>
        <h3>Cart Total: \${useDynamic("cart.total")}</h3>
        {Props.children}
    </div>
    '''

# Watch for cart changes and log
app.useWatch("cart.total", log("Cart total changed!"))

@route("/")
def index():
    return Page(
        CartSummary(id="cart-summary", total=0),
        # Button to add $10 to cart total using V() with state path
        Button("Add $10", on_click=cartState.total.set(
            V("cart.total").float() + 10
        ))
    )

app.add_page("index", index(), title="hooks", index=True)

if __name__ == "__main__":
    app.rTimeCompile()
\`\`\`

### Combining Multiple Hooks

You can combine multiple hooks for complex interactive components:

\`\`\`python
from dars.all import *

app = App("Example of hooks")

productState = State("product", 
    name="Widget", 
    price=19.99, 
    quantity=1,
    total=19.99
)

@FunctionComponent
def ProductCard(**props):
    return f'''
    <div {Props.id} {Props.class_name} {Props.style}>
        <!-- useDynamic for reactive display -->
        <h3>{useDynamic("product.name")}</h3>
        <p>Price: \${useDynamic("product.price")}</p>
        <!-- useValue for editable quantity -->
        <h3>Number to multiply with price</h3>
        <input type="number" 
               value="{useValue("product.quantity", ".qty-input")}"
               min="1" />
        
        
        <!-- useDynamic for calculated total -->
        <p>Total: \${useDynamic("product.total")}</p>
        
        {Props.children}
    </div>
    '''

# Watch for total changes and show alert
app.useWatch("product.total", log("Total updated!"))

@route("/")
def index():
    return Page(
        ProductCard(id="product-card",name="Milk", price=100, quantity=0, total=0 ),
        Button(
            "Calculate Total",
            on_click=productState.total.set(
                V(".qty-input").int() * V("product.price").float()
            )
        )

    )

app.add_page("index", index(), title="hooks", index=True)

if __name__ == "__main__":
    app.rTimeCompile()
\`\`\`

---

## Class Components (Legacy)

This is the older method of creating components by inheriting from the \`Component\` class. It is more verbose and requires manual handling of rendering logic.

\`\`\`python
from dars.all import *
from dars.core.component import Component

class CustomComponent(Component):
    def __init__(self, title: str, id: str = None, **props):
        super().__init__(**props)
        self.title = title
        self.id = id
        # Manual event attachment
        self.set_event(EventTypes.CLICK, dScript("console.log('click')"))

    def render(self, exporter: 'Exporter') -> str:
        # Manual children rendering
        children_html = self.render_children(exporter)
        
        return f'''
        <div class="my-component" id="{self.id}" style="{self.style}">
            <h2>{self.title}</h2>
            <div class="content">
                {children_html}
            </div>
        </div>
        '''
\`\`\`

---
`},{type:"T9",id:"markdown_122",key:"0/2/0/11",text:`# Hooks System

Dars Framework introduces a **Hooks system** inspired by React, enabling reactive and stateful behavior in both FunctionComponents and built-in components.

## Overview Hooks

Hooks provide a way to add reactive capabilities to your application. They enable features like:

- **Reactive state bindings** - Automatically update UI when data changes
- **State monitoring** - Watch for state changes and execute side effects
- **External state integration** - Connect components to global state

---

## Important: State ID Best Practices

> [!IMPORTANT]
> When using \`State\` objects with hooks like \`useDynamic\` and \`useValue\`, the **state ID should NOT match any component ID** in your DOM. The state ID is a unique identifier for the state object itself, not a component.

### Why This Matters

The reactive system uses **watchers** to update components when state changes. When you create a \`State\` object, the ID you provide is used to register the state in the internal registry, not to identify a specific DOM element.

### Examples

**X Incorrect - State ID matches component ID:**
\`\`\`python
# DON'T do this
state = State("my-button", count=0, disabled=False)
Button(id="my-button", text=useDynamic("my-button.count"))
\`\`\`

In this example, both the state and the button have the ID \`"my-button"\`, which can cause confusion and unexpected behavior.

**\u2713 Correct - State has unique ID:**
\`\`\`python
# DO this - give state a descriptive, unique ID
counter_state = State("counter-state", count=0, disabled=False)
Button(id="my-button", text=useDynamic("counter-state.count"))
Button(id="another-button", disabled=useDynamic("counter-state.disabled"))
\`\`\`

**\u2713 Also Correct - Multiple components sharing same state:**
\`\`\`python
# One state can control multiple components
ui_state = State("ui", count=0, is_disabled=False, message="Hello")

Container(
    Text(text=useDynamic("ui.message")),
    Button(id="btn-1", disabled=useDynamic("ui.is_disabled")),
    Button(id="btn-2", disabled=useDynamic("ui.is_disabled")),
    Text(text=useDynamic("ui.count"))
)
\`\`\`

### Key Takeaways

1. **State IDs are for the state object**, not for DOM elements
2. **One state can control many components** through reactive bindings
3. **Component IDs should be unique** across your DOM
4. **State IDs should be descriptive** of what they manage (e.g., \`"user-data"\`, \`"cart-state"\`, \`"ui-controls"\`)

---

## useValue() - Initial Value Access

The \`useValue()\` hook allows you to access the **initial value** of a state property without creating a reactive binding. This is ideal for form inputs where you want to set a default value but allow the user to edit it freely.

### Basic Usage

Pass \`useValue()\` to component properties to set their initial value from state:

\`\`\`python
from dars.all import *

userState = State("user", name="John Doe", email="john@example.com")

# Input with initial value from state (editable by user)
Input(value=useValue("user.name"))

# Textarea with initial value
Textarea(value=useValue("user.email"))
\`\`\`

### Usage in FunctionComponents with Selectors

\`useValue()\` supports automatic selector application in FunctionComponents! When you provide a selector (class or ID), it will be automatically applied to the element where the value is used.

\`\`\`python
from dars.all import *

app = App("Example of hooks")

userState = State("user", name="Jane Doe", email="jane@example.com", display="None")

@FunctionComponent
def UserForm(**props):
    return f'''
    <div {Props.id} {Props.class_name} {Props.style}>
        <input value="{useValue("user.name", ".name-input")}" />
        <input value="{useValue("user.email", "#email-field")}" />
        <span>{useValue("user.age", ".age-display")}</span>
        <span>{useDynamic("user.display")}</span>
    </div>
    '''


@route("/")
def index():
    return Page(
        UserForm(id="user-form"),
        # Extract values using V() helper with the selectors
        Button(
            "Get Name",
            on_click=userState.display.set(
                "Name: " + V(".name-input")  # Extract current value
            )
        ),

        Button(
            "Combine Values",
            on_click=userState.display.set(
                V(".name-input") + " (" + V("#email-field") + ")"
            )
        )
    )

app.add_page("index", index(), title="hooks", index=True)

if __name__ == "__main__":
    app.rTimeCompile()
\`\`\`

**How it works:**
1. \`useValue("user.name", ".name-input")\` sets initial value "Jane Doe" and applies class \`name-input\` to the input
2. User can edit the value freely
3. \`V(".name-input")\` extracts the current value (even if modified by user)
4. Perfect for forms where you need both initial values and value extraction

**Supported selectors:**
- **Class selectors** (\`.foo\`) \u2192 Added to element's \`class\` attribute
- **ID selectors** (\`#bar\`) \u2192 Set as element's \`id\` attribute

### Difference from useDynamic

- **\`useDynamic("state.prop")\`**: Creates a **reactive binding**. If the state changes, the input value updates automatically.
- **\`useValue("state.prop")\`**: Sets the **initial value only**. If the state changes later, the input value does NOT update. This prevents overwriting user input while they are typing.

### Syntax

\`\`\`python
useValue(state_path: str, selector: str = None) -> ValueMarker
\`\`\`

**Parameters:**
- \`state_path\`: Dot-notation path to state property (e.g., \`"user.name"\`)
- \`selector\`: Optional CSS selector (class or ID) to apply to the element

**Returns:**
- \`ValueMarker\` object that resolves to the initial value during component rendering.

---

## useDynamic() - Reactive State Binding

The \`useDynamic()\` hook creates reactive bindings between external \`State\` objects and component properties.

### 1. Usage in Built-in Components

You can pass \`useDynamic()\` directly to properties of built-in components like \`Text\`, \`Button\`, \`Input\`, etc.

\`\`\`python
from dars.all import *

# Create state
userState = State("user", name="John Doe", status="Active", is_admin=False)

# Bind directly to props
card = Container(
    # Bind text property
    Text(text=useDynamic("user.name"), style={"font-weight": "bold"}),
    
    # Bind input value
    Input(value=useDynamic("user.name"), placeholder="Edit name"),
    
    # Bind button text and disabled state
    Button(
        text=useDynamic("user.status"), 
        disabled=useDynamic("user.is_admin"),
        on_click=userState.status.set("Clicked!")
    )
)
\`\`\`

### Supported Properties

\`useDynamic\` and \`useValue\` supports binding to the following properties on built-in components:

| Component | Properties |
|-----------|------------|
| \`Text\` | \`text\`, \`innerHTML\` |
| \`Button\` | \`text\`, \`disabled\` |
| \`Input\` | \`value\`, \`placeholder\`, \`disabled\`, \`readonly\`, \`required\` |
| \`Textarea\` | \`value\`, \`placeholder\`, \`disabled\`, \`readonly\`, \`required\` |
| \`Image\` | \`src\`, \`alt\` |
| \`Link\` | \`href\`, \`text\` |
| \`Checkbox\` | \`checked\`, \`disabled\`, \`required\` |
| \`RadioButton\` | \`checked\`, \`disabled\`, \`required\` |
| \`Select\` | \`disabled\`, \`required\` |
| \`Slider\` | \`disabled\` |

Boolean attributes like \`disabled\` and \`checked\` will be toggled based on the truthiness of the state value.

### 2. Usage in FunctionComponents

You can also use \`useDynamic()\` within \`FunctionComponent\` templates to create reactive spans.

\`\`\`python
@FunctionComponent
def UserCard(**props):
    return f'''
    <div {Props.id} {Props.class_name} {Props.style}>
        <h3>Name: {useDynamic("user.name")}</h3>
        <p>Status: {useDynamic("user.status")}</p>
    </div>
    '''
\`\`\`

### Syntax

\`\`\`python
useDynamic(state_path: str) -> DynamicBinding
\`\`\`

**Parameters:**
- \`state_path\`: Dot-notation path to state property (e.g., \`"user.name"\`, \`"cart.total"\`)

**Returns:**
- \`DynamicBinding\` object that resolves to the current value during render and updates automatically when state changes.

---

## useWatch() - State Monitoring

The \`useWatch()\` hook allows you to monitor state changes and execute callbacks (side effects). It supports watching single or multiple state properties and executing one or more callbacks.

### Basic Usage

The recommended way to use \`useWatch\` is via the \`app.useWatch()\` or \`page.useWatch()\` methods:

**Single State Property**
\`\`\`python
from dars.all import *

cartState = State("cart", count=0, total=0.0)

# Logs to console whenever cart.count changes
app.useWatch("cart.count", log("Cart updated!"))
app.useWatch("cart.total", log("Total changed"))
\`\`\`

**Multiple State Properties (Array Syntax)**
\`\`\`python
productState = State("product", name="Widget", price=19.99, info="")

# Watch multiple properties - callback executes when ANY of them change
app.useWatch(
    ["product.name", "product.price"],
    productState.info.set("Product: " + V("product.name") + " - $" + V("product.price"))
)
\`\`\`

**Multiple Callbacks**
\`\`\`python
# Execute multiple callbacks when state changes
app.useWatch(
    "cart.total",
    log("Total changed!"),
    alert("Cart updated")
)

# Combine array syntax with multiple callbacks
app.useWatch(
    ["product.name", "product.price"],
    productState.info.set("Product: " + V("product.name") + " - $" + V("product.price")),
    log("Product info updated")
)
\`\`\`

**Page-Specific Watchers (page.useWatch)**
\`\`\`python
@route("/cart")
def cart_page():
    page = Page()
    
    # This watcher only runs on the cart page
    page.useWatch("cart.total", log("Total changed!"))
    
    page.add(
        Container(
            Text(useDynamic("cart.total"))
        )
    )
    return page
\`\`\`

You can also use the classic syntax with \`add_script\`:
\`\`\`python
app.add_script(useWatch("state.prop", log("Changed!")))
\`\`\`

### Syntax

\`\`\`python
useWatch(
    state_path: Union[str, List[str]], 
    *callbacks: Union[dScript, str, Callable]
) -> Union[dScript, WatchMarker]
\`\`\`

**Parameters:**
- \`state_path\`: State property path(s) to watch. Can be:
    - Single path string (e.g., \`"user.name"\`)
    - List of paths (e.g., \`["product.name", "product.price"]\`)
- \`*callbacks\`: One or more callbacks to execute when state changes. Each can be:
    - \`dScript\` object (e.g., \`log("Changed")\`, \`alert("Update")\`)
    - State setter (e.g., \`productState.info.set(...)\`)
    - Inline JavaScript string
    - Python callable returning a \`dScript\`

**Behavior:**
- When using an array of state paths, the callback(s) execute when **any** of the watched properties change
- Multiple callbacks execute in the order they are provided
- Callbacks can access current state values using \`V()\` helper

---

## Pythonic Value Helpers

Dars provides a set of helpers to make working with DOM values and reactive state completely Pythonic, eliminating the need for raw JavaScript.

### V() - Value Reference

The \`V()\` helper allows you to extract values from **DOM elements** (via CSS selectors) or **reactive state** (via state paths).

#### CSS Selectors (DOM Elements)

\`\`\`python
from dars.all import *

# Select by ID
V("#myInput")

# Select by Class
V(".myClass")

\`\`\`

#### State Paths (Reactive State)

**New in v1.5.8**: \`V()\` now supports extracting values directly from reactive state created by \`useDynamic()\`:

\`\`\`python
# Extract from reactive state
V("cart.total")      # Gets current value of cart.total
V("user.name")       # Gets current value of user.name
V("product.price")   # Gets current value of product.price
\`\`\`

**How it works:**
- \`V("cart.total")\` finds the reactive element created by \`useDynamic("cart.total")\`
- Reads its current \`textContent\` value
- Perfect for combining reactive state with calculations

#### Transformations

You can chain transformation methods to process values before using them:

\`\`\`python
# String transformations
V("#name").upper()   # "JOHN"
V("#name").lower()   # "john"
V("#name").trim()    # Remove whitespace

# Numeric transformations (required for math operations!)
V("#age").int()      # 25 (integer)
V("#price").float()  # 19.99 (float)
V("cart.total").float()  # Extract state value as float
\`\`\`

#### Operations

\`ValueRef\` objects support Python operators with **important validation**:

**String Concatenation (Always Allowed)**
\`\`\`python
# Concatenation works without transformations
state.fullname.set(V("#first") + " " + V("#last"))
message = "Total: $" + V("cart.total")
\`\`\`

**Arithmetic Operations (Require Numeric Transformations)**

**New in v1.5.8**: Arithmetic operators (\`*\`, \`/\`, \`-\`, \`%\`, \`**\`) now **require** \`.int()\` or \`.float()\` transformations to prevent accidental string concatenation:

\`\`\`python
# CORRECT - With numeric transformations
state.total.set(V("#price").float() * V("#qty").int())
state.age.set(V("#age").int() + 10)
discount = V("product.price").float() * 0.9

# CORRECT - Combining DOM and state values
productState.total.set(
    V(".qty-input").int() * V("product.price").float()
)

# ERROR - Without transformations
state.total.set(V("#price") * V("#qty"))
# TypeError: Multiplication requires numeric transformation.
#            Use V('#price').int() or V('#price').float() before multiplying.
\`\`\`

**Supported Operators:**
- \`+\` - Addition/Concatenation (always allowed)
- \`*\` - Multiplication (requires \`.int()\` or \`.float()\`)
- \`/\` - Division (requires \`.int()\` or \`.float()\`)
- \`-\` - Subtraction (requires \`.int()\` or \`.float()\`)
- \`%\` - Modulo (requires \`.int()\` or \`.float()\`)
- \`**\` - Power (requires \`.int()\` or \`.float()\`)

#### Complete Example

\`\`\`python
from dars.all import *

app = App("Shopping Cart")

# Reactive state
cartState = State("cart", total=0.0)
productState = State("product", name="Widget", price=19.99, quantity=1)

@FunctionComponent
def ProductCard(**props):
    return f'''
    <div {Props.id} {Props.class_name} {Props.style}>
        <!-- Reactive display -->
        <h3>{useDynamic("product.name")}</h3>
        <p>Price: \${useDynamic("product.price")}</p>
        
        <!-- Editable quantity with selector -->
        <input type="number" 
               value="{useValue("product.quantity", ".qty-input")}"
               min="1" />
        
        <!-- Reactive total -->
        <p>Total: \${useDynamic("cart.total")}</p>
    </div>
    '''

@route("/")
def index():
    return Page(
        ProductCard(id="product-card", name="Milk", price=100, quantity=2, total=0),
        
        # Calculate: DOM input \xD7 State value
        Button("Calculate Total", on_click=cartState.total.set(
            V(".qty-input").int() * V("product.price").float()
        )),
        
        # String concatenation (no transformation needed)
        Button("Show Info", on_click=productState.name.set(
            "Product: " + V("product.name") + " - $" + V("product.price")
            )
        )
    )

app.add_page("index", index(), title="Product", index=True)

# Watch for changes
app.useWatch("cart.total", log("Cart total changed!"))

if __name__ == "__main__":
    app.rTimeCompile()
\`\`\`

### url() - URL Builder

The \`url()\` helper constructs dynamic URLs by interpolating \`ValueRef\` objects into a template string.

\`\`\`python
# Generates: https://api.example.com/users/123/profile
fetch(
    url("https://api.example.com/users/{id}/profile", id=V("#userId"))
)

# With state values
fetch(
    url("/api/products/{id}", id=V("product.id"))
)

# Mixed
fetch(
    url("/api/{resource}/{id}", 
        resource="users", 
        id=V("#userId"))
)
\`\`\`

**Note:** Use standard Python format string syntax \`{key}\` for placeholders.

---

## Best Practices

**Do:**
- Use \`useDynamic\` for simple text/value updates.
- Use \`useWatch\` for side effects like logging, analytics, or complex logic.
- Use \`useValue\` with selectors for form inputs that need value extraction.
- Use consistent state naming (e.g., \`"user"\`, \`"cart"\`).
- Always use \`.int()\` or \`.float()\` before arithmetic operations with \`V()\`.

**Don't:**
- Use with non-existent state paths.
- Nest state paths more than 2 levels deep (currently supports \`stateName.property\`).
- Use arithmetic operators without numeric transformations.

---`},{type:"T9",id:"markdown_123",key:"0/2/0/12",text:`# Keyboard Events in Dars

Dars provides a powerful and intuitive system for handling keyboard events in your applications. This guide covers everything from basic key detection to advanced global shortcuts.

---

## Basic Keyboard Events

All Dars components support the \`on_key_press\` event handler for keyboard interactions.

### Simple Example

\`\`\`python
from dars.all import *

Input(
    id="search",
    on_key_press=log("Key pressed!")
)
\`\`\`

> **Note:** Use \`on_key_press\` as the universal keyboard event. The older \`on_key_down\` and \`on_key_up\` events have been deprecated in favor of this simpler approach.

---

## KeyCode Constants

The \`KeyCode\` class provides constants for all keyboard keys, making your code more readable and maintainable.

### Available Keys

\`\`\`python
from dars.all import *

# Navigation keys
KeyCode.ENTER
KeyCode.TAB
KeyCode.ESCAPE  # or KeyCode.ESC
KeyCode.BACKSPACE
KeyCode.DELETE

# Arrow keys
KeyCode.UP       # or KeyCode.ARROWUP
KeyCode.DOWN     # or KeyCode.ARROWDOWN
KeyCode.LEFT     # or KeyCode.ARROWLEFT
KeyCode.RIGHT    # or KeyCode.ARROWRIGHT

# Letters (a-z)
KeyCode.A
KeyCode.B
# ... through ...
KeyCode.Z

# Numbers
KeyCode.ZERO  # or KeyCode.0
KeyCode.ONE   # or KeyCode.1
# ... through ...
KeyCode.NINE  # or KeyCode.9

# Function keys
KeyCode.F1
KeyCode.F2
# ... through ...
KeyCode.F12

# Special characters
KeyCode.SPACE
KeyCode.PLUS
KeyCode.MINUS
KeyCode.SLASH
KeyCode.COMMA
KeyCode.PERIOD
\`\`\`

### Dynamic Key Access

\`\`\`python
# Get key code by name
key = KeyCode.key('enter')  # Returns 'Enter'
key = KeyCode.key('A')      # Returns 'a'
\`\`\`

---

## The onKey() Helper

The \`onKey()\` function is the **recommended way** to handle specific keyboard keys with optional modifier keys.

### Basic Usage

\`\`\`python
from dars.all import *

# Simple key detection
Input(
    on_key_press=onKey(KeyCode.ENTER, log("Enter pressed!"))
)
\`\`\`

### With Modifiers

\`\`\`python
# Ctrl modifier
Container(
    on_key_press=onKey(KeyCode.S, alert("Saving..."), ctrl=True)
)

# Multiple modifiers
Container(
    on_key_press=onKey(KeyCode.Z, log("Redo"), ctrl=True, shift=True)
)
\`\`\`

### Available Modifiers

- \`ctrl\` - Ctrl key (Command on Mac)
- \`shift\` - Shift key
- \`alt\` - Alt key
- \`meta\` - Meta/Command key

### Complete Example

\`\`\`python
from dars.all import *

app = App("onKey Example")

formState = State("form", message="")

@route("/")
def index():
    return Page(
        Input(
            id="input",
            placeholder="Press Enter to submit",
            on_key_press=onKey(
                KeyCode.ENTER,
                formState.message.set("Submitted!"),
                ctrl=False  # Just Enter, no modifier needed
            )
        ),
        Text(useDynamic("form.message"))
    )

app.add_page("index", index(), index=True)
\`\`\`

---

## The switch() Function

Use \`switch()\` to handle multiple different keys in a single event handler.

### Basic Usage

\`\`\`python
from dars.all import *

Input(
    on_key_press=switch({
        KeyCode.ENTER: log("Enter pressed"),
        KeyCode.ESCAPE: alert("Escape pressed"),
    })
)
\`\`\`

### With Multiple Actions

\`\`\`python
formState = State("form", username="", password="")

Input(
    on_key_press=switch({
        KeyCode.ENTER: [
            formState.message.set("Submitted!"),
            alert("Form submitted!")
        ],
        KeyCode.ESCAPE: [
            clearInput("username"),
            clearInput("password"),
            formState.message.set("Cleared!")
        ]
    })
)
\`\`\`

### Complete Example

\`\`\`python
from dars.all import *

app = App("KeyCode Clean Example")

# State
formState = State("form", 
    username="", 
    password="", 
    message="Use keyboard shortcuts!"
)

@FunctionComponent
def LoginForm(**props):
    return f'''
    <div {Props.id} {Props.class_name} {Props.style}>
        <h2>Login Form with Keyboard Shortcuts</h2>
        <p style="color: #666;">{useDynamic("form.message")}</p>
        
        <input 
            type="text" 
            id="username-input"
            placeholder="Username"
            style="display: block; margin: 10px 0; padding: 8px; width: 300px;"
        />
        
        <input 
            type="password" 
            id="password-input"
            placeholder="Password"
            style="display: block; margin: 10px 0; padding: 8px; width: 300px;"
        />
        
        <div style="margin-top: 30px; padding: 15px; background: #f5f5f5; border-radius: 4px;">
            <h3 style="margin-top: 0;">Global Keyboard Shortcuts:</h3>
            <ul style="margin: 0; padding-left: 20px;">
                <li><strong>Ctrl+Enter</strong> - Submit form (shows alert)</li>
                <li><strong>Ctrl+F</strong> - Clear form</li>
                <li><strong>Ctrl+S</strong> - Save document</li>
            </ul>
            <p style="margin-top: 10px; font-size: 0.9em; color: #666;">
                Note: These are GLOBAL shortcuts that work anywhere on the page without blocking normal typing.
            </p>
        </div>
    </div>
    '''

@route("/")
def index():
    return Page(
        LoginForm(id="login-form"),
        Input(value="", on_key_up=onKey("R", action=log("Logged"))),
        # Buttons using State.set() and utils_ds functions
        Button(
            "Submit",
            on_click=[
                formState.message.set("Form submitted via button!"),
                alert("Form submitted!")
            ]
        ),
        
        Button(
            "Clear", 
            on_click=[
                formState.username.set(""),
                formState.password.set(""),
                formState.message.set("Form cleared via button!"),
                clearInput("username-input"),
                clearInput("password-input")
            ]
        ),
        
        Button(
            "Show Username",
            on_click=alert(V("#username-input"))
        ),
        
        Button(
            "Log Message",
            on_click=log(V("form.message"))
        ),
    )

addGlobalKeys(app, {
    (KeyCode.ENTER, 'ctrl'): [
        formState.message.set("Form submitted with Ctrl+Enter!"),
        alert("Form submitted!")
    ],
    (KeyCode.F, 'ctrl'): [
        formState.username.set(""),
        formState.password.set(""),
        formState.message.set("Form cleared with Ctrl+F!"),
        clearInput("username-input"),
        clearInput("password-input")
    ],
    (KeyCode.S, 'ctrl'): alert("Document saved! (Ctrl+S)"),
})

app.add_page("index", index(), title="KeyCode Example", index=True)

if __name__ == "__main__":
    app.rTimeCompile()
\`\`\`

---

## Global Keyboard Shortcuts

Use \`addGlobalKeys()\` to create app-wide keyboard shortcuts that work anywhere on the page.

### Why Global Shortcuts?

Global shortcuts are perfect for:
- App-level commands (Save, Undo, Redo)
- Navigation shortcuts
- Quick actions that should work anywhere

> **Important:** Always use modifier keys (Ctrl, Alt, etc.) with global shortcuts to avoid blocking normal typing in input fields.

### Basic Usage

\`\`\`python
from dars.all import *

app = App("Global Shortcuts")

# Define your actions
def save_document():
    return alert("Document saved!")

def undo():
    return log("Undo action")

# Add global shortcuts
addGlobalKeys(app, {
    (KeyCode.S, 'ctrl'): save_document(),
    (KeyCode.Z, 'ctrl'): undo()
})
\`\`\`

### With Multiple Actions

\`\`\`python
formState = State("form", data="")

addGlobalKeys(app, {
    (KeyCode.ENTER, 'ctrl'): [
        formState.data.set("Submitted!"),
        alert("Form submitted with Ctrl+Enter")
    ],
    (KeyCode.ESCAPE, 'ctrl'): [
        formState.data.set(""),
        log("Form cleared")
    ]
})
\`\`\`

### Multiple Modifiers

\`\`\`python
addGlobalKeys(app, {
    (KeyCode.Z, 'ctrl'): undo(),
    (KeyCode.Z, 'ctrl', 'shift'): redo(),
    (KeyCode.S, 'ctrl', 'shift'): save_as()
})
\`\`\`

### Complete Example

\`\`\`python
from dars.all import *

app = App("Global Shortcuts Example")

docState = State("document", 
    content="", 
    saved=False,
    message="Ready"
)

@route("/")
def index():
    return Page(
        Container(
            Text("Document Editor", style={"font-size": "24px", "font-weight": "bold"}),
            Text(useDynamic("document.message"), style={"color": "#666"}),
            
            Input(
                id="editor",
                placeholder="Start typing...",
                style={"width": "100%", "min-height": "200px"}
            ),
            
            Container(
                style={"margin-top": "20px", "padding": "15px", "background": "#f5f5f5"},
                children=[
                    Text("Global Shortcuts:", style={"font-weight": "bold"}),
                    Text("\u2022 Ctrl+S - Save"),
                    Text("\u2022 Ctrl+Z - Undo"),
                    Text("\u2022 Ctrl+Shift+Z - Redo"),
                ]
            )
        )
    )

# Global keyboard shortcuts
addGlobalKeys(app, {
    (KeyCode.S, 'ctrl'): [
        docState.saved.set(True),
        docState.message.set("Document saved!"),
        alert("Saved!")
    ],
    (KeyCode.Z, 'ctrl'): [
        docState.message.set("Undo"),
        log("Undo action")
    ]
})

app.add_page("index", index(), index=True)

if __name__ == "__main__":
    app.rTimeCompile()
\`\`\`

---

## Best Practices

### 1. Use Modifiers for Global Shortcuts

**Bad - Blocks typing:**
\`\`\`python
addGlobalKeys(app, {
    KeyCode.ENTER: submit_form()  # Blocks Enter in all inputs!
})
\`\`\`

**Good - Doesn't interfere:**
\`\`\`python
addGlobalKeys(app, {
    (KeyCode.ENTER, 'ctrl'): submit_form()  # Only Ctrl+Enter
})
\`\`\`

### 2. Use onKey() for Component-Specific Keys

**For specific components:**
\`\`\`python
Input(
    id="search",
    on_key_press=onKey(KeyCode.ENTER, perform_search())
)
\`\`\`

**For app-wide shortcuts:**
\`\`\`python
addGlobalKeys(app, {
    (KeyCode.F, 'ctrl'): focus("search")
})
\`\`\`

### 3. Use switch() for Multiple Keys

**Bad - Repetitive:**
\`\`\`python
Input(
    on_key_press=onKey(KeyCode.ENTER, action1())
)
Input(
    on_key_press=onKey(KeyCode.ESCAPE, action2())
)
\`\`\`

**Good - Clean:**
\`\`\`python
Container(
    on_key_press=switch({
        KeyCode.ENTER: action1(),
        KeyCode.ESCAPE: action2()
    })
)
\`\`\`

### 4. Combine with State and V()

\`\`\`python
formState = State("form", username="")

Input(
    id="username",
    on_key_press=onKey(KeyCode.ENTER, formState.username.set(V("#username")))
)
\`\`\`

---

## Summary

- **Use \`on_key_press\`** for all keyboard events (replaces \`on_key_down\` and \`on_key_up\`)
- **Use \`KeyCode\`** constants for readable key references
- **Use \`onKey()\`** for single key detection with optional modifiers
- **Use \`switch()\`** for handling multiple different keys
- **Use \`addGlobalKeys()\`** for app-wide shortcuts (always with modifiers!)
- **Combine with State and V()** for dynamic, reactive keyboard interactions
`},{type:"T9",id:"markdown_124",key:"0/2/0/13",text:`# Events in Dars

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


---

## Backend HTTP Integration

Dars provides HTTP utilities that can be used directly in event handlers:

\`\`\`python
from dars.all import *
from dars.backend import get, post, useData

# GET request on button click
fetch_btn = Button(
    "Fetch Data",
    on_click=get(
        id="apiData",
        url="https://api.example.com/data",
        callback=status_state.text.set("\u2705 Loaded!")
    )
)

# POST request with data binding
submit_btn = Button(
    "Submit",
    on_click=post(
        id="submitResult",
        url="https://api.example.com/submit",
        body={"name": "John", "email": "john@example.com"},
        callback=result_state.text.set(useData('submitResult').message)
    )
)

# Chain HTTP request with state updates
button.on_click = [
    status_state.text.set("Loading..."),
    get(
        id="userData",
        url="https://api.example.com/user/1",
        callback=(
            name_state.text.set(useData('userData').name)
            .then(status_state.text.set("Done!"))
        )
    )
]
\`\`\`
`},{type:"T9",id:"markdown_125",key:"0/2/0/14",text:`# Dars - Exporter Documentation

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

### Native Functions & Dynamic Updates

You can access native filesystem functions via the \`dars.desktop\` module:

\`\`\`python
from dars.desktop import read_text, write_text, read_file, write_file, list_directory, get_value
from dars.core.state import this
from dars.scripts.dscript import RawJS, dScript
\`\`\`

#### File System Operations

The desktop module provides async file operations that return \`dScript\` objects, perfect for chaining with \`this().state()\`:

**Reading Text Files**
\`\`\`python
# Simple read - button updates itself with file content
read_btn = Button("Load Config",
    on_click=read_text("config.txt").then(
        this().state(text=RawJS(dScript.ARG))
    )
)

# Update another component
display = Text("", id="display")
load_btn = Button("Load Data",
    on_click=read_text("data.txt").then(
        update_component("display", text=RawJS(dScript.ARG))
    )
)
\`\`\`

**Writing Text Files**
\`\`\`python

save_btn = Button("Save",
    on_click=write_text("output.txt", "Hello Dars!").then(
        this().state(text="Saved!", style={"color": "green"})
    )
)
\`\`\`

**Listing Directories**
\`\`\`python
from dars.desktop import list_directory, get_value


Button("Browse",
    on_click=list_directory(".").then(
        this().state(id="file-list", html=RawJS("""
            value.map(f => {
                const icon = f.isDirectory ? '\u{1F4C1}' : '\u{1F4C4}';
                return \`<div>\${icon} \${f.name}</div>\`;
            }).join('')
        """))
    )
)


Button("Python Files",
    on_click=list_directory(".", "*.py").then(
        this().state(id="count", text=RawJS("\`Found \${value.length} files\`"))
    )
)


Input(id="path", value=".")
Button("List Directory",
    on_click=list_directory(get_value("path")).then(
        this().state(id="output", html=RawJS("value.map(f => f.name).join('<br>')"))
    )
)


list_directory(".", "*", include_size=True)
\`\`\`

**Binary File Operations**
\`\`\`python

img_data = read_file("image.png")


write_file("output.bin", data_bytes)
\`\`\`

#### Chaining Multiple Operations

Use \`dScript.then()\` for sequential operations:

\`\`\`python
# Read \u2192 Process \u2192 Update \u2192 Write
Button("Process File",
    on_click=read_text("input.txt")
        .then(dScript(code="const processed = value.toUpperCase(); return processed;"))
        .then(write_text("output.txt", RawJS("processed")))
        .then(this().state(text="Complete!"))
)
\`\`\`

All file paths are relative to the app's directory. See [State Management](state_management.md#dynamic-state-updates--this) and [Scripts](scripts.md#chaining-scripts-then) for more details on \`this()\` and chaining.

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
`},{type:"T9",id:"markdown_126",key:"0/2/0/15",text:`# Dars - Script System

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

### Chaining Scripts (\`.then()\`)

You can chain multiple \`dScript\` objects using the \`.then()\` method. This is particularly useful when working with asynchronous operations like file reading in Electron.

\`\`\`python
from dars.desktop import read_text
from dars.core.state import this
from dars.scripts.dscript import RawJS, dScript

# Read a file and update a component with its content
# The result of the previous script is available as dScript.ARG (which resolves to 'value')
read_op = read_text("data.txt")
update_op = this().state(text=RawJS(dScript.ARG))

chained_script = read_op.then(update_op)
\`\`\`

The \`RawJS\` wrapper ensures that \`dScript.ARG\` is treated as a variable name (\`value\`) rather than a string literal \`"value"\`.

### State Navigation with \`state.state()\`

The \`state.state(idx)\` method allows you to navigate a component to a specific state index. This is the recommended way to trigger state transitions.

**Requirements**:
- The component must have a \`dState\` defined with the target index in its \`states\` array
- The index must be valid (0 to states.length - 1)

**Example: Toggle Button**
\`\`\`python
from dars.all import *
from dars.core.state import dState

# Create a button that toggles between two states
toggle_btn = Button("Off", id="ToggleBtn")

# Define states for the button
toggle_state = dState("toggle", component=toggle_btn, states=[0, 1])

# Configure state 1 appearance and behavior
toggle_state.cState(1, mods=[
    Mod.set(toggle_btn, 
        text="On",
        style={'background-color': 'green', 'color': 'white'},
        on_click=toggle_state.state(0)  # Return to state 0 when clicked
    )
])

# Initial click navigates to state 1
toggle_btn.on_click = toggle_state.state(1)
\`\`\`

**Example: Cycle Through States**
\`\`\`python
# Create a button that cycles through multiple states
cycle_btn = Button("State 0", id="CycleBtn")
cycle_state = dState("cycler", component=cycle_btn, states=[0, 1, 2, 3])

# Each state navigates to the next
cycle_state.cState(1, mods=[
    Mod.set(cycle_btn, text="State 1", on_click=cycle_state.state(2))
])
cycle_state.cState(2, mods=[
    Mod.set(cycle_btn, text="State 2", on_click=cycle_state.state(3))
])
cycle_state.cState(3, mods=[
    Mod.set(cycle_btn, text="State 3", on_click=cycle_state.state(0))
])

cycle_btn.on_click = cycle_state.state(1)  # Start the cycle
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

### Integration with Exporter

The exporter (\`html_css_js.py\`) automatically detects and exports all scripts of type \`dScript\`, \`InlineScript\`, and \`FileScript\`. You can safely mix and match them in your app, and all will be included in the generated JS.

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

## Utility Scripts (\`utils_ds\`)

Dars provides a collection of utility functions in \`dars.scripts.utils_ds\` (exported in \`dars.all\`) that return pre-configured \`dScript\` objects for common tasks. These allow you to implement interactivity without writing raw JavaScript.

### Navigation

- \`goTo(href)\`: Navigate to a URL in the current tab.
- \`goToNew(href)\`: Open a URL in a new tab.
- \`reload()\`: Reload the current page.
- \`goBack()\`: Navigate back in browser history.
- \`goForward()\`: Navigate forward in browser history.

\`\`\`python
Button("Home", on_click=goTo("/"))
Button("Docs", on_click=goToNew("https://docs.dars.dev"))
\`\`\`

### DOM Manipulation

- \`show(id)\`: Show an element (display: block).
- \`hide(id)\`: Hide an element (display: none).
- \`toggle(id)\`: Toggle visibility.
- \`setText(id, text)\`: Set text content.
- \`addClass(id, class_name)\`: Add a CSS class.
- \`removeClass(id, class_name)\`: Remove a CSS class.
- \`toggleClass(id, class_name)\`: Toggle a CSS class.

\`\`\`python
Button("Show Details", on_click=show("details-panel"))
Button("Toggle Theme", on_click=toggleClass("app-root", "dark-mode"))
\`\`\`

### Timeouts

- \`setTimeout(delay, code)\`: Set a timeout to execute a script after a delay.

\`\`\`python
Button("Delayed Action", on_click=setTimeout(delay=2000, code="alert('Delayed!')"))
\`\`\`

### Modals

- \`showModal(id)\`: Show a Dars Modal component (handles hidden attribute and class).
- \`hideModal(id)\`: Hide a Dars Modal component.

\`\`\`python
Button("Open Modal", on_click=showModal("my-modal"))
\`\`\`

### Forms

- \`submitForm(form_id)\`: Submit a form.
- \`resetForm(form_id)\`: Reset a form.
- \`getValue(input_id, target_id)\`: Copy value from input to another element's text.
- \`clearInput(input_id)\`: Clear an input field.

\`\`\`python
Button("Submit", on_click=submitForm("contact-form"))
Button("Clear", on_click=clearInput("search-box"))
\`\`\`

### Storage (localStorage)

- \`saveToLocal(key, value)\`: Save string value.
- \`loadFromLocal(key, target_id)\`: Load value and set as text of target element.
- \`removeFromLocal(key)\`: Remove item.
- \`clearLocalStorage()\`: Clear all storage.

\`\`\`python
Button("Save Prefs", on_click=saveToLocal("theme", "dark"))
\`\`\`

### Clipboard

- \`copyToClipboard(text)\`: Copy text string.
- \`copyElementText(id)\`: Copy text content of an element.

\`\`\`python
Button("Copy Code", on_click=copyElementText("code-block"))
\`\`\`

### Scroll

- \`scrollTo(x, y)\`: Scroll to position.
- \`scrollToTop()\`: Smooth scroll to top.
- \`scrollToBottom()\`: Smooth scroll to bottom.
- \`scrollToElement(id)\`: Smooth scroll to specific element.

\`\`\`python
Button("Back to Top", on_click=scrollToTop())
\`\`\`

### Alerts & Focus

- \`alert(message)\`: Show browser alert.
- \`confirm(message, on_ok, on_cancel)\`: Show confirm dialog.

\`\`\`python
read_op = read_text("data.txt")
update_op = this().state(text=RawJS(dScript.ARG))

chained_script = read_op.then(update_op)
\`\`\`

The \`RawJS\` wrapper ensures that \`dScript.ARG\` is treated as a variable name (\`value\`) rather than a string literal \`"value"\`.

### State Navigation with \`state.state()\`

The \`state.state(idx)\` method allows you to navigate a component to a specific state index. This is the recommended way to trigger state transitions.

**Requirements**:
- The component must have a \`dState\` defined with the target index in its \`states\` array
- The index must be valid (0 to states.length - 1)

**Example: Toggle Button**
\`\`\`python
from dars.all import *
from dars.core.state import dState

# Create a button that toggles between two states
toggle_btn = Button("Off", id="ToggleBtn")

# Define states for the button
toggle_state = dState("toggle", component=toggle_btn, states=[0, 1])

# Configure state 1 appearance and behavior
toggle_state.cState(1, mods=[
    Mod.set(toggle_btn, 
        text="On",
        style={'background-color': 'green', 'color': 'white'},
        on_click=toggle_state.state(0)  # Return to state 0 when clicked
    )
])

# Initial click navigates to state 1
toggle_btn.on_click = toggle_state.state(1)
\`\`\`

**Example: Cycle Through States**
\`\`\`python
# Create a button that cycles through multiple states
cycle_btn = Button("State 0", id="CycleBtn")
cycle_state = dState("cycler", component=cycle_btn, states=[0, 1, 2, 3])

# Each state navigates to the next
cycle_state.cState(1, mods=[
    Mod.set(cycle_btn, text="State 1", on_click=cycle_state.state(2))
])
cycle_state.cState(2, mods=[
    Mod.set(cycle_btn, text="State 2", on_click=cycle_state.state(3))
])
cycle_state.cState(3, mods=[
    Mod.set(cycle_btn, text="State 3", on_click=cycle_state.state(0))
])

cycle_btn.on_click = cycle_state.state(1)  # Start the cycle
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

### Integration with Exporter

The exporter (\`html_css_js.py\`) automatically detects and exports all scripts of type \`dScript\`, \`InlineScript\`, and \`FileScript\`. You can safely mix and match them in your app, and all will be included in the generated JS.

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

## Utility Scripts (\`utils_ds\`)

Dars provides a collection of utility functions in \`dars.scripts.utils_ds\` (exported in \`dars.all\`) that return pre-configured \`dScript\` objects for common tasks. These allow you to implement interactivity without writing raw JavaScript.

### Navigation

- \`goTo(href)\`: Navigate to a URL in the current tab.
- \`goToNew(href)\`: Open a URL in a new tab.
- \`reload()\`: Reload the current page.
- \`goBack()\`: Navigate back in browser history.
- \`goForward()\`: Navigate forward in browser history.

\`\`\`python
Button("Home", on_click=goTo("/"))
Button("Docs", on_click=goToNew("https://docs.dars.dev"))
\`\`\`

### DOM Manipulation

- \`show(id)\`: Show an element (display: block).
- \`hide(id)\`: Hide an element (display: none).
- \`toggle(id)\`: Toggle visibility.
- \`setText(id, text)\`: Set text content.
- \`addClass(id, class_name)\`: Add a CSS class.
- \`removeClass(id, class_name)\`: Remove a CSS class.
- \`toggleClass(id, class_name)\`: Toggle a CSS class.

\`\`\`python
Button("Show Details", on_click=show("details-panel"))
Button("Toggle Theme", on_click=toggleClass("app-root", "dark-mode"))
\`\`\`

### Timeouts

- \`setTimeout(delay, code)\`: Set a timeout to execute a script after a delay.

\`\`\`python
Button("Delayed Action", on_click=setTimeout(delay=2000, code="alert('Delayed!')"))
\`\`\`

### Modals

- \`showModal(id)\`: Show a Dars Modal component (handles hidden attribute and class).
- \`hideModal(id)\`: Hide a Dars Modal component.

\`\`\`python
Button("Open Modal", on_click=showModal("my-modal"))
\`\`\`

### Forms

- \`submitForm(form_id)\`: Submit a form.
- \`resetForm(form_id)\`: Reset a form.
- \`getValue(input_id, target_id)\`: Copy value from input to another element's text.
- \`clearInput(input_id)\`: Clear an input field.

\`\`\`python
Button("Submit", on_click=submitForm("contact-form"))
Button("Clear", on_click=clearInput("search-box"))
\`\`\`

### Storage (localStorage)

- \`saveToLocal(key, value)\`: Save string value.
- \`loadFromLocal(key, target_id)\`: Load value and set as text of target element.
- \`removeFromLocal(key)\`: Remove item.
- \`clearLocalStorage()\`: Clear all storage.

\`\`\`python
Button("Save Prefs", on_click=saveToLocal("theme", "dark"))
\`\`\`

### Clipboard

- \`copyToClipboard(text)\`: Copy text string.
- \`copyElementText(id)\`: Copy text content of an element.

\`\`\`python
Button("Copy Code", on_click=copyElementText("code-block"))
\`\`\`

### Scroll

- \`scrollTo(x, y)\`: Scroll to position.
- \`scrollToTop()\`: Smooth scroll to top.
- \`scrollToBottom()\`: Smooth scroll to bottom.
- \`scrollToElement(id)\`: Smooth scroll to specific element.

\`\`\`python
Button("Back to Top", on_click=scrollToTop())
\`\`\`

### Alerts & Focus

- \`alert(message)\`: Show browser alert.
- \`confirm(message, on_ok, on_cancel)\`: Show confirm dialog.
- \`log(message)\`: Log to console.
- \`focus(id)\`: Focus an element.
- \`blur(id)\`: Blur an element.

\`\`\`python
Button("Delete", on_click=confirm(
    "Are you sure?", 
    on_ok="console.log('Deleted')", 
    on_cancel="console.log('Cancelled')"
))
\`\`\`

## Animation System

Dars includes a comprehensive animation system with 15+ built-in animations. All animation functions return \`dScript\` objects and can be chained for complex sequences.

### Basic Animations

#### fadeIn / fadeOut

\`\`\`python
from dars.all import fadeIn, fadeOut

# Fade in an element
button.on_click = fadeIn(id="box", duration=500, easing="ease")

# Fade out an element
button.on_click = fadeOut(id="box", duration=500, hide_after=True)
\`\`\`

**Parameters:**
- \`id\`: Element ID to animate
- \`duration\`: Animation duration in milliseconds (default: 500)
- \`easing\`: CSS easing function (default: "ease")
- \`hide_after\`: For fadeOut, set display:none after animation (default: True)

#### slideIn / slideOut

\`\`\`python
from dars.all import slideIn, slideOut

# Slide in from left
button.on_click = slideIn(id="panel", direction="left", duration=400)

# Slide out to right
button.on_click = slideOut(id="panel", direction="right", duration=400)
\`\`\`

**Directions:** \`"left"\`, \`"right"\`, \`"top"\`, \`"bottom"\`, \`"top-left"\`, \`"top-right"\`, \`"bottom-left"\`, \`"bottom-right"\`

#### scaleIn / scaleOut

\`\`\`python
from dars.all import scaleIn, scaleOut

# Scale in from 0.3 to 1
button.on_click = scaleIn(id="popup", from_scale=0.3, duration=400)

# Scale out to 0.5
button.on_click = scaleOut(id="popup", to_scale=0.5, duration=400)
\`\`\`

### Interactive Animations

#### shake

\`\`\`python
from dars.all import shake

# Shake effect
button.on_click = shake(id="alert", intensity=10, duration=500)
\`\`\`

**Parameters:**
- \`intensity\`: Shake distance in pixels (default: 10)
- \`duration\`: Total animation duration (default: 500)

#### bounce

\`\`\`python
from dars.all import bounce

# Bounce effect
button.on_click = bounce(id="element", distance=20, duration=600)
\`\`\`

#### pulse

\`\`\`python
from dars.all import pulse

# Pulse effect
button.on_click = pulse(id="button", scale=1.1, duration=400, iterations=2)
\`\`\`

**Parameters:**
- \`scale\`: Maximum scale factor (default: 1.1)
- \`iterations\`: Number of pulses (default: 1, use "infinite" for continuous)

#### rotate

\`\`\`python
from dars.all import rotate

# Rotate 360 degrees
button.on_click = rotate(id="spinner", degrees=360, duration=1000)
\`\`\`

#### flip

\`\`\`python
from dars.all import flip

# Flip on Y axis
button.on_click = flip(id="card", axis="y", duration=600)
\`\`\`

**Axis:** \`"x"\` (horizontal), \`"y"\` (vertical)

### Color and Size Animations

#### colorChange

\`\`\`python
from dars.all import colorChange

# Change background color
button.on_click = colorChange(
    id="box",
    property="background",
    from_color="#ff0000",
    to_color="#00ff00",
    duration=500
)
\`\`\`

**Properties:** \`"color"\`, \`"background"\`, \`"border-color"\`

#### morphSize

\`\`\`python
from dars.all import morphSize

# Morph to new size
button.on_click = morphSize(
    id="box",
    to_width="300px",
    to_height="200px",
    duration=500
)
\`\`\`

### Animation Chaining

#### sequence

Chain multiple animations to run one after another:

\`\`\`python
from dars.all import sequence, fadeIn, pulse, shake

button.on_click = sequence(
    fadeIn(id="box", duration=300),
    pulse(id="box", scale=1.2, iterations=2),
    shake(id="box", intensity=5)
)
\`\`\`

#### parallel

Run animations simultaneously (use \`.then()\` with same timing):

\`\`\`python
from dars.all import fadeIn, scaleIn

# Both animations run at the same time
button.on_click = fadeIn(id="box").then(scaleIn(id="other-box"))
\`\`\`

### Chaining with State Operations

Animations integrate seamlessly with State V2:

\`\`\`python
from dars.all import *

display = Text("0", id="counter")
counter = State(display, text=0)

button.on_click = sequence(
    counter.text.increment(by=1),
    pulse(id="counter", scale=1.2),
    fadeOut(id="counter", duration=200),
    counter.text.set(value=0),
    fadeIn(id="counter", duration=200)
)
\`\`\`

### Complete Animation Example

\`\`\`python
from dars.all import *

app = App("Animation Demo")

# Create animated box
box = Container(
    Text("Animate Me!", style={"color": "white"}),
    id="anim-box",
    style={
        "background": "linear-gradient(135deg, #667eea, #764ba2)",
        "padding": "40px",
        "border-radius": "16px",
        "text-align": "center"
    }
)

# Animation buttons
fade_btn = Button("Fade In", on_click=fadeIn(id="anim-box", duration=600))
slide_btn = Button("Slide In", on_click=slideIn(id="anim-box", direction="left"))
shake_btn = Button("Shake", on_click=shake(id="anim-box", intensity=10))
pulse_btn = Button("Pulse", on_click=pulse(id="anim-box", scale=1.15, iterations=3))

# Sequence button
sequence_btn = Button("Combo", on_click=sequence(
    fadeIn(id="anim-box", duration=400),
    pulse(id="anim-box", scale=1.1, iterations=2),
    shake(id="anim-box", intensity=5, duration=400)
))

page = Page(Container(box, fade_btn, slide_btn, shake_btn, pulse_btn, sequence_btn))
app.add_page("index", page, index=True)
\`\`\`

### Animation Best Practices

1. **Use appropriate durations**: Most animations work well between 300-600ms
   \`\`\`python
   fadeIn(id="box", duration=400)  # Good - feels responsive
   fadeIn(id="box", duration=2000)  # Too slow - users will get impatient
   \`\`\`

2. **Match animation to context**: Use subtle animations for frequent actions
   \`\`\`python
   # Frequent action - subtle
   button.on_click = pulse(id="counter", scale=1.05, duration=200)
   
   # Important action - more dramatic
   success_btn.on_click = sequence(
       scaleIn(id="message", from_scale=0.5, duration=400),
       pulse(id="message", scale=1.1, iterations=2)
   )
   \`\`\`

3. **Don't overuse sequence**: Long animation chains can frustrate users
   \`\`\`python
   # Good - 2-3 animations
   sequence(fadeIn(id="a"), pulse(id="b"))
   
   # Avoid - too many steps
   sequence(fadeIn(id="a"), slideIn(id="b"), shake(id="c"), bounce(id="d"), fadeOut(id="e"))
   \`\`\`

4. **Provide visual feedback**: Use animations to acknowledge user actions
   \`\`\`python
   submit_btn.on_click = sequence(
       pulse(id="submit-btn", scale=0.95, duration=100),  # Button press feedback
       fadeOut(id="form", duration=300),
       fadeIn(id="success-message", duration=300)
   )
   \`\`\`

### Available Animations Reference

| Function | Purpose | Key Parameters |
|----------|---------|----------------|
| \`fadeIn\` | Fade element in | \`id\`, \`duration\`, \`easing\` |
| \`fadeOut\` | Fade element out | \`id\`, \`duration\`, \`hide_after\` |
| \`slideIn\` | Slide element in | \`id\`, \`direction\`, \`distance\`, \`duration\` |
| \`slideOut\` | Slide element out | \`id\`, \`direction\`, \`distance\`, \`duration\` |
| \`scaleIn\` | Scale element in | \`id\`, \`from_scale\`, \`duration\` |
| \`scaleOut\` | Scale element out | \`id\`, \`to_scale\`, \`duration\` |
| \`shake\` | Shake effect | \`id\`, \`intensity\`, \`duration\` |
| \`bounce\` | Bounce effect | \`id\`, \`distance\`, \`duration\` |
| \`pulse\` | Pulse/heartbeat | \`id\`, \`scale\`, \`duration\`, \`iterations\` |
| \`rotate\` | Rotate element | \`id\`, \`degrees\`, \`duration\` |
| \`flip\` | Flip on axis | \`id\`, \`axis\`, \`duration\` |
| \`colorChange\` | Change color | \`id\`, \`property\`, \`from_color\`, \`to_color\` |
| \`morphSize\` | Change size | \`id\`, \`to_width\`, \`to_height\`, \`duration\` |
| \`sequence\` | Chain animations | \`*animations\` |

All animations return \`dScript\` objects and can be used with \`.then()\` for advanced chaining.
`},{type:"T9",id:"markdown_127",key:"0/2/0/16",text:`# Dars CLI Reference

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

For more, see the [Getting Started](#getting-started-with-dars) guide and the main documentation index.`}]},{type:"T2",id:"footer-section",key:"0/2/1",children:[{type:"T2",id:"container_128",key:"0/2/1/0",children:[{type:"T2",id:"container_129",key:"0/2/1/0/0",children:[{type:"T2",id:"container_130",key:"0/2/1/0/0/0",children:[{type:"T4",id:"image_131",key:"0/2/1/0/0/0/0"},{type:"T2",id:"container_132",key:"0/2/1/0/0/0/1",children:[{type:"T5",id:"text_133",key:"0/2/1/0/0/0/1/0",text:"Dars Framework"}]}]},{type:"T2",id:"container_134",key:"0/2/1/0/0/1",children:[{type:"T2",id:"container_135",key:"0/2/1/0/0/1/0",children:[{type:"T5",id:"text_136",key:"0/2/1/0/0/1/0/0",text:"Quick Links"},{type:"T6",id:"link_137",key:"0/2/1/0/0/1/0/1",text:"Documentation"},{type:"T6",id:"link_138",key:"0/2/1/0/0/1/0/2",text:"GitHub"},{type:"T6",id:"link_139",key:"0/2/1/0/0/1/0/3",text:"Examples"}]},{type:"T2",id:"container_140",key:"0/2/1/0/0/1/1",children:[{type:"T5",id:"text_141",key:"0/2/1/0/0/1/1/0",text:"Resources"},{type:"T6",id:"link_142",key:"0/2/1/0/0/1/1/1",text:"Getting Started"},{type:"T6",id:"link_143",key:"0/2/1/0/0/1/1/2",text:"Releases"}]},{type:"T2",id:"container_144",key:"0/2/1/0/0/1/2",children:[{type:"T5",id:"text_145",key:"0/2/1/0/0/1/2/0",text:"Info: "},{type:"T5",id:"text_146",key:"0/2/1/0/0/1/2/1",text:"A modern Python framework for web and desktop applications"}]}]},{type:"T2",id:"container_147",key:"0/2/1/0/0/2",children:[{type:"T2",id:"container_148",key:"0/2/1/0/0/2/0",children:[{type:"T5",id:"text_149",key:"0/2/1/0/0/2/0/0",text:"\xA9 2024 Dars Framework."}]},{type:"T2",id:"container_150",key:"0/2/1/0/0/2/1",children:[{type:"T5",id:"text_151",key:"0/2/1/0/0/2/1/0",text:"Created with "},{type:"T6",id:"link_152",key:"0/2/1/0/0/2/1/1",text:"Dars Framework"},{type:"T5",id:"text_153",key:"0/2/1/0/0/2/1/2",text:" by "},{type:"T6",id:"link_154",key:"0/2/1/0/0/2/1/3",text:"ZtaDev"}]}]}]}]}]}]}]},function(){const c=new Map;let l=null,p=null;function u(){}function S(){}function _(n,t){if(!n)return;t(n);const e=n.children||[];for(let o=0;o<e.length;o++)_(e[o],t)}function w(n,t){if(!(!n||!t))for(const[e,o]of Object.entries(t))try{o===!1||o===null||typeof o>"u"?n.removeAttribute(e):n.setAttribute(e,String(o))}catch{}}function E(n,t={},e={}){for(const o in t)if(!(o in e))try{n.removeAttribute(o)}catch{}for(const o in e){const i=e[o];try{i===!1||i===null||typeof i>"u"?n.removeAttribute(o):n.setAttribute(o,String(i))}catch{}}}function I(n,t={},e={}){for(const o in t)if(!(o in e))try{n.style.removeProperty(o.replace(/_/g,"-"))}catch{}for(const o in e){const i=e[o];try{n.style.setProperty(o.replace(/_/g,"-"),String(i))}catch{}}}function M(n,t){(t||document).addEventListener(n,function(e){let o=e.target;const i=t||document;for(;o&&o!==i;){const m=o.id;if(m&&c.has(m)){const y=c.get(m);if(o&&o.__darsEv&&o.__darsEv[n])return;let d=y[n];if(!d&&(n==="keydown"||n==="keyup"||n==="keypress")){const a=e.key||e.code;if(a){const r=n+"."+a;d=y[r]}}if(typeof d=="function"){try{d.call(o,e)}catch(a){console.error("[Dars] handler error",a)}return}}o=o.parentNode}},!0)}function k(n,t){return n&&t?n.type!==t.type:n!==t}function v(n){if(!n)return;const t=n.children||[];for(let e=0;e<t.length;e++)v(t[e]);if(n.id&&c.delete(n.id),n.id){const e=document.getElementById(n.id);if(e&&e.parentNode)try{e.parentNode.removeChild(e)}catch{}}}function x(n,t){if(!t||!t.id)return{ok:!1,reason:"missing-new"};let e=document.getElementById(t.id);if(!e){const a=n&&n.id?document.getElementById(n.id):null;if(a)try{a.id=t.id,e=a}catch{}}if(!e)return{ok:!1,reason:"missing-el"};if(k(n,t))return{ok:!1,reason:"type-changed"};const o=!!t.isIsland;if(!o&&t.class&&(e.className=t.class),o||E(e,n&&n.props||{},t.props||{}),o||I(e,n&&n.style||{},t.style||{}),!o&&Object.prototype.hasOwnProperty.call(t,"text")&&e.textContent!==String(t.text||"")&&(e.textContent=String(t.text||"")),o)return{ok:!0};const i=n&&n.children?n.children:[],m=t.children?t.children:[],y=new Map;for(let a=0;a<i.length;a++){const r=i[a]&&(i[a].id||i[a].key)||null;r&&y.set(String(r),i[a])}const d=new Set;for(let a=0;a<m.length;a++){const r=m[a],h=r&&(r.id||r.key)||null;if(!h)if(a<i.length){const s=x(i[a],r);if(!s.ok)return s;d.add(i[a]);continue}else return{ok:!1,reason:"children-added"};const b=y.get(String(h));if(b){const s=x(b,r);if(!s.ok)return s;d.add(b)}else{if(a<i.length){const f=i[a];if(!k(f,r)){const g=x(f,r);if(!g.ok)return g;d.add(f);continue}}const s=createSubtree(r);if(s){const f=a<i.length?i[a]:null;if(f&&f.id){const g=document.getElementById(f.id);g&&g.parentNode?g.parentNode.insertBefore(s,g):e.appendChild(s)}else e.appendChild(s);continue}return{ok:!1,reason:"children-added"}}}for(let a=0;a<i.length;a++){const r=i[a];d.has(r)||v(r)}return{ok:!0}}function L(n){typeof requestAnimationFrame=="function"?requestAnimationFrame(n):setTimeout(n,16)}function O(n){const t=l;if(!t){l=n;try{window.__DARS_VDOM__=n}catch{}return}L(()=>{const e=x(t,n);if(!e.ok){console.warn("[Dars] Structural change detected (",e.reason,"), reloading...");try{location.reload()}catch{}return}l=n;try{window.__DARS_VDOM__=n}catch{}})}function F(n){l=n;try{window.__DARS_VDOM__=n}catch{}["click","dblclick","mousedown","mouseup","mouseenter","mouseleave","mousemove","keydown","keyup","keypress","change","input","submit","focus","blur"].forEach(e=>M(e,document))}function R(){try{if(window.__DARS_HOTRELOAD_DISABLED__)return()=>{}}catch{}const n=window.__DARS_VERSION_URL||"version.txt";let t=null,e=!1,o=0;const i=10;let m=!1;function y(a,r,h,b){try{const s=new XMLHttpRequest;b&&(s.responseType=b),s.open("GET",a,!0),s.timeout=5e3,s.onreadystatechange=function(){s.readyState===4&&(s.status>=200&&s.status<300?r(s.response):h())},s.onerror=h,s.ontimeout=h,s.setRequestHeader("Cache-Control","no-store"),s.send()}catch{h()}}function d(){m||y(n,function(a){let r=(a||"").toString().trim();if(!r||r==="0"){if(o+=1,o>=i){console.warn("[Dars] version file not found after",i,"attempts. Hot reload disabled for this session."),m=!0;try{window.__DARS_HOTRELOAD_DISABLED__=!0,window.__DARS_STOP_HOTRELOAD=null}catch{}if(t)try{clearTimeout(t)}catch{}return}e||(console.warn("[Dars] waiting for version file..."),e=!0),t=setTimeout(d,600);return}if(o=0,e=!1,p||(p=r),r&&r!==p){p=r;try{location.reload()}catch{}return}t=setTimeout(d,600)},function(){if(o+=1,o>=i){console.warn("[Dars] version file not reachable after",i,"attempts. Hot reload disabled for this session."),m=!0;try{window.__DARS_HOTRELOAD_DISABLED__=!0,window.__DARS_STOP_HOTRELOAD=null}catch{}if(t)try{clearTimeout(t)}catch{}return}e||(console.warn("[Dars] waiting for version file..."),e=!0),t=setTimeout(d,600)},"text")}return d(),()=>{try{m=!0,t&&clearTimeout(t),window.__DARS_STOP_HOTRELOAD=null}catch{}}}document.addEventListener("DOMContentLoaded",function(){if(window.__DARS_VDOM__?F(window.__DARS_VDOM__):console.warn("[Dars] No VDOM snapshot found for hydration"),window.__DARS_VERSION_URL&&window.__DARS_SNAPSHOT_URL){try{typeof window.__DARS_STOP_HOTRELOAD=="function"&&window.__DARS_STOP_HOTRELOAD()}catch{}try{window.__DARS_STOP_HOTRELOAD=R()}catch{}}})}(),window.addEventListener("scroll",()=>{const c=document.getElementById("dars-navbar");window.scrollY>20?c.classList.add("scrolled"):c.classList.remove("scrolled");const l=document.getElementById("features-section");if(l&&!l.classList.contains("visible")){const p=l.getBoundingClientRect().top,u=window.innerHeight/1.5;p<u&&(l.classList.add("visible"),document.querySelectorAll('[id^="feature-card-"]').forEach((_,w)=>{setTimeout(()=>{_.style.opacity="1",_.style.transform="translateY(0)"},w*100)}))}});const T=document.getElementById("hero-logo"),C=document.getElementById("hero-title"),D=document.getElementById("hero-description"),P=document.getElementById("pip-command"),A=document.getElementById("get-started-btn"),B=document.getElementById("scroll-text");T&&setTimeout(()=>T.classList.add("show"),5),C&&setTimeout(()=>C.classList.add("show"),350),D&&setTimeout(()=>D.classList.add("show"),650),P&&setTimeout(()=>P.classList.add("show"),950),A&&setTimeout(()=>A.classList.add("show"),1250),B&&setTimeout(()=>B.classList.add("show"),1500),document.addEventListener("DOMContentLoaded",function(){const c=document.getElementById("hamburger-btn"),l=document.getElementById("mobile-menu"),p=document.body;c&&l&&(c.addEventListener("click",function(u){u.stopPropagation(),l.style.display==="flex"?(l.style.display="none",c.classList.remove("menu-open"),p.classList.remove("menu-open")):(l.style.display="flex",c.classList.add("menu-open"),p.classList.add("menu-open"))}),l.querySelectorAll("a").forEach(u=>{u.addEventListener("click",function(){l.style.display="none",c.classList.remove("menu-open"),p.classList.remove("menu-open")})}),document.addEventListener("click",function(u){!c.contains(u.target)&&!l.contains(u.target)&&(l.style.display="none",c.classList.remove("menu-open"),p.classList.remove("menu-open"))}),document.addEventListener("keydown",function(u){u.key==="Escape"&&l.style.display==="flex"&&(l.style.display="none",c.classList.remove("menu-open"),p.classList.remove("menu-open"))}))});
