# Release Notes v1.3.8

> Dynamic state updates, improved event handling, and enhanced Electron dev experience. Introduces `this()` for event-time component updates, `RawJS` for JavaScript injection, and `dScript.then()` for async chaining.

## Installation

```bash
pip install --upgrade dars-framework
```

or

```bash
pip install dars-framework==1.3.8
```

## What's New

### Dynamic State Updates with `this()`

**Effortless Component Updates:**
- New `this()` helper for direct, event-time component updates without pre-registering states
- Update any component property: `text`, `html`, `style`, `attrs`, `classes`
- Works in both desktop and web exports
- Perfect for async operations and file I/O

**Usage:**
```python
from dars.core.state import this

# Button that updates itself
btn = Button("Click me", on_click=this().state(
    text="Clicked!",
    style={"color": "red"}
))

# Counter with Mod helpers
counter = Text("0", id="count")
inc_btn = Button("+1", on_click=this().state(text=Mod.inc("count")))
```

### Raw JavaScript Injection with `RawJS`

**Dynamic Value Passing:**
- New `RawJS` class for injecting raw JavaScript variables into state updates
- Essential for passing values from async operations
- Use `dScript.ARG` as a placeholder for chained script results

**Usage:**
```python
from dars.scripts.dscript import RawJS, dScript
from dars.desktop import read_text

# File content becomes button text
read_btn = Button("Load",
    on_click=read_text("data.txt").then(
        this().state(text=RawJS(dScript.ARG))
    )
)
```

### Script Chaining with `dScript.then()`

**Sequential Async Operations:**
- New `.then()` method for chaining `dScript` objects
- Pass results between scripts using `dScript.ARG` (resolves to `value`)
- Built-in error handling and logging for debugging
- Enables complex workflows like read → process → update → write

**Usage:**
```python
# Chain file operations
Button("Process",
    on_click=read_text("input.txt")
        .then(dScript(code="return value.toUpperCase()"))
        .then(write_text("output.txt", RawJS("value")))
        .then(this().state(text="Done!"))
)
```

### Event Handler Assignment Fix

**Fixed Critical Bug:**
- Event handlers can now be assigned via attribute assignment: `btn.on_click = handler`
- Previously only constructor assignment worked: `Button(on_click=handler)`
- Added `__setattr__` override to properly register events in all cases
- Maintains backward compatibility with existing code

### Enhanced Electron Dev Mode

**Improved Development Experience:**
- Filtered harmless Chrome DevTools warnings (Autofill.enable, etc.)
- Fixed double Electron window bug on file save/reload
- Added debounce logic to prevent concurrent restarts
- Cleaner console output with better error formatting
- Chrome DevTools auto-open in dev mode for easier debugging

**Better Logging:**
- Error-only stderr filtering (no more noise)
- Color-coded messages for different log levels
- Stack traces properly displayed for JavaScript errors

## Technical Improvements

### State System Enhancements
- **Dynamic Updates**: New `change({dynamic: true, ...})` path in `dars/js_lib.py`
- **RawJS Support**: State methods now detect and preserve `RawJS` values
- **this() Proxy**: Clean API for self-referential component updates

### Script System Improvements
- **Chaining Infrastructure**: Robust async IIFE wrapping for sequential execution
- **Value Passing**: Standardized `value` variable for inter-script communication
- **Debug Logging**: Verbose console output for troubleshooting chains

### Component System Fixes
- **Event Collection**: `VDomBuilder` now correctly serializes all event handlers
- **Attribute Interception**: `__setattr__` catches `on_*` assignments
- **Backward Compatible**: All existing event patterns continue working

### Dev Mode Stability
- **Debounce**: 300ms consolidation window for file change events
- **State Management**: Proper `restart_triggered` flag handling
- **Process Cleanup**: Reliable Electron termination before restart

## Documentation Updates

**Comprehensive Coverage:**
- New `this()` section in README with quick examples
- Expanded `state_management.md` with complete file operations guide
- Enhanced `exporters.md` with desktop API examples and chaining patterns
- Updated `scripts.md` with `.then()` method documentation

## Migration Notes

### For Existing Projects

**Seamless Upgrade:**
- No breaking changes - all existing code remains compatible
- New features are opt-in and additive
- Event handlers work with both constructor and attribute assignment

**Adopting New Features:**
```python
# Old way (still works)
my_state = dState("counter", counter, states=[0, 1, 2])
btn = Button("Next", on_click=my_state.state(goto='+1'))

# New way (more direct)
btn = Button("Increment", on_click=this().state(text=Mod.inc("counter")))
```

## Desktop Exporter Status

**Still in BETA:**
- File operations (`read_text`, `write_text`, `read_file`, `write_file`) are stable
- Dev mode with hot reload is fully functional
- Production packaging continues in experimental status
- Native API surface expanding with each release

## Performance & Compatibility

- **Zero Overhead**: Dynamic updates only activate when used
- **Bundle Size**: Minimal impact from new features
- **Browser Support**: Maintains full cross-browser compatibility
- **Desktop Integration**: Enhanced with improved error handling

---

**Upgrade Highly Recommended** for all desktop projects and applications requiring dynamic, event-driven UI updates.
