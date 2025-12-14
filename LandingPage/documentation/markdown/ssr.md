# Server-Side Rendering in Dars Framework

Dars Framework provides a complete Server-Side Rendering solution integrated with FastAPI, allowing you to build full-stack applications with both server-rendered and client-side pages in a single codebase.

## Overview

SSR in Dars renders your pages on the server before sending them to the client, providing:

- **Faster Initial Load**: Users see content immediately without waiting for JavaScript
- **Flexible Architecture**: Mix SSR and SPA routes in the same application

## Architecture

### How SSR Works in Dars

1. **Client Request**: Browser requests a page (e.g., `/dashboard`)
2. **Server Rendering**: FastAPI backend renders the Dars component to HTML
3. **HTML Response**: Server sends fully-rendered HTML with embedded VDOM
4. **Client Hydration**: Browser loads JavaScript and "hydrates" the static HTML
5. **Interactive**: Page becomes fully interactive with event handlers

### Dual Hydration System

Dars uses a sophisticated "Dual Hydration" approach to prevent flickering and ensure smooth transitions:

```
Server Side:
1. Render component to HTML
2. Build VDOM representation
3. Inject VDOM as window.__ROUTE_VDOM__
4. Send HTML + VDOM to client

Client Side:
1. Display server-rendered HTML (instant)
2. Load dars.min.js runtime
3. Detect __ROUTE_VDOM__ presence
4. Hydrate DOM without re-rendering
5. Attach event handlers and state
```

This prevents:
- Flash of Unstyled Content (FOUC)
- Double rendering
- Race conditions
- Lost event handlers

### SEO & Metadata

SSR routes are fully SEO-optimized. Using the `Head` component allows you to inject metadata directly into the server-rendered HTML.

```python
@route("/blog/post-1", route_type=RouteType.SSR)
def blog_post():
    return Page(
        Head(
            title="My Amazing Blog Post",
            description="Read this incredible story...",
            keywords="blog, story, amazing",
            og_type="article"
        ),
        # ... content ...
    )
```

## Dars Server Components

Dars Introduces **Server Components**, a granular way to render individual components on the server within any application structure (even inside SPA routes).

### Concept

While traditional SSR renders entire pages, Server Components allow you to mark specific parts of your UI to be rendered by the backend. This is useful for:
- Accessing database or file system directly from component logic.
- Reducing client-side bundle size.
- Dynamic content that updates on the server.

### Usage

To make any component a Server Component, simply set the `use_server=True` property:

```python
from dars.all import *

# This button is rendered on the server
Button(
    "Check Status", 
    use_server=True,
    on_click=dScript("alert('Clicked!')")
)

# This container and its children are rendered on the server
Container(
    Text(f"Server Time: {datetime.now()}"),
    use_server=True
)
```

### Requirements

Server Components require a running Dars FastAPI backend to handle the rendering requests.
- **Development**: Run `dars dev --backend`.
- **Production**: Deploy the full FastAPI application.
The Dars runtime automatically handles fetching the server-rendered HTML and hydrating it with events, so from a developer perspective, they behave just like local components.

---

## Quick Start

### Creating an SSR Project

Use the Dars CLI to scaffold a complete SSR project:

```bash
dars init my-ssr-app --type ssr
cd my-ssr-app
```

This creates:
```
my-ssr-app/
├── main.py              # Frontend (Dars app)
├── backend/
│   ├── api.py          # FastAPI server with SSR
│   └── apiConfig.py    # Environment configuration
└── dars.config.json    # Dars configuration

```

### Project Structure

#### Frontend (`main.py`)

```python
from dars.all import *
from backend.apiConfig import DarsEnv

# Configure SSR URL
ssr_url = DarsEnv.get_urls()['backend']
app = App(title="My SSR App", ssr_url=ssr_url)

# Define SSR route
@route("/", route_type=RouteType.SSR)
def index():
    return Page(
        Text("Hello from Server!", style="fs-[32px]"),
        Button("Click Me", on_click=alert("Interactive!"))
    )

app.add_page("index", index(), title="Home")

if __name__ == "__main__":
    app.rTimeCompile()
```

#### Backend (`backend/api.py`)

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dars.backend.ssr import create_ssr_app
from apiConfig import DarsEnv

# Import Dars app
import sys
sys.path.insert(0, '.')
from main import app as dars_app

# Create FastAPI app with SSR
app = create_ssr_app(dars_app)

# Enable CORS for development
if DarsEnv.is_dev():
    urls = DarsEnv.get_urls()
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[urls['frontend']],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=3000)
```

#### Environment Config (`backend/apiConfig.py`)

```python
class DarsEnv:
    MODE = "development"  # or "production"
    
    DEV = "development"
    BUILD = "production"
    
    @staticmethod
    def is_dev():
        return DarsEnv.MODE == DarsEnv.DEV
    
    @staticmethod
    def get_urls():
        if DarsEnv.is_dev():
            return {
                "backend": "http://localhost:3000",
                "frontend": "http://localhost:8000"
            }
        return {
            "backend": "/",
            "frontend": "/"
        }
```

---

## Route Types

Dars supports two routing modes that can be mixed in the same application:

### 1. SSR Routes (`RouteType.SSR`)

Server-rendered on every request.

```python
@route("/dashboard", route_type=RouteType.SSR)
def dashboard():
    return Page(
        Text("Dashboard", level=1),
        Text(f"Rendered at: {datetime.now()}")
    )
```

**When to use:**
- SEO-critical pages (landing pages, blog posts)
- Dynamic content that changes frequently
- Pages requiring authentication checks server-side
- Initial load performance is critical

### 2. SPA Routes (`RouteType.PUBLIC`) - Default

Client-side navigation, no server rendering.

```python
@route("/settings")  # Default is PUBLIC
def settings():
    return Page(
        Text("Settings", level=1),
        # Interactive forms, real-time updates
    )
```

**When to use:**
- Admin dashboards (not recommended for now in the future will be supported with Dars Middleware)
- Interactive tools
- Pages behind authentication
- Real-time applications

## SSR Lazy-Load Placeholders (SPA Navigation)

When you navigate to an `RouteType.SSR` route from the SPA router, the client fetches route data from the backend (`/api/ssr/...`).
You can configure global loading and error placeholders for this lazy-load step:

```python
app.set_loading_state(
    loadingComp=Page(Container(Text("Loading..."))),
    onErrorComp=Page(Container(Text("Failed to load route")))
)
```

These placeholders are rendered as static HTML (similar to SPA 404/403 pages), which means they do not register states/events and do not interfere with hydration.

### Nested Layouts and `Outlet(placeholder=...)`

For nested routes, layouts typically include one or more `Outlet` placeholders. You can optionally render a layout-level placeholder inside an outlet:

```python
Outlet(outlet_id="main", placeholder=Container(Text("Loading section...")))
```

This is useful when the parent layout is already visible and you want a placeholder only for the child region.

---

## Development Workflow

### Running in Development

You need **two processes** running simultaneously:

**Terminal 1 - Frontend Dev Server:**
```bash
dars dev
# Runs on http://localhost:8000
# Uses app.rTimeCompile() with hot reload for UI changes
```

**Terminal 2 - Backend SSR Server:**
```bash
dars dev --backend
# Runs on http://localhost:3000
# Starts uvicorn with the backendEntry from dars.config.json (by default "backend.api:app")
```

### How It Works

1. **Frontend Server (8000)**: Serves the Dars preview (HTML/CSS/JS) and handles SPA routing.
2. **Backend Server (3000)**: Renders SSR routes and provides API endpoints.

3. **Communication**: Frontend fetches SSR content from backend via `/api/ssr/*`

### Environment Detection

The `DarsEnv` class automatically configures URLs:

```python
# Development
DarsEnv.get_urls() → {
    "backend": "http://localhost:3000",
    "frontend": "http://localhost:8000"
}

# Production
DarsEnv.get_urls() → {
    "backend": "/",
    "frontend": "/"
}
```

---

## SSR API Reference

### `create_ssr_app(dars_app, prefix="/api/ssr", streaming=False)`

Creates a FastAPI application with automatic SSR endpoints.

**Parameters:**
- `dars_app` (App): Your Dars application instance
- `prefix` (str): URL prefix for SSR endpoints (default: `/api/ssr`)
- `streaming` (bool): When `True`, enables HTML streaming so the `<head>` and opening `<body>` are sent first, and the rest of the document is streamed afterwards. Default is `False` (classic non-streaming response).

**Returns:**
- FastAPI application with registered SSR routes

**Auto-generated Endpoints:**

For each SSR route in your Dars app, `create_ssr_app` creates:
- `GET {prefix}/{route_name}` - JSON payload used by the SPA router for lazy SSR loading
- `GET {route_path}` - Full HTML SSR endpoint (e.g. `/`, `/blog`, `/dashboard`)

Additionally, if no SSR route takes `/`, a health-check endpoint is added at:
- `GET /` - Returns basic JSON info about the SSR backend

**Example (non-streaming):**
```python
from dars.backend.ssr import create_ssr_app

app = create_ssr_app(dars_app)
# Automatically creates, for example:
# - GET /api/ssr/index
# - GET /api/ssr/dashboard
# - GET /           (if root not taken by an SSR route)
```

**Example (streaming enabled):**
```python
from dars.backend.ssr import create_ssr_app

app = create_ssr_app(dars_app, streaming=True)
# HTML responses for SSR routes are sent in two chunks:
# 1) <html> + <head> + opening <body>
# 2) The rest of the document (body content + scripts)
```

Behind the scenes, `create_ssr_app` uses `SSRRenderer` to:
- Render the SSR route to HTML and wrap it in `__dars_spa_root__` for hydration.
- Build a minimal SPA config and expose it as `window.__DARS_SPA_CONFIG__`.
- Serialize initial state snapshots:
  - V1: `window.__DARS_STATE__` (STATE_BOOTSTRAP)
  - V2: `window.__DARS_STATE_V2__` (STATE_V2_REGISTRY via `to_dict()`)
- Inject a VDOM snapshot as `window.__ROUTE_VDOM__`.

### `SSRRenderer`

Low-level class for manual SSR rendering.

```python
from dars.backend.ssr import SSRRenderer

renderer = SSRRenderer(dars_app)
result = renderer.render_route("dashboard", params={"user_id": "123"})

# Returns (simplified):
{
    "name": "dashboard",
    "html": "<div>...</div>",              # Body HTML for SPA hydration
    "fullHtml": "<!DOCTYPE html>...",      # Complete HTML document with <head>
    "scripts": [...],                       # Core + page-specific scripts
    "events": {...},                        # Event map for client-side binding
    "vdom": {...},                          # VDOM snapshot for the route
    "states": [...],                        # V1 state snapshot (STATE_BOOTSTRAP)
    "statesV2": [...],                      # V2 state snapshot (STATE_V2_REGISTRY)
    "spaConfig": {...},                     # Minimal SPA routing config
    "headMetadata": {...}                   # Metadata extracted from Head component
}
```

```python
app = App(title="Hybrid App", ssr_url=ssr_url)

# SSR for landing page (SEO)
@route("/", route_type=RouteType.SSR)
def home():
    return Page(Text("Welcome!"))

# SPA for dashboard (interactive)
@route("/dashboard")
def dashboard():
    return Page(Text("Dashboard"))

# Static for docs (performance)
@route("/docs", route_type=RouteType.STATIC)
def docs():
    return Page(Text("Documentation"))

app.add_page("home", home(), title="Home", index=True)
app.add_page("dashboard", dashboard(), title="Dashboard")
app.add_page("docs", docs(), title="Docs")
```

**Navigation Behavior:**
- SSR → SPA: Fetches from backend, hydrates
- SPA → SPA: Client-side navigation (instant)
- Any → Static: Loads pre-rendered HTML

---

## Deployment

### Production Configuration

**1. Update Environment Mode:**

```python
# backend/apiConfig.py
class DarsEnv:
    MODE = "production"  # Change from "development"
```

**2. Build Frontend:**

```bash
dars build
# Generates static files in ./dist
```

**3. Deploy Backend:**

Your FastAPI backend serves both:
- SSR-rendered pages via `/api/ssr/*`
- Static files from `./dist`

**Example Production Server:**

```python
# backend/api.py
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from dars.backend.ssr import create_ssr_app
from main import app as dars_app

app = create_ssr_app(dars_app)

# Serve static files
app.mount("/", StaticFiles(directory="dist", html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

### Deployment Platforms

**Vercel / Netlify:**
- Deploy FastAPI backend as serverless function
- Serve static files from CDN
- Configure environment variables

---