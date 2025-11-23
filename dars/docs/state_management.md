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
-
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

### Targeting Other Components with `updateComp`

While `this()` refers to the clicked component, you can target other components by using the `updateComp` helper from `dars.backend` (exported in `dars.all`).

```python
from dars.all import updateComp

# Read file and update a different component
btn = Button("Load to Display",
    on_click=read_text("data.txt").then(
        updateComp("display", text=RawJS(dScript.ARG))
    )
)

# Update multiple properties of another component
btn2 = Button("Style It",
    on_click=updateComp("display", 
        style={"color": "blue", "fontWeight": "bold"},
        text="Styled!"
    )
)
```

### Key Benefits

- **No State Pre-registration**: Update components directly without defining states
- **Works Everywhere**: Both desktop and web exports support dynamic updates
- **Async-Friendly**: Perfect for chaining with file operations, network requests, etc.
- **Type-Safe**: Use `RawJS` for JavaScript values, regular Python values for literals
- **Composable**: Combine with `dScript.then()` for complex workflows

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

### Difference from `this().state()`

- **`this().state(**kwargs)`**: Dynamic property updates without state tracking
  - Updates component properties directly (text, style, etc.)
  - No dState required
  - Changes are immediate and don't follow state rules
  - Use for simple, one-off updates

- **`state.state(idx)`**: Navigate to a registered dState index
  - Requires a dState to be defined for the component
  - Triggers all `cState` rules and mods for that index
  - Maintains state history and allows returning to previous states
  - Follows the complete state lifecycle (enter/exit behaviors)
  - Use for structured state machines

### Error Handling

Runtime validation throws descriptive errors:

**Example: Missing dState**
```python
btn = Button("Click me", id="MyBtn")
btn.on_click = some_state.state(1)  # Error if some_state doesn't exist
```

**Example: Invalid Index**
```python
my_state = dState("st", component=btn, states=[0, 1])
btn.on_click = my_state.state(5)  # Runtime error: index 5 doesn't exist
# Error: [Dars.goto] Index 5 out of bounds for state 'st' (valid: 0-1)
```

### Complete Interactive Example

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

### Best Practices

1. **Always use `state.state()`** when you have a reference to the dState object
2. **Avoid state 0 mutations**: State 0 is immutable and restores default values
3. **Use states 1+ for toggles**: For a toggle, use states [0, 1, 2] and toggle between 1 and 2
4. **Name states meaningfully**: Use descriptive dState names like "workflow", "toggle", "menu"
5. **Keep state machines simple**: Avoid deeply nested or overly complex state transitions