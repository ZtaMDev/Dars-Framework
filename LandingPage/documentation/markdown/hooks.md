# Hooks System

Dars Framework introduces a **Hooks system** inspired by React, enabling reactive and stateful behavior in FunctionComponents.

## Overview

Hooks provide a way to add reactive capabilities to FunctionComponents without using class-based components. They enable features like:

- **Reactive state bindings** - Automatically update UI when data changes
- **External state integration** - Connect components to global state
- **Reusable stateful logic** - Share behavior across components

---

## useDynamic() - Reactive State Binding

The `useDynamic()` hook creates reactive bindings between external `State` objects and FunctionComponents.

### Basic Usage

```python
from dars.all import *

# Create state
userState = State("user", name="John Doe", email="john@example.com")

# Use in FunctionComponent with useDynamic
@FunctionComponent
def UserCard(**props):
    return f'''
    <div {Props.id} {Props.class_name} {Props.style}>
        <h3>Name: {useDynamic("user.name")}</h3>
        <p>Email: {useDynamic("user.email")}</p>
    </div>
    '''

# Render the component
card = UserCard(id="userCard", style={"padding": "20px"})

# When you update the state, the DOM automatically updates!
app.add_script(userState.name.set("Jane Doe"))  # UI updates instantly
```

### How It Works

1. **Initial Render**: `useDynamic()` creates a reactive span with the initial prop value
2. **State Changes**: When you call `.set()` on a state property, the hook intercepts it
3. **DOM Updates**: All matching reactive spans update automatically

### Syntax

```python
useDynamic(state_path: str) -> DynamicBinding
```

**Parameters:**
- `state_path`: Dot-notation path to state property (e.g., `"user.name"`, `"cart.total"`)

**Returns:**
- `DynamicBinding` object that renders as a reactive `<span>` element

### Complete Example

```python
from dars.all import *

app = App("User Profile Editor")

# Create state for user data
userState = State("user", 
    name="John Doe", 
    email="john@example.com",
    bio="Software Developer"
)

# Display component with reactive bindings
@FunctionComponent
def ProfileDisplay(**props):
    return f'''
    <div {Props.id} {Props.class_name} {Props.style}>
        <h2>{useDynamic("user.name")}</h2>
        <p>Email: {useDynamic("user.email")}</p>
        <p>Bio: {useDynamic("user.bio")}</p>
    </div>
    '''

# Edit form
def ProfileEditor():
    return Container(
        Text("Name:"),
        Input(id="nameInput", value="John Doe"),
        
        Text("Email:"),
        Input(id="emailInput", type="email", value="john@example.com"),
        
        Text("Bio:"),
        TextArea(id="bioInput", value="Software Developer"),
        
        Button("Save", on_click=[
            userState.name.set(getInputValue("nameInput")),
            userState.email.set(getInputValue("emailInput")),
            userState.bio.set(getInputValue("bioInput"))
        ])
    )

# Page
@route("/")
def index():
    return Page(
        ProfileDisplay(id="profile", style={"margin-bottom": "20px"}),
        ProfileEditor()
    )

app.add_page("index", index())

if __name__ == "__main__":
    app.rTimeCompile()
```

### Integration with State V2

`useDynamic()` works seamlessly with State V2's dynamic state system:

```python
# State V2 with ID
userState = State("user", name="John", age=25)

# Use in FunctionComponent
@FunctionComponent
def UserInfo(**props):
    return f'''
    <div {Props.id}>
        <p>Name: {useDynamic("user.name")}</p>
        <p>Age: {useDynamic("user.age")}</p>
    </div>
    '''

# Updates work automatically
btn = Button("Birthday", on_click=userState.age.increment(by=1))
```

### With `getInputValue()`

Combine `useDynamic()` with `getInputValue()` for form-to-display updates:

```python
state = State("product", title="", price=0)

@FunctionComponent
def ProductCard(**props):
    return f'''
    <div {Props.id}>
        <h3>{useDynamic("product.title")}</h3>
        <p>Price: ${useDynamic("product.price")}</p>
    </div>
    '''

# Form
form = Container(
    Input(id="titleInput", placeholder="Product name"),
    Input(id="priceInput", type="number", placeholder="Price"),
    Button("Update", on_click=[
        state.title.set(getInputValue("titleInput")),
        state.price.set(getInputValue("priceInput"))
    ])
)
```

### Multiple Components, Same State

Multiple components can bind to the same state - all update when state changes:

```python
state = State("counter", value=0)

@FunctionComponent
def Display1(**props):
    return f'<div {Props.id}>Display 1: {useDynamic("counter.value")}</div>'

@FunctionComponent
def Display2(**props):
    return f'<div {Props.id}>Display 2: {useDynamic("counter.value")}</div>'

# Both update when button is clicked
page = Page(
    Display1(id="d1"),
    Display2(id="d2"),
    Button("Increment", on_click=state.value.increment())
)
```

### Best Practices

**Do:**
- Use for simple reactive bindings in FunctionComponents
- Combine with `getInputValue()` for form updates
- Use consistent state naming (e.g., `"user"`, `"cart"`)

**Don't:**
- Use with non-existent state paths (will render empty)
- Use for complex state machines (use dState instead)
- Nest state paths more than 2 levels deep

### Limitations

- **One-way binding**: State → DOM only (not DOM → State)
- **Property depth**: Currently supports `stateName.property` format only
- **String values**: Best for text content; style objects need `.set()`

---
