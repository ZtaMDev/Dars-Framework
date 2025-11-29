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
card = UserCard("John Doe", "john@example.com", id="user-1", style={"padding": "20px"})
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
        self.set_event(EventTypes.CLICK, dScript("console.log('click')"))

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

