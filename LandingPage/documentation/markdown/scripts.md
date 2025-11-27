# Dars - Script System

## Introduction to Scripts

The script system of Dars allows adding interactive logic and dynamic behaviors to applications. Scripts are written in JavaScript and seamlessly integrate with UI components.

## Fundamentals of Scripts

### What are Scripts?

Scripts in Dars are fragments of JavaScript code that:

- Handle user interface events
- Implement client-side business logic
- Provide advanced interactivity
- Run in the context of the exported application

### Types of Scripts

Dars supports three main types of scripts:

1. **InlineScript**: Code defined directly in Python
2. **FileScript**: Code loaded from external files
3. **dScript**: Flexible script that can be defined either inline (as a string) or as a reference to an external file. Only one mode is allowed at a time.

## Base Script Class

All scripts inherit from the base `Script` class:

```python
from abc import ABC, abstractmethod

class Script(ABC):
    def __init__(self):
        pass
        
    @abstractmethod
    def get_code(self) -> str:
        """Retorna el código del script"""
        pass
```

## dScript

### When to use dScript

dScript is a flexible class that allows you to define a script as either:
- Inline JavaScript (via the `code` argument)
- Or as a reference to an external file (via the `file_path` argument)

But **never both at the same time**. This is useful for presets, user-editable actions, and advanced integrations.

### Basic Syntax

```python
from dars.scripts.dscript import dScript

# Inline JS
script_inline = dScript(code="""
function hello() { alert('Hello from dScript!'); }
document.addEventListener('DOMContentLoaded', hello);
""")

# External file
script_file = dScript(file_path="./scripts/my_script.js")
```

### Example: Editable JS preset from Python

```python
from dars.scripts.dscript import dScript

custom_action = dScript(code="""
function customClick() {
    alert('Custom action from preset!');
}
document.addEventListener('DOMContentLoaded', function() {
    var btn = document.getElementById('my-btn');
    if (btn) btn.onclick = customClick;
});
""")

app.add_script(custom_action)
```

### Chaining Scripts (`.then()`)

You can chain multiple `dScript` objects using the `.then()` method. This is particularly useful when working with asynchronous operations like file reading in Electron.

```python
from dars.desktop import read_text
from dars.core.state import this
from dars.scripts.dscript import RawJS, dScript

# Read a file and update a component with its content
# The result of the previous script is available as dScript.ARG (which resolves to 'value')
read_op = read_text("data.txt")
update_op = this().state(text=RawJS(dScript.ARG))

chained_script = read_op.then(update_op)
```

The `RawJS` wrapper ensures that `dScript.ARG` is treated as a variable name (`value`) rather than a string literal `"value"`.

### State Navigation with `state.state()`

The `state.state(idx)` method allows you to navigate a component to a specific state index. This is the recommended way to trigger state transitions.

**Requirements**:
- The component must have a `dState` defined with the target index in its `states` array
- The index must be valid (0 to states.length - 1)

**Example: Toggle Button**
```python
from dars.all import *
from dars.core.state import dState

# Create a button that toggles between two states
toggle_btn = Button("Off", id="ToggleBtn")

# Define states for the button
toggle_state = dState("toggle", component=toggle_btn, states=[0, 1])

# Configure state 1 appearance and behavior
toggle_state.cState(1, mods=[
    Mod.set(toggle_btn, 
        text="On",
        style={'background-color': 'green', 'color': 'white'},
        on_click=toggle_state.state(0)  # Return to state 0 when clicked
    )
])

# Initial click navigates to state 1
toggle_btn.on_click = toggle_state.state(1)
```

**Example: Cycle Through States**
```python
# Create a button that cycles through multiple states
cycle_btn = Button("State 0", id="CycleBtn")
cycle_state = dState("cycler", component=cycle_btn, states=[0, 1, 2, 3])

# Each state navigates to the next
cycle_state.cState(1, mods=[
    Mod.set(cycle_btn, text="State 1", on_click=cycle_state.state(2))
])
cycle_state.cState(2, mods=[
    Mod.set(cycle_btn, text="State 2", on_click=cycle_state.state(3))
])
cycle_state.cState(3, mods=[
    Mod.set(cycle_btn, text="State 3", on_click=cycle_state.state(0))
])

cycle_btn.on_click = cycle_state.state(1)  # Start the cycle
```

## InlineScript

### Basic Syntax InlineScript

```python
from dars.scripts.script import InlineScript

script = InlineScript("""
function saludar() {
    alert('¡Hola desde Dars!');
}

document.addEventListener('DOMContentLoaded', function() {
    console.log('Aplicación cargada');
});
""")
```

### Integration with Exporter

The exporter (`html_css_js.py`) automatically detects and exports all scripts of type `dScript`, `InlineScript`, and `FileScript`. You can safely mix and match them in your app, and all will be included in the generated JS.

- Script objects embedded in state bootstrap (e.g., inside `Mod.set(..., on_*=...)`) are serialized to a JSON-safe form as `{ "code": "..." }` and reconstituted at runtime.
- Event attributes (`on_*`) accept a single script or an array of scripts (any mix of InlineScript, FileScript, dScript, or raw JS strings). The runtime runs them sequentially and guarantees a single active dynamic listener per event.

---

## FileScript

### Basic Syntax for FileScript
```python
from dars.scripts.script import FileScript

# Load script from file
script = FileScript("./scripts/mi_script.js")
```

## Utility Scripts (`utils_ds`)

Dars provides a collection of utility functions in `dars.scripts.utils_ds` (exported in `dars.all`) that return pre-configured `dScript` objects for common tasks. These allow you to implement interactivity without writing raw JavaScript.

### Navigation

- `goTo(href)`: Navigate to a URL in the current tab.
- `goToNew(href)`: Open a URL in a new tab.
- `reload()`: Reload the current page.
- `goBack()`: Navigate back in browser history.
- `goForward()`: Navigate forward in browser history.

```python
Button("Home", on_click=goTo("/"))
Button("Docs", on_click=goToNew("https://docs.dars.dev"))
```

### DOM Manipulation

- `show(id)`: Show an element (display: block).
- `hide(id)`: Hide an element (display: none).
- `toggle(id)`: Toggle visibility.
- `setText(id, text)`: Set text content.
- `addClass(id, class_name)`: Add a CSS class.
- `removeClass(id, class_name)`: Remove a CSS class.
- `toggleClass(id, class_name)`: Toggle a CSS class.

```python
Button("Show Details", on_click=show("details-panel"))
Button("Toggle Theme", on_click=toggleClass("app-root", "dark-mode"))
```

### Timeouts

- `setTimeout(delay, code)`: Set a timeout to execute a script after a delay.

```python
Button("Delayed Action", on_click=setTimeout(delay=2000, code="alert('Delayed!')"))
```

### Modals

- `showModal(id)`: Show a Dars Modal component (handles hidden attribute and class).
- `hideModal(id)`: Hide a Dars Modal component.

```python
Button("Open Modal", on_click=showModal("my-modal"))
```

### Forms

- `submitForm(form_id)`: Submit a form.
- `resetForm(form_id)`: Reset a form.
- `getValue(input_id, target_id)`: Copy value from input to another element's text.
- `clearInput(input_id)`: Clear an input field.

```python
Button("Submit", on_click=submitForm("contact-form"))
Button("Clear", on_click=clearInput("search-box"))
```

### Storage (localStorage)

- `saveToLocal(key, value)`: Save string value.
- `loadFromLocal(key, target_id)`: Load value and set as text of target element.
- `removeFromLocal(key)`: Remove item.
- `clearLocalStorage()`: Clear all storage.

```python
Button("Save Prefs", on_click=saveToLocal("theme", "dark"))
```

### Clipboard

- `copyToClipboard(text)`: Copy text string.
- `copyElementText(id)`: Copy text content of an element.

```python
Button("Copy Code", on_click=copyElementText("code-block"))
```

### Scroll

- `scrollTo(x, y)`: Scroll to position.
- `scrollToTop()`: Smooth scroll to top.
- `scrollToBottom()`: Smooth scroll to bottom.
- `scrollToElement(id)`: Smooth scroll to specific element.

```python
Button("Back to Top", on_click=scrollToTop())
```

### Alerts & Focus

- `alert(message)`: Show browser alert.
- `confirm(message, on_ok, on_cancel)`: Show confirm dialog.
# Read a file and update a component with its content
# The result of the previous script is available as dScript.ARG (which resolves to 'value')
read_op = read_text("data.txt")
update_op = this().state(text=RawJS(dScript.ARG))

chained_script = read_op.then(update_op)
```

The `RawJS` wrapper ensures that `dScript.ARG` is treated as a variable name (`value`) rather than a string literal `"value"`.

### State Navigation with `state.state()`

The `state.state(idx)` method allows you to navigate a component to a specific state index. This is the recommended way to trigger state transitions.

**Requirements**:
- The component must have a `dState` defined with the target index in its `states` array
- The index must be valid (0 to states.length - 1)

**Example: Toggle Button**
```python
from dars.all import *
from dars.core.state import dState

# Create a button that toggles between two states
toggle_btn = Button("Off", id="ToggleBtn")

# Define states for the button
toggle_state = dState("toggle", component=toggle_btn, states=[0, 1])

# Configure state 1 appearance and behavior
toggle_state.cState(1, mods=[
    Mod.set(toggle_btn, 
        text="On",
        style={'background-color': 'green', 'color': 'white'},
        on_click=toggle_state.state(0)  # Return to state 0 when clicked
    )
])

# Initial click navigates to state 1
toggle_btn.on_click = toggle_state.state(1)
```

**Example: Cycle Through States**
```python
# Create a button that cycles through multiple states
cycle_btn = Button("State 0", id="CycleBtn")
cycle_state = dState("cycler", component=cycle_btn, states=[0, 1, 2, 3])

# Each state navigates to the next
cycle_state.cState(1, mods=[
    Mod.set(cycle_btn, text="State 1", on_click=cycle_state.state(2))
])
cycle_state.cState(2, mods=[
    Mod.set(cycle_btn, text="State 2", on_click=cycle_state.state(3))
])
cycle_state.cState(3, mods=[
    Mod.set(cycle_btn, text="State 3", on_click=cycle_state.state(0))
])

cycle_btn.on_click = cycle_state.state(1)  # Start the cycle
```

## InlineScript

### Basic Syntax InlineScript

```python
from dars.scripts.script import InlineScript

script = InlineScript("""
function saludar() {
    alert('¡Hola desde Dars!');
}

document.addEventListener('DOMContentLoaded', function() {
    console.log('Aplicación cargada');
});
""")
```

### Integration with Exporter

The exporter (`html_css_js.py`) automatically detects and exports all scripts of type `dScript`, `InlineScript`, and `FileScript`. You can safely mix and match them in your app, and all will be included in the generated JS.

- Script objects embedded in state bootstrap (e.g., inside `Mod.set(..., on_*=...)`) are serialized to a JSON-safe form as `{ "code": "..." }` and reconstituted at runtime.
- Event attributes (`on_*`) accept a single script or an array of scripts (any mix of InlineScript, FileScript, dScript, or raw JS strings). The runtime runs them sequentially and guarantees a single active dynamic listener per event.

---

## FileScript

### Basic Syntax for FileScript
```python
from dars.scripts.script import FileScript

# Load script from file
script = FileScript("./scripts/mi_script.js")
```

## Utility Scripts (`utils_ds`)

Dars provides a collection of utility functions in `dars.scripts.utils_ds` (exported in `dars.all`) that return pre-configured `dScript` objects for common tasks. These allow you to implement interactivity without writing raw JavaScript.

### Navigation

- `goTo(href)`: Navigate to a URL in the current tab.
- `goToNew(href)`: Open a URL in a new tab.
- `reload()`: Reload the current page.
- `goBack()`: Navigate back in browser history.
- `goForward()`: Navigate forward in browser history.

```python
Button("Home", on_click=goTo("/"))
Button("Docs", on_click=goToNew("https://docs.dars.dev"))
```

### DOM Manipulation

- `show(id)`: Show an element (display: block).
- `hide(id)`: Hide an element (display: none).
- `toggle(id)`: Toggle visibility.
- `setText(id, text)`: Set text content.
- `addClass(id, class_name)`: Add a CSS class.
- `removeClass(id, class_name)`: Remove a CSS class.
- `toggleClass(id, class_name)`: Toggle a CSS class.

```python
Button("Show Details", on_click=show("details-panel"))
Button("Toggle Theme", on_click=toggleClass("app-root", "dark-mode"))
```

### Timeouts

- `setTimeout(delay, code)`: Set a timeout to execute a script after a delay.

```python
Button("Delayed Action", on_click=setTimeout(delay=2000, code="alert('Delayed!')"))
```

### Modals

- `showModal(id)`: Show a Dars Modal component (handles hidden attribute and class).
- `hideModal(id)`: Hide a Dars Modal component.

```python
Button("Open Modal", on_click=showModal("my-modal"))
```

### Forms

- `submitForm(form_id)`: Submit a form.
- `resetForm(form_id)`: Reset a form.
- `getValue(input_id, target_id)`: Copy value from input to another element's text.
- `clearInput(input_id)`: Clear an input field.

```python
Button("Submit", on_click=submitForm("contact-form"))
Button("Clear", on_click=clearInput("search-box"))
```

### Storage (localStorage)

- `saveToLocal(key, value)`: Save string value.
- `loadFromLocal(key, target_id)`: Load value and set as text of target element.
- `removeFromLocal(key)`: Remove item.
- `clearLocalStorage()`: Clear all storage.

```python
Button("Save Prefs", on_click=saveToLocal("theme", "dark"))
```

### Clipboard

- `copyToClipboard(text)`: Copy text string.
- `copyElementText(id)`: Copy text content of an element.

```python
Button("Copy Code", on_click=copyElementText("code-block"))
```

### Scroll

- `scrollTo(x, y)`: Scroll to position.
- `scrollToTop()`: Smooth scroll to top.
- `scrollToBottom()`: Smooth scroll to bottom.
- `scrollToElement(id)`: Smooth scroll to specific element.

```python
Button("Back to Top", on_click=scrollToTop())
```

### Alerts & Focus

- `alert(message)`: Show browser alert.
- `confirm(message, on_ok, on_cancel)`: Show confirm dialog.
- `log(message)`: Log to console.
- `focus(id)`: Focus an element.
- `blur(id)`: Blur an element.

```python
Button("Delete", on_click=confirm(
    "Are you sure?", 
    on_ok="console.log('Deleted')", 
    on_cancel="console.log('Cancelled')"
))
```

## Animation System

Dars includes a comprehensive animation system with 15+ built-in animations. All animation functions return `dScript` objects and can be chained for complex sequences.

### Basic Animations

#### fadeIn / fadeOut

```python
from dars.all import fadeIn, fadeOut

# Fade in an element
button.on_click = fadeIn(id="box", duration=500, easing="ease")

# Fade out an element
button.on_click = fadeOut(id="box", duration=500, hide_after=True)
```

**Parameters:**
- `id`: Element ID to animate
- `duration`: Animation duration in milliseconds (default: 500)
- `easing`: CSS easing function (default: "ease")
- `hide_after`: For fadeOut, set display:none after animation (default: True)

#### slideIn / slideOut

```python
from dars.all import slideIn, slideOut

# Slide in from left
button.on_click = slideIn(id="panel", direction="left", duration=400)

# Slide out to right
button.on_click = slideOut(id="panel", direction="right", duration=400)
```

**Directions:** `"left"`, `"right"`, `"top"`, `"bottom"`, `"top-left"`, `"top-right"`, `"bottom-left"`, `"bottom-right"`

#### scaleIn / scaleOut

```python
from dars.all import scaleIn, scaleOut

# Scale in from 0.3 to 1
button.on_click = scaleIn(id="popup", from_scale=0.3, duration=400)

# Scale out to 0.5
button.on_click = scaleOut(id="popup", to_scale=0.5, duration=400)
```

### Interactive Animations

#### shake

```python
from dars.all import shake

# Shake effect
button.on_click = shake(id="alert", intensity=10, duration=500)
```

**Parameters:**
- `intensity`: Shake distance in pixels (default: 10)
- `duration`: Total animation duration (default: 500)

#### bounce

```python
from dars.all import bounce

# Bounce effect
button.on_click = bounce(id="element", distance=20, duration=600)
```

#### pulse

```python
from dars.all import pulse

# Pulse effect
button.on_click = pulse(id="button", scale=1.1, duration=400, iterations=2)
```

**Parameters:**
- `scale`: Maximum scale factor (default: 1.1)
- `iterations`: Number of pulses (default: 1, use "infinite" for continuous)

#### rotate

```python
from dars.all import rotate

# Rotate 360 degrees
button.on_click = rotate(id="spinner", degrees=360, duration=1000)
```

#### flip

```python
from dars.all import flip

# Flip on Y axis
button.on_click = flip(id="card", axis="y", duration=600)
```

**Axis:** `"x"` (horizontal), `"y"` (vertical)

### Color and Size Animations

#### colorChange

```python
from dars.all import colorChange

# Change background color
button.on_click = colorChange(
    id="box",
    property="background",
    from_color="#ff0000",
    to_color="#00ff00",
    duration=500
)
```

**Properties:** `"color"`, `"background"`, `"border-color"`

#### morphSize

```python
from dars.all import morphSize

# Morph to new size
button.on_click = morphSize(
    id="box",
    to_width="300px",
    to_height="200px",
    duration=500
)
```

### Animation Chaining

#### sequence

Chain multiple animations to run one after another:

```python
from dars.all import sequence, fadeIn, pulse, shake

button.on_click = sequence(
    fadeIn(id="box", duration=300),
    pulse(id="box", scale=1.2, iterations=2),
    shake(id="box", intensity=5)
)
```

#### parallel

Run animations simultaneously (use `.then()` with same timing):

```python
from dars.all import fadeIn, scaleIn

# Both animations run at the same time
button.on_click = fadeIn(id="box").then(scaleIn(id="other-box"))
```

### Chaining with State Operations

Animations integrate seamlessly with State V2:

```python
from dars.all import *

display = Text("0", id="counter")
counter = State(display, text=0)

button.on_click = sequence(
    counter.text.increment(by=1),
    pulse(id="counter", scale=1.2),
    fadeOut(id="counter", duration=200),
    counter.text.set(value=0),
    fadeIn(id="counter", duration=200)
)
```

### Complete Animation Example

```python
from dars.all import *

app = App("Animation Demo")

# Create animated box
box = Container(
    Text("Animate Me!", style={"color": "white"}),
    id="anim-box",
    style={
        "background": "linear-gradient(135deg, #667eea, #764ba2)",
        "padding": "40px",
        "border-radius": "16px",
        "text-align": "center"
    }
)

# Animation buttons
fade_btn = Button("Fade In", on_click=fadeIn(id="anim-box", duration=600))
slide_btn = Button("Slide In", on_click=slideIn(id="anim-box", direction="left"))
shake_btn = Button("Shake", on_click=shake(id="anim-box", intensity=10))
pulse_btn = Button("Pulse", on_click=pulse(id="anim-box", scale=1.15, iterations=3))

# Sequence button
sequence_btn = Button("Combo", on_click=sequence(
    fadeIn(id="anim-box", duration=400),
    pulse(id="anim-box", scale=1.1, iterations=2),
    shake(id="anim-box", intensity=5, duration=400)
))

page = Page(Container(box, fade_btn, slide_btn, shake_btn, pulse_btn, sequence_btn))
app.add_page("index", page, index=True)
```

### Animation Best Practices

1. **Use appropriate durations**: Most animations work well between 300-600ms
   ```python
   fadeIn(id="box", duration=400)  # Good - feels responsive
   fadeIn(id="box", duration=2000)  # Too slow - users will get impatient
   ```

2. **Match animation to context**: Use subtle animations for frequent actions
   ```python
   # Frequent action - subtle
   button.on_click = pulse(id="counter", scale=1.05, duration=200)
   
   # Important action - more dramatic
   success_btn.on_click = sequence(
       scaleIn(id="message", from_scale=0.5, duration=400),
       pulse(id="message", scale=1.1, iterations=2)
   )
   ```

3. **Don't overuse sequence**: Long animation chains can frustrate users
   ```python
   # Good - 2-3 animations
   sequence(fadeIn(id="a"), pulse(id="b"))
   
   # Avoid - too many steps
   sequence(fadeIn(id="a"), slideIn(id="b"), shake(id="c"), bounce(id="d"), fadeOut(id="e"))
   ```

4. **Provide visual feedback**: Use animations to acknowledge user actions
   ```python
   submit_btn.on_click = sequence(
       pulse(id="submit-btn", scale=0.95, duration=100),  # Button press feedback
       fadeOut(id="form", duration=300),
       fadeIn(id="success-message", duration=300)
   )
   ```

### Available Animations Reference

| Function | Purpose | Key Parameters |
|----------|---------|----------------|
| `fadeIn` | Fade element in | `id`, `duration`, `easing` |
| `fadeOut` | Fade element out | `id`, `duration`, `hide_after` |
| `slideIn` | Slide element in | `id`, `direction`, `distance`, `duration` |
| `slideOut` | Slide element out | `id`, `direction`, `distance`, `duration` |
| `scaleIn` | Scale element in | `id`, `from_scale`, `duration` |
| `scaleOut` | Scale element out | `id`, `to_scale`, `duration` |
| `shake` | Shake effect | `id`, `intensity`, `duration` |
| `bounce` | Bounce effect | `id`, `distance`, `duration` |
| `pulse` | Pulse/heartbeat | `id`, `scale`, `duration`, `iterations` |
| `rotate` | Rotate element | `id`, `degrees`, `duration` |
| `flip` | Flip on axis | `id`, `axis`, `duration` |
| `colorChange` | Change color | `id`, `property`, `from_color`, `to_color` |
| `morphSize` | Change size | `id`, `to_width`, `to_height`, `duration` |
| `sequence` | Chain animations | `*animations` |

All animations return `dScript` objects and can be used with `.then()` for advanced chaining.
