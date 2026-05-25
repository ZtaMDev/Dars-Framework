# Backend & Fullstack API

Dars provides a complete fullstack toolkit: HTTP utilities, a declarative fetch hook, form validation, file uploads, a JSON store, security middleware, and environment management — all in pure Python.

## Table of Contents

- [SSR Backend Setup](#ssr-backend-setup)
- [useFetch — Declarative Data Fetching](#usefetch--declarative-data-fetching)
- [updateVRefFromResponse](#updatevrefromresponse)
- [FormValidator — Client-Side Validation](#formvalidator--client-side-validation)
- [JsonStore — File-Backed Storage](#jsonstore--file-backed-storage)
- [UploadPipeline — File Uploads](#uploadpipeline--file-uploads)
- [SecurityHeadersMiddleware](#securityheadersmiddleware)
- [DarsEnv — Environment Variables](#darsenv--environment-variables)
- [HTTP Client Utilities](#http-client-utilities)
- [Component Management](#component-management)
- [Full Fullstack Example](#full-fullstack-example)

---

## SSR Backend Setup

Dars SSR projects use `SSRApp` to wire together FastAPI, CORS, security headers, and file uploads in one place.

### Project Structure

```
my-app/
├── main.py                  # Dars frontend (routes, components)
├── backend/
│   ├── api.py               # FastAPI entry point
│   └── apiConfig.py         # Environment config
├── dars.config.json
└── .env                     # Environment variables (auto-loaded)
```

### `backend/api.py`

```python
from dars.backend.ssr import SSRApp
from backend.apiConfig import DarsEnv
from main import app as dars_app

ssr = SSRApp(dars_app, prefix="/api/ssr", title="My App - Backend")

urls = DarsEnv.get_urls()
ssr.use_cors(
    origins=[urls["frontend"], "http://127.0.0.1:4000"],
    credentials=True,
)
ssr.use_security_headers()
ssr.use_upload(
    upload_dir="uploads",
    allowed_types=["image/png", "image/jpeg", "application/pdf"],
    max_size_bytes=10 * 1024 * 1024,
    path="/api/upload",
)

app = ssr.fastapi_app

# ── Production: serve dist/ as static files with SPA fallback ───────────────
if not DarsEnv.is_dev():
    ssr.use_spa_fallback()
# ────────────────────────────────────────────────────────────────────────────

# Custom API routes
from fastapi import Request
from fastapi.responses import JSONResponse
from dars.backend.store import JsonStore

_store = JsonStore("tasks_db.json", default={"tasks": []})

@app.get("/api/tasks")
async def get_tasks():
    return JSONResponse({"tasks": _store.get("tasks", [])})

@app.post("/api/tasks")
async def create_task(request: Request):
    body = await request.json()
    tasks = _store.get("tasks", [])
    task = {"id": len(tasks) + 1, "title": body.get("title", ""), "done": False}
    tasks.append(task)
    _store.set("tasks", tasks)
    return JSONResponse(task, status_code=201)

if __name__ == "__main__":
    import uvicorn
    print("\n" + "=" * 60)
    print("Dars Fullstack Backend")
    print("=" * 60)
    if DarsEnv.is_dev():
        print(f"  Backend:  {urls['backend']}")
        print(f"  Frontend: {urls['frontend']}  (run 'dars dev' separately)")
        print(f"  API Docs: {urls['backend']}/docs")
        port, host = 3000, "127.0.0.1"
    else:
        frontend_dir = DarsEnv.get_frontend_dist_dir()
        print(f"  App:      http://0.0.0.0:8000  (frontend + API, same origin)")
        print(f"  Frontend: {frontend_dir}")
        port, host = 8000, "0.0.0.0"
    print("=" * 60 + "\n")
    uvicorn.run(app, host=host, port=port)
```

### `backend/apiConfig.py`

```python
import os

class DarsEnv:
    MODE = os.environ.get("DARS_MODE", "development")

    @staticmethod
    def is_dev():
        return DarsEnv.MODE == "development"

    @staticmethod
    def get_urls():
        if DarsEnv.is_dev():
            return {"backend": "http://localhost:3000", "frontend": "http://localhost:4000"}
        return {"backend": "/", "frontend": "/"}
```

### Running

```bash
# Run frontend and backend together in development
# (backendEntry must be configured in dars.config.json)
dars dev
```

> Note: `dars dev --backend` is deprecated in v1.9.14. Use `dars dev` to start the fullstack development workflow.

---

## useFetch — Declarative Data Fetching

`useFetch` creates a fetch trigger and three reactive VRefs (loading, data, error) wired to a `network_request` DAP action. No JavaScript needed.

### Signature

```python
useFetch(
    url: str,
    method: str = "GET",
    body: Any = None,
    headers: dict = None,
    on_success: dScript = None,
    on_error: dScript = None,
) -> Tuple[dScript, VRefValue, VRefValue, VRefValue]
```

Returns `(trigger_script, loading_vref, data_vref, error_vref)`.

### Basic Usage

```python
from dars.all import *

trigger, loading, data_vref, error = useFetch("/api/users")

page = Page(
    Show(loading, Spinner()),
    Show(error,   Text("Error loading data", style="text-red-500")),
    Text(data_vref),
    Button("Reload", on_click=trigger),
)
page.add_script(trigger)  # auto-run on load
```

### With Callbacks

```python
tasks_sel = ".tasks-data"
_tasks = setVRef([], tasks_sel)

trigger, loading, _, error = useFetch(
    "/api/tasks",
    on_success=runSequence(
        updateVRef(".loading", False),
        updateVRefFromResponse(tasks_sel),   # store response → VRef
    ),
    on_error=runSequence(
        updateVRef(".loading", False),
        updateVRef(".error", True),
    ),
)
```

### POST with Body

```python
trigger, loading, data, error = useFetch(
    "/api/search",
    method="POST",
    body={"query": "dars"},
    headers={"Content-Type": "application/json"},
)
```

---

## updateVRefFromResponse

Stores the API response from a `useFetch` `on_success` context into a VRef selector. The `network_request` DAP op passes the parsed response as `ctx.response`.

```python
updateVRefFromResponse(selector: str, key: str = "response") -> dScript
```

```python
on_success=runSequence(
    updateVRef(".loading", False),
    updateVRefFromResponse(".tasks-data"),
)
```

#### Nested JSON Path Extraction (Dot-Notation)
You can use dot-notation in the `key` parameter to drill down into nested JSON response structures (e.g. `response.user.username`, `response.data.items`). This makes Dars completely compatible with any backend or third-party JSON API, extracting just the data you need without manual transformation.

```python
on_success=runSequence(
    updateVRefFromResponse(".user-name", key="response.user.username"),
    updateVRefFromResponse(".user-role", key="response.user.role"),
)
```

---

## FormValidator — Client-Side Validation

Declarative validation with dual client/server enforcement. Rules are declared once in Python.

### Rules

| Constructor | Description |
|---|---|
| `required()` | Field must be non-empty |
| `min_length(n)` | Minimum character count |
| `max_length(n)` | Maximum character count |
| `email()` | Must be a valid email address |
| `pattern(regex)` | Must match regex |
| `min_value(n)` | Numeric minimum |
| `max_value(n)` | Numeric maximum |
| `custom(fn)` | Python callable `(value) -> Optional[str]` |

### `validated_submit`

Validates all rules client-side first. Only fires the network request if every rule passes. Error messages appear in `#{field}-error` elements.

```python
from dars.all import *

task_form = collect_form(title=V("#title"))

validator = FormValidator({
    "title": [required(), min_length(3), max_length(100)],
})

submit_action = validator.validated_submit(
    url="/api/tasks",
    form_data=task_form,
    on_success=runSequence(clearInput("title"), fetch_trigger),
    on_error=setText("submit-error", "Error submitting. Try again."),
)

# In your Page:
Input(id="title", placeholder="Task title…"),
Text("", id="title-error", style="text-red-500 text-sm"),
Button("Add Task", on_click=submit_action),
```

> **Important:** The input `id` must match the field name in `FormValidator` so the selector `#title` resolves correctly.

### Server-Side Validation

```python
errors = validator.validate_server({"title": "Hi"})
# → {"title": ["Must be at least 3 characters."]}

errors = validator.validate_server({"title": "Hello World"})
# → {}  (all pass)
```

### Get Rules as JSON

```python
rules_json = validator.get_rules_json()
# → '{"title": [{"type": "required"}, {"type": "min_length", "n": 3}]}'
```

---

## JsonStore — File-Backed Storage

Thread-safe, atomic-write JSON persistence. Ideal for prototyping and small backends.

```python
from dars.all import *

store = JsonStore("data.json", default={"tasks": []})

# Read
tasks = store.get("tasks", [])

# Write (atomic)
store.set("tasks", tasks + [{"id": 1, "title": "New task"}])

# Delete key
store.delete("tasks")

# Get all
all_data = store.all()

# Clear
store.clear()
```

- Writes to a `.tmp` file then atomically replaces the target via `os.replace()`
- Per-instance `threading.Lock` on all mutating operations
- Raises `ValueError` on malformed JSON with a descriptive message

---

## UploadPipeline — File Uploads

Server-side file upload handler with MIME type validation, size limits, and filename sanitisation.

```python
from dars.all import *

pipeline = UploadPipeline(
    upload_dir="uploads",
    allowed_types=["image/png", "image/jpeg", "image/gif", "application/pdf"],
    max_size_bytes=10 * 1024 * 1024,  # 10 MB
)
pipeline.create_endpoint(app, path="/api/upload")
```

| Status | Condition |
|---|---|
| `200` | Upload successful — returns `{"url": "/uploads/filename.png"}` |
| `413` | File exceeds `max_size_bytes` |
| `415` | MIME type not in `allowed_types` |
| `500` | Disk write failure |

### Custom Rename

```python
import uuid

pipeline = UploadPipeline(
    upload_dir="uploads",
    rename_fn=lambda name: f"{uuid.uuid4().hex}_{name}",
)
```

### Filename Sanitisation

`UploadPipeline.sanitize_filename(filename)` removes `../`, `./`, and any character outside `[a-zA-Z0-9._-]`.

### FileUpload Component

```python
FileUpload(
    upload_url="/api/upload",
    accepted_types=["image/png", "image/jpeg"],
    max_size_bytes=5 * 1024 * 1024,
    on_upload_complete=setText("status", "Uploaded!"),
    on_upload_error=setText("status", "Upload failed."),
)
```

---

## SecurityHeadersMiddleware

Injects HTTP security headers into every response. Headers are only added when not already present, so application code can override any individual header.

```python
from dars.all import *

# Via SSRApp (recommended)
ssr.use_security_headers()

# Or manually
from dars.backend.middleware import SecurityHeadersMiddleware
app.add_middleware(SecurityHeadersMiddleware, csp="default-src 'self'", hsts=True)
```

**Default headers injected:**

| Header | Value |
|---|---|
| `X-Content-Type-Options` | `nosniff` |
| `X-Frame-Options` | `DENY` |
| `X-XSS-Protection` | `1; mode=block` |
| `Referrer-Policy` | `strict-origin-when-cross-origin` |
| `Permissions-Policy` | `geolocation=(), microphone=(), camera=()` |

**Optional:**
- `csp="..."` → adds `Content-Security-Policy`
- `hsts=True` → adds `Strict-Transport-Security: max-age=31536000; includeSubDomains`

---

## DarsEnv — Environment Variables

`DarsEnv` loads `.env` files and provides typed access to environment variables.

### `.env` File

```env
API_KEY=my-secret-key
DATABASE_URL=sqlite:///./app.db
DEBUG=true
```

### Usage

```python
from dars.env import DarsEnv

# Load .env (called automatically by load_config)
DarsEnv.load()
DarsEnv.load(path="config/.env")  # custom path

# Read
api_key = DarsEnv.get("API_KEY")           # None if missing
api_key = DarsEnv.get("API_KEY", "default")

# Require (raises KeyError if missing)
secret = DarsEnv.require("SECRET_KEY")

# Dev/prod mode
DarsEnv.set_dev_mode(True)
if DarsEnv.dev:
    print("Running in development mode")
```

**Rules:**
- Does not overwrite existing `os.environ` keys
- Strips surrounding single or double quotes from values
- Skips blank lines and `#` comments
- Splits on the first `=` only (values may contain `=`)
- Called automatically by `load_config()` before reading `dars.config.json`

---

## HTTP Client Utilities

Lower-level HTTP helpers that return `dScript` objects for use in event handlers.

```python
from dars.backend.http import fetch, get, post, put, delete, patch

# GET
get_users = get(id="userData", url="/api/users")

# POST
create_user = post(
    id="createResult",
    url="/api/users",
    body={"name": "Alice"},
    callback=alert("User created!"),
    on_error=alert("Error!"),
)
```

### Interceptors

```python
from dars.backend.http import add_request_interceptor, use_auth_interceptor

# Add auth token to every request
use_auth_interceptor(token_key="dars_auth_token")

# Custom interceptor
add_request_interceptor(lambda cfg: {**cfg, "headers": {**cfg.get("headers", {}), "X-App": "1"}})
```

### `useData` — Access Response Data

```python
from dars.backend.data import useData

# Dot-notation access to fetched data
name_state.text.set(useData("userData").name)
city_state.text.set(useData("userData").address.city)
```

---

## Component Management

Create, update, and delete components dynamically at runtime.

```python
from dars.all import *

new_item = Text("Hello!", id="new-item")

Button("Add",    on_click=createComp(new_item, root="container-id", position="append"))
Button("Remove", on_click=deleteComp("new-item"))
Button("Update", on_click=updateComp("new-item", text="Updated!"))
```

---

## Full Fullstack Example

A complete task manager using `useFetch`, `Each`, `FormValidator`, `JsonStore`, and `SSRApp`.

### Frontend (`pages/did.py`)

```python
from dars.all import *

@route("/did")
def did():
    loading_sel = ".tasks-loading"
    error_sel   = ".tasks-error"
    tasks_sel   = ".tasks-data"

    is_loading = setVRef(True,  loading_sel)
    has_error  = setVRef(False, error_sel)
    _tasks     = setVRef([],    tasks_sel)

    on_fetch_success = runSequence(
        updateVRef(loading_sel, False),
        updateVRef(error_sel,   False),
        updateVRefFromResponse(tasks_sel),
    )
    on_fetch_error = runSequence(
        updateVRef(loading_sel, False),
        updateVRef(error_sel,   True),
    )

    fetch_trigger, _lv, _dv, _ev = useFetch(
        "/api/tasks",
        on_success=on_fetch_success,
        on_error=on_fetch_error,
    )

    task_form = collect_form(title=V("#title"))
    validator = FormValidator({"title": [required(), min_length(3), max_length(100)]})

    submit_action = validator.validated_submit(
        url="/api/tasks",
        form_data=task_form,
        on_success=runSequence(clearInput("title"), fetch_trigger),
        on_error=setText("submit-error", "Error submitting. Try again."),
    )

    def task_item(t):
        title   = t.get("title", "__item_title__") if isinstance(t, dict) else "__item_title__"
        item_id = t.get("id",    "__item_id__")    if isinstance(t, dict) else "__item_id__"
        return Container(
            Text(title,        style="flex: 1 1 0%", class_name="__item_done_class__"),
            Text(f"#{item_id}", style="text-xs text-gray-400 ml-2"),
            style="flex items-center gap-2 p-2 border rounded mb-1 bg-white shadow-sm",
        )

    page = Page(
        Container(
            Head("Task Manager"),
            Text("Task Manager", style="text-3xl font-bold mb-1 text-indigo-600"),

            Show(is_loading, Container(Spinner(), Text("Loading…"), style="flex gap-2 mb-4")),
            Show(has_error,  Container(Text("Backend not running?", style="text-red-600"),
                                       style="bg-red-50 border rounded p-3 mb-4")),

            Each(items=_tasks, render=task_item, class_name="space-y-1 mb-6 min-h-[40px]"),

            Container(
                Text("Add a task", style="font-semibold mb-2"),
                Input(id="title", placeholder="Task title (min 3 chars)…",
                      class_name="border rounded px-3 py-2 w-full mb-1"),
                Text("", id="title-error",  style="text-red-500 text-sm mb-1"),
                Text("", id="submit-error", style="text-red-500 text-sm mb-2"),
                Button("Add Task", on_click=submit_action,
                       style="bg-indigo-600 text-white px-4 py-2 rounded"),
                style="bg-white border rounded-xl p-4 shadow-sm mb-4",
            ),
            Button("↻ Refresh", on_click=fetch_trigger,
                   style="text-sm text-indigo-500 underline"),
            style="max-w-xl mx-auto p-8 font-sans",
        )
    )
    page.add_script(fetch_trigger)
    return page
```

### Backend (`backend/api.py`)

```python
from dars.backend.ssr import SSRApp
from backend.apiConfig import DarsEnv
from main import app as dars_app
from dars.backend.store import JsonStore
from fastapi import Request
from fastapi.responses import JSONResponse
import os

ssr = SSRApp(dars_app, prefix="/api/ssr")
urls = DarsEnv.get_urls()
ssr.use_cors(origins=[urls["frontend"]], credentials=True)
ssr.use_security_headers()

app = ssr.fastapi_app

# ── Production: serve dist/ as static files with SPA fallback ───────────────
if not DarsEnv.is_dev():
    ssr.use_spa_fallback()
# ────────────────────────────────────────────────────────────────────────────

_store = JsonStore(
    path=os.path.join(os.path.dirname(__file__), "..", "tasks_db.json"),
    default={"tasks": []},
)

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

### How It All Connects

1. Page loads → `fetch_trigger` fires → `network_request` DAP op hits `/api/tasks`
2. Backend reads from `JsonStore` → returns `{"tasks": [...]}`
3. `on_success` runs → `updateVRefFromResponse(".tasks-data")` stores response in VRef
4. `dom_each_render` detects VRef change → substitutes `__item_title__`, `__item_id__` placeholders → list renders
5. User types in `#title` input → clicks "Add Task"
6. `FormValidator` checks `required()` + `min_length(3)` client-side
7. If valid → `network_request` POSTs to `/api/tasks` → backend appends to `JsonStore`
8. `on_success` → `clearInput("title")` + `fetch_trigger` → list refreshes

---

## API Reference

### `useFetch(url, method, body, headers, on_success, on_error)`
Returns `(trigger, loading_vref, data_vref, error_vref)`.

### `updateVRefFromResponse(selector, key="response")`
Stores `ctx[key]` from fetch context into a VRef.

### `FormValidator(fields)`
- `.validated_submit(url, form_data, on_success, on_error)` — validate then submit
- `.validate_server(data)` → `dict` of errors
- `.get_rules_json()` → JSON string

### `JsonStore(path, default)`
- `.get(key, default)`, `.set(key, value)`, `.delete(key)`, `.all()`, `.clear()`

### `UploadPipeline(upload_dir, allowed_types, max_size_bytes, rename_fn)`
- `.create_endpoint(app, path)` — registers FastAPI POST endpoint
- `.sanitize_filename(filename)` — static method

### `SecurityHeadersMiddleware(app, csp, hsts)`
Starlette middleware. Use via `ssr.use_security_headers()` or `app.add_middleware(...)`.

### `DarsEnv`
- `.load(path=".env")`, `.get(key, default)`, `.require(key)`, `.set_dev_mode(bool)`
