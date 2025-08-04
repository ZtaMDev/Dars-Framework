# Estructura del Proyecto Dars

## 📁 Estructura General

```
dars-framework/
├── README.md                    # Documentación principal
├── INSTALL.md                   # Guía de instalación
├── STRUCTURE.md                 # Este archivo
├── dars_architecture.md         # Documentación de arquitectura
├── pyproject.toml               # Configuración del proyecto Python
│
├── dars/                       # Framework principal
│   ├── __init__.py
│   ├── core/                   # Núcleo del framework
│   ├── components/             # Componentes UI
│   ├── scripts/                # Sistema de scripts
│   ├── exporters/              # Exportadores
│   ├── templates/              # Templates de exportación
│   ├── cli/                    # Herramientas CLI
│   └── docs/                   # Documentación detallada
│
└── dars/templates/examples/    # Ejemplos de aplicaciones
    ├── README.md
    ├── basic/                  # Ejemplos básicos
    ├── advanced/               # Ejemplos avanzados
    └── demo/                   # Aplicación de demostración
```

## 🏗️ Núcleo del Framework (`dars/core/`)

```
core/
├── __init__.py
├── app.py                      # Clase principal App
├── component.py                # Clase base Component
├── properties.py               # Sistema de propiedades y estilos
└── events.py                   # Sistema de manejo de eventos
```

### Descripción de Archivos

- **`app.py`**: Clase principal que representa una aplicación Dars
- **`component.py`**: Clase base abstracta para todos los componentes
- **`properties.py`**: Define propiedades de estilo y eventos
- **`events.py`**: Sistema de manejo de eventos

## 🧩 Componentes (`dars/components/`)

```
components/
├── __init__.py
├── basic/                      # Componentes básicos
│   ├── __init__.py
│   ├── text.py                 # Componente Text
│   ├── button.py               # Componente Button
│   ├── input.py                # Componente Input
│   ├── container.py            # Componente Container
│   ├── image.py                # Componente Image
│   ├── link.py                 # Componente Link
│   └── textarea.py             # Componente Textarea
├── advanced/                   # Componentes avanzados
│   ├── __init__.py
│   ├── card.py                 # Componente Card
│   ├── modal.py                # Componente Modal
│   └── navbar.py               # Componente Navbar
└── layout/                     # Componentes de layout (futuro)
    └── __init__.py
```

### Componentes Implementados

- **Text**: Mostrar texto estático o dinámico
- **Button**: Botones interactivos
- **Input**: Campos de entrada de datos
- **Container**: Contenedores para organizar layout
- **Image**: Mostrar imágenes
- **Link**: Crear enlaces de navegación
- **Textarea**: Áreas de texto multilínea
- **Card**: Contenedor estilizado para agrupar contenido
- **Modal**: Ventana emergente superpuesta
- **Navbar**: Barra de navegación

## 📜 Sistema de Scripts (`dars/scripts/`)

```
scripts/
├── __init__.py
└── script.py                   # Clases InlineScript y FileScript
```

### Tipos de Scripts

- **InlineScript**: Código JavaScript definido en Python
- **FileScript**: Código cargado desde archivos externos

## 🔄 Exportadores (`dars/exporters/`)

```
exporters/
├── __init__.py
├── base.py                     # Clase base Exporter
└── web/                        # Exportadores web
    ├── __init__.py
    └── html_css_js.py          # Exportador HTML/CSS/JS
```

### Exportadores Disponibles

#### Web
- **HTML/CSS/JS**: Aplicaciones web estándar

## 📋 Templates (`dars/templates/`)

```
templates/
├── __init__.py
├── examples/                   # Ejemplos de aplicaciones
│   ├── README.md
│   ├── basic/                  # Ejemplos básicos
│   ├── advanced/               # Ejemplos avanzados
│   └── demo/                   # Aplicación de demostración
└── html/                       # Templates HTML
    └── __init__.py
```

## 🛠️ Herramientas CLI (`dars/cli/`)

```
cli/
├── __init__.py
├── main.py                     # CLI principal con Rich
└── preview.py                  # Sistema de preview
```

### Herramientas Disponibles

- **main.py**: CLI principal para exportar aplicaciones
- **preview.py**: Sistema de preview para aplicaciones exportadas

## 📚 Documentación (`dars/docs/`)

```
docs/
├── __init__.py
├── getting_started.md          # Guía de inicio rápido
├── components.md               # Documentación de componentes
├── scripts.md                  # Sistema de scripts
└── exporters.md                # Guía de exportadores
```

## 🎯 Ejemplos (`dars/templates/examples/`)

```
examples/
├── README.md                   # Guía de ejemplos
├── basic/                      # Ejemplos básicos
│   ├── hello_world.py          # Ejemplo Hello World
│   └── simple_form.py          # Formulario simple
├── advanced/                   # Ejemplos avanzados
│   └── dashboard.py            # Dashboard empresarial
└── demo/                       # Demostración completa
    └── complete_app.py         # Aplicación completa
```

### Tipos de Ejemplos

#### Básicos
- **Hello World**: Aplicación simple con texto y botón
- **Simple Form**: Formulario con validación

#### Avanzados
- **Dashboard**: Panel de control con navegación y estadísticas

#### Demostración
- **Complete App**: Aplicación que muestra todas las características

## 🔧 Archivos de Configuración

### `pyproject.toml`
Archivo de configuración para el proyecto Python, incluyendo metadatos y dependencias para PyPI.

### `__init__.py`
Archivos de inicialización de módulos Python en cada directorio.

## 📊 Flujo de Datos

```
Aplicación Python (*.py)
         ↓
    Dars Core
         ↓
    Validación
         ↓
    Exportador Específico
         ↓
    Código de Salida (HTML/CSS/JS)
```

## 🎨 Patrones de Diseño Utilizados

### Factory Pattern
- Los exportadores se crean dinámicamente según el formato solicitado

### Component Pattern
- Todos los elementos UI heredan de la clase base Component

### Strategy Pattern
- Diferentes estrategias de exportación para cada plataforma

### Template Method Pattern
- Proceso de exportación común con pasos específicos por plataforma

## 🔍 Puntos de Extensión

### Nuevos Componentes

```python
# dars/components/basic/mi_componente.py
from dars.core.component import Component

class MiComponente(Component):
    def __init__(self, **props):
        super().__init__(**props)
        # Implementación específica
```

### Nuevos Exportadores

```python
# dars/exporters/mi_plataforma/mi_exportador.py
from dars.exporters.base import Exporter

class MiExportador(Exporter):
    def get_platform(self):
        return "mi_plataforma"
    
    def export(self, app, output_path):
        # Lógica de exportación
        return True
```

### Nuevos Scripts

```python
# Extender funcionalidad de scripts
from dars.scripts.script import Script

class MiTipoScript(Script):
    def get_code(self):
        # Generar código específico
        return "código_generado"
```

## 📈 Métricas del Proyecto

### Líneas de Código (Aproximado)

- **Core**: ~800 líneas
- **Componentes**: ~1000 líneas (actualizado con nuevos componentes)
- **Exportadores**: ~500 líneas (solo HTML/CSS/JS)
- **CLI**: ~400 líneas
- **Scripts**: ~200 líneas
- **Ejemplos**: ~800 líneas
- **Documentación**: ~3000 líneas (actualizado con nueva documentación)

### Total: ~7000 líneas de código y documentación

## 🚀 Roadmap de Desarrollo

### Implementado ✅

- [x] Núcleo del framework
- [x] Componentes básicos (Text, Button, Input, Container, Image, Link, Textarea)
- [x] Componentes avanzados (Card, Modal, Navbar)
- [x] Sistema de scripts
- [x] Exportador HTML/CSS/JS
- [x] CLI con Rich
- [x] Sistema de preview
- [x] Documentación completa
- [x] Ejemplos funcionales

### Futuras Mejoras 🔮

- [ ] Más componentes (Video, Table, Chart, etc.)
- [ ] Sistema de temas avanzado
- [ ] Hot reloading en desarrollo
- [ ] Plugin system
- [ ] Generador de código automático
- [ ] Testing framework integrado
- [ ] Exportadores para otras plataformas (React, React Native, Desktop)

## 🛡️ Consideraciones de Seguridad

### Scripts
- Los scripts se ejecutan en el contexto del navegador/aplicación
- Validación de entrada en formularios
- Sanitización de datos

### Exportación
- Validación de rutas de salida
- Verificación de permisos de escritura
- Escape de caracteres especiales

## 📝 Convenciones de Código

### Python
- PEP 8 para estilo de código
- Type hints donde sea apropiado
- Docstrings para clases y métodos públicos

### JavaScript
- ES6+ features
- Comentarios descriptivos
- Manejo de errores

### Estructura de Archivos
- Un componente por archivo
- Nombres descriptivos
- Organización lógica por funcionalidad

---

Esta estructura proporciona una base sólida y extensible para el framework Dars, permitiendo fácil mantenimiento y expansión futura.


