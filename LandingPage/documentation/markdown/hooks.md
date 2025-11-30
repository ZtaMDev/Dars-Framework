# Hooks System

Dars Framework introduces a **Hooks system** inspired by React, enabling reactive and stateful behavior in both FunctionComponents and built-in components.

## Overview Hooks

Hooks provide a way to add reactive capabilities to your application. They enable features like:

- **Reactive state bindings** - Automatically update UI when data changes
- **State monitoring** - Watch for state changes and execute side effects
- **External state integration** - Connect components to global state

---

## useDynamic() - Reactive State Binding

The `useDynamic()` hook creates reactive bindings between external `State` objects and component properties.

### 1. Usage in Built-in Components

You can pass `useDynamic()` directly to properties of built-in components like `Text`, `Button`, `Input`, etc.

```python
from dars.all import *

# Create state
userState = State("user", name="John Doe", status="Active", is_admin=False)

# Bind directly to props
card = Container(
    # Bind text property
    Text(text=useDynamic("user.name"), style={"font-weight": "bold"}),
    
    # Bind input value
    Input(value=useDynamic("user.name"), placeholder="Edit name"),
    
    # Bind button text and disabled state
    Button(
        text=useDynamic("user.status"), 
        disabled=useDynamic("user.is_admin"), # Disables button if is_admin is True (or False depending on logic)
        on_click=userState.status.set("Clicked!")
    )
)
```

### Supported Properties

`useDynamic` supports binding to the following properties on built-in components:

| Component | Properties |
|-----------|------------|
| `Text` | `text`, `innerHTML` |
| `Button` | `text`, `disabled` |
| `Input` | `value`, `placeholder`, `disabled`, `readonly`, `required` |
| `Textarea` | `value`, `placeholder`, `disabled`, `readonly`, `required` |
| `Image` | `src`, `alt` |
| `Link` | `href`, `text` |
| `Checkbox` | `checked`, `disabled`, `required` |
| `RadioButton` | `checked`, `disabled`, `required` |
| `Select` | `disabled`, `required` |
| `Slider` | `disabled` |

Boolean attributes like `disabled` and `checked` will be toggled based on the truthiness of the state value.

### 2. Usage in FunctionComponents

You can also use `useDynamic()` within `FunctionComponent` templates to create reactive spans.

```python
@FunctionComponent
def UserCard(**props):
    return f'''
    <div {Props.id} {Props.class_name} {Props.style}>
        <h3>Name: {useDynamic("user.name")}</h3>
        <p>Status: {useDynamic("user.status")}</p>
    </div>
    '''
```

### Syntax

```python
useDynamic(state_path: str) -> DynamicBinding
```

**Parameters:**
- `state_path`: Dot-notation path to state property (e.g., `"user.name"`, `"cart.total"`)

**Returns:**
- `DynamicBinding` object that resolves to the current value during render and updates automatically when state changes.

---

## useWatch() - State Monitoring

The `useWatch()` hook allows you to monitor state changes and execute callbacks (side effects).

### Usage

The recommended way to use `useWatch` is via the `app.useWatch()` or `page.useWatch()` methods:

**Global Watchers (app.useWatch)**
```python
from dars.all import *

cartState = State("cart", count=0, total=0.0)

# Logs to console whenever cart.count changes
app.useWatch("cart.count", log("Cart updated!"))
app.useWatch("cart.total", log("Total changed"))
```

**Page-Specific Watchers (page.useWatch)**
```python
@route("/cart")
def cart_page():
    page = Page()
    
    # This watcher only runs on the cart page
    page.useWatch("cart.total", log("Total changed!"))
    
    page.add(
        Container(
            Text(useDynamic("cart.total"))
        )
    )
    return page
```

You can also use the classic syntax with `add_script`:
```python
app.add_script(useWatch("state.prop", log("Changed!")))
```

### Syntax

```python
useWatch(state_path: str, callback: Union[dScript, str, Callable]) -> Union[dScript, WatchMarker]
```

**Parameters:**
- `state_path`: Dot-notation path to state property (e.g., `"user.name"`)
- `callback`: The script or function to execute when the state changes. Can be:
    - `dScript` object (e.g., `log("Changed")`, `alert("Update")`)
    - Inline JavaScript string
    - Python callable returning a `dScript`

---

## Best Practices

**Do:**
- Use `useDynamic` for simple text/value updates.
- Use `useWatch` for side effects like logging, analytics, or complex logic.
- Use consistent state naming (e.g., `"user"`, `"cart"`).

**Don't:**
- Use with non-existent state paths.
- Nest state paths more than 2 levels deep (currently supports `stateName.property`).

---