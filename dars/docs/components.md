# Dars - Components Documentation

## Introduction to Components

Components are the fundamental elements of Dars that represent UI elements. Each component encapsulates its appearance, behavior, and state, allowing you to create complex interfaces by composing simple elements.

---

### Quick Access

- [Base Component Class](#base-component-class)
- [Page](#Page)
- [Text](#Text)
- [Button](#Button)
- [Input](#Input)
- [Container](#Container)
- [Image](#Image)
- [Link](#Link)
- [Textarea](#Textarea)
- [Checkbox](#Checkbox)
- [RadioButton](#RadioButton)
- [Select](#Select)
- [Slider](#Slider)
- [ProgressBar](#ProgressBar)
- [Tooltip](#Tooltip)
- [DatePicker](#DatePicker)
- [Card](#Card)
- [Modal](#Modal)
- [Navbar](#Navbar)
- [Accordion](#Accordion)
- [Tabs](#Tabs)
- [Table](#Table)
- [Layout Components](#layout-components)
  - [GridLayout](#GridLayout)
  - [FlexLayout](#FlexLayout)
  - [LayoutBase](#LayoutBase)
  - [AnchorPoint](#AnchorPoint)

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
    # on_click=my_function, # Los eventos se manejan con app.add_script o InlineScript
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
    # on_change=my_function_cambio, # Los eventos se manejan con app.add_script o InlineScript
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

The `Container` component is a container that can hold other components.

#### Syntax

```python
from dars.components.basic.container import Container

container = Container(
    children=[componente1, componente2],
    style={
        "display": "flex",
        "flex-direction": "column",
        "padding": "20px",
        "background-color": "#f8f9fa"
    }
)

# O agregar hijos después
container.add_child(componente3)
```

#### Properties

| Property | Type | Description |
|-----------|------|-------------|
| `children` | list | List of child components |

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

#### Syntax

```python
from dars.components.advanced.modal import Modal
from dars.components.basic.text import Text
from dars.components.basic.button import Button

my_modal = Modal(
    title="Bienvenido al Modal",
    is_open=True, # O False para que esté oculto inicialmente
    children=[
        Text("Este es el contenido de tu ventana modal."),
        Button("Cerrar")
    ],
    class_name="welcome-modal",
    style={
        "background-color": "rgba(0, 0, 0, 0.7)" # Estilo para el overlay
    }
)
```

#### Properties

| Property | Type | Description |
|-----------|------|-------------|
| `title` | str | Modal title |
| `is_open` | bool | Controls modal visibility (`True` to show, `False` to hide) |
| `children` | list | List of child components |

#### Example

```python
my_modal = Modal(
    title="Bienvenido al Modal",
    is_open=True, # O False para que esté oculto inicialmente
    children=[
        Text("Este es el contenido de tu ventana modal."),
        Button("Cerrar")
    ],
    class_name="welcome-modal",
    style={
        "background-color": "rgba(0, 0, 0, 0.7)" # Estilo para el overlay
    }
)
```

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

## Events and Interactivity

Components can respond to user events. To handle events, you can use `InlineScript` or `ExternalScript` to add JavaScript logic that interacts with the generated HTML elements. Each component has a unique `id` that you can use to select it in JavaScript.

```python
from dars.core.app import App
from dars.components.basic.button import Button
from dars.components.basic.text import Text
from dars.scripts.script import InlineScript

app = App(title="App con Eventos")

# Crear un componente de text para mostrar mensajes
message_text = Text("Esperando interacción...", id="status-message")

# Crear un botón
my_button = Button("Haz clic aquí", id="my-button")

# Añadir un script inline para manejar el evento en el frontend
frontend_script = InlineScript("""
document.getElementById("my-button").addEventListener("click", function() {
    alert("¡Evento de click detectado en el navegador!");
    document.getElementById("status-message").innerText = "¡Botón clickeado!";
});
""")

app.set_root(my_button) # Or a container that contains both
app.add_child(message_text) # Assuming App has an add_child method or similar for components outside the root
app.add_script(frontend_script)
```

**Common Event Types:**

Dars supports a variety of standard browser events, such as:

*   **Mouse Events**: `click`, `dblclick`, `mousedown`, `mouseup`, `mouseenter`, `mouseleave`, `mousemove`.
*   **Keyboard Events**: `keydown`, `keyup`, `keypress`.
*   **Form Events**: `change`, `input`, `submit`, `focus`, `blur`.
*   **Other**: `load`, `error`, `resize`.

You can also define custom events.

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


