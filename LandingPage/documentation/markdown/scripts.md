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
Button("Delayed Action", on_click=setTimeout(code=alert('Delayed!'), delay=2000))
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
