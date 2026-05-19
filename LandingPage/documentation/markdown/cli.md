# Dars CLI Reference

The Dars Command Line Interface (CLI) lets you manage your projects, export apps, and preview results quickly from the terminal.

## How to Use the CLI

Open your terminal in your project directory and use any of the following commands:

```bash
# Show information about your app
 dars info my_app.py

# List supported export formats
 dars formats

# Initialize a new project (Default is SPA)
 dars init my_new_project

# Initialize a Full-Stack SSR project
 dars init my_new_project --type ssr

# Initialize a project with a specific template
 dars init my_new_project -t demo/complete_app

# Preview an exported app
 dars preview ./output_directory
 # New in v1.9.6: Path is optional (defaults to config outdir or ./dist)
 dars preview
 # New in v1.9.6: Custom port support
 dars preview -p 9000

# Build using project config (dars.config.json)
 dars build
 # Build desktop (BETA) when format is desktop in config
 dars build
 # Build without the default Python minifier
 dars build --no-minify

# Help
 dars --help

# Version
 dars -v
```

## Code Generation (New in v1.9.6)

Scaffold new components and pages instantly with automatic project integration.

```bash
# Generate a new FunctionComponent
 dars generate component MyComponent
 dars g component MyComponent

# Generate a new Page
 dars generate page About
 # Specify page type directly
 dars generate page About --page-type spa
 dars generate page Home --page-type static
 dars generate page Profile --page-type ssr

# Generate with auto-injection to main.py
 dars generate page Contact -y
```

## Main Commands Table

| Command                                           | What it does                                                      |
| ------------------------------------------------- | ----------------------------------------------------------------- |
| `dars export my_app.py --format html`             | Export app to HTML/CSS/JS in `./my_app_web`                       |
| `dars export my_app.py --format html --no-minify` | Export skipping default Python minifier                           |
| `dars preview`                                    | Preview exported app (auto-detects output)                        |
| `dars preview --port 9000`                        | Preview on a custom port                                          |
| `dars build`                                      | Build using dars.config.json                                      |
| `dars init --type desktop`                        | Scaffold desktop-capable project (BETA)                           |
| `dars build` (desktop config)                     | Build desktop app artifacts (BETA)                                |
| `dars build --no-minify`                          | Build skipping default Python minifier                            |
| `dars init my_project --type ssr`                 | Create a new Full-Stack SSR project                               |
| `dars init my_project`                            | Create a new Dars project (SPA Default)                           |
| `dars dev`                                        | Run the configured entry file with hot preview (app.rTimeCompile) |
| `dars dev --port 9000`                            | Run the dev server on a custom port                               |
| `dars dev --backend`                              | Run only the configured backendEntry (FastAPI/SSR backend)        |
| `dars info my_app.py`                             | Show info about your app                                          |
| `dars formats`                                    | List supported export formats                                     |
| `dars generate component <name>`                  | Scaffold a new FunctionComponent                                  |
| `dars generate page <name>`                       | Scaffold a new page (static or SPA)                               |
| `dars generate page <name> -y`                    | Scaffold and auto-inject into main app                            |
| `dars --help`                                     | Show help and all CLI options                                     |

## Using Official Templates

Dars provides official templates to help you start new projects quickly. Templates include ready-to-use apps for forms, layouts, dashboards, multipage, and more.

### How to Use a Template

1. **Initialize a new project with a template:**
   ```bash
   dars init my_new_project -t basic/HelloWorld
   # ...and more (see below)
   ```

You can see the templates available with

```bash
dars init --list-templates
dars init  -L
```

2. **Export the template to HTML/CSS/JS:**
   ```bash
   dars export {file.py} --format html --output ./hello_output
   dars export {file.py} --format html --output ./dashboard_output
   # ...etc
   ```
3. **Preview the exported app:**
   ```bash
   dars preview ./hello_output
   ```

## Tips CLI

- Use `dars --help` for a full list of commands and options.
- You can preview apps either live (with `app.rTimeCompile()`) or from exported files with `dars preview`.
- Templates are available for quick project setup: use `dars init my_project -t <template>`.

### Desktop (BETA) CLI

- Mark your project with `"format": "desktop"` in `dars.config.json`.
- Use `dars init --type desktop` (or `--update`) to scaffold backend files.
- Run `dars doctor --all --yes` to set up optional tooling.
- Build with `dars build`. This feature is in BETA: suitable for testing, not yet for production.

### Minification labels in output

- Applying minification (default): default Python-side minifier is active.
- Applying minification (vite): Vite/esbuild minification is active (JS/CSS) and default is disabled.
- Applying minification (default + vite): both are active.

For more, see the [Getting Started](#getting-started-with-dars) guide and the main documentation index.

### SSR Workflow (Full-Stack)

When working with SSR (`dars init --type ssr`), the workflow involves two processes:

1.  **Frontend (`dars dev`)**: Runs the Dars preview server on port `8000` (or the one set in `dars.config.json`) using `app.rTimeCompile()`.
2.  **Backend (`dars dev --backend`)**: Runs the FastAPI SSR backend on port `3000` using `backendEntry` from `dars.config.json`.

**Common Commands:**

| Command                | Description                                                |
| ---------------------- | ---------------------------------------------------------- |
| `dars init --type ssr` | Scaffolds a project with `backend/` folder and SSR config. |
| `dars dev`             | Starts the hot-reload frontend preview server.             |
| `dars dev --backend`   | Starts the SSR/backend server defined by `backendEntry`.   |
| `dars build`           | Builds static assets to `dist/` for production.            |

\_Note: For production, you only need to run the backend (which serves the built assets).
