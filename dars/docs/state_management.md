# State management in Dars (dState, cState, goto, mods)

This document describes the new state system available in Dars 1.1.9.

- dState(name, component|id, states): declares a state tied to a DOM target (component id).
- state(idx=None, goto=None, cComp=False, render=None): triggers a state change from Python by producing a JS inline script.
- cState(idx, mods=[...]): declares rules to execute when entering a state.
- Mod helpers: inc, dec, set, toggle_class, append_text, prepend_text.
- goto: absolute (e.g. 2) or relative ("+1", "-1") state jumps.


## Quick start with states

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

## Mod operations

- inc/dec(target, prop='text', by=1): increments or decrements a numeric value (textContent by default).
- set(target, **attrs): sets attributes; `text` sets textContent; `html` sets innerHTML; other keys map to element attributes.
- toggle_class(target, name, on=None): toggles a class; when `on` is True/False, forces add/remove.
- append_text / prepend_text: concatenates to textContent.

## Cross-state calls with Mod.call

- Use `Mod.call(target, state=None, goto=None)` inside a `cState` to trigger another `dState`.
- `target` can be the `DarsState` instance or its name (string). Example:

```python
txt = dState("txt", id="txt1", states=[0,1])
btn = dState("btn", id="btn1", states=[0,1])

txt.cState(1, mods=[
    Mod.set("txt1", text="Bye"),
    Mod.call(btn, state=1)  # or Mod.call("btn", state=1)
])
```

## Immutable default state (index 0)

- State `0` is the component's default configuration (as instantiated) and is immutable.
- Authoring-time: `cState(0, ...)` is forbidden and raises an error.
- Runtime: switching to state `0` restores the initial DOM snapshot (attributes except `id`, plus innerHTML) and ignores any rules for state `0`.
- This guarantees that returning to `0` reverts the UI to its original state.

## Mod.set now supports multiple attributes and event arrays

- You can set multiple properties in one call, e.g.:

```python
Mod.set("btn1", text="Don't click it", class_name="warn")
```

- Event attributes accept a single script or an array of scripts (executed sequentially). Valid values are:
  - InlineScript, FileScript, dScript, or plain JS strings

```python
Mod.set("btn1", on_click=[txt.state(0), dScript(code="console.log('clicked')")])
```

- The runtime ensures only one dynamic listener per event is active at a time and cleans it up when returning to state `0`.

## Full HTML replacement (custom components)

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

## Runtime behavior

- At export time, state declarations are embedded in the page as a bootstrap JSON.
- The runtime (dars.min.js) registers states with: id, states, current index, and optional rules.
- `change({...})` resolves `goto`, updates `current`, applies `rules[<state>].mods` and optional `rules[<state>].goto` (single hop), then dispatches a `CustomEvent('dars:state', ...)`.

## Best practices

- Keep the label text purely numeric if you plan to use `inc/dec` on `text`.
- Use `goto` in rules to avoid infinite accumulation when staying at the same state.
- Prefer `mods` for small changes; use `cComp=True` only when you need full HTML replacement.

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

### Complete Example: File Reading with Dynamic Updates

```python
from dars.all import *
from dars.desktop import read_text, write_text

# Display component that will show file content
display = Text("No file loaded", id="display")

# Button that reads file and updates display with content
read_btn = Button("Load File", 
    on_click=read_text("data.txt").then(
        this().state(text=RawJS(dScript.ARG))
    )
)

# Button that writes file and updates its own text
write_btn = Button("Save File",
    on_click=write_text("output.txt", "Hello Dars!").then(
        this().state(text="Saved!", style={"color": "green"})
    )
)

# Counter with increment using Mod
counter = Text("0", id="count")
inc_btn = Button("+1", on_click=this().state(text=Mod.inc("count")))

app = App(title="Dynamic Updates Demo", desktop=True)
app.set_root(Container(display, read_btn, write_btn, counter, inc_btn))
```

### Targeting Other Components

While `this()` refers to the clicked component, you can target other components by using a manual update helper:

```python
def update_component(target_id, **kwargs):
    """Update a specific component by ID"""
    import json
    from dars.scripts.dscript import RawJS
    
    parts = [f"id: '{target_id}'", "dynamic: true"]
    for k, v in kwargs.items():
        if isinstance(v, RawJS):
            parts.append(f"{k}: {v.code}")
        else:
            parts.append(f"{k}: {json.dumps(v)}")
    payload = ", ".join(parts)
    return dScript(code=f"if(window.Dars && window.Dars.change) window.Dars.change({{{payload}}});")

# Read file and update a different component
btn = Button("Load to Display",
    on_click=read_text("data.txt").then(
        update_component("display", text=RawJS(dScript.ARG))
    )
)
```

### Key Benefits

- **No State Pre-registration**: Update components directly without defining states
- **Works Everywhere**: Both desktop and web exports support dynamic updates
- **Async-Friendly**: Perfect for chaining with file operations, network requests, etc.
- **Type-Safe**: Use `RawJS` for JavaScript values, regular Python values for literals
- **Composable**: Combine with `dScript.then()` for complex workflows

---

## Self-Navigation with `this().goto()`

The `this().goto(idx)` method enables a component to navigate its own `dState` to a specific index. This creates self-contained interactive components that manage their own state transitions.

### Basic Usage

```python
from dars.all import *
from dars.core.state import dState, this

# Create a toggle button
btn = Button("Off", id="ToggleBtn")

# Define state with 2 options
toggle = dState("toggle", component=btn, states=[0, 1])

# Configure "On" state
toggle.cState(1, mods=[
    Mod.set(btn, 
        text="On",
        style={'background-color': 'green'},
        on_click=this().goto(0)  # Go back to state 0
    )
])

# Initial click goes to state 1
btn.on_click = this().goto(1)
```

### Difference from `this().state()`

- **`this().state(**kwargs)`**: Dynamic property updates without state tracking
  - Updates component properties directly (text, style, etc.)
  - No dState required
  - Changes are immediate and don't follow state rules

- **`this().goto(idx)`**: Navigate to a registered dState index
  - Requires a dState to be defined for the component
  - Triggers all `cState` rules and mods for that index
  - Maintains state history and allows returning to previous states
  - Follows the complete state lifecycle (enter/exit behaviors)

### Multi-State Navigation

```python
# Create a button that cycles through 4 states
cycle_btn = Button("State 0", id="StatusBtn")
status = dState("status", component=cycle_btn, states=[0, 1, 2, 3])

# Define each state to navigate to the next
status.cState(1, mods=[
    Mod.set(cycle_btn, text="State 1 - Loading...", on_click=this().goto(2))
])
status.cState(2, mods=[
    Mod.set(cycle_btn, text="State 2 - Processing...", on_click=this().goto(3))
])
status.cState(3, mods=[
    Mod.set(cycle_btn, text="State 3 - Complete!", on_click=this().goto(0))
])

# Start the cycle
cycle_btn.on_click = this().goto(1)
```

### Requirements

1. **dState must be defined**: The component must have a `dState` registered with it
2. **Valid index**: The index must exist in the `dState.states` array (0 to length-1)
3. **Component ID**: The component must have an `id` attribute

### Error Handling

`this().goto()` performs runtime validation and throws descriptive errors:

**Error: No dState found**
```python
# This will error - button has no dState
btn = Button("Click me", id="MyBtn", on_click=this().goto(1))
# Console: [Dars.goto] No dState found for component MyBtn. Define a dState for this component first.
```

**Error: Index out of bounds**
```python
btn = Button("Click me", id="MyBtn")
state = dState("btn_state", component=btn, states=[0, 1])  # Only 2 states
btn.on_click = this().goto(5)  # Index 5 doesn't exist!
# Console: [Dars.goto] Index 5 out of bounds for state 'btn_state' (valid: 0-1)
```

All errors are logged to the browser console and thrown as JavaScript errors. Open the browser console (F12) to see detailed error messages.

### Complete Example: Interactive Status Indicator

```python
from dars.all import *

app = App(title="Status Demo")

# Status indicator that changes based on user interaction
status_btn = Button("Idle", id="StatusBtn", style={
    'padding': '16px 32px',
    'font-size': '18px',
    'border-radius': '8px'
})

# Define 4 states: Idle, Active, Warning, Error
status_state = dState("status", component=status_btn, states=[0, 1, 2, 3])

# Active state (green)
status_state.cState(1, mods=[
    Mod.set(status_btn,
        text="✓ Active",
        style={'background-color': '#4CAF50', 'color': 'white'},
        on_click=this().goto(2)
    )
])

# Warning state (orange)
status_state.cState(2, mods=[
    Mod.set(status_btn,
        text="⚠ Warning",
        style={'background-color': '#FF9800', 'color': 'white'},
        on_click=this().goto(3)
    )
])

# Error state (red)
status_state.cState(3, mods=[
    Mod.set(status_btn,
        text="✗ Error",
        style={'background-color': '#F44336', 'color': 'white'},
        on_click=this().goto(0)
    )
])

# Initial click starts the sequence
status_btn.on_click = this().goto(1)

page = Page(Container(status_btn))
app.add_page("index", page, index=True)
app.rTimeCompile()
```

### Best Practices

1. **Use for Sequential States**: `goto()` is ideal for multi-step processes, wizards, or state machines
2. **Combine with Mods**: Use `Mod.set()` in `cState` to update visual appearance and behavior for each state
3. **Debug with Console**: Always check browser console for `goto()` errors during development
4. **Document States**: Comment your state definitions to explain what each index represents
5. **Validate Indices**: Ensure all `goto()` calls use valid indices from your states array