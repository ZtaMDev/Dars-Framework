# Components Reference

Dars provides a comprehensive set of UI components for building modern, responsive, and cross-platform interfaces using Python. This page documents all core, advanced, and layout components, with detailed examples, property tables, and best practices.

---

## Table of Contents
- [Basic Components](#basic-components)
  - [Text](#text)
  - [Button](#button)
  - [Input](#input)
  - [Container](#container)
  - [Image](#image)
  - [Link](#link)
  - [Textarea](#textarea)
- [Advanced Components](#advanced-components)
  - [Card](#card)
  - [Modal](#modal)
  - [Navbar](#navbar)
  - [Checkbox](#checkbox)
  - [RadioButton](#radiobutton)
  - [Select](#select)
  - [Slider](#slider)
  - [DatePicker](#datepicker)
- [Layout Components](#layout-components)
  - [GridLayout](#gridlayout)
  - [FlexLayout](#flexlayout)
- [Styling and Interactivity](#styling-and-interactivity)
- [Best Practices](#best-practices)

---

## Basic Components

### Text

Displays static or dynamic text content.

```python
from dars.components.basic.text import Text

headline = Text(
    text="Main Title",
    id="main-title",
    class_name="headline",
    style={
        "font-size": "32px",
        "font-weight": "bold",
        "color": "#2c3e50",
        "margin-bottom": "20px",
        "text-align": "center"
    }
)
```

**Properties:**

| Property     | Type   | Description                | Example           |
|--------------|--------|----------------------------|-------------------|
| `text`       | str    | Text content               | `"Hello world"`   |
| `id`         | str    | Unique identifier          | `"title-main"`    |
| `class_name` | str    | CSS class name             | `"highlight"`     |
| `style`      | dict   | CSS style dictionary       | `{ "color": "red" }` |

---

### Button

Creates an interactive button that can trigger actions via scripts.

```python
from dars.components.basic.button import Button

submit_btn = Button(
    text="Submit",
    button_type="submit",  # "button", "submit", "reset"
    disabled=False,
    style={
        "background-color": "#3498db",
        "color": "white",
        "padding": "10px 20px",
        "border": "none",
        "border-radius": "4px"
    }
)
```

**Properties:**

| Property      | Type   | Description              | Values                          |
|---------------|--------|--------------------------|----------------------------------|
| `text`        | str    | Button label             | `"Send"`                        |
| `button_type` | str    | Button type              | `"button"`, `"submit"`, `"reset"`|
| `disabled`    | bool   | Disabled state           | `True`, `False`                  |
| `id`          | str    | Unique identifier        | `"submit-btn"`                   |
| `class_name`  | str    | CSS class                | `"primary-btn"`                  |
| `style`       | dict   | CSS style dictionary     | `{ "color": "white" }`           |

---

### Input

Text input field for user data entry.

```python
from dars.components.basic.input import Input

username_input = Input(
    value="",
    placeholder="Enter your username...",
    input_type="text",  # "text", "password", "email", "number", etc.
    disabled=False,
    readonly=False,
    required=True,
    max_length=30,
    style={
        "width": "300px",
        "padding": "10px",
        "border": "1px solid #ddd",
        "border-radius": "4px"
    }
)
```

**Properties:**

| Property      | Type   | Description            | Example/Values             |
|---------------|--------|------------------------|----------------------------|
| `value`       | str    | Initial value          | `"text"`                  |
| `placeholder` | str    | Placeholder text       | `"Enter your name"`        |
| `input_type`  | str    | Input type             | `"text"`, `"email"`, etc.  |
| `disabled`    | bool   | Disabled state         | `True`, `False`            |
| `readonly`    | bool   | Read-only              | `True`, `False`            |
| `required`    | bool   | Required field         | `True`, `False`            |
| `max_length`  | int    | Maximum length         | `50`                       |
| `min_length`  | int    | Minimum length         | `3`                        |
| `pattern`     | str    | Validation pattern     | `"[0-9]+"`                 |
| `id`          | str    | Unique identifier      | `"user-input"`             |
| `class_name`  | str    | CSS class              | `"input-field"`            |
| `style`       | dict   | CSS style dictionary   | `{ "width": "100%" }`      |

---

### Container

Flexible container for grouping components. Supports layout via `style`.

```python
from dars.components.basic.container import Container

vertical_layout = Container(
    children=[Text("Header"), Button("Action")],
    style={
        "display": "flex",
        "flex-direction": "column",
        "gap": "15px",
        "padding": "20px"
    }
)
```

**Properties:**

| Property   | Type  | Description               |
|------------|-------|---------------------------|
| `children` | list  | List of child components  |
| `id`       | str   | Unique identifier         |
| `class_name`| str  | CSS class                 |
| `style`    | dict  | CSS style dictionary      |

---

### Image

Displays images with optional alt, width, and height.

```python
from dars.components.basic.image import Image

logo = Image(
    src="static/logo.png",
    alt="Dars logo",
    width="120px",
    height="auto",
    class_name="responsive-img",
    style={
        "border-radius": "8px",
        "box-shadow": "0 4px 8px rgba(0,0,0,0.1)"
    }
)
```

**Properties:**

| Property   | Type   | Description           | Example              |
|------------|--------|-----------------------|----------------------|
| `src`      | str    | Image path            | `"images/logo.png"`  |
| `alt`      | str    | Alt text              | `"Logo"`             |
| `width`    | str    | CSS width             | `"100%"`, `"200px"`  |
| `height`   | str    | CSS height            | `"auto"`, `"150px"`  |
| `id`       | str    | Unique identifier     | `"main-img"`         |
| `class_name`| str   | CSS class             | `"img-fluid"`        |
| `style`    | dict   | CSS style dictionary  | `{ "border": "1px solid #eee" }` |

---

### Link

Navigation or external link.

```python
from dars.components.basic.link import Link

external_link = Link(
    text="Visit Google",
    href="https://www.google.com",
    target="_blank", # Open in new tab
    class_name="external-link",
    style={
        "color": "#007bff",
        "text-decoration": "none",
        "font-weight": "bold"
    }
)
```

**Properties:**

| Property   | Type   | Description           | Example/Values                  |
|------------|--------|-----------------------|---------------------------------|
| `text`     | str    | Link text             | `"Go to page"`                  |
| `href`     | str    | Destination URL       | `"/about"`, `"https://..."`     |
| `target`   | str    | Link target           | `"_self"`, `"_blank"`           |
| `id`       | str    | Unique identifier     | `"main-link"`                   |
| `class_name`| str   | CSS class             | `"nav-link"`                    |
| `style`    | dict   | CSS style dictionary  | `{ "color": "blue" }`           |

---

### Textarea

Multiline text input.

```python
from dars.components.basic.textarea import Textarea

comment_box = Textarea(
    value="Initial text",
    placeholder="Write your message here...",
    rows=5,
    cols=40,
    disabled=False,
    readonly=False,
    required=True,
    max_length=500,
    class_name="comment-box",
    style={
        "width": "100%",
        "padding": "10px",
        "border": "1px solid #ccc",
        "border-radius": "5px"
    }
)
```

**Properties:**

| Property      | Type   | Description          | Example/Values         |
|---------------|--------|----------------------|------------------------|
| `value`       | str    | Initial value        | `""`                  |
| `placeholder` | str    | Placeholder text     | `"Type here..."`      |
| `rows`        | int    | Number of rows       | `4`                    |
| `cols`        | int    | Number of columns    | `50`                   |
| `disabled`    | bool   | Disabled state       | `True`, `False`        |
| `readonly`    | bool   | Read-only            | `True`, `False`        |
| `required`    | bool   | Required field       | `True`, `False`        |
| `max_length`  | int    | Maximum length       | `500`                  |
| `id`          | str    | Unique identifier    | `"comment-box"`        |
| `class_name`  | str    | CSS class            | `"input-area"`         |
| `style`       | dict   | CSS style dictionary | `{ "width": "100%" }` |

---

## Advanced Components

### Card

Stylized container for grouping related content (title, body, actions).

```python
from dars.components.advanced.card import Card
from dars.components.basic.text import Text
from dars.components.basic.button import Button

my_card = Card(
    title="Card Title",
    children=[
        Text("This is the card content."),
        Button("Learn More")
    ],
    class_name="product-card",
    style={
        "background-color": "#fff",
        "border": "1px solid #e0e0e0",
        "border-radius": "10px",
        "padding": "20px",
        "box-shadow": "0 4px 8px rgba(0,0,0,0.05)"
    }
)
```

**Properties:**

| Property   | Type   | Description             |
|------------|--------|-------------------------|
| `title`    | str    | Card title              |
| `children` | list   | List of child components|
| `id`       | str    | Unique identifier       |
| `class_name`| str   | CSS class               |
| `style`    | dict   | CSS style dictionary    |

---

### Modal

Popup dialog overlaying main content.

```python
from dars.components.advanced.modal import Modal
from dars.components.basic.text import Text
from dars.components.basic.button import Button

welcome_modal = Modal(
    title="Welcome!",
    is_open=True, # or False for initially hidden
    children=[
        Text("This is your modal content."),
        Button("Close")
    ],
    class_name="welcome-modal",
    style={
        "background-color": "rgba(0, 0, 0, 0.7)" # Overlay style
    }
)
```

**Properties:**

| Property   | Type   | Description           |
|------------|--------|-----------------------|
| `title`    | str    | Modal title           |
| `is_open`  | bool   | Modal visibility      |
| `children` | list   | Modal content         |
| `id`       | str    | Unique identifier     |
| `class_name`| str   | CSS class             |
| `style`    | dict   | CSS style dictionary  |

---

### Navbar

Navigation bar, typically at the top of the page.

```python
from dars.components.advanced.navbar import Navbar
from dars.components.basic.link import Link

main_navbar = Navbar(
    brand="My App",
    children=[
        Link("Home", "/"),
        Link("About", "/about"),
        Link("Contact", "/contact")
    ],
    class_name="main-nav",
    style={
        "background-color": "#333",
        "color": "white",
        "padding": "15px 20px"
    }
)
```

**Properties:**

| Property   | Type   | Description           |
|------------|--------|-----------------------|
| `brand`    | str    | Brand/logo text       |
| `children` | list   | Navigation links      |
| `id`       | str    | Unique identifier     |
| `class_name`| str   | CSS class             |
| `style`    | dict   | CSS style dictionary  |

---

### Checkbox

Checkbox input for selecting options.

```python
from dars.components.basic.checkbox import Checkbox

accept_terms = Checkbox(
    label="I accept the terms",
    checked=True,
    style={
        "margin": "10px"
    }
)
```

**Properties:**

| Property   | Type   | Description           | Example/Values         |
|------------|--------|-----------------------|------------------------|
| `label`    | str    | Checkbox label        | `"Accept terms"`       |
| `checked`  | bool   | Checked state         | `True`, `False`        |
| `id`       | str    | Unique identifier     | `"accept-checkbox"`    |
| `class_name`| str   | CSS class             | `"checkbox-input"`     |
| `style`    | dict   | CSS style dictionary  | `{ "margin": "10px" }`|

---

### RadioButton

Radio button for selecting a single option from a group.

```python
from dars.components.basic.radio_button import RadioButton

option_a = RadioButton(
    label="Option A",
    name="group1",
    checked=False,
    style={
        "margin": "10px"
    }
)
```

**Properties:**

| Property   | Type   | Description           | Example/Values         |
|------------|--------|-----------------------|------------------------|
| `label`    | str    | Radio label           | `"Option A"`           |
| `name`     | str    | Group name            | `"group1"`             |
| `checked`  | bool   | Checked state         | `True`, `False`        |
| `id`       | str    | Unique identifier     | `"radio-a"`            |
| `class_name`| str   | CSS class             | `"radio-input"`        |
| `style`    | dict   | CSS style dictionary  | `{ "margin": "10px" }`|

---

### Select

Dropdown for selecting one option from a list.

```python
from dars.components.basic.select import Select

fruit_select = Select(
    options=["Apple", "Banana", "Cherry"],
    value="Banana",
    style={
        "width": "200px",
        "padding": "10px",
        "border": "1px solid #ccc"
    }
)
```

**Properties:**

| Property   | Type   | Description           | Example/Values         |
|------------|--------|-----------------------|------------------------|
| `options`  | list   | List of options       | `["One", "Two"]`      |
| `value`    | str    | Selected value        | `"Two"`               |
| `id`       | str    | Unique identifier     | `"select-fruit"`       |
| `class_name`| str   | CSS class             | `"select-input"`       |
| `style`    | dict   | CSS style dictionary  | `{ "width": "200px" }`|

---

### Slider

Slider for selecting a value in a range.

```python
from dars.components.basic.slider import Slider

volume_slider = Slider(
    min_value=0,
    max_value=100,
    value=50,
    show_value=True,
    style={
        "width": "200px",
        "padding": "10px"
    }
)
```

**Properties:**

| Property     | Type   | Description           | Example/Values         |
|--------------|--------|-----------------------|------------------------|
| `min_value`  | int    | Minimum value         | `0`                    |
| `max_value`  | int    | Maximum value         | `100`                  |
| `value`      | int    | Selected value        | `50`                   |
| `show_value` | bool   | Show value            | `True`, `False`        |
| `id`         | str    | Unique identifier     | `"slider-vol"`         |
| `class_name` | str    | CSS class             | `"slider-input"`       |
| `style`      | dict   | CSS style dictionary  | `{ "width": "200px" }`|

---

### DatePicker

Date selection input.

```python
from dars.components.basic.date_picker import DatePicker

date_picker = DatePicker(
    value="2025-08-06",
    style={
        "width": "200px",
        "padding": "10px",
        "border": "1px solid #ccc"
    }
)
```

**Properties:**

| Property   | Type   | Description           | Example/Values         |
|------------|--------|-----------------------|------------------------|
| `value`    | str    | Selected date         | `"2025-08-06"`         |
| `id`       | str    | Unique identifier     | `"date-picker"`        |
| `class_name`| str   | CSS class             | `"date-input"`         |
| `style`    | dict   | CSS style dictionary  | `{ "width": "200px" }`|

---

## Layout Components

### GridLayout

Responsive grid layout for arranging components in rows and columns.

```python
from dars.components.layout.grid import GridLayout
from dars.components.basic.text import Text

my_grid = GridLayout(
    columns=3,
    gap="16px",
    children=[
        Text("Column 1"),
        Text("Column 2"),
        Text("Column 3")
    ],
    style={
        "margin": "20px auto",
        "max-width": "900px"
    }
)
```

**Properties:**

| Property   | Type   | Description           | Example/Values         |
|------------|--------|-----------------------|------------------------|
| `columns`  | int    | Number of columns     | `3`                    |
| `gap`      | str    | Gap between columns   | `"16px"`, `"2em"`      |
| `children` | list   | List of components    |                        |
| `id`       | str    | Unique identifier     |                        |
| `class_name`| str   | CSS class             |                        |
| `style`    | dict   | CSS style dictionary  |                        |

---

### FlexLayout

Flexible layout for vertical or horizontal stacking.

```python
from dars.components.layout.flex import FlexLayout
from dars.components.basic.button import Button

my_flex = FlexLayout(
    direction="row",  # "row" or "column"
    gap="12px",
    children=[
        Button("Yes"),
        Button("No")
    ],
    style={
        "margin": "10px 0"
    }
)
```

**Properties:**

| Property    | Type   | Description           | Example/Values         |
|-------------|--------|-----------------------|------------------------|
| `direction` | str    | Flex direction        | `"row"`, `"column"`    |
| `gap`       | str    | Gap between items     | `"12px"`               |
| `children`  | list   | List of components    |                        |
| `id`        | str    | Unique identifier     |                        |
| `class_name`| str    | CSS class             |                        |
| `style`     | dict   | CSS style dictionary  |                        |

---

## Styling and Interactivity

Dars supports most standard CSS properties for styling components. You can pass a `style` dictionary to any component. Example:

```python
# Gradient background
from dars.components.basic.container import Container

gradient_bg = Container(
    style={
        "background": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
        "min-height": "100vh",
        "display": "flex",
        "align-items": "center",
        "justify-content": "center"
    }
)
```

**Common CSS Properties:**

- `width`, `height`, `min-width`, `max-width`
- `margin`, `padding`, `background-color`, `color`, `border`, `border-radius`
- `font-size`, `font-family`, `font-weight`, `text-align`, `line-height`
- `display`, `position`, `top`, `left`, `right`, `bottom`, `z-index`
- `flex-direction`, `justify-content`, `align-items`, `grid-template-columns`, `gap`
- `box-shadow`, `opacity`, `transition`, `transform`

### Adding Interactivity

To handle user events (click, input, etc.), use `InlineScript` or `ExternalScript` to inject JavaScript logic. Each component has a unique `id` for selection in JS.

```python
from dars.core.app import App
from dars.components.basic.button import Button
from dars.components.basic.text import Text
from dars.scripts.script import InlineScript

app = App(title="App with Events")

status_text = Text("Waiting for interaction...", id="status-message")
my_button = Button("Click me!", id="my-button")

frontend_script = InlineScript("""
document.getElementById("my-button").addEventListener("click", function() {
    alert("Click event detected!");
    document.getElementById("status-message").innerText = "Button clicked!";
});
""")

app.set_root(my_button)
app.add_child(status_text)
app.add_script(frontend_script)
```

**Common Events:**
- Mouse: `click`, `dblclick`, `mouseenter`, `mouseleave`, etc.
- Keyboard: `keydown`, `keyup`, `keypress`
- Form: `change`, `input`, `submit`, `focus`, `blur`
- Others: `load`, `error`, `resize`

---

## Best Practices

### Component Organization

```python
def create_header():
    return Container(
        children=[
            Text("My Application", style={"font-size": "24px", "font-weight": "bold"}),
            Text("Descriptive subtitle", style={"color": "#666"})
        ],
        style={
            "padding": "20px",
            "background-color": "#f8f9fa",
            "border-bottom": "1px solid #dee2e6"
        }
    )

def create_form():
    return Container(
        children=[
            Text("Contact Form", style={"font-size": "20px", "margin-bottom": "20px"}),
            Input(placeholder="Name", style={"margin-bottom": "10px"}),
            Input(placeholder="Email", input_type="email", style={"margin-bottom": "10px"}),
            Button("Send", style={"background-color": "#007bff", "color": "white"})
        ],
        style={
            "max-width": "400px",
            "margin": "20px auto",
            "padding": "20px"
        }
    )
```

### Style Reuse

```python
# Define common styles
BASE_BUTTON_STYLE = {
    "padding": "10px 20px",
    "border": "none",
    "border-radius": "4px",
    "font-size": "14px",
    "cursor": "pointer"
}

PRIMARY_BUTTON_STYLE = {
    **BASE_BUTTON_STYLE,
    "background-color": "#007bff",
    "color": "white"
}

SECONDARY_BUTTON_STYLE = {
    **BASE_BUTTON_STYLE,
    "background-color": "#6c757d",
    "color": "white"
}

# Usage
save_btn = Button("Save", style=PRIMARY_BUTTON_STYLE)
cancel_btn = Button("Cancel", style=SECONDARY_BUTTON_STYLE)
```

---

Dars components provide a solid foundation for building modern, responsive UIs in Python, exportable to multiple platforms while maintaining consistency and functionality.

For more advanced layouts, see [GridLayout](#gridlayout) and [FlexLayout](#flexlayout). For scripting, see [Scripts](scripts.md).

Dars provides a wide variety of UI components to build modern, responsive interfaces using only Python.

## Basic Components
- **Text**: Display static or dynamic text.
- **Button**: Interactive button.
- **Input**: Text input field.
- **Container**: Flexible container to group other components.
- **Image**: Display images.
- **Link**: Navigation links.
- **Textarea**: Multiline text area.

## Advanced Components
- **Checkbox** / **RadioButton** / **Select** / **Slider** / **DatePicker**
- **Card**, **Modal**, **Navbar**, **Table**, **Tabs**, **Accordion**, **ProgressBar**, **Spinner**, **Tooltip**

## Layout Components
- **GridLayout**: Responsive grid system.
- **FlexLayout**: Vertical/horizontal flexbox.
- **AnchorPoint**: Semantic anchor for layouts.

## Barrel Import
Import all main components with a single line:
```python
from dars.all import *
```

## Example Composition
```python
from dars.components.basic import Container, Text, Button

container = Container(children=[
    Text("Main title"),
    Button("Action")
])
```

See the documentation for each component for all properties and usage examples.
