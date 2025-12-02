# Keyboard Events in Dars

Dars provides a powerful and intuitive system for handling keyboard events in your applications. This guide covers everything from basic key detection to advanced global shortcuts.

---

## Basic Keyboard Events

All Dars components support the `on_key_press` event handler for keyboard interactions.

### Simple Example

```python
from dars.all import *

Input(
    id="search",
    on_key_press=log("Key pressed!")
)
```

> **Note:** Use `on_key_press` as the universal keyboard event. The older `on_key_down` and `on_key_up` events have been deprecated in favor of this simpler approach.

---

## KeyCode Constants

The `KeyCode` class provides constants for all keyboard keys, making your code more readable and maintainable.

### Available Keys

```python
from dars.all import *

# Navigation keys
KeyCode.ENTER
KeyCode.TAB
KeyCode.ESCAPE  # or KeyCode.ESC
KeyCode.BACKSPACE
KeyCode.DELETE

# Arrow keys
KeyCode.UP       # or KeyCode.ARROWUP
KeyCode.DOWN     # or KeyCode.ARROWDOWN
KeyCode.LEFT     # or KeyCode.ARROWLEFT
KeyCode.RIGHT    # or KeyCode.ARROWRIGHT

# Letters (a-z)
KeyCode.A
KeyCode.B
# ... through ...
KeyCode.Z

# Numbers
KeyCode.ZERO  # or KeyCode.0
KeyCode.ONE   # or KeyCode.1
# ... through ...
KeyCode.NINE  # or KeyCode.9

# Function keys
KeyCode.F1
KeyCode.F2
# ... through ...
KeyCode.F12

# Special characters
KeyCode.SPACE
KeyCode.PLUS
KeyCode.MINUS
KeyCode.SLASH
KeyCode.COMMA
KeyCode.PERIOD
```

### Dynamic Key Access

```python
# Get key code by name
key = KeyCode.key('enter')  # Returns 'Enter'
key = KeyCode.key('A')      # Returns 'a'
```

---

## The onKey() Helper

The `onKey()` function is the **recommended way** to handle specific keyboard keys with optional modifier keys.

### Basic Usage

```python
from dars.all import *

# Simple key detection
Input(
    on_key_press=onKey(KeyCode.ENTER, log("Enter pressed!"))
)
```

### With Modifiers

```python
# Ctrl modifier
Container(
    on_key_press=onKey(KeyCode.S, alert("Saving..."), ctrl=True)
)

# Multiple modifiers
Container(
    on_key_press=onKey(KeyCode.Z, log("Redo"), ctrl=True, shift=True)
)
```

### Available Modifiers

- `ctrl` - Ctrl key (Command on Mac)
- `shift` - Shift key
- `alt` - Alt key
- `meta` - Meta/Command key

### Complete Example

```python
from dars.all import *

app = App("onKey Example")

formState = State("form", message="")

@route("/")
def index():
    return Page(
        Input(
            id="input",
            placeholder="Press Enter to submit",
            on_key_press=onKey(
                KeyCode.ENTER,
                formState.message.set("Submitted!"),
                ctrl=False  # Just Enter, no modifier needed
            )
        ),
        Text(useDynamic("form.message"))
    )

app.add_page("index", index(), index=True)
```

---

## The switch() Function

Use `switch()` to handle multiple different keys in a single event handler.

### Basic Usage

```python
from dars.all import *

Input(
    on_key_press=switch({
        KeyCode.ENTER: log("Enter pressed"),
        KeyCode.ESCAPE: alert("Escape pressed"),
    })
)
```

### With Multiple Actions

```python
formState = State("form", username="", password="")

Input(
    on_key_press=switch({
        KeyCode.ENTER: [
            formState.message.set("Submitted!"),
            alert("Form submitted!")
        ],
        KeyCode.ESCAPE: [
            clearInput("username"),
            clearInput("password"),
            formState.message.set("Cleared!")
        ]
    })
)
```

### Complete Example

```python
from dars.all import *

app = App("KeyCode Clean Example")

# State
formState = State("form", 
    username="", 
    password="", 
    message="Use keyboard shortcuts!"
)

@FunctionComponent
def LoginForm(**props):
    return f'''
    <div {Props.id} {Props.class_name} {Props.style}>
        <h2>Login Form with Keyboard Shortcuts</h2>
        <p style="color: #666;">{useDynamic("form.message")}</p>
        
        <input 
            type="text" 
            id="username-input"
            placeholder="Username"
            style="display: block; margin: 10px 0; padding: 8px; width: 300px;"
        />
        
        <input 
            type="password" 
            id="password-input"
            placeholder="Password"
            style="display: block; margin: 10px 0; padding: 8px; width: 300px;"
        />
        
        <div style="margin-top: 30px; padding: 15px; background: #f5f5f5; border-radius: 4px;">
            <h3 style="margin-top: 0;">Global Keyboard Shortcuts:</h3>
            <ul style="margin: 0; padding-left: 20px;">
                <li><strong>Ctrl+Enter</strong> - Submit form (shows alert)</li>
                <li><strong>Ctrl+F</strong> - Clear form</li>
                <li><strong>Ctrl+S</strong> - Save document</li>
            </ul>
            <p style="margin-top: 10px; font-size: 0.9em; color: #666;">
                Note: These are GLOBAL shortcuts that work anywhere on the page without blocking normal typing.
            </p>
        </div>
    </div>
    '''

@route("/")
def index():
    return Page(
        LoginForm(id="login-form"),
        Input(value="", on_key_up=onKey("R", action=log("Logged"))),
        # Buttons using State.set() and utils_ds functions
        Button(
            "Submit",
            on_click=[
                formState.message.set("Form submitted via button!"),
                alert("Form submitted!")
            ]
        ),
        
        Button(
            "Clear", 
            on_click=[
                formState.username.set(""),
                formState.password.set(""),
                formState.message.set("Form cleared via button!"),
                clearInput("username-input"),
                clearInput("password-input")
            ]
        ),
        
        Button(
            "Show Username",
            on_click=alert(V("#username-input"))
        ),
        
        Button(
            "Log Message",
            on_click=log(V("form.message"))
        ),
    )

addGlobalKeys(app, {
    (KeyCode.ENTER, 'ctrl'): [
        formState.message.set("Form submitted with Ctrl+Enter!"),
        alert("Form submitted!")
    ],
    (KeyCode.F, 'ctrl'): [
        formState.username.set(""),
        formState.password.set(""),
        formState.message.set("Form cleared with Ctrl+F!"),
        clearInput("username-input"),
        clearInput("password-input")
    ],
    (KeyCode.S, 'ctrl'): alert("Document saved! (Ctrl+S)"),
})

app.add_page("index", index(), title="KeyCode Example", index=True)

if __name__ == "__main__":
    app.rTimeCompile()
```

---

## Global Keyboard Shortcuts

Use `addGlobalKeys()` to create app-wide keyboard shortcuts that work anywhere on the page.

### Why Global Shortcuts?

Global shortcuts are perfect for:
- App-level commands (Save, Undo, Redo)
- Navigation shortcuts
- Quick actions that should work anywhere

> **Important:** Always use modifier keys (Ctrl, Alt, etc.) with global shortcuts to avoid blocking normal typing in input fields.

### Basic Usage

```python
from dars.all import *

app = App("Global Shortcuts")

# Define your actions
def save_document():
    return alert("Document saved!")

def undo():
    return log("Undo action")

# Add global shortcuts
addGlobalKeys(app, {
    (KeyCode.S, 'ctrl'): save_document(),
    (KeyCode.Z, 'ctrl'): undo()
})
```

### With Multiple Actions

```python
formState = State("form", data="")

addGlobalKeys(app, {
    (KeyCode.ENTER, 'ctrl'): [
        formState.data.set("Submitted!"),
        alert("Form submitted with Ctrl+Enter")
    ],
    (KeyCode.ESCAPE, 'ctrl'): [
        formState.data.set(""),
        log("Form cleared")
    ]
})
```

### Multiple Modifiers

```python
addGlobalKeys(app, {
    (KeyCode.Z, 'ctrl'): undo(),
    (KeyCode.Z, 'ctrl', 'shift'): redo(),
    (KeyCode.S, 'ctrl', 'shift'): save_as()
})
```

### Complete Example

```python
from dars.all import *

app = App("Global Shortcuts Example")

docState = State("document", 
    content="", 
    saved=False,
    message="Ready"
)

@route("/")
def index():
    return Page(
        Container(
            Text("Document Editor", style={"font-size": "24px", "font-weight": "bold"}),
            Text(useDynamic("document.message"), style={"color": "#666"}),
            
            Input(
                id="editor",
                placeholder="Start typing...",
                style={"width": "100%", "min-height": "200px"}
            ),
            
            Container(
                style={"margin-top": "20px", "padding": "15px", "background": "#f5f5f5"},
                children=[
                    Text("Global Shortcuts:", style={"font-weight": "bold"}),
                    Text("• Ctrl+S - Save"),
                    Text("• Ctrl+Z - Undo"),
                    Text("• Ctrl+Shift+Z - Redo"),
                ]
            )
        )
    )

# Global keyboard shortcuts
addGlobalKeys(app, {
    (KeyCode.S, 'ctrl'): [
        docState.saved.set(True),
        docState.message.set("Document saved!"),
        alert("Saved!")
    ],
    (KeyCode.Z, 'ctrl'): [
        docState.message.set("Undo"),
        log("Undo action")
    ]
})

app.add_page("index", index(), index=True)

if __name__ == "__main__":
    app.rTimeCompile()
```

---

## Best Practices

### 1. Use Modifiers for Global Shortcuts

**Bad - Blocks typing:**
```python
addGlobalKeys(app, {
    KeyCode.ENTER: submit_form()  # Blocks Enter in all inputs!
})
```

**Good - Doesn't interfere:**
```python
addGlobalKeys(app, {
    (KeyCode.ENTER, 'ctrl'): submit_form()  # Only Ctrl+Enter
})
```

### 2. Use onKey() for Component-Specific Keys

**For specific components:**
```python
Input(
    id="search",
    on_key_press=onKey(KeyCode.ENTER, perform_search())
)
```

**For app-wide shortcuts:**
```python
addGlobalKeys(app, {
    (KeyCode.F, 'ctrl'): focus("search")
})
```

### 3. Use switch() for Multiple Keys

**Bad - Repetitive:**
```python
Input(
    on_key_press=onKey(KeyCode.ENTER, action1())
)
Input(
    on_key_press=onKey(KeyCode.ESCAPE, action2())
)
```

**Good - Clean:**
```python
Container(
    on_key_press=switch({
        KeyCode.ENTER: action1(),
        KeyCode.ESCAPE: action2()
    })
)
```

### 4. Combine with State and V()

```python
formState = State("form", username="")

Input(
    id="username",
    on_key_press=onKey(KeyCode.ENTER, formState.username.set(V("#username")))
)
```

---

## Summary

- **Use `on_key_press`** for all keyboard events (replaces `on_key_down` and `on_key_up`)
- **Use `KeyCode`** constants for readable key references
- **Use `onKey()`** for single key detection with optional modifiers
- **Use `switch()`** for handling multiple different keys
- **Use `addGlobalKeys()`** for app-wide shortcuts (always with modifiers!)
- **Combine with State and V()** for dynamic, reactive keyboard interactions
