# Dars - Components Documentation

---

## Barrel Import

You can import all main components and modules with a single line:

```python
from dars.all import *
```

This simplifies integration and improves developer experience by exposing components like `Text`, `Button`, `Container`, `State`, and DAP functions like `log`, `alert`, `showModal`, etc.

> **Note**: Be careful if you create custom components with the same names as built-in components to avoid conflicts.

---

## Introduction to Components

Components are the fundamental UI elements in Dars. Each component encapsulates its appearance, behavior, and state.
In modern Dars, you should heavily rely on **Utility Classes** (Tailwind-like classes) using the `class_name` property instead of the old `style` dictionary, and use **DAP Functions** (`show()`, `hide()`, `log()`, `alert()`, `updateVRef()`) instead of writing raw inline JavaScript for events.

For custom components, refer to [Custom Components](#custom-components).

---

## Base Component Class

All UI elements inherit from the `Component` base class, which provides standard attributes and DOM manipulation methods.

### Global Properties

- **id**: Unique identifier for the component.
- **class_name**: String containing CSS utility classes (e.g., `"flex flex-col bg-slate-100 p-4 rounded-lg"`).
- **style**: Optional dictionary or string for direct inline styles (prefer `class_name`).
- **children**: List of child components.
- **Events**: Handlers like `on_click`, `on_change`, `on_mouse_enter`, etc. Accept DAP utility functions or state setters.

---

## Core Components

### Container

The `Container` acts as a generic `<div>` to group components.

```python
from dars.all import *

layout = Container(
    Text("Welcome to Dars", style="text-4xl font-black text-slate-900 mb-4"),
    Button("Get Started", style="bg-indigo-600 text-white px-6 py-3 rounded-xl shadow-lg hover:bg-indigo-700 transition-all scale-105 active:scale-95"),
    style="flex flex-col items-center justify-center min-h-screen bg-slate-50"
)
```

### Section

Similar to `Container`, but renders as a semantic `<section>` HTML tag.

```python
main_section = Section(
    Text("About Us", style="text-xl font-semibold"),
    style="p-8 border-t border-slate-200"
)
```

### Text

Displays static or reactive text.

```python
title = Text(
    "Dars Framework",
    style="text-6xl font-black text-transparent bg-clip-text bg-gradient-to-r from-indigo-500 via-purple-500 to-pink-500"
)

# Reactive text using useDynamic
user_name = Text(useDynamic("user.name"), style="text-lg font-medium")
```

---

## Interactive Components

### Button

Creates interactive clickable buttons. Use DAP functions for events instead of inline JavaScript.

```python
submit_btn = Button(
    "Save Changes",
    style="bg-emerald-500 text-white font-semibold py-3 px-6 rounded-lg transition-all hover:bg-emerald-600 hover:shadow-xl active:scale-95",
    on_click=log("Changes saved successfully!")
)
```

### Input

Allows text or numeric user input.

```python
email_input = Input(
    placeholder="Enter your email",
    input_type="email",
    required=True,
    style="w-full p-3 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500",
    on_change=log("Email updated")
)
```

### Checkbox & RadioButton

For boolean selections or single-choice groups.

```python
terms = Checkbox(
    label="I accept the terms",
    checked=False,
    style="accent-blue-500"
)

theme_radio = RadioButton(
    label="Dark Mode",
    name="theme_group",
    checked=True
)
```

### Select

Dropdown menu for options.

```python
dropdown = Select(
    options=["Option 1", "Option 2", "Option 3"],
    value="Option 1",
    style="p-2 border rounded bg-white text-slate-700"
)
```

### Textarea

For multi-line inputs.

```python
comment = Textarea(
    placeholder="Write your comment...",
    rows=4,
    style="w-full p-2 border border-slate-300 rounded resize-y"
)
```

### Slider

Range selection slider.

```python
volume = Slider(
    min_value=0, max_value=100, value=50,
    style="w-[200px] accent-blue-500"
)
```

### FileUpload

```python
upload = FileUpload(
    label="Upload Document",
    accept=".pdf",
    style="cursor-pointer bg-slate-100 p-2 rounded border-dashed border-2"
)
```

### DatePicker

```python
date = DatePicker(value="2025-01-01", style="p-2 rounded border")
```

---

## Visual & Media Components

### Image

```python
logo = Image(
    src="/assets/logo.png",
    alt="Logo",
    style="w-[120px] h-auto object-contain drop-shadow-md"
)
```

### Video & Audio

Wrappers over HTML5 media tags with reactivity support.

```python
video_player = Video(
    src="/media/promo.mp4",
    controls=True,
    autoplay=False,
    style="w-full rounded-xl shadow-lg"
)

audio_player = Audio(
    src="/media/soundtrack.mp3",
    controls=True
)
```

### Link

```python
nav_link = Link(
    "Go to Dashboard",
    href="/dashboard",
    style="text-blue-500 hover:text-blue-700 underline"
)
```

---

## Advanced UI Components

### Card

A structured container for displaying related info.

```python
user_card = Card(
    title="Profile Info",
    children=[Text("Username: ZtaDev"), Button("Edit")],
    style="bg-white rounded-xl shadow-md p-6 max-w-sm border border-slate-100"
)
```

### Modal

An overlay dialog. Modals are hidden by default to prevent flicker on load. Use `showModal()` and `hideModal()` DAP utilities to control them.

```python
from dars.all import *

info_modal = Modal(
    id="info-modal",
    title="Information",
    is_open=False,
    children=[Text("Here are some details.")],
    style="bg-white rounded-lg p-6 w-[400px]",
    overlay_class="bg-black/50 backdrop-blur-sm"
)

# Open modal using the utility function
open_btn = Button("Show Info", on_click=showModal("info-modal"))
```

### Navbar

Top navigation bar structure.

```python
nav = Navbar(
    brand=Text("MyApp", style="text-xl font-bold"),
    children=[Link("Home", "/"), Link("Settings", "/settings")],
    style="flex justify-between items-center bg-slate-900 text-white p-4 sticky top-0 z-50"
)
```

### Accordion & Tabs

For collapsing content or switching between views.

```python
faq = Accordion(
    items=[
        {"title": "What is Dars?", "content": "A reactive Python web framework."},
        {"title": "Is it fast?", "content": "Yes!"}
    ],
    style="border rounded"
)

dashboard_tabs = Tabs(
    tabs=[
        {"label": "Overview", "content": Text("Overview data")},
        {"label": "Metrics", "content": Text("Metrics data")}
    ]
)
```

### Markdown

Renders Markdown as HTML. Built-in support for highlight.js code highlighting.

```python
doc = Markdown(
    content="## Hello\nThis is **Markdown**",
    style="prose prose-slate max-w-none p-4"
)
```

### ProgressBar & Tooltip

```python
prog = ProgressBar(value=75, max_value=100, style="w-full h-2 bg-slate-200 rounded-full [&::-webkit-progress-value]:bg-blue-500")

tip = Tooltip(text="Click to save", child=Button("Save"))
```

---

## Data Visualization

### DataTable

Render tabular data from lists or Pandas DataFrames.

```python
data = [
    {'Name': 'Alice', 'Role': 'Admin'},
    {'Name': 'Bob', 'Role': 'User'}
]
table = DataTable(data, striped=True, hover=True, theme="light", style="w-full text-left")
```

### Chart

Renders Plotly.js charts.

```python
import plotly.graph_objects as go
fig = go.Figure(data=[go.Bar(x=['A', 'B'], y=[10, 20])])

chart = Chart(figure=fig, style="w-full h-[400px]")
```

---

## Layout Components

While you can use `Container` with CSS classes (`style="flex gap-4"`), Dars provides dedicated layout components for convenience.

### FlexLayout

```python
row = FlexLayout(
    direction="row",
    justify="space-between",
    align="center",
    gap="16px",
    children=[Button("Cancel"), Button("Confirm")],
    style="w-full p-4"
)
```

### GridLayout

```python
grid = GridLayout(
    rows=2, cols=2, gap="24px",
    children=[Text("1"), Text("2"), Text("3"), Text("4")],
    style="w-full max-w-4xl mx-auto"
)
```

---

## Dynamic Creation & Lifecycle

Dars allows you to create and delete components dynamically at runtime, with full support for lifecycle hooks.

### Runtime Component Manipulation

```python
from dars.all import *

# Component to be generated
msg = Text("Dynamic Message", id="msg", style="text-emerald-600 font-medium")

# Creates the component inside the container with ID 'root'
create_btn = Button("Add Message", on_click=createComp(msg, root="root", position="append"))

# Deletes the component with ID 'msg'
delete_btn = Button("Remove Message", on_click=deleteComp("msg"))
```

### Lifecycle Hooks (onMount, onUpdate, onUnmount)

Components can trigger DAP operations or callbacks when they are created, updated, or destroyed.

```python
dynamic_box = Container(
    id="dyn_box",
    class_name="p-4 border rounded",
    onMount=log("dyn_box was added to DOM"),
    onUpdate=log("dyn_box was updated"),
    onUnmount=log("dyn_box was removed from DOM")
)
```

- **onMount**: Runs once when the component is inserted into the DOM.
- **onUpdate**: Runs after dynamic updates (e.g., via `updateComp` or reactive `V()` updates).
- **onUnmount**: Runs right before the component is deleted from the DOM.
