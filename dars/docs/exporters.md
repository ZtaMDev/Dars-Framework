# Dars - Documentación de Exportadores

## Introducción

Los exportadores son el corazón de Dars que permiten transformar aplicaciones escritas en Python a diferentes tecnologías y plataformas. Cada exportador traduce los componentes, estilos y scripts de Dars al código nativo de la plataforma objetivo.

## Arquitectura de Exportadores

### Clase Base Exporter

Todos los exportadores heredan de la clase base `Exporter`:

```python
from abc import ABC, abstractmethod

class Exporter(ABC):
    def __init__(self):
        self.templates_path = "templates/"
        
    @abstractmethod
    def export(self, app: App, output_path: str) -> bool:
        """Exporta la aplicación al formato específico"""
        pass
        
    @abstractmethod
    def render_component(self, component: Component) -> str:
        """Renderiza un componente individual"""
        pass
        
    @abstractmethod
    def get_platform(self) -> str:
        """Retorna el nombre de la plataforma"""
        pass
```

### Flujo de Exportación

1. **Validación**: Verificar que la aplicación sea válida
2. **Preparación**: Crear estructura de directorios
3. **Renderizado**: Convertir componentes al formato objetivo
4. **Generación**: Crear archivos de configuración y dependencias
5. **Finalización**: Escribir archivos al sistema

## Exportadores Web

### HTML/CSS/JavaScript

El exportador HTML genera aplicaciones web estándar que pueden ejecutarse en cualquier navegador.

#### Características

- **Compatibilidad**: Funciona en todos los navegadores modernos
- **Simplicidad**: No requiere herramientas de build
- **Performance**: Carga rápida y ejecución eficiente
- **SEO**: Contenido indexable por motores de búsqueda

#### Uso

```bash
dars export mi_app.py --format html --output ./dist
```

#### Estructura Generada

```
dist/
├── index.html      # Página principal
├── styles.css      # Estilos CSS
└── script.js       # Lógica JavaScript
```

#### Ejemplo de Salida

**index.html**
```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Mi Aplicación</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <div id="container_123" class="dars-container" style="display: flex; flex-direction: column; padding: 20px;">
        <span id="text_456" class="dars-text" style="font-size: 24px; color: #333;">¡Hola Dars!</span>
        <button id="button_789" class="dars-button" style="background-color: #007bff; color: white;">Hacer clic</button>
    </div>
    <script src="script.js"></script>
</body>
</html>
```

**styles.css**
```css
/* Estilos base de Dars */
* {
    box-sizing: border-box;
}

body {
    margin: 0;
    padding: 0;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
}

.dars-button {
    display: inline-block;
    padding: 8px 16px;
    border: 1px solid #ccc;
    background-color: #f8f9fa;
    color: #333;
    cursor: pointer;
    border-radius: 4px;
    font-size: 14px;
}

.dars-button:hover {
    background-color: #e9ecef;
}
```

#### Ventajas

- **Universalidad**: Funciona en cualquier servidor web
- **Debugging**: Fácil de depurar con herramientas del navegador
- **Personalización**: CSS y JavaScript completamente modificables
- **Hosting**: Puede alojarse en cualquier servicio de hosting estático

#### Casos de Uso

- Sitios web corporativos
- Landing pages
- Aplicaciones web simples
- Prototipos rápidos
- Documentación interactiva

## Personalización de Exportadores

### Extender Exportadores Existentes

```python
from dars.exporters.base import Exporter

class MiExportadorPersonalizado(Exporter):
    def get_platform(self):
        return "mi_plataforma_personalizada"
    
    def export(self, app, output_path):
        # Implementar lógica de exportación personalizada
        return True
    
    def render_component(self, component):
        # Implementar renderizado de componentes personalizado
        return "código_generado"
```


