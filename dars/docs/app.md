# App Class and PWA Features in Dars Framework

## Overview

The `App` class is the core of any Dars Framework application. It represents the complete application and manages all configuration, components, pages, and functionalities, including Progressive Web App (PWA) support.

## Basic Structure

```python
class App:
    def __init__(
        self, 
        title: str = "Dars App",
        description: str = "",
        author: str = "",
        keywords: List[str] = None,
        language: str = "en",
        favicon: str = "",
        icon: str = "",
        apple_touch_icon: str = "",
        manifest: str = "",
        theme_color: str = "#000000",
        background_color: str = "#ffffff",
        service_worker_path: str = "",
        service_worker_enabled: bool = False,
        **config
    ):
```

## Global Styles Management

### Enhanced add_global_style() Method

The `App` class now includes an enhanced `add_global_style()` method that supports both inline style definitions and external CSS file imports.


#### Usage Examples

**1. Inline Style Definition (Traditional)**
```python
app.add_global_style(
    selector=".my-button",
    styles={
        "background-color": "#4CAF50",
        "color": "white",
        "padding": "10px 20px",
        "border-radius": "5px"
    }
)
```

**2. External CSS File Import (New in v1.1.2)**
```python
app.add_global_style(file_path="styles.css")
```

**3. Combined Usage**
```python
# Add inline styles
app.add_global_style(
    selector=".primary-btn",
    styles={
        "background-color": "#007bff",
        "color": "white"
    }
)

# Import external CSS file
app.add_global_style(file_path="components.css")
```

#### Practical Example with External CSS

**main.py:**
```python
from dars.all import *

app = App(title="Dars Styling Test")

index = Page(
    Container(
        Button("Styled Button", class_name="button-styling-test"),
        id="page_sub_container"
    )
)

app.add_page(name="index", root=index, title="index", index=True)
app.add_global_style(file_path="styles.css")

if __name__ == "__main__":
    app.rTimeCompile(add_file_types=".py, .css")
```

**styles.css:**
```css
.button-styling-test {
    background-color: rgb(51, 255, 0);
    padding: 15px 30px;
    border-radius: 8px;
    border: none;
    font-weight: bold;
    cursor: pointer;
}

.button-styling-test:hover {
    background-color: rgb(30, 200, 0);
    transform: scale(1.05);
}

#page_sub_container {
    padding: 20px;
    background-color: #f5f5f5;
    min-height: 100vh;
}
```

### Hot Reload for CSS Files

When using `app.rTimeCompile()` with the `add_file_types=".css"` parameter, the development server automatically watches for changes in CSS files and reloads the application when modifications are detected.

```python
# Watch for both Python and CSS file changes
app.rTimeCompile(add_file_types=".py, .css")

# Or watch for CSS files only
app.rTimeCompile(add_file_types=".css")
```

### Benefits of External CSS Import

1. **Separation of Concerns**: Keep styles separate from application logic
2. **Better Organization**: Maintain complex stylesheets in dedicated files
3. **Team Collaboration**: Designers and developers can work simultaneously
4. **CSS Preprocessors**: Use SASS, LESS, or other preprocessors
5. **Performance**: Browser caching for external CSS files

### Backward Compatibility

The enhanced method maintains full backward compatibility - existing code using `add_global_style(selector, styles)` will continue to work without modification.


## PWA Configuration Properties

The App class includes these PWA-specific properties:

```python
# Icons and visual resources
self.favicon = favicon  # Path to traditional favicon
self.icon = icon  # Main icon for PWA (multiple sizes)
self.apple_touch_icon = apple_touch_icon  # Icon for Apple devices
self.manifest = manifest  # Path to manifest.json file

# Colors and theme
self.theme_color = theme_color  # Theme color (#RRGGBB)
self.background_color = background_color  # Background color for splash screens

# Service Worker
self.service_worker_path = service_worker_path  # Path to service worker file
self.service_worker_enabled = service_worker_enabled  # Enable/disable

# Additional PWA configuration
self.pwa_enabled = config.get('pwa_enabled', False)
self.pwa_name = config.get('pwa_name', title)
self.pwa_short_name = config.get('pwa_short_name', title[:12])
self.pwa_display = config.get('pwa_display', 'standalone')
self.pwa_orientation = config.get('pwa_orientation', 'portrait')
```

## Meta Tag Generation for PWA

The App class provides methods to generate PWA meta tags:

```python
def get_meta_tags(self) -> Dict[str, str]:
    """Returns all meta tags as a dictionary"""
    meta_tags = {}
    
    # Viewport configured for responsiveness
    viewport_parts = []
    for key, value in self.config['viewport'].items():
        if key == 'initial_scale':
            viewport_parts.append(f'initial-scale={value}')
        elif key == 'user_scalable':
            viewport_parts.append(f'user-scalable={value}')
        else:
            viewport_parts.append(f'{key.replace("_", "-")}={value}')
    meta_tags['viewport'] = ', '.join(viewport_parts)
    
    # Specific tags for PWA
    meta_tags['theme-color'] = self.theme_color
    if self.pwa_enabled:
        meta_tags['mobile-web-app-capable'] = 'yes'
        meta_tags['apple-mobile-web-app-capable'] = 'yes'
        meta_tags['apple-mobile-web-app-status-bar-style'] = 'default'
        meta_tags['apple-mobile-web-app-title'] = self.pwa_short_name
    
    return meta_tags
```

## Integration with HTML/CSS/JS Exporter

The `HTMLCSSJSExporter` uses the PWA configuration from the App class to generate:

1. **manifest.json file** - Progressive web app configuration
2. **Meta tags** - To indicate PWA capabilities in different browsers
3. **Icon references** - For multiple devices and sizes
4. **Service Worker registration** - For offline functionality

### Example of Generated Manifest.json

```json
{
  "name": "App Name",
  "short_name": "Short Name",
  "description": "Application description",
  "start_url": "/",
  "display": "standalone",
  "background_color": "#ffffff",
  "theme_color": "#000000",
  "orientation": "portrait",
  "icons": [
    {
      "src": "icon-192x192.png",
      "sizes": "192x192",
      "type": "image/png"
    },
    {
      "src": "icon-512x512.png",
      "sizes": "512x512",
      "type": "image/png"
    }
  ]
}
```

### Service Worker Registration Script

The exporter automatically generates code to register the service worker:

```javascript
if ('serviceWorker' in navigator && '{service_worker_path}') {
  window.addEventListener('load', function() {
    navigator.serviceWorker.register('{service_worker_path}')
      .then(function(registration) {
        console.log('ServiceWorker registration successful');
      })
      .catch(function(error) {
        console.log('ServiceWorker registration failed: ', error);
      });
  });
}
```

## Complete PWA App Configuration Example

```python
# Create a complete PWA application
app = App(
    title="My PWA App",
    description="An amazing progressive application",
    author="My Company",
    keywords=["pwa", "webapp", "productivity"],
    language="en",
    favicon="assets/favicon.ico",
    icon="assets/icon-192x192.png",
    apple_touch_icon="assets/apple-touch-icon.png",
    theme_color="#4A90E2",
    background_color="#FFFFFF",
    service_worker_path="sw.js",
    service_worker_enabled=True,
    pwa_enabled=True,
    pwa_name="My App",
    pwa_short_name="MyApp",
    pwa_display="standalone"
)

# Add pages and components
app.add_page("home", HomeComponent(), title="Home", index=True)
app.add_page("about", AboutComponent(), title="About")
```

## Implementation Considerations

### Browser Compatibility

Dars Framework's PWA implementation is compatible with:
- Chrome/Chromium (full support)
- Firefox (basic support)
- Safari (limited support on iOS)
- Edge (full support)