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