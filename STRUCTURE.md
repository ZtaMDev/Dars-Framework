# Estructura del Proyecto Dars

## 📁 Estructura General

```
pywebui-framework/
├── README.md                    # Documentación principal
├── INSTALL.md                   # Guía de instalación
├── STRUCTURE.md                 # Este archivo
├── pywebui_exporter            # CLI principal ejecutable
├── pywebui_architecture.md     # Documentación de arquitectura
├── todo.md                     # Lista de tareas (desarrollo)
│
├── pywebui/                    # Framework principal
│   ├── __init__.py
│   ├── core/                   # Núcleo del framework
│   ├── components/             # Componentes UI
│   ├── scripts/                # Sistema de scripts
│   ├── exporters/              # Exportadores
│   ├── templates/              # Templates de exportación
│   ├── cli/                    # Herramientas CLI
│   └── docs/                   # Documentación detallada
│
└── examples/                   # Ejemplos de aplicaciones
    ├── README.md
    ├── basic/                  # Ejemplos básicos
    ├── advanced/               # Ejemplos avanzados
    └── demo/                   # Aplicación de demostración
```

## 🏗️ Núcleo del Framework (`pywebui/core/`)

```
core/
├── __init__.py
├── app.py                      # Clase principal App
├── component.py                # Clase base Component
├── properties.py               # Sistema de propiedades y estilos
└── events.py                   # Sistema de eventos
```

### Descripción de Archivos

- **`app.py`**: Clase principal que representa una aplicación Dars
- **`component.py`**: Clase base abstracta para todos los componentes
- **`properties.py`**: Define propiedades de estilo y eventos
- **`events.py`**: Sistema de manejo de eventos

## 🧩 Componentes (`pywebui/components/`)

```
components/
├── __init__.py
├── basic/                      # Componentes básicos
│   ├── __init__.py
│   ├── text.py                 # Componente Text
│   ├── button.py               # Componente Button
│   ├── input.py                # Componente Input
│   └── container.py            # Componente Container
├── advanced/                   # Componentes avanzados (futuro)
│   └── __init__.py
└── layout/                     # Componentes de layout (futuro)
    └── __init__.py
```

### Componentes Implementados

- **Text**: Mostrar texto estático o dinámico
- **Button**: Botones interactivos con eventos
- **Input**: Campos de entrada de datos
- **Container**: Contenedores para organizar layout

## 📜 Sistema de Scripts (`pywebui/scripts/`)

```
scripts/
├── __init__.py
└── script.py                   # Clases InlineScript y FileScript
```

### Tipos de Scripts

- **InlineScript**: Código JavaScript/TypeScript definido en Python
- **FileScript**: Código cargado desde archivos externos

## 🔄 Exportadores (`pywebui/exporters/`)

```
exporters/
├── __init__.py
├── base.py                     # Clase base Exporter
├── web/                        # Exportadores web
│   ├── __init__.py
│   ├── html_css_js.py          # Exportador HTML/CSS/JS
│   ├── react.py                # Exportador React
│   └── react_native.py         # Exportador React Native
└── native/                     # Exportadores nativos
    ├── __init__.py
    ├── pyside6.py              # Exportador PySide6
    ├── csharp.py               # Exportador C#
    └── kotlin.py               # Exportador Kotlin
```

### Exportadores Disponibles

#### Web
- **HTML/CSS/JS**: Aplicaciones web estándar
- **React**: Aplicaciones React modernas
- **React Native**: Aplicaciones móviles

#### Nativos
- **PySide6**: Aplicaciones de escritorio Qt
- **C#**: Aplicaciones Windows WinForms
- **Kotlin**: Aplicaciones Kotlin Multiplatform

## 📋 Templates (`pywebui/templates/`)

```
templates/
├── __init__.py
├── html/                       # Templates HTML
│   └── __init__.py
├── react/                      # Templates React
│   └── __init__.py
├── react_native/               # Templates React Native
│   └── __init__.py
├── pyside6/                    # Templates PySide6
│   └── __init__.py
├── csharp/                     # Templates C#
│   └── __init__.py
└── kotlin/                     # Templates Kotlin
    └── __init__.py
```

## 🛠️ Herramientas CLI (`pywebui/cli/`)

```
cli/
├── __init__.py
├── exporter.py                 # CLI principal con Rich
└── preview.py                  # Sistema de preview
```

### Herramientas Disponibles

- **exporter.py**: CLI principal para exportar aplicaciones
- **preview.py**: Sistema de preview para aplicaciones exportadas

## 📚 Documentación (`pywebui/docs/`)

```
docs/
├── __init__.py
├── getting_started.md          # Guía de inicio rápido
├── components.md               # Documentación de componentes
├── scripts.md                  # Sistema de scripts
└── exporters.md                # Guía de exportadores
```

## 🎯 Ejemplos (`examples/`)

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

### `pywebui_exporter`
Script ejecutable principal que proporciona la interfaz CLI.

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
    Código de Salida (HTML/React/etc.)
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
# pywebui/components/basic/mi_componente.py
from pywebui.core.component import Component

class MiComponente(Component):
    def __init__(self, **props):
        super().__init__(**props)
        # Implementación específica
```

### Nuevos Exportadores

```python
# pywebui/exporters/mi_plataforma/mi_exportador.py
from pywebui.exporters.base import Exporter

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
from pywebui.scripts.script import Script

class MiTipoScript(Script):
    def get_code(self):
        # Generar código específico
        return "código_generado"
```

## 📈 Métricas del Proyecto

### Líneas de Código (Aproximado)

- **Core**: ~800 líneas
- **Componentes**: ~600 líneas
- **Exportadores**: ~1200 líneas
- **CLI**: ~400 líneas
- **Scripts**: ~200 líneas
- **Ejemplos**: ~800 líneas
- **Documentación**: ~2000 líneas

### Total: ~6000 líneas de código y documentación

## 🚀 Roadmap de Desarrollo

### Implementado ✅

- [x] Núcleo del framework
- [x] Componentes básicos
- [x] Sistema de scripts
- [x] Exportadores principales
- [x] CLI con Rich
- [x] Sistema de preview
- [x] Documentación completa
- [x] Ejemplos funcionales

### Futuras Mejoras 🔮

- [ ] Más componentes (Image, Video, Table, etc.)
- [ ] Sistema de temas
- [ ] Hot reloading en desarrollo
- [ ] Plugin system
- [ ] Generador de código automático
- [ ] Testing framework integrado

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

