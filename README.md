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
  <em>Dars is a Full-Stack Python UI framework for building modern, interactive web applications entirely in Python. Seamlessly integrated with FastAPI, it lets you build complete applications with Server-Side Rendering (SSR), reactive SPA routing, static site generation, and a production-ready backend API — all from a single Python codebase, with zero JavaScript required.</em>
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

Try Dars without installing anything — visit the [Dars Playground](https://dars-playground.vercel.app/)

---

## How It Works

- Build your UI using Python classes and components (`Text`, `Button`, `Container`, `Page`, `Each`, `Show`, `If`, etc.).
- Preview instantly with hot-reload using `app.rTimeCompile()`.
- Export your app to static/dynamic/SSR web files with a single CLI command.
- Use multipage layouts, scripts, hooks, and more — see docs for advanced features.
- **One app, four deployment targets simultaneously:** Dars supports Static Site Generation (SSG), Single-Page Application (SPA) routing, Server-Side Rendering (SSR) with FastAPI, and a full Backend API — all from the same Python codebase. Mix and match freely: export some pages as static HTML for SEO, serve others via SSR for dynamic content, and expose REST API endpoints alongside your UI.
- **Full backend toolkit included:** `useFetch` for declarative data fetching, `FormValidator` for client-side validation, `Each` for runtime list rendering from API responses, `JsonStore` for file-backed persistence, `UploadPipeline` for secure file uploads, `SecurityHeadersMiddleware` for HTTP security, and `DarsEnv` for `.env` file support.
- For more information visit the [Documentation](https://ztamdev.github.io/Dars-Framework/docs.html)

---

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
        Text(
            text=useValue("app.title_val"),
            style="fs-[33px] text-black font-bold mb-[5px]",
        ),
        Text(
            text=useDynamic("app.count"),
            style="fs-[48px] mt-5 mb-[12px]"
        ),
        Button(
            text="+1",
            on_click=state.count.increment(1),
            style="bg-[#3498db] text-white p-[15px] px-[30px] rounded-[8px] cursor-pointer fs-[18px]",
        ),
        Button(
            text="-1",
            on_click=state.count.decrement(1),
            style="bg-[#3498db] text-white p-[15px] px-[30px] rounded-[8px] cursor-pointer fs-[18px] mt-[5px]",
        ),
        Button(
            text="Reset",
            on_click=state.reset(),
            style="bg-[#3498db] text-white p-[15px] px-[30px] rounded-[8px] cursor-pointer fs-[18px] mt-[5px]",
        ),
        style="flex flex-col items-center justify-center h-[100vh] ffam-[Arial] bg-[#f0f2f5]",
    )

app.add_page("index", index(), title="index")

if __name__ == "__main__":
    app.rTimeCompile()
```

---

## State Management System

Dars features a **powerful state management system** designed for different use cases.

### Hook-Based State Management

Modern, Pythonic state management for reactive updates. Best for counters, timers, and component interactions.

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
        Text(text=useDynamic("counter.count"), style="fs-[24px]"),
        Button("Increment", on_click=state.count.increment(1)),
        Button("Decrement", on_click=state.count.decrement(1)),
        Button("Reset",     on_click=state.count.set(0)),
    )

app.add_page("index", index())

if __name__ == "__main__":
    app.rTimeCompile()
```

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
```

**Available Animations:** `fadeIn`, `fadeOut`, `slideIn`, `slideOut`, `scaleIn`, `scaleOut`, `pulse`, `shake`, `bounce`, `rotate`, `flip`, `colorChange`, `morphSize`, `popIn`, `popOut`

For complete animation documentation, visit the [Animation Guide](https://ztamdev.github.io/Dars-Framework/docs.html#dars-animation-system).

---

## Routing System (SPA & SSR)

Dars offers a flexible routing system supporting Client-Side Routing (SPA), Server-Side Rendering (SSR), and Static Site Generation — all in one app.

### Server-Side Rendering (SSR)

```python
from dars.all import *

@route("/dashboard", route_type=RouteType.SSR)
def dashboard():
    return Page(
        Text("Server-Side Rendered Page"),
        Button("Click Me", on_click=alert("Hello from Client")),
    )
```

### Client-Side Routing (SPA)

```python
@route("/")
def home():
    return Page(Text("Home Page"))

@route("/about")
def about():
    return Page(Text("About Us"))
```

### Nested Routes with Outlet

```python
@route("/dashboard")
def dashboard():
    return Page(
        Text("Dashboard", style="fs-[24px]"),
        Container(
            Link("Settings", href="/dashboard/settings"),
            Link("Profile",  href="/dashboard/profile"),
        ),
        Outlet(),
    )

app.add_page("dashboard", dashboard(), index=True)
app.add_page("settings", settings_page, route="/dashboard/settings", parent="dashboard")
app.add_page("profile",  profile_page,  route="/dashboard/profile",  parent="dashboard")
```

### 404 Error Handling

```python
app.set_404_page(Page(
    Text("Page not found", style="fs-[32px] text-red-500"),
    Link("Go Home", href="/"),
))
```

---

## Custom Components

### Function Components

```python
from dars.all import *

@FunctionComponent
def UserCard(name, email, **props):
    return f"""
    <div {Props.id} {Props.class_name} {Props.style}>
        <h3>{name}</h3>
        <p>{email}</p>
        <div class="card-body">{Props.children}</div>
    </div>
    """

card = UserCard("John Doe", "john@example.com", id="user-1", style="p-[20px]")
```

---

## Control Flow Components

### `Show` — Runtime Visibility Toggle

Always renders children into the DOM. A falsy VRef condition hides the wrapper with `display:none`. Reacts to VRef changes at runtime — perfect for loading spinners, error banners, and any UI that toggles based on live state.

```python
from dars.all import *

is_loading = setVRef(True,  ".loading")
has_error  = setVRef(False, ".error")

Show(
    is_loading,
    Container(Spinner(), Text("Loading…"), style="flex items-center gap-2"),
)

Show(
    has_error,
    Container(
        Text("Something went wrong.", style="text-red-600"),
        style="bg-red-50 border rounded p-3",
    ),
)
```

### `Each` — List Rendering from Python or API

Renders a list using a template function. Works with both compile-time Python lists and runtime VRef arrays (e.g. from `useFetch`).

**Compile-time list:**

```python
users = [{"name": "Alice"}, {"name": "Bob"}]

Each(items=users, render=lambda u: Text(u["name"]))
```

**Runtime VRef list (from API):**

The render function is called at export time with a sentinel dict containing `__item_<field>__` placeholders. At runtime, `dom_each_render` substitutes real values for each item. Use `__item_done_class__` to get `"line-through text-gray-400"` for done items automatically.

```python
tasks_vref = setVRef([], ".tasks-data")  # filled by useFetch

def task_item(t):
    title   = t.get("title", "__item_title__") if isinstance(t, dict) else "__item_title__"
    item_id = t.get("id",    "__item_id__")    if isinstance(t, dict) else "__item_id__"
    return Container(
        Text(title,         style="flex: 1 1 0%", class_name="__item_done_class__"),
        Text(f"#{item_id}", style="text-xs text-gray-400 ml-2"),
        style="flex items-center gap-2 p-2 border rounded bg-white shadow-sm",
    )

Each(items=tasks_vref, render=task_item, class_name="space-y-1 mb-6")
```

Supported API response shapes are automatically unwrapped: `{"tasks":[...]}`, `{"items":[...]}`, `{"data":[...]}`, `{"results":[...]}`, or a plain `[...]` array.

---

## Backend & API Communication

Dars ships a complete production-grade backend toolkit. Everything is pure Python — no JavaScript required.

### `useFetch` — Declarative Data Fetching

Fetch data from any API and bind the response to reactive VRefs automatically:

```python
from dars.all import *

tasks_sel = ".tasks-data"
_tasks    = setVRef([], tasks_sel)

trigger, loading, data, error = useFetch(
    "/api/tasks",
    on_success=runSequence(
        updateVRef(".loading", False),
        updateVRefFromResponse(tasks_sel),  # stores API response → VRef
    ),
    on_error=runSequence(
        updateVRef(".loading", False),
        updateVRef(".error", True),
    ),
)

page = Page(
    Show(loading, Spinner()),
    Show(error,   Text("Could not load tasks.", style="text-red-500")),
    Each(items=_tasks, render=lambda t: Container(
        Text(t.get("title", "__item_title__"), style="flex-1"),
        Text(f"#{t.get('id', '__item_id__')}",  style="text-xs text-gray-400"),
        style="flex gap-2 p-2 border rounded bg-white",
    )),
    Button("↻ Refresh", on_click=trigger),
)
page.add_script(trigger)  # auto-run on page load
```

### `FormValidator` — Client-Side Validation

Validate forms before submitting — rules declared once in Python, enforced both client-side and server-side:

```python
validator = FormValidator({
    "email":    [required(), email()],
    "password": [required(), min_length(8)],
})

submit = validator.validated_submit(
    url="/api/login",
    form_data=collect_form(email=V("#email"), password=V("#password")),
    on_success=goTo("/dashboard"),
    on_error=setText("error-msg", "Login failed."),
)

page = Page(
    Input(id="email",    placeholder="Email"),
    Text("", id="email-error",    style="text-red-500 text-sm"),
    Input(id="password", placeholder="Password"),
    Text("", id="password-error", style="text-red-500 text-sm"),
    Text("", id="error-msg",      style="text-red-500 text-sm"),
    Button("Login", on_click=submit),
)
```

### `JsonStore` — File-Backed Persistence

Thread-safe, atomic-write JSON storage for rapid prototyping and small backends:

```python
from dars.backend.store import JsonStore

store = JsonStore("tasks.json", default={"tasks": []})

tasks = store.get("tasks", [])
tasks.append({"id": 1, "title": "New task", "done": False})
store.set("tasks", tasks)
```

### `UploadPipeline` — Secure File Uploads

```python
from dars.backend.upload import UploadPipeline

pipeline = UploadPipeline(
    upload_dir="uploads",
    allowed_types=["image/png", "image/jpeg", "application/pdf"],
    max_size_bytes=10 * 1024 * 1024,
)
pipeline.create_endpoint(app, path="/api/upload")
```

Frontend component:

```python
FileUpload(
    upload_url="/api/upload",
    accepted_types=["image/png", "image/jpeg"],
    max_size_bytes=5 * 1024 * 1024,
    on_upload_complete=setText("status", "Uploaded!"),
    on_upload_error=setText("status", "Upload failed."),
)
```

### `SecurityHeadersMiddleware` — HTTP Security

```python
from dars.backend.ssr import SSRApp

ssr = SSRApp(dars_app, prefix="/api/ssr")
ssr.use_cors(origins=["http://localhost:4000"], credentials=True)
ssr.use_security_headers()  # X-Frame-Options, CSP, HSTS, etc.
ssr.use_upload(upload_dir="uploads", allowed_types=["image/*"])

app = ssr.fastapi_app
```

### `DarsEnv` — Environment Variables

```python
from dars.env import DarsEnv

DarsEnv.load()                          # loads .env silently if present
api_key = DarsEnv.get("API_KEY")        # None if missing
secret   = DarsEnv.require("SECRET")   # raises KeyError if missing
```

### Full Backend API Example

```python
from dars.backend.ssr import SSRApp
from dars.backend.store import JsonStore
from main import app as dars_app
from fastapi import Request
from fastapi.responses import JSONResponse
import os

ssr = SSRApp(dars_app, prefix="/api/ssr")
ssr.use_cors(origins=["http://localhost:4000"], credentials=True)
ssr.use_security_headers()

app = ssr.fastapi_app

# ── Production: serve dist/ as static files with SPA fallback ───────────────
from backend.apiConfig import DarsEnv
if not DarsEnv.is_dev():
    ssr.use_spa_fallback()
# ────────────────────────────────────────────────────────────────────────────

_store = JsonStore("tasks_db.json", default={"tasks": []})

@app.get("/api/tasks")
async def get_tasks():
    return JSONResponse({"tasks": _store.get("tasks", [])})

@app.post("/api/tasks")
async def create_task(request: Request):
    body  = await request.json()
    tasks = _store.get("tasks", [])
    task  = {"id": len(tasks) + 1, "title": body.get("title", ""), "done": False}
    tasks.append(task)
    _store.set("tasks", tasks)
    return JSONResponse(task, status_code=201)

@app.put("/api/tasks/{task_id}")
async def update_task(task_id: int, request: Request):
    body  = await request.json()
    tasks = _store.get("tasks", [])
    for t in tasks:
        if t["id"] == task_id:
            t.update({k: v for k, v in body.items() if k != "id"})
            _store.set("tasks", tasks)
            return JSONResponse(t)
    return JSONResponse({"error": "Not found"}, status_code=404)

@app.delete("/api/tasks/{task_id}")
async def delete_task(task_id: int):
    tasks = [t for t in _store.get("tasks", []) if t["id"] != task_id]
    _store.set("tasks", tasks)
    return JSONResponse({"deleted": task_id})

if __name__ == "__main__":
    import uvicorn
    print("\n" + "=" * 60)
    print("Dars Fullstack Backend")
    print("=" * 60)
    if DarsEnv.is_dev():
        port, host = 3000, "127.0.0.1"
    else:
        port, host = 8000, "0.0.0.0"
    print("=" * 60 + "\n")
    uvicorn.run(app, host=host, port=port)
```

For complete backend documentation, see the [Backend & API Guide](https://ztamdev.github.io/Dars-Framework/docs.html#backend-http-utilities).

---

## CLI Usage

| Command                               | What it does                                               |
| ------------------------------------- | ---------------------------------------------------------- |
| `dars export my_app.py --format html` | Export app to HTML/CSS/JS in `./my_app_web`                |
| `dars init --type fullstack`          | Scaffold full-stack project (SPA + SSR + API)              |
| `dars preview`                        | Preview exported app (auto-detects output)                 |
| `dars preview --port 9000`            | Preview on a custom port                                   |
| `dars init my_project`                | Create a new Dars project                                  |
| `dars init --update`                  | Create/Update dars.config.json in current dir              |
| `dars build`                          | Build using dars.config.json                               |
| `dars config validate`                | Validate dars.config.json and print report                 |
| `dars info my_app.py`                 | Show info about your app                                   |
| `dars formats`                        | List supported export formats                              |
| `dars dev`                            | Run the configured entry file with hot preview             |
| `dars dev --port 9000`                | Run dev server on a custom port                            |
| `dars dev --backend`                  | Deprecated: use `dars dev` with backendEntry configured.   |
| `dars generate component <name>`      | Scaffold a new FunctionComponent                           |
| `dars generate page <name>`           | Scaffold a new page (static, SPA, or SSR)                  |
| `dars --help`                         | Show help and all CLI options                              |

Tip: use `dars doctor` to review optional tooling that can enhance bundling/minification.

### Running with Backend

```bash
# Run both frontend and backend together in development
# (backendEntry must be configured in dars.config.json)
dars dev
```

> Note: `dars dev --backend` is deprecated in v1.9.14. `dars dev` now starts the fullstack development server automatically when `backendEntry` is configured.

---

## Local Execution and Live Preview

```python
if __name__ == "__main__":
    app.rTimeCompile()
```

```bash
python my_app.py
# → http://localhost:8000

python my_app.py --port 8088
```

```bash
# Auto-detects output directory and port from config
dars preview

# Or specify a custom path and port
dars preview ./my_exported_app -p 8080
```

---

## Project Configuration (`dars.config.json`)

```json
{
  "entry": "main.py",
  "format": "html",
  "outdir": "dist",
  "publicDir": null,
  "include": [],
  "exclude": ["**/__pycache__", ".git", ".venv", "node_modules"],
  "bundle": true,
  "minify": true,
  "utility_styles": {},
  "markdownHighlight": true,
  "markdownHighlightTheme": "auto",
  "port": 8000,
  "backendEntry": "backend.api:app"
}
```

| Key                 | Description                                                                                           |
| ------------------- | ----------------------------------------------------------------------------------------------------- |
| `entry`             | Python entry file for `dars build` and `dars export config`                                           |
| `format`            | Export format: `html`                                                                                 |
| `outdir`            | Output directory                                                                                      |
| `publicDir`         | Folder copied into output (auto-detected if null)                                                     |
| `bundle`            | Reserved for future use                                                                               |
| `minify`            | Enable/disable JS & CSS minification via **dars-bundler** (default `true`). No Node.js/Vite required. |
| `utility_styles`    | Custom utility class definitions                                                                      |
| `markdownHighlight` | Auto-inject Prism.js for Markdown code blocks (default `true`)                                        |
| `backendEntry`      | Python import path for SSR/backend app (e.g. `"backend.api:app"`)                                     |
| `port`              | Dev preview server port (default `8000`)                                                              |

```bash
dars config validate
dars build
```

---

## Documentation

- [Getting Started](https://ztamdev.github.io/Dars-Framework/docs.html#getting-started-with-dars)
- [Components](https://ztamdev.github.io/Dars-Framework/docs.html#dars-components-documentation)
- [Hooks & Utilities](https://ztamdev.github.io/Dars-Framework/docs.html#hooks-system)
- [Backend & API](https://ztamdev.github.io/Dars-Framework/docs.html#backend-http-utilities)
- [State Management](https://ztamdev.github.io/Dars-Framework/docs.html#state-management-in-dars)
- [Styling](https://ztamdev.github.io/Dars-Framework/docs.html#styling-system-in-dars)
- [Routing](https://ztamdev.github.io/Dars-Framework/docs.html#spa-routing-in-dars-framework)
- [SSR & Deployment](https://ztamdev.github.io/Dars-Framework/docs.html#server-side-rendering-in-dars-framework)
- [Animations](https://ztamdev.github.io/Dars-Framework/docs.html#dars-animation-system)
- [Release Notes](LandingPage/releases/versions.md)

---

- Visit the Dars [official website](https://ztamdev.github.io/Dars-Framework/)
- Visit the Dars official [Documentation](https://ztamdev.github.io/Dars-Framework/docs.html)
- Try Dars without installing anything — visit the [Dars Playground](https://dars-playground.vercel.app/)
