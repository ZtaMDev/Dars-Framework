# Exporters

Dars supports exporting your apps to different platforms. The main focus is web (HTML/CSS/JS), but the architecture allows for new exporters.

## Web (HTML/CSS/JS)
- Generates files ready for static deploy
- Multipage support
- PWA Ready (manifest, icons, service worker)

### Export Example
```bash
dars export my_app.py --format html --output ./my_app_web
```

## Custom Exporters
You can create your own exporters by extending the `Exporter` class:

```python
from dars.exporters.base import Exporter
class MyExporter(Exporter):
    def get_platform(self):
        return "my_platform"
    def export(self, app, output_path):
        # export logic
        return True
```

For more details, see the [Architecture](architecture.md) and [CLI Reference](cli.md).

Dars supports exporting your apps to different platforms. The main focus is web (HTML/CSS/JS), but the architecture allows for new exporters.

## Web (HTML/CSS/JS)
- Generates files ready for static deploy
- Multipage support
- PWA Ready (manifest, icons, service worker)

## Export Example
```bash
dars export my_app.py --format html --output ./my_app_web
```

## Custom Exporters
You can create your own exporters by extending the `Exporter` class.

```python
from dars.exporters.base import Exporter
class MyExporter(Exporter):
    def get_platform(self):
        return "my_platform"
    def export(self, app, output_path):
        # export logic
        return True
```
