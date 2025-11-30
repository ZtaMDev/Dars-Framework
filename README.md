<h1 align="center">Dars Framework</h1>
 
<p align="center">
  <img src="https://raw.githubusercontent.com/ZtaMDev/Dars-Framework/CrystalMain/Dars-logo.png" alt="Dars Framework Logo" width="200" />
</p>

<p align="center">
  <em>Dars is a multiplatform Python UI framework for building modern, interactive web and desktop apps with Python code. Write your interface in Python, export it to web technologies and deploy anywhere.</em>
</p>

<div align="center">

Official [Website](https://ztamdev.github.io/Dars-Framework/) | 
Documentation [Docs](https://ztamdev.github.io/Dars-Framework/docs.html) | 
DeepWiki [here](https://deepwiki.com/ZtaMDev/Dars-Framework) |

</div>


```bash
pip install dars-framework
```

Try dars without installing nothing(single page mode) just visit the [Dars Playground](https://dars-playground.vercel.app/)

## How It Works
- Build your UI using Python classes and components (like Text, Button, Container, Page, etc).
- Preview instantly with hot-reload using `app.rTimeCompile()`.
- Export your app to static web files with a single CLI command.
- Export to native desktop apps (BETA) using project config `format: "desktop"` and `dars build`.
- Use multipage, layouts, scripts, and more—see docs for advanced features.
- For more information visit the [Documentation](https://ztamdev.github.io/Dars-Framework/docs.html)

## Quick Example: Your First App
```python
from dars.all import *

app = App(title="Hello World", theme="dark")

index = Page(
     Text(
        text="Hello World",
        style={
            'font-size': '48px',
            'color': '#2c3e50',
            'margin-bottom': '20px',
            'font-weight': 'bold',
            'text-align': 'center'
        }
    ),
    Text(
        text="Hello World",
        style={
            'font-size': '20px',
            'color': '#7f8c8d',
            'margin-bottom': '40px',
            'text-align': 'center'
        }
    ),

    Button(
        text="Click Me!",
        on_click= alert('Hello from DARS!'),
        style={
            'background-color': '#3498db',
            'color': 'white',
            'padding': '15px 30px',
            'border': 'none',
            'border-radius': '8px',
            'font-size': '18px',
            'cursor': 'pointer',
            'transition': 'background-color 0.3s'
        }
    ),
    style={
        'display': 'flex',
        'flex-direction': 'column',
        'align-items': 'center',
        'justify-content': 'center',
        'min-height': '100vh',
        'background-color': '#f0f2f5',
        'font-family': 'Arial, sans-serif'
    }
) 

app.add_page("index", index, title="Hello World", index=True)

if __name__ == "__main__":
    app.rTimeCompile()
```

---

### Key Features

1.  **Automatic Property Injection**: The framework automatically injects the correct HTML attributes for `{id}`, `{class_name}`, and `{style}`.
2.  **State V2 Compatible**: Function components work seamlessly with `State()` and reactive updates.
3.  **Event Handling**: Events like `on_click` are handled automatically by the framework (passed via `**props`).
4.  **Children Support**: Use `{Props.children}` or `{children}` to render nested content.

## Backend HTTP Utilities & API Communication

Dars provides a system for HTTP requests and API communication without writing JavaScript. Use `useData()` for clean data binding:

```python
from dars.all import *
from dars.backend import get, useData

# Create components
user_display = Text("", id="user-name")
user_state = State(user_display, text="")

# Fetch and bind data - pure Python!
fetch_btn = Button(
    "Fetch User",
    on_click=get(
        id="userData",
        url="https://api.example.com/users/1",
        # Access nested data with dot notation
        callback=user_state.text.set(useData('userData').name)
    )
)
```

### Chain Multiple Updates

Use `.then()` to chain state updates sequentially:

```python
# Update multiple components from API response
callback=(
    name_state.text.set(useData('userData').name)
    .then(email_state.text.set(useData('userData').email))
    .then(website_state.text.set(useData('userData').website))
)
```

### Available HTTP Methods

- **`get(id, url, **options)`** - GET request
- **`post(id, url, body, **options)`** - POST request  
- **`put(id, url, body, **options)`** - PUT request
- **`delete(id, url, **options)`** - DELETE request

For complete documentation, see the [Backend API Guide](https://ztamdev.github.io/Dars-Framework/docs.html#backend-http-utilities).

---


## State Management System

Dars Framework features **two powerful state management systems**, each designed for different use cases:

### 1. State V2 (Dynamic)
Modern, Pythonic state management for simple reactive updates. Best for counters, timers, and single-component interactions.

```python
from dars.all import *

# Create state with component
counter = State(Text("0", id="counter"), text=0)

# Or use string ID for dynamic components
dynamic_state = State("dynamic-counter", text=0)

# Reactive operations
inc_btn = Button("+1", on_click=counter.text.increment(by=1))
set_btn = Button("Reset", on_click=counter.reset())

# Auto-increment
start_btn = Button("Start", on_click=counter.text.auto_increment(by=1, interval=1000))
```

**String ID Support:** State() can accept either a component object or a string ID, perfect for components created dynamically with `createComp()`.


### 2. dState & cState (Indexed)
Powerful indexed state system for complex state machines, multi-step workflows, and cross-component coordination.

```python
from dars.core.state import dState, Mod

# Define state with indices [0, 1, 2]
toggle = dState("toggle", component=btn, states=[0, 1, 2])

# Define rules for state 1
toggle.cState(1, mods=[
    Mod.set(btn, text="Active", style={'background': 'green'}),
    Mod.set(status_text, text="System Online")
])

# Navigate by index
btn.on_click = toggle.state(1)
```

### Comparison

| Feature | State V2 (Dynamic) | dState/cState (Indexed) |
|---------|-------------------|-------------------------|
| **Best For** | Simple updates, counters, timers | Complex workflows, state machines |
| **API Style** | Clean, Pythonic | Explicit, Indexed |
| **State Tracking** | Dynamic values | Fixed Indices (0, 1, 2...) |
| **Auto Ops** | Built-in (`auto_increment`) | Manual via Mod |
| **Cross-State** | No | `Mod.call()` supported |
| **Dynamic Components** | String ID support | Component required |

For detailed documentation, visit the [State Management Guide](https://ztamdev.github.io/Dars-Framework/docs.html#state-management-in-dars).

---

## Animation System

Dars includes **15+ built-in animations** that work seamlessly with state management:

```python
from dars.all import fadeIn, fadeOut, pulse, shake, sequence

# Single animation
button.on_click = fadeIn(id="modal", duration=500)

# Chain multiple animations
button.on_click = sequence(
    fadeIn(id="box"),
    pulse(id="box", scale=1.2, iterations=2),
    shake(id="box", intensity=5)
)

# Combine with state updates
button.on_click = sequence(
    counter.text.increment(by=1),
    pulse(id="counter", scale=1.2)
)
```

**Available Animations:**
- **Opacity:** `fadeIn`, `fadeOut`
- **Movement:** `slideIn`, `slideOut` (up, down, left, right)
- **Scaling:** `scaleIn`, `scaleOut`, `pulse`
- **Interactive:** `shake`, `bounce`, `rotate`, `flip`
- **Effects:** `colorChange`, `morphSize`

For complete animation documentation, visit the [Animation Guide](https://ztamdev.github.io/Dars-Framework/docs.html#dars-animation-system).

---

### Dynamic Updates with `this()`

Update components directly without pre-defining states:

```python
from dars.all import *

# Self-updating button
btn = Button("Click Me!", on_click=this().state(
    text="Clicked!",
    style={"background-color": "green"}
))
```

### Script Chaining with `.then()`

Chain asynchronous operations using `.then()` or `sequence()`:

```python
from dars.all import *

# Chain animation + state update
button.on_click = sequence(
    fadeOut(id="status"),
    state.text.set(value="Loading...")
).then(
    fadeIn(id="status")
)
```

---


## SPA Routing System

Dars 1.4.6 introduces a powerful client-side routing system for Single Page Applications:

### Basic Routing

Use the `@route` decorator or `route` parameter to create SPA routes:

```python
from dars.all import *

app = App(title="My SPA")

# Using decorator
@route("/")
def home():
    return Page(Text("Home Page"))

# Using parameter
about_page = Page(Text("About Us"))
app.add_page("about", about_page, route="/about")

app.add_page("home", home())
```

### Nested Routes with Outlet

Create complex layouts with parent-child routes using the `Outlet` component:

```python
# Parent layout with navigation
@route("/dashboard")
def dashboard():
    return Page(
        Text("Dashboard", style={"fontSize": "24px"}),
        Container(
            Link("Settings", href="/dashboard/settings"),
            Link("Profile", href="/dashboard/profile"),
            id="nav",
            
        ),
        Outlet(),  # Child routes render here
        style={"padding": "20px"}
    )

# Child routes
settings_page = Page(Text("Settings Content"))
profile_page = Page(Text("Profile Content"))

# NOTE if you don't assign index=True to one of the pages when using more than 1 page with SPA route system
# you get a 404 error because the router doesn't knwow the index page and cannot assign it as index.
# this is probably going to be fixed in next updates
app.add_page("dashboard", dashboard(), index=True)
app.add_page("settings", settings_page, route="/dashboard/settings", parent="dashboard")
app.add_page("profile", profile_page, route="/dashboard/profile", parent="dashboard")
```

### 404 Error Handling

Dars automatically handles 404 errors with a default page, or you can customize it:

```python
# Custom 404 page
custom_404 = Page(
    Text("Oops! Page not found", style={"fontSize": "32px", "color": "red"}),
    Link("Go Home", href="/")
)

app.set_404_page(custom_404)
```

### Hot Reload for SPAs

The development preview server includes intelligent hot reload:
- Detects changes and reloads automatically
- Stops polling after 10 errors to prevent browser lag
- Clean console output without spam

## Custom Components

Dars provides Custom Components as the modern way to create simple UI DOM elements directly from python.

### Function Components

Function Components are the modern way to create reusable UI elements. They use simple functions with f-string templates and automatically handle framework features like IDs, styling, and events.

#### Basic Syntax

Use the `@FunctionComponent` decorator. You can access framework properties (`id`, `class_name`, `style`, `children`) using the `Props` helper object or by declaring them as arguments.

#### Option 1: Using `Props` Object (Cleanest)

```python
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
```

#### Option 2: Explicit Arguments

```python
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
```

### Example with State and Events

```python
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
```

---

## CLI Usage

| Command                                 | What it does                               |
|-----------------------------------------|--------------------------------------------|
| `dars export my_app.py --format html`   | Export app to HTML/CSS/JS in `./my_app_web` |
| `dars init --type desktop`               | Scaffold desktop-capable project (BETA)     |
| `dars build` (desktop config)            | Build desktop app artifacts (BETA)          |
| `dars preview ./my_app_web`             | Preview exported app locally                |
| `dars init my_project`                  | Create a new Dars project (also creates dars.config.json) |
| `dars init --update`                    | Create/Update dars.config.json in current dir |
| `dars build`                            | Build using dars.config.json (entry/outdir/format) |
| `dars config validate`                  | Validate dars.config.json and print report   |
| `dars info my_app.py`                   | Show info about your app                    |
| `dars formats`                          | List supported export formats               |
| `dars --help`                           | Show help and all CLI options               |

Tip: use `dars doctor` to review optional tooling that can enhance bundling/minification.

### Desktop Export (BETA)

- Mark your project for desktop in `dars.config.json` with `"format": "desktop"`.
- Initialize backend scaffolding with `dars init --type desktop` (or `--update`).
- Build with `dars build` to produce desktop artifacts under `dist/`.
- This feature is in BETA: usable for testing, not yet recommended for production.

---

- Visit dars [official website](https://ztamdev.github.io/Dars-Framework/)
- Visit the dars official [Documentation](https://ztamdev.github.io/Dars-Framework/docs.html) now on separate website.
- Try dars without installing nothing just visit the [Dars Playground](https://dars-playground.vercel.app/)

## Local Execution and Live Preview

To test your app locally before exporting, use the hot-reload preview from any Python file that defines your app:

```python
if __name__ == "__main__":
    app.rTimeCompile()
```

Then run your file directly:

```bash
python my_app.py
```

This will start a local server at http://localhost:8000 so you can view your app in the browser—no manual export needed. You can change the port with:

```bash
python my_app.py --port 8088
```

---

You can also use the CLI preview command on an exported app:

```bash
dars preview ./my_exported_app
```

This will start a local server at http://localhost:8000 to view your exported app in the browser.

---

## Project Configuration (dars.config.json)

Dars can read build/export settings from a `dars.config.json` at your project root. It is created automatically by `dars init`, and you can add it to existing projects with `dars init --update`.

Example default:

```json
{
  "entry": "main.py",
  "format": "html",
  "outdir": "dist",
  "publicDir": null,
  "include": [],
  "exclude": ["**/__pycache__", ".git", ".venv", "node_modules"],
  "bundle": true,
  "defaultMinify": true,
  "viteMinify": true
}
```

- `entry`: Python entry file. Used by `dars build` and `dars export config`.
- `format`: Export format. Currently only `html` is supported.
- `outdir`: Output directory. Used by `dars build` and default for `dars export` when not overridden.
- `publicDir`: Folder (e.g., `public/` or `assets/`) copied into the output. If null, it is autodetected.
- `include`/`exclude`: Basic filters for copying from `publicDir`.
- `bundle`: Reserved for future use. CLI exports and build already bundle appropriately.
- `defaultMinify`: Toggle the built-in Python minifier (safe, conservatively preserves `<pre>`, `<code>`, `script`, `style`, `textarea`). Controls HTML minification and provides JS/CSS fallback when advanced tools are unavailable. Default `true`.
- `viteMinify`: Toggle the Vite/esbuild minifier for JS/CSS. Default `true`.

Validate your config:

```bash
dars config validate
```

Build using config:

```bash
dars build
```

Export using the config entry and outdir:

```bash
dars export config --format html
```

---

See LandingPage docs for details: state_management.md, events.md, scripts.md, routing.md.
