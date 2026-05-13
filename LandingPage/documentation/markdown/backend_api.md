# Backend HTTP Utilities 

Dars Framework provides a powerful, **Pythonic system** for handling HTTP requests and API communication without writing any JavaScript. The `dars.backend` module enables you to fetch data, bind it to components, and create reactive UIs entirely in Python.

## Table of Contents

- [Quick Start with HTTP UTILS](#quick-start-with-http-utils)
- [HTTP Functions](#http-functions)
- [Data Binding with useData()](#data-binding-with-usedata)
- [JSON Utilities](#json-utilities)
- [Component Management](#component-management)

---

## Quick Start with HTTP UTILS

```python
from dars.all import *
from dars.backend import get, useData

app = App(title="API Demo")

# Create display component
user_display = Text("No data", id="user-name")
user_state = State(user_display, text="No data")

# Fetch and bind data - pure Python!
fetch_btn = Button(
    "Fetch User",
    on_click=get(
        id="userData",
        url="https://api.example.com/user/1",
        callback=user_state.text.set(useData('userData').name)
    )
)

app.set_root(Container(user_display, fetch_btn))

if __name__ == "__main__":
    app.rTimeCompile()
```

---

## HTTP Functions

The `dars.backend` module provides standard HTTP methods that return `dScript` objects:

### `get(id, url, **options)`

Performs a GET request.

```python
from dars.backend import get

# Basic GET
get_user = get(
    id="userData",
    url="https://jsonplaceholder.typicode.com/users/1"
)

# With callback
get_user = get(
    id="userData",
    url="https://api.example.com/user/1",
    callback=status_state.text.set("✅ Loaded!"),
    on_error=status_state.text.set("❌ Error!")
)
```

### `post(id, url, body, **options)`

Performs a POST request.

```python
from dars.backend import post

# POST with JSON body
create_user = post(
    id="createResult",
    url="https://api.example.com/users",
    body={"name": "John", "email": "john@example.com"},
    callback=status_state.text.set("User created!")
)
```

### Other Methods

- **`put(id, url, body, **options)`** - Update resource
- **`delete(id, url, **options)`** - Delete resource
- **`patch(id, url, body, **options)`** - Partial update
- **`fetch(id, url, method, **options)`** - Generic fetch

### Common Options

All HTTP functions accept these options:

| Option | Type | Description |
|--------|------|-------------|
| `id` | `str` | **Required**. Operation ID (NOT HTML ID) for accessing data |
| `url` | `str` | **Required**. API endpoint URL |
| `headers` | `dict` | Custom HTTP headers |
| `callback` | `dScript` | Executed on success |
| `on_error` | `dScript` | Executed on error |
| `parse_json` | `bool` | Auto-parse JSON response (default: `True`) |
| `timeout` | `int` | Request timeout in milliseconds |

---

## Data Binding with useData()

The `useData()` function provides **Pythonic access** to fetched data using dot notation:

### Basic Usage

```python
from dars.backend import useData

# Access fetched data by operation ID
user_data = useData('userData')

# Access nested properties with dot notation
user_name = useData('userData').name
user_email = useData('userData').email
user_address_city = useData('userData').address.city
```

### How It Works

1. **Operation ID**: When you call `get(id="userData", ...)`, the response is stored in `window.userData`
2. **DataAccessor**: `useData('userData')` creates a `DataAccessor` object
3. **Dot Notation**: `.name` uses `__getattr__` to create `window.userData?.name`
4. **RawJS Generation**: The `.code` property generates the JavaScript expression

### Binding to StateV2

The most powerful feature is binding API data directly to component states:

```python
from dars.all import *
from dars.backend import get, useData

# Create components and states
name_display = Text("", id="user-name")
email_display = Text("", id="user-email")

name_state = State(name_display, text="")
email_state = State(email_display, text="")

# Fetch and bind - pure Python!
fetch_button = Button(
    "Fetch User",
    on_click=get(
        id="userData",
        url="https://jsonplaceholder.typicode.com/users/1",
        # Chain multiple state updates with .then()
        callback=(
            name_state.text.set(useData('userData').name)
            .then(email_state.text.set(useData('userData').email))
        )
    )
)
```

### Chaining with `.then()`

Chain multiple operations sequentially:

```python
# Update multiple components
callback=(
    status_state.text.set("Loading...")
    .then(name_state.text.set(useData('userData').name))
    .then(email_state.text.set(useData('userData').email))
    .then(status_state.text.set("✅ Loaded!"))
)
```

---

## JSON Utilities

Helper functions for working with JSON data:

### `stringify(data, pretty=False)`

Convert data to JSON string:

```python
from dars.backend import stringify, useData

# Stringify fetched data
display_state.text.set(stringify(useData('userData'), pretty=True))

# Stringify Python objects
json_str = stringify({"name": "John", "age": 30})
```

### `parse(json_string)`

Parse JSON string:

```python
from dars.backend import parse

# Parse JSON string
data = parse('{"name": "John"}')
```

### `get_value(obj, path, default=None)`

Safely access nested values:

```python
from dars.backend import get_value, useData

# Safe nested access with default
city = get_value(useData('userData'), 'address.city', default='Unknown')
```

---

## Component Management

Create, update, and delete components dynamically at runtime:

### `createComp(target, root, position="append")`

Create a new component in the DOM:

```python
from dars.backend import createComp

# Create new component
new_text = Text("Hello!", id="new-item")
create_btn.on_click = createComp(
    target=new_text,
    root="container-id",
    position="append"  # or "prepend", "before:id", "after:id"
)
```

**Tip:** You can create a `State()` for a component before it exists using a string ID:

```python
# Create state with string ID
item_state = State("new-item", text="Hello!")

# Create component later
create_btn.on_click = createComp(
    target=Text("Hello!", id="new-item"),
    root="container-id"
)

# State works immediately!
update_btn.on_click = item_state.text.set("Updated!")
```


### `updateComp(target, **props)`

Update component properties:

```python
from dars.backend import updateComp

# Update component
update_btn.on_click = updateComp(
    "my-component-id",
    text="Updated!",
    style="text-red-500"
)
```

### `deleteComp(id)`

Remove a component from the DOM:

```python
from dars.backend import deleteComp

# Delete component
delete_btn.on_click = deleteComp("component-id")
```

---

## Best Practices

1. **Use Unique Operation IDs**: Each HTTP operation should have a unique `id` to avoid conflicts
2. **Chain Updates**: Use `.then()` to chain multiple state updates sequentially
3. **Handle Errors**: Always provide `on_error` callbacks for better UX
4. **Leverage useData()**: Use dot notation for clean, readable data access
5. **Combine with StateV2**: Bind API data directly to component states for reactive UIs

---

## API Reference Summary

### HTTP Functions
- `get(id, url, **options)` - GET request
- `post(id, url, body, **options)` - POST request
- `put(id, url, body, **options)` - PUT request
- `delete(id, url, **options)` - DELETE request
- `patch(id, url, body, **options)` - PATCH request
- `fetch(id, url, method, **options)` - Generic fetch

### Data Access
- `useData(operation_id)` - Access fetched data with dot notation
- `stringify(data, pretty=False)` - Convert to JSON string
- `parse(json_string)` - Parse JSON
- `get_value(obj, path, default=None)` - Safe nested access

### Component Management
- `createComp(target, root, position)` - Create component
- `updateComp(target, **props)` - Update component
- `deleteComp(id)` - Delete component

---

For more examples, see the test files in `tst/proj/test_http_demo.py` and `tst/proj/test_http_utils.py`.

---

## SSR Backend Setup

Dars provides a built-in `create_ssr_app` helper to easily serve your Dars application with Server-Side Rendering (SSR) using FastAPI.

### Project Structure
When you run `dars init --type ssr`, Dars creates a backend structure for you:
*   `backend/api.py`: Entry point for the FastAPI server (Default Port: 8000).
*   `backend/apiConfig.py`: Configuration helper for environment management.

### Configuration (`apiConfig.py`)
To switch between Development and Production modes, simply edit the `MODE` variable in `backend/apiConfig.py`:

```python
class DarsEnv:
    # Set this to "production" when deploying
    MODE = "development" 
    
    DEV = "development"
    BUILD = "production"
    
    # ...
```

*   **Development**: Backend runs on `localhost:8000`, Frontend on `localhost:3000`. `dars dev` proxies requests.
*   **Production**: Backend serves everything.

### Running the Backend

```bash
# Start the SSR Backend (Port 3000)
python backend/api.py
```

In a separate terminal, run the frontend dev server:

```bash
# Start Frontend Dev Server (Port 8000)
dars dev
```
