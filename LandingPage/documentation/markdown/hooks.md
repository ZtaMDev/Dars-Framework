# Hooks System

Dars Framework introduces a **Hooks system** inspired by React, enabling reactive and stateful behavior in both FunctionComponents and built-in components.

The reactivity system in Dars is divided into the following sections:

1. **Pythonic Value Helpers**: The `V()` helper and expression system used throughout all hooks.
2. **Component-Level State (VRefs)**: Lightweight, fast, and DOM-bound reactive state.
3. **Global Application State**: Structured `State` objects for shared application logic.
4. **Forms & Validation**: Hooks for form collection and client-side validation.
5. **Network & Async Operations**: Data fetching and chained actions.
6. **Best Practices**: Guidelines and tips.

---

## 1. Pythonic Value Helpers

Dars provides a set of helpers to make working with DOM values and reactive state completely Pythonic, eliminating the need for raw JavaScript.

### V() - Value Reference

The `V()` helper allows you to extract values from **DOM elements** (via CSS selectors) or **reactive state** (via state paths).

#### CSS Selectors (DOM Elements)

```python
from dars.all import *

# Select by ID
V("#myInput")

# Select by Class
V(".myClass")

```

#### State Paths (Reactive State)

`V()` also supports extracting values directly from reactive state created by `useDynamic()` (covered in detail in the [Global Application State](#3-global-application-state) section below):

```python
# Extract from reactive state
V("cart.total")      # Gets current value of cart.total
V("user.name")       # Gets current value of user.name
V("product.price")   # Gets current value of product.price
```

**How it works:**

- `V("cart.total")` finds the reactive element created by `useDynamic("cart.total")`
- Reads its current `textContent` value
- Perfect for combining reactive state with calculations

#### Transformations

You can chain transformation methods to process values before using them:

```python
# String transformations
V("#name").upper()   # "JOHN"
V("#name").lower()   # "john"
V("#name").trim()    # Remove whitespace

# Numeric transformations (required for math operations!)
V("#age").int()      # 25 (integer)
V("#price").float()  # 19.99 (float)
V("cart.total").float()  # Extract state value as float
```

#### Operations

`V()` now supports declarative mathematical expressions with operator overloading!

```python
# Simple arithmetic
calc.result.set(V(".a").float() + V(".b").float())

# Complex expressions with automatic precedence
calc.result.set(
    (V(".a").float() + V(".b").float()) * V(".c").float()
)

# Dynamic operators from Select elements
calc.result.set(
    V(".num1").float() + V(".operation").operator() + V(".num2").float()
)
```

**Features:**

- Operator overloading (`+`, `-`, `*`, `/`, `%`, `**`)
- Automatic operator precedence
- Dynamic operators from Select/Input
- NaN validation with console warnings
- Type safety (numeric ops require `.float()` or `.int()`)

> [!TIP]
> For complete documentation on mathematical operations, operator precedence, dynamic operators, and advanced examples, see the Mathematical Operations docs.

#### equal() helper

Sometimes you want to normalize a value (literal or expression) to safely combine it within an expression with `V()` without worrying about precedence or operators:

```python
from dars.hooks.value_helpers import V, equal

# Add 1 using V() + literal
updateVRef(".dyn_count", V(".dyn_count").int() + 1)

# Normalize a literal as a mathematical expression
updateVRef(".dyn_count", equal(0))           # forces to 0

# Combine with another expression based on V()
expr = V(".a").int() + equal(V(".b").int())
updateVRef(".result", expr)
```

- `equal(value)` wraps the value in a `MathExpression`, so it integrates into the same operation tree as `V()` and respects the async/NaN-safe semantics of the expression system.

#### Complete Example

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

#### url() - URL Builder

The `url()` helper constructs dynamic URLs by interpolating `ValueRef` objects into a template string.

```python
# Generates: https://api.example.com/users/123/profile
fetch(
    url("https://api.example.com/users/{id}/profile", id=V("#userId"))
)

# With state values
fetch(
    url("/api/products/{id}", id=V("product.id"))
)

# Mixed
fetch(
    url("/api/{resource}/{id}",
        resource="users",
        id=V("#userId"))
)
```

**Note:** Use standard Python format string syntax `{key}` for placeholders.

#### Boolean & Comparison Operators

`V()` supports boolean and comparison operations, enabling declarative validation and conditional logic without raw JavaScript!

##### Comparison Operators

Compare values using Python-style operators:

```python
from dars.all import *

# Numeric comparisons (require .int() or .float())
V("#age").int() >= 18
V("#price").float() < 100.0
V("#quantity").int() == 5

# String equality
V("#password") == V("#confirm-password")
V("#email") != ""

# All operators: ==, !=, >, <, >=, <=
```

#### String Methods

Check string properties with built-in methods:

```python
# Check if string contains substring
V("#email").includes("@")

# Check string start/end
V("#filename").startswith("report_")
V("#filename").endswith(".pdf")

# Get string length (returns ValueRef with .int())
V("#password").length() >= 8

# Convert to boolean
V("#checkbox").bool()
```

#### Logical Operators

Combine boolean expressions with `.and_()` and `.or_()`:

```python
# AND operator
(V("#age").int() >= 18).and_(V("#age").int() <= 65)

# OR operator
(V("#email").includes("@")).or_(V("#phone").length() >= 10)

# Complex combinations
(V("#name").length() >= 3).and_(
    (V("#email").includes("@")).and_(
        V("#email").includes(".")
    )
)
```

#### Conditional Expressions

Use `.then()` for ternary operations (condition ? trueVal : falseVal):

```python
# Simple conditional
(V("#age").int() >= 18).then("Adult", "Minor")

# With state updates
state.message.set(
    (V("#score").int() >= 60).then("Pass", "Fail")
)

# Nested conditionals
(V("#premium").bool()).then("10% discount", "No discount")

# Complex validation
state.validation.set(
    (V("#password").length() >= 8).and_(
        V("#password") == V("#confirm")
    ).then("✓ Valid", "✗ Invalid")
)
```

#### Complete Validation Example

```python
from dars.all import *

app = App("Form Validation")
form = State("form",
    email_valid="",
    age_valid="",
    password_valid=""
)

@route("/")
def index():
    return Page(
        Container(
            # Email validation
            Input(id="email", placeholder="Email"),
            Button(
                "Validate Email",
                on_click=form.email_valid.set(
                    (V("#email").includes("@")).and_(
                        V("#email").includes(".")
                    ).then("✓ Valid email", "✗ Invalid email")
                )
            ),
            Text(text=useDynamic("form.email_valid")),

            # Age validation
            Input(id="age", input_type="number", placeholder="Age"),
            Button(
                "Validate Age",
                on_click=form.age_valid.set(
                    (V("#age").int() >= 18).and_(
                        V("#age").int() <= 120
                    ).then("✓ Valid age", "✗ Must be 18-120")
                )
            ),
            Text(text=useDynamic("form.age_valid")),

            # Password match validation
            Input(id="password", input_type="password", placeholder="Password"),
            Input(id="confirm", input_type="password", placeholder="Confirm"),
            Button(
                "Check Match",
                on_click=form.password_valid.set(
                    (V("#password") == V("#confirm")).and_(
                        V("#password").length() >= 8
                    ).then("✓ Passwords match", "✗ Passwords don't match")
                )
            ),
            Text(text=useDynamic("form.password_valid"))
        )
    )

app.add_page("index", index())
```

---

### getDateTime() - Timestamp Helper

\*\*Generate client-side timestamps for forms and state updates.

#### Basic Usage

```python
from dars.all import *

# Default ISO format
getDateTime()  # "2025-12-04T22:04:09.123Z"

# Different formats
getDateTime("iso")        # "2025-12-04T22:04:09.123Z"
getDateTime("locale")     # "12/4/2025, 10:04:09 PM"
getDateTime("date")       # "12/4/2025"
getDateTime("time")       # "10:04:09 PM"
getDateTime("timestamp")  # 1733362449123
```

#### Usage in Forms

```python
# Add timestamp to form submission
form_data = collect_form(
    name=V("#name"),
    email=V("#email"),
    submitted_at=getDateTime()  # ISO format
)

# Different timestamp formats
form_data = collect_form(
    name=V("#name"),
    created_at=getDateTime("iso"),
    display_date=getDateTime("locale"),
    date_only=getDateTime("date"),
    time_only=getDateTime("time"),
    unix_timestamp=getDateTime("timestamp")
)
```

#### Usage with State

```python
# Update state with current timestamp
Button("Save", on_click=state.last_updated.set(getDateTime()))

# Different formats
Button("Save Date", on_click=state.date.set(getDateTime("date")))
Button("Save Time", on_click=state.time.set(getDateTime("time")))
```

#### Complete Example

```python
from dars.all import *

app = App("Timestamp Demo")
state = State("state", last_action="", timestamp="")

form_data = collect_form(
    action=V("#action"),
    timestamp=getDateTime("locale")
)

@route("/")
def index():
    return Page(
        Container(
            Input(id="action", placeholder="What did you do?"),

            Button(
                "Record Action",
                on_click=form_data.to_state(state.last_action)
            ),

            Text("Last Action:", style="font-bold"),
            Text(text=useDynamic("state.last_action")),

            Button(
                "Update Timestamp",
                on_click=state.timestamp.set(getDateTime("locale"))
            ),

            Text("Current Time:", style="font-bold"),
            Text(text=useDynamic("state.timestamp"))
        )
    )

app.add_page("index", index())

if __name__ == "__main__":
    app.rTimeCompile()
```

---

## 2. Component-Level State (VRef System)

The VRef system allows you to define and manage state declaratively without creating complex global objects. It is the recommended approach for local component state.

### setVRef() - Independent Value Reference

The `setVRef()` hook allows you to define initial values that are tied to a specific CSS selector. This is the foundation for creating component-level state that can be shared across multiple components without using global `State` objects.

#### Basic Usage

Create a reference with an initial value and a selector, then pass it to components.

```python
from dars.all import *

# Create a reference tied to the "#count" ID
count_ref = setVRef(0, "#count")

# Use it in a component
Text(count_ref, id="count")
```

#### Shared Values (Multi-Component Updates)

By using a **class selector**, you can share the same value across multiple components and update them all simultaneously!

```python
# Create a reference tied to a CLASS selector
price_ref = setVRef(99.99, ".product-price")

# Use in multiple places
Container(
    Text("Price: $", style="font-bold"),
    Text(price_ref, class_name="product-price"),  # Main display

    Container(
        Text("Also shown here: $"),
        Text(price_ref, class_name="product-price")   # Secondary display
    )
)

# Update ALL elements matching ".product-price" at once
Button("Discount", on_click=updateVRef(".product-price", 49.99))
```

#### Usage in FunctionComponents

`setVRef` works seamlessly with `@FunctionComponent`. The value is resolved internally, so your templates remain clean.

```python
@FunctionComponent
def UserBadge(name_ref, **props):
    return f'''
    <div {Props.class_name} {Props.style}>
        User: <span class="user-name">{name_ref}</span>
    </div>
    '''

# Define ref
user_ref = setVRef("Guest", ".user-name")

# Render
UserBadge(user_ref, class_name="badge")

# Update
Button("Login", on_click=updateVRef(".user-name", "John Doe"))
```

#### Syntax

```python
setVRef(initial_value: Any, selector: str) -> VRefValue
```

**Parameters:**

- `initial_value`: The initial value to display (string, number, boolean).
- `selector`: The CSS selector (ID or Class) that identifies the element(s).
  - Use `#id` for single elements.
  - Use `.class` for multiple elements sharing the value.

**Returns:**

- `VRefValue`: An object representing the value, ready to be passed to components.

---

### useVRef() - Consume VRef State

The `useVRef()` hook allows you to create reactive bindings between `setVRef` values and your UI. It seamlessly works with the `V()` value extractor and mathematical expressions.

#### Basic Usage

Use it to wrap `V()` expressions directly into component properties:

```python
from dars.all import *

# Define the state globally or locally
price = setVRef(10.0, ".item-price")

# Consume the state reactively
Container(
    Text("Price: $"),
    Text(text=useVRef(V(".item-price")))
)
```

#### Advanced Expressions

`useVRef()` truly shines when combined with mathematical and boolean operations. It automatically tracks dependencies and updates the UI instantly:

```python
# Create basic states
setVRef(19.99, ".price")
setVRef(2, ".quantity")

# Reactive mathematical expression
Text(
    text=useVRef(V(".price").float() * V(".quantity").int())
)

# Reactive boolean expressions
Button(
    "Checkout",
    disabled=useVRef(V(".quantity").int() == 0)
)
```

#### Auto-Dependency Detection

You do **not** need to specify which selectors to watch. The compiler automatically walks the `V()` expression tree and extracts every CSS selector used. At runtime, whenever any of those selectors is updated via `updateVRef()`, the binding re-evaluates and patches the DOM.

```python
# The framework auto-detects that this binding depends on ".price" and ".qty"
Text(text=useVRef(V(".price").float() * V(".qty").int()))

# When either changes, the text updates automatically:
Button("Double price", on_click=updateVRef(".price", V(".price").float() * 2))
Button("+1 qty",       on_click=updateVRef(".qty",   V(".qty").int() + 1))
```

If you need to override auto-detection, pass explicit selectors via the `dependencies` parameter:

```python
Text(text=useVRef(
    V(".total").float(),
    dependencies=[V(".price"), V(".qty")]   # explicit override
))
```

#### Reactive Callbacks

Pass `dScript`, `RawJS`, or plain strings via the `callbacks` parameter. They fire every time the binding re-evaluates, enabling side-effects like logging or chained updates.

```python
from dars.scripts.dscript import RawJS

# Single callback (no list needed)
Text(text=useVRef(
    V(".value-stuff"),
    callbacks=RawJS("console.log('value-stuff changed!');")
))

# dScript callback
Text(text=useVRef(
    V(".score").int(),
    callbacks=log("Score was updated")
))

# Multiple callbacks (list)
Text(text=useVRef(
    V(".total").float(),
    callbacks=[
        log("total changed"),
        RawJS("document.title = 'Total: ' + document.querySelector('.total-display').textContent;")
    ]
))
```

#### Syntax

```python
useVRef(
    vexpr: Union[ValueRef, MathExpression, BooleanExpression, Any],
    dependencies: Optional[List[ValueRef]] = None,
    callbacks: Optional[Union[dScript, RawJS, str, List[Union[dScript, RawJS, str]]]] = None
) -> VRefBinding
```

**Parameters:**

- `vexpr`: A `V()` expression, an operator chain, or a direct literal value.
- `dependencies`: Optional explicit list of `V()` selectors to watch. If omitted, selectors are auto-detected from the expression tree.
- `callbacks`: Optional callback(s) fired every time the binding re-evaluates. Accepts a single `dScript`, `RawJS`, or `str`, or a list of those.

**Returns:**

- `VRefBinding`: An object that resolves to the current value on render, and injects JavaScript to update reactively on hydration.

---

### updateVRef() - Component-Level State Updates

Update DOM element values declaratively without State objects!

The `updateVRef()` function completes the component-level state management cycle, providing a Pythonic way to update values alongside `V()` for reading and boolean operators for validation.

**The Complete Cycle:**

1. **Read**: `V("#input")` - Extract values
2. **Validate**: `V("#input").length() >= 3` - Boolean validation
3. **Update**: `updateVRef("#input", "new value")` - Update values ✨ **NEW!**

#### Basic Usage

```python
from dars.all import *

# Update text content
Button("Set Name", on_click=updateVRef("#name", "John Doe"))

# Update input value
Button("Clear Email", on_click=updateVRef("#email", ""))

# Update checkbox
Button("Check Box", on_click=updateVRef("#agree", True))

# Update number
Button("Set Price", on_click=updateVRef("#price", 99.99))
```

#### With V() Expressions

Combine `updateVRef()` with `V()` expressions for dynamic updates:

```python
# Copy values between elements
Button("Copy", on_click=updateVRef("#target", V("#source")))

# With transformations
Button("Uppercase", on_click=updateVRef("#output", V("#input").upper()))

# With calculations
Button("Calculate Total", on_click=updateVRef("#total",
    V("#price").float() * V("#qty").int()
))

# With string concatenation
Button("Generate Full Name", on_click=updateVRef("#full-name",
    V("#first-name") + " " + V("#last-name")
))
```

#### With Boolean Expressions

Use boolean operators for conditional updates:

```python
# Conditional text based on age
Button("Check Age", on_click=updateVRef("#status",
    (V("#age").int() >= 18).then("Adult", "Minor")
))

# Validation messages
Button("Validate Email", on_click=updateVRef("#message",
    (V("#email").includes("@")).and_(
        V("#email").includes(".")
    ).then("✓ Valid email", "✗ Invalid email")
))

# Complex validation
Button("Check Password", on_click=updateVRef("#pwd-status",
    (V("#password").length() >= 8).and_(
        V("#password") == V("#confirm")
    ).then("✓ Passwords match", "✗ Passwords don't match")
))
```

#### Batch Updates

Update multiple elements with a single call:

```python
# Clear entire form
Button("Clear All", on_click=updateVRef({
    "#name": "",
    "#email": "",
    "#age": "",
    "#phone": ""
}))

# Fill sample data
Button("Fill Sample Data", on_click=updateVRef({
    "#name": "John Doe",
    "#email": "john@example.com",
    "#age": 25,
    "#phone": "555-0123"
}))

# Mix literals and expressions
Button("Update All", on_click=updateVRef({
    "#full-name": V("#first") + " " + V("#last"),
    "#email-lower": V("#email").lower(),
    "#age-status": (V("#age").int() >= 18).then("Adult", "Minor")
}))
```

#### Complete Examples

##### Example 1: Counter (No State Object!)

```python
from dars.all import *

app = App("Counter Demo")

@route("/")
def index():
    return Page(
        Container(
            # Display count
            Text("Count: ", style="font-bold"),
            Text("0", id="count", style="text-[48px] font-bold text-blue-600"),

            # Update buttons
            Container(
                Button(
                    "+",
                    on_click=updateVRef("#count", V("#count").int() + 1),
                    style="bg-green-500 text-white px-6 py-3 rounded"
                ),
                Button(
                    "-",
                    on_click=updateVRef("#count", V("#count").int() - 1),
                    style="bg-red-500 text-white px-6 py-3 rounded"
                ),
                Button(
                    "Reset",
                    on_click=updateVRef("#count", 0),
                    style="bg-gray-500 text-white px-6 py-3 rounded"
                ),
                style="flex gap-2"
            )
        )
    )

app.add_page("index", index())
```

##### Example 2: Form Auto-Fill

```python
@route("/form")
def form():
    return Page(
        Container(
            Input(id="first-name", placeholder="First Name"),
            Input(id="last-name", placeholder="Last Name"),
            Input(id="full-name", placeholder="Full Name", readonly=True),

            # Auto-generate full name
            Button(
                "Generate Full Name",
                on_click=updateVRef("#full-name",
                    V("#first-name") + " " + V("#last-name")
                )
            ),

            # Normalize inputs
            Button(
                "Normalize All",
                on_click=updateVRef({
                    "#first-name": V("#first-name").trim(),
                    "#last-name": V("#last-name").trim()
                })
            ),

            # Clear all
            Button(
                "Clear All",
                on_click=updateVRef({
                    "#first-name": "",
                    "#last-name": "",
                    "#full-name": ""
                })
            )
        )
    )
```

##### Example 3: Shopping Cart

```python
@route("/cart")
def cart():
    return Page(
        Container(
            Input(id="price", input_type="number", value="19.99", placeholder="Price"),
            Input(id="quantity", input_type="number", value="1", placeholder="Quantity"),

            Text("Total: $", style="font-bold"),
            Text("0", id="total", style="text-[24px] text-green-600"),

            # Calculate total
            Button(
                "Calculate Total",
                on_click=updateVRef("#total",
                    V("#price").float() * V("#quantity").int()
                )
            ),

            # Apply discount
            Button(
                "Apply 10% Discount",
                on_click=updateVRef("#total",
                    V("#total").float() * 0.9
                )
            ),

            # Reset
            Button(
                "Reset",
                on_click=updateVRef({
                    "#price": "19.99",
                    "#quantity": "1",
                    "#total": "0"
                })
            )
        )
    )
```

#### Syntax

```python
updateVRef(selector, value) -> dScript
updateVRef(dict) -> dScript
```

**Parameters:**

- `selector`: CSS selector string (e.g., `"#id"`, `".class"`)
- `value`: Value to set - can be:
  - Literal: `"text"`, `42`, `True`
  - V() expression: `V("#source")`
  - Transformation: `V("#input").upper()`
  - Math expression: `V("#a").int() + V("#b").int()`
  - Boolean expression: `(V("#age").int() >= 18).then("Adult", "Minor")`
- `dict`: Dictionary of `{selector: value}` pairs for batch updates

**Returns:**

- `dScript` object for use in event handlers

**Supported Elements:**

- `Input` / `Textarea`: Updates `.value` property
- `Checkbox` / `Radio`: Updates `.checked` property
- `Select`: Updates `.value` property
- Other elements: Updates `.textContent`

#### Integration with Other Features

##### With collect_form()

```python
# Normalize before collecting
form_data = collect_form(
    name=V("#name"),
    email=V("#email")
)

Button(
    "Normalize & Submit",
    on_click=sequence(
        updateVRef({
            "#name": V("#name").trim(),
            "#email": V("#email").lower().trim()
        }),
        form_data.submit("http://localhost:3000/submit")
    )
)
```

##### With State (Hybrid Approach)

```python
# Local updates for preview
Button("Preview", on_click=updateVRef("#preview",
    "Name: " + V("#name") + ", Email: " + V("#email")
))

# Save to global state
user = State("user", name="", email="")
Button("Save to State", on_click=sequence(
    user.name.set(V("#name")),
    user.email.set(V("#email"))
))
```

### When to Use updateVRef() vs State.set()

**Use `updateVRef()` when:**

- Updating UI elements temporarily
- Form auto-fill and normalization
- Local calculations and previews
- Component-level state
- You don't need reactivity across components

**Use `State.set()` when:**

- Data needs to persist
- Multiple components need the value
- You need automatic reactivity
- Application-level state

**Use both (Hybrid):**

- Local updates for immediate feedback
- State updates for persistence
- Best of both worlds!

---

# Global Application State

For state that needs to be shared across many disconnected components or persists across navigation, use `State` objects.

### useDynamic() - Reactive State Binding

The `useDynamic()` hook creates reactive bindings between external `State` objects and component properties.

#### 1. Usage in Built-in Components

You can pass `useDynamic()` directly to properties of built-in components like `Text`, `Button`, `Input`, etc.

```python
from dars.all import *

# Create state
userState = State("user", name="John Doe", status="Active", is_admin=False)

# Bind directly to props
card = Container(
    # Bind text property
    Text(text=useDynamic("user.name"), style="font-bold"),

    # Bind input value
    Input(value=useDynamic("user.name"), placeholder="Edit name"),

    # Bind button text and disabled state
    Button(
        text=useDynamic("user.status"),
        disabled=useDynamic("user.is_admin"),
        on_click=userState.status.set("Clicked!")
    )
)
```

#### Supported Properties

`useDynamic` and `useValue` supports binding to the following properties on built-in components:

| Component     | Properties                                                 |
| ------------- | ---------------------------------------------------------- |
| `Text`        | `text`, `innerHTML`                                        |
| `Button`      | `text`, `disabled`                                         |
| `Input`       | `value`, `placeholder`, `disabled`, `readonly`, `required` |
| `Textarea`    | `value`, `placeholder`, `disabled`, `readonly`, `required` |
| `Image`       | `src`, `alt`                                               |
| `Link`        | `href`, `text`                                             |
| `Checkbox`    | `checked`, `disabled`, `required`                          |
| `RadioButton` | `checked`, `disabled`, `required`                          |
| `Select`      | `disabled`, `required`                                     |
| `Slider`      | `disabled`                                                 |

Boolean attributes like `disabled` and `checked` will be toggled based on the truthiness of the state value.

#### 2. Usage in FunctionComponents

You can also use `useDynamic()` within `FunctionComponent` templates to create reactive spans.

```python
@FunctionComponent
def UserCard(**props):
    return f'''
    <div {Props.id} {Props.class_name} {Props.style}>
        <h3>Name: {useDynamic("user.name")}</h3>
        <p>Status: {useDynamic("user.status")}</p>
    </div>
    '''
```

#### Syntax

```python
useDynamic(state_path: str) -> DynamicBinding
```

**Parameters:**

- `state_path`: Dot-notation path to state property (e.g., `"user.name"`, `"cart.total"`)

**Returns:**

- `DynamicBinding` object that resolves to the current value during render and updates automatically when state changes.

---

### useValue() - Initial Value Access

The `useValue()` hook allows you to access the **initial value** of a state property without creating a reactive binding. This is ideal for form inputs where you want to set a default value but allow the user to edit it freely.

#### Basic Usage

Pass `useValue()` to component properties to set their initial value from state:

```python
from dars.all import *

userState = State("user", name="John Doe", email="john@example.com")

# Input with initial value from state (editable by user)
Input(value=useValue("user.name"))

# Textarea with initial value
Textarea(value=useValue("user.email"))
```

#### Usage in FunctionComponents with Selectors

`useValue()` supports automatic selector application in FunctionComponents! When you provide a selector (class or ID), it will be automatically applied to the element where the value is used.

```python
from dars.all import *

app = App("Example of hooks")

userState = State("user", name="Jane Doe", email="jane@example.com", display="None")

@FunctionComponent
def UserForm(**props):
    return f'''
    <div {Props.id} {Props.class_name} {Props.style}>
        <input value="{useValue("user.name", ".name-input")}" />
        <input value="{useValue("user.email", "#email-field")}" />
        <span>{useValue("user.age", ".age-display")}</span>
        <span>{useDynamic("user.display")}</span>
    </div>
    '''


@route("/")
def index():
    return Page(
        UserForm(id="user-form"),
        # Extract values using V() helper with the selectors
        Button(
            "Get Name",
            on_click=userState.display.set(
                "Name: " + V(".name-input")  # Extract current value
            )
        ),

        Button(
            "Combine Values",
            on_click=userState.display.set(
                V(".name-input") + " (" + V("#email-field") + ")"
            )
        )
    )

app.add_page("index", index(), title="hooks", index=True)

if __name__ == "__main__":
    app.rTimeCompile()
```

**How it works:**

1. `useValue("user.name", ".name-input")` sets initial value "Jane Doe" and applies class `name-input` to the input
2. User can edit the value freely
3. `V(".name-input")` extracts the current value (even if modified by user)
4. Perfect for forms where you need both initial values and value extraction

**Supported selectors:**

- **Class selectors** (`.foo`) → Added to element's `class` attribute
- **ID selectors** (`#bar`) → Set as element's `id` attribute

##### Difference from useDynamic

- **`useDynamic("state.prop")`**: Creates a **reactive binding**. If the state changes, the input value updates automatically.
- **`useValue("state.prop")`**: Sets the **initial value only**. If the state changes later, the input value does NOT update. This prevents overwriting user input while they are typing.

#### Syntax

```python
useValue(state_path: str, selector: str = None) -> ValueMarker
```

**Parameters:**

- `state_path`: Dot-notation path to state property (e.g., `"user.name"`)
- `selector`: Optional CSS selector (class or ID) to apply to the element

**Returns:**

- `ValueMarker` object that resolves to the initial value during component rendering.

---

### useWatch() - State Monitoring

The `useWatch()` hook allows you to monitor state changes and execute callbacks (side effects). It supports watching single or multiple state properties and executing one or more callbacks.

#### Basic Usage

The recommended way to use `useWatch` is via the `app.useWatch()` or `page.useWatch()` methods:

**Single State Property**

```python
from dars.all import *

cartState = State("cart", count=0, total=0.0)

# Logs to console whenever cart.count changes
app.useWatch("cart.count", log("Cart updated!"))
app.useWatch("cart.total", log("Total changed"))
```

**Multiple State Properties (Array Syntax)**

```python
productState = State("product", name="Widget", price=19.99, info="")

# Watch multiple properties - callback executes when ANY of them change
app.useWatch(
    ["product.name", "product.price"],
    productState.info.set("Product: " + V("product.name") + " - $" + V("product.price"))
)
```

**Multiple Callbacks**

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

**Page-Specific Watchers (page.useWatch)**

```python
@route("/cart")
def cart_page():
    page = Page()

    # This watcher only runs on the cart page
    page.useWatch("cart.total", log("Total changed!"))

    page.add(
        Container(
            Text(useDynamic("cart.total"))
        )
    )
    return page
```

You can also use the classic syntax with `add_script`:

```python
app.add_script(useWatch("state.prop", log("Changed!")))
```

#### Syntax

```python
useWatch(
    state_path: Union[str, List[str]],
    *callbacks: Union[dScript, str, Callable]
) -> Union[dScript, WatchMarker]
```

**Parameters:**

- `state_path`: State property path(s) to watch. Can be:
  - Single path string (e.g., `"user.name"`)
  - List of paths (e.g., `["product.name", "product.price"]`)
- `*callbacks`: One or more callbacks to execute when state changes. Each can be:
  - `dScript` object (e.g., `log("Changed")`, `alert("Update")`)
  - State setter (e.g., `productState.info.set(...)`)
  - Inline JavaScript string
  - Python callable returning a `dScript`

**Behavior:**

- When using an array of state paths, the callback(s) execute when **any** of the watched properties change
- Multiple callbacks execute in the order they are provided
- Callbacks can access current state values using `V()` helper

---

#### Important: State ID Best Practices

> [!IMPORTANT]
> When using `State` objects with hooks like `useDynamic` and `useValue`, the **state ID should NOT match any component ID** in your DOM. The state ID is a unique identifier for the state object itself, not a component.

##### Why This Matters

The reactive system uses **watchers** to update components when state changes. When you create a `State` object, the ID you provide is used to register the state in the internal registry, not to identify a specific DOM element.

##### Examples

**X Incorrect - State ID matches component ID:**

```python
# DON'T do this
state = State("my-button", count=0, disabled=False)
Button(id="my-button", text=useDynamic("my-button.count"))
```

In this example, both the state and the button have the ID `"my-button"`, which can cause confusion and unexpected behavior.

**✓ Correct - State has unique ID:**

```python
# DO this - give state a descriptive, unique ID
counter_state = State("counter-state", count=0, disabled=False)
Button(id="my-button", text=useDynamic("counter-state.count"))
Button(id="another-button", disabled=useDynamic("counter-state.disabled"))
```

**✓ Also Correct - Multiple components sharing same state:**

```python
# One state can control multiple components
ui_state = State("ui", count=0, is_disabled=False, message="Hello")

Container(
    Text(text=useDynamic("ui.message")),
    Button(id="btn-1", disabled=useDynamic("ui.is_disabled")),
    Button(id="btn-2", disabled=useDynamic("ui.is_disabled")),
    Text(text=useDynamic("ui.count"))
)
```

#### Key Takeaways

1. **State IDs are for the state object**, not for DOM elements
2. **One state can control many components** through reactive bindings
3. **Component IDs should be unique** across your DOM
4. **State IDs should be descriptive** of what they manage (e.g., `"user-data"`, `"cart-state"`, `"ui-controls"`)

---

## 4. Forms & Validation

### Form Collection System

Pythonic form data collection and submission without raw JavaScript!

#### FormData & collect_form()

The `FormData` class and `collect_form()` helper provide a declarative way to collect form data using `V()` expressions.

##### Basic Usage

```python
from dars.all import *

# Collect form data with kwargs syntax
form_data = collect_form(
    name=V("#name-input"),
    email=V("#email-input"),
    age=V("#age-input").int(),
    is_premium=V("#premium-checkbox")
)

# Show in alert
Button("Submit", on_click=form_data.alert())

# Log to console
Button("Log", on_click=form_data.log())

# Save to state
Button("Save", on_click=form_data.to_state(state.data))
```

##### Advanced Features

**Nested Dictionaries & Lists:**

```python
form_data = collect_form(
    name=V("#name"),
    email=V("#email"),

    # Nested validation results
    validation={
        "email_valid": V("#email").includes("@"),
        "age_ok": (V("#age").int() >= 18).and_(
                   V("#age").int() <= 120)
    },

    # Conditional values
    discount=(V("#premium").bool()).then("10%", "0%"),

    # Timestamp
    submitted_at=getDateTime()
)
```

**Alternative Syntaxes:**

```python
# Using tuples
form_data = collect_form(
    ("name", V("#name")),
    ("email", V("#email"))
)

# Using dict
form_data = collect_form({
    "name": V("#name"),
    "email": V("#email")
})
```

##### FormData Methods

**`.alert(title)`** - Show form data in alert dialog:

```python
Button("Show Data", on_click=form_data.alert("Form Data"))
```

**`.log(message)`** - Log form data to console:

```python
Button("Log Data", on_click=form_data.log("Form submitted"))
```

**`.to_state(property)`** - Save form data to state:

```python
Button("Save", on_click=form_data.to_state(state.form_data))
```

**`.submit(url, state_property, on_success, on_error)`** - Submit to backend:

```python
# Simple submit
Button("Submit", on_click=form_data.submit("http://localhost:3000/submit"))

# With state and callbacks
Button("Submit", on_click=form_data.submit(
    url="http://localhost:3000/submit",
    state_property=state.response,
    on_success=alert("Success!"),
    on_error=alert("Error!")
))
```

**`.submit_and_alert(state_property, title)`** - Submit with alert:

```python
Button("Submit", on_click=form_data.submit_and_alert(
    state.data,
    "Form Submitted!"
))
```

##### Backend Integration Example

```python
from dars.all import *

app = App("Form with Backend")
form = State("form", response="")

# Collect form data
form_data = collect_form(
    name=V("#name"),
    email=V("#email"),
    age=V("#age").int(),
    submitted_at=getDateTime()
)

@route("/")
def index():
    return Page(
        Container(
            Input(id="name", placeholder="Name"),
            Input(id="email", placeholder="Email"),
            Input(id="age", input_type="number", placeholder="Age"),

            # Submit to backend
            Button(
                "Submit to Backend",
                on_click=form_data.submit(
                    url="http://localhost:3000/submit",
                    state_property=form.response,
                    on_success=alert("Form submitted successfully!")
                )
            ),

            # Display backend response
            Container(
                Text("Backend Response:", style="font-bold"),
                Text(text=useDynamic("form.response"))
            )
        )
    )

app.add_page("index", index())
```

### FormValidator — Client-Side Validation

Declarative form validation with dual client/server enforcement.

#### Rules

| Constructor      | Description                                |
| ---------------- | ------------------------------------------ |
| `required()`     | Field must be non-empty                    |
| `min_length(n)`  | Minimum character count                    |
| `max_length(n)`  | Maximum character count                    |
| `email()`        | Must be a valid email address              |
| `pattern(regex)` | Must match regex                           |
| `min_value(n)`   | Numeric minimum                            |
| `max_value(n)`   | Numeric maximum                            |
| `custom(fn)`     | Python callable `(value) -> Optional[str]` |

#### `validated_submit`

Validates all rules client-side first. Only fires the network request if every rule passes. Error messages appear in `#{field}-error` elements.

```python
task_form = collect_form(title=V("#title"))

validator = FormValidator({
    "title": [required(), min_length(3), max_length(100)],
})

submit_action = validator.validated_submit(
    url="/api/tasks",
    form_data=task_form,
    on_success=runSequence(clearInput("title"), fetch_trigger),
    on_error=setText("submit-error", "Error submitting. Try again."),
)

# In your Page:
Input(id="title", placeholder="Task title…"),
Text("", id="title-error", style="text-red-500 text-sm"),
Button("Add Task", on_click=submit_action),
```

> **Important:** The input `id` must match the field name in `FormValidator` so the selector `#title` resolves correctly.

#### Server-Side Validation

```python
errors = validator.validate_server({"title": "Hi"})
# → {"title": ["Must be at least 3 characters."]}

errors = validator.validate_server({"title": "Hello World"})
# → {}  (all pass)
```

---

## 5. Network & Async Operations

### useFetch() — Declarative Data Fetching

`useFetch` is the primary hook for fetching data from APIs and binding the response to reactive VRefs. It returns a 4-tuple of `(trigger, loading_vref, data_vref, error_vref)` — all pure Python objects.

#### Basic Usage

```python

from dars.all import *

trigger, loading, data, error = useFetch("/api/users")

page = Page(
    Show(loading, Spinner()),
    Show(error,   Text("Error loading data", style="text-red-500")),
    Button("Reload", on_click=trigger),
)
page.add_script(trigger)  # auto-run on page load

```

#### With Callbacks

```python

tasks_sel = ".tasks-data"
_tasks    = setVRef([], tasks_sel)

trigger, loading, _, error = useFetch(
    "/api/tasks",
    on_success=runSequence(
        updateVRef(".loading", False),
        updateVRefFromResponse(tasks_sel),  # store response → VRef
    ),
    on_error=runSequence(
        updateVRef(".loading", False),
        updateVRef(".error", True),
    ),
)

```

#### POST with Body

```python

trigger, loading, data, error = useFetch(
    "/api/search",
    method="POST",
    body={"query": "dars"},
    headers={"Content-Type": "application/json"},
)

```

##### Signature

```python

useFetch(
    url: str,
    method: str = "GET",
    body: Any = None,
    headers: dict = None,
    on_success: dScript = None,
    on_error: dScript = None,
) -> Tuple[dScript, VRefValue, VRefValue, VRefValue]

```

**Returns:** `(trigger_script, loading_vref, data_vref, error_vref)`

- `trigger_script` — `dScript` that initiates the fetch. Use as `on_click` handler or in `runSequence`, or pass to `page.add_script()` to auto-run on load.
- `loading_vref` — `VRefValue` that is `True` while the request is in flight.
- `data_vref` — `VRefValue` that holds the parsed response on success.
- `error_vref` — `VRefValue` that holds the error message on failure.

---

### updateVRefFromResponse() — Store Fetch Response

Stores the API response from a `useFetch` `on_success` context into a VRef selector. The `network_request` DAP op passes the parsed response as `ctx.response`.

```python

updateVRefFromResponse(selector: str, key: str = "response") -> dScript

```

```python

on_success=runSequence(
    updateVRef(".loading", False),
    updateVRefFromResponse(".tasks-data"),  # stores ctx.response → VRef
)

```

Use `key` to read a different context field if needed (default is `"response"`).

---

### runSequence() — Chain Multiple Actions

Execute multiple `dScript` / `RawJS` actions in sequence. Accepts any mix of hooks, VRef updates, fetch triggers, and DAP actions.

```python

from dars.all import *

Button("Submit",
    on_click=runSequence(
        updateVRef(".loading", True),
        fetch_trigger,
        clearInput("my-input"),
    )
)

```

---

## 6. Appendix

### Best Practices

**Do:**

- Use `useDynamic` for simple text/value updates.
- Use `useWatch` for side effects like logging, analytics, or complex logic.
- Use `useValue` with selectors for form inputs that need value extraction.
- Use consistent state naming (e.g., `"user"`, `"cart"`).
- Always use `.int()` or `.float()` before arithmetic operations with `V()`.

**Don't:**

- Use with non-existent state paths.
- Nest state paths more than 2 levels deep (currently supports `stateName.property`).
- Use arithmetic operators without numeric transformations.

---
