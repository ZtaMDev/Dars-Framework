# Dars CLI Reference

The Dars Command Line Interface (CLI) lets you manage your projects, export apps, and preview results quickly from the terminal.

## How to Use the CLI

Open your terminal in your project directory and use any of the following commands:

```bash
# Show information about your app
 dars info my_app.py

# Export to different formats (web)
 dars export my_app.py --format html --output ./output
 # Skip default Python minifier for this run (does not affect viteMinify)
 dars export my_app.py --format html --output ./output --no-minify

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

## Main Commands Table
| Command                                 | What it does                               |
|-----------------------------------------|--------------------------------------------|
| `dars export my_app.py --format html`   | Export app to HTML/CSS/JS in `./my_app_web` |
| `dars export my_app.py --format html --no-minify` | Export skipping default Python minifier |
| `dars preview ./my_app_web`             | Preview exported app locally                |
| `dars build`                            | Build using dars.config.json                |
| `dars init --type desktop`              | Scaffold desktop-capable project (BETA)     |
| `dars build` (desktop config)           | Build desktop app artifacts (BETA)          |
| `dars build --no-minify`                | Build skipping default Python minifier      |
| `dars init my_project --type ssr`       | Create a new Full-Stack SSR project        |
| `dars init my_project`                  | Create a new Dars project (SPA Default)     |
| `dars info my_app.py`                   | Show info about your app                    |
| `dars formats`                          | List supported export formats               |
| `dars --help`                           | Show help and all CLI options               |

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
   dars export main.py --format html --output ./hello_output
   dars export main.py --format html --output ./dashboard_output
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

1.  **Backend (`python backend/api.py`)**: Runs on port 8000. Handles API requests and initial HTML rendering.
2.  **Frontend (`dars dev`)**: Runs on port 3000. Serves static assets, bundles scripts, and proxies to backend.

**Common Commands:**

| Command | Description |
|---------|-------------|
| `dars init --type ssr` | Scaffolds a project with `backend/` folder and SSR config. |
| `dars dev` | Starts the hot-reload frontend server (requires backend running). |
| `dars build` | Builds static assets to `dist/` for production. |

*Note: For production, you only need to run the backend (which serves the built assets).*