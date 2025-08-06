# Quickstart

Welcome to Dars Framework! This guide will help you create your first web app in Python and export it to HTML/CSS/JS.

## Installation
```bash
pip install dars-framework
```

## Your First App
```python
from dars.core.app import App
from dars.components.basic.text import Text
from dars.components.basic.button import Button
from dars.components.basic.container import Container

app = App(title="My First App")
container = Container()
container.add_child(Text("Hello Dars!"))
container.add_child(Button("Click me"))
app.set_root(container)

if __name__ == "__main__":
    app.rTimeCompile()  # Quick preview
```

## Export the App
```bash
dars export my_app.py --format html --output ./my_app_web
```

## Preview
```bash
dars preview ./my_app_web
```

## Multipage Example
Define several pages using `Page`:
```python
from dars.components.basic import Page, Text, Button

home = Page(Text("Home"), Button("Go to About"))
about = Page(Text("About Us"))

app.add_page("home", root=home, index=True)
app.add_page("about", root=about)
```

---

See the rest of the documentation for more details on [components](components.md), [scripts](scripts.md), [exporters](exporters.md), and [examples](examples_basic.md).

Welcome to Dars Framework! This guide will help you create your first web app in Python and export it to HTML/CSS/JS.

## Installation
```bash
pip install dars-framework
```

## Your First App
```python
from dars.core.app import App
from dars.components.basic.text import Text
from dars.components.basic.button import Button
from dars.components.basic.container import Container

app = App(title="My First App")
container = Container()
container.add_child(Text("Hello Dars!"))
container.add_child(Button("Click me"))
app.set_root(container)

if __name__ == "__main__":
    app.rTimeCompile()  # Quick preview
```

## Export the App
```bash
dars export my_app.py --format html --output ./my_app_web
```

## Preview
```bash
dars preview ./my_app_web
```

## Multipage
Define several pages using `Page`:
```python
from dars.components.basic import Page, Text, Button

home = Page(Text("Home"), Button("Go to About"))
about = Page(Text("About Us"))

app.add_page("home", root=home, index=True)
app.add_page("about", root=about)
```

---

See the rest of the documentation for more details on components, scripts, exporters, and examples.
