# Dars Framework Release Notes v1.0.5

## What's New

- **Modal Flicker-Free:** The Modal component is now exported as hidden by default (`hidden` attribute and `dars-modal-hidden` class) when `is_open=False`, eliminating any flicker on initial page load, even if CSS/JS loads slowly.
- **Robust Recursive Detection:** The exporter now recursively detects advanced components (Tabs, Accordion, Modal, Card) at any nesting level (including inside containers, panels, sections, or multipage apps) and applies `minimum_logic` robustly. Minimum JS is only injected if relevant components are present, even if deeply nested.
- **Barrel Import:** Import all main components and modules with a single line: `from dars.all import *` for easier integration.
- **New Advanced Modal Template:** A new advanced template `advanced/advanced_modal_demo` is now available. You can quickly scaffold a project with this template using the CLI:

  ```bash
  dars init myproject --template advanced/advanced_modal_demo
  ```
  This template demonstrates advanced modal usage, multi-page navigation, and integration of Cards, Tabs, and Accordions.
- **Stability Improvements:** Several minor bug fixes and stability enhancements.
- **Preview Ctrl+C Clean Shutdown:** The preview server (rTimeCompile) now shuts down cleanly on Ctrl+C using a shutdown_event, ensuring all resources and threads are properly closed on exit, even on Windows.

## Usage Example: Flicker-Free Modal

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

## Notes
- If you use custom JS logic, ensure you do not force `display:flex` unless appropriate.
- The `hidden` attribute is native to HTML and will be removed automatically when the modal should be shown.
- All recursive detection applies to multipage apps as well.
