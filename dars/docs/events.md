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


