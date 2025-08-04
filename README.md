# Dars Framework

**Framework de UI multiplataforma en Python**

Dars es un framework que permite crear interfaces de usuario modernas utilizando únicamente Python y exportarlas a HTML/CSS/JavaScript.

## Características Principales

- **Python Puro**: Permite el desarrollo de interfaces de usuario utilizando exclusivamente Python.
- **Multiplataforma**: Soportado por todos los sistemas operativos compatibles con python.
- **Facilidad de Uso**: Ofrece una sintaxis intuitiva y simplificada.
- **Personalización**: Proporciona un sistema de estilos flexible para una adaptación visual completa.
- **Extensibilidad**: Diseñado con una arquitectura modular que facilita la expansión.
- **Diseño Adaptativo**: Genera interfaces que se ajustan a diferentes tamaños de pantalla.
- **Componentes Modernos**: Incluye Checkbox, RadioButton, Select, Slider, DatePicker y más.
- **SEO Optimizado**: Meta tags completos, Open Graph, Twitter Cards y configuración robots.
- **PWA Ready**: Soporte completo para Progressive Web Apps con manifest y configuración móvil.
- **Templates Oficiales**: Templates básicos y avanzados para inicio rápido de proyectos.

## Instalación

Para instalar Dars, simplemente usa pip:

```bash
pip install dars-framework
```

### Requisitos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)

## Inicio Rápido

### Tu Primera Aplicación

```python
#!/usr/bin/env python3
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
dars export mi_app.py --format html --output ./mi_app_web
```

### Previsualizar

```bash
dars preview ./mi_app_web
```

## Herramientas de Línea de Comandos (CLI)

### Dars CLI

El CLI de Dars te permite gestionar tus proyectos, exportar aplicaciones y previsualizar resultados. Aquí están los comandos principales:

```bash
# Ver información de una aplicación
dars info mi_app.py

# Exportar a diferentes formatos
dars export mi_app.py --format html --output ./output

# Ver formatos soportados
dars formats

# Inicializar un nuevo proyecto
dars init mi_nuevo_proyecto

# Inicializar un proyecto con una plantilla específica
dars init mi_nuevo_proyecto -t demo/complete_app

# Previsualizar una aplicación exportada
dars preview ./output_directory

# Ayuda
dars --help
```

## Componentes Disponibles

### Componentes Básicos

#### Componentes de Texto y Navegación
- **Text**: Mostrar texto estático o dinámico
- **Link**: Crear enlaces de navegación
- **Image**: Mostrar imágenes

#### Componentes de Entrada
- **Input**: Campos de entrada de datos
- **Textarea**: Áreas de texto multilínea
- **Button**: Botones interactivos

#### Nuevos Componentes de Formulario (2024)
- **Checkbox**: Casillas de verificación con etiquetas
- **RadioButton**: Botones de opción para selección única
- **Select**: Menús desplegables con opciones múltiples
- **Slider**: Controles deslizantes para valores numéricos
- **DatePicker**: Selectores de fecha con múltiples formatos

#### Componentes de Layout
- **Container**: Contenedores para layout y organización

### Componentes Avanzados

- **Card**: Contenedor estilizado para agrupar contenido relacionado
- **Modal**: Ventana emergente superpuesta al contenido principal
- **Navbar**: Barra de navegación

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

# Imagen
imagen = Image(
    src="https://via.placeholder.com/150",
    alt="Placeholder Image",
    width="150px"
)

# Enlace
enlace = Link(
    text="Visitar Dars",
    href="https://github.com/your-repo/dars",
    target="_blank"
)

# Nuevos Componentes de Formulario

# Checkbox
checkbox = Checkbox(
    label="Acepto los términos y condiciones",
    checked=False,
    required=True
)

# RadioButton
radio1 = RadioButton(
    label="Opción A",
    name="opciones",
    value="a",
    checked=True
)

radio2 = RadioButton(
    label="Opción B",
    name="opciones",
    value="b"
)

# Select con opciones
select = Select(
    placeholder="Selecciona un país"
)
select.add_option(SelectOption(value="es", label="España"))
select.add_option(SelectOption(value="mx", label="México"))
select.add_option(SelectOption(value="ar", label="Argentina"))

# Slider
slider = Slider(
    min_value=0,
    max_value=100,
    value=50,
    show_value=True,
    label="Porcentaje"
)

# DatePicker
date_picker = DatePicker(
    format="DD/MM/YYYY",
    placeholder="Selecciona una fecha"
)

# Textarea
comentarios = Textarea(
    placeholder="Tus comentarios...",
    rows=4,
    cols=50
)

# Card
mi_card = Card(
    title="Mi Tarjeta",
    children=[
        Text("Contenido de la tarjeta."),
        Button("Acción")
    ]
)

# Navbar
mi_navbar = Navbar(
    brand="Mi App",
    children=[
        Link("Inicio", "/"),
        Link("Acerca de", "/about")
    ]
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

### Ejemplos y Templates Oficiales

- [**Básicos**](dars/templates/examples/basic/) - Ejemplos simples para empezar
- [**Avanzados**](dars/templates/examples/advanced/) - Ejemplos complejos y características avanzadas
- [**Demostración**](dars/templates/examples/demo/) - Aplicación completa de demostración

#### Templates Disponibles

**Template Básico - Componentes de Formulario:**
```bash
# Crear proyecto con nuevos componentes básicos
dars init mi_formulario -t basic/form_components
```
Incluye: Checkbox, RadioButton, Select, Slider, DatePicker con ejemplos interactivos.

**Template Avanzado - Aplicación Web Moderna:**
```bash
# Crear aplicación con SEO, PWA y Open Graph
dars init mi_app_moderna -t advanced/modern_web_app
```
Incluye: SEO completo, Open Graph, Twitter Cards, PWA, todos los componentes nuevos.

## Ejemplos de Aplicaciones

### Hello World

```bash
dars export dars/templates/examples/basic/hello_world.py --format html --output ./hello_output
```

### Formulario de Contacto

```bash
dars export dars/templates/examples/basic/simple_form.py --format html --output ./form_output
```

### Dashboard Empresarial

```bash
dars export dars/templates/examples/advanced/dashboard.py --format html --output ./dashboard_output
```

### Aplicación Completa

```bash
dars export dars/templates/examples/demo/complete_app.py --format html --output ./demo_output
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
│   ├── basic/            # Componentes básicos
│       ├── text.py       # Componente Text
│       ├── button.py     # Componente Button
│       ├── input.py      # Componente Input
│       ├── container.py  # Componente Container
│       ├── image.py      # Componente Image
│       ├── link.py       # Componente Link
│       └── textarea.py   # Componente Textarea
│   └── advanced/         # Componentes avanzados
│       ├── card.py       # Componente Card
│       ├── modal.py      # Componente Modal
│       └── navbar.py     # Componente Navbar
├── scripts/              # Sistema de scripts
│   └── script.py         # Clases de scripts
├── exporters/            # Exportadores
│   ├── base.py          # Clase base Exporter
│   └── web/             # Exportadores web
├── cli/                 # Herramientas CLI
│   ├── main.py          # CLI principal
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

Ahora que Dars se instala como un paquete, las importaciones son directas:

```python
# ✅ Correcto
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
dars info mi_app.py

# Verificar formatos soportados
dars formats
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
from dars.exporters.base import Exporter

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

- [Ejemplos Básicos](dars/templates/examples/basic/)
- [Ejemplos Avanzados](dars/templates/examples/advanced/)
- [Aplicación de Demostración](dars/templates/examples/demo/)

### Comandos de Ayuda

```bash
# Ayuda general
dars --help

# Información de aplicación
dars info mi_app.py

# Formatos disponibles
dars formats
```

---

**¡Comienza a crear interfaces increíbles con Dars hoy mismo!**




