# Environment Management (DarsEnv)

Dars provides a simple, built-in way to detect the current running environment (Development vs Production) through the `DarsEnv` class.

## Why use DarsEnv?

It is common to have logic that should only run during development (like showing debug tools, detailed logs, or specific navigation links) or only in production (like analytics scripts).

## DarsEnv Class

The `DarsEnv` class is available directly from `dars.env`:

```python
from dars.env import DarsEnv
```

### Properties

#### `DarsEnv.dev`

A boolean property that indicates if the application is running in development mode.

- **Returns `True`**: When running via `dars dev` (where bundling is disabled by default).
- **Returns `False`**: When running via `dars build` or `dars export` (production builds).

## Examples

### Conditional Rendering

You can use `DarsEnv.dev` to conditionally render components:

```python
from dars.all import *
from dars.env import DarsEnv

def MyPage():
    return Page(
        Container(
            Text("Welcome to My App"),
            
            # This link only appears in development
            Link("/debug-dashboard", "Debug Tools") if DarsEnv.dev else None,
            
            # Different footer for environments
            Text("Dev Mode: Active" if DarsEnv.dev else "Production Build")
        )
    )
```

### Conditional Configuration

You can also use it to toggle configuration values:

```python
api_url = "http://localhost:3000" if DarsEnv.dev else "https://api.myapp.com"
```

> **Note**: `DarsEnv` is initialized automatically by the Dars CLI tools. You do not need to configure it manually.
