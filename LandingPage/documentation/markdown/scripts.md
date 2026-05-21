# Dars - Script & Action System

Dars Framework features a dual-layer logic system: **Structured DAP Actions** for high-security, high-performance interactions, and **JavaScript Scripts** for complex client-side logic.

---

## The Dars Action Protocol (DAP)

DAP is the modern backbone of Dars interactivity. It replaces raw JavaScript strings with structured data objects that describe actions.

### Why DAP?

1. **Security**: DAP actions are executed by a built-in registry, avoiding dangerous `eval()` or `new Function()` calls. This enables a strict Content Security Policy (CSP).
2. **Predictability**: Actions are defined as Python dictionaries, making them easier to debug and validate.

- **Full-Stack Consistency**: The same action structure works in SPA and SSR targets.

---

## dScript: The Universal Action Container

The `dScript` class is the primary way to define logic in Dars. It supports three modes:

### 1. Structured Action (Recommended)

Define actions using the `data` parameter. This is the most secure and modern approach.

```python
from dars.all import dScript

# A structured DAP action
my_action = dScript(data={
    "op": "alert",
    "args": {"message": "Hello from DAP!"}
})
```

### 2. Inline JavaScript (Legacy/Complex)

For logic that DAP cannot yet express, you can use raw JS. Dars will attempt to convert this to DAP at compile-time.

```python
script = dScript(code="console.log('Legacy JS');")
```

### 3. External File Reference

Load complex JS modules from your project files.

```python
script = dScript(file_path="./scripts/my_module.js")
```

---

## Advanced Logic Helpers

### RawJS: Escaping String Literals

When you pass a string to a DAP helper (like `this().state()`), Dars treats it as a text literal. Use `RawJS` to tell the compiler: "This is a JavaScript variable/expression".

```python
from dars.scripts.dscript import RawJS
from dars.core.state import this

# Updates the component text with the value of a JS variable named 'myVar'
update_op = this().state(text=RawJS("myVar"))
```

### The Arg Helper: Accessing Chained Results

When chaining scripts with `.then()`, the result of the previous script is passed to the next one. Use the `Arg` helper to access this value Pythonically. `Arg` is a singleton instance of `_ArgHelper` (a `RawJS` subclass).

```python
from dars.scripts.dscript import Arg

# Example chaining: use the previous result in the next script
update_op = this().state(text=Arg) # Accesses the entire result
update_op_nested = this().state(text=Arg.content) # Accesses 'result.content'

chained = some_async_action.then(update_op)
```

---

## Logic Chaining (`.then()`)

All `dScript` and `RawJS` objects support the `.then()` method for sequential execution. This creates an asynchronous pipeline where values flow between steps.

```python
from dars.all import *

action = (
    alert("Starting process...")
    .then(log("Process step 1"))
    .then(alert("Finished!"))
)
```

---

## Utility Functions (`utils_ds`)

Dars provides high-level Python helpers that return pre-configured, DAP-compatible `dScript` objects.

### Interactive Utilities

| Function                | Description                                       |
| ----------------------- | ------------------------------------------------- |
| `alert(msg)`            | Shows a browser alert dialog.                     |
| `log(msg)`              | Logs a message to the browser console.            |
| `goTo(url)`             | Navigates to a new URL in the same tab.           |
| `goToNew(url)`          | Opens a URL in a new browser tab.                 |
| `reload()`              | Reloads the current page.                         |
| `show(id)`              | Makes an element visible (`display: block`).      |
| `hide(id)`              | Hides an element (`display: none`).               |
| `toggle(id)`            | Toggles an element's visibility.                  |
| `setText(id, text)`     | Sets the text content of an element.              |
| `addClass(id, name)`    | Adds a CSS class to an element.                   |
| `removeClass(id, name)` | Removes a CSS class.                              |
| `toggleClass(id, name)` | Toggles a CSS class.                              |
| `copyToClipboard(text)` | Copies the provided text to the system clipboard. |

and a LOT more..

## Animation System

Animations in Dars return `dScript` objects and can be combined using `sequence()` or chained with `.then()`.

```python
from dars.all import fadeIn, pulse, sequence

# Animate an element when clicked
btn = Button("Animate", on_click=sequence(
    fadeIn("box", duration=300),
    pulse("box", scale=1.2)
))
```

### Available Animations Reference

| Function   | Purpose           | Key Parameters                 |
| ---------- | ----------------- | ------------------------------ |
| `fadeIn`   | Fade element in   | `id`, `duration`, `easing`     |
| `fadeOut`  | Fade element out  | `id`, `duration`, `hide_after` |
| `slideIn`  | Slide element in  | `id`, `direction`, `duration`  |
| `slideOut` | Slide element out | `id`, `direction`, `duration`  |
| `scaleIn`  | Scale element in  | `id`, `from_scale`, `duration` |
| `shake`    | Shake effect      | `id`, `intensity`, `duration`  |
| `pulse`    | Pulse/heartbeat   | `id`, `scale`, `iterations`    |
| `rotate`   | Rotate element    | `id`, `degrees`, `duration`    |
| `flip`     | Flip on axis      | `id`, `axis`, `duration`       |

---

## Best Practices

1. **Prefer DAP**: Always use built-in helpers (like `alert()`, `show()`, `this().state()`) instead of raw JS strings.
2. **Use RawJS for Variables**: Only use `RawJS` when you explicitly need to reference a client-side JavaScript variable or expression.
3. **Chain for Flow**: Use `.then()` to create logical sequences, keeping each step focused.
4. **Arg for Data**: Use the `Arg` helper to handle results from asynchronous operations (like API calls or file reading) without writing JavaScript.
