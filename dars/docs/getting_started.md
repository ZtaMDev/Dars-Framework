# Dars - Guía de Inicio Rápido

## Introducción

Dars es un framework que permite a los desarrolladores crear interfaces de usuario modernas utilizando únicamente Python, y exportarlas a HTML/CSS/JS.

## Instalación

### Requisitos del Sistema

- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Instalación del Framework

Para instalar Dars, simplemente usa pip:

```bash
pip install dars-framework
```

Esto instalará Dars y todas sus dependencias automáticamente.

## Tu Primera Aplicación

Vamos a crear una aplicación simple que muestre un saludo y un botón interactivo.

### Paso 1: Crear el Archivo de la Aplicación

Crea un archivo llamado `mi_primera_app.py`:

```python
from dars.core.app import App
from dars.components.basic.text import Text
from dars.components.basic.button import Button
from dars.components.basic.container import Container
from dars.scripts.script import InlineScript

# Crear la aplicación con propiedades básicas
app = App(
    title="Mi Primera Aplicación Dars",
    description="Una aplicación de ejemplo creada con Dars Framework",
    author="Tu Nombre",
    keywords=["dars", "framework", "python", "web"]
)

# Crear componentes
container = Container(
    style={
        'display': 'flex',
        'flex-direction': 'column',
        'align-items': 'center',
        'padding': '40px',
        'background-color': '#f8f9fa'
    }
)

titulo = Text(
    text="Bienvenido a Dars",
    style={
        'font-size': '32px',
        'color': '#333',
        'margin-bottom': '20px',
        'font-weight': 'bold'
    }
)

descripcion = Text(
    text="Framework de UI multiplataforma en Python",
    style={
        'font-size': '18px',
        'color': '#666',
        'margin-bottom': '30px'
    }
)

boton = Button(
    text="¡Haz clic aquí!",
    style={
        'background-color': '#007bff',
        'color': 'white',
        'padding': '12px 24px',
        'border': 'none',
        'border-radius': '6px',
        'font-size': '16px',
        'cursor': 'pointer'
    }
)

# Agregar script interactivo
script = InlineScript("""
function handleButtonClick() {
    alert('¡Hola desde Dars!');
    console.log('Botón presionado');
}

// Agregar evento al botón cuando se cargue la página
document.addEventListener('DOMContentLoaded', function() {
    const button = document.querySelector('button');
    if (button) {
        button.addEventListener('click', handleButtonClick);
    }
});
""")

# Ensamblar la aplicación
container.add_child(titulo)
container.add_child(descripcion)
container.add_child(boton)

app.set_root(container)
app.add_script(script)
```

### Paso 2: Exportar la Aplicación

Ahora puedes exportar tu aplicación a HTML/CSS/JS usando el exportador de Dars:

#### Exportar a HTML/CSS/JS

```bash
dars export mi_primera_app.py --format html --output ./mi_app_web
```

### Paso 3: Previsualizar la Aplicación

Para ver tu aplicación en acción:

#### Para aplicaciones HTML

```bash
dars preview ./mi_app_web
```

Esto iniciará un servidor local y abrirá tu aplicación en el navegador.

## Conceptos Fundamentales

### Componentes

Los componentes son los bloques de construcción básicos de Dars. Cada componente hereda de la clase base `Component` y puede tener:

- **Propiedades**: Configuración del componente (texto, estilos, etc.)
- **Hijos**: Otros componentes anidados
- **Eventos**: Manejadores de interacciones del usuario

### Estilos

Dars utiliza un sistema de estilos similar a CSS, pero definido en Python usando diccionarios:

```python
estilo = {
    'background-color': '#007bff',
    'color': 'white',
    'padding': '10px 20px',
    'border': 'none',
    'border-radius': '4px',
    'font-size': '16px'
}
```

## Nuevos Componentes de Formulario

Dars ahora incluye componentes modernos de formulario para crear interfaces interactivas:

### Ejemplo con Nuevos Componentes

```python
from dars.core.app import App
from dars.components.basic.container import Container
from dars.components.basic.text import Text
from dars.components.basic.checkbox import Checkbox
from dars.components.basic.radiobutton import RadioButton
from dars.components.basic.select import Select, SelectOption
from dars.components.basic.slider import Slider
from dars.components.basic.datepicker import DatePicker
from dars.components.basic.button import Button

# Crear aplicación
app = App(title="Formulario Moderno")

# Container principal
formulario = Container(style={
    'max-width': '600px',
    'margin': '0 auto',
    'padding': '20px'
})

# Título
titulo = Text(
    text="Formulario con Nuevos Componentes",
    style={'font-size': '24px', 'margin-bottom': '20px'}
)

# Checkbox
terms_checkbox = Checkbox(
    label="Acepto los términos y condiciones",
    required=True
)

# Radio buttons
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

# Select
country_select = Select(placeholder="Selecciona tu país")
country_select.add_option(SelectOption(value="es", label="España"))
country_select.add_option(SelectOption(value="mx", label="México"))

# Slider
age_slider = Slider(
    min_value=18,
    max_value=100,
    value=25,
    show_value=True,
    label="años"
)

# Date picker
date_picker = DatePicker(
    format="DD/MM/YYYY",
    placeholder="Fecha de nacimiento"
)

# Botón de envío
submit_btn = Button(
    text="Enviar Formulario",
    style={
        'background': '#28a745',
        'color': 'white',
        'padding': '12px 24px',
        'border': 'none',
        'border-radius': '4px'
    }
)

# Ensamblar formulario
formulario.add_child(titulo)
formulario.add_child(terms_checkbox)
formulario.add_child(radio1)
formulario.add_child(radio2)
formulario.add_child(country_select)
formulario.add_child(age_slider)
formulario.add_child(date_picker)
formulario.add_child(submit_btn)

app.set_root(formulario)
```

## Aplicaciones Web Modernas

### Propiedades Extendidas de la Clase App

Dars ahora soporta propiedades avanzadas para SEO, redes sociales y PWA:

```python
from dars.core.app import App

# Aplicación con propiedades modernas
app = App(
    # Propiedades básicas
    title="Mi App Moderna | Dars Framework",
    description="Una aplicación web moderna con SEO y PWA",
    author="Tu Nombre",
    keywords=["dars", "framework", "python", "web", "pwa"],
    language="es",
    
    # Iconos y favicon
    favicon="/favicon.ico",
    icon="/icon-192.png",
    apple_touch_icon="/apple-touch-icon.png",
    manifest="/manifest.json",
    
    # Colores de tema (PWA)
    theme_color="#1e3a8a",
    background_color="#f8fafc",
    
    # Open Graph para redes sociales
    og_title="Mi App - Framework Dars",
    og_description="Aplicación moderna creada con Dars",
    og_image="https://mi-dominio.com/og-image.jpg",
    og_url="https://mi-dominio.com",
    
    # Twitter Cards
    twitter_card="summary_large_image",
    twitter_site="@mi_usuario",
    
    # SEO avanzado
    robots="index, follow",
    canonical_url="https://mi-dominio.com",
    
    # PWA configuración
    pwa_enabled=True,
    pwa_name="Mi App",
    pwa_short_name="MiApp"
)

# Usar métodos extendidos
app.add_keywords(["responsive", "moderno"])
app.set_theme_colors("#1e3a8a", "#f8fafc")
app.enable_pwa("Mi App Moderna", "AppModerna")
```

### Características de Aplicaciones Modernas

- **SEO Completo**: Meta tags, keywords, description, robots.txt
- **Open Graph**: Integración con Facebook, LinkedIn
- **Twitter Cards**: Optimización para Twitter
- **Progressive Web App**: Manifest, iconos, instalación nativa
- **Favicon Multi-dispositivo**: Soporte para diferentes tamaños

## Templates Oficiales

### Inicio Rápido con Templates

Dars incluye templates oficiales para empezar rápidamente:

#### Template Básico - Componentes de Formulario
```bash
# Crear proyecto con nuevos componentes
dars init mi_formulario -t basic/form_components
dars export mi_formulario.py --format html --output ./mi_formulario
dars preview ./mi_formulario
```

#### Template Avanzado - Aplicación Web Moderna
```bash
# Crear aplicación con SEO, PWA y Open Graph
dars init mi_app_moderna -t advanced/modern_web_app
dars export mi_app_moderna.py --format html --output ./mi_app_moderna
dars preview ./mi_app_moderna
```

```python
estilo_boton = {
    'background-color': '#007bff',
    'color': 'white',
    'padding': '10px 20px',
    'border': 'none',
    'border-radius': '4px'
}
```

### Scripts

Los scripts permiten agregar lógica interactiva a tus aplicaciones. Puedes usar:

- **InlineScript**: Código JavaScript definido directamente en Python
- **FileScript**: Código cargado desde archivos externos

### Aplicación (App)

La clase `App` es el contenedor principal que:

- Mantiene la configuración global
- Contiene el componente raíz
- Gestiona los scripts
- Define estilos globales

## Próximos Pasos

Ahora que has creado tu primera aplicación, puedes:

1. Explorar más componentes en la [documentación de componentes](components.md)
2. Aprender sobre el sistema de scripts en [scripts.md](scripts.md)
3. Descubrir todos los exportadores disponibles en [exporters.md](exporters.md)
4. Ver ejemplos avanzados en el directorio `dars/templates/examples/`

## Comandos Útiles

### Inicializar un Nuevo Proyecto

```bash
# Proyecto básico con Hello World
dars init mi_proyecto

# Proyecto con una plantilla específica
dars init mi_proyecto -t demo/complete_app
```

### Información de la Aplicación

```bash
dars info mi_primera_app.py
```

### Ver Formatos Soportados

```bash
dars formats
```

### Ayuda del CLI

```bash
dars --help
```

¡Felicidades! Has creado tu primera aplicación con Dars. El framework te permite crear interfaces modernas y exportarlas a múltiples plataformas con facilidad y elegancia.


