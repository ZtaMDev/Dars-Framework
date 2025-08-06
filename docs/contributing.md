# Contributing to Dars

Thank you for your interest in contributing to Dars Framework!

## How to Contribute
- Report bugs or request features via GitHub Issues
- Submit pull requests with improvements, fixes, or new components
- Improve the documentation

## Code Style
- Follow PEP8 for Python
- Document your components and functions
- Add usage examples

## Adding Components
```python
from dars.core.component import Component
class MyComponent(Component):
    pass
```

## Adding Exporters
```python
from dars.exporters.base import Exporter
class MyExporter(Exporter):
    def get_platform(self):
        return "my_platform"
    def export(self, app, output_path):
        # export logic
        return True
```

Thank you for your interest in contributing to Dars Framework!

## How to Contribute
- Report bugs or request features via GitHub Issues
- Submit pull requests with improvements, fixes, or new components
- Improve the documentation

## Code Style
- Follow PEP8 for Python
- Document your components and functions
- Add usage examples

## Adding Components
```python
from dars.core.component import Component
class MyComponent(Component):
    pass
```

## Adding Exporters
```python
from dars.exporters.base import Exporter
class MyExporter(Exporter):
    def get_platform(self):
        return "my_platform"
    def export(self, app, output_path):
        # export logic
        return True
```
