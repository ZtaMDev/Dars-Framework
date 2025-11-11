# Events in Dars

This is the documentation for the events in Dars.

## Event Calling System

Custom components in Dars can have events associated with them. You can set an event on a custom component using the `set_event` method.

```python
self.set_event(EventTypes.CLICK, dScript("console.log('click')"))
```

### Available Event Types

To use the event types, you need to import them from `dars.core.events`:

```python
from dars.core.events import EventTypes
```

Here are the different event types available:

- **Mouse Events:**
    - `CLICK = "click"`
    - `DOUBLE_CLICK = "dblclick"`
    - `MOUSE_DOWN = "mousedown"`
    - `MOUSE_UP = "mouseup"`
    - `MOUSE_ENTER = "mouseenter"`
    - `MOUSE_LEAVE = "mouseleave"`
    - `MOUSE_MOVE = "mousemove"`

- **Keyboard Events:**
    - `KEY_DOWN = "keydown"`
    - `KEY_UP = "keyup"`
    - `KEY_PRESS = "keypress"`

- **Form Events:**
    - `CHANGE = "change"`
    - `INPUT = "input"`
    - `SUBMIT = "submit"`
    - `FOCUS = "focus"`
    - `BLUR = "blur"`

- **Load Events:**
    - `LOAD = "load"`
    - `ERROR = "error"`
    - `RESIZE = "resize"`


---

## New in v1.2.2: Event arrays and dynamic handlers

- Any `on_*` attribute can now accept:
  - A single script (InlineScript, FileScript, dScript) or plain JS string
  - An array mixing any of the above (executed sequentially)

Example using `Mod.set`:

```python
Mod.set("btn1", on_click=[st1.state(0), dScript(code="console.log('clicked')")])
```

Runtime behavior:

- Only one dynamic listener per event is active at a time; subsequent `Mod.set` replaces the previous one.
- Dynamic handlers run in capture phase and stop propagation for the same event.
- Returning to the default state (index 0) removes any dynamic listeners from that element and restores its initial DOM.

