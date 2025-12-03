# Release Notes v1.6.1

> **Side Effects System Enhancement - useWatch Arrays & Multiple Callbacks**

## Installation

```bash
pip install --upgrade dars-framework
```

## What's New

### Enhanced useWatch Hook - Array Syntax & Multiple Callbacks

The `useWatch` hook now supports watching multiple state properties simultaneously and executing multiple callbacks, enabling powerful reactive patterns and side effects.

**Watch Multiple State Properties:**
```python
# Watch multiple properties - callback executes when ANY of them change
app.useWatch(
    ["product.name", "product.price"],
    productState.info.set("Product: " + V("product.name") + " - $" + V("product.price"))
)
```

**Multiple Callbacks:**
```python
# Execute multiple callbacks when state changes
app.useWatch(
    "cart.total",
    log("Total changed!"),
    alert("Cart updated")
)

# Combine array syntax with multiple callbacks
app.useWatch(
    ["product.name", "product.price"],
    productState.info.set("Product: " + V("product.name") + " - $" + V("product.price")),
    log("Product info updated")
)
```

**Key Features:**
- **Array Syntax**: Watch multiple state paths with a single watcher
- **Multiple Callbacks**: Execute multiple side effects in sequence
- **Reactive Composition**: Automatically sync derived state when source properties change
- **Clean API**: Simple comma-separated syntax for callbacks

### Bug Fixes

#### Fixed Custom State Property Handling

Resolved an issue where custom state properties (properties other than `text`, `html`, `style`, `attrs`) were not correctly triggering watchers when updated via `change()`.

**What was fixed:**
- Custom properties like `info`, `count`, `status` now correctly update in `st.values`
- Watchers for custom properties now trigger reliably
- State registry properly maintains current values for all properties

**Example that now works correctly:**
```python
productState = State("product", name="Milk", price=100, info="")

# This now correctly updates product.info when name or price changes
app.useWatch(
    ["product.name", "product.price"],
    productState.info.set("Product: " + V("product.name") + " - $" + V("product.price"))
)
```

#### Improved V() Helper State Access

The `V()` helper now correctly retrieves current state values from the state registry instead of reading stale values from the DOM.

**Previous Behavior:**
- `V("product.name")` would read the displayed text from the DOM
- This could lead to recursive string concatenation issues
- Values might not reflect the actual state

**Fixed Behavior:**
- `V("product.name")` now reads directly from `window.Dars.getState('product').values['name']`
- Always returns the current, raw state value
- Falls back to DOM reading for legacy support

---

# Release Notes v1.6.0


> **Critical Bug Fixes & State Management Improvements**

## Installation

```bash
pip install --upgrade dars-framework
```

## What's Fixed

### 1. Hook Initialization Fixes

Fixed critical bugs where `useDynamic` and `useValue` hooks were not properly displaying default values from `State` objects when used in `FunctionComponent`s.

**Issues Resolved:**
- `useDynamic` now correctly retrieves default values from the state registry even when props are not explicitly passed to the component
- `useValue` now works correctly without requiring a selector parameter
- Both hooks properly display initial state values on first render

**Example:**
```python
# This now works correctly!
state = State("ui", count=0, disabled=False)

@FunctionComponent
def Counter(**props):
    return f'''
        <div>
            <p>Count: {useDynamic("ui.count")}</p>
            <button disabled="{useDynamic("ui.disabled")}">Click</button>
        </div>
    '''
```

### 2. State Reset Functionality Enhancement

Completely rewrote the `reset()` function to correctly handle **all** component properties, including boolean attributes like `checked`, `disabled`, `readonly`, and `required`.

**Previous Behavior:**
- Boolean attributes were incorrectly set to `"false"` string instead of being removed
- Properties like `disabled="false"` would still disable elements (incorrect HTML behavior)

**Fixed Behavior:**
- Boolean attributes are now properly removed when `False`
- Both HTML attributes AND DOM properties are synchronized correctly
- Works for: `checked`, `disabled`, `readonly`, `required`, `selected`, `autofocus`, `autoplay`, `controls`, `loop`, `muted`

**Example:**
```python
state = State("ui", is_disabled=False, is_checked=True)

Button(disabled=useDynamic("ui.is_disabled"))
Checkbox(checked=useDynamic("ui.is_checked"))

# Reset now works perfectly
Button("Reset All", on_click=state.reset())
```

### 3. JavaScript Variable Name Sanitization

Fixed `SyntaxError` in generated JavaScript caused by HTML IDs containing hyphens being used as variable names.

**Issue:**
```javascript
// Generated invalid JS
const el_control-panel = ...  // SyntaxError!
```

**Fixed:**
```javascript
// Now generates valid JS
const el_control_panel = ...  // ✓ Valid
```

### 4. Boolean Attribute Handling Improvements

Enhanced the reactive binding system to properly handle boolean attributes with the `is_` prefix.

**Supported Patterns:**
```python
# All of these now work correctly
state = State("ui", is_disabled=False, disabled=False)

# Automatic mapping: is_disabled -> disabled attribute
Button(disabled=useDynamic("ui.is_disabled"))

# State changes properly update the DOM
state.is_disabled.set(True)   # Adds disabled attribute
state.is_disabled.set(False)  # Removes disabled attribute completely
```

## Important Notes

### State ID Best Practices

> **[!IMPORTANT] When using `State` objects with hooks like `useDynamic` and `useValue`, the state ID should **NOT** match any component ID in your DOM. The state ID is a unique identifier for the state object itself, not a component.**

**X Incorrect:**
```python
# DON'T do this - state ID matches button ID
state = State("my-button", count=0)
Button(id="my-button", text=useDynamic("my-button.count"))
```

**✓ Correct:**
```python
# DO this - state has unique ID
state = State("counter-state", count=0)
Button(id="my-button", text=useDynamic("counter-state.count"))
```

The reactive system uses watchers to update components when state changes, so the state ID doesn't need to (and shouldn't) match any specific component ID.

## Technical Details

### Changes to `js_lib.py`

1. **`change()` function**: Added intelligent boolean attribute detection with `is_` prefix support
2. **`_applyMods()` function**: Enhanced to handle boolean attributes in state modifications
3. **`_restoreDefault()` function**: Improved to correctly restore boolean attributes to their initial state

### Changes to `html_css_js.py`

1. **`_generate_reactive_bindings_js()`**: Added boolean attribute handling in watcher code generation
2. **Variable name sanitization**: Replaces hyphens with underscores in generated JS variable names
3. **`_process_function_component()`**: Added fallback to `STATE_V2_REGISTRY` for missing prop values

### Changes to `use_value.py`

1. **`ValueMarker.__init__()`**: Now always registers markers, even without a selector

---

# Release Notes v1.5.9

> **Unified Keyboard Events & KeyCode System**

## Installation

```bash
pip install --upgrade dars-framework
```

## What's New

### 1. Unified Keyboard Events (`on_key_press`)

Simplified keyboard event handling by consolidating `on_key_down` and `on_key_up` into a single, robust **`on_key_press`** event. This ensures consistent behavior across all components and browsers.

**Deprecated:**
- `on_key_down`
- `on_key_up`

**New Standard:**
```python
Input(on_key_press=log("Key pressed!"))
```

### 2. The `KeyCode` System

No more magic strings or numbers! The new `KeyCode` class provides constants for all keyboard keys, making your code readable and maintainable.

```python
from dars.all import KeyCode

# Use constants
KeyCode.ENTER
KeyCode.ESCAPE
KeyCode.TAB
KeyCode.SPACE
KeyCode.A
KeyCode.F1
```

### 3. Powerful Helpers: `onKey`, `switch`, `addGlobalKeys`

Introduced three powerful helpers to make keyboard handling elegant and Pythonic.

#### `onKey()` - Single Key Handler
Handle specific keys with optional modifiers easily:

```python
# Simple
Input(on_key_press=onKey(KeyCode.ENTER, submit_form()))

# With Modifiers
Container(on_key_press=onKey(KeyCode.S, save(), ctrl=True))
```

#### `switch()` - Multiple Key Handler
Handle multiple keys in a single component without messy if-statements:

```python
Input(on_key_press=switch({
    KeyCode.ENTER: submit_form(),
    KeyCode.ESCAPE: clear_form(),
    KeyCode.TAB: focus_next()
}))
```

#### `addGlobalKeys()` - App-wide Shortcuts
Register global keyboard shortcuts that work anywhere in your app:

```python
addGlobalKeys(app, {
    (KeyCode.S, 'ctrl'): save_document(),
    (KeyCode.Z, 'ctrl'): undo(),
    (KeyCode.Z, 'ctrl', 'shift'): redo()
})
```

### 4. Documentation

A comprehensive guide to the new system is available in `KeyEvents.md`, covering everything from basic usage to advanced global shortcuts and best practices.

## Migration Guide

**From `on_key_down` / `on_key_up`:**
Simply rename your event handlers to `on_key_press`. The underlying behavior uses `keydown` for maximum reliability.

```python
# Before
Input(on_key_down=dScript("..."))

# After
Input(on_key_press=dScript("..."))
```

---

# Release Notes v1.5.8

> **Enhanced V() Helper & useValue Selector Support**

## Installation

```bash
pip install --upgrade dars-framework
```

## What's New

### 1. V() Helper - State Path Support

The `V()` helper now supports extracting values from **reactive state** in addition to DOM elements!

#### State Path Extraction

```python
# Extract from reactive state created by useDynamic()
V("cart.total")      # Gets current value of cart.total
V("user.name")       # Gets current value of user.name
V("product.price")   # Gets current value of product.price
```

**How it works:**
- `V("cart.total")` finds the reactive element created by `useDynamic("cart.total")`
- Reads its current `textContent` value
- Perfect for combining reactive state with calculations

#### Complete Integration Example

```python
from dars.all import *

productState = State("product", price=19.99, quantity=1, total=19.99)

@FunctionComponent
def ProductCard(**props):
    return f'''
    <div {Props.id}>
        <p>Price: ${useDynamic("product.price")}</p>
        <input type="number" value="{useValue("product.quantity", ".qty-input")}" />
        <p>Total: ${useDynamic("product.total")}</p>
    </div>
    '''

# Calculate total: DOM input × State value
Button("Calculate", on_click=productState.total.set(
    V(".qty-input").int() * V("product.price").float()
))
```

### 2. V() Helper - Arithmetic Operator Validation

**Breaking Change (Validation)**: Arithmetic operators now **require** numeric transformations to prevent bugs.

#### The Problem

Previously, you could accidentally multiply strings:
```python
# Before: This would concatenate strings, not multiply!
V("#price") * V("#qty")  # "19.99" * "5" = NaN or unexpected behavior
```

#### The Solution

Arithmetic operators (`*`, `/`, `-`, `%`, `**`) now require `.int()` or `.float()`:

```python
# CORRECT - With transformations
V("#price").float() * V("#qty").int()  # 19.99 * 5 = 99.95

# ERROR - Without transformations
V("#price") * V("#qty")
# TypeError: Multiplication requires numeric transformation.
#            Use V('#price').int() or V('#price').float() before multiplying.
```

**String concatenation (`+`) still works without transformations:**
```python
# Always allowed
V("#first") + " " + V("#last")  # String concatenation
"Total: $" + V("cart.total")    # String concatenation
```

**Supported Operators:**
- `+` - Addition/Concatenation (always allowed)
- `*` - Multiplication (requires `.int()` or `.float()`)
- `/` - Division (requires `.int()` or `.float()`)
- `-` - Subtraction (requires `.int()` or `.float()`)
- `%` - Modulo (requires `.int()` or `.float()`)
- `**` - Power (requires `.int()` or `.float()`)

### 3. useValue() - Selector Support in FunctionComponents

`useValue()` now supports automatic selector application in FunctionComponents!

#### Automatic Selector Application

```python
@FunctionComponent
def UserForm(**props):
    return f'''
    <div {Props.id}>
        <input value="{useValue("user.name", ".name-input")}" />
        <input value="{useValue("user.email", "#email-field")}" />
    </div>
    '''

# Extract values using the selectors
Button("Save", on_click=userState.name.set(V(".name-input")))
```

**How it works:**
1. `useValue("user.name", ".name-input")` sets initial value AND applies class `name-input`
2. `V(".name-input")` extracts the current value (even if modified by user)
3. Perfect for forms with initial values and value extraction

**Supported selectors:**
- **Class selectors** (`.foo`) → Added to element's `class` attribute
- **ID selectors** (`#bar`) → Set as element's `id` attribute

---

## Migration Guide

### V() Arithmetic Operations

If you were using arithmetic operators without transformations, add `.int()` or `.float()`:

**Before:**
```python
state.total.set(V("#price") * V("#qty"))
```

**After:**
```python
state.total.set(V("#price").float() * V("#qty").int())
```

**String concatenation is unchanged:**
```python
# Still works the same
state.fullname.set(V("#first") + " " + V("#last"))
```

---

## Complete Example

```python
from dars.all import *

app = App("Shopping Cart")

# Reactive state
cartState = State("cart", total=0.0)
productState = State("product", name="Widget", price=19.99, quantity=1)

@FunctionComponent
def ProductCard(**props):
    return f'''
    <div {Props.id} {Props.class_name} {Props.style}>
        <!-- Reactive display -->
        <h3>{useDynamic("product.name")}</h3>
        <p>Price: ${useDynamic("product.price")}</p>
        
        <!-- Editable quantity with selector -->
        <input type="number" 
               value="{useValue("product.quantity", ".qty-input")}"
               min="1" />
        
        <!-- Reactive total -->
        <p>Total: ${useDynamic("cart.total")}</p>
    </div>
    '''

@route("/")
def index():
    return Page(
        ProductCard(id="product-card", name="Milk", price=100, quantity=2, total=0),
        
        # Calculate: DOM input × State value
        Button("Calculate Total", on_click=cartState.total.set(
            V(".qty-input").int() * V("product.price").float()
        )),
        
        # String concatenation (no transformation needed)
        Button("Show Info", on_click=productState.name.set(
            "Product: " + V("product.name") + " - $" + V("product.price")
            )
        )
    )

app.add_page("index", index(), title="Product", index=True)

# Watch for changes
app.useWatch("cart.total", log("Cart total changed!"))

if __name__ == "__main__":
    app.rTimeCompile()
```

---

## Bug Fixes

### useValue Selector Application
- **Issue**: Selectors in `useValue()` were not being applied to FunctionComponent elements
- **Fix**: Implemented BeautifulSoup-based HTML parsing to detect and apply selectors
- **Impact**: `useValue()` now works identically in FunctionComponents and built-in components

### V() State Path Detection
- **Issue**: No way to extract values from reactive state without DOM elements
- **Fix**: Added intelligent state path detection (e.g., `"cart.total"` vs `".cart-total"`)
- **Impact**: Seamless integration between `useDynamic()`, `useValue()`, and `V()`

---

## Breaking Changes

### Arithmetic Operator Validation

**Change**: Arithmetic operators (`*`, `/`, `-`, `%`, `**`) now require `.int()` or `.float()` transformations.

**Reason**: Prevents accidental string operations that cause bugs.

**Migration**: Add `.int()` or `.float()` before arithmetic operations:
```python
V("#price").float() * V("#qty").int()
```

**Note**: String concatenation (`+`) is unchanged and still works without transformations.

---

## Documentation Updates

- **hooks.md**: Comprehensive V() documentation with state path examples
- **custom_components.md**: Updated examples showing V() with state paths
- **New examples**: Complete integration patterns for `useValue()`, `useDynamic()`, and `V()`

---

## What's Next

The enhanced V() helper and complete hooks integration pave the way for more advanced reactive patterns and seamless state management in future releases.

---

# Release Notes v1.5.7

> **useValue hook & Value Access Helpers**

## Installation

```bash
pip install --upgrade dars-framework
```

## What's New

### 1. `useValue` Hook

The new `useValue` hook allows you to access the **initial value** of a state property without creating a reactive binding. This is perfect for form inputs where you want to set a default value but allow the user to edit it freely.

```python
# Initial value from state, but editable by user
Input(value=useValue("user.name"))

# In FunctionComponent templates (resolves to initial value string)
@FunctionComponent
def Profile(**props):
    return f"<div>{useValue('user.name')}</div>"
```

### 2. Pythonic Helpers (`V`, `url`, `transform`)

Introducing a set of helpers to make working with DOM values completely Pythonic, eliminating the need for `RawJS`.

#### V() - Value Reference
Select DOM elements and perform operations directly in Python:

```python
# Concatenation
Button("Combine", on_click=state.fullname.set(
    V("#first") + " " + V("#last")
))

# Transformations
Button("Upper", on_click=state.name.set(V("#name").upper()))
Button("Add", on_click=state.count.set(V("#num1").int() + 10))
```

#### url() - URL Builder
Construct dynamic URLs easily with proper interpolation:

```python
Button("Fetch", on_click=fetch(
    url("https://api.example.com/users/{id}", id=V("#userId"))
))
```

### Stability
- **Fix**: Resolved an issue where reactive bindings could generate duplicate JavaScript variables, causing "Identifier has already been declared" errors during hot reloads or complex state updates.

# Release Notes v1.5.6

> **Enhanced `useDynamic` Support & StateV2 Fixes**

## Installation

```bash
pip install --upgrade dars-framework
```

## What's New

### 1. Expanded `useDynamic` Support for Built-in Components

`useDynamic` now works with **all properties** of built-in components, including:

#### Image & Link Components
```python
# Dynamic image source and alt text
Image(
    src=useDynamic("product.imageUrl"),
    alt=useDynamic("product.name")
)

# Dynamic link href and text
Link(
    href=useDynamic("navigation.url"),
    text=useDynamic("navigation.label")
)
```

#### Boolean Attributes
All boolean attributes now support dynamic binding:
```python
# Dynamic disabled state
Button(
    text="Submit",
    disabled=useDynamic("form.isSubmitting")
)

# Dynamic checked state
Checkbox(
    checked=useDynamic("settings.notifications"),
    label="Enable Notifications"
)

# Dynamic readonly and required
Input(
    value=useDynamic("user.email"),
    readonly=useDynamic("form.isLocked"),
    required=useDynamic("form.emailRequired")
)
```

**Supported Boolean Properties:**
- `disabled` - Button, Input, Textarea, Checkbox, RadioButton, Select, Slider
- `checked` - Checkbox, RadioButton
- `readonly` - Input, Textarea
- `required` - Input, Textarea, Checkbox, RadioButton, Select

### 2. StateV2 `increment()` & `decrement()` Fixes

Fixed critical issues with `StateV2` reactive operations:

#### Fixed Validation Error
Previously, `increment()` and `decrement()` only worked on properties named `text`. Now they work on **any numeric property**:

```python
# Before: This would error
state = State("counter", count=0)
Button("Increment", on_click=state.count.increment(by=1))  # ❌ ValueError

# After: Works perfectly!
state = State("counter", count=0)
Button("Increment", on_click=state.count.increment(by=1))  # ✅ Works!
```

#### Fixed Persistence Issue
Increment/decrement operations now correctly persist across multiple clicks:

```python
state = State("counter", count=0)

# Before: Would increment 0→1, then stay at 1 forever
# After: Correctly increments 0→1→2→3→...
Button("Increment", on_click=state.count.increment(by=1))
Button("Decrement", on_click=state.count.decrement(by=1))
```

**Technical Details:**
- Implemented client-side state value tracking in `window.Dars.getState()`
- State registry now maintains current values for all properties
- `increment()`/`decrement()` use `window.Dars.change()` for proper state updates
- Watchers and UI updates now trigger correctly on every operation

### 3. Documentation Updates

#### Enhanced Hooks Documentation
- Added comprehensive "Supported Properties" table showing which properties work with `useDynamic` for each component type
- Documented boolean attribute support

#### New Component Documentation
Added documentation for visualization components in `components.md`:

**Chart Component:**
```python
import plotly.graph_objects as go

fig = go.Figure(data=[go.Bar(x=['A', 'B', 'C'], y=[1, 3, 2])])
Chart(figure=fig, width="100%", height="400px")
```

**DataTable Component:**
```python
import pandas as pd

df = pd.DataFrame({
    'Name': ['Alice', 'Bob'],
    'Age': [25, 30]
})
DataTable(data=df, theme="striped", page_size=10)
```

## Bug Fixes

### StateV2 Increment/Decrement
- **Issue**: `increment()` raised `ValueError` for non-`text` properties
- **Fix**: Validation now checks if value is numeric (`int` or `float`) instead of checking property name
- **Impact**: All numeric state properties can now use `increment()` and `decrement()`

### StateV2 State Persistence
- **Issue**: Increment operations stuck at first value (0→1, then stayed at 1)
- **Fix**: Implemented proper client-side state tracking and payload structuring
- **Impact**: Reactive operations now work correctly across multiple invocations

## Breaking Changes

None.

---


## What's Next

The enhanced `useDynamic` system and robust StateV2 operations pave the way for more advanced reactive patterns and state management features in future releases.

---

# Release Notes v1.5.5


> **Hooks System Enhanced**: `useDynamic` for built-in components and new `useWatch` hook.

## Installation

```bash
pip install --upgrade dars-framework
```

## What's New

### 1. `useDynamic` for Built-in Components

You can now use `useDynamic` directly in properties of built-in components!

```python
# Bind directly to component props
Text(text=useDynamic("user.name"))
Input(value=useDynamic("user.name"))
Button(text=useDynamic("user.status"))
```

This works for `Text`, `Button`, `Input`, `Textarea`, and more.

### 2. New `useWatch` Hook
Monitor state changes and execute side effects with `useWatch`.

```python
# Global watcher
app.useWatch("cart.total", log("Cart updated!"))

# Page-specific watcher
@route("/cart")
def cart_page():
    page = Page()
    page.useWatch("cart.total", log("Total changed!"))
    return page
```

New methods `app.useWatch()` and `page.useWatch()` make integration seamless.

### 3. Fixes

- Fixed execution order in exporter to ensure reactive bindings are generated correctly.
- Improved state initialization for dynamic props.

---

# Release Notes v1.5.4 (Relaunch from 1.5.3)

> **Hooks System & Reactive Bindings** relaunch with correct license.

## Installation

```bash
pip install --upgrade dars-framework
```

## What's New

### Hooks System - `useDynamic()`

Dars Framework introduces its **first hook** - `useDynamic()` - enabling reactive state bindings in FunctionComponents!

#### Reactive State Bindings

Create components that automatically update when state changes:

```python
from dars.all import *

# Create state
userState = State("user", name="John Doe", email="john@example.com")

# Use useDynamic in FunctionComponent
@FunctionComponent
def UserCard(**props):
    return f'''
    <div {Props.id} {Props.class_name} {Props.style}>
        <h3>{useDynamic("user.name")}</h3>
        <p>{useDynamic("user.email")}</p>
    </div>
    '''

# Render
card = UserCard(id="userCard")

# Update - DOM automatically reacts!
app.add_script(userState.name.set("Jane Doe"))  # UI updates instantly
```

#### How It Works

1. **Initial Render**: `useDynamic()` inserts reactive spans with initial prop values
2. **State Changes**: When you call `.set()`, the hook intercepts the change
3. **Auto Updates**: All matching reactive spans update automatically

#### Key Features

- **Zero boilerplate** - Just use `useDynamic("state.property")  in templates
- **Automatic updates** - No manual DOM manipulation needed
- **Multiple bindings** - Multiple components can bind to the same state
- **State V2 integration** - Works seamlessly with dynamic state system

---

### `getInputValue()` Utility

New utility function specifically designed for State V2 integration:

```python
state = State("product", title="", price=0)

Button("Save", on_click=[
    state.title.set(getInputValue("titleInput")),
    state.price.set(getInputValue("priceInput"))
])
```

**Features:**
- Returns input value as JavaScript expression
- Works with `State.set()` and other dynamic operations
- Optional `parent_id` parameter for scoped searches
- Complements existing `getValue()` for assignments

**Difference from `getValue()`:**
- `getValue(input_id, target_id)` - Performs assignment (sets textContent)
- `getInputValue(input_id)` - Returns value expression (for State.set())

---

### CSS Improvements

#### Modern Default Styles

- Updated all component CSS to use CSS variables for easy theming
- Removed opinionated sizing - better CSS flow and overridability
- Added `accent-color` support for form controls
- Improved transitions and hover effects
- Better disabled states across all components

#### CSS Variables

Components now respect theme colors:

```css
--dars-primary: #007bff;
--dars-spacing-md: 12px;
/* ... and more */
```

#### Better Customization

```python
# Inline styles work better now
Button("Click", style={"width": "200px", "padding": "16px"})

# Global styles via app.add_global_styles()
app.add_global_styles("""
    .dars-button {
        border-radius: 8px;
    }
""")
```

---

### Bug Fixes

#### Fixed Markdown Syntax Highlighting in Multipage Apps

- **Issue**: Prism.js scripts were only injected on first page with Markdown
- **Fix**: Per-page script injection tracking ensures all pages get highlighting(Markdown Component)
- **Impact**: Multipage apps now correctly highlight code on all routes

```python
# Now works correctly across all pages
@route("/docs")
def docs():
    return Page(Markdown(content=code_example))

@route("/tutorial")
def tutorial():
    return Page(Markdown(content=tutorial_code))  # Also highlighted now!
```

---

## Breaking Changes

None! This release is 100% backwards compatible.

---

## Complete Example

**User Profile with Reactive Updates:**

```python
from dars.all import *

app = App("Reactive Profile")

# State for user data
userState = State("user", 
    name="John Doe",
    email="john@example.com"
)

# Reactive display component
@FunctionComponent
def ProfileDisplay(**props):
    return f'''
    <div {Props.id} {Props.class_name} {Props.style}>
        <h2>{useDynamic("user.name")}</h2>
        <p>Email: {useDynamic("user.email")}</p>
    </div>
    '''

# Edit form
def ProfileEditor():
    return Container(
        Input(id="nameInput", value="John Doe"),
        Input(id="emailInput", value="john@example.com"),
        Button("Save", on_click=[
            userState.name.set(getInputValue("nameInput")),
            userState.email.set(getInputValue("emailInput"))
        ])
    )

# Page
@route("/")
def index():
    return Page(
        ProfileDisplay(id="profile"),
        ProfileEditor()
    )

app.add_page("index", index())

if __name__ == "__main__":
    app.rTimeCompile()
```

**Result**: Edit the inputs and click Save - the profile display updates instantly!

---

## Migration Guide

No migration needed! Add `useDynamic()` to new or existing FunctionComponents:

**Before (static):**
```python
@FunctionComponent
def UserCard(name, email, **props):
    return f'<div {Props.id}><h3>{name}</h3><p>{email}</p></div>'
```

**After (reactive):**
```python
@FunctionComponent
def UserCard(**props):
    return f'''
    <div {Props.id}>
        <h3>{useDynamic("user.name")}</h3>
        <p>{useDynamic("user.email")}</p>
    </div>
    '''
```

---

## Documentation

New documentation added:

- **Hooks System** - Complete guide to `useDynamic()` and future hooks
- **`getInputValue()`** - Usage guide in Scripts documentation
- **Updated Examples** - Reactive patterns and best practices

Visit the [Dars Documentation](https://ztamdev.github.io/Dars-Framework/docs.html) for more details.

---

## What's Next

The hooks system opens the door for more reactive features...


# Release Notes v1.5.3

> **Hooks System & Reactive Bindings**

## Installation

```bash
pip install --upgrade dars-framework
```

## What's New

### Hooks System - `useDynamic()`

Dars Framework introduces its **first hook** - `useDynamic()` - enabling reactive state bindings in FunctionComponents!

#### Reactive State Bindings

Create components that automatically update when state changes:

```python
from dars.all import *

# Create state
userState = State("user", name="John Doe", email="john@example.com")

# Use useDynamic in FunctionComponent
@FunctionComponent
def UserCard(**props):
    return f'''
    <div {Props.id} {Props.class_name} {Props.style}>
        <h3>{useDynamic("user.name")}</h3>
        <p>{useDynamic("user.email")}</p>
    </div>
    '''

# Render
card = UserCard(id="userCard")

# Update - DOM automatically reacts!
app.add_script(userState.name.set("Jane Doe"))  # UI updates instantly
```

#### How It Works

1. **Initial Render**: `useDynamic()` inserts reactive spans with initial prop values
2. **State Changes**: When you call `.set()`, the hook intercepts the change
3. **Auto Updates**: All matching reactive spans update automatically

#### Key Features

- **Zero boilerplate** - Just use `useDynamic("state.property")  in templates
- **Automatic updates** - No manual DOM manipulation needed
- **Multiple bindings** - Multiple components can bind to the same state
- **State V2 integration** - Works seamlessly with dynamic state system

---

### `getInputValue()` Utility

New utility function specifically designed for State V2 integration:

```python
state = State("product", title="", price=0)

Button("Save", on_click=[
    state.title.set(getInputValue("titleInput")),
    state.price.set(getInputValue("priceInput"))
])
```

**Features:**
- Returns input value as JavaScript expression
- Works with `State.set()` and other dynamic operations
- Optional `parent_id` parameter for scoped searches
- Complements existing `getValue()` for assignments

**Difference from `getValue()`:**
- `getValue(input_id, target_id)` - Performs assignment (sets textContent)
- `getInputValue(input_id)` - Returns value expression (for State.set())

---

### CSS Improvements

#### Modern Default Styles

- Updated all component CSS to use CSS variables for easy theming
- Removed opinionated sizing - better CSS flow and overridability
- Added `accent-color` support for form controls
- Improved transitions and hover effects
- Better disabled states across all components

#### CSS Variables

Components now respect theme colors:

```css
--dars-primary: #007bff;
--dars-spacing-md: 12px;
/* ... and more */
```

#### Better Customization

```python
# Inline styles work better now
Button("Click", style={"width": "200px", "padding": "16px"})

# Global styles via app.add_global_styles()
app.add_global_styles("""
    .dars-button {
        border-radius: 8px;
    }
""")
```

---

### Bug Fixes

#### Fixed Markdown Syntax Highlighting in Multipage Apps

- **Issue**: Prism.js scripts were only injected on first page with Markdown
- **Fix**: Per-page script injection tracking ensures all pages get highlighting(Markdown Component)
- **Impact**: Multipage apps now correctly highlight code on all routes

```python
# Now works correctly across all pages
@route("/docs")
def docs():
    return Page(Markdown(content=code_example))

@route("/tutorial")
def tutorial():
    return Page(Markdown(content=tutorial_code))  # Also highlighted now!
```

---

## Breaking Changes

None! This release is 100% backwards compatible.

---

## Complete Example

**User Profile with Reactive Updates:**

```python
from dars.all import *

app = App("Reactive Profile")

# State for user data
userState = State("user", 
    name="John Doe",
    email="john@example.com"
)

# Reactive display component
@FunctionComponent
def ProfileDisplay(**props):
    return f'''
    <div {Props.id} {Props.class_name} {Props.style}>
        <h2>{useDynamic("user.name")}</h2>
        <p>Email: {useDynamic("user.email")}</p>
    </div>
    '''

# Edit form
def ProfileEditor():
    return Container(
        Input(id="nameInput", value="John Doe"),
        Input(id="emailInput", value="john@example.com"),
        Button("Save", on_click=[
            userState.name.set(getInputValue("nameInput")),
            userState.email.set(getInputValue("emailInput"))
        ])
    )

# Page
@route("/")
def index():
    return Page(
        ProfileDisplay(id="profile"),
        ProfileEditor()
    )

app.add_page("index", index())

if __name__ == "__main__":
    app.rTimeCompile()
```

**Result**: Edit the inputs and click Save - the profile display updates instantly!

---

## Migration Guide

No migration needed! Add `useDynamic()` to new or existing FunctionComponents:

**Before (static):**
```python
@FunctionComponent
def UserCard(name, email, **props):
    return f'<div {Props.id}><h3>{name}</h3><p>{email}</p></div>'
```

**After (reactive):**
```python
@FunctionComponent
def UserCard(**props):
    return f'''
    <div {Props.id}>
        <h3>{useDynamic("user.name")}</h3>
        <p>{useDynamic("user.email")}</p>
    </div>
    '''
```

---

## Documentation

New documentation added:

- **Hooks System** - Complete guide to `useDynamic()` and future hooks
- **`getInputValue()`** - Usage guide in Scripts documentation
- **Updated Examples** - Reactive patterns and best practices

Visit the [Dars Documentation](https://ztamdev.github.io/Dars-Framework/docs.html) for more details.

---

## What's Next

The hooks system opens the door for more reactive features...

# Release Notes v1.5.2

> **Function Components**

## Installation

```bash
pip install --upgrade dars-framework
```

## What's New

### Function Components System

Dars Framework now features **Function Components** as the primary and recommended way to create custom UI components. This new system provides a clean, Pythonic approach to component creation without the complexity of class inheritance.

#### What are Function Components?

Function Components allow you to create reusable UI elements using simple Python functions with f-string templates. The framework automatically handles IDs, styling, events, and other properties.

**Key Benefits:**
- **Simple & Pythonic**: Just write a function that returns an HTML string
- **No Boilerplate**: No need to inherit from Component class or implement render methods
- **Automatic Property Injection**: Framework handles `id`, `class_name`, `style`, and `children` automatically
- **Linter-Friendly**: Two patterns available to avoid linter warnings
- **State Compatible**: Works seamlessly with State V2 for reactive UIs

#### Basic Usage

```python
from dars.all import FunctionComponent, Props

@FunctionComponent
def UserCard(name, email, **props):
    return f"""
    <div {Props.id} {Props.class_name} {Props.style}>
        <h3>{name}</h3>
        <p>{email}</p>
        <div class="card-body">
            {Props.children}
        </div>
    </div>
    """

# Usage
card = UserCard("John Doe", "john@example.com", id="user-1", style={"padding": "20px"})
```

#### Two Supported Patterns

**Option 1: Using Props Helper (Recommended)**
```python
@FunctionComponent
def MyComponent(**props):
    return f"""
    <div {Props.id} {Props.class_name} {Props.style}>
        {Props.children}
    </div>
    """
```

**Option 2: Explicit Arguments**
```python
@FunctionComponent
def MyComponent(id, class_name, style, children, **props):
    return f"""
    <div {id} {class_name} {style}>
        {children}
    </div>
    """
```

Both patterns are fully supported and avoid linter warnings about undefined variables.

#### Props Helper Class

The new `Props` class provides static constants for framework properties:

```python
Props.id          # "{id}"
Props.class_name  # "{class_name}"
Props.style       # "{style}"
Props.children    # "{children}"
```

These resolve to the correct placeholders that the framework replaces during rendering.

#### State V2 Integration Clarification

**Important Concept:** State V2 updates DOM properties, not arbitrary component arguments.

**Correct Usage:**
```python
@FunctionComponent
def Counter(**props):
    return f"""
    <div {Props.id}>
        Current count: {Props.children}
    </div>
    """

counter = Counter(id="my-counter", children="0")
state = State(counter, text="Current count: 0")

# Updates textContent of the div
Button("Increment", on_click=state.text.set("Current count: 5"))
```

**Why:** Dars exports to static HTML/JS. The JavaScript runtime can only manipulate DOM properties (`textContent`, `style`, `innerHTML`), not re-execute Python functions with new arguments.

# Release Notes v1.5.1

> **Backend HTTP Utilities & Pythonic API Communication**

## Installation

```bash
pip install --upgrade dars-framework
```

## What's New

### Backend HTTP Utilities System

Dars now includes a comprehensive **Pythonic system** for HTTP requests and API communication without writing any JavaScript. The new `dars.backend` module enables you to fetch data, bind it to components, and create reactive UIs entirely in Python.

**Key Features:**
- HTTP functions (get, post, put, delete, patch, fetch)
- `useData()` with dot notation for nested data access
- Seamless StateV2 integration
- `.then()` chaining for sequential operations
- Component management (createComp, updateComp, deleteComp)
- JSON utilities (stringify, parse, get_value)
- **State() string ID support** - Create states for dynamic components

### HTTP Functions

```python
from dars.all import *
from dars.backend import get, post, useData

# GET request with data binding
fetch_btn = Button(
    "Fetch User",
    on_click=get(
        id="userData",
        url="https://api.example.com/users/1",
        callback=name_state.text.set(useData('userData').name)
    )
)

# POST request
submit_btn = Button(
    "Submit",
    on_click=post(
        id="result",
        url="https://api.example.com/submit",
        body={"name": "John", "email": "john@example.com"},
        callback=status_state.text.set("✅ Submitted!")
    )
)
```

### useData() with Dot Notation

Access fetched data using Pythonic dot notation:

```python
# Access nested properties
useData('userData').name           # → window.userData?.name
useData('user').address.city       # → window.user?.address?.city
useData('posts').items[0].title    # → window.posts?.items?.[0]?.title
```

### Chaining with .then()

Chain multiple state updates sequentially:

```python
callback=(
    status_state.text.set("Loading...")
    .then(name_state.text.set(useData('userData').name))
    .then(email_state.text.set(useData('userData').email))
    .then(status_state.text.set("✅ Loaded!"))
)
```

### Component Management

Create, update, and delete components dynamically at runtime:

```python
from dars.backend import createComp, updateComp, deleteComp

# Create new component
create_btn.on_click = createComp(
    target=Text("Hello!", id="new-item"),
    root="container-id",
    position="append"
)

# Update component
update_btn.on_click = updateComp(
    "my-component-id",
    text="Updated!",
    style={"color": "red"}
)

# Delete component
delete_btn.on_click = deleteComp("component-id")
```

### JSON Utilities

Helper functions for working with JSON data:

```python
from dars.backend import stringify, parse, get_value

# Stringify with pretty printing
display_state.text.set(stringify(useData('userData'), pretty=True))

# Parse JSON string
data = parse('{"name": "John"}')

# Safe nested access
city = get_value(useData('userData'), 'address.city', default='Unknown')
```

### State() String ID Support

`State()` now accepts both component objects and string IDs, enabling state management for dynamically created components:

```python
from dars.all import *
from dars.backend import createComp

# Traditional: State with component object
existing_text = Text("0", id="counter")
existing_state = State(existing_text, text=0)

# New: State with string ID (for components created later)
dynamic_state = State("dynamic-counter", text=0)

# Create the component later
create_btn.on_click = createComp(
    target=Text("0", id="dynamic-counter"),
    root="container-id"
)

# State works even though component was created after state!
increment_btn.on_click = dynamic_state.text.increment(by=1)
```

**Use Cases:**
- Components created with `createComp()`
- Dynamically generated UIs
- Conditional component rendering
- Server-side rendered components

## Technical Implementation

### DataAccessor Class

New `DataAccessor` class with:
- `__getattr__` for dot notation support
- `.code` property for RawJS generation
- `.bind()` method for StateV2 integration
- `.get()` method for safe property access

### StateV2 Enhancements

Updated `StateV2._generate_change_call()` to handle `DataAccessor` objects:
- Automatically detects `DataAccessor` instances
- Extracts `.code` property for JavaScript generation
- Seamless integration with existing state management

## Documentation

### New Documentation

**`backend_api.md`** - Comprehensive guide (500+ lines) covering:
- Quick Start examples
- HTTP Functions reference
- Data Binding with useData()
- JSON Utilities
- Component Management
- 3 Advanced Examples
- Best Practices
- Complete API Reference

**Documentation URL:** https://ztamdev.github.io/Dars-Framework/docs.html#backend-http-utilities

## Breaking Changes

**None** - This is a fully backward-compatible release. All existing code continues to work.

## Bug Fixes

- **Fixed**: `StateV2` now correctly handles `DataAccessor` objects in `to_js_value()`
- **Fixed**: `RawJS` objects are properly serialized in state updates
- **Fixed**: `dScript.then()` chaining works correctly with backend operations

## Performance & Compatibility

- **Zero Overhead**: Backend utilities only activate when imported
- **Backward Compatible**: All existing code works without changes
- **Bundle Size**: Minimal impact (+~10KB for backend module)
- **Desktop Support**: Full Electron compatibility maintained

## Migration Guide

No migration needed - this is an additive release. To start using the new features:

```python
# Add to your imports
from dars.backend import get, post, useData

# Start using Pythonic HTTP
button.on_click = get(
    id="data",
    url="https://api.example.com/data",
    callback=state.text.set(useData('data').message)
)
```

---

**This release makes Dars fully self-contained for building reactive, API-driven UIs without writing any JavaScript!**

---

# Release Notes v1.5.0

> **Animation System Stability & Runtime Improvements**

## Installation

```bash
pip install --upgrade dars-framework
```

## What's New

### Animation System Stability

Significant improvements to the animation system's reliability and ease of use:

- **Fixed Infinite Pulse**: `pulse(iterations="infinite")` now works correctly (fixed `TypeError`).
- **Chaining Support**: State updates like `increment()` can now be chained with animations using `.then()` or `sequence()`.
- **Documentation**: Added comprehensive [Animation Guide](https://ztamdev.github.io/Dars-Framework/docs.html#dars-animation-system) to the documentation.

### Dynamic Event Updates

The client-side runtime has been upgraded to fully support dynamic event handler updates:

```python
# This now works perfectly in real-time
button.on_click = state.update(
    text="Clicked!",
    on_click=alert("New handler attached!")
)
```

## Bug Fixes

- **Fixed**: `pulse` animation now correctly handles `iterations="infinite"` (mapped to `Infinity`).
- **Fixed**: `SyntaxError` when chaining state updates (wrapped in async IIFE).

---

# Release Notes v1.4.9

> **Event Handler Support & Dual State System Documentation**

## Installation

```bash
pip install --upgrade dars-framework
```

## What's New

### State V2: Event Handler Support

State V2 now supports updating event handlers:

```python
from dars.all import *

# Update events in State V2
state.update(
    text="Click me",
    on_click=alert("Success!"),
    on_mouseover=dScript("showTooltip()")
)

# Works with dScript objects
button_state.update(on_click=dScript("console.log('clicked')"))
```

**Implementation:**
- Automatic detection of `on_*` properties
- Extracts `.code` from dScript objects  
- Handles arrays of event handlers
- Gracefully skips non-serializable values

### Dual State System Documentation

Documentation now presents **two coexisting state management systems**:

**State V2 (Dynamic)**
- Auto-increment/decrement built-in
- Best for: counters, timers, simple updates

**dState/cState (Indexed)**
- Full state machine support
- Immutable state 0
- Cross-state calls with `Mod.call()`
- Best for: workflows, complex UI transitions

Comprehensive comparison table and use case guidance added to state management documentation.

## Bug Fixes

- **Fixed**: State V2 can now handle dScript event handlers without errors
- **Fixed**: `_generate_change_call()` properly handles non-JSON-serializable values

## Documentation

- Complete restructure of `state_management.md` to include both systems
- Added comparison table for State V2 vs dState/cState
- Restored all original dState/cState documentation
- Added use case recommendations for choosing the right system

---

# Release Notes v1.4.8


> **Critical Fix**: State V2 now properly supports all component properties including `class_name`, `style`, `attrs`, and more.

## Installation

```bash
pip install --upgrade dars-framework
```

or

```bash
pip install dars-framework==1.4.8
```

## What's Fixed

### State V2 Complete Property Support

**Previously (v1.4.7):** State V2 only updated `text` content, incorrectly setting textContent for all properties.

```python
# This didn't work correctly in v1.4.7
counter.class_name.set("active")
```

**Now (v1.4.8):** State V2 properly handles **all component properties** using the `change()` client function.

```python
# All properties now work correctly!
state.text.set("New text")
state.class_name.set("active")
state.style.set({"color": "red"})
state.attrs.set({"title": "Tooltip"})
state.html.set("<strong>Bold</strong>") 
```

### Unified Property Handling

All State V2 methods now use the same `change()` function as `this()` and `dState`, ensuring consistent behavior across the framework:

- `ReactiveProperty.set()` - Works with any property type
- `State.update()` - Updates multiple properties correctly
- `State.reset()` - Resets all property types to defaults

### Validation Improvements

**Increment/Decrement Validation:**
Now properly validates that `increment()` and `decrement()` are only used on numeric properties:

```python
# Correct usage
counter.text.increment(by=1)

# Now throws helpful error
counter.class_name.increment(by=1)
```

## Bug Fixes

### Fixed: Property Type Handling

- **Fixed**: `class_name.set()` now correctly updates element's `className`
- **Fixed**: `style.set()` now correctly updates inline styles
- **Fixed**: `attrs.set()` now correctly updates HTML attributes
- **Fixed**: `html.set()` now correctly updates `innerHTML`
- **Fixed**: `update()` now correctly handles multiple properties simultaneously
- **Fixed**: `reset()` now correctly restores all property types

### Technical Details

**Root Cause:** 
State V2 methods were directly manipulating `el.textContent` instead of using the framework's `change()` function, which properly routes updates based on property type.

**Solution:**
Created `_generate_change_call()` helper that generates proper `change()` payloads:
- `text` → `{text: value}`
- `html` → `{html: value}`
- `style` → `{style: object}`
- `class_name` → `{attrs: {class: value}}` or `{classes: object}`
- `attrs` → `{attrs: object}`

All reactive methods now use this helper for consistent, correct property updates.

## Complete Property Examples

### Setting Different Property Types

```python
from dars.all import *

display = Container(Text("Example"), id="demo")

# Create state with multiple properties
state = State(display, 
    text="Hello",
    class_name="",
    style={"background": "#333"}
)

# Update text
text_btn.on_click = state.text.set("Updated!")

# Update CSS class
class_btn.on_click = state.class_name.set("active highlight")

# Update styles
style_btn.on_click = state.style.set({
    "background": "linear-gradient(135deg, #667eea, #764ba2)",
    "color": "white",
    "padding": "20px"
})

# Update HTML attributes
attr_btn.on_click = state.attrs.set({
    "data-status": "complete",
    "title": "Completed task"
})
```

### Advanced Class Manipulation

```python
# Add/remove specific classes
state.classes.set({
    "add": ["active", "highlight"],
    "remove": ["disabled", "hidden"]
})

# Toggle classes
state.classes.set({
    "toggle": ["expanded"]
})
```

### Update Multiple Properties

```python
# Update several properties at once
success_btn.on_click = state.update(
    text="Success!",
    class_name="success",
    style={"color": "green", "fontSize": "18px"},
    attrs={"data-result": "ok"}
)
```

## Migration from v1.4.7

**No breaking changes** - all existing code continues to work. However, if you tried using non-`text` properties in v1.4.7 and they didn't work, they will now work correctly in v1.4.8.

**If you worked around the limitation:**
```python
# Old workaround (v1.4.7)
from dars.core.state import this
button.on_click = this().state(class_name="active")  # Had to use this()

# Now works directly with State V2 (v1.4.8)
button.on_click = state.class_name.set("active")  # ✅ Works!
```

## Dependency Cleanup

- **Removed**: `rjsmin` dependency (Apache license, replaced with regex fallback)
- **Removed**: `fastapi` dependency (not used in framework)

JS/CSS minification now uses:
1. Vite (if available)
2. esbuild (if available)
3. Regex fallback (always available, no external dependencies)

## Performance & Compatibility

- **Zero overhead**: Property handling uses existing `change()` infrastructure
- **Backward compatible**: All v1.4.7 code works in v1.4.8
- **Consistent behavior**: State V2, `this()`, and dState now all use same property system
- **Desktop support**: Full Electron compatibility maintained

---

**Upgrade highly recommended** for all projects using State V2, especially if you need to update component properties beyond just `text`.

---

# Release Notes v1.4.7


> Introducing State V2 and comprehensive animation system. This is the biggest update to Dars state management, bringing a pure Pythonic API and 15+ built-in animations.

## Installation

```bash
pip install --upgrade dars-framework
```

or

```bash
pip install dars-framework==1.4.7
```

## What's New

### State V2 - Pure Pythonic State Management

**New `State` Class:**
- Pure Python API - no more verbose dState syntax
- Direct property access with reactive operations
- Built-in auto-increment/auto-decrement operations
- Clean reset functionality
- Seamless animation integration

**Before (dState - deprecated):**
```python
from dars.core.state import dState, Mod

display = Text("0", id="counter")
st = dState("counter", component=display, states=[0, 1, 2])
st.cState(1, mods=[Mod.inc(display, prop='text', by=1)])
button.on_click = st.state(1)
```

**After (State V2 - recommended):**
```python
from dars.all import State

display = Text("0", id="counter")
counter = State(display, text=0)
button.on_click = counter.text.increment(by=1)
```

**Key Features:**
- **Reactive Properties**: Direct access with `state.property.operation()`
- **Auto Operations**: Continuous operations with `auto_increment()`, `auto_decrement()`
- **Reset**: Simple `state.reset()` to restore initial values
- **Intuitive**: Pythonic API that feels natural

**Usage:**
```python
from dars.all import *

# Create component and state
timer_display = Text("0", id="timer", style={"font-size": "36px"})
timer = State(timer_display, text=0)

# Auto-incrementing timer
start_btn.on_click = timer.text.auto_increment(by=1, interval=1000)
stop_btn.on_click = timer.text.stop_auto()
reset_btn.on_click = timer.reset()
```

### Comprehensive Animation System

**15+ Built-in Animations:**
- `fadeIn` / `fadeOut` - Opacity transitions
- `slideIn` / `slideOut` - Position-based slides (8 directions)
- `scaleIn` / `scaleOut` - Size transformations
- `shake` - Shake effect for alerts
- `bounce` - Bounce effect
- `pulse` - Heartbeat/pulse effect
- `rotate` - Rotation animations
- `flip` - Flip on X/Y axis
- `colorChange` - Color transitions
- `morphSize` - Size morphing
- `sequence` - Chain multiple animations

**Animation Chaining:**
```python
from dars.all import *

button.on_click = sequence(
    fadeIn(id="box", duration=400),
    pulse(id="box", scale=1.2, iterations=2),
    shake(id="box", intensity=5)
)
```

**Integration with State V2:**
```python
button.on_click = sequence(
    counter.text.increment(by=1),
    pulse(id="counter", scale=1.2),
    fadeOut(id="counter", duration=200),
    counter.text.set(value=0),
    fadeIn(id="counter", duration=200)
)
```

**All Animations:**
- Return `dScript` objects for chaining
- Customizable duration, easing, and parameters
- Proper async completion handling
- Work seamlessly with event handlers

### Professional State V2 Template

**New Example Template:**
- Located in `dars/templates/examples/advanced/StateV2/`
- Professional, production-ready demonstration
- Function component pattern (LandingPage style)
- Comprehensive showcases:
  - Interactive counter with increment/decrement
  - Auto-incrementing timer
  - Animation showcase with 15+ animations
  - State management best practices
- Responsive design with modern styling
- Complete documentation and code examples

**Template Structure:**
```
dars/templates/examples/advanced/StateV2/
├── index.py                 # Main application
├── hero_component.py        # Hero section
├── counter_component.py     # Counter demo
├── timer_component.py       # Timer demo
├── animation_component.py   # Animation showcase
├── styles.css              # Global styles
└── README.md               # Documentation
```

## Breaking Changes

**dState/cState Deprecation:**
- `dState` and `cState` are now deprecated
- All functionality replaced by State V2
- Legacy code still works for backward compatibility
- Migration path provided in updated documentation
- New projects should use State V2 exclusively

## Documentation Updates

**Updated Files:**
- `state_management.md` - Completely rewritten for State V2
- `scripts.md` - Added comprehensive animation system documentation
- All dState/cState references removed from active docs
- Migration guides included for existing projects

## Bug Fixes

**Animation System:**
- Fixed animation chaining with proper Promise handling
- Fixed initial state rendering with `transition='none'` pattern
- Fixed `sequence()` function trailing semicolon issue
- All animations now properly await completion
- Animations use `setTimeout(20ms)` for reliable state application

**State Operations:**
- `auto_increment` and `auto_decrement` now return proper `dScript` objects
- Client-side loop management with `startLoop` and `stopLoop`
- Proper cleanup of active loops

## Technical Improvements

### Animation Implementation

- All animations wrapped in async IIFEs
- Proper transition timing with `setTimeout`
- Force reflow with `void el.offsetWidth`
- Set `transition='none'` before initial styles
- `animation.finished` for Web Animations API
- Proper Promise chaining in `sequence()`

## Migration Guide

### From dState to State V2

**1. Import Changes:**
```python
# Old
from dars.core.state import dState, Mod

# New
from dars.all import State
```

**2. State Creation:**
```python
# Old
counter_state = dState("counter", component=display, states=[0, 1, 2])
counter_state.cState(1, mods=[Mod.inc(display, prop='text', by=1)])

# New
counter = State(display, text=0)
```

**3. Event Handlers:**
```python
#Old
button.on_click = counter_state.state(1)

# New
button.on_click = counter.text.increment(by=1)
```

**4.Auto Operations (New Feature):**
```python
# Only available in State V2
start_btn.on_click = timer.text.auto_increment(by=1, interval=1000)
stop_btn.on_click = timer.text.stop_auto()
```

### Adding Animations

```python
from dars.all import fadeIn, pulse, sequence

# Simple animation
button.on_click = fadeIn(id="element", duration=500)

# Chained animations
button.on_click = sequence(
    fadeIn(id="box"),
    pulse(id="box", scale=1.1)
)
```

## Performance & Compatibility

- **Zero Overhead**: State V2 only activates when used
- **Backward Compatible**: dState still works for existing code
- **Bundle Size**: Minimal impact (+~15KB for animations)
- **Desktop Support**: Full Electron compatibility

## Examples

### Complete Counter App

```python
from dars.all import *

app = App("Counter Demo")

# Create display with state
counter_display = Text("0", id="counter", style={
    "font-size": "48px", 
    "color": "#2563eb"
})
counter = State(counter_display, text=0)

# Buttons with operations
inc_btn = Button("+1", on_click=counter.text.increment(by=1))
dec_btn = Button("-1", on_click=counter.text.decrement(by=1))
reset_btn = Button("Reset", on_click=counter.reset())
pulse_btn = Button("Pulse", on_click=pulse(id="counter", scale=1.2))

page = Page(Container(counter_display, inc_btn, dec_btn, reset_btn, pulse_btn))
app.add_page("index", page, index=True)
app.rTimeCompile()
```

### Auto-Incrementing Timer

```python
from dars.all import *

app = App("Timer Demo")

timer_display = Text("0", id="timer")
timer = State(timer_display, text=0)

start_btn = Button("Start", on_click=timer.text.auto_increment(by=1, interval=1000))
stop_btn = Button("Stop", on_click=timer.text.stop_auto())
reset_btn = Button("Reset", on_click=timer.reset())

page = Page(Container(timer_display, start_btn, stop_btn, reset_btn))
app.add_page("index", page, index=True)
app.rTimeCompile()
```

## Desktop Exporter Status

**Still in BETA** - State V2 and animations fully supported in both web and desktop exports.

---

**This is a landmark release** - State V2 represents the future of Dars state management. Upgrade highly recommended for all projects.

---

# Release Notes v1.4.6


> **Major Feature Release**: Introduces Single Page Application (SPA) support and a powerful client-side routing system.

## Installation

```bash
pip install --upgrade dars-framework
```

or

```bash
pip install dars-framework==1.4.5
```

## What's New

### Single Page Application (SPA) Support

**New Routing System:**
- **Client-Side Routing**: Build fast, responsive SPAs with Python.
- **Nested Routes & Layouts**: Create complex UI hierarchies using the `parent` parameter and the new `Outlet` component.
- **Persistent Layouts**: Keep headers, sidebars, and navigation bars active while content changes dynamically.

**Robust Error Handling:**
- **Automatic 404 Handling**: Dars now automatically redirects invalid routes to a 404 page.
- **Default & Custom 404**: Includes a built-in clean 404 page, or define your own with `app.set_404_page()`.

### Developer Experience

**Hot Reload Stability:**
- **Intelligent Polling**: New hot reload system for SPAs that detects changes without spamming logs.
- **Auto-Stop**: Prevents browser lag by stopping polling after 10 consecutive connection failures.

### Fixes & Improvements

- **SPA Export**: Fixed issues where SPA child routes were conflicting with multipage exports.
- **Preview Server**: Improved handling of SPA routes and query parameters.
- **Assets**: Enforced absolute paths for SPA assets to ensure correct loading from any depth.

---


# Release Notes v1.4.4

> Critical bug fix release. Removes non-functional features, fixes style merge, and improves state restoration.

## Installation

```bash
pip install --upgrade dars-framework
```

or

```bash
pip install dars-framework==1.4.4
```

## What's Fixed

- **Style Merge Fix (CRITICAL)** - `Mod.set()` now correctly merges style properties
- **Removed `this().goto()`** - Non-functional feature removed; use `state.state()` instead
- **Fixed Syntax Warning** - Corrected invalid escape sequence in `js_lib.py`
- **Improved State 0 Restoration** - Event handlers now re-attach when returning to default state

---

# Release Notes v1.4.3 (DEPRECATED)

> State management enhancements with compile-time validation, component self-navigation, and critical style merge fix. Improves developer experience and fixes property replacement bug.

## Installation

```bash
pip install --upgrade dars-framework
```

or

```bash
pip install dars-framework==1.4.3
```

## What's New

- **`this().goto(idx)`** - Component self-navigation for state transitions
- **`this_for(id)`** - Compile-time validation helper for state navigation
- **Style Merge Fix** - Critical fix: `Mod.set()` now merges style properties instead of replacing them
- **Enhanced Documentation** - Guides for state management patterns

---

# Release Notes v1.4.2

> New utility dScript functions added to `utils_ds` for enhanced client-side interactions.

## Installation

```bash
pip install --upgrade dars-framework
```

or

```bash
pip install dars-framework==1.4.2
```

## What's New

### Utility Functions (`utils_ds`)

- `setTimeout(delay: int, code: dScript)`: Execute a dScript after a delay (ms).
- `setText(id: str, text: str)`: Set the text content of an element.
- `showModal(id: str)`, `hideModal(id: str)`: Modal visibility helpers.
- `goTo(href: str)`, `goToNew(href: str)`, `reload()`, `goBack()`, `goForward()`: Navigation utilities.
- `alert(message: str)`, `confirm(message: str, on_ok: str = "", on_cancel: str = "")`, `log(message: str)`: Alert & console utilities.
- `show(id: str)`, `hide(id: str)`, `toggle(id: str)`, `addClass(id: str, class_name: str)`, `removeClass(id: str, class_name: str)`, `toggleClass(id: str, class_name: str)`: DOM manipulation utilities.
- `scrollTo(x: int = 0, y: int = 0)`, `scrollToTop()`, `scrollToBottom()`, `scrollToElement(id: str)`: Scroll utilities.
- `submitForm(form_id: str)`, `resetForm(form_id: str)`, `getValue(input_id: str, target_id: str)`, `clearInput(input_id: str)`: Form utilities.
- `saveToLocal(key: str, value: str)`, `loadFromLocal(key: str, target_id: str)`, `removeFromLocal(key: str)`, `clearLocalStorage()`: Storage utilities.
- `copyToClipboard(text: str)`, `copyElementText(id: str)`: Clipboard utilities.
- `focus(id: str)`, `blur(id: str)`: Focus utilities.

These functions are documented in `https://ztamdev.github.io/Dars-Framework/docs.html#dars-script-system` and for states in `https://ztamdev.github.io/Dars-Framework/docs.html#state-management-in-dars-dstate-cstate-goto-mods`.

---

# Release Notes v1.4.1

> SEO and Apple device optimizations. Enhanced metadata generation with automatic MIME type detection for favicons and comprehensive iOS/Safari support.

## Installation

```bash
pip install --upgrade dars-framework
```

or

```bash
pip install dars-framework==1.4.1
```

## What's New

### Automatic Favicon MIME Type Detection

**Smart Icon Type Recognition:**
- Favicon links now automatically detect and use the correct MIME type based on file extension
- Supports PNG, ICO, SVG, JPG/JPEG, WebP, and GIF formats
- No manual type specification needed
- Eliminates incorrect `image/x-icon` type for PNG files

**Before (v1.4.0):**
```html
<link rel="icon" href="logo.png" type="image/x-icon">  <!-- Incorrect! -->
```

**After (v1.4.1):**
```html
<link rel="icon" href="logo.png" type="image/png">  <!-- Correct! -->
```

### Enhanced Apple Device Support

**New App Properties:**
- `apple_mobile_web_app_capable` - Enable fullscreen mode when added to home screen
- `apple_mobile_web_app_status_bar_style` - Control status bar appearance:
  - `"default"` - Standard iOS status bar
  - `"black"` - Black status bar
  - `"black-translucent"` - **Transparent status bar** (solves Safari iOS 16+ solid color issue)
- `apple_mobile_web_app_title` - Custom title for home screen icon

**Usage:**
```python
app = App(
    title="My App",
    favicon="logo.png",
    apple_touch_icon="logo.png",
    apple_mobile_web_app_capable=True,
    apple_mobile_web_app_status_bar_style="black-translucent",  # Enables transparency!
    apple_mobile_web_app_title="MyApp"
)
```

### Safari 15+ Theme Color Enhancements

**Adaptive Theme Colors:**
- Theme color now includes media query variants for light/dark mode
- Proper integration with iOS system appearance settings
- **Fixes Safari iOS 16+ transparency issues** where solid colors blocked background visibility

**Generated Meta Tags:**
```html
<meta name="theme-color" content="#0d1513">
<meta name="theme-color" media="(prefers-color-scheme: light)" content="#0d1513">
<meta name="theme-color" media="(prefers-color-scheme: dark)" content="#0d1513">
```

### Improved Apple Touch Icon

**Multiple Size Specifications:**
- Apple touch icon now includes size attribute for better iOS home screen quality
- Generates both standard and 180x180 sized icon links

**Generated Links:**
```html
<link rel="apple-touch-icon" href="logo.png">
<link rel="apple-touch-icon" sizes="180x180" href="logo.png">
```

### Modern Mobile Web App Meta Tag

**Standards Compliance:**
- Added `mobile-web-app-capable` meta tag alongside `apple-mobile-web-app-capable`
- Eliminates deprecation warnings in modern browsers
- Maintains backward compatibility with older iOS versions

**Generated Meta Tags:**
```html
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-capable" content="yes">
```

## Technical Improvements

### Exporter Enhancements (`dars/exporters/web/html_css_js.py`)

- **New `_detect_icon_mime_type()` Helper**: Automatically detects MIME types from file extensions
- **Enhanced `_generate_meta_tags()`**: Adds Apple-specific meta tags and theme-color variants
- **Updated `_generate_links()`**: Applies automatic MIME detection and sizes attribute

### App Class Updates (`dars/core/app.py`)

- Added 3 new initialization parameters for Apple mobile web app support
- Properties auto-initialize with sensible defaults (`apple_mobile_web_app_title` defaults to app title)
- All new properties are **optional** and **backward compatible**

## Migration Notes

### For Existing Projects

**Automatic Upgrade:**
- No configuration changes required
- Favicons automatically get correct MIME types
- Theme colors automatically include light/dark variants
- All new features are opt-in

**Optional iOS Enhancement:**
```python
# Add to your App initialization
app = App(
    # ... existing params ...
    apple_mobile_web_app_capable=True,
    apple_mobile_web_app_status_bar_style="black-translucent",
    apple_mobile_web_app_title="MyApp"
)
```

## SEO & Performance Impact

- **Improved SEO**: Correct MIME types and proper meta tags
- **Better Mobile Indexing**: Enhanced metadata for mobile search results
- **iOS User Retention**: Superior home screen experience encourages app-like usage

## Desktop Exporter Status

**Still in BETA** - No changes from v1.4.0

---

**Upgrade Highly Recommended** for all projects, especially those targeting iOS/Safari users or requiring proper favicon MIME types.

# Release Notes v1.4.0

> Simple Template update.

## Installation

```bash
pip install --upgrade dars-framework
```

or

```bash
pip install dars-framework==1.4.0
```

## Notes:

All advanced and basic templates are now updated using the new features.

# Release Notes v1.3.9

> Desktop File System API, Pythonic Arg helper, keyboard event filtering, and comprehensive template synchronization. Major enhancements to desktop capabilities with improved developer experience.

## Installation

```bash
pip install --upgrade dars-framework
```

or

```bash
pip install dars-framework==1.3.9
```

## What's New

### Desktop File System API - `list_directory`

**Comprehensive Directory Listing:**
- New `list_directory()` function for browsing files and folders
- Optional glob pattern filtering (e.g., `"*.py"` for Python files only)
- Optional `include_size` parameter (default: False) to show/hide file sizes
- Full integration with `get_value()` for dynamic paths from inputs
- Seamless chaining with `dScript.then()` for UI updates
- Returns array of `{name, isDirectory, size?}` objects

**Usage:**
```python
from dars.desktop import list_directory, get_value
from dars.core.state import this

# Simple directory listing
Button("List", 
    on_click=list_directory(get_value("path")).then(
        this().state(id="output", html=RawJS("value.map(f => f.name).join('<br>')"))
    )
)

# Filter by pattern
Button("Python Files",
    on_click=list_directory(".", "*.py").then(
        this().state(id="count", text=RawJS("`Found ${value.length} files`"))
    )
)

# Include file sizes
list_directory(".", "*", include_size=True)
```

### Pythonic `Arg` Helper

**Cleaner dScript.ARG Access:**
- New `Arg` singleton for Pythonic access to `dScript.ARG`
- More readable than `RawJS("dScript.ARG")`
- Provides helper methods like `.map()`, `.join()`, `.length`, etc.
- Auto-generates proper JavaScript code
- Exported in `dars.all` for easy access

**Usage:**
```python
from dars.scripts.dscript import Arg

# Old way (still works)
this().state(text=RawJS("dScript.ARG.map(f => f.name).join('\\n')"))

# New Pythonic way
this().state(text=Arg.map("f => f.name").join("\\n"))

# Properties
Arg.length  # -> "dScript.ARG.length"
Arg.value   # -> "dScript.ARG.value"

# Methods
Arg.map("f => f.name")  # -> "dScript.ARG.map(f => f.name)"
Arg.filter("x => x > 0")  # -> "dScript.ARG.filter(x => x > 0)"
```

### Enhanced Keyboard Event Filtering

**Specific Key Event Handlers:**
- New keyboard event constants for specific keys (e.g., `KEY_DOWN_ENTER`, `KEY_DOWN_ESCAPE`)
- Event type parsing with `.` delimiter for key filtering (e.g., `"keydown.Enter"`)
- Proper event delegation with key matching
- Works across all event attachment mechanisms
- Backward compatible with existing keyboard events

**New Event Constants:**
```python
from dars.core.events import EventTypes

# Specific Enter key events
on_keydown_enter    # Triggered only when Enter is pressed
on_keyup_enter      # Triggered only when Enter is released

# Specific Escape key events  
on_keydown_escape   # Triggered only when Escape is pressed
on_keyup_escape     # Triggered only when Escape is released

# Usage
Input(
    id="search",
    on_keydown_enter=search_action,  # Only fires on Enter
    on_keydown_escape=clear_action   # Only fires on Escape
)
```

### Configurable DevTools

**Electron DevTools Control:**
- New `devtools` parameter in `App` class (default: `True`)
- Respects `DARS_DEV` and `DARS_DEVTOOLS` environment variables
- DevTools only open when both conditions met: dev mode + devtools enabled
- Better control over development environment
- Applies to all Electron generation methods

**Usage:**
```python
# Disable DevTools even in dev mode
app = App(
    title="My App",
    desktop=True,
    devtools=False  # Won't open DevTools
)

# Default behavior (DevTools enabled)
app = App(
    title="My App",
    desktop=True
)
```

### Dynamic Form Element Updates

**Fixed `change` Function:**
- Corrected dynamic text updates for form elements
- Uses `.value` for `Input`, `Textarea`, `Select`
- Uses `.textContent` for other elements (Text, Button, etc.)
- Ensures UI updates properly reflect state changes
- Fixed issue where form input values weren't updating

### Improved Event Delegation

**Keyboard Event Fix:**
- Fixed event delegation for key-filtered keyboard events
- Properly checks both base event name and filtered event name in eventMap
- Ensures `keydown.Enter` and similar events work correctly
- Maintains backward compatibility with non-filtered events

## Bug Fixes

- Fixed `change` function to use `.value` for form elements instead of `.textContent`
- Fixed event delegation to properly handle key-filtered keyboard events like `keydown.Enter`
- Fixed ElectronExporter default templates to include latest IPC handlers
- Fixed CLI template generation to include all current File System API functions

## Improved

- Enhanced developer experience with configurable DevTools
- Cleaner syntax with `Arg` helper for dScript.ARG access
- More powerful keyboard event handling with key-specific filtering

## Migration Guide

### From v1.3.8 to v1.3.9

No breaking changes. You can upgrade safely:

```bash
pip install --upgrade dars-framework
```

**Optional: Use new features**

1. **Use `list_directory` for file browsing:**
```python
from dars.desktop import list_directory, get_value

Button("Browse", 
    on_click=list_directory(get_value("dir")).then(...)
)
```

2. **Use `Arg` helper for cleaner code:**
```python
from dars.scripts.dscript import Arg

# Instead of RawJS("dScript.ARG.map(...)") 
text=Arg.map("x => x.name").join("\\n")
```

3. **Use specific keyboard events:**
```python
Input(
    on_keydown_enter=submit_action,
    on_keydown_escape=cancel_action
)
```

## Documentation

- Updated Desktop exporter documentation with File System API examples
- Added `Arg` helper documentation in scripts section
- Enhanced keyboard events documentation with key-specific examples

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


# Release Notes v1.3.6

> Compile-time and runtime component manipulation. Introduces `app.create()` / `app.delete()` for pre-export tree editing, and `createComp()` / `deleteComp()` for dynamic DOM operations with safe event hydration.

## Installation

```bash
pip install --upgrade dars-framework
```

or

```bash
pip install dars-framework==1.3.6
```

## What's New

### Compile-Time Component Manipulation

- `app.create(target, root=None, on_top_of=None, on_bottom_of=None)`
  - Inserts components before/after a reference child or at the end of the `root`.
  - Accepts `target` as an instance, a callable, or a `str` (id to move an existing component).
  - Multipage support: `root` can be a component id, a component instance, or a page name.
- `app.delete(id)`
  - Removes a component by id from the tree before export (no-op if not found).

### Runtime Component Manipulation

- `createComp(target, root, position='append')`
  - Generates a `dScript` that calls `Dars.runtime.createComponent(root_id, vdom_data, position)`.
  - Serializes the Python component to VDOM and rehydrates events for the subtree.
  - Positions: `append`, `prepend`, `before:<id>`, `after:<id>`.
- `deleteComp(id)`
  - Generates `dScript` that calls `Dars.runtime.deleteComponent(id)`.

### Event Hydration for Dynamic Content

- Event rehydration for the newly created subtree (supports arrays of handlers).
- Every dynamic node with an `id` also gets `class="dars-id-<id>"` for reliable selection when multiple instances exist.

### Barrel Import

- `from dars.all import *` now includes `createComp` and `deleteComp` from `dars.backend`.


# Release Notes v1.3.5

> Enhanced styling and development experience update featuring active styles, improved preview system, and advanced file monitoring. Delivers better visual feedback and faster development workflow.

## Installation

```bash
pip install --upgrade dars-framework
```

or

```bash
pip install dars-framework==1.3.5
```

## What's New

### Active Styles Support

**Complete Component Styling System:**
- New `active_style` attribute for all components, providing visual feedback during user interaction
- Completes the styling triad: `style`, `hover_style`, and `active_style`
- Works seamlessly with existing hover styles introduced in v1.3.4

**Usage:**
```python
Button("Click it",
        id="btn1",
        on_click=[dScript('console.log(`HI`)'), txtstate.state(1)],
        style={"color": "green"},
        hover_style={"color": "red"},      # from v1.3.4
        active_style={"color": "purple"},  # new in v1.3.5
)
```

### Enhanced Preview System

**Optimized Development Server:**
- Completely redesigned preview system with faster load times
- Improved hot reload support for instant code changes
- Better error handling and cleanup processes
- Enhanced Ctrl+C handling for smooth server shutdown

### Advanced File Watcher

**Comprehensive Project Monitoring:**
- New file watching system monitors file creation, deletion, and modification
- Automatic detection of new files in the project directory
- Supports multiple file extensions (.py, .js, .css, etc.)
- Real-time updates without manual intervention

## Fixed Issues

### Responsiveness Improvements
- **Landing Page**: Fixed responsiveness issues on smaller screens
- **Mobile Compatibility**: Enhanced display and interaction on mobile devices

## Technical Improvements

### Development Experience
- **Faster Hot Reload**: Reduced reload intervals and improved change detection
- **Better Error Recovery**: Enhanced error handling during file changes
- **Clean Shutdown**: Improved server termination and resource cleanup

## Migration Notes

### For Existing Projects

**Seamless Upgrade:**
- No breaking changes - all existing code remains compatible
- Active styles can be added incrementally to enhance user interaction

## Desktop Exporter Status

**Still in BETA**

# Release Notes v1.3.4

> Enhanced interactivity update featuring hover styles, multi-handler events, and runtime versioning. Improves component styling and event handling flexibility.

## Installation

```bash
pip install --upgrade dars-framework
```

or

```bash
pip install dars-framework==1.3.4
```

## What's New

### Hover Styles Support

**Enhanced Component Interactivity:**
- New `hover_style` attribute for all components, allowing dynamic styling on mouse hover
- Styles are automatically generated with higher specificity to ensure proper application

### Multi-Handler Event System

**Flexible Event Management:**
- Components now support arrays of event handlers for the same event type
- Multiple `dScript`, inline JavaScript, or mixed handlers can be assigned to single events
- Handlers execute in sequence with individual error handling
- Full backward compatibility with existing single-handler syntax

### Runtime Versioning

**Enhanced Debugging & Tracking:**
- JavaScript runtime now includes version information accessible via `Dars.version`
- Release URL exposed through `Dars.releaseUrl` for quick reference
- Better debugging and environment identification
- Framework version tracking in deployed applications

**Usage:**
```javascript
// Access version information
console.log(`Using Dars v${Dars.version}`);
console.log(`Release: ${Dars.releaseUrl}`);
```

## Technical Improvements

### Web Exporter Enhancements
- **Improved Style Application**: Fixed CSS generation to ensure all component styles render correctly
- **Robust Event Serialization**: Enhanced handler extraction and code generation for reliable event execution
- **Better Error Handling**: Individual error catching for multi-handler events prevents cascade failures

### Component System
- **Backward Compatibility**: All existing single-handler events continue working unchanged
- **Enhanced Flexibility**: Mix and match handler types (dScript, strings, arrays) with consistent behavior
- **Cleaner Code Generation**: Improved JavaScript output with proper handler separation and error boundaries

## Migration Notes

### For Existing Projects

**Automatic Upgrade:**
- No breaking changes - existing code works identically
- Hover styles can be incrementally added to enhance existing components
- Multi-handler events are optional - single handlers remain fully supported

## Desktop Exporter Status

**Still in BETA** - No changes from v1.3.3

## Performance & Compatibility

- **Zero Overhead**: New features only activate when used
- **Bundle Size**: Minimal impact on final application size
- **Browser Support**: Maintains full cross-browser compatibility
- **Framework Integration**: Seamless with existing Dars ecosystem

---

**Upgrade Recommended** for all projects requiring enhanced interactivity and better development tooling.

# Release Notes v1.3.3

> Minor update featuring new semantic Section component and enhanced state serialization. Continues JavaScript migration improvements from v1.3.2.

## Installation

```bash
pip install --upgrade dars-framework
```

or

```bash
pip install dars-framework==1.3.3
```

## What's New

### Section Component

**Semantic HTML Container:**
- New `Section` component that renders as `<section></section>` instead of generic `<div>`
- Maintains all functionality of Container component (children, styles, etc.)
- Improves HTML readability and semantic structure for debugging
- Better accessibility and SEO through proper sectioning elements

**Usage:**
```python
# Creates <section> with all container capabilities
Section(Button("HI"), styles={...})
```

### Enhanced State & Event Serialization

**Complete JavaScript Migration:**
- States are now fully serialized in JavaScript and no longer exposed in HTML
- Final migration of both state and event systems to pure JavaScript
- Eliminates need for state/event data in VDOM structure
- Improved security and cleaner HTML output

**Benefits:**
- More secure: State data hidden from direct HTML inspection
- Cleaner markup: Reduced data attributes in rendered HTML
- Better performance: Streamlined state management
- Enhanced minification: Better compatibility with Vite optimization

### Documentation Updates

- Updated documentation to reflect new Section component usage
- Enhanced examples and best practices for semantic HTML
- Migration guides for state serialization changes

## Technical Improvements

- **Backward Compatible**: No breaking changes to existing components
- **Progressive Enhancement**: Existing containers continue working as before
- **Performance**: Maintains all optimizations from v1.3.2

## Migration Notes

### For Existing Projects

**Automatic Upgrade:**
- No configuration changes required
- Existing container components remain unchanged
- State management automatically uses new serialization

**Optional Section Component Adoption:**
```python
# Old way (still works)
Container(children=[...])

# New semantic way
Section(children=[...])
```

## Desktop Exporter Status

**Still in BETA** - No changes from v1.3.2

## Known Issues

- None introduced in this release
- Continuing to monitor Electron desktop exporter stability

---

# Release Notes v1.3.2

> Major minification improvements with combined JS files and optimized event handling. Electron desktop exporter remains in beta.

## Installation

```bash
pip install --upgrade dars-framework
```

or

```bash
pip install dars-framework==1.3.2
```

## Highlights

### Enhanced Minification System

**Combined JavaScript Bundles:**
- When `viteMinify: true` and `bundle: true` are enabled, the exporter now combines all JavaScript files into single optimized bundles
- Single-page apps: All JS combined into `app.js`
- Multi-page apps: Each page gets its own `app_{slug}.js` bundle
- Eliminates reference issues between separate files during minification

**Optimized Event Handling:**
- Events are no longer stored in VDOM tree
- Event handlers are now generated as valid JavaScript directly in runtime
- Improved compatibility with Vite minification and obfuscation
- Better performance and smaller bundle sizes

**Smart File Management:**
- When using combined bundles, individual files (`runtime_dars.js`, `script.js`, `vdom_tree.js`) are not generated
- HTML files are updated to reference only the combined bundle
- Backward compatible - falls back to separate files when `viteMinify: false`

### Vite Minification Perfection

- Vite can now minify the entire application as a single cohesive unit
- Resolves function reference issues that previously broke minification
- Proper obfuscation of all JavaScript code, including event handlers
- Maintains full functionality while significantly reducing bundle size

### Configuration-Driven Behavior

```json
{
  "viteMinify": true,
  "bundle": true,
  "defaultMinify": true
}
```

- **viteMinify**: Enables advanced Vite-based minification with combined bundles
- **bundle**: Required for production-optimized builds
- **defaultMinify**: Fallback minification when Vite is unavailable

## Bug Fixes

- **Fixed**: Vite minification breaking function references between separate JS files
- **Fixed**: Event handlers not being properly minified and obfuscated
- **Improved**: Multi-page application build performance

## Desktop Exporter Status

**Desktop Exporter remains in BETA**

While the web exporter is now stable and production-ready, the Electron desktop exporter continues in beta due to:

- Ongoing refinement of native API integrations
- Cross-platform packaging and signing requirements
- Advanced IPC and system integration features still in development

**Current Desktop Capabilities:**
- Basic file system operations (`read_text`, `write_text`)
- Development mode with hot reload
- Production packaging still experimental

## Migration Notes

### For Existing Projects

**No breaking changes** - existing configurations continue to work. To benefit from the new minification:

1. Update your `dars.config.json`:
```json
{
  "viteMinify": true,
  "bundle": true
}
```

2. Run `dars build` or `dars export` as usual

### Performance Improvements

- **Bundle Size**: Up to 40% reduction in minified JavaScript
- **Load Time**: Faster initial page loads with combined bundles
- **Runtime Performance**: Better optimized event handling
- **Build Time**: More efficient minification process

## Known Issues

- Electron desktop apps may require additional configuration for native module support
- Some edge cases in complex component trees being investigated

## Next Steps

We're working on:
- **v1.4.0**: Production-ready Electron desktop exporter
- **v1.5.0**: Advanced native desktop APIs and system integrations
- **Future**: Plugin system and extended component library

---

# Release Notes v1.3.1 BETA

> Native desktop functions and DX improved with dev mode and file system integration.

## Installation

```bash
pip install --upgrade dars-framework
```

or

```bash
pip install dars-framework==1.3.1
```

## Highlights

### Native Functions

You can acces native functions via `dars.desktop` module:

```python
from dars.desktop import *
```

With this module you can acces for now 2 main functions:

```python 
write_text("./app/lib/hello.txt", "Hello Text")
```
and

```python
read_text("./app/lib/hello.txt")
```

This two functions allows you to read and write text files in your desktop application filesystem, both returns an dScript() with the code to be executed in the desktop app, and also the 2 functions can be used in events of any component.

Also you can use dScripts to run custom javascript code in the desktop app. and for now 'dars dev' is supported but python main.py with rTimeCompile() is not supported because it have issues with relative paths.

## Bug Fixes

- Fixed dev failures with hot reload using desktop format.

## Notes(Warning)

- This feature set is **BETA**. Many options (signing, advanced IPC, updates, and deeper configuration) are still evolving.
- Usable for internal tools and early testing. Not recommended for production deployment yet.
- Expect changes to configuration keys and defaults in future versions.


# Release Notes v1.3.0 BETA

> Native desktop export (BETA), improved CLI and doctor integration, and metadata fixes for packaging. This is a BETA release: usable for testing, not recommended for production.

## Installation

```bash
pip install --upgrade dars-framework
```

or

```bash
pip install dars-framework==1.3.0
```

## Highlights

- **New: Native Desktop Export (BETA)**
  - Build desktop apps directly from Dars projects.
  - Project config supports `format: "desktop"` and `targetPlatform` (`auto|windows|linux|macos`).
  - Backend scaffold via `dars init --type desktop` (or `--update`), generating minimal main process files and preload bridge.
  - IPC bridge includes basic FS read/write for quick experiments.
  - Source emitted to `dist/source-electron/`; packaged artifacts in `dist/`.
  - Note: This capability is BETA and not recommended for production yet.

- **New: Desktop Build Flow in CLI**
  - `dars build` respects `format: "desktop"` in `dars.config.json`.
  - Platform flags are selected automatically or via `targetPlatform`.
  - Robust error output: full stdout/stderr on packaging failure.

- **New: Doctor Integration for Desktop Tooling**
  - `dars doctor --all --yes` checks and installs optional desktop tooling.
  - Pins the desktop runtime to a compatible version automatically when needed.

- **Packaging Reliability Improvements**
  - Project metadata auto-filled from `App` (name/title, description, author, version) with sensible defaults.
  - Version defaulted to `0.1.0` when absent (warning emitted).
  - Package manager forced to a stable toolchain to avoid ENOENT errors during packaging.
  - Runtime version pinned explicitly in both dev deps and build config to ensure predictable builds.

## Quickstart (Desktop BETA)

```bash
# Initialize or update a project with desktop scaffolding
dars init --type desktop
# or
dars init --update

# Verify optional tooling
dars doctor --all --yes

# Build using project config (format: "desktop")
dars build
```

Minimal `dars.config.json` for desktop:

```json
{
  "entry": "main.py",
  "format": "desktop",
  "outdir": "dist",
  "targetPlatform": "auto"
}
```

## Bug Fixes

- Fixed packaging failures caused by missing metadata in project manifests by auto-populating:
  - `description` from `App.description` (fallback to a default)
  - `author` from `App.author` (fallback to a default)
  - `version` from `App.version` (fallback `0.1.0` with warning)
- Stabilized packaging by pinning desktop runtime version in both dev dependencies and build configuration.
- Avoided package-manager ENOENT errors in packaging by forcing a stable manager and resolving runners reliably on Windows.
- Correct platform flags for packaging: `--win`, `--linux`, `--mac`.
- Improved error reporting to include stdout and stderr from the packaging tool.

## Notes

- This feature set is **BETA**. Many options (signing, advanced IPC, updates, and deeper configuration) are still evolving.
- Usable for internal tools and early testing. Not recommended for production deployment yet.
- Expect changes to configuration keys and defaults in future versions.

I spent ~1 month iterating on this capability and consolidated changes into this single BETA release once it reached a usable threshold. Feedback is welcome to help stabilize and expand the desktop feature set.

# Release Notes v1.2.9

> Optional default minification, precise CLI control, faster builds, and clearer minification status.

## Installation

```bash
pip install --upgrade dars-framework
```

or

```bash
pip install dars-framework==1.2.8
```

## Highlights

- **New: Configurable Default Minifier**
  - `defaultMinify` (default: true) controls the built‑in Python minifier.
  - Preserves `pre`, `code`, `textarea`, `script`, `style`.
  - Only removes non‑conditional HTML comments and collapses spaces between tags.
  - Does not collapse text-node spaces (Markdown and `<pre><code>` remain intact).

- **New: CLI Flag `--no-minify`**
  - Available in `dars build` and `dars export`.
  - Disables only the default Python minifier for that run.
  - Independent from `viteMinify`.

- **Minification Modes Work Together**
  - When `defaultMinify` and `viteMinify` are both true:
    - Default minifier applies (safe HTML and fallback for JS/CSS).
    - Vite/esbuild minify JS/CSS where available.
  - Status line now reflects the active mode:
    - “Applying minification (default)”
    - “Applying minification (vite)”
    - “Applying minification (default + vite)”

- **Faster Default Minifier**
  - Default minifier uses fast Python fallback (rjsmin/rcssmin/regex) and never shells out to Vite/esbuild.
  - Results in near‑instant minification step.

## Bug Fixes

- Default minifier no longer ignores config; `defaultMinify` and `--no-minify` are strictly honored.
- Eliminated unintended use of esbuild/Vite inside the default minifier.
- Improved label accuracy to match the actual minification pipeline (default, vite, or both).

## Notes

- Relevant configuration:
  - `defaultMinify`: true/false. Controls the Python-side minification (HTML + JS/CSS fallback).
  - `viteMinify`: true/false. Controls Vite/esbuild for JS/CSS when available.
- Backward compatibility:
  - Defaults maintain previous behavior, now safer for Markdown/code blocks.
  - You can disable default minification per-run with `--no-minify` without affecting `viteMinify`.

Upgrade Recommendation: Recommended for all users; especially helpful for projects with Markdown/code samples and those wanting faster, more controllable minification.

# Older release notes can be found

In the github repository [Here](https://github.com/ZtaMDev/Dars-Framework/releases).
