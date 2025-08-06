# Scripts System

Dars allows you to add JavaScript scripts to your app for advanced interactivity and custom logic.

## Script Types
- **InlineScript**: Embed JS code directly as a Python string
- **FileScript**: Reference an external JS file

## Adding Scripts

You can add scripts globally (to the whole app) or to specific pages:

```python
from dars.scripts.script import InlineScript
from dars.components.basic import Page, Text

# Global script (included on all pages)
app.add_script(InlineScript("console.log('Hello from Dars');"))

# Script for a single page
page = Page(Text("Demo"))
page.add_script(InlineScript("alert('Page loaded');"))
```

- **Global scripts** are included on every page of your app.
- **Page scripts** are only included on the specific page.

For more, see [Components Reference](components.md) and [Exporter Guide](exporters.md).

You can add scripts to your app for advanced interactivity.

## Script Types
- **InlineScript**: Embedded JS code (as a Python string)
- **FileScript**: Reference to an external JS file

## Global and Per-Page Usage
```python
from dars.scripts.script import InlineScript
app.add_script(InlineScript("console.log('Hello from Dars');"))

# Script for a single page
page = Page(Text("Demo"))
page.add_script(InlineScript("alert('Page loaded');"))
```

Global scripts are included on all pages. Page scripts only on that page.
