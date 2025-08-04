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

# Crear la aplicación
app = App(title="Mi Primera Aplicación Dars")

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


