# State Management in Dars

Dars Framework features **two powerful state management systems**, each designed for different use cases:

- **State V2** - Modern, dynamic state management for simple reactive updates
- **dState & cState** - Indexed state system for complex state machines and workflows

##Choose the Right System

| Feature | State V2 | dState/cState |
|---------|----------|---------------|
| **API Style** | Clean Pythonic | Verbose but explicit |
| **Setup** | Minimal | Requires registration |
| **State Tracking** | Dynamic | Indexed (0, 1, 2...) |
| **Auto Operations** | Built-in | Manual with Mod |
| **Event Updates** | Supported | Supported |
| **State Machines** | Limited |  Full support |
| **Cross-State Calls** | No |  Mod.call() |
| **Immutable Default** | No |  State 0 |
| **Best For** | Counters, timers, simple updates | Workflows, toggles, complex UI transitions |

---

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

# Advanced class manipulation
state.classes.set({"add": ["active", "highlight"], "remove": ["disabled"]})
```

**HTML Attributes:**
```python
state.attrs.set({"data-value": "100", "title": "Tooltip"})
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
app.rTimeCompile()
```

### When to Use State V2

** Good for:**
- Simple counters and timers
- Dynamic text/style updates
- Auto-incrementing values
- Quick prototypes
- Single-component state

** Not ideal for:**
- Complex state machines
- Multi-step workflows
- State history/undo
- Cross-component state coordination

For these cases, use **dState & cState** instead.

---

# dState & cState - Indexed State Management

Powerful indexed state system for complex UI transitions and state machines.

## Quick Start with dState

```python
from dars.all import *
from dars.core.state import dState, Mod

app = App(title="State Demo")
label = Text("0", id="Counter")
st = dState("counter", component=label, states=[0,1,2,3])

# Rules on state entry
st.cState(1, mods=[Mod.inc(label, prop='text', by=1)])
st.cState(2, mods=[Mod.dec(label, prop='text', by=1)])
st.cState(3, mods=[Mod.toggle_class(label, name='highlight', on=None)])

# Buttons to navigate
next_btn = Button("Next", on_click=st.state(goto='+1'))
prev_btn = Button("Prev", on_click=st.state(goto='-1'))
```

## Mod Operations

- `inc/dec(target, prop='text', by=1)`: increments or decrements a numeric value (textContent by default).
- `set(target, **attrs)`: sets attributes; `text` sets textContent; `html` sets innerHTML; other keys map to element attributes.
- `toggle_class(target, name, on=None)`: toggles a class; when `on` is True/False, forces add/remove.
- `append_text / prepend_text`: concatenates to textContent.

## Cross-State Calls with Mod.call

Use `Mod.call(target, state=None, goto=None)` inside a `cState` to trigger another `dState`.

`target` can be the `DarsState` instance or its name (string). Example:

```python
txt = dState("txt", id="txt1", states=[0,1])
btn = dState("btn", id="btn1", states=[0,1])

txt.cState(1, mods=[
    Mod.set("txt1", text="Bye"),
    Mod.call(btn, state=1)  # or Mod.call("btn", state=1)
])
```

## Immutable Default State (Index 0)

- State `0` is the component's default configuration (as instantiated) and is **immutable**.
- Authoring-time: `cState(0, ...)` is forbidden and raises an error.
- Runtime: switching to state `0` restores the initial DOM snapshot (attributes except `id`, plus innerHTML) and ignores any rules for state `0`.
- This guarantees that returning to `0` reverts the UI to its original state.

## Mod.set with Multiple Attributes

You can set multiple properties in one call:

```python
Mod.set("btn1", text="Don't click it", class_name="warn")
```

Event attributes accept a single script or an array of scripts (executed sequentially). Valid values are:
- InlineScript, FileScript, dScript, or plain JS strings

```python
Mod.set("btn1", on_click=[txt.state(0), dScript(code="console.log('clicked')")])
```

The runtime ensures only one dynamic listener per event is active at a time and cleans it up when returning to state `0`.

## Full HTML Replacement (Custom Components)

If you need full HTML replacement on state change:
```python
swap_btn = Button(
    "Swap",
    on_click=st.state(2, cComp=True, render=label.mod(text="SWAPPED"))
)
```

`render` accepts:
- A DeferredAttr produced by `component.mod(...)` or `component.attr(..., defer=True)`.
- A Component instance (will be rendered to HTML at event time).
- A raw HTML string.

## State Navigation Patterns

There are two main ways to trigger state changes in Dars:

### 1. Using `state.state(idx)` - Recommended

The `state.state(idx)` method is the standard way to navigate to a specific state when you have a reference to the dState object:

```python
from dars.all import *
from dars.core.state import dState

# Create a toggle button
btn = Button("Off", id="ToggleBtn")

# Define state with 2 options
toggle = dState("toggle", component=btn, states=[0, 1])

# Configure "On" state
toggle.cState(1, mods=[
    Mod.set(btn, 
        text="On",
        style={'background-color': 'green'},
        on_click=toggle.state(0)  # Use state.state() to go back
    )
])

# Initial click goes to state 1
btn.on_click = toggle.state(1)
```

**Advantages:**
- Clean and straightforward syntax
- Compile-time safety (if state object doesn't exist, Python will error)
- No runtime lookups needed
- Works in all contexts

### 2. Multi-State Cycles

```python
# Create a button that cycles through 4 states
cycle_btn = Button("State 0", id="StatusBtn")
status = dState("status", component=cycle_btn, states=[0, 1, 2, 3])

# Define each state to navigate to the next
status.cState(1, mods=[
    Mod.set(cycle_btn, text="State 1 - Loading...", on_click=status.state(2))
])
status.cState(2, mods=[
    Mod.set(cycle_btn, text="State 2 - Processing...", on_click=status.state(3))
])
status.cState(3, mods=[
    Mod.set(cycle_btn, text="State 3 - Complete!", on_click=status.state(0))
])

# Start the cycle
cycle_btn.on_click = status.state(1)
```

## Complete Interactive Example

```python
from dars.all import *
from dars.core.state import dState

app = App(title="Status Indicator")

# Create button and status text
status_btn = Button("Idle", id="StatusBtn", style={
    'padding': '12px 24px',
    'background': '#gray'
})
status_text = Text("Ready", id="StatusText")

# Define 4-state workflow
workflow = dState("workflow", component=status_btn, states=[0, 1, 2, 3])

# State 1: Loading
workflow.cState(1, mods=[
    Mod.set(status_btn, 
        text="Loading...",
        style={'background': '#blue'},
        on_click=workflow.state(2)
    ),
    Mod.set(status_text, text="Fetching data...")
])

# State 2: Processing
workflow.cState(2, mods=[
    Mod.set(status_btn,
        text="Processing...",
        style={'background': '#orange'},
        on_click=workflow.state(3)
    ),
    Mod.set(status_text, text="Analyzing results...")
])

# State 3: Complete
workflow.cState(3, mods=[
    Mod.set(status_btn,
        text="Complete!",
        style={'background': '#green'},
        on_click=workflow.state(0)  # Back to idle
    ),
    Mod.set(status_text, text="All done!")
])

# Start workflow on click
status_btn.on_click = workflow.state(1)

index = Page(Container(status_btn, status_text))
app.add_page("index", index, index=True)
```

### When to Use dState/cState

**Good for:**
- Complex state machines
- Multi-step workflows (wizards, forms)
- UI toggles with multiple states
- State history and reversion
- Cross-component state coordination

**Overkill for:**
- Simple counters
- Single property updates
- Quick prototypes
- Auto operations

For these cases, **State V2** is simpler.

---

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