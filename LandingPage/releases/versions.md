# Release Notes v1.9.17

> **Database Layer, Server Actions, Route Types, Guards, Middleware System & Auth Simplification**
> *Major full-stack expansion: built-in ORM, server-side actions, security middleware, and a simplified decorator-based auth system.*

## Installation

```bash
pip install --upgrade dars-framework
```

## What's New

### Database Layer: Declarative ORM for SQLite

Dars now ships with a complete built-in database layer for SQLite:

- **`DarsModel`** — Declarative model base class with auto-detected fields
- **Field Types**: `TextField`, `IntegerField`, `FloatField`, `BooleanField`, `DateTimeField`, `JSONField`, `ForeignKey`
- **`ModelManager`** — Per-model query API: `all()`, `get()`, `filter()`, `count()`, `create()`, `delete()`
- **`Database`** — Thread-safe SQLite connection manager with WAL mode, migration tracking, and raw SQL support
- **`register_model_api()`** — Auto-generate full CRUD REST endpoints (`GET/POST/PUT/DELETE`) for all registered models

```python
class Product(DarsModel):
    __tablename__ = "products"
    name = TextField(nullable=False)
    price = IntegerField(default=0)

db = Database("app.db")
db.register(Product)
db.create_all()

# Query
Product.objects.filter(price=0)
```

### Server Actions — Call Python from the Browser

A new `@server_action` decorator system that registers Python functions as API endpoints callable from client-side events:

```python
from dars.backend.actions import server_action, call_server

@server_action
def greet(name: str, count: int = 1) -> list:
    return [f"Hello {name}! x{i}" for i in range(count)]

Button("Greet", on_click=call_server("greet", name="World", count=3))
```

- Type-annotated parameters validated via Pydantic
- Sync and async support
- Auth-protected actions with `@server_action(auth_required=True, roles=["admin"])`
- CSRF protection for mutating actions
- Auto-discovery: `discover_actions("backend.api")`
- Exposed as `POST /api/actions/{action_name}`

### Route Types

New `RouteType` enum system for SPA-level route protection:

- **`RouteType.PUBLIC`** — No auth required (default)
- **`RouteType.SSR`** — Server-side rendered
- **`RouteType.PRIVATE`** — Requires authentication, redirects to login
- **`RouteType.PROTECTED`** — Requires authentication AND specific roles

```python
@route("/admin", route_type=RouteType.PROTECTED, roles=["admin"])
def admin_panel():
    return Page(...)
```

### Simplified Auth System with `@requires_auth`

The authentication system has been fundamentally simplified:

- **`@requires_auth`** — Now a proper FastAPI route decorator that auto-injects `request.state.user`. Can be used bare (`@requires_auth`) or with custom callback/secret (`@requires_auth(verify_credentials_callback=fn, secret="...")`).
- **`@requires_role("admin")`** — Role-based access control decorator compatible with any FastAPI route.
- **Auto-registration**: When `verify_credentials_callback` and `secret` are passed to `@requires_auth`, it auto-registers the auth config with a predictable `auth_id` (e.g., `auth_dashboard` for `def dashboard()`).
- **`app.setup_auth()`** — Global auth configuration with optional `auth_id` and custom `login_page`.
- **Scoped auth endpoints**: `/_dars/auth/{auth_id}/login`, `/me`, `/logout`, `/refresh` generated automatically for each scheme.
- **Session management**: `SessionManager` + `InMemorySessionStore` with `SessionStore` protocol for custom backends.
- **CSRF protection** with automatic `XSRF-TOKEN` cookie/header validation and refresh token rotation.

### Production-Grade Middleware System

A complete middleware pipeline for FastAPI/Starlette:

- **`DarsMiddleware`** — Abstract base class with `before_request` / `after_response` lifecycle hooks
- **`AuthMiddleware`** — JWT Bearer/cookie validation with CSRF protection and multi-auth cookie detection
- **`SecurityHeadersMiddleware`** — CSP, HSTS, X-Frame-Options, X-Content-Type-Options, Referrer-Policy, Permissions-Policy, XSS-Protection
- **`CORSMiddleware`** — Configurable CORS with origin matching, credential support, and preflight handling
- **`RateLimitMiddleware`** — Sliding-window per-IP/per-user rate limiter with burst support
- **`LoggingMiddleware`** — Structured request/response logging with body and header capture
- **`CompressionMiddleware`** — Gzip response compression for text-based content types
- **`MiddlewareChain`** — Compose multiple middlewares into a single Starlette middleware
- **`register_default_middlewares()`** — One-call setup of the full middleware stack
---

# Release Notes v1.9.15

> **Production-Grade Authentication: Multi-Auth, Secure Cookies & Server-Side Security**
> *This is a major update that has been in preparation and development for a long time.*

## Installation

```bash
pip install --upgrade dars-framework
```

## What's New

### Secure-by-Default Authentication System

Dars now ships with a complete, production-ready authentication system that is **completely isolated from the VDOM**. 

- **HttpOnly Cookie-Based Sessions**: Tokens never touch the browser's JavaScript context. They live exclusively in HttpOnly cookies.
- **CSRF Protection**: Built-in `XSRF-TOKEN` cookie and header validation for all mutating requests (`POST`, `PUT`, `DELETE`, `PATCH`).
- **Refresh Token Rotation**: Long-lived refresh tokens are automatically rotated on every use.
- **Pure Python JWT**: Zero third-party dependencies for generating and verifying JSON Web Tokens.

### Multi-Auth: Multiple Isolated Schemes

You can now register **multiple independent authentication configurations** in the same app, each with its own secret, callback, and scoped cookies.

- A user can be logged in as an "admin" and a "guest" simultaneously without session collision.
- Handled seamlessly by scoped cookie names (e.g., `dars_access_token_admin`).

### Three Ways to Declare Auth

1. **`@requires_auth` (Inline)**: Simply add the decorator below your route. Auto-registers the auth scheme with an ID derived from the function name.
2. **`Page.setup_auth()` (Component-level)**: Configure auth directly on your `Page` components.
3. **`App.setup_auth()` (Global)**: Register an auth configuration globally across your app.

### JSON Field Extraction in `updateVRefFromResponse`

`updateVRefFromResponse` now supports a `key` parameter, allowing you to easily extract deeply nested fields from JSON API responses using dot-notation. This makes Dars fully server-compatible using standard JSON responses.

```python
# Extracts response["user"]["username"] and stores it in the VRef
updateVRefFromResponse(".user-name", key="response.user.username")
```

---

# Release Notes v1.9.14

> **Unified fullstack dev:** `dars dev` now starts frontend and backend together when `backendEntry` is configured. `dars dev --backend` is deprecated.

## Installation

```bash
pip install --upgrade dars-framework
```

## What's New

### Unified fullstack development

- `dars dev` now launches the frontend preview server and backend SSR/API server together when `backendEntry` is configured in `dars.config.json`.
- Development environment variables are propagated automatically so the frontend knows the backend URL.
- `dars dev --backend` remains supported for compatibility, but it now prints a deprecation warning.
- Documentation and release notes updated to reflect the new single-command workflow.

---

# Release Notes v1.9.13

> **Desktop exporter removed, future `dars-desktop` with PyQt6 + WebEngine, and continued web exporter stability**

## Installation

```bash
pip install --upgrade dars-framework
```

## What's New

### Desktop exporter removal and new desktop strategy

The legacy desktop export path has been removed from the core Dars framework. This makes the framework leaner and keeps the main package focused on web application export, build, and SSR workflows.

- The `format: "desktop"` export path is no longer supported in `dars-framework`.
- Desktop application support is being re-architected as a separate package: `dars-desktop`.
- The new approach will use **pure Python** with **PyQt6** and **PyQt6 WebEngine**, avoiding Electron and Node/npm dependencies.
- This future package will embed the Dars web runtime inside a native Qt browser view and provide a Python-first desktop packaging experience.

### Core framework focus

- `dars-framework` now prioritizes stable web export, SPA/SSR workflows, and the improved `dars-bundler` pipeline.
- This separation allows desktop packaging innovation without affecting the core web framework.

### Future package roadmap: `dars-desktop`

- Planned as an independent companion package delivering desktop shells using PyQt6 WebEngine.
- Designed for Python-only install flows and Qt-native desktop lifecycle management.
- Will allow clean separation between web export features in `dars-framework` and desktop-specific packaging logic.

---

# Release Notes v1.9.12

> **dars-bundler: Standalone Rust Minifier, Static Site Router Optimization & Unified Config**

## Installation

```bash
pip install --upgrade dars-framework
```

## What's New

### dars-bundler — High-Performance Standalone Rust Minifier

Dars now ships with **dars-bundler**, a standalone cross-platform binary written in Rust that replaces the entire `rjsmin` / `rcssmin` / Vite/esbuild minification pipeline. It requires **zero external dependencies** — no Node.js, npm, or Vite installation needed on the developer's machine.

Under the hood, dars-bundler uses:

- **SWC** (Speedy Web Compiler) for AST-level JavaScript minification: dead-code elimination, constant folding, variable mangling, and unreachable-code pruning.
- **LightningCSS** for CSS minification: vendor-prefix removal, color value optimization, and redundant rule elimination.
- **Rayon** for parallelized, multi-core file processing across the entire output directory.

The binary is discovered automatically in this priority order:

1. `DARS_BUNDLER_PATH` environment variable (user override)
2. Alongside the Python executable (venv-friendly)
3. System `PATH`
4. `dars/bundler/` inside the framework package (shipped with Dars)
5. Dev-mode: adjacent `DarsBundler/` repo `target/debug|release` build

Pre-built binaries for **Windows (amd64)**, **Linux (amd64)**, and **macOS (amd64 + arm64)** are released via GitHub Actions on every tagged release.

### Simplified `dars.config.json` — Single `minify` Key

The old dual-key minification configuration (`defaultMinify` + `viteMinify`) has been replaced by a single, unified key:

```json
{
  "minify": true
}
```

- `true` (default) — dars-bundler runs after export, minifying all JS and CSS files in-place.
- `false` — minification is skipped entirely.

Old keys are accepted for backward compatibility but are no longer the source of truth. Existing projects do **not** need to update their configs immediately.

All 13 `dars.config.json` files in the framework's own repos have been updated to use the new format.

### Static Site Generation: Router Elimination

When exporting a **purely static site** (no SPA routes), Dars now automatically:

1. **Omits `router.js`** from the generated `lib/` directory entirely — shaving ~11 KB from the cold load.
2. **Patches `dars.min.js` on-the-fly** to strip the `import { ... } from "./router.js"` statement and the `router:` key from the exported `Dars` object, ensuring no broken import references at runtime.

SPA projects are unaffected — the full router is still included when `app._spa_routes` is populated.

### CLI Minification Flow Cleanup

The `dars export` and `dars build` commands previously contained ~90 lines of duplicated, branching environment-variable logic (`DARS_VITE_MINIFY`, `DARS_DEFAULT_MINIFY`, `DARS_DEFAULT_MINIFY_ONLY_FALLBACK`, etc.) wired across three separate code paths. This has been replaced with a single, clean block:

```python
minify_enabled = cfg.get('minify', cfg.get('defaultMinify', True))
os.environ['DARS_MINIFY'] = '1' if minify_enabled else '0'
```

The `--no-minify` CLI flag continues to work on both `dars export` and `dars build`.

## Deprecations

| Old key         | Status                            | Replacement |
| --------------- | --------------------------------- | ----------- |
| `viteMinify`    | Deprecated (backward-compat read) | `minify`    |
| `defaultMinify` | Deprecated (backward-compat read) | `minify`    |

---

# Release Notes v1.9.11

> **Secure Asynchronous SSR Hydration, `useVRef` Hook, Pure SPA Shells & CLI Lifecycle Hardening**

## Installation

```bash
pip install --upgrade dars-framework
```

## What's New

### Secure Asynchronous SSR Hydration

The Dars Server Protocol (DSP) payload handling has been fundamentally redesigned to prioritize security and DOM cleanliness.

- **Clean HTML Payload**: The bulky inline JSON payload (`<script id="__DARS_DSP_DATA__">`) has been entirely removed from the SSR HTML source. Pre-rendered pages are now shipped with pure, semantic HTML.
- **Same-Origin Async Fetching**: The SPA Router now securely retrieves hydration data (VDOM snapshots, states, and specific scripts) via asynchronous API requests. These requests strictly enforce `mode: "same-origin"` and `credentials: "same-origin"` to prevent external interception.
- **Anti-Flash Routing**: Fixed a rendering regression where the router's initialization sequence would accidentally hide the active SSR DOM. `router.js` now correctly identifies and preserves the visibility of the hydrated `.dars-page` root container.

### Decoupled SPA Shell Runtime (`app.js`)

- **Pure Bootloader**: `app.js` no longer incorrectly bundles VRef and reactive state bindings (`window.__DARS_VREF_VALUES__`) from all compiled routes. It has been refactored into a pristine, lightweight bootloader that _exclusively_ contains the SPA route map and framework initialization logic.
- **Isolated Route States**: Individual `app_{slug}.js` files (like `app_did.js`) now retain complete, isolated control over their specific states, preventing namespace pollution and duplicate execution on navigation.
- **Smart Script Deduplication**: The SPA router now scans the DOM before injecting scripts fetched from the SSR API, preventing issues where route-specific scripts were appended twice during initial hydration.

### Hardened Dev Server Lifecycle

The CLI process management for `dars preview` (specifically with Uvicorn backends) has been aggressively optimized.

- **Instant Termination**: Pressing `Ctrl+C` no longer results in a hanging terminal or "zombie" background processes waiting for WebSockets to close.
- **Force Kill Tree**: The CLI now utilizes forced OS-level termination (`taskkill /F /T` on Windows, `SIGKILL` on Unix) combined with an immediate `os._exit(0)`, ensuring the backend server is dismantled instantly.

### `useVRef()` — Reactive VRef Consumer Hook

The VRef ecosystem is now complete with the introduction of `useVRef()`, closing the reactive loop alongside `setVRef` (define) and `updateVRef` (mutate).

```python
from dars.all import *

# Define initial state
price = setVRef(19.99, ".item-price")
qty   = setVRef(2,     ".item-qty")

# Consume reactively — initial value is resolved at SSR time (no flash!)
Text(text=useVRef(V(".item-price")))
Text(text=useVRef(V(".item-price").float() * V(".item-qty").int()))  # "39.98"
Button("Checkout", disabled=useVRef(V(".item-qty").int() == 0))

# Mutate to trigger reactive updates everywhere
Button("+", on_click=updateVRef(".item-qty", V(".item-qty").int() + 1))
```

- **Zero flash on SSR**: `useVRef` pre-resolves the initial value at build time by looking up the bound selector in the `setVRef` registry -- the server HTML already has the correct value.
- **Auto-dependency detection**: The compiler walks the `V()` expression tree and automatically extracts every CSS selector used. At runtime, whenever any of those selectors is updated via `updateVRef()`, the binding re-evaluates and patches the DOM instantly -- no manual `dependencies` list required.
- **Reactive callbacks**: Pass `dScript`, `RawJS`, or plain strings via the `callbacks` parameter (single value or list). They fire every time the binding re-evaluates, enabling side-effects like logging or chained updates.

```python
# Callbacks fire every time .value-stuff changes
Text(text=useVRef(
    V(".value-stuff"),
    callbacks=log("value-stuff changed!")
))
```

- **Expression support**: Accepts any `V()` expression, `MathExpression`, `BooleanExpression`, or plain literal.
- **Hydration bridge**: At runtime, the framework injects a JS registration block that reconnects the DOM element to the live `window.__DARS_VREF_VALUES__` registry, keeping it in sync with any subsequent `updateVRef` calls.
- **Compiler fix**: Resolved a regression where `VRefBinding` objects were iterated by key instead of by value, causing the reactive JS block to be silently omitted from the output bundle.

---

# Release Notes v1.9.9

> **Production-Grade Fullstack: useFetch, FormValidator, Each, JsonStore, UploadPipeline, SecurityHeaders & .env Support**

## Installation

```bash
pip install --upgrade dars-framework
```

## What's New

### `useFetch` — Declarative Data Fetching Hook

A new `useFetch` hook provides a fully Pythonic way to fetch data from APIs and bind the response to reactive VRefs — no JavaScript required.

```python
from dars.all import *

trigger, loading, data, error = useFetch(
    "/api/tasks",
    method="GET",
    on_success=runSequence(
        updateVRef(".loading", False),
        updateVRefFromResponse(".tasks-data"),
    ),
    on_error=updateVRef(".error", True),
)

page.add_script(trigger)  # auto-run on page load
```

- Returns `(trigger_script, loading_vref, data_vref, error_vref)` — all pure Python objects
- Integrates with `Show`, `Each`, and `updateVRefFromResponse` for zero-boilerplate reactive UIs
- Handles loading state, 401 interception, and error propagation automatically via the `network_request` DAP op

### `updateVRefFromResponse` — Store Fetch Response into VRef

New helper that stores the API response from a `useFetch` `on_success` context directly into a VRef selector. Works seamlessly with `Each` for runtime list rendering.

```python
on_success=runSequence(
    updateVRef(".loading", False),
    updateVRefFromResponse(".tasks-data"),  # stores ctx.response → VRef
)
```

### `Each` — Runtime List Rendering from VRef

The `Each` component now fully supports runtime VRef items (e.g. from `useFetch`). Pass a `VRefValue` as `items` and a render function — the exporter generates an HTML template at compile time, and the browser substitutes real item values at runtime.

```python
Each(
    items=tasks_vref,   # VRefValue from setVRef([])
    render=lambda t: Container(
        Text(t.get("title", "__item_title__")),
        Text(f"#{t.get('id', '__item_id__')}"),
        style="flex items-center gap-2 p-2 border rounded bg-white",
    ),
)
```

- Compile-time: render function called with a sentinel dict to produce the HTML template
- Runtime: `dom_each_render` substitutes `__item_<field>__` placeholders with real values
- Automatically unwraps common API response shapes (`{tasks:[...]}`, `{items:[...]}`, `{data:[...]}`)
- `done_class` placeholder supported for conditional styling (e.g. strikethrough for completed items)

**Fixed:** `VRefValue` objects passed as `items` no longer cause `TypeError: 'VRefValue' object is not iterable` at export time.

### `FormValidator` — Client-Side Form Validation

Declarative form validation with dual client/server enforcement. Rules are declared once in Python and evaluated both server-side and client-side via DAP.

```python
validator = FormValidator({
    "title": [required(), min_length(3), max_length(100)],
    "email": [required(), email()],
})

# validated_submit: validates first, only submits if all rules pass
submit_action = validator.validated_submit(
    url="/api/tasks",
    form_data=collect_form(title=V("#title")),
    on_success=runSequence(clearInput("title"), fetch_trigger),
    on_error=setText("submit-error", "Error submitting."),
)
```

**Available rules:** `required()`, `min_length(n)`, `max_length(n)`, `pattern(regex)`, `email()`, `min_value(n)`, `max_value(n)`, `custom(fn)`

**Fixed:** `validated_submit` now correctly blocks the network request when any validation rule fails. Previously, the submit fired unconditionally after validation.

**Fixed:** `conditional` DAP op now properly resolves DAP expressions (e.g. `bool_expr`, `transform`) as the condition — previously it only evaluated pre-resolved boolean values.

**Fixed:** `transform` DAP op now supports `length`, `is_email`, and `test_pattern` methods needed by the validator runtime.

### `JsonStore` — File-Backed Key-Value Store

Thread-safe, atomic-write JSON persistence for rapid prototyping and small-scale backends.

```python
from dars.all import *

store = JsonStore("data.json", default={"tasks": []})
store.set("tasks", [{"id": 1, "title": "Hello"}])
tasks = store.get("tasks")
store.delete("tasks")
store.clear()
```

- Atomic writes via write-to-`.tmp` then `os.replace()`
- Per-instance `threading.Lock` on all mutating operations
- Raises `ValueError` with a descriptive message on malformed JSON

### `UploadPipeline` — Server-Side File Upload Handler

Validates MIME type and file size, sanitises filenames, and saves uploads to a configurable directory.

```python
from dars.all import *

pipeline = UploadPipeline(
    upload_dir="uploads",
    allowed_types=["image/png", "image/jpeg"],
    max_size_bytes=10 * 1024 * 1024,
)
pipeline.create_endpoint(app, path="/api/upload")
```

- Returns HTTP 415 for unsupported MIME types
- Returns HTTP 413 for oversized files
- `sanitize_filename()` removes path traversal (`../`, `./`) and unsafe characters

### `SecurityHeadersMiddleware` — HTTP Security Headers

Injects five security headers into every response without overwriting existing ones.

```python
from dars.all import *

ssr.use_security_headers()
# or manually:
app.add_middleware(SecurityHeadersMiddleware, csp="default-src 'self'", hsts=True)
```

Default headers: `X-Content-Type-Options`, `X-Frame-Options`, `X-XSS-Protection`, `Referrer-Policy`, `Permissions-Policy`. Optional `Content-Security-Policy` and `Strict-Transport-Security`.

### `DarsEnv` — `.env` File Support

`DarsEnv` now loads `.env` files automatically at config load time.

```python
from dars.env import DarsEnv

DarsEnv.load()                        # loads .env silently if present
api_key = DarsEnv.get("API_KEY")      # os.environ.get with default
secret   = DarsEnv.require("SECRET")  # raises KeyError if missing
```

- Does not overwrite existing `os.environ` keys
- Strips surrounding quotes from values
- Skips blank lines and `#` comments
- Called automatically by `load_config()` before reading `dars.config.json`

### `SSRApp` — Production-Ready SSR Backend Helper

The `SSRApp` class (used in `backend/api.py`) now exposes clean methods for CORS, security headers, file uploads, and custom routes:

```python
ssr = SSRApp(dars_app, prefix="/api/ssr")
ssr.use_cors(origins=["http://localhost:4000"], credentials=True)
ssr.use_security_headers()
ssr.use_upload(upload_dir="uploads", allowed_types=["image/png"], max_size_bytes=10_485_760)

# In production, serve the exported frontend files with built-in SPA 404 fallback:
if not DarsEnv.is_dev():
    ssr.use_spa_fallback()

app = ssr.fastapi_app
```

### CLI UX Upgrades & `fullstack` Renaming

- **`dars preview` Revamp**: The `preview` command UI has been completely redesigned with a beautiful `rich` terminal UI, detailing project mode, target directories, and the backend server. It now interactively asks to start the server and automatically opens your browser. Graceful `taskkill` shutdown has been added to prevent orphaned background processes.
- **`--type fullstack`**: The `dars init --type ssr` command has been renamed to `dars init --type fullstack` to better reflect the complete SPA + SSR + API nature of the scaffolded backend.

---

# Release Notes v1.9.7

> **Hybrid Stability, Anti-Flash System & CLI UX Overhaul**

## Installation

```bash
pip install --upgrade dars-framework
```

## What's New

### Hybrid SSR/SPA Stabilization

Resolved critical race conditions and hydration bugs that affected projects using a mix of Server-Side Rendering and Single Page Application routing.

- **Cross-Route Hydration Fix**: Introduced `window.__DARS_HYDRATED_PATH__` to ensure the router only hydrates the page if the current path matches the pre-rendered content. This prevents "blank screens" or incorrect content display when deep-linking into sub-routes.
- **Static to SSR Seamless Navigation**: Resolved a JSON parsing error when navigating from a static root page to an SSR route. The lightweight SPA configuration injected into static pages now correctly resolves the backend URL, ensuring smooth hydration.
- **Native 404 Interception**: The SPA router now proactively intercepts clicks to non-existent internal routes (broken links) even when navigating from a static page, gracefully redirecting to the custom 404 component instead of triggering a raw server error.
- **Single-Source Registration**: Standardized the router configuration to ensure only one authoritative `registerConfig` call is made during the boot sequence, preventing state corruption in SPA shells.

### Anti-Flash Visibility System (`dars-ready`)

To provide a premium feel, we've implemented a robust visibility management system that hides the page during the delicate hydration phase to prevent "Flash of Unstyled Content" (FOUC).

- **`dars-ready` Attribute**: The framework now manages a `dars-ready` attribute on the root element. Visibility is automatically triggered once the runtime is ready.
- **Resilient Fallback**: Added a 2.5s safety timeout that forces the page to be visible even if a third-party script or network error hangs the hydration process, ensuring the user is never stuck with a blank screen.

### CLI UX Upgrades: `dars preview` v2

The `dars preview` command has been significantly improved to be more intuitive and configuration-aware.

- **Optional Path**: You can now run `dars preview` without any arguments. It will automatically detect your `outdir` from `dars.config.json` (falling back to `./dist`).
- **Customizable Ports**: Added `--port` / `-p` support to specify the server port. The command also respects the `"port"` setting in your project's configuration file.
- **Standardized Dev Propagation**: The `dars dev` command now more reliably propagates port settings to the underlying application process.

### Robustness & Usability

- **Input Validation**: The CLI now prevents the creation of projects, components, or pages with empty names, issuing clear warnings and re-prompting the user.
- **Improved HTML Injection**: The SPA shell exporter now uses a more resilient replacement logic for the root mounting point, handling whitespace variations introduced by different HTML formatters to ensure consistent pre-rendering.

### New Code Generation Suite (`dars generate`)

Accelerate your development workflow with the new code generation commands. Scaffold components and pages instantly with automatic project integration.

- **`dars generate component <name>`**: Quickly create new reusable FunctionComponents.
- **`dars generate page <name>`**: Scaffold new pages (**Static, SPA or SSR**) with pre-filled templates.
- **Intelligent Backend Detection**: Generating an SSR route without an existing backend will trigger a prompt to automatically scaffold the required FastAPI `/backend` infrastructure and update `dars.config.json` for you.
- **Intelligent Auto-Injection**: Use the `-y` flag (e.g., `dars g page Contact -y`) to automatically add imports and register the new page in your `main.py` file, linking it to your application instantly.

---

# Release Notes v1.9.5

> **Modular Animation Engine, Scroll Triggers & Zero-Jitter Handoffs**

## Installation

```bash
pip install --upgrade dars-framework
```

## What's New

### Modular Animation Engine (`anim.js`)

The core animation system has been completely decoupled from the monolithic `dars.min.js` runtime into a dedicated `anim.js` module. This provides a cleaner architecture, better caching, and lays the groundwork for future advanced animation plugins.

### High-Performance Scroll & Viewport Animations

Added a suite of new Web Animations API-based triggers that run autonomously on the client. These features use `IntersectionObserver` to trigger animations the exact moment an element enters the viewport.

- **`animateOnView`**: Trigger CSS keyframe animations when an element scrolls into view.
- **`staggerOnView`**: Sequence animations across multiple elements with a defined delay, triggered when the first element becomes visible.
- **`scrollProgress`**: Tie CSS properties directly to the scroll percentage of the page (e.g. fading out the hero section on scroll).
- **`runOnView` / `classOnView`**: Execute JS callbacks or toggle classes based on viewport intersection.

### Zero-Jitter WAAPI to CSS Handoff

Implemented a bulletproof handoff mechanism between the Web Animations API (WAAPI) and native CSS transitions.

**The Problem:**
Historically, using `fill: forwards` in WAAPI locks CSS properties, breaking `:hover` states. If you cancel the animation and apply inline styles, it triggers a "phantom" CSS transition, causing visual jitter (especially with matrix interpolation on 3D transforms).

**The Solution:**
The new engine uses a specialized `_setStylesWithoutTransition` helper that:

1. Temporarily disables CSS transitions using `transition: none !important`.
2. Injects the final animation frame as persistent inline styles.
3. Forces a synchronous browser reflow (`void el.offsetHeight`) to commit the changes silently.
4. Cancels the WAAPI lock and restores the original CSS transition.

**Result:** Flawless CSS `:hover` effects immediately after an entrance animation, with zero jitter or layout thrashing.

### Security Hardening (Zero-Eval Continued)

Continuing our commitment to security, the new animation triggers are built entirely without `eval()` or `new Function()`. Python payloads compile to strict JavaScript object references and IIFEs, completely mitigating dynamic string execution vulnerabilities.

### DAP Compilation & Reactivity Hardening

- **Native DAP Compilation**: Fixed a critical bug where chained animations via `sequence()` were being compiled as raw JavaScript strings, resulting in `<...dScript object...>` memory references output to the DOM. They are now correctly serialized into pure DAP JSON payloads.
- **Async Execution in `dap.js`**: `dispatch()`, `sequence()`, and `delay()` commands inside the browser runtime are now fully `async`/`await` capable. This resolves an issue where delayed actions within a sequence were firing synchronously.
- **`display: block` Layout Shift Fix**: Removed hardcoded `display: block` from core functions like `fadeIn`, `slideIn`, `scaleIn`, `dom_show`, and `dom_toggle`. They now clear the `display` style (i.e. `display: ""`), allowing inline-block elements (like Buttons) to retain their native layout without unwanted line breaks.

---

# Release Notes v1.9.4

> **Relative Import Paths for Static Deployments**

## Installation

```bash
pip install --upgrade dars-framework
```

## What's New

### Fixed: Relative Paths for Runtime Resources

All JavaScript imports inside the framework's runtime resources (`dars/exporters/web/resources/`) have been updated to use **relative paths** (e.g., `./dap.js`) instead of absolute paths (e.g., `lib/dap.js`).

**The Problem:**

When deploying a Dars application to GitHub Pages (or any host that serves from a subpath like `https://user.github.io/my-project/`), the browser resolved non-relative paths against the **host's base URL** instead of the application's directory:

```
❌  https://user.github.io/lib/dap.js         → 404
✅  https://user.github.io/my-project/lib/dap.js  → OK
```

This caused `dap.js`, `dompurify.js`, and other runtime scripts to fail loading with `404` errors on any subpath-based deployment.

**The Fix:**

All `import` and `<script src="...">` references within the exported runtime files now use `./` relative paths, ensuring correct resolution regardless of the hosting base URL:

```diff
- import { ActionProtocol } from "lib/dap.js";
+ import { ActionProtocol } from "./dap.js";
```

**Impact:**

- GitHub Pages deployments now work out of the box.
- Any static hosting behind a subpath (Vercel preview, Netlify subdirectories, etc.) is also fixed.
- No changes required to user projects — the fix is internal to the framework's exporter.

### Files Modified

- `dars/exporters/web/resources/dars.min.js` — Relative import paths
- `dars/exporters/web/resources/dap.js` — Relative import paths
- All runtime JS resources — Consistent `./` prefix for local imports

---

# Release Notes v1.9.3

> **Configurable Dev Port, Local DOMPurify & Runtime Resource Optimization**

## Installation

```bash
pip install --upgrade dars-framework
```

## What's New

### Configurable Development Port

You can now customize the port used by the `dars dev` preview server directly in your project configuration or via CLI:

- **`dars.config.json`**: Added a new `"port"` field (default: `8000`).
- **CLI Override**: Use `--port` or `-P` to override the configuration at runtime.
  ```bash
  dars dev --port 4000
  ```
- **Automatic Propagation**: The CLI now correctly propagates the port setting to the underlying application process.

### Localized Runtime Dependencies (CDN-Free)

To improve load times and reliability, especially in offline or restricted environments, we have moved core runtime dependencies from CDNs to local assets:

- **Local DOMPurify**: The framework now includes and uses a local version of `dompurify.js`.
- **Resource Management**: Core runtime resources are now managed within a dedicated `resources/` directory in the web exporter and copied to the `/lib` directory of the final export.

### Python-Native Resource Minification

The minification pipeline has been extended to ensure all runtime assets are as lean as possible:

- **`rjsmin` Integration**: All JavaScript resources, including `dompurify.js` and the Dars runtime, are now minified using the Python-native `rjsmin` during the export process.
- **Improved Build Speed**: By avoiding external tools like Vite for core library minification, we maintain a fast and stable build process.

### Runtime Architecture Improvements

- **Resource Decoupling**: The legacy `js_lib.py` has been retired in favor of a file-based resource system. This allows for better code splitting and easier maintenance of the Dars runtime components.
- **Port Detection Hardening**: Improved the `rTimeCompile` logic to reliably detect the project root and configuration, ensuring that custom settings are respected even when starting the app from different working directories.

---

# Release Notes v1.9.2

> **Documentation Corrections & Complete App Class Docstring**

## Installation

```bash
pip install --upgrade dars-framework
```

## What's New

### Standardized Component Docstrings

Fixed documentation inconsistencies across all component modules:

- **`class_name` Documentation**: Corrected to reflect that it contains **regular CSS class names** (not utility classes) for standard HTML class attributes.
- **`style` Documentation**: Updated to clarify that it contains **CSS utility classes** (Tailwind-like syntax) for convenience styling.

### Complete App Class Docstring

Added a comprehensive docstring to the `App` class with:

- Detailed description of SPA, MPA, and Desktop modes.
- Complete property documentation for all constructor parameters.
- SEO and PWA configuration details.
- Usage examples for each mode.

---

# Release Notes v1.9.1

> **Premium Utility Styles, DAP Reactivity Fixes & Documentation Overhaul**

## Installation

```bash
pip install --upgrade dars-framework
```

## What's New

### Utility Style System

We've significantly expanded the utility-first styling system to bring it closer to a better developer experience, adding many features:

- **Advanced Gradients**: Full support for multi-stop gradients using `bg-gradient-to-{dir}`, `from-{color}`, `via-{color}`, and `to-{color}`. Internally uses a modern CSS variable architecture (`--tw-gradient-stops`).
- **Ring System**: New utilities for outer rings and focus indicators: `ring`, `ring-{n}`, `ring-{color}`, `ring-opacity-{n}`, and `ring-offset-{n}`.
- **Smart Property Switching**: The `text-` prefix is now intelligent. It automatically switches between `font-size` and `color` based on the provided value (e.g., `text-xl` vs `text-indigo-500`).
- **Divide Utilities**: Added `divide-x` and `divide-y` to easily add borders between child elements.
- **New UI Utilities**: Added `accent-{color}`, `caret-{color}`, `line-clamp-{n}`, and expanded support for specific border sides (e.g., `border-t-2`, `border-x-4`).
- **Shadow Colors**: Support for colored shadows via `shadow-{color}`.

### DAP & Reactivity Hardening

- **Fixed `updateVRef` Reactivity**: Resolved a critical issue where components using `ValueRef` (via `setVRef`) were not consistently re-rendering when updated through Dars Action Protocol (DAP) scripts.

### Documentation

- **Complete Documentation**: All guides in the landing page have been restructured for better flow and clarity.
- **Standardized Docstrings**: Every core component and utility function now features a complete Python docstring, including:
  - Detailed property descriptions.
  - Standard global props list.

---

# Release Notes v1.9.0

> **Secure Action Protocol (DAP) & Zero-Eval Runtime Hardening**

## Installation

```bash
pip install --upgrade dars-framework
```

## What's New

### Definitive Removal of `new Function()`

Building on the milestone of v1.8.9, v1.9.0 achieves a 100% "Zero-Eval" runtime for all dynamic event execution.

- **Context-Aware Script Injection**: Dynamic scripts (event handlers, lifecycle hooks) are now executed via a secure script injection mechanism that natively propagates `event` and `element` (the `this` context) without using `eval()` or `new Function()`.

### Dars Action Protocol (DAP) v2: Command Registry

Introduced a centralized **Command Registry** in the browser runtime (`dars.min.js`). This moves the framework from "sending code strings" to "sending structured commands".

- **Pre-defined Operations**: All common UI tasks (navigation, state changes, modal control, DOM updates) are now registered as secure, pre-defined operations.
- **Protocol-Driven Execution**: The `dispatch(action, context)` function ensures that actions are processed as structured data objects `{op, args}`, eliminating the risk of arbitrary code execution.
- **Advanced Control Flow**: Support for sequences, delays, and conditional logic within the protocol itself.

### Expanded DAP Command Library

The browser runtime now includes a comprehensive library of registered commands, covering almost all utility functions in `utils_ds.py`:

- **Interactive Dialogs**: `alert`, `confirm` (with DAP-driven `on_ok`/`on_cancel` callbacks), and `log`.
- **Navigation & History**: `navigate`, `reload`, `history_back`, `history_forward`.
- **DOM & Visibility**: `dom_show`, `dom_hide`, `dom_toggle`, `dom_focus`, `dom_blur`, `dom_reflow`.
- **Content & Styles**: `dom_set_text`, `dom_set_html` (sanitized via DOMPurify), `dom_set_style`, `dom_set_attr`, `class_add`, `class_remove`, `class_toggle`.
- **Storage & State**: `storage_set`, `storage_remove`, `storage_clear`, and `storage_get` (with direct state-update mapping).
- **Network**: Native `fetch` support with success and error handlers.
- **VRefs**: `vref_update` and `vref_get`.

### Reliable Markdown Highlighting & Assets

Fixed several long-standing issues with Prism.js integration and global asset management:

- **SSR Highlight Consistency**: Ensured that syntax highlighting works reliably in SSR, static exports, and SPA transitions using a robust retry-based initialization and a centralized asset registry.

---

# Release Notes v1.8.11

> **Native String Concatenation & Math Fixes**

## Installation

```bash
pip install --upgrade dars-framework
```

## What's New

### Restored Native String Concatenation

Fixed a major regression in `MathExpression` where using the `+` operator aggressively coerced all operands into `parseFloat()`. This behavior broke string concatenation, resulting in `0` or `NaN` when attempting to combine strings and `ValueRef` values.

- The compiler now generates native JavaScript addition `(left + right)`.
- JavaScript handles type inference automatically: combining strings will safely concatenate them, and combining numeric values will add them.
- If strict numeric addition is required from a DOM input (which usually returns strings), developers must explicitly use `.float()` or `.int()` on the `ValueRef` (e.g. `V(".num1").float() + V(".num2").float()`).

---

# Release Notes v1.8.10

> **State V2 Reactivity Hardening & FunctionComponent Fixes**

## Installation

```bash
pip install --upgrade dars-framework
```

## What's New

### State V2 Reactivity Decoupling

The Dars runtime state manager has been decoupled from strict physical DOM bindings, enabling robust reactivity for headless and virtual components:

- **State Registry Priority**: The `change()` handler now persists new state values to the internal `__reactiveRegistry` before attempting to locate a DOM element. This ensures that virtual states update reliably even when no matching element ID exists.
- **Arithmetic State Operations**: Fixed a critical bug where `increment` and `decrement` methods would always evaluate from `0` when bound to headless states. The `startLoop()` runtime function now checks the state registry if a target element is not found, allowing seamless mathematical operations in the background.

### FunctionComponent Reactivity Fixes

Resolved multiple issues affecting `useDynamic` and reactive bindings inside `@FunctionComponent` trees:

- **Binding Export Fix**: FunctionComponent templates are now correctly pre-rendered during multi-page (`app.add_page`) generation. This ensures that all `useDynamic` bindings nested inside FunctionComponents are successfully collected and exported into the reactive Javascript bundle.
- **Runtime Generation Fix**: Repaired a syntax error in the internal reactive JavaScript generator (`_generate_reactive_bindings_js`) that caused silent failures (missing closing braces) when exporting a project containing exclusively FunctionComponent bindings without any standard built-in bindings.

---

# Release Notes v1.8.9

> **Ultimate Security & Reactivity Hardening: Removal of Eval/New Function & Native JS Compilation**

> [!IMPORTANT]
> **SECURITY ADVISORY**: v1.8.9 achieves a major milestone by removing `eval()` and `new Function()` from the core client-side runtime (`dars.min.js`). However, the web framework (as seen in certain SSR/Fullstack exports) is not yet 100% free of `new Function()` and `_executeExternalScript` for specific dynamic execution flows. This will be fully addressed in the upcoming **Dars Flight Protocol (DFP)** release.

## Installation

```bash
pip install --upgrade dars-framework
```

## What's New

### Zero Eval Runtime & Secure Script Execution

We have completely overhauled how Dars executes dynamic code in the browser.

- **Removal of Legacy Eval**: Major instances of `eval()` and `new Function()` have been eliminated from the runtime (`dars.min.js`).
- **Async IIFE Injection**: Dynamic scripts (event handlers, lifecycle hooks) are now executed via a secure, async IIFE-based script injection mechanism. This provides better scope isolation and prevents global scope pollution.
- **Native `await` Support**: You can now use `await` directly within any event handler or transformation script.

### Native JavaScript Compilation Pipeline

The `dScript` compiler is now a core framework utility, moving complex resolution logic from the browser to the build/export phase.

- **Optimized JS Emission**: Python expressions using `V()`, `MathExpression`, and `BooleanExpression` are now compiled into clean, native JavaScript code strings.
- **Consistent Serialization**: Centralized the `compile_val` logic to ensure that complex structures (lists, dicts) containing reactive objects are correctly translated into executable JS literals, resolving previous "RawJS is not serializable" warnings.

### Hardened Reactivity & Math Logic

Fixed several long-standing issues with the reactivity pipeline:

- **Smart Arithmetic vs Concatenation**: Resolved the `NaN` errors in calculators. The compiler now correctly handles the `+` operator, favoring native JS concatenation for strings and addition for numbers.
- **Template Literal Safety**: Refactored the `url()` and `transform()` helpers to use a structured concatenation model, eliminating `SyntaxError: Unexpected identifier` issues caused by nested backticks in template literals.

### Async-Aware VDOM & Lazy Hydration

The initial rendering engine (`_elFromVNode`) is now asynchronous-aware:

- **Lazy Property Resolution**: VDOM properties (text, class, style, attributes) can now be initialized with Promises. The runtime will automatically hydrate these properties as they resolve, enabling powerful async patterns during the initial render.
- **Fixed Code Injection Bugs**: Resolved the issue where raw JS code strings were occasionally rendered as text in the browser instead of being executed.

### Bug Fixes

- **Recursive Compiler**: `compile_val` now recursively handles nested collections, ensuring all parts of a complex prop are correctly compiled.
- **Fixed VRef Rendering**: Improved the `ValueRef` string representation to integrate seamlessly with the new native compiler.

---

# Release Notes v1.8.8

> **Critical Security Update: Dars Server Protocol (DSP) & SSR Hydration Fix**

> [!CAUTION]
> **SECURITY WARNING**: Versions <= v1.8.7 are considered deprecated and NOT recommended for production use. v1.8.8 addresses critical security surfaces by temporarily removing experimental Server Components. Upgrading is mandatory.

## Installation

```bash
pip install --upgrade dars-framework
```

## What's New

### Dars Server Protocol (DSP)

Introduced a new unified protocol for transmitting VDOM snapshots, component states, and reactive bindings from the server to the client. This ensures that SSR-rendered pages are hydrated with full parity to client-side renders.

### SSR Hydration & Interactivity Fixes

Resolved critical issues where reactive bindings (`useDynamic`) and `VRef` bindings were not correctly executed after initial server rendering.

- **Unified Reactivity Registry**: Client-side bindings are now registered through a centralized mechanism, preventing ID mismatches.
- **Improved SPA Routing**: The client-side router now natively supports DSP payloads, allowing seamless interactivity when navigating between SSR-rendered routes.

### [IMPORTANT] Server Components Removal

As part of security hardening, the experimental "Dars Server Components" feature (using `use_server=True`) has been removed from this version.

- Projects using this feature should transition to the standard **SSR Route** architecture, which now provides superior performance and security through the DSP.
- This removal reduces the attack surface while we work on a more robust, sandboxed implementation for future releases.

---

# Release Notes v1.8.7

> **Dars Server Components & FastAPI Integration**

## Installation

```bash
pip install --upgrade dars-framework
```

## What's New

### Dars Server Components

v1.8.7 introduces **first-class Server Components**, allowing individual components to be fully rendered on the server while maintaining client-side interactivity.

- **Simple Usage**: Just add `use_server=True` to any component inheriting from the base `Component` class.
- **Full Support**: All standard Dars components (Text, Button, Container, etc.) support server-side rendering out of the box.
- **Seamless Hydration**: Components are rendered on the backend (FastAPI) and hydrated on the client, preserving events and state.

```python
Button("Server Rendered Button", use_server=True, on_click=...)
```

### FastAPI Integration Plugin

The new version of `create_dars_app` plugin provides tight integration with FastAPI, making it easier than ever to build full-stack SSR applications.

- **Backend-Driven**: The Dars frontend is served and managed by your FastAPI backend.
- **API Co-location**: Define your API routes and your UI components in the same project structure.

### SSR Project Template

Scaffold a complete SSR project and then add Server Components support in seconds:

```bash
dars init my-app --type ssr
```

This template sets up:

- A FastAPI backend using `create_dars_app`.
- A Dars frontend configured for SSR.
- Best practices for project structure and deployment.

---

# Release Notes v1.8.6

> **Environment Management & File Upload Component**

## Installation

```bash
pip install --upgrade dars-framework
```

## What's New

### DarsEnv: Environment Awareness

New `DarsEnv` class provides a standard way to check the current environment mode:

- `DarsEnv.dev`: returns `True` during development (`dars dev`), and `False` during production builds (`dars build` / `dars export`).

This allows you to write conditional logic in your components:

```python
from dars.env import DarsEnv

Link(target="/docs" if DarsEnv.dev else "https://example.domain.com/env", text="Docs")
```

### FileUpload Component

A new `FileUpload` component is now available in `dars.components.advanced`:

- Wraps `<input type="file">` with a custom, styleable interface.
- Supports `accept`, `multiple`, and hidden input handling.
- Fully reactive `on_change` events.

```python
from dars.components.advanced import FileUpload

FileUpload(
    label="Upload Document",
    accept=".pdf",
    on_change=log("File uploaded")
)
```

---

# Release Notes v1.8.5

> **Outlet improvements + SSR lazy-load placeholders + SPA router hardening**

## Installation

```bash
pip install --upgrade dars-framework
```

## What's New

### Multiple Outlets via `outlet_id`

Nested routing now supports targeting a specific outlet in a parent layout:

- `Outlet(outlet_id="main" | "sidebar" | ...)`
- `app.add_page(..., outlet_id="...")`
- The SPA config includes `outletId` per route so the client router can mount the child route into the correct outlet.

### Optional `Outlet(placeholder=...)`

`Outlet` can render an optional placeholder while the child route region is empty (e.g. SSR lazy-load or SPA navigation).
If `placeholder` is not provided, the outlet remains empty.

### SSR lazy-load loading/error placeholders (SPA navigation)

New API:

- `app.set_loading_state(loadingComp, onErrorComp)`

Exporters and the SSR backend render these as static HTML placeholders and expose them to the SPA router.
This keeps state/events safe and avoids breaking hydration.

### Trailing slash normalization

The SPA router now treats paths with trailing slashes as equivalent:

- `/dashboard` and `/dashboard/` match the same route

This prevents incorrect 404 redirects when a user navigates to a valid route with a trailing slash.

---

# Release Notes v1.8.4

> **Python-native minification + major Utility Styles upgrade**

## Installation

```bash
pip install --upgrade dars-framework
```

## What's New

### Python-native minification by default (no Node/Bun required)

v1.8.4 upgrades the default minification pipeline to use real, battle-tested Python minifiers:

- **JavaScript**: `rjsmin`
- **CSS**: `rcssmin`

This makes builds and exports work reliably in pure-Python environments.

### Optional `viteMinify` mode preserved

If you enable `viteMinify: true` in `dars.config.json`, Dars can still use Vite/esbuild **optionally** when available.
When tools are not installed, Dars falls back to the Python minifiers automatically.

### Runtime bundle safety: `dars.min.js`

The embedded runtime bundle (`dars.min.js`) is now treated as a special case:

- It is **never** passed through Vite/esbuild (to prevent corruption / ESM `export` output).
- It is minified using **Python-only `rjsmin`**, regardless of `viteMinify`.

### Utility Styles: Arbitrary Properties (`prop-[value]`)

The utility system now supports Tailwind-like **arbitrary properties**:

```python
style="background-image-[linear-gradient(90deg,_rgba(0,0,0,.35),_#00ffcc)]"
style="padding-[calc(1rem_+_2vw)]"
style="color-[var(--brand-color)]"
style="--brand-color-[#00ffcc]"
```

Also includes background gradient support via `bg-[linear-gradient(...)]` (maps to `background-image`).

### Utility Styles: composable `filter` / `backdrop-filter` / `transform`

Multiple filter/transform utilities now **compose** instead of overwriting:

```python
style="filter-[blur(6px)] filter-[brightness(120%)]"
```

### Bug fixes for utility parsing

- Fixed `text-[#hex]` / `text-[rgba(...)]` being interpreted as `font-size` instead of `color`.
- Fixed prefix collisions like `border-top-[...]` incorrectly becoming `border-color: top-[...]`.

### LandingPage: navbar styles migrated to utility strings

The LandingPage navbar now uses `style="..."` utility strings instead of large inline style dicts,
improving consistency and providing a real-world example of the upgraded styling system.

---

# Release Notes v1.8.3

> **Critical Build Fix**

## Installation

```bash
pip install --upgrade dars-framework
```

## What's New

### Fixed production build crash: `Unexpected token 'export'`

In some environments, the JS minification pipeline (Vite/esbuild) could emit ESM output ending with `export default ...` inside `app.js`. Since exported pages load `app.js` as a classic script, browsers would fail to parse it with:

`Uncaught SyntaxError: Unexpected token 'export'`

v1.8.3 fixes this by forcing the minifier output format to **IIFE** for browser scripts, preventing ESM `export` statements from being generated during build.

---

# Release Notes v1.8.2

> **Bug Fixes & Utility System Improvements**

## Installation

```bash
pip install --upgrade dars-framework
```

## What's New

### Fixed setTimeout Promise Handling

The `setTimeout` utility function in `utils_ds.py` has been updated to properly return a Promise, enabling correct chaining with `.then()` operations. This fixes JavaScript syntax errors that occurred when using sequential animations or delayed operations.

### Enhanced Animation System

Improved the animation chaining system to handle missing DOM elements gracefully, preventing runtime errors when referenced elements don't exist in the component tree.

### Responsive Design Enhancements

Updated CSS media queries for better handling of text overflow on small screens, ensuring content remains readable across all device sizes without cutting off important information.

---

# Release Notes v1.8.1

> **Style System Optimization & SSR-Aware Registry**

## Installation

```bash
pip install --upgrade dars-framework
```

## What's New

### New Style Optimization Pipeline (Phase 1)

v1.8.1 introduces the first phase of a new **style optimization system** focused on reducing inline CSS while keeping full compatibility with Dars reactivity and dynamic operations.

- Static styles defined via `style={...}` or Tailwind-like strings in `style="..."` are now:
  - Parsed into CSS dicts by the exporter.
  - Fingerprinted and converted into generated classes: `.dars-s-<hash>`.
  - Emitted once into a central style registry instead of repeating large inline `style` blocks.
- The exporter automatically attaches the generated class to the component and clears the redundant inline style, resulting in:
  - Smaller HTML output.
  - Less DOM churn on updates.
  - Better cacheability for repeated style patterns.

The original `class_name` remains fully respected and is appended **after** the generated `dars-s-*` class, so user classes (and external CSS frameworks) retain override power.

### Central Style Registry in the HTML Head

The optimized styles are accumulated into a central registry and injected in the `<head>` as:

```html
<link rel="stylesheet" href="runtime_css.css" />
<style id="dars-style-registry">
  /* .dars-s-* rules here */
</style>
<link rel="stylesheet" href="styles.css" />
```

Order is carefully chosen so that:

- `runtime_css.css` provides the base UI tokens and default component styling.
- `#dars-style-registry` contains all extracted `.dars-s-*` rules (including those coming from `hover_style`/`active_style` phases on future releases).
- `styles.css` (hover/active styles + `app.add_global_style()` + user CSS files) comes last, ensuring user styles can override the framework-generated ones.

### Full Export Coverage: Single/Multi Page, SPA & SSR

The new style pipeline now runs consistently across all export modes:

- **Single page & multipage**:
  - `HTMLCSSJSExporter.export` collects static styles from the component tree before rendering.
  - The generated HTML includes the `#dars-style-registry` block in the head.

- **SPA export (`_export_spa`)**:
  - Each SPA route runs the same static-style collection before serializing its `html`.
  - The per-route config in `__DARS_SPA_CONFIG__` now includes a `styles` field containing the CSS for that route.
  - At runtime, the SPA router calls `_injectStyles(routeName, styles)` so that SSR/SPA navigations share the same optimized classes.

- **SSR backend (`dars.backend.ssr`)**:
  - `SSRRenderer.render_route` uses a **deep copy** of each route's root tree to avoid mutating the original components when collecting styles.
  - Static styles are extracted to `.dars-s-*` classes, and the resulting CSS is injected into the SSR HTML head using `#dars-style-registry`.
  - The SSR JSON API (`/api/ssr/<route>`) now returns a `styles` field alongside `html`, `vdom`, `events`, etc., so the SPA router can inject the same registry CSS on client-side navigations.

### Runtime & Router Adjustments

The embedded JS runtime (`dars/js_lib.py` → `DARS_MIN_JS`) has been updated to be style-optimization aware without breaking existing behavior:

- `Dars.change({ id, dynamic: true, style: {...} })` and state rules that manipulate `attrs.style` continue to write directly to `el.style[...]`.
  - They do **not** depend on an initial inline `style` attribute, so elements whose base styles were moved to `.dars-s-*` remain fully reactive.
- Class updates via `attrs.class` preserve internal `dars-*` classes (including `.dars-s-*`) and only replace user classes, ensuring the optimization never gets wiped by state changes.
- The SPA router:
  - Loads SSR route data from `/api/ssr/...` and now respects the `styles` payload from the backend.
  - Uses `_injectStyles(routeName, styles)` on every SSR navigation so that optimized classes stay active even after client-side route changes.

These changes are designed to be **backwards compatible** for projects that used only `style`/`class_name` and dynamic state. The main effect you will notice in v1.8.1 is smaller, cleaner HTML with fewer repeated inline styles, especially for static or Tailwind-like styling.

---

# Release Notes v1.8.0

> **Advanced Multimedia Components & Electron Security Baseline**

## Installation

```bash
pip install --upgrade dars-framework
```

## What's New

### New Advanced Multimedia Components: Video & Audio

v1.8.0 introduces two new first-class components in the basic library:

- `Video`: wrapper around `<video>`
- `Audio`: wrapper around `<audio>`

Both are **fully reactive** and integrate with the existing hooks system:

- `State` + `useDynamic` for:
  - `src`
  - `autoplay`
  - `muted`
  - `loop`
  - `controls`
  - `plays_inline` (Video)
- `useValue` for non-reactive initial values.
- `VRef` (setVRef/useVRef) can target `src` and other props when needed.

Example:

```python
from dars.all import *
from dars.hooks.value_helpers import V

media_state = State(
    "media",
    current_video="/media/intro.mp4",
    current_audio="/media/theme1.mp3",
    autoplay_video=False,
    muted_video=True,
    loop_audio=True,
)

@route("/", index=True)
def index():
    return Page(
        Container(
            Video(
                src=useDynamic("media.current_video"),
                poster="/media/poster.jpg",
                width="720",
                controls=True,
                autoplay=useDynamic("media.autoplay_video"),
                muted=useDynamic("media.muted_video"),
                preload="metadata",
            ),
            Button(
                "Toggle Mute",
                on_click=media_state.muted_video.set(
                    (V("media.muted_video").bool() == True).then(False, True)
                ),
            ),
            Button(
                "Toggle Autoplay",
                on_click=media_state.autoplay_video.set(
                    (V("media.autoplay_video").bool() == True).then(False, True)
                ),
            ),
            Text("Audio actual:"),
            Text(useDynamic("media.current_audio")),
            Audio(
                src=useDynamic("media.current_audio"),
                controls=True,
                loop=useDynamic("media.loop_audio"),
                preload="auto",
            ),
        )
    )
```

#### Reactive Boolean Attributes

The web exporter has been extended so that `useDynamic` bindings on boolean attributes behave correctly:

- When a `State` value changes, the runtime:
  - Adds or removes the HTML attributes: `autoplay`, `muted`, `loop`, `controls`, `playsinline`.
  - Synchronizes the corresponding JS properties on the media element (`el.autoplay`, `el.muted`, etc.).
- Dynamic markers (from `useDynamic`) no longer count as _truthy_ defaults:
  - `controls=True`, `plays_inline=True` remain active by default.
  - `autoplay`, `loop`, `muted` are off by default unless explicitly set by state or by a literal `True`.

This ensures that Video/Audio behave predictably both on initial render and during reactive updates.

### Automatic media/ Directory Copy

The HTML/CSS/JS exporter now supports a **convention-based media folder**:

- If your project root contains a `media/` directory, Dars will:
  - Recursively copy `media/` into the export `output_path`.
  - Preserve subdirectory structure.
- Any `src="/media/..."` used in `Image`, `Video` or `Audio` will point to real files in the exported build.

This makes it straightforward to ship videos, audio tracks and posters alongside your static export.

### Electron 39.2.6 Security Baseline

To keep desktop builds secure and reproducible, v1.8.0 introduces an **Electron security baseline**:

- All desktop templates and Electron scaffolds now pin Electron to `39.2.6`:
  - `dars/templates/desktop/template/backend/package.json`
  - CLI `init` desktop scaffolds and `init --update` flows.
- `dars doctor` gains version-awareness:
  - New constant `MIN_SAFE_ELECTRON = "39.2.6"`.
  - When you run `dars doctor --all --yes`, Dars will install/update Electron globally via Bun as `electron@39.2.6` and `electron-builder@latest`.
- `dars dev` for desktop projects now warns if your installed Electron is below the baseline and suggests:

  ```bash
  dars doctor --all --yes
  ```

This keeps both templates and global tooling aligned with a reviewed Electron version.

### Desktop Dev Flow Fixes (Electron + rTimeCompile)

Several quality-of-life fixes improve desktop (Electron) development:

- `App.rTimeCompile` desktop branch:
  - Stops the "Starting preview..." spinner after Electron launches.
  - Exits the method immediately when desktop mode finishes, preventing the web preview server from starting on top of Electron dev.
- `dars core/js_bridge`:
  - `electron_dev_spawn` now sets `ELECTRON_DISABLE_SECURITY_WARNINGS=true` for dev runs.
  - This suppresses the noisy _Electron Security Warning (Insecure Content-Security-Policy)_ in dev tools without touching the CSP used by the Dars runtime.

Result: smoother desktop dev cycle with clear logs and no accidental web preview server when working on Electron apps.

### Documentation Updates

- `LandingPage/documentation/markdown/components.md` now documents:
  - `Video` and `Audio` components.
  - Reactive integration with `State`, `useDynamic`, `V()` and VRefs.
  - Recommended `media/` folder convention for assets.

---
