# Dars CLI Reference

The Dars Command Line Interface (CLI) lets you manage your projects, export apps, and preview results quickly from the terminal.

## How to Use the CLI

Open your terminal in your project directory and use any of the following commands:

```bash
# Show information about your app
 dars info my_app.py

# Export to different formats
 dars export my_app.py --format html --output ./output

# List supported export formats
 dars formats

# Initialize a new project
 dars init my_new_project

# Initialize a project with a specific template
 dars init my_new_project -t demo/complete_app

# Preview an exported app
 dars preview ./output_directory

# Help
 dars --help
```

## Main Commands Table
| Command                                 | What it does                               |
|-----------------------------------------|--------------------------------------------|
| `dars export my_app.py --format html`   | Export app to HTML/CSS/JS in `./my_app_web` |
| `dars preview ./my_app_web`             | Preview exported app locally                |
| `dars init my_project`                  | Create a new Dars project                   |
| `dars info my_app.py`                   | Show info about your app                    |
| `dars formats`                          | List supported export formats               |
| `dars --help`                           | Show help and all CLI options               |

## Using Official Templates

Dars provides official templates to help you start new projects quickly. Templates include ready-to-use apps for forms, layouts, dashboards, multipage, and more.

### How to Use a Template

1. **Initialize a new project with a template:**
   ```bash
   dars init my_new_project -t basic/hello_world
   dars init my_new_project -t basic/simple_form
   dars init my_new_project -t advanced/dashboard
   dars init my_new_project -t demo/complete_app
   # ...and more (see below)
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

### Available Templates
- [Hello World](template_hello_world.md)
- [Simple Form](template_simple_form.md)
- [Form Components](template_form_components.md)
- [Flex Layout Responsive](template_flex_layout_responsive.md)
- [Grid Layout Responsive](template_grid_layout_responsive.md)
- [Multipage Example](template_multipage_example.md)
- [Layout Multipage Demo](template_layout_multipage_demo.md)
- [PWA Custom Icons](template_pwa_custom_icons.md)
- [All Components Demo](template_all_components_demo.md)
- [Dashboard](template_dashboard.md)
- [Modern Web App](template_modern_web_app.md)
- [Complete App](template_complete_app.md)

Each template has its own documentation file with a brief description and usage notes.

## Tips
- Use `dars --help` for a full list of commands and options.
- You can preview apps either live (with `app.rTimeCompile()`) or from exported files with `dars preview`.
- Templates are available for quick project setup: use `dars init my_project -t <template>`.

For more, see the [Getting Started](getting_started.md) guide and the main documentation index.
