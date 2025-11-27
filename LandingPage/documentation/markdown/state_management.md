# State Management in Dars

Dars Framework features a modern, state management system that makes building reactive UIs simple and intuitive.

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
- `component`: The component to manage
- `**default_props`: Default property values (e.g., `text=0`, `style={...}`)

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

### Set Value

```python
button.on_click = counter.text.set(value=0)
```

### Auto Operations

Auto operations create continuous reactive updates:

```python
# Auto-increment timer
timer = State(display, text=0)

start_btn.on_click = timer.text.auto_increment(
    by=1,           # Increment amount
    interval=1000,  # Every 1 second
    max=60          # Optional: stop at max value
)

stop_btn.on_click = timer.text.stop_auto()
```

**Parameters:**
- `by`: Amount to increment/decrement (default: 1)
- `interval`: Milliseconds between updates (default: 1000)
- `max`: Optional maximum value (auto-stops when reached)
- `min`: Optional minimum value (auto-stops when reached)

## Complete Examples

### Interactive Counter

```python
from dars.all import *

app = App("Counter Demo")

# Create display
counter_display = Text("0", id="counter", style={
    "font-size": "48px",
    "color": "#2563eb"
})

# Create state
counter = State(counter_display, text=0)

# Control buttons
inc_btn = Button("+1", on_click=counter.text.increment(by=1))
dec_btn = Button("-1", on_click=counter.text.decrement(by=1))
reset_btn = Button("Reset", on_click=counter.reset())

# Add animation
pulse_btn = Button("Pulse", on_click=pulse(id="counter", scale=1.2))

page = Page(Container(counter_display, inc_btn, dec_btn, reset_btn, pulse_btn))
app.add_page("index", page, index=True)
```

### Auto-Incrementing Timer

```python
from dars.all import *

app = App("Timer Demo")

# Timer display
timer_display = Text("0", id="timer", style={
    "font-size": "36px",
    "color": "#059669"
})

# Timer state
timer = State(timer_display, text=0)

# Control buttons
start_btn = Button("Start", on_click=timer.text.auto_increment(by=1, interval=1000))
stop_btn = Button("Stop", on_click=timer.text.stop_auto())
reset_btn = Button("Reset", on_click=timer.reset())

page = Page(Container(timer_display, start_btn, stop_btn, reset_btn))
app.add_page("index", page, index=True)
```

## Dynamic Updates with `this()`

The `this()` helper allows components to update themselves dynamically:

```python
from dars.all import this

# Update self on click
button = Button("Click me", 
    on_click=this().state(
        text="Clicked!",
        style={"background-color": "green"}
    )
)

# Chain with animations
button = Button("Animate", 
    on_click=fadeIn(id="box").then(
        this().state(text="Animation complete!")
    )
)
```

**Supported properties:**
- `text`: Update text content
- `html`: Update inner HTML
- `style`: Dictionary of CSS styles
- `attrs`: Dictionary of HTML attributes
- `classes`: Dictionary with `add`, `remove`, or `toggle` operations

### Using RawJS for Dynamic Values

```python
from dars.scripts.dscript import RawJS, dScript

# Use JavaScript expressions
button.on_click = this().state(
    text=RawJS("new Date().toLocaleTimeString()")
)

# Chain with dScript results
read_btn.on_click = read_file("data.txt").then(
    this().state(text=RawJS(dScript.ARG))
)
```

## Animation Integration

State V2 works seamlessly with the animation system:

```python
from dars.all import *

display = Text("Hello", id="message")
state = State(display, text="Hello")

# Trigger animation on state change
button.on_click = sequence(
    state.text.set(value="Loading..."),
    fadeOut(id="message", duration=300),
    fadeIn(id="message", duration=300),
    state.text.set(value="Complete!")
)
```

## Best Practices

1. **Use descriptive IDs**: Components need unique IDs for state management
   ```python
   display = Text("0", id="counter-display")  # Good
   display = Text("0")  # Bad - no ID for targeting
   ```

2. **Initialize with defaults**: Always provide default values for reactive properties
   ```python
   state = State(display, text=0)  # Good
   state = State(display)  # Works, but no defaults to reset to
   ```

3. **One state per component**: Each component should have its own State instance
   ```python
   # Good
   counter1 = State(display1, text=0)
   counter2 = State(display2, text=0)
   
   # Avoid
   shared_state = State(display1, text=0)  # Don't reuse for display2
   ```

4. **Use auto operations wisely**: Remember to provide stop controls
   ```python
   start_btn.on_click = timer.text.auto_increment()
   stop_btn.on_click = timer.text.stop_auto()  # Always provide a way to stop
   ```

## Migration from dState

If you're migrating from the legacy dState system:

**Old (dState):**
```python
from dars.core.state import dState, Mod

display = Text("0", id="counter")
st = dState("counter", component=display, states=[0, 1, 2])
st.cState(1, mods=[Mod.inc(display, prop='text', by=1)])
button.on_click = st.state(1)
```

**New (State V2):**
```python
from dars.all import State

display = Text("0", id="counter")
counter = State(display, text=0)
button.on_click = counter.text.increment(by=1)
```

Key improvements:
- No state indices - direct property operations
- Cleaner, more Pythonic syntax
- Built-in auto operations
- Seamless animation integration
- More intuitive API

---

## Advanced Features

### Custom Intervals

```python
# Very fast updates (100ms)
timer.text.auto_increment(by=1, interval=100)

# Slow countdown (2 seconds)
countdown.text.auto_decrement(by=1, interval=2000)
```

### Bounded Auto Operations

```python
# Count from 0 to 10, then stop
timer.text.auto_increment(by=1, interval=1000, max=10)

# Count from 100 to 0, then stop
countdown.text.auto_decrement(by=1, interval=1000, min=0)
```

### Multiple Properties

```python
# State can manage multiple properties
state = State(component, 
    text="Hello",
    style={"color": "blue"},
    custom_attr="value"
)

# Each property gets reactive operations
state.text.set(value="Goodbye")
state.custom_attr.set(value="new_value")
```