# Hooks System

Dars Framework introduces a **Hooks system** inspired by React, enabling reactive and stateful behavior in both FunctionComponents and built-in components.

## Overview Hooks

Hooks provide a way to add reactive capabilities to your application. They enable features like:

- **Reactive state bindings** - Automatically update UI when data changes
- **State monitoring** - Watch for state changes and execute side effects
- **External state integration** - Connect components to global state

---

## Important: State ID Best Practices

> [!IMPORTANT]
> When using `State` objects with hooks like `useDynamic` and `useValue`, the **state ID should NOT match any component ID** in your DOM. The state ID is a unique identifier for the state object itself, not a component.

### Why This Matters

The reactive system uses **watchers** to update components when state changes. When you create a `State` object, the ID you provide is used to register the state in the internal registry, not to identify a specific DOM element.

### Examples

**X Incorrect - State ID matches component ID:**
```python
# DON'T do this
state = State("my-button", count=0, disabled=False)
Button(id="my-button", text=useDynamic("my-button.count"))
```

In this example, both the state and the button have the ID `"my-button"`, which can cause confusion and unexpected behavior.

**✓ Correct - State has unique ID:**
```python
# DO this - give state a descriptive, unique ID
counter_state = State("counter-state", count=0, disabled=False)
Button(id="my-button", text=useDynamic("counter-state.count"))
Button(id="another-button", disabled=useDynamic("counter-state.disabled"))
```

**✓ Also Correct - Multiple components sharing same state:**
```python
# One state can control multiple components
ui_state = State("ui", count=0, is_disabled=False, message="Hello")

Container(
    Text(text=useDynamic("ui.message")),
    Button(id="btn-1", disabled=useDynamic("ui.is_disabled")),
    Button(id="btn-2", disabled=useDynamic("ui.is_disabled")),
    Text(text=useDynamic("ui.count"))
)
```

### Key Takeaways

1. **State IDs are for the state object**, not for DOM elements
2. **One state can control many components** through reactive bindings
3. **Component IDs should be unique** across your DOM
4. **State IDs should be descriptive** of what they manage (e.g., `"user-data"`, `"cart-state"`, `"ui-controls"`)

---

## useValue() - Initial Value Access

The `useValue()` hook allows you to access the **initial value** of a state property without creating a reactive binding. This is ideal for form inputs where you want to set a default value but allow the user to edit it freely.

### Basic Usage

Pass `useValue()` to component properties to set their initial value from state:

```python
from dars.all import *

userState = State("user", name="John Doe", email="john@example.com")

# Input with initial value from state (editable by user)
Input(value=useValue("user.name"))

# Textarea with initial value
Textarea(value=useValue("user.email"))
```

### Usage in FunctionComponents with Selectors

`useValue()` supports automatic selector application in FunctionComponents! When you provide a selector (class or ID), it will be automatically applied to the element where the value is used.

```python
from dars.all import *

app = App("Example of hooks")

userState = State("user", name="Jane Doe", email="jane@example.com", display="None")

@FunctionComponent
def UserForm(**props):
    return f'''
    <div {Props.id} {Props.class_name} {Props.style}>
        <input value="{useValue("user.name", ".name-input")}" />
        <input value="{useValue("user.email", "#email-field")}" />
        <span>{useValue("user.age", ".age-display")}</span>
        <span>{useDynamic("user.display")}</span>
    </div>
    '''


@route("/")
def index():
    return Page(
        UserForm(id="user-form"),
        # Extract values using V() helper with the selectors
        Button(
            "Get Name",
            on_click=userState.display.set(
                "Name: " + V(".name-input")  # Extract current value
            )
        ),

        Button(
            "Combine Values",
            on_click=userState.display.set(
                V(".name-input") + " (" + V("#email-field") + ")"
            )
        )
    )

app.add_page("index", index(), title="hooks", index=True)

if __name__ == "__main__":
    app.rTimeCompile()
```

**How it works:**
1. `useValue("user.name", ".name-input")` sets initial value "Jane Doe" and applies class `name-input` to the input
2. User can edit the value freely
3. `V(".name-input")` extracts the current value (even if modified by user)
4. Perfect for forms where you need both initial values and value extraction

**Supported selectors:**
- **Class selectors** (`.foo`) → Added to element's `class` attribute
- **ID selectors** (`#bar`) → Set as element's `id` attribute

### Difference from useDynamic

- **`useDynamic("state.prop")`**: Creates a **reactive binding**. If the state changes, the input value updates automatically.
- **`useValue("state.prop")`**: Sets the **initial value only**. If the state changes later, the input value does NOT update. This prevents overwriting user input while they are typing.

### Syntax

```python
useValue(state_path: str, selector: str = None) -> ValueMarker
```

**Parameters:**
- `state_path`: Dot-notation path to state property (e.g., `"user.name"`)
- `selector`: Optional CSS selector (class or ID) to apply to the element

**Returns:**
- `ValueMarker` object that resolves to the initial value during component rendering.

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
        disabled=useDynamic("user.is_admin"),
        on_click=userState.status.set("Clicked!")
    )
)
```

### Supported Properties

`useDynamic` and `useValue` supports binding to the following properties on built-in components:

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

The `useWatch()` hook allows you to monitor state changes and execute callbacks (side effects). It supports watching single or multiple state properties and executing one or more callbacks.

### Basic Usage

The recommended way to use `useWatch` is via the `app.useWatch()` or `page.useWatch()` methods:

**Single State Property**
```python
from dars.all import *

cartState = State("cart", count=0, total=0.0)

# Logs to console whenever cart.count changes
app.useWatch("cart.count", log("Cart updated!"))
app.useWatch("cart.total", log("Total changed"))
```

**Multiple State Properties (Array Syntax)**
```python
productState = State("product", name="Widget", price=19.99, info="")

# Watch multiple properties - callback executes when ANY of them change
app.useWatch(
    ["product.name", "product.price"],
    productState.info.set("Product: " + V("product.name") + " - $" + V("product.price"))
)
```

**Multiple Callbacks**
```python
# Execute multiple callbacks when state changes
app.useWatch(
    "cart.total",
    log("Total changed!"),
    alert("Cart updated")
)

# Combine array syntax with multiple callbacks
app.useWatch(
    ["product.name", "product.price"],
    productState.info.set("Product: " + V("product.name") + " - $" + V("product.price")),
    log("Product info updated")
)
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
useWatch(
    state_path: Union[str, List[str]], 
    *callbacks: Union[dScript, str, Callable]
) -> Union[dScript, WatchMarker]
```

**Parameters:**
- `state_path`: State property path(s) to watch. Can be:
    - Single path string (e.g., `"user.name"`)
    - List of paths (e.g., `["product.name", "product.price"]`)
- `*callbacks`: One or more callbacks to execute when state changes. Each can be:
    - `dScript` object (e.g., `log("Changed")`, `alert("Update")`)
    - State setter (e.g., `productState.info.set(...)`)
    - Inline JavaScript string
    - Python callable returning a `dScript`

**Behavior:**
- When using an array of state paths, the callback(s) execute when **any** of the watched properties change
- Multiple callbacks execute in the order they are provided
- Callbacks can access current state values using `V()` helper

---

## Pythonic Value Helpers

Dars provides a set of helpers to make working with DOM values and reactive state completely Pythonic, eliminating the need for raw JavaScript.

### V() - Value Reference

The `V()` helper allows you to extract values from **DOM elements** (via CSS selectors) or **reactive state** (via state paths).

#### CSS Selectors (DOM Elements)

```python
from dars.all import *

# Select by ID
V("#myInput")

# Select by Class
V(".myClass")

```

#### State Paths (Reactive State)

**New in v1.5.8**: `V()` now supports extracting values directly from reactive state created by `useDynamic()`:

```python
# Extract from reactive state
V("cart.total")      # Gets current value of cart.total
V("user.name")       # Gets current value of user.name
V("product.price")   # Gets current value of product.price
```

**How it works:**
- `V("cart.total")` finds the reactive element created by `useDynamic("cart.total")`
- Reads its current `textContent` value
- Perfect for combining reactive state with calculations

#### Transformations

You can chain transformation methods to process values before using them:

```python
# String transformations
V("#name").upper()   # "JOHN"
V("#name").lower()   # "john"
V("#name").trim()    # Remove whitespace

# Numeric transformations (required for math operations!)
V("#age").int()      # 25 (integer)
V("#price").float()  # 19.99 (float)
V("cart.total").float()  # Extract state value as float
```

#### Operations

`ValueRef` objects support Python operators with **important validation**:

**String Concatenation (Always Allowed)**
```python
# Concatenation works without transformations
state.fullname.set(V("#first") + " " + V("#last"))
message = "Total: $" + V("cart.total")
```

**Arithmetic Operations (Require Numeric Transformations)**

**New in v1.5.8**: Arithmetic operators (`*`, `/`, `-`, `%`, `**`) now **require** `.int()` or `.float()` transformations to prevent accidental string concatenation:

```python
# CORRECT - With numeric transformations
state.total.set(V("#price").float() * V("#qty").int())
state.age.set(V("#age").int() + 10)
discount = V("product.price").float() * 0.9

# CORRECT - Combining DOM and state values
productState.total.set(
    V(".qty-input").int() * V("product.price").float()
)

# ERROR - Without transformations
state.total.set(V("#price") * V("#qty"))
# TypeError: Multiplication requires numeric transformation.
#            Use V('#price').int() or V('#price').float() before multiplying.
```

**Supported Operators:**
- `+` - Addition/Concatenation (always allowed)
- `*` - Multiplication (requires `.int()` or `.float()`)
- `/` - Division (requires `.int()` or `.float()`)
- `-` - Subtraction (requires `.int()` or `.float()`)
- `%` - Modulo (requires `.int()` or `.float()`)
- `**` - Power (requires `.int()` or `.float()`)

#### Complete Example

```python
from dars.all import *

app = App("Shopping Cart")

# Reactive state
cartState = State("cart", total=0.0)
productState = State("product", name="Widget", price=19.99, quantity=1)

@FunctionComponent
def ProductCard(**props):
    return f'''
    <div {Props.id} {Props.class_name} {Props.style}>
        <!-- Reactive display -->
        <h3>{useDynamic("product.name")}</h3>
        <p>Price: ${useDynamic("product.price")}</p>
        
        <!-- Editable quantity with selector -->
        <input type="number" 
               value="{useValue("product.quantity", ".qty-input")}"
               min="1" />
        
        <!-- Reactive total -->
        <p>Total: ${useDynamic("cart.total")}</p>
    </div>
    '''

@route("/")
def index():
    return Page(
        ProductCard(id="product-card", name="Milk", price=100, quantity=2, total=0),
        
        # Calculate: DOM input × State value
        Button("Calculate Total", on_click=cartState.total.set(
            V(".qty-input").int() * V("product.price").float()
        )),
        
        # String concatenation (no transformation needed)
        Button("Show Info", on_click=productState.name.set(
            "Product: " + V("product.name") + " - $" + V("product.price")
            )
        )
    )

app.add_page("index", index(), title="Product", index=True)

# Watch for changes
app.useWatch("cart.total", log("Cart total changed!"))

if __name__ == "__main__":
    app.rTimeCompile()
```

### url() - URL Builder

The `url()` helper constructs dynamic URLs by interpolating `ValueRef` objects into a template string.

```python
# Generates: https://api.example.com/users/123/profile
fetch(
    url("https://api.example.com/users/{id}/profile", id=V("#userId"))
)

# With state values
fetch(
    url("/api/products/{id}", id=V("product.id"))
)

# Mixed
fetch(
    url("/api/{resource}/{id}", 
        resource="users", 
        id=V("#userId"))
)
```

**Note:** Use standard Python format string syntax `{key}` for placeholders.

---

## Best Practices

**Do:**
- Use `useDynamic` for simple text/value updates.
- Use `useWatch` for side effects like logging, analytics, or complex logic.
- Use `useValue` with selectors for form inputs that need value extraction.
- Use consistent state naming (e.g., `"user"`, `"cart"`).
- Always use `.int()` or `.float()` before arithmetic operations with `V()`.

**Don't:**
- Use with non-existent state paths.
- Nest state paths more than 2 levels deep (currently supports `stateName.property`).
- Use arithmetic operators without numeric transformations.

---