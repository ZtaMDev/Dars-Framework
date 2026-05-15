<h1 align="center">Dars Framework</h1>
 
<p align="center">
  <img src="https://raw.githubusercontent.com/ZtaMDev/Dars-Framework/CrystalMain/Dars-logo.png" alt="Dars Framework Logo" width="200" />
</p>

<p align="center">
  <img src="https://img.shields.io/pypi/v/dars-framework?color=brightgreen" alt="PyPI Version" />
  <img src="https://img.shields.io/pypi/pyversions/dars-framework?color=blue" alt="Python Versions" />
  <img src="https://img.shields.io/github/license/ZtaMDev/Dars-Framework" alt="License" />
  <a href="https://deepwiki.com/ZtaMDev/Dars-Framework"><img src="https://deepwiki.com/badge.svg" alt="Ask DeepWiki"></a>
</p>

<p align="center">
  <em>Dars is a Full-Stack multiplatform Python UI framework for building modern, interactive web and desktop apps with Python code. Seamlessly integrated with FastAPI, it allows you to build complete applications with Server-Side Rendering (SSR) and reactive SPA capabilities also classic multipage html and desktop apps in a single codebase.</em>

</p>

<div align="center">

Official [Website](https://ztamdev.github.io/Dars-Framework/) |
Documentation [Docs](https://ztamdev.github.io/Dars-Framework/docs.html) |
Official [Roadmap](https://ztamdev.github.io/Dars-Framework/roadmap.html) |
Extension for VSCode [here](https://marketplace.visualstudio.com/items?itemName=ZtaMDev.dars-framework) and OpenVSX version [here](https://open-vsx.org/extension/ztamdev/dars-framework)

</div>

```bash
pip install dars-framework
```

Try dars without installing nothing just visit the [Dars Playground](https://dars-playground.vercel.app/)

## How It Works

- Build your UI using Python classes and components (like Text, Button, Container, Page, etc).
- Preview instantly with hot-reload using `app.rTimeCompile()`.
- Export your app to static/dynamic/ssr web files with a single CLI command.
- Export to native desktop apps (BETA) using project config `format: "desktop"` and `dars build`.
- Use multipage, layouts, scripts, and more—see docs for advanced features.
- For more information visit the [Documentation](https://ztamdev.github.io/Dars-Framework/docs.html)

## Quick Example: Your First App

```python
from dars.all import *

app = App(title="Hello World", theme="dark")

# 1. Define State
state = State("app", title_val="Simple Counter", count=0)

# 2. Define Route
@route("/")
def index():
    return Page(
        # 3. Use useValue for app text
        Text(
            text=useValue("app.title_val"),
            style="fs-[33px] text-black font-bold mb-[5x] ",
        ),

        # 4. Display reactive count
        Text(
            text=useDynamic("app.count"),
            style="fs-[48px] mt-5 mb-[12px]"
        ),
        # 5. Interactive Button
        Button(
            text="+1",
            on_click=(
                state.count.increment(1)
            ),
            style="bg-[#3498db] text-white p-[15px] px-[30px] rounded-[8px] border-none cursor-pointer fs-[18px]",
        ),

        # 6. Interactive Button
        Button(
            text="-1",
            on_click=(
                state.count.decrement(1)
            ),
            style="bg-[#3498db] text-white p-[15px] px-[30px] rounded-[8px] border-none cursor-pointer fs-[18px] mt-[5px]",
        ),
        # 7. Interactive Button
        Button(
            text="Reset",
            on_click=(
                state.reset()
            ),
            style="bg-[#3498db] text-white p-[15px] px-[30px] rounded-[8px] border-none cursor-pointer fs-[18px] mt-[5px]",
        ),
        style="flex flex-col items-center justify-center h-[100vh] ffam-[Arial] bg-[#f0f2f5]",

    )

# 8. Add page
app.add_page("index", index(), title="index")

# 9. Run app with preview
if __name__ == "__main__":
    app.rTimeCompile()
```

---

## State Management System

Dars Framework features **powerful state management system**, designed for different use cases.

### State V2

Modern, Pythonic state management for reactive updates. Best for counters, timers, and component interactions using hooks.

**Hooks System:**

- `useDynamic()`: Reactive state binding for automatic UI updates.
- `useValue()`: Set initial values from state (non-reactive).
- `useWatch()`: Monitor state changes and trigger side effects.

[Learn more about Hooks](https://ztamdev.github.io/Dars-Framework/docs.html#hooks-system)

```python
from dars.all import *

app = App("State Demo")
state = State("counter", count=0)

@route("/")
def index():
    return Page(
        # Bind to state with useDynamic
        Text(text=useDynamic("counter.count"), style={"font-size": "24px"}),

        # Update state on click
        Button("Increment", on_click=state.count.increment(1)),
        Button("Decrement", on_click=state.count.decrement(1)),
        Button("Reset", on_click=state.count.set(0))
    )

app.add_page("index", index())

if __name__ == "__main__":
    app.rTimeCompile()
```

**String ID Support:** `State()` can accept a string ID (e.g., `State("my-state", ...)`).

> [!WARNING]
> **Important:** When using hooks, the State ID is used for binding. **Do not use an ID that belongs to another unrelated component**, as hooks use this ID as the State ID. Using a conflicting ID may cause unexpected behavior or state collisions.

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

## Routing System (SPA & SSR)

Dars Framework offers a flexible routing system that supports both Client-Side Routing (SPA) and Server-Side Rendering (SSR).

### Server-Side Rendering (SSR)

Render pages on the server for faster initial loads using dars backend integration with fastapi. Use the `route_type` parameter:

```python
from dars.all import *

# Rendered on the server before being sent to the client
@route("/dashboard", route_type=RouteType.SSR)
def dashboard():
    return Page(
        Text("Server-Side Rendered Page"),
        Text(f"Hello from dashboard"),
        # Client-side reactivity still works after hydration!
        Button("Click Me", on_click=alert("Hello from Client"))
    )
```

More information about SSR can be found in the [SSR/SPA Routing Guide](https://ztamdev.github.io/Dars-Framework/docs.html#server-side-rendering-in-dars-framework).

### Client-Side Routing (SPA)

Default routing behaves as a standard Single Page Application (SPA), handling navigation instantly in the browser without reloading.

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

### Key Features

1.  **Automatic Property Injection**: The framework automatically injects the correct HTML attributes for `{id}`, `{class_name}`, and `{style}`.
2.  **State V2 Compatible**: Function components work seamlessly with `State()` and reactive updates.
3.  **Event Handling**: Events like `on_click` are handled automatically by the framework (passed via `**props`).
4.  **Children Support**: Use `{Props.children}` or `{children}` to render nested content.

---

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

- **`get(id, url, **options)`\*\* - GET request
- **`post(id, url, body, **options)`\*\* - POST request
- **`put(id, url, body, **options)`\*\* - PUT request
- **`delete(id, url, **options)`\*\* - DELETE request

For complete documentation, see the [Backend API Guide](https://ztamdev.github.io/Dars-Framework/docs.html#backend-http-utilities).

---

## CLI Usage

| Command                               | What it does                                                      |
| ------------------------------------- | ----------------------------------------------------------------- |
| `dars export my_app.py --format html` | Export app to HTML/CSS/JS in `./my_app_web`                       |
| `dars init --type desktop`            | Scaffold desktop-capable project (BETA)                           |
| `dars init --type ssr`                | Scaffold full-stack SSR project (SSR + API)                       |
| `dars build` (desktop config)         | Build desktop app artifacts (BETA)                                |
| `dars preview ./my_app_web`           | Preview exported app locally                                      |
| `dars init my_project`                | Create a new Dars project (also creates dars.config.json)         |
| `dars init --update`                  | Create/Update dars.config.json in current dir                     |
| `dars build`                          | Build using dars.config.json (entry/outdir/format)                |
| `dars config validate`                | Validate dars.config.json and print report                        |
| `dars info my_app.py`                 | Show info about your app                                          |
| `dars formats`                        | List supported export formats                                     |
| `dars dev`                            | Run the configured entry file with hot preview (app.rTimeCompile) |
| `dars dev --port 9000`                | Run dev server on a custom port (overrides config)                |
| `dars dev --backend`                  | Run only the configured backendEntry (FastAPI/SSR backend)        |
| `dars --help`                         | Show help and all CLI options                                     |

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

This will start a local server at the port specified in your `dars.config.json` (defaults to http://localhost:8000) so you can view your app in the browser—no manual export needed. You can override the port with:

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
  "viteMinify": true,
  "utility_styles": {},
  "markdownHighlight": true,
  "markdownHighlightTheme": "auto",
  "port": 8000,
  "backendEntry": "backend.api:app"
}
```

- `entry`: Python entry file. Used by `dars build` and `dars export config`.
- `format`: Export format. Currently `html` and `desktop` are supported.
- `outdir`: Output directory. Used by `dars build` and default for `dars export` when not overridden.
- `publicDir`: Folder (e.g., `public/` or `assets/`) copied into the output. If null, it is autodetected.
- `include`/`exclude`: Basic filters for copying from `publicDir`.
- `bundle`: Reserved for future use. CLI exports and build already bundle appropriately.
- `defaultMinify`: Toggle the built-in Python minifier (safe, conservatively preserves `<pre>`, `<code>`, `script`, `style`, `textarea`). Controls HTML minification and provides JS/CSS fallback when advanced tools are unavailable. Default `true`.
- `viteMinify`: Toggle the Vite/esbuild minifier for JS/CSS. Default `true`.
- `utility_styles`: Dictionary defining custom utility classes. Keys are class names, values are lists of utility strings or raw CSS properties.
- `markdownHighlight`: Auto-inject a client-side syntax highlighter for fenced code blocks in Markdown. Default `true`.
- `backendEntry`: Python import path for your SSR/backend app (e.g. `"backend.api:app"`). Required when your app uses `RouteType.SSR` routes. Used by `dars dev --backend`.
- `port`: The port for the development preview server. Default `8000`.

Validate your config:

```bash
dars config validate
```

Build using config:

```bash
dars build
```

---

See LandingPage docs for details.
