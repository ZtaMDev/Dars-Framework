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

When you navigate to `/dashboard/settings`, Dars will render the `dashboard` layout and place the `settings` content inside the `Outlet`.

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
        Text("Oops! Page not found 😢", style={"fontSize": "32px"}),
        Link("Go Home", href="/")
    )
)

# Register it
app.set_404_page(not_found_page)
```

Now, when a 404 occurs, users will be redirected to `/404` but will see your custom design.

## Hot Reload

The development server (`dars dev`) includes an intelligent hot reload system for SPAs:

- **Automatic Detection**: The browser automatically detects changes to your Python code.
- **Smart Polling**: It checks for updates every 500ms without spamming your console logs.
- **Retry Limit**: If the server goes down, the client stops polling after 10 consecutive errors to prevent browser lag.
- **State Preservation**: When possible, navigation state is preserved across reloads.
