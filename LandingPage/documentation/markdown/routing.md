# SPA Routing in Dars Framework

Dars Framework 1.4.5 introduces a powerful SPA (Single Page Application) routing system that supports nested routes, layouts, and automatic 404 handling.

## Basic Routing

To create a basic SPA, you define pages and add them to your app. One page must be designated as the index.

```python
from dars.all import *

app = App(title="My SPA App")

# Create pages
home = Page(Container(Text("Home Page")))
about = Page(Container(Text("About Us")))

# Add pages to app
app.add_page(name="home", root=home, route="/", title="Home", index=True)
app.add_page(name="about", root=about, route="/about", title="About")
```

you can also use the `@route` decorator to add pages to your app.

```python
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
```

> Note: If you use the `@route` decorator, you can't add the route of the page in `app.add_page()`.

## Nested Routes & Layouts

Nested routes allow you to create layouts that persist while child content changes. This is achieved using the `parent` parameter and the `Outlet` component.

### The Outlet Component

The `Outlet` component serves as a placeholder where child routes will be rendered within a parent layout.

```python
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
```

The `Outlet` can also render an optional placeholder while the child route is still loading (SSR lazy-load or SPA navigation).
If `placeholder` is not provided, nothing is rendered.

```python
from dars.components.advanced.outlet import Outlet

dashboard_layout = Page(
    Container(
        Text("Dashboard Header"),
        Outlet(
            placeholder=Container(Text("Loading section..."))
        ),
        Text("Dashboard Footer")
    )
)
```

### Multiple Outlets (outlet_id)

You can declare multiple outlets in the same layout by giving each `Outlet` an `outlet_id`.
Child routes can then target a specific outlet via `app.add_page(..., outlet_id="...")`.

```python
from dars.components.advanced.outlet import Outlet

dashboard_layout = Page(
    Container(
        Text("Dashboard Header"),
        Container(
            Outlet(outlet_id="main"),
            Outlet(outlet_id="sidebar", placeholder=Text("Loading sidebar...")),
            style="flex gap-4"
        ),
        Text("Dashboard Footer")
    )
)
```

### Configuring Nested Routes

Use the `parent` parameter in `add_page` to define the hierarchy.

```python
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
```

If your parent layout contains multiple outlets, pass `outlet_id` in the child route to target the correct outlet:

```python
app.add_page(
    name="dashboard",
    root=dashboard_layout,
    route="/dashboard",
    title="Dashboard"
)

app.add_page(
    name="settings",
    root=settings_page,
    route="/dashboard/settings",
    title="Settings",
    parent="dashboard",
    outlet_id="main"
)
```

When you navigate to `/dashboard/settings`, Dars will render the `dashboard` layout and place the `settings` content inside the `Outlet`.

## Trailing Slashes

The SPA router normalizes paths so that trailing slashes do not create false 404s:

- `/dashboard` and `/dashboard/` are treated as the same route.
- The root path `/` remains `/`.

## 404 Handling

Dars provides robust handling for non-existent routes.

### Default 404 Page

If a user navigates to a route that doesn't exist, Dars automatically:
1. Redirects the user to `/404`.
2. Displays a built-in, clean "404 Page Not Found" error page.

### Custom 404 Page

You can customize the 404 page using `app.set_404_page()`.

```python
# Create your custom 404 page
not_found_page = Page(
    Container(
        Text("Oops! Page not found 😢", style="text-3xl"),
        Link("Go Home", href="/")
    )
)

# Register it
app.set_404_page(not_found_page)
```

Now, when a 404 occurs, users will be redirected to `/404` but will see your custom design.

## 403 Handling

Similar to 404 pages, you can define a custom 403 Forbidden page for unauthorized access to private routes.

### Default 403 Page

Dars includes a default 403 page that informs users they don't have permission to access the requested resource.

### Custom 403 Page

You can customize the 403 page using `app.set_403_page()`.

```python
# Create your custom 403 page
forbidden_page = Page(
    Container(
        Text("⛔ Access Denied", style="text-3xl text-red-500"),
        Text("You do not have permission to view this page."),
        Link("Go to Login", href="/login")
    )
)

# Register it
app.set_403_page(forbidden_page)
```

Dars will automatically redirect to `/prohibited` and show this page when a user tries to access a private route without authentication.

## Hot Reload

The development server (`dars dev`) includes an intelligent hot reload system for SPAs:

- **Automatic Detection**: The browser automatically detects changes to your Python code.
- **Smart Polling**: It checks for updates every 500ms without spamming your console logs.
- **Retry Limit**: If the server goes down, the client stops polling after 10 consecutive errors to prevent browser lag.
- **State Preservation**: When possible, navigation state is preserved across reloads.

## SEO & Metadata

Dars handles SEO automatically in Single Page Applications. The router intelligently updates the document metadata when navigating between routes.

### Using the Head Component

To control page metadata for each route, use the `Head` component:

```python
from dars.components.advanced.head import Head

@app.route("/about")
def about():
    return Page(
        Head(
            title="About Us - My App",
            description="Learn more about our company.",
            og_image="/images/about-og.jpg"
        ),
        Container(Text("About Content"))
    )
```

The router dynamically updates:
- `<title>`
- Meta tags (`description`, `keywords`, etc.)
- Open Graph tags (`og:title`, `og:type`, etc.)
- Twitter Cards

This ensures that even client-side routes display the correct information in the browser tab and when shared on social media.


---

## Route Types & Security Guards

Dars provides four route types that control rendering strategy and access control:

### RouteType Enum

| Type | Value | Description |
|---|---|---|
| `RouteType.PUBLIC` | `"public"` | Client-side rendered, no auth required. Default. |
| `RouteType.SSR` | `"ssr"` | Server-side rendered, fetched from backend on navigation. |
| `RouteType.PRIVATE` | `"private"` | Requires authentication. Not included in initial bundle. Redirects to login. |
| `RouteType.PROTECTED` | `"protected"` | Requires authentication AND specific roles/permissions. |

### Using Route Types

```python
from dars.core.route_types import RouteType

@route("/")                         # PUBLIC (default)
def home():
    return Page(Text("Home"))

@route("/dashboard", route_type=RouteType.SSR)
def dashboard():
    return Page(Text("Dashboard"))

@route("/account", route_type=RouteType.PRIVATE)
def account():
    return Page(Text("My Account"))

@route("/admin", route_type=RouteType.PROTECTED, roles=["admin"])
def admin_panel():
    return Page(Text("Admin Panel"))
```

### Route Guards

The `@guard` decorator provides fine-grained access control:

```python
from dars.core.routing import guard

@route("/premium")
@guard(requires_auth=True, roles=["premium"], redirect="/pricing")
def premium_page():
    return Page(...)
```

Or inline via the `RouteGuard` class:

```python
from dars.core.route_types import RouteGuard

@route("/enterprise", guard=RouteGuard(
    requires_auth=True,
    roles=["enterprise"],
    redirect="/contact-sales",
))
def enterprise():
    return Page(...)
```

### Custom Guard Checks

```python
@route("/beta")
@guard(
    requires_auth=True,
    custom_check=lambda user: user.get("beta_access", False),
)
def beta_page():
    return Page(...)
```

### How Guards Work

1. **Client-side**: The SPA router checks the `RouteGuard` configuration before loading a route
2. **Unauthenticated**: Redirects to `/login` (or custom `redirect` path)
3. **No matching role**: Shows 403 forbidden page
4. **Custom check fails**: Blocked without rendering

---

## Server-Side Rendering (SSR)

Dars Framework provides complete Server-Side Rendering support integrated with FastAPI, allowing you to build full-stack applications with both server-rendered and client-side pages.

### Quick Overview

SSR routes are rendered on the server before being sent to the client, providing:
- Faster initial page load
- Progressive enhancement
- Flexible architecture (mix SSR, SPA, and Static routes)

### Basic SSR Route

```python
from dars.all import *
from backend.apiConfig import DarsEnv

# Configure SSR URL
ssr_url = DarsEnv.get_urls()['backend']
app = App(title="My App", ssr_url=ssr_url)

# Define SSR route
@route("/", route_type=RouteType.SSR)
def home():
    return Page(
        Text("Welcome!", style="text-3xl font-bold"),
        Text("This page is rendered on the server!")
    )

app.add_page("home", home(), title="Home")
```

### Dual Hydration System

Dars uses a sophisticated "Dual Hydration" approach:

1. **Server Side**: Renders component to HTML and builds VDOM snapshot
2. **Client Side**: Displays server HTML immediately, then hydrates with JavaScript
3. **Result**: No flickering, instant content, full interactivity

This prevents Flash of Unstyled Content (FOUC), double rendering, and race conditions.

### Creating an SSR Project

Use the Dars CLI to scaffold a complete SSR project with FastAPI backend:

```bash
dars init my-ssr-app --type ssr
cd my-ssr-app
```

This creates a full-stack project with:
- Frontend Dars app (`main.py`)
- FastAPI backend (`backend/api.py`)
- Environment configuration
- Development and production setup

### Complete SSR Documentation

For comprehensive SSR documentation including:
- Architecture and how it works
- Development workflow
- API reference (`create_ssr_app`, `SSRRenderer`)
- Mixing SSR, SPA, and Static routes
- Deployment guide
- Advanced features (authentication, custom endpoints)
- Best practices and troubleshooting
- Real-world examples

**See the [Complete SSR Guide](#server-side-rendering-in-dars-framework)**

---
