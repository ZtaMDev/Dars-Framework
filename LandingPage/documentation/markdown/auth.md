# Authentication And Security

Dars provides a production-grade, secure-by-default authentication system that is **completely isolated from the VDOM**. Tokens never touch the browser's JavaScript context — they live exclusively in HttpOnly cookies managed by the browser itself. This means even if an attacker injects malicious JS (XSS), they cannot steal session tokens.

## Table of Contents

- [Security Architecture](#security-architecture)
- [Multi-Auth: Multiple Isolated Schemes](#multi-auth-multiple-isolated-schemes)
- [Three Ways to Declare Auth](#three-ways-to-declare-auth)
- [Native Auth Endpoints](#native-auth-endpoints)
- [Building Auth Pages with Dars APIs](#building-auth-pages-with-dars-apis)
- [Middleware & Route Guards](#middleware--route-guards)
- [API Reference](#api-reference-auth)

---

## Overview

Dars Authentication provides:

- **HttpOnly Cookie-Based Sessions** — Access and refresh tokens are transported as invisible cookies; JavaScript cannot read them.
- **CSRF Protection** — Built-in `XSRF-TOKEN` cookie + header validation for all mutating requests.
- **Refresh Token Rotation** — Long-lived refresh tokens are automatically rotated on every use and can be revoked server-side.
- **Multi-Auth Support** — Run multiple independent authentication schemes in the same app, each with its own secret, session store, and scoped cookies.
- **Pure Python JWT** — Zero third-party dependencies. JWTs are signed with HMAC-SHA256 using Python's standard library.
- **Password Hashing** — PBKDF2 with SHA-256 (100,000 iterations), timing-attack resistant comparison.

---

## Security Architecture

### Token Flow

```
┌─────────────────────────────────────────────────────────┐
│                      Browser                            │
│                                                         │
│   ┌───────────────┐     Cookies (HttpOnly, Secure)      │
│   │   Dars VDOM   │ ──── dars_access_token ────────►    │
│   │   (JS/HTML)   │ ──── dars_refresh_token ───────►    │
│   │               │ ──── XSRF-TOKEN (readable) ───►     │
│   │  Cannot read  │                                     │
│   │  token values │                                     │
│   └───────────────┘                                     │
└─────────────────────────────────────────────────────────┘
              │ Automatic cookie attachment
              ▼
┌─────────────────────────────────────────────────────────┐
│                   Dars Backend (FastAPI)                 │
│                                                         │
│   /_dars/auth/login   → Issues tokens as cookies        │
│   /_dars/auth/me      → Returns user data (JSON)        │
│   /_dars/auth/refresh → Rotates tokens                  │
│   /_dars/auth/logout  → Revokes & clears cookies        │
│                                                         │
│   AuthMiddleware validates token on protected routes     │
└─────────────────────────────────────────────────────────┘
```

### Cookie Configuration

| Cookie               | HttpOnly | SameSite | Secure | Max-Age | Purpose                                            |
| -------------------- | -------- | -------- | ------ | ------- | -------------------------------------------------- |
| `dars_access_token`  | ✅       | Strict   | ✅     | 15 min  | Short-lived JWT for API access                     |
| `dars_refresh_token` | ✅       | Strict   | ✅     | 7 days  | Long-lived opaque token for token rotation         |
| `XSRF-TOKEN`         | ❌       | Strict   | ✅     | 7 days  | CSRF protection (readable by JS to send as header) |

### CSRF Protection

For cookie-based auth, Dars requires the `X-XSRF-TOKEN` header on all mutating requests (`POST`, `PUT`, `DELETE`, `PATCH`). The client reads the `XSRF-TOKEN` cookie and sends its value as the header. The `AuthMiddleware` validates the match automatically.

---

## Quick Start

### 1. Define a Verification Callback

Your callback receives `(username, password)` and returns a user dictionary or `None`:

```python
def verify_user(username, password):
    # Replace with your actual database lookup
    if username == "admin" and password == "secret":
        return {"id": "1", "username": "admin", "role": "admin"}
    return None
```

### 2. Register with the App

```python
from dars.all import *

app = App(title="My Secure App")
app.setup_auth(verify_credentials_callback=verify_user, secret="your_secret_key_here")
```

### 3. Build the Login Page

Use native Dars APIs (`useFetch`, `VRefs`, `Show`) to build the UI — no raw JavaScript needed:

```python
@route("/auth", route_type=RouteType.SSR)
def auth():
    show_login = setVRef(True, ".show-login")
    show_dashboard = setVRef(False, ".show-dashboard")
    username_sel = ".user-name"

    # Check if already logged in
    on_me_success = runSequence(
        updateVRef(".show-login", False),
        updateVRef(".show-dashboard", True),
        updateVRefFromResponse(username_sel, key="response.user.username"),
    )
    on_me_error = runSequence(
        updateVRef(".show-login", True),
    )
    fetch_me, *_ = useFetch("/_dars/auth/me", method="GET",
                             on_success=on_me_success, on_error=on_me_error)

    # Login form
    login_form = collect_form(username=V("#username"), password=V("#password"))
    validator = FormValidator({"username": [required()], "password": [required()]})

    on_login_success = runSequence(
        updateVRef(".show-login", False),
        updateVRef(".show-dashboard", True),
        updateVRefFromResponse(username_sel, key="response.user.username"),
    )
    submit_login = validator.validated_submit(
        url="/_dars/auth/login", form_data=login_form,
        on_success=on_login_success,
        on_error=runSequence(updateVRefFromResponse(".login-error", key="response.detail"))
    )

    # Logout
    fetch_logout, *_ = useFetch("/_dars/auth/logout", method="POST",
        on_success=runSequence(updateVRef(".show-dashboard", False), updateVRef(".show-login", True)))

    page = Page(
        Container(
            Show(show_login, Container(
                Input(id="username", placeholder="Username"),
                Input(id="password", placeholder="Password", type="password"),
                Text("", class_name="login-error", style="color: red;"),
                Button("Login", on_click=submit_login),
            )),
            Show(show_dashboard, Container(
                Text("Welcome, ", style="font-weight: bold;"),
                Text("", class_name="user-name"),
                Button("Logout", on_click=fetch_logout),
            )),
        )
    )
    page.add_script(fetch_me)
    return page
```

> A complete working example is available in the repository at [`/examples/FullStack-app`](https://github.com/ZtaDev/Dars-Framework/tree/main/examples/FullStack-app).

---

## Multi-Auth: Multiple Isolated Schemes

Dars allows registering **multiple independent authentication configurations**, each with its own:

- Verification callback
- Secret key
- Session manager
- Scoped cookies

Each auth scheme is identified by a unique `auth_id`. The default global scheme uses the ID `"default"`.

### How Cookies Are Scoped

| Auth ID        | Access Cookie                  | Refresh Cookie                  |
| -------------- | ------------------------------ | ------------------------------- |
| `"default"`    | `dars_access_token`            | `dars_refresh_token`            |
| `"admin"`      | `dars_access_token_admin`      | `dars_refresh_token_admin`      |
| `"auth_about"` | `dars_access_token_auth_about` | `dars_refresh_token_auth_about` |

This ensures that sessions for different auth schemes never collide. A user can be simultaneously logged in as "admin" and "guest" in different sections.

---

## Three Ways to Declare Auth

### 1. `@requires_auth` Decorator (Inline — Recommended)

The simplest way. Place it right below your `@route` decorator. It auto-registers the auth config and generates a predictable `auth_id` based on the function name:

```python
def verify_guest(username, password):
    if username == "guest" and password == "guest":
        return {"id": "g1", "username": "guest", "role": "guest"}
    return None

@route("/about", route_type=RouteType.SSR)
@requires_auth(verify_credentials_callback=verify_guest, secret="about_secret")
def about():
    # auth_id is automatically "auth_about" (from the function name)
    # Endpoints: /_dars/auth/auth_about/login, /me, /logout, /refresh
    ...
```

### 2. `Page.setup_auth()` (Component-Level)

Configure auth directly on a `Page` instance:

```python
@route("/profile", route_type=RouteType.SSR)
def profile():
    page = Page(...)
    page.setup_auth(
        verify_credentials_callback=verify_user,
        secret="profile_secret",
        auth_id="profile_auth"  # optional, auto-generated if omitted
    )
    return page
```

### 3. `App.setup_auth()` (Global)

Register a global auth scheme:

```python
app = App(title="My App")
app.setup_auth(
    verify_credentials_callback=verify_user,
    secret="global_secret",
    auth_id="default"  # optional, defaults to "default"
)
```

You can call `app.setup_auth()` multiple times with different `auth_id` values to register additional schemes.

---

## Native Auth Endpoints

When auth is configured, Dars automatically exposes the following FastAPI endpoints under `/_dars/auth/`:

### Default Auth (auth_id = `"default"`)

| Method | Path                  | Description                                   |
| ------ | --------------------- | --------------------------------------------- |
| `POST` | `/_dars/auth/login`   | Validates credentials, issues session cookies |
| `POST` | `/_dars/auth/refresh` | Rotates access token using refresh token      |
| `POST` | `/_dars/auth/logout`  | Revokes session, clears cookies               |
| `GET`  | `/_dars/auth/me`      | Returns authenticated user's data             |

### Custom Auth (e.g. auth_id = `"admin"`)

| Method | Path                        | Description                      |
| ------ | --------------------------- | -------------------------------- |
| `POST` | `/_dars/auth/admin/login`   | Login for the "admin" scheme     |
| `POST` | `/_dars/auth/admin/refresh` | Refresh for the "admin" scheme   |
| `POST` | `/_dars/auth/admin/logout`  | Logout for the "admin" scheme    |
| `GET`  | `/_dars/auth/admin/me`      | User info for the "admin" scheme |

---

## Building Auth Pages with Dars APIs

Since the frontend compiles to pure HTML/CSS/JS, you use Dars native APIs to interact with the auth system:

### Checking Session on Page Load

```python
fetch_me, *_ = useFetch(
    "/_dars/auth/me",   # or "/_dars/auth/{auth_id}/me"
    method="GET",
    on_success=runSequence(
        updateVRef(".show-dashboard", True),
        updateVRefFromResponse(".user-name", key="response.user.username"),
    ),
    on_error=runSequence(
        updateVRef(".show-login", True),
    )
)
page.add_script(fetch_me)  # runs on page load
```

### Extracting Nested JSON Fields

Use dot-notation in `updateVRefFromResponse` to extract specific fields from the JSON response:

```python
updateVRefFromResponse(".user-name", key="response.user.username")
updateVRefFromResponse(".user-role", key="response.user.role")
updateVRefFromResponse(".user-email", key="response.user.email")
```

### Login Form Submission

```python
login_form = collect_form(username=V("#username"), password=V("#password"))
validator = FormValidator({"username": [required()], "password": [required()]})

submit = validator.validated_submit(
    url="/_dars/auth/login",
    form_data=login_form,
    on_success=on_login_success,
    on_error=runSequence(updateVRefFromResponse(".error-msg", key="response.detail"))
)
```

---

## Middleware & Route Guards

### AuthMiddleware

Protects backend API routes by validating JWT cookies. Automatically detects scoped cookies from multiple auth schemes.

```python
ssr.use_auth(secret="my_secret", exclude_paths=["/_dars/auth", "/api/public"])
```

### `@requires_auth` (FastAPI Routes)

For custom FastAPI endpoints (not Dars pages), use the decorator to enforce authentication:

```python
from dars.core.auth import requires_auth

@app.get("/api/protected")
@requires_auth
async def protected_route(request: Request):
    user = request.state.user  # injected by the decorator
    return {"message": f"Hello {user['username']}"}
```

### `@requires_role` (RBAC)

```python
from dars.core.auth import requires_role

@app.get("/api/admin")
@requires_role("admin")
async def admin_only(request: Request):
    return {"message": "Admin access granted"}
```

---

## API Reference Auth

### `DarsAuth.encode_token(payload, secret, algorithm="HS256", expires_in=3600)`

Generates a signed JWT. Returns the token string.

### `DarsAuth.decode_token(token, secret, algorithm="HS256")`

Validates signature, checks expiration, returns payload dict. Raises `ValueError` on failure.

### `DarsAuth.hash_password(password)`

Returns a PBKDF2-SHA256 hash string (100,000 iterations).

### `DarsAuth.verify_password(password, hashed)`

Timing-attack resistant password verification. Returns `bool`.

### `DarsAuth.set_auth_cookies(response, access_token, refresh_token, xsrf_token, auth_id="default")`

Sets the three secure cookies with scoped names.

### `DarsAuth.clear_auth_cookies(response, auth_id="default")`

Clears scoped auth cookies.

### `App.setup_auth(verify_credentials_callback, secret, auth_id="default")`

Registers an auth configuration globally.

### `Page.setup_auth(verify_credentials_callback, secret, auth_id=None)`

Registers an auth configuration for a specific page.

### `@requires_auth` / `@requires_auth(verify_credentials_callback=..., secret=...)`

Decorator for FastAPI routes or Dars page functions. Supports both bare and parameterized forms.

### `@requires_role(role)`

Decorator for role-based access control on FastAPI routes.
