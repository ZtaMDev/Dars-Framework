# Custom Components in Dars Framework

Dars offers two ways to create custom components: **Function Components** (Recommended) and **Class Components** (Legacy).

## Function Components (Recommended)

Function Components are the modern way to create reusable UI elements. They use simple functions with f-string templates and automatically handle framework features like IDs, styling, and events.

### Basic Syntax

Use the `@FunctionComponent` decorator. You can access framework properties (`id`, `class_name`, `style`, `children`) using the `Props` helper object or by declaring them as arguments.

#### Option 1: Using `Props` Object (Cleanest)

```python
from dars.all import *

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
card = UserCard("John Doe", "john@example.com", id="user-1", style="p-5")
```

#### Option 2: Explicit Arguments

```python
@FunctionComponent
def UserCard(name, email, id, class_name, style, children, **props):
    return f"""
    <div {id} {class_name} {style}>
        <h3>{name}</h3>
        <p>{email}</p>
        <div class="card-body">
            {children}
        </div>
    </div>
    """
```

### Key Features

1.  **Automatic Property Injection**: The framework automatically injects the correct HTML attributes for `{id}`, `{class_name}`, and `{style}`.
2.  **State V2 Compatible**: Function components work seamlessly with `State()` and reactive updates.
3.  **Event Handling**: Events like `on_click` are handled automatically by the framework (passed via `**props`).
4.  **Children Support**: Use `{Props.children}` or `{children}` to render nested content.

### Example with State and Events

```python
@FunctionComponent
def Counter(**props):
    return f"""
    <div {Props.id} {Props.class_name} {Props.style}>
        0 {Props.children}
    </div>
    """

# Create component with initial value "0"
counter = Counter(id="my-counter", children="0")

# Make it reactive controlling the 'text' property (textContent)
# Note: This replaces the entire content of the div with the new text
state = State(counter, text="0")

# Update it
Button("Increment", on_click=state.text.set("5"))
```

---

## Using Hooks in FunctionComponents

FunctionComponents work seamlessly with all Dars hooks, enabling reactive and interactive behavior.

### useDynamic() - Reactive Bindings

Use `useDynamic()` to create reactive text that updates automatically when state changes:

```python
from dars.all import *

userState = State("user", name="John Doe", status="Active")

@FunctionComponent
def UserCard(**props):
    return f'''
    <div {Props.id} {Props.class_name} {Props.style}>
        <h3>Name: {useDynamic("user.name")}</h3>
        <p>Status: {useDynamic("user.status")}</p>
        {Props.children}
    </div>
    '''

# The name and status will update automatically when state changes
card = UserCard(id="user-card")
Button("Update", on_click=userState.name.set("Jane Doe"))
```

### useValue() - Initial Values with Selectors

Use `useValue()` with selectors to set initial values and enable value extraction:

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

### useWatch() - Side Effects

Use `useWatch()` to monitor state changes and execute side effects:

```python
from dars.all import *

app = App("Example of hooks")

cartState = State("cart", total=0.0)

@FunctionComponent
def CartSummary(total=0,**props):
    return f'''
    <div {Props.id} {Props.class_name} {Props.style}>
        <h3>Cart Total: ${useDynamic("cart.total")}</h3>
        {Props.children}
    </div>
    '''

# Watch for cart changes and log
app.useWatch("cart.total", log("Cart total changed!"))

@route("/")
def index():
    return Page(
        CartSummary(id="cart-summary", total=0),
        # Button to add $10 to cart total using V() with state path
        Button("Add $10", on_click=cartState.total.set(
            V("cart.total").float() + 10
        ))
    )

app.add_page("index", index(), title="hooks", index=True)

if __name__ == "__main__":
    app.rTimeCompile()
```

### Combining Multiple Hooks

You can combine multiple hooks for complex interactive components:

```python
from dars.all import *

app = App("Example of hooks")

productState = State("product", 
    name="Widget", 
    price=19.99, 
    quantity=1,
    total=19.99
)

@FunctionComponent
def ProductCard(**props):
    return f'''
    <div {Props.id} {Props.class_name} {Props.style}>
        <!-- useDynamic for reactive display -->
        <h3>{useDynamic("product.name")}</h3>
        <p>Price: ${useDynamic("product.price")}</p>
        <!-- useValue for editable quantity -->
        <h3>Number to multiply with price</h3>
        <input type="number" 
               value="{useValue("product.quantity", ".qty-input")}"
               min="1" />
        
        
        <!-- useDynamic for calculated total -->
        <p>Total: ${useDynamic("product.total")}</p>
        
        {Props.children}
    </div>
    '''

# Watch for total changes and show alert
app.useWatch("product.total", log("Total updated!"))

@route("/")
def index():
    return Page(
        ProductCard(id="product-card",name="Milk", price=100, quantity=0, total=0 ),
        Button(
            "Calculate Total",
            on_click=productState.total.set(
                V(".qty-input").int() * V("product.price").float()
            )
        )

    )

app.add_page("index", index(), title="hooks", index=True)

if __name__ == "__main__":
    app.rTimeCompile()
```

---

## Class Components (Legacy)

This is the older method of creating components by inheriting from the `Component` class. It is more verbose and requires manual handling of rendering logic.

```python
from dars.all import *
from dars.core.component import Component

class CustomComponent(Component):
    def __init__(self, title: str, id: str = None, **props):
        super().__init__(**props)
        self.title = title
        self.id = id
        # Manual event attachment
        self.set_event(EventTypes.CLICK, log('click'))

    def render(self, exporter: 'Exporter') -> str:
        # Manual children rendering
        children_html = self.render_children(exporter)
        
        return f'''
        <div class="my-component" id="{self.id}" style="{self.style}">
            <h2>{self.title}</h2>
            <div class="content">
                {children_html}
            </div>
        </div>
        '''
```

---
