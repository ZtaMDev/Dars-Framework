The documentstion of dars is moving to the documentation official website please visit https://ztamdev.github.io/Dars-Framework/documentation.html because this documents will be deprecated in some time...

# Dars - Components Documentation

---

## Barrel Import

You can now import all main components and modules with a single line:

```python
from dars.all import *
```

This simplifies integration and improves the developer experience. 
> But if you crate your own components it can cause conflicts with names of your components and built in components if they have the same name.

---

## Introduction to Components

Components are the fundamental elements of Dars that represent UI elements. Each component encapsulates its appearance, behavior, and state, allowing you to create complex interfaces by composing simple elements.

To learn how to create your own custom components, refer to the documentation in [Custom Components](#custom-components-in-dars-framework).

## Event Handling with dScript

Dars provides a powerful way to handle user interactions through the `dScript` class. You can attach event handlers to interactive components like `Button` and `Input` to create dynamic and responsive user interfaces.

For a complete list of available event types and how to use them, refer to the documentation in [Events](#events-in-dars).

### Basic Usage

```python
from dars.scripts.dscript import dScript

# Button with click handler
button = Button(
    text="Click me",
    on_click=dScript("""
        function handleClick(event) {
            alert('Button was clicked!');
            // Access the button element
            const button = event.target;
            // Toggle a class on click
            button.classList.toggle('clicked');
        }
    """)
)

# Input with change handler
input_field = Input(
    placeholder="Type something...",
    on_change=dScript("""
        function handleChange(event) {
            console.log('Input value changed to:', event.target.value);
            // Add validation or other logic here
            if (event.target.value.length < 3) {
                event.target.style.borderColor = 'red';
            } else {
                event.target.style.borderColor = 'green';
            }
        }
    """
)
```

### Available Events

| Component | Event | Description |
|-----------|-------|-------------|
| `Button` | `on_click` | Triggered when the button is clicked |
| `Button` | `on_double_click` | Triggered on double click |
| `Button` | `on_mouse_enter` | Triggered when mouse enters the button |
| `Button` | `on_mouse_leave` | Triggered when mouse leaves the button |
| `Input` | `on_change` | Triggered when input value changes |
| `Input` | `on_key_up` | Triggered when a key is released |
| `Input` | `on_key_down` | Triggered when a key is pressed |

### Best Practices

1. **Use Named Functions**: Makes debugging easier and allows reusing the same function for multiple events.
2. **Keep Handlers Small**: Move complex logic to separate functions in your JavaScript code.
3. **Access Event Object**: The event object provides useful properties like `target`, `keyCode`, etc.
4. **Return `false`** to prevent default behavior when needed.

---

### Quick Access

- [Base Component Class](#base-component-class)
- [Component Search](#component-search-and-modification)
- [Page](#page)
- [Text](#text)
- [Button](#button)
- [Input](#input)
- [Container](#container)
- [Markdown](#markdown)
- [Image](#image)
- [Link](#link)
- [Textarea](#textarea)
- [Checkbox](#checkbox)
- [RadioButton](#radiobutton)
- [Select](#select)
- [Slider](#slider)
- [ProgressBar](#progressBar)
- [Tooltip](#tooltip)
- [DatePicker](#datepicker)
- [Card](#card)
- [Modal](#modal)
- [Navbar](#navbar)
- [Accordion](#accordion)
- [Tabs](#tabs)
- [Table](#table)
- [Layout Components](#layout-components)
  - [GridLayout](#gridlayout)
  - [FlexLayout](#flexlayout)
  - [LayoutBase](#layoutbase)
  - [AnchorPoint](#anchorpoint)

---

## Base Component Class

All components in Dars inherit from the base `Component` class, which provides common functionality:

```python
from dars.core.component import Component

class Component(ABC):
    def __init__(self, **props):
        self.props = props
        self.children = []
        self.parent = None
        self.id = props.get("id")
        self.class_name = props.get("class_name")
        self.style = props.get("style", {})
        self.events = {}
```

### Common Properties

All components support these basic properties:

- **id**: Unique component identifier
- **class_name**: CSS class for additional styles
- **style**: Dictionary of CSS styles
- **children**: List of child components (for containers)

### Component-Search-and-Modification

All components include a powerful search and modification system through the `find()` method. This allows you to search for components in the component tree and modify their attributes using a fluent interface.

#### Basic Search

```python
# Find by ID
component.find(id="search-button")

# Find by CSS class
component.find(class_name="primary-button")

# Find by component type
component.find(type="Button")  # or type=Button

# Find using a custom predicate
component.find(predicate=lambda c: "welcome" in c.text.lower())
```

#### Chained Searches

You can chain multiple `find()` calls to search within the results of previous searches:

```python
# Find a container and then search within it
component.find(id="main-container")\
        .find(type="Text")\
        .attr(text="New text")

# Multiple levels of search
component.find(class_name="section")\
        .find(type="Container")\
        .find(id="special-text")\
        .attr(text="Modified text")
```

#### Modifying Components

Use the `attr()` method to modify the found components:

```python
# Modify styles
component.find(type="Button").attr(
    style={"background-color": "red", "color": "white"}
)

# Modify class names
component.find(class_name="btn").attr(
    class_name="btn primary"
)

# Modify component-specific attributes
component.find(type="Text").attr(
    text="New content"
)

# Multiple modifications at once
component.find(type="Input").attr(
    placeholder="Type here...",
    style={"padding": "10px"},
    class_name="modern-input"
)
```

#### Getting Results

```python
# Get all matched components
components = component.find(type="Button").get()

# Get only the first match
first_button = component.find(type="Button").first()
```

#### Search Parameters

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `id` | str | Search by component ID | `find(id="search-btn")` |
| `class_name` | str | Search by CSS class | `find(class_name="primary")` |
| `type` | str/Type | Search by component type | `find(type="Button")` or `find(type=Button)` |
| `predicate` | Callable | Custom search function | `find(predicate=lambda c: len(c.children) > 0)` |

### Page

The `Page` component represents the root of a multipage app. It can contain other components and scripts specific to that page.

#### Syntax

```python
from dars.components.basic import Page, Text, Button
from dars.scripts.script import InlineScript
page = Page(
    Text("Bienvenido!"),
    Button("Click aquí", id="btn-demo")
)
# Añadir script JS solo a esta página
page.add_script(InlineScript("""
document.addEventListener('DOMContentLoaded', function() {
    var btn = document.getElementById('btn-demo');
    if (btn) btn.onclick = () => alert('¡Botón de esta página!');
});
"""))
```

Use `Page` as the root of each page in the multipage system. Allows passing children directly as arguments and JS scripts per page.

#### Properties

| Property    | Type   | Description                                         |
|-------------|--------|-----------------------------------------------------|
| `children`  | list   | List of child components                            |
| `anchors`   | dict   | Optional anchor points for child placement          |

#### Page Scripts System

The new page scripts system allows assigning scripts to specific pages instead of globally:

* **Adding Scripts**:
  Use the `add_script()` method on a page instance.

```python
from dars.scripts.dscript import dScript

index.add_script(
    dScript(code="console.log('Hello world')")
)
```

### Text

The `Text` component displays static or dynamic text.

#### Syntax

```python
from dars.components.basic.text import Text

text = Text(
    text="Contenido del text",
    id="mi-text",
    class_name="text-principal",
    style={
        "font-size": "16px",
        "color": "#333",
        "font-weight": "bold"
    }
)
```

#### Properties

| Property | Type | Description | Example |
|-----------|------|-------------|---------|
| `text` | str | Text content | `"Hello world"` |
| `id` | str | Unique identifier | `"title-primary"` |
| `class_name` | str | CSS class | `"text-highlight"` |
| `style` | dict | CSS styles | `{"color": "red"}` |

#### Common Styles

```python
# Título principal
title = Text(
    text="Título Principal",
    style={
        "font-size": "32px",
        "font-weight": "bold",
        "color": "#2c3e50",
        "margin-bottom": "20px",
        "text-align": "center"
    }
)

# Párrafo de contenido
paragraph = Text(
    text="Este es un párrafo de ejemplo con contenido descriptivo.",
    style={
        "font-size": "16px",
        "line-height": "1.6",
        "color": "#34495e",
        "margin-bottom": "15px"
    }
)

# Texto pequeño
note = Text(
    text="Nota: Esta información es importante.",
    style={
        "font-size": "12px",
        "color": "#7f8c8d",
        "font-style": "italic"
    }
)
```

### Button

The `Button` component creates interactive buttons that can execute actions.

#### Syntax

```python
from dars.components.basic.button import Button

boton = Button(
    text="Hacer clic",
    button_type="button",  # "button", "submit", "reset"
    disabled=False,
    on_click=dScript("""
        function handleClick() {
            alert('Button clicked!');
        }
    """)
    style={
        "background-color": "#3498db",
        "color": "white",
        "padding": "10px 20px",
        "border": "none",
        "border-radius": "4px"
    }
)
```

#### Properties

| Property | Type | Description | Values |
|-----------|------|-------------|---------|
| `text` | str | Button text | `"Enviar"` |
| `button_type` | str | Button type | `"button"`, `"submit"`, `"reset"` |
| `disabled` | bool | Si está deshabilitado | `True`, `False` |
| `on_click` | dScript | Click handler | `dScript("function() { ... }")` |
| `on_double_click` | dScript | Double click handler | `dScript("function() { ... }")` |
| `on_mouse_enter` | dScript | Mouse enter handler | `dScript("function() { ... }")` |
| `on_mouse_leave` | dScript | Mouse leave handler | `dScript("function() { ... }")` |
| `on_key_up` | dScript | Key up handler | `dScript("function(e) { ... }")` |
| `on_key_down` | dScript | Key down handler | `dScript("function(e) { ... }")` |

#### Button Examples

```python
# Primary Button
primary_button = Button(
    text="Acción Principal",
    style={
        "background-color": "#007bff",
        "color": "white",
        "padding": "12px 24px",
        "border": "none",
        "border-radius": "6px",
        "font-size": "16px",
        "font-weight": "500",
        "cursor": "pointer",
        "transition": "background-color 0.3s"
    }
)

# Secondary Button
secondary_button = Button(
    text="Cancelar",
    style={
        "background-color": "transparent",
        "color": "#6c757d",
        "padding": "12px 24px",
        "border": "1px solid #6c757d",
        "border-radius": "6px",
        "font-size": "16px",
        "cursor": "pointer"
    }
)

# Danger Button
delete_button = Button(
    text="Eliminar",
    style={
        "background-color": "#dc3545",
        "color": "white",
        "padding": "8px 16px",
        "border": "none",
        "border-radius": "4px",
        "font-size": "14px"
    }
)

# Disabled Button
disabled_button = Button(
    text="No disponible",
    disabled=True,
    style={
        "background-color": "#e9ecef",
        "color": "#6c757d",
        "padding": "10px 20px",
        "border": "none",
        "border-radius": "4px",
        "cursor": "not-allowed"
    }
)
```

### Input

The `Input` component allows user data entry.

#### Syntax

```python
from dars.components.basic.input import Input

entrada = Input(
    value="Valor inicial",
    placeholder="Escribe aquí...",
    input_type="text",  # "text", "password", "email", "number", etc.
    disabled=False,
    readonly=False,
    required=False,
    max_length=100,
    on_change=dScript("""
        function handleChange(event) {
            console.log('Input changed:', event.target.value);
        }
    """)
    style={
        "width": "300px",
        "padding": "10px",
        "border": "1px solid #ddd",
        "border-radius": "4px"
    }
)
```

#### Properties

| Property | Type | Description | Values |
|-----------|------|-------------|---------|
| `value` | str | Initial value | `"text"` |
| `placeholder` | str | Help text | `"Ingresa tu name"` |
| `input_type` | str | Tipo de entrada | `"text"`, `"password"`, `"email"`, `"number"` |
| `disabled` | bool | Si está deshabilitado | `True`, `False` |
| `readonly` | bool | Solo lectura | `True`, `False` |
| `required` | bool | Campo obligatorio | `True`, `False` |
| `on_change` | dScript | Change handler | `dScript("function(e) { ... }")` |
| `on_key_up` | dScript | Key up handler | `dScript("function(e) { ... }")` |
| `on_key_down` | dScript | Key down handler | `dScript("function(e) { ... }")` |
| `max_length` | int | Longitud máxima | `50` |
| `min_length` | int | Longitud mínima | `3` |
| `pattern` | str | Validation pattern | `"[0-9]+"` |

#### Input Types

```python
# Basic text input
name = Input(
    placeholder="Ingresa tu name",
    input_type="text",
    required=True,
    style={
        "width": "100%",
        "padding": "12px",
        "border": "2px solid #e1e5e9",
        "border-radius": "8px",
        "font-size": "16px"
    }
)

# Email input
email = Input(
    placeholder="tu@email.com",
    input_type="email",
    required=True,
    style={
        "width": "100%",
        "padding": "12px",
        "border": "2px solid #e1e5e9",
        "border-radius": "8px"
    }
)

# Password input
password = Input(
    placeholder="Contraseña",
    input_type="password",
    required=True,
    min_length=8,
    style={
        "width": "100%",
        "padding": "12px",
        "border": "2px solid #e1e5e9",
        "border-radius": "8px"
    }
)

# Numeric input
edad = Input(
    placeholder="Edad",
    input_type="number",
    style={
        "width": "100px",
        "padding": "8px",
        "border": "1px solid #ccc",
        "border-radius": "4px",
        "text-align": "center"
    }
)

# Search input
busqueda = Input(
    placeholder="Buscar...",
    input_type="search",
    style={
        "width": "300px",
        "padding": "10px 15px",
        "border": "1px solid #ddd",
        "border-radius": "20px",
        "background-color": "#f8f9fa"
    }
)
```

### Container

The `Container` component is a container that can hold other components. It supports multiple ways to add child components.

#### Syntax

```python
from dars.components.basic.container import Container

# Method 1: Pass components as arguments
container = Container(
    Text("Hello"),
    Button("Click me"),
    style={
        "display": "flex",
        "flex-direction": "column",
        "padding": "20px",
        "background-color": "#f8f9fa"
    }
)

# Method 2: Use additional_children parameter
components = [Text("Hello"), Button("Click me")]
container = Container(
    additional_children=components,
    style={
        "display": "flex",
        "flex-direction": "column",
        "padding": "20px",
        "background-color": "#f8f9fa"
    }
)

# Method 3: Add children after creation
container = Container(style={
    "display": "flex",
    "flex-direction": "column",
    "padding": "20px",
    "background-color": "#f8f9fa"
})
container.add_child(Text("Hello"))
container.add_child(Button("Click me"))
```

#### Properties

| Property | Type | Description |
|-----------|------|-------------|
| `children` | tuple | Components passed as positional arguments |
| `additional_children` | list | Optional list of additional components |

#### Container Layouts

```python
# Vertical layout (column)
columna = Container(
    style={
        "display": "flex",
        "flex-direction": "column",
        "gap": "15px",
        "padding": "20px"
    }
)

# Horizontal layout (row)
fila = Container(
    style={
        "display": "flex",
        "flex-direction": "row",
        "gap": "20px",
        "align-items": "center"
    }
)

# Layout centrado
centrado = Container(
    style={
        "display": "flex",
        "justify-content": "center",
        "align-items": "center",
        "min-height": "100vh",
        "background-color": "#f0f2f5"
    }
)

# Card/Tarjeta
tarjeta = Container(
    style={
        "background-color": "white",
        "border-radius": "12px",
        "padding": "24px",
        "box-shadow": "0 2px 10px rgba(0,0,0,0.1)",
        "max-width": "400px",
        "margin": "20px auto"
    }
)

# Sidebar
sidebar = Container(
    style={
        "width": "250px",
        "height": "100vh",
        "background-color": "#2c3e50",
        "padding": "20px",
        "position": "fixed",
        "left": "0",
        "top": "0"
    }
)
```

# Markdown

The `Markdown` component allows you to render markdown content directly in your Dars applications, converting markdown syntax to beautiful HTML with proper styling.

## Syntax

```python
from dars.components.basic.markdown import Markdown

# From string content
markdown_component = Markdown(
    content="# Welcome\nThis is **markdown** content",
    id="my-markdown",
    class_name="custom-markdown",
    style={"padding": "20px"}
)

# From file
markdown_from_file = Markdown(
    file_path="README.md",
    id="documentation",
    dark_theme=True
)
```

## Properties

| Property | Type | Description | Example |
|-----------|------|-------------|---------|
| `content` | str | Markdown content as string | `"# Heading"` |
| `file_path` | str | Path to a markdown file | `"docs/intro.md"` |
| `dark_theme` | bool | Enable dark theme styling | `True` |
| `id` | str | Component ID | `"markdown-content"` |
| `class_name` | str | CSS class | `"markdown-body"` |
| `style` | dict | CSS styles | `{"fontSize": "16px"}` |

## Methods

| Method | Description | Example |
|--------|-------------|---------|
| `update_content(new_content=None, new_file_path=None)` | Update markdown content | `markdown_component.update_content(new_content="# New")` |
| `set_dark_theme(enabled=True)` | Enable/disable dark theme | `markdown_component.set_dark_theme(True)` |

## Examples

```python
# Simple markdown from string
simple_md = Markdown(
    content="# Hello\nThis is a **markdown** example",
    style={"maxWidth": "800px", "margin": "0 auto"}
)

# Load from file with dark theme
docs_md = Markdown(
    file_path="documentation.md",
    dark_theme=True,
    class_name="docs-content"
)

# Update content dynamically
simple_md.update_content(new_content="# Updated\nNew content here")
```

## Dependencies

The Markdown component requires the `markdown2` library. Included with the framework.

## Supported Markdown Features

- Headers (`#`, `##`, `###`)
- **Bold** and *italic* text
- Lists (ordered and unordered)
- [Links](https://github.com/ZtaMDev/Dars-Framework)
- `Inline code` and code blocks
- Tables
- Blockquotes
- Images
- Horizontal rules

## Styling

The Markdown component includes comprehensive default styling for both light and dark themes:

```python
# Light theme (default)
markdown_light = Markdown(content="# Light theme")

# Dark theme
markdown_dark = Markdown(
    content="# Dark theme", 
    dark_theme=True,
    style={"padding": "20px", "borderRadius": "8px"}
)
```

## Best Practices

1. Use file paths for large documentation content
2. Enable dark theme for better readability in low-light environments
3. Combine with layout components for responsive designs
4. Use the update methods for dynamic content changes

## Integration Example

```python
from dars.core.app import App
from dars.components.basic.markdown import Markdown
from dars.components.basic.container import Container

app = App(title="Documentation Viewer")

# Load documentation from file
docs = Markdown(
    file_path="README.md",
    dark_theme=True,
    class_name="documentation",
    style={
        "maxWidth": "800px",
        "margin": "0 auto",
        "padding": "40px",
        "lineHeight": "1.6"
    }
)

app.set_root(Container(children=[docs]))
```

This component is perfect for creating documentation pages, blog posts, content management systems, and any application that needs to display formatted text content.

### Image

The `Image` component displays images.

#### Syntax

```python
from dars.components.basic.image import Image

image = Image(
    src="path/to/your/image.jpg",
    alt="Descripción de la image",
    width="300px",
    height="200px",
    class_name="responsive-img",
    style={
        "border-radius": "8px",
        "box-shadow": "0 4px 8px rgba(0,0,0,0.1)"
    }
)
```

#### Properties

| Property | Type | Description | Example |
|-----------|------|-------------|---------|
| `src` | str | Image path | `"images/logo.png"` |
| `alt` | str | Alternative text | `"Logo of the company"` |
| `width` | str | Ancho de la image (CSS) | `"100%"`, `"200px"` |
| `height` | str | Alto de la image (CSS) | `"auto"`, `"150px"` |

### Link

The `Link` component creates navigation links.

#### Syntax

```python
from dars.components.basic.link import Link

link = Link(
    text="Visitar Google",
    href="https://www.google.com",
    target="_blank", # Abre en una nueva pestaña
    class_name="external-link",
    style={
        "color": "#007bff",
        "text-decoration": "none",
        "font-weight": "bold"
    }
)
```

#### Properties

| Property | Type | Description | Values |
|-----------|------|-------------|---------|
| `text` | str | Link text | `"Ir a la página"` |
| `href` | str | URL of destination | `"/about"`, `"https://example.com"` |
| `target` | str | Dónde abrir el link | `"_self"` (misma pestaña), `"_blank"` (nueva pestaña) |

### Textarea

The `Textarea` component allows for multi-line text input.

#### Syntax

```python
from dars.components.basic.textarea import Textarea

area_text = Textarea(
    value="Texto inicial",
    placeholder="Escribe tu mensaje aquí...",
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

#### Properties

| Property | Type | Description | Values |
|-----------|------|-------------|---------|
| `value` | str | Initial value | `""` |
| `placeholder` | str | Help text | `"Escribe aquí..."` |
| `rows` | int | Número de filas visibles | `4` |
| `cols` | int | Número de columnas visibles | `50` |
| `disabled` | bool | Si está deshabilitado | `True`, `False` |
| `readonly` | bool | Solo lectura | `True`, `False` |
| `required` | bool | Campo obligatorio | `True`, `False` |
| `max_length` | int | Longitud máxima | `500` |

---

---

### ProgressBar

The `ProgressBar` component visually displays progress for a task, such as loading or completion percentage.

#### Syntax

```python
from dars.components.basic.progressbar import ProgressBar

progress = ProgressBar(value=40, max_value=100)
```

#### Properties

| Property    | Type | Description                       |
|-------------|------|-----------------------------------|
| `value`     | int  | Current progress value            |
| `max_value` | int  | Maximum value (default: 100)      |

#### Example

```python
progress = ProgressBar(value=75, max_value=100)
```

---

### Tooltip

The `Tooltip` component displays a tooltip when hovering over a child component.

#### Syntax

```python
from dars.components.basic.tooltip import Tooltip
from dars.components.basic.button import Button

tooltip = Tooltip(
    text="More info",
    child=Button(text="Hover me")
)
```

#### Properties

| Property   | Type      | Description                             |
|------------|-----------|-----------------------------------------|
| `text`     | str       | Tooltip text                            |
| `child`    | Component | Component to wrap                       |
| `position` | str       | Tooltip position (e.g., "top")          |

#### Example

```python
tooltip = Tooltip(text="Help", child=Button(text="?"))
```

---

### Accordion

The `Accordion` component creates a vertically stacked set of expandable/collapsible panels for organizing content.

#### Syntax

```python
from dars.components.advanced.accordion import Accordion

accordion = Accordion(
    items=[
        {"title": "Section 1", "content": "Content for section 1"},
        {"title": "Section 2", "content": "Content for section 2"}
    ],
    allow_multiple=False
)
```

#### Properties

| Property         | Type    | Description                                         |
|------------------|---------|-----------------------------------------------------|
| `items`          | list    | List of dicts with `title` and `content`            |
| `allow_multiple` | bool    | Allow multiple sections open at once                |

#### Example

```python
accordion = Accordion(
    items=[
        {"title": "FAQ 1", "content": "Answer 1"},
        {"title": "FAQ 2", "content": "Answer 2"}
    ]
)
```

---

### Tabs

The `Tabs` component allows navigation between different views or content panels.

> **New in 1.0.5:** The exporter now recursively detects Tabs at any nesting level (including inside containers, panels, or multipage apps) for `minimum_logic` and JS injection. You can safely nest Tabs in any structure and the export will work as expected.


#### Syntax

```python
from dars.components.advanced.tabs import Tabs

tabs = Tabs(
    tabs=[
        {"label": "Tab 1", "content": "Content 1"},
        {"label": "Tab 2", "content": "Content 2"}
    ],
    default_index=0
)
```

#### Properties

| Property        | Type | Description                              |
|-----------------|------|------------------------------------------|
| `tabs`          | list | List of dicts with `label` and `content` |
| `default_index` | int  | Index of the initially selected tab      |

#### Example

```python
tabs = Tabs(
    tabs=[
        {"label": "Overview", "content": "Main content"},
        {"label": "Details", "content": "Detailed info"}
    ],
    default_index=0
)
```

---

### Table

The `Table` component displays tabular data with rows and columns.

#### Syntax

```python
from dars.components.advanced.table import Table

table = Table(
    columns=["Name", "Age", "Country"],
    data=[
        ["Alice", 30, "USA"],
        ["Bob", 25, "UK"]
    ]
)
```

#### Properties

| Property   | Type   | Description                       |
|------------|--------|-----------------------------------|
| `columns`  | list   | List of column headers            |
| `data`     | list   | List of rows (each a list/tuple)  |

#### Example

```python
table = Table(
    columns=["Product", "Price"],
    data=[
        ["Book", "$10"],
        ["Pen", "$2"]
    ]
)
```

---

## Layout Components

### GridLayout

The `GridLayout` component provides a responsive grid-based layout with customizable rows, columns, gaps, and anchor points for precise positioning of children.

#### Syntax

```python
from dars.components.layout.grid import GridLayout
from dars.components.basic.text import Text

grid = GridLayout(
    rows=2,
    cols=2,
    gap="24px",
    children=[
        Text("Top Left"),
        Text("Top Right"),
        Text("Bottom Left"),
        Text("Bottom Right")
    ]
)
```

#### Properties

| Property   | Type   | Description                                 |
|------------|--------|---------------------------------------------|
| `rows`     | int    | Number of grid rows                         |
| `cols`     | int    | Number of grid columns                      |
| `gap`      | str    | Gap between grid cells (e.g., "16px")      |
| `children` | list   | List of child components                    |
| `anchors`  | dict   | Optional anchor points for child placement  |

#### Example

```python
grid = GridLayout(
    rows=3,
    cols=2,
    gap="16px",
    children=[Text(f"Cell {i}") for i in range(6)]
)
```

---

### FlexLayout

The `FlexLayout` component provides a responsive flexbox layout, supporting direction, wrap, alignment, and gap between children. Useful for row/column layouts.

#### Syntax

```python
from dars.components.layout.flex import FlexLayout
from dars.components.basic.button import Button

flex = FlexLayout(
    direction="row",
    justify="space-between",
    align="center",
    gap="12px",
    children=[Button("A"), Button("B"), Button("C")]
)
```

#### Properties

| Property    | Type   | Description                                         |
|-------------|--------|-----------------------------------------------------|
| `direction` | str    | Flex direction: "row" or "column"                   |
| `wrap`      | str    | Flex wrap: "wrap" or "nowrap"                       |
| `justify`   | str    | Justify content: e.g., "flex-start", "center"      |
| `align`     | str    | Align items: e.g., "stretch", "center"             |
| `gap`       | str    | Gap between children (e.g., "16px")                |
| `children`  | list   | List of child components                            |
| `anchors`   | dict   | Optional anchor points for child placement          |

#### Example

```python
flex = FlexLayout(
    direction="column",
    gap="24px",
    children=[Button("Save"), Button("Cancel")]
)
```

---

### LayoutBase

The `LayoutBase` component is the base class for all layout components. It allows adding children and anchor/positioning info. You typically use `FlexLayout` or `GridLayout` directly.

#### Syntax

```python
from dars.components.layout.grid import LayoutBase
from dars.components.basic.text import Text

layout = LayoutBase(
    children=[Text("Item 1"), Text("Item 2")],
    anchors={}
)
```

#### Properties

| Property    | Type   | Description                    |
|-------------|--------|--------------------------------|
| `children`  | list   | List of child components       |
| `anchors`   | dict   | Anchor/positioning information |

---

### AnchorPoint

The `AnchorPoint` class represents an anchor or alignment point for a child in a layout (e.g., top, left, right, bottom, center, percent, or px).

#### Syntax

```python
from dars.components.layout.anchor import AnchorPoint

anchor = AnchorPoint(x="left", y="top", name="top-left")
```

#### Properties

| Property | Type | Description                                      |
|----------|------|--------------------------------------------------|
| `x`      | str  | Horizontal alignment (e.g., "left", "center")    |
| `y`      | str  | Vertical alignment (e.g., "top", "center")       |
| `name`   | str  | Optional semantic name for the anchor            |

#### Example

```python
anchor = AnchorPoint(x="50%", y="50%", name="center")
```

---

### Card

The `Card` component is a styled container to group related content, such as a title and other components.

#### Syntax

```python
from dars.components.basic.card import Card
from dars.components.basic.text import Text
from dars.components.basic.button import Button

my_card = Card(
    title="Título de la Tarjeta",
    children=[
        Text("Este es el contenido de la tarjeta."),
        Button("Ver más")
    ],
    class_name="product-card",
    style={
        "background-color": "#ffffff",
        "border": "1px solid #e0e0e0",
        "border-radius": "10px",
        "padding": "20px",
        "box-shadow": "0 4px 8px rgba(0,0,0,0.05)"
    }
)
```

#### Properties

| Property | Type | Description |
|-----------|------|-------------|
| `title` | str | Card title |
| `children` | list | List of child components |

#### Example

```python
my_card = Card(
    title="Título de la Tarjeta",
    children=[
        Text("Este es el contenido de la tarjeta."),
        Button("Ver más")
    ],
    class_name="product-card",
    style={
        "background-color": "#ffffff",
        "border": "1px solid #e0e0e0",
        "border-radius": "10px",
        "padding": "20px",
        "box-shadow": "0 4px 8px rgba(0,0,0,0.05)"
    }
)
```

---

### Modal

The `Modal` component creates an overlay window that appears on top of the main page content.

> **New in 1.0.5:** Modal is now exported as hidden by default (`hidden` attribute and `dars-modal-hidden` class) if `is_open=False`, preventing any visual flicker on page load, even if CSS/JS loads slowly.

#### Syntax

```python
from dars.components.advanced.modal import Modal
from dars.components.basic.text import Text
from dars.components.basic.button import Button

my_modal = Modal(
    title="Welcome to the Modal",
    is_open=False, # Now hidden from the very first render
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

#### Properties

| Property   | Type | Description |
|------------|------|------------------------------------------------------------|
| `title`    | str  | Modal title |
| `is_open`  | bool | Controls modal visibility (`True` to show, `False` to hide). If `False`, modal is hidden from exported HTML. |
| `children` | list | List of child components |

#### Updated Example

```python
my_modal = Modal(
    title="Welcome to the Modal",
    is_open=False,  # Hidden from the very first render
    children=[
        Text("This is your modal content."),
        Button("Close")
    ],
    class_name="welcome-modal",
    style={
        "background-color": "rgba(0, 0, 0, 0.7)"
    }
)
```

> **Note:** The exporter now recursively detects advanced components (Tabs, Accordion, Modal, Card) at any nesting level, including inside multipage apps, and applies `minimum_logic` robustly.

---

### Navbar

The `Navbar` component creates a navigation bar, commonly used at the top of pages.

#### Syntax

```python
from dars.components.advanced.navbar import Navbar
from dars.components.basic.link import Link

my_navbar = Navbar(
    brand="Mi App",
    children=[
        Link("Inicio", "/"),
        Link("Acerca de", "/about"),
        Link("Contacto", "/contact")
    ],
    class_name="main-nav",
    style={
        "background-color": "#333",
        "color": "white",
        "padding": "15px 20px"
    }
)
```

#### Properties

| Property | Type | Description |
|-----------|------|-------------|
| `brand` | str | Texto o componente para la marca/logo de la navegación |
| `children` | list | List of child components (navigation items, usually `Link`s) |

## Additional Components

### Checkbox

The `Checkbox` component allows users to select options.

#### Syntax

```python
from dars.components.basic.checkbox import Checkbox

mi_checkbox = Checkbox(
    label="Acepto términos",
    checked=True,
    style={
        "margin": "10px"
    }
)
```

#### Properties

| Property | Type | Description | Values |
|-----------|------|-------------|---------|
| `label` | str | Texto de la etiqueta | `"Acepto términos"` |
| `checked` | bool | Estado de selección | `True`, `False` |

### RadioButton

The `RadioButton` component allows users to select one option from a group of options.

#### Syntax

```python
from dars.components.basic.radio_button import RadioButton

mi_radio_button = RadioButton(
    label="Opción A",
    name="grupo1",
    checked=False,
    style={
        "margin": "10px"
    }
)
```

#### Properties

| Property | Type | Description | Values |
|-----------|------|-------------|---------|
| `label` | str | Texto de la etiqueta | `"Opción A"` |
| `name` | str | Nombre del grupo de radio buttons | `"grupo1"` |
| `checked` | bool | Estado de selección | `True`, `False` |

### Select

The `Select` component allows users to select one option from a group of options.

#### Syntax

```python
from dars.components.basic.select import Select

mi_select = Select(
    options=["Uno", "Dos", "Tres"],
    value="Dos",
    style={
        "width": "200px",
        "padding": "10px",
        "border": "1px solid #ccc"
    }
)
```

#### Properties

| Property | Type | Description | Values |
|-----------|------|-------------|---------|
| `options` | list | List of options | `["Uno", "Dos", "Tres"]` |
| `value` | str | Selected value | `"Dos"` |

### Slider

The `Slider` component allows users to select a value within a range.

#### Syntax

```python
from dars.components.basic.slider import Slider

mi_slider = Slider(
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

#### Properties

| Property | Type | Description | Values |
|-----------|------|-------------|---------|
| `min_value` | int | Minimum value | `0` |
| `max_value` | int | Maximum value | `100` |
| `value` | int | Valor selectado | `50` |
| `show_value` | bool | Mostrar el valor selectado | `True`, `False` |


### DatePicker

The `DatePicker` component allows users to select a date.

#### Syntax

```python
from dars.components.basic.date_picker import DatePicker

mi_date_picker = DatePicker(
    value="2025-08-06",
    style={
        "width": "200px",
        "padding": "10px",
        "border": "1px solid #ccc"
    }
)
```

#### Properties

| Property | Type | Description | Values |
|-----------|------|-------------|---------|
| `value` | str | Selected date | `"2025-08-06"` |

## Styling System

### Supported Style Properties

Dars supports most standard CSS properties:

#### Dimensions
- `width`, `height`
- `min-width`, `min-height`
- `max-width`, `max-height`

#### Spacing
- `margin`, `margin-top`, `margin-right`, `margin-bottom`, `margin-left`
- `padding`, `padding-top`, `padding-right`, `padding-bottom`, `padding-left`

#### Colors
- `background-color`
- `color`
- `border-color`

#### Typography
- `font-size`, `font-family`, `font-weight`, `font-style`
- `text-align`, `text-decoration`, `line-height`

#### Borders
- `border`, `border-width`, `border-style`, `border-radius`

#### Layout
- `display`, `position`
- `top`, `right`, `bottom`, `left`, `z-index`

#### Flexbox
- `flex-direction`, `flex-wrap`
- `justify-content`, `align-items`, `align-content`
- `flex`, `flex-grow`, `flex-shrink`, `flex-basis`

#### Grid
- `grid-template-columns`, `grid-template-rows`
- `grid-gap`, `grid-column`, `grid-row`

#### Effects
- `opacity`, `box-shadow`, `transform`, `transition`

### Advanced Style Examples

```python
# Gradiente de fondo
gradiente = Container(
    style={
        "background": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
        "min-height": "100vh",
        "display": "flex",
        "align-items": "center",
        "justify-content": "center"
    }
)

# Animación de hover (para web)
boton_animado = Button(
    text="Hover me",
    style={
        "background-color": "#3498db",
        "color": "white",
        "padding": "15px 30px",
        "border": "none",
        "border-radius": "8px",
        "transition": "all 0.3s ease",
        "transform": "translateY(0)",
        "box-shadow": "0 4px 15px rgba(52, 152, 219, 0.3)"
    }
)

# Layout de grid
grid_container = Container(
    style={
        "display": "grid",
        "grid-template-columns": "repeat(auto-fit, minmax(250px, 1fr))",
        "grid-gap": "20px",
        "padding": "20px"
    }
)

# Responsive design
responsive_container = Container(
    style={
        "width": "100%",
        "max-width": "1200px",
        "margin": "0 auto",
        "padding": "0 20px"
    }
)
```



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
BASE_BUTTON_STYLES = {
    "padding": "10px 20px",
    "border": "none",
    "border-radius": "4px",
    "font-size": "14px",
    "cursor": "pointer"
}

PRIMARY_BUTTON_STYLES = {
    **BASE_BUTTON_STYLES,
    "background-color": "#007bff",
    "color": "white"
}

SECONDARY_BUTTON_STYLES = {
    **BASE_BUTTON_STYLES,
    "background-color": "#6c757d",
    "color": "white"
}

# Use in components
cancel_button = Button("Cancelar", style=SECONDARY_BUTTON_STYLES)
save_button = Button("Guardar", style=PRIMARY_BUTTON_STYLES)
```

Components provide a solid foundation for creating modern and responsive user interfaces that can be exported to multiple platforms while maintaining consistency and functionality.

