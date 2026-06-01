# Authentication & Security

Dars provides a production-grade, secure-by-default authentication system. Tokens are transported exclusively via HttpOnly cookies — completely isolated from the VDOM/JavaScript context, making XSS-based token theft impossible.

## Table of Contents

- [Architecture Overview](#architecture-overview)
- [Quick Start](#quick-start)
- [Three Ways to Configure Auth](#three-ways-to-configure-auth)
- [Route Guards & Route Types](#route-guards--route-types)
- [Multi-Auth: Multiple Isolated Schemes](#multi-auth-multiple-isolated-schemes)
- [Building Auth Pages](#building-auth-pages)
- [Middleware Reference](#middleware-reference)
- [API Reference](#api-reference)

---

## Architecture Overview

### Token Flow

```
┌─────────────────────────────────────────────┐
│                  Browser                      │
│                                               │
│  ┌───────────────┐   Cookies (HttpOnly)      │
│  │   Dars VDOM   │ ── dars_access_token ──►  │
│  │   (JS/HTML)   │ ── dars_refresh_token ─►  │
│  │               │ ── XSRF-TOKEN (read) ──►  │
│  │  Cannot read  │                            │
│  │  token values │                            │
│  └───────────────┘                            │
└──────────────────────┬────────────────────────┘
                       │ Auto cookie attach
                       ▼
┌──────────────────────────────────────────────┐
│            Dars Backend (FastAPI)              │
│                                                │
│  /_dars/auth/{id}/login    → Issue tokens     │
│  /_dars/auth/{id}/me       → User data        │
│  /_dars/auth/{id}/refresh  → Rotate tokens    │
│  /_dars/auth/{id}/logout   → Revoke session   │
│                                                │
│  @requires_auth  → Validates JWT, injects     │
│                     request.state.user        │
└──────────────────────────────────────────────┘
```

### Cookie Configuration

| Cookie | HttpOnly | SameSite | Secure | Max-Age | Purpose |
|---|---|---|---|---|---|
| `dars_access_token` | Yes | Strict | Yes | 15 min | Short-lived JWT |
| `dars_refresh_token` | Yes | Strict | Yes | 7 days | Long-lived opaque token |
| `XSRF-TOKEN` | No | Strict | Yes | 7 days | CSRF protection |

For multi-auth, cookie names are scoped: `dars_access_token_{auth_id}`, `dars_refresh_token_{auth_id}`.

---

## Quick Start

### 1. Define a Verification Callback

The callback receives `(username, password)` and returns a user dict (must include `"id"` or `"username"`) or `None`:

```python
def verify_user(username, password):
    if username == "admin" and password == "secret":
        return {"id": "1", "username": "admin", "role": "admin"}
    return None
```

Supports both sync and async callbacks.

### 2. Register Auth with the App

```python
from dars.all import *

app = App(title="My Secure App")
app.setup_auth(
    verify_credentials_callback=verify_user,
    secret="your-secret-key-change-in-production"
)
```

### 3. Protect a Route

Use `@requires_auth` **below** `@route` for SSR/API routes that need authentication. The decorator automatically injects `request.state.user`:

```python
@route("/dashboard", route_type=RouteType.SSR)
@requires_auth
async def dashboard(request: Request):
    user = request.state.user  # injected by @requires_auth
    return Page(
        Text(f"Welcome, {user['username']}!"),
    )
```

### 4. Build a Login Page

```python
@route("/login", route_type=RouteType.SSR)
def login_page():
    login_form = collect_form(username=V("#username"), password=V("#password"))
    validator = FormValidator({"username": [required()], "password": [required()]})

    on_success = redirect_after_login("/dashboard")
    submit = validator.validated_submit(
        url="/_dars/auth/login",
        form_data=login_form,
        on_success=on_success,
        on_error=setText(".error", "Invalid credentials"),
    )

    return Page(
        Container(
            Text("Login", style="text-2xl font-bold"),
            Input(id="username", placeholder="Username"),
            Input(id="password", placeholder="Password", type="password"),
            Text("", class_name="error", style="color: red;"),
            Button("Login", on_click=submit),
        )
    )
```

---

## Three Ways to Configure Auth

### 1. `@requires_auth` Decorator (Per-Route — Recommended)

Place `@requires_auth` directly below `@route`. You can optionally pass `verify_credentials_callback` and `secret` to auto-register a custom auth scheme:

```python
def verify_guest(username, password):
    if username == "guest" and password == "guest":
        return {"id": "g1", "username": "guest", "role": "guest"}
    return None

@route("/about", route_type=RouteType.SSR)
@requires_auth(verify_credentials_callback=verify_guest, secret="about_secret")
def about():
    # Auto-registers auth config with auth_id = "auth_about"
    # Endpoints: /_dars/auth/auth_about/login, /me, /logout, /refresh
    return Page(...)
```

When used without arguments (`@requires_auth` as bare decorator), it uses the **default** auth configuration (configured via `app.setup_auth()`).

### 2. `app.setup_auth()` (Global)

Register one or more global auth configurations:

```python
app = App(title="My App")
app.setup_auth(verify_credentials_callback=verify_admin, secret="admin_secret", auth_id="admin")
app.setup_auth(verify_credentials_callback=verify_user, secret="user_secret", auth_id="default")
```

### 3. `register_auth_config()` (Programmatic)

For advanced use cases, register directly:

```python
from dars.backend.auth_routes import register_auth_config

register_auth_config(verify_callback, secret, auth_id="custom")
```

---

## Route Guards & Route Types

Dars provides two layers of route protection:

### Layer 1: Route Types (Client-Side Guards)

The `@route` decorator supports `RouteType` for client-side routing guards:

```python
from dars.core.route_types import RouteType

# Public — no auth required (default)
@route("/")

# SSR — server-side rendered, no auth
@route("/blog", route_type=RouteType.SSR)

# Private — requires authentication, redirects to login if not auth'd
@route("/account", route_type=RouteType.PRIVATE)

# Protected — requires auth + specific role
@route("/admin", route_type=RouteType.PROTECTED, roles=["admin"])
```

These guards work at the SPA router level — unauthenticated users are redirected to `/login` (or custom `redirect` path) without the protected component ever loading.

### Layer 2: `@requires_auth` (Server-Side Enforcement)

For SSR routes and API endpoints, the `@requires_auth` decorator validates the JWT on every request:

```python
from dars.core.auth import requires_auth, requires_role

# Protect any FastAPI route
@app.get("/api/protected")
@requires_auth
async def protected_route(request: Request):
    return {"user": request.state.user}

# Role-based access control
@app.get("/api/admin")
@requires_role("admin")
async def admin_only(request: Request):
    return {"message": "Admin access granted"}
```

### Combining Both Layers

For maximum security, combine client-side guards with server-side enforcement:

```python
@route("/admin", route_type=RouteType.PROTECTED, roles=["admin"])
@requires_auth(verify_credentials_callback=verify_admin, secret="admin_secret")
async def admin_panel(request: Request):
    user = request.state.user
    return Page(...)
```

---

## Multi-Auth: Multiple Isolated Schemes

Dars supports running multiple independent authentication schemes simultaneously, each with its own:

- Verification callback
- Secret key
- Session store
- Scoped cookies (identified by `auth_id` suffix)

| Auth ID | Access Cookie | Refresh Cookie |
|---|---|---|
| `"default"` | `dars_access_token` | `dars_refresh_token` |
| `"admin"` | `dars_access_token_admin` | `dars_refresh_token_admin` |
| `"auth_about"` | `dars_access_token_auth_about` | `dars_refresh_token_auth_about` |

A user can be simultaneously logged in with different identities in different sections of the same app without any session collision.

---

## Building Auth Pages

Since the frontend compiles to pure HTML/CSS/JS, you use Dars native APIs to interact with the auth system:

### Checking Session on Page Load

```python
fetch_me, *_ = useFetch(
    "/_dars/auth/me",
    method="GET",
    on_success=runSequence(
        updateVRef(".show-dashboard", True),
        updateVRefFromResponse(".user-name", key="response.user.username"),
    ),
    on_error=runSequence(updateVRef(".show-login", True)),
)
page.add_script(fetch_me)
```

For multi-auth, scope the endpoint:

```python
fetch_me, *_ = useFetch("/_dars/auth/admin/me", method="GET", ...)
```

### Login with Form Validation

```python
login_form = collect_form(username=V("#username"), password=V("#password"))
validator = FormValidator({"username": [required()], "password": [required()]})

submit = validator.validated_submit(
    url="/_dars/auth/login",
    form_data=login_form,
    on_success=redirect_after_login("/dashboard"),
    on_error=runSequence(updateVRefFromResponse(".error", key="response.detail")),
)
```

### Logout

```python
fetch_logout, *_ = useFetch("/_dars/auth/logout", method="POST",
    on_success=runSequence(updateVRef(".show-dashboard", False), updateVRef(".show-login", True)))
```

---

## Middleware Reference

### AuthMiddleware

Validates JWT on every request (except excluded paths). Injects `request.state.user`:

```python
from dars.backend.middleware import AuthMiddleware

app.add_middleware(
    AuthMiddleware,
    secret="your-secret",
    exclude_paths=["/_dars/auth", "/api/public", "/docs"],
    csrf_protection=True,
)
```

### SecurityHeadersMiddleware

Injects security headers into every response:

```python
from dars.backend.middleware import SecurityHeadersMiddleware

app.add_middleware(
    SecurityHeadersMiddleware,
    csp="default-src 'self'",
    hsts=True,
)
```

Default headers: `X-Content-Type-Options`, `X-Frame-Options`, `X-XSS-Protection`, `Referrer-Policy`, `Permissions-Policy`.

---

## API Reference

### `DarsAuth.encode_token(payload, secret, algorithm="HS256", expires_in=3600)`

JWT encoding with HMAC-SHA256. Returns token string.

### `DarsAuth.decode_token(token, secret, algorithm="HS256")`

Validate JWT, return payload dict. Raises `ValueError` on failure/expiry.

### `DarsAuth.hash_password(password)` / `DarsAuth.verify_password(password, hashed)`

PBKDF2-SHA256 password hashing (100k iterations) with timing-attack resistant comparison.

### `DarsAuth.set_auth_cookies(response, access_token, refresh_token, xsrf_token, auth_id="default")`

Sets HttpOnly secure cookies with scoped names.

### `DarsAuth.clear_auth_cookies(response, auth_id="default")`

Clears all auth cookies.

### `@requires_auth(verify_credentials_callback=None, secret=None, auth_id=None)`

Decorator for FastAPI route handlers. Validates JWT, injects `request.state.user`. Auto-registers auth config when callback and secret are provided.

### `@requires_role(role)`

Decorator for role-based access control. Requires `@requires_auth` or middleware to have set `request.state.user` first.

### `app.setup_auth(verify_credentials_callback, secret, auth_id="default", login_page="/login")`

Register a global auth configuration.

### `register_auth_config(verify_credentials_callback, secret, auth_id)`

Programmatic auth config registration.

### `get_auth_config(auth_id)`

Retrieve an auth configuration by ID.

### Native Auth Endpoints

When auth is configured, Dars automatically exposes:

| Method | Path | Description |
|---|---|---|
| `POST` | `/_dars/auth/{auth_id}/login` | Validate credentials, issue session |
| `POST` | `/_dars/auth/{auth_id}/refresh` | Rotate tokens using refresh token |
| `POST` | `/_dars/auth/{auth_id}/logout` | Revoke session, clear cookies |
| `GET` | `/_dars/auth/{auth_id}/me` | Return authenticated user data |

For the default scheme (`auth_id="default"`), the path simplifies to `/_dars/auth/login`, etc.

### Session Management

```python
from dars.backend.session import SessionManager, InMemorySessionStore

store = InMemorySessionStore()
manager = SessionManager(store)

token = manager.issue_refresh_token(user_id, payload)
session = manager.validate_refresh_token(token)
manager.revoke_refresh_token(token)
```

The `SessionStore` protocol allows custom implementations for Redis, database-backed sessions, etc.
