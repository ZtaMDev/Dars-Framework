<h1 align="center">Dars Framework</h1>
 
<p align="center">
  <img src="./Dars-logo.png" alt="Dars Framework Logo" width="200" />
</p>

<p align="center">
  <em>Dars is a Python UI framework for building modern, interactive web apps with Python code. Write your interface in Python, export it to static HTML/CSS/JS, and deploy anywhere.</em>
  <br/>
  <em><strong>New (BETA):</strong> Export to native desktop apps. This capability is in BETA and not yet recommended for production.</em>
</p>

```bash
pip install dars-framework
```

> Some Javascript or frontend stack required. 

Try dars without installing nothing just visit the [Dars Playground](https://dars-playground.vercel.app/)

## How It Works
- Build your UI using Python classes and components (like Text, Button, Container, Page, etc).
- Preview instantly with hot-reload using `app.rTimeCompile()`.
- Export your app to static web files with a single CLI command.
- Export to native desktop apps (BETA) using project config `format: "desktop"` and `dars build`.
- Use multipage, layouts, scripts, and more—see docs for advanced features.
- For more information visit the [Documentation](https://ztamdev.github.io/Dars-Framework/docs.html)

## Quick Example: Your First App
```python
from dars.all import *

app = App(title="Hello World", theme="dark")
# Crear componentes
index = Page(
     Text(
        text="Hello World",
        style={
            'font-size': '48px',
            'color': '#2c3e50',
            'margin-bottom': '20px',
            'font-weight': 'bold',
            'text-align': 'center'
        }
    ),
    Text(
        text="Hello World",
        style={
            'font-size': '20px',
            'color': '#7f8c8d',
            'margin-bottom': '40px',
            'text-align': 'center'
        }
    ),

    Button(
        text="Click Me!",
        on_click= dScript("alert('Hello World')"),
        on_mouse_enter=dScript("this.style.backgroundColor = '#2980b9';"),
        on_mouse_leave=dScript("this.style.backgroundColor = '#3498db';"),
        style={
            'background-color': '#3498db',
            'color': 'white',
            'padding': '15px 30px',
            'border': 'none',
            'border-radius': '8px',
            'font-size': '18px',
            'cursor': 'pointer',
            'transition': 'background-color 0.3s'
        }
    ),
    style={
        'display': 'flex',
        'flex-direction': 'column',
        'align-items': 'center',
        'justify-content': 'center',
        'min-height': '100vh',
        'background-color': '#f0f2f5',
        'font-family': 'Arial, sans-serif'
    }
) 
index.attr()
app.add_page("index", index, title="Hello World", index=True)

if __name__ == "__main__":
    app.rTimeCompile()

```

---

## Reactivity and State System

**Dars Framework** includes a built-in **reactive state system** (`dState` / `cState`) that allows dynamic and modular DOM updates directly from Python.
It enables fully event-driven interfaces without requiring manual JavaScript.

### Key Concepts

* **`dState(name, component, states)`**
  Creates a reactive state controller bound to a specific component and a list of possible states.

* **`cState(idx, mods=[...])`**
  Defines rules (modifications) that are automatically applied when entering a specific state.

* **`Mod` Helpers**
  A compact way to modify DOM elements on state changes: `inc`, `dec`, `set`, `toggle_class`, `append_text`, `prepend_text`, `goto`, and more.

* **Deferred Mutations**
  Using `component.attr(..., defer=True)` or `component.mod(...)` inside a `cComp=True` state defers HTML updates until an event occurs, preventing authoring-time mutations.

### Example Template

A complete example demonstrating `dState`, `cState`, `Mod`, and deferred updates is available [here](https://github.com/ZtaMDev/Dars-Framework/blob/CrystalMain/dars/templates/examples/advanced/dState/state_mods_demo.py)

<img width="384" height="187" alt="imagen" src="https://github.com/user-attachments/assets/7750ee7f-768f-48da-94df-2fa00339a99c" /> <img width="361" height="215" alt="imagen" src="https://github.com/user-attachments/assets/9b8a3e67-2424-49b4-aee0-9f1c0f747d66" />



### Features

* Reactive Mod system with compact `Mod` helpers
* Unified event model — any component can use `on_*` props (`on_click`, `on_input`, `on_change`, etc.)
* Deferred rendering for safer, predictable state transitions (`cComp=True`)
* Navigation between states using `goto`, including relative moves (`'+1'`, `'-1'`)
* Consistent, event-time mutation flow for reliable behavior
* Secure minification for production bundles (strong JS/CSS minifier integrated into the build pipeline)

---

## CLI Usage
| Command                                 | What it does                               |
|-----------------------------------------|--------------------------------------------|
| `dars export my_app.py --format html`   | Export app to HTML/CSS/JS in `./my_app_web` |
| `dars init --type desktop`               | Scaffold desktop-capable project (BETA)     |
| `dars build` (desktop config)            | Build desktop app artifacts (BETA)          |
| `dars preview ./my_app_web`             | Preview exported app locally                |
| `dars init my_project`                  | Create a new Dars project (also creates dars.config.json) |
| `dars init --update`                    | Create/Update dars.config.json in current dir |
| `dars build`                            | Build using dars.config.json (entry/outdir/format) |
| `dars config validate`                  | Validate dars.config.json and print report   |
| `dars info my_app.py`                   | Show info about your app                    |
| `dars formats`                          | List supported export formats               |
| `dars --help`                           | Show help and all CLI options               |

Tip: use `dars doctor` to review optional tooling that can enhance bundling/minification.

### Desktop Export (BETA)

- Mark your project for desktop in `dars.config.json` with `"format": "desktop"`.
- Initialize backend scaffolding with `dars init --type desktop` (or `--update`).
- Build with `dars build` to produce desktop artifacts under `dist/`.
- This feature is in BETA: usable for testing, not yet recommended for production.

## More

- Visit dars [official website](https://ztamdev.github.io/Dars-Framework/)
- Visit the dars official [Documentation](https://ztamdev.github.io/Dars-Framework/docs.html) now on separate website.
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

---

## Project Configuration (dars.config.json)

Dars can read build/export settings from a `dars.config.json` at your project root. It is created automatically by `dars init`, and you can add it to existing projects with `dars init --update`.

Example default:

```json
{
  "entry": "main.py",
  "format": "html",
  "outdir": "dist",
  "publicDir": null,
  "include": [],
  "exclude": ["**/__pycache__", ".git", ".venv", "node_modules"],
  "bundle": true,
  "defaultMinify": true,
  "viteMinify": true
}
```

- `entry`: Python entry file. Used by `dars build` and `dars export config`.
- `format`: Export format. Currently only `html` is supported.
- `outdir`: Output directory. Used by `dars build` and default for `dars export` when not overridden.
- `publicDir`: Folder (e.g., `public/` or `assets/`) copied into the output. If null, it is autodetected.
- `include`/`exclude`: Basic filters for copying from `publicDir`.
- `bundle`: Reserved for future use. CLI exports and build already bundle appropriately.
- `defaultMinify`: Toggle the built-in Python minifier (safe, conservatively preserves `<pre>`, `<code>`, `script`, `style`, `textarea`). Controls HTML minification and provides JS/CSS fallback when advanced tools are unavailable. Default `true`.
- `viteMinify`: Toggle the Vite/esbuild minifier for JS/CSS. Default `true`.

Validate your config:

```bash
dars config validate
```

Build using config:

```bash
dars build
```

Export using the config entry and outdir:

```bash
dars export config --format html
```

---

See LandingPage docs for details: state_management.md, events.md, scripts.md.

## More

- Visit dars [official website](https://ztamdev.github.io/Dars-Framework/)
- Visit the dars official [Documentation](https://ztamdev.github.io/Dars-Framework/docs.html) now on separate website.
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
