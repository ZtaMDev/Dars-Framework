# Dars Framework

Dars is a Python UI framework for building modern, interactive web apps with Python code. Write your interface in Python, export it to static HTML/CSS/JS, and deploy anywhere.

```bash
pip install dars-framework
```

> Some Javascript or frontend stack required.

Try dars without installing nothing just visit the [Dars Playground](https://dars-playground.vercel.app/)

## How It Works
- Build your UI using Python classes and components (like Text, Button, Container, Page, etc).
- Preview instantly with hot-reload using `app.rTimeCompile()`.
- Export your app to static web files with a single CLI command.
- Use multipage, layouts, scripts, and more—see docs for advanced features.
- For mor information visit the [Documentation](https://ztamdev.github.io/Dars-Framework/documentation.html)

## Quick Example: Your First App
> Note: this is an single page example but you can build multipage apps with Page component see the [Components Documentation](https://ztamdev.github.io/Dars-Framework/documentation.html#dars-components-documentation) to know more.

```python
from dars.all import *

app = App()

# Crear aplicación con sintaxis nueva (v1.0.3)
container = Container(
    Text(
        "Hola Dars",
        style={'font-size': '32px', 'color': '#333'}
    ),
    Button(
        "Hacer clic",
        style={'background-color': '#007bff', 'color': 'white'}
    ),
    style={
        'display': 'flex',
        'flex-direction': 'column',
        'align-items': 'center',
        'padding': '40px'
    }
)

# Script para interactividad
script = InlineScript("""
document.addEventListener('DOMContentLoaded', function() {
    const boton = document.querySelector('button');
    boton.addEventListener('click', function() {
        alert('Hola desde Dars.');
    });
});
""")

# Ensamblar aplicación
app.set_root(container)
app.add_script(script)

if __name__ == "__main__":
    app.rTimeCompile()  # Live preview at http://localhost:8000

```

## CLI Usage
| Command                                 | What it does                               |
|-----------------------------------------|--------------------------------------------|
| `dars export my_app.py --format html`   | Export app to HTML/CSS/JS in `./my_app_web` |
| `dars preview ./my_app_web`             | Preview exported app locally                |
| `dars init my_project`                  | Create a new Dars project                   |
| `dars info my_app.py`                   | Show info about your app                    |
| `dars formats`                          | List supported export formats               |
| `dars --help`                           | Show help and all CLI options               |

## More

- Visit dars [official website](https://ztamdev.github.io/Dars-Framework/)
- Visit the dars official [Documentation](https://ztamdev.github.io/Dars-Framework/documentation.html) now on separate website.
- Try dars without installing nothing just visit the [Dars Playground](https://dars-playground.vercel.app/)

## Local Execution and Live Preview

To test your app locally before exporting, use the hot-reload preview from any Python file that defines your app:

```python
if __name__ == "__main__":
    app.rTimeCompile()
```

Then run your file directly:

```bash
python my_app.py
```

This will start a local server at http://localhost:8000 so you can view your app in the browser—no manual export needed. You can change the port with:

```bash
python my_app.py --port 8088
```

---

You can also use the CLI preview command on an exported app:

```bash
dars preview ./my_exported_app
```

This will start a local server at http://localhost:8000 to view your exported app in the browser.

