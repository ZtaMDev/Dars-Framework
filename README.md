# Dars Framework

**Framework de UI multiplataforma en Python**

Dars es un framework que permite crear interfaces de usuario modernas utilizando únicamente Python y exportarlas a HTML/CSS/JavaScript.

## Características Principales

- **Python Puro**: Permite el desarrollo de interfaces de usuario utilizando exclusivamente Python.
- **Multiplataforma**: Soporta la exportación a HTML/CSS/JavaScript.
- **Facilidad de Uso**: Ofrece una sintaxis intuitiva y simplificada.
- **Personalización**: Proporciona un sistema de estilos flexible para una adaptación visual completa.
- **Extensibilidad**: Diseñado con una arquitectura modular que facilita la expansión.
- **Diseño Adaptativo**: Genera interfaces que se ajustan a diferentes tamaños de pantalla.

## Instalación

### Requisitos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Dependencias

```bash
pip install rich
```

### Configuración

1. Descarga o clona el framework Dars
2. Asegúrate de que la carpeta `dars` esté en tu proyecto
3. ¡Listo para usar!

## Inicio Rápido

### Tu Primera Aplicación

```python
#!/usr/bin/env python3
import sys
import os

# Configurar path para Dars
framework_path = os.path.join(os.path.dirname(__file__), 'dars')
sys.path.insert(0, framework_path)

from dars.core.app import App
from dars.components.basic.text import Text
from dars.components.basic.button import Button
from dars.components.basic.container import Container
from dars.scripts.script import InlineScript

# Crear aplicación
app = App(title="Mi Primera App")

# Crear componentes
container = Container(style={
    'display': 'flex',
    'flex-direction': 'column',
    'align-items': 'center',
    'padding': '40px'
})

titulo = Text(
    text="Hola Dars",
    style={'font-size': '32px', 'color': '#333'}
)

boton = Button(
    text="Hacer clic",
    style={'background-color': '#007bff', 'color': 'white'}
)

# Script para interactividad
script = InlineScript("""
document.addEventListener('DOMContentLoaded', function() {
    const boton = document.querySelector('button');
    boton.addEventListener('click', function() {
        alert('Hola desde Dars.');
    });
});
""")

# Ensamblar aplicación
container.add_child(titulo)
container.add_child(boton)
app.set_root(container)
app.add_script(script)
```

### Exportar la Aplicación

```bash
# Exportar a HTML
dars export mi_app.py --format html --output ./mi_app_web
```

### Previsualizar

```bash
# Para aplicaciones HTML
python3 dars/cli/preview.py ./mi_app_web
```

## Herramientas de Línea de Comandos

### Dars

El exportador principal con interfaz rica en colores:

```bash
# Ver información de una aplicación
dars info mi_app.py

# Exportar a diferentes formatos
dars export mi_app.py --format html --output ./output

# Ver formatos soportados
dars formats

# Ayuda
dars --help
```

### Sistema de Preview

```bash
# Preview automático (detecta formato)
python3 dars/cli/preview.py ./output_directory

# Preview específico
python3 dars/cli/preview.py ./output_directory --format html

# Sin abrir navegador automáticamente
python3 dars/cli/preview.py ./output_directory --no-open
```

## Componentes Disponibles

### Componentes Básicos

- **Text**: Mostrar texto estático o dinámico
- **Button**: Botones interactivos
- **Input**: Campos de entrada de datos
- **Container**: Contenedores para layout

### Ejemplo de Uso

```python
# Texto con estilos
titulo = Text(
    text="Mi Título",
    style={
        'font-size': '24px',
        'color': '#2c3e50',
        'font-weight': 'bold'
    }
)

# Botón con eventos
boton = Button(
    text="Enviar",
    style={
        'background-color': '#28a745',
        'color': 'white',
        'padding': '10px 20px',
        'border': 'none',
        'border-radius': '4px'
    }
)

# Input con validación
email = Input(
    placeholder="tu@email.com",
    input_type="email",
    required=True,
    style={
        'width': '300px',
        'padding': '10px',
        'border': '1px solid #ccc'
    }
)

# Container con layout
formulario = Container(
    children=[titulo, email, boton],
    style={
        'display': 'flex',
        'flex-direction': 'column',
        'gap': '15px',
        'padding': '20px'
    }
)
```

## Sistema de Scripts

### Scripts Inline

```python
from dars.scripts.script import InlineScript

script = InlineScript("""
function validarFormulario() {
    const email = document.querySelector('input[type="email"]').value;
    if (!email.includes('@')) {
        alert('Email inválido');
        return false;
    }
    return true;
}

document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('form');
    form.addEventListener('submit', function(e) {
        if (!validarFormulario()) {
            e.preventDefault();
        }
    });
});
""")

app.add_script(script)
```

### Scripts desde Archivo

```python
from dars.scripts.script import FileScript

script = FileScript("./scripts/validaciones.js")
app.add_script(script)
```

## Exportadores Soportados

### Web

| Formato | Descripción | Comando |
|---------|-------------|---------|
| **html** | HTML/CSS/JavaScript estándar | `--format html` |

## Documentación

### Guías Completas

- [**Inicio Rápido**](dars/docs/getting_started.md) - Primeros pasos con Dars
- [**Componentes**](dars/docs/components.md) - Documentación completa de componentes
- [**Scripts**](dars/docs/scripts.md) - Sistema de scripts y eventos
- [**Exportadores**](dars/docs/exporters.md) - Guía de todos los exportadores

### Ejemplos

- [**Básicos**](examples/basic/) - Ejemplos simples para empezar
- [**Avanzados**](examples/advanced/) - Ejemplos complejos y características avanzadas
- [**Demostración**](examples/demo/) - Aplicación completa de demostración

## Ejemplos de Aplicaciones

### Hello World

```bash
./dars export examples/basic/hello_world.py --format html --output ./hello_output
```

### Formulario de Contacto

```bash
./dars export examples/basic/simple_form.py --format html --output ./form_output
```

### Dashboard Empresarial

```bash
./dars export examples/advanced/dashboard.py --format html --output ./dashboard_output
```

### Aplicación Completa

```bash
./dars export examples/demo/complete_app.py --format html --output ./demo_output
```

## Arquitectura del Framework

```
dars/
├── core/                   # Núcleo del framework
│   ├── app.py             # Clase principal App
│   ├── component.py       # Clase base Component
│   ├── properties.py      # Sistema de propiedades
│   └── events.py          # Sistema de eventos
├── components/            # Componentes UI
│   └── basic/            # Componentes básicos
│       ├── text.py       # Componente Text
│       ├── button.py     # Componente Button
│       ├── input.py      # Componente Input
│       └── container.py  # Componente Container
├── scripts/              # Sistema de scripts
│   └── script.py         # Clases de scripts
├── exporters/            # Exportadores
│   ├── base.py          # Clase base Exporter
│   ├── web/             # Exportadores web
│   └── native/          # Exportadores nativos
├── cli/                 # Herramientas CLI
│   ├── exporter.py      # CLI principal
│   └── preview.py       # Sistema de preview
└── docs/                # Documentación
```

## Casos de Uso

### Desarrollo Web

- **Landing Pages**: Sitios web estáticos y dinámicos
- **Aplicaciones Web**: SPAs con HTML/CSS/JavaScript
- **Dashboards**: Paneles de control empresariales

## Mejores Prácticas

### Organización del Código

```python
# Separar componentes en funciones
def crear_header():
    return Container(
        children=[
            Text("Mi App", style={'font-size': '24px'}),
            Text("Subtítulo", style={'color': '#666'})
        ],
        style={'padding': '20px'}
    )

def crear_contenido():
    return Container(
        children=[
            # Componentes del contenido
        ]
    )

# Ensamblar la aplicación
app = App(title="Mi Aplicación")
app.set_root(Container(children=[
    crear_header(),
    crear_contenido()
]))
```

### Estilos Reutilizables

```python
# Definir estilos comunes
ESTILOS_BOTON = {
    'padding': '10px 20px',
    'border': 'none',
    'border-radius': '4px',
    'cursor': 'pointer'
}

ESTILOS_BOTON_PRIMARIO = {
    **ESTILOS_BOTON,
    'background-color': '#007bff',
    'color': 'white'
}

# Usar en componentes
boton = Button("Enviar", style=ESTILOS_BOTON_PRIMARIO)
```

### Scripts Modulares

```python
# Separar funcionalidad en scripts específicos
validacion_script = FileScript("./scripts/validacion.js")
ui_script = FileScript("./scripts/ui-effects.js")
api_script = FileScript("./scripts/api-client.js")

app.add_script(validacion_script)
app.add_script(ui_script)
app.add_script(api_script)
```

## Solución de Problemas

### Errores Comunes

#### Error de Importación

```python
# ❌ Incorrecto
from core.app import App

# ✅ Correcto
import sys
import os
framework_path = os.path.join(os.path.dirname(__file__), 'dars')
sys.path.insert(0, framework_path)
from dars.core.app import App
```

#### Variable 'app' No Encontrada

```python
# ❌ Falta definir la variable app
container = Container()
# ...

# ✅ Correcto
app = App(title="Mi App")
container = Container()
app.set_root(container)
```

#### Problemas de Exportación

```bash
# Verificar que el archivo sea válido
./dars info mi_app.py

# Verificar formatos soportados
./dars formats
```

## Contribuir

Dars es un framework extensible. Puedes contribuir:

### Nuevos Componentes

```python
from dars.core.component import Component

class MiComponente(Component):
    def __init__(self, **props):
        super().__init__(**props)
        # Implementar lógica del componente
```

### Nuevos Exportadores

```python
from darss.base import Exporter

class MiExportador(Exporter):
    def get_platform(self):
        return "mi_plataforma"
    
    def export(self, app, output_path):
        # Implementar lógica de exportación
        return True
    
    def render_component(self, component):
        # Implementar renderizado
        return "código_generado"
```

## Licencia

Dars Framework - Creado en Python

## Soporte

### Documentación

- [**Inicio Rápido**](dars/docs/getting_started.md)
- [**Componentes**](dars/docs/components.md)
- [**Scripts**](dars/docs/scripts.md)
- [**Exportadores**](dars/docs/exporters.md)

### Ejemplos

- [Ejemplos Básicos](examples/basic/)
- [Ejemplos Avanzados](examples/advanced/)
- [Aplicación de Demostración](examples/demo/)

### Comandos de Ayuda

```bash
# Ayuda general
./dars --help

# Información de aplicación
./dars info mi_app.py

# Formatos disponibles
./dars formats
```

---

**¡Comienza a crear interfaces increíbles con Dars hoy mismo!**


