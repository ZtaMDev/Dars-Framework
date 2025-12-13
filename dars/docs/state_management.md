# State Management in Dars

Dars Framework features **powerful state management systems**, designed for different use cases:

# State V2 - Dynamic State Management

Modern, Pythonic state management for reactive UIs.

## Quick Start

```python
from dars.all import *

# Create a component
display = Text("0", id="counter")

# Create state
counter = State(display, text=0)

# Use reactive properties
increment_btn = Button("Increment", on_click=counter.text.increment(by=1))
decrement_btn = Button("Decrement", on_click=counter.text.decrement(by=1))
reset_btn = Button("Reset", on_click=counter.reset())
```

## Core Concepts

### State Class

The `State` class wraps a component and provides reactive property access.

```python
from dars.all import State

display = Text("0", id="counter")
counter_state = State(display, text=0)
```

**Constructor Parameters:**
- `component`: The component to manage (can be a component object or string ID)
- `**default_props`: Default property values (e.g., `text=0`, `style={...}`)

### State with String IDs (for Dynamic Components)

`State()` can accept either a component object or a string ID. This is useful for components created dynamically:

```python
from dars.all import *
from dars.backend import createComp

# Traditional: State with component object
existing_text = Text("0", id="counter")
existing_state = State(existing_text, text=0)

# New: State with string ID (for components created later)
dynamic_state = State("dynamic-counter", text=0)

# Create the component later
create_btn.on_click = createComp(
    target=Text("0", id="dynamic-counter"),
    root="container-id"
)

# State works even though component was created after state!
increment_btn.on_click = dynamic_state.text.increment(by=1)
```

**Use Cases:**
- Components created with `createComp()`
- Dynamically generated UIs
- Conditional component rendering
- Server-side rendered components


### Reactive Properties

Access component properties through the state object to get reactive operations:

```python
# Increment/decrement numeric properties
counter.text.increment(by=1)
counter.text.decrement(by=2)

# Set property values
counter.text.set(value=100)

# Auto operations (continuous)
counter.text.auto_increment(by=1, interval=1000)  # +1 every second
counter.text.auto_decrement(by=1, interval=500)   # -1 every 500ms
counter.text.stop_auto()  # Stop auto operations
```

### Reset to Defaults

The `reset()` method restores all properties to their initial values:

```python
state = State(display, text=0, style={"color": "blue"})

# ... user modifies the component ...

# Reset everything back to initial state
reset_btn.on_click = state.reset()
```

## Reactive Operations

### Increment and Decrement

```python
# Increment by 1 (default)
button.on_click = counter.text.increment()

# Increment by custom amount
button.on_click = counter.text.increment(by=5)

# Decrement (negative increment)
button.on_click = counter.text.decrement(by=1)
# OR
button.on_click = counter.text.increment(by=-1)
```

```python
button.on_click = counter.text.set(value=0)
```

### All Property Types Supported

State V2 supports updating **all component properties**, not just text:

**Text Content:**
```python
state.text.set("New text")
```

**HTML Content:**
```python
state.html.set("<strong>Bold text</strong>")
```

**CSS Styles:**
```python
state.style.set({"color": "red", "fontSize": "24px"})
```

**CSS Classes:**
```python
# Set class name
state.class_name.set("active")
```

**Event Handlers:**
```python
# Update event handler dynamically
state.update(on_click=alert("New handler!"))

# Or with dScript
from dars.scripts.dscript import dScript
state.update(on_click=dScript("console.log('clicked')"))
```

**Multiple Properties at Once:**
```python
state.update(
    text="Updated!",
    class_name="success",
    style={"color": "green"},
    on_click=alert("Done!")
)
```

### Auto Operations


Auto operations create continuous reactive updates:

```python
# Auto-increment timer
timer = State(display, text=0)

start_btn.on_click = timer.text.auto_increment(by=1, interval=1000)
stop_btn.on_click = timer.text.stop_auto()
```

**With Limits:**
```python
# Auto-increment up to 100
timer.text.auto_increment(by=1, interval=1000, max=100)

# Auto-decrement down to 0
countdown.text.auto_decrement(by=1, interval=1000, min=0)
```

## Backend Integration with useData()

State V2 integrates seamlessly with Dars backend HTTP utilities for reactive API-driven UIs:

```python
from dars.all import *
from dars.backend import get, useData

# Create components
user_name = Text("", id="user-name")
user_email = Text("", id="user-email")

# Create states
name_state = State(user_name, text="")
email_state = State(user_email, text="")

# Fetch and bind API data - pure Python!
fetch_btn = Button(
    "Load User",
    on_click=get(
        id="userData",
        url="https://api.example.com/users/1",
        # Access nested data with dot notation
        callback=(
            name_state.text.set(useData('userData').name)
            .then(email_state.text.set(useData('userData').email))
        )
    )
)
```

**Key Features:**
- **`useData('id')`** - Access fetched data by operation ID
- **Dot notation** - `useData('userData').name` accesses nested properties
- **`.then()` chaining** - Chain multiple state updates sequentially
- **No JavaScript** - Everything is pure Python

## Complete Example

```python
from dars.all import *

app = App("State V2 Demo")

# Timer display
timer_display = Text("0", id="timer", style={"font-size": "36px"})
timer = State(timer_display, text=0)

# Status display
status = Text("Paused", id="status")
status_state = State(status, text="Paused", class_name="paused")

# Control buttons
start_btn = Button("Start",
    on_click=timer.text.auto_increment(by=1, interval=1000)
)
stop_btn = Button("Stop", 
    on_click=[
        timer.text.stop_auto(),
        status_state.update(text="Paused", class_name="paused")
    ]
)
reset_btn = Button("Reset",
    on_click=[
        timer.text.stop_auto(),
        timer.reset(),
        status_state.reset()
    ]
)

page = Page(Container(timer_display, status, start_btn, stop_btn, reset_btn))
app.add_page("index", page, index=True)

if __name__ == "__main__":
    app.rTimeCompile()
```

## Dynamic State Updates & `this()`

Dars introduces dynamic state updates, allowing you to modify component properties directly without pre-registering state indices.

### `this()` helper

The `this()` helper allows a component to refer to itself in an event handler and apply updates dynamically.

```python
from dars.core.state import this

btn = Button("Click me", on_click=this().state(text="Clicked!", style={"color": "red"}))
```

Supported dynamic properties:
- `text`: Update text content.
- `html`: Update inner HTML.
- `style`: Dictionary of CSS styles.
- `attrs`: Dictionary of attributes.
- `classes`: Dictionary with `add`, `remove`, or `toggle` (single string or list of strings).

```python
this().state(
    text="Updated",
    style={"backgroundColor": "#f0f0f0"},
    classes={"add": ["active"], "remove": ["inactive"]}
)
```

### Using Raw JavaScript Values (`RawJS`)

You can pass raw JavaScript variables to dynamic updates using `RawJS`. This is particularly useful when:
- Chaining scripts where a previous script returns a value
- Working with async operations like file reading
- Using `dScript.ARG` to reference values from previous scripts

```python
from dars.scripts.dscript import RawJS, dScript

# Using dScript.ARG placeholder for chained values
this().state(text=RawJS(dScript.ARG))

# Using custom JavaScript expressions
this().state(text=RawJS("someVar + ' processed'"))
```

---

## Best Practices

### Choose State V2 When:
- Building simple counters or timers
- Need auto-increment/decrement
- Want quick reactive updates
- Working with single components

### Choose dState/cState When:
- Building complex state machines
- Need immutable default state (state 0)
- Require cross-state calls
- Managing multi-step workflows

### Use `this()` When:
- Don't need state tracking
- Making one-off updates
- Working with async operations
- Targeting the clicked element