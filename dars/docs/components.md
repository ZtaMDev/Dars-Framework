# Dars - Documentación de Componentes

## Introducción a los Componentes

Los componentes son los elementos fundamentales de Dars que representan elementos de la interfaz de usuario. Cada componente encapsula su apariencia, comportamiento y estado, permitiendo crear interfaces complejas mediante la composición de elementos simples.

## Clase Base Component

Todos los componentes en Dars heredan de la clase base `Component`, que proporciona la funcionalidad común:

```python
from pywebui.core.component import Component

class Component(ABC):
    def __init__(self, **props):
        self.props = props
        self.children = []
        self.parent = None
        self.id = props.get('id')
        self.class_name = props.get('class_name')
        self.style = props.get('style', {})
        self.events = {}
```

### Propiedades Comunes

Todos los componentes soportan estas propiedades básicas:

- **id**: Identificador único del componente
- **class_name**: Clase CSS para estilos adicionales
- **style**: Diccionario con estilos CSS
- **children**: Lista de componentes hijos (para contenedores)

## Componentes Básicos

### Text

El componente `Text` muestra texto estático o dinámico.

#### Sintaxis

```python
from pywebui.components.basic.text import Text

texto = Text(
    text="Contenido del texto",
    id="mi-texto",
    class_name="texto-principal",
    style={
        'font-size': '16px',
        'color': '#333',
        'font-weight': 'bold'
    }
)
```

#### Propiedades

| Propiedad | Tipo | Descripción | Ejemplo |
|-----------|------|-------------|---------|
| `text` | str | Contenido del texto | `"Hola mundo"` |
| `id` | str | Identificador único | `"titulo-principal"` |
| `class_name` | str | Clase CSS | `"texto-destacado"` |
| `style` | dict | Estilos CSS | `{'color': 'red'}` |

#### Estilos Comunes

```python
# Título principal
titulo = Text(
    text="Título Principal",
    style={
        'font-size': '32px',
        'font-weight': 'bold',
        'color': '#2c3e50',
        'margin-bottom': '20px',
        'text-align': 'center'
    }
)

# Párrafo de contenido
parrafo = Text(
    text="Este es un párrafo de ejemplo con contenido descriptivo.",
    style={
        'font-size': '16px',
        'line-height': '1.6',
        'color': '#34495e',
        'margin-bottom': '15px'
    }
)

# Texto pequeño
nota = Text(
    text="Nota: Esta información es importante.",
    style={
        'font-size': '12px',
        'color': '#7f8c8d',
        'font-style': 'italic'
    }
)
```

### Button

El componente `Button` crea botones interactivos que pueden ejecutar acciones.

#### Sintaxis

```python
from pywebui.components.basic.button import Button

boton = Button(
    text="Hacer clic",
    button_type="button",  # "button", "submit", "reset"
    disabled=False,
    on_click=mi_funcion,
    style={
        'background-color': '#3498db',
        'color': 'white',
        'padding': '10px 20px',
        'border': 'none',
        'border-radius': '4px'
    }
)
```

#### Propiedades

| Propiedad | Tipo | Descripción | Valores |
|-----------|------|-------------|---------|
| `text` | str | Texto del botón | `"Enviar"` |
| `button_type` | str | Tipo de botón | `"button"`, `"submit"`, `"reset"` |
| `disabled` | bool | Si está deshabilitado | `True`, `False` |
| `on_click` | function | Función de callback | Función Python |

#### Ejemplos de Botones

```python
# Botón primario
boton_primario = Button(
    text="Acción Principal",
    style={
        'background-color': '#007bff',
        'color': 'white',
        'padding': '12px 24px',
        'border': 'none',
        'border-radius': '6px',
        'font-size': '16px',
        'font-weight': '500',
        'cursor': 'pointer',
        'transition': 'background-color 0.3s'
    }
)

# Botón secundario
boton_secundario = Button(
    text="Cancelar",
    style={
        'background-color': 'transparent',
        'color': '#6c757d',
        'padding': '12px 24px',
        'border': '1px solid #6c757d',
        'border-radius': '6px',
        'font-size': '16px',
        'cursor': 'pointer'
    }
)

# Botón de peligro
boton_eliminar = Button(
    text="Eliminar",
    style={
        'background-color': '#dc3545',
        'color': 'white',
        'padding': '8px 16px',
        'border': 'none',
        'border-radius': '4px',
        'font-size': '14px'
    }
)

# Botón deshabilitado
boton_deshabilitado = Button(
    text="No disponible",
    disabled=True,
    style={
        'background-color': '#e9ecef',
        'color': '#6c757d',
        'padding': '10px 20px',
        'border': 'none',
        'border-radius': '4px',
        'cursor': 'not-allowed'
    }
)
```

### Input

El componente `Input` permite la entrada de datos del usuario.

#### Sintaxis

```python
from pywebui.components.basic.input import Input

entrada = Input(
    value="Valor inicial",
    placeholder="Escribe aquí...",
    input_type="text",  # "text", "password", "email", "number", etc.
    disabled=False,
    readonly=False,
    required=False,
    max_length=100,
    on_change=mi_funcion_cambio,
    style={
        'width': '300px',
        'padding': '10px',
        'border': '1px solid #ddd',
        'border-radius': '4px'
    }
)
```

#### Propiedades

| Propiedad | Tipo | Descripción | Valores |
|-----------|------|-------------|---------|
| `value` | str | Valor inicial | `"texto"` |
| `placeholder` | str | Texto de ayuda | `"Ingresa tu nombre"` |
| `input_type` | str | Tipo de entrada | `"text"`, `"password"`, `"email"`, `"number"` |
| `disabled` | bool | Si está deshabilitado | `True`, `False` |
| `readonly` | bool | Solo lectura | `True`, `False` |
| `required` | bool | Campo obligatorio | `True`, `False` |
| `max_length` | int | Longitud máxima | `50` |
| `min_length` | int | Longitud mínima | `3` |
| `pattern` | str | Patrón de validación | `"[0-9]+"` |

#### Tipos de Input

```python
# Campo de texto básico
nombre = Input(
    placeholder="Ingresa tu nombre",
    input_type="text",
    required=True,
    style={
        'width': '100%',
        'padding': '12px',
        'border': '2px solid #e1e5e9',
        'border-radius': '8px',
        'font-size': '16px'
    }
)

# Campo de email
email = Input(
    placeholder="tu@email.com",
    input_type="email",
    required=True,
    style={
        'width': '100%',
        'padding': '12px',
        'border': '2px solid #e1e5e9',
        'border-radius': '8px'
    }
)

# Campo de contraseña
password = Input(
    placeholder="Contraseña",
    input_type="password",
    required=True,
    min_length=8,
    style={
        'width': '100%',
        'padding': '12px',
        'border': '2px solid #e1e5e9',
        'border-radius': '8px'
    }
)

# Campo numérico
edad = Input(
    placeholder="Edad",
    input_type="number",
    style={
        'width': '100px',
        'padding': '8px',
        'border': '1px solid #ccc',
        'border-radius': '4px',
        'text-align': 'center'
    }
)

# Campo de búsqueda
busqueda = Input(
    placeholder="Buscar...",
    input_type="search",
    style={
        'width': '300px',
        'padding': '10px 15px',
        'border': '1px solid #ddd',
        'border-radius': '20px',
        'background-color': '#f8f9fa'
    }
)
```

### Container

El componente `Container` es un contenedor que puede albergar otros componentes.

#### Sintaxis

```python
from pywebui.components.basic.container import Container

contenedor = Container(
    children=[componente1, componente2],
    style={
        'display': 'flex',
        'flex-direction': 'column',
        'padding': '20px',
        'background-color': '#f8f9fa'
    }
)

# O agregar hijos después
contenedor.add_child(componente3)
```

#### Propiedades

| Propiedad | Tipo | Descripción |
|-----------|------|-------------|
| `children` | list | Lista de componentes hijos |

#### Layouts con Container

```python
# Layout vertical (columna)
columna = Container(
    style={
        'display': 'flex',
        'flex-direction': 'column',
        'gap': '15px',
        'padding': '20px'
    }
)

# Layout horizontal (fila)
fila = Container(
    style={
        'display': 'flex',
        'flex-direction': 'row',
        'gap': '20px',
        'align-items': 'center'
    }
)

# Layout centrado
centrado = Container(
    style={
        'display': 'flex',
        'justify-content': 'center',
        'align-items': 'center',
        'min-height': '100vh',
        'background-color': '#f0f2f5'
    }
)

# Card/Tarjeta
tarjeta = Container(
    style={
        'background-color': 'white',
        'border-radius': '12px',
        'padding': '24px',
        'box-shadow': '0 2px 10px rgba(0,0,0,0.1)',
        'max-width': '400px',
        'margin': '20px auto'
    }
)

# Sidebar
sidebar = Container(
    style={
        'width': '250px',
        'height': '100vh',
        'background-color': '#2c3e50',
        'padding': '20px',
        'position': 'fixed',
        'left': '0',
        'top': '0'
    }
)
```

## Sistema de Estilos

### Propiedades de Estilo Soportadas

Dars soporta la mayoría de propiedades CSS estándar:

#### Dimensiones
- `width`, `height`
- `min-width`, `min-height`
- `max-width`, `max-height`

#### Espaciado
- `margin`, `margin-top`, `margin-right`, `margin-bottom`, `margin-left`
- `padding`, `padding-top`, `padding-right`, `padding-bottom`, `padding-left`

#### Colores
- `background-color`
- `color`
- `border-color`

#### Tipografía
- `font-size`, `font-family`, `font-weight`, `font-style`
- `text-align`, `text-decoration`, `line-height`

#### Bordes
- `border`, `border-width`, `border-style`, `border-radius`

#### Layout
- `display`, `position`
- `top`, `right`, `bottom`, `left`, `z-index`

#### Flexbox
- `flex-direction`, `flex-wrap`
- `justify-content`, `align-items`, `align-content`
- `flex`, `flex-grow`, `flex-shrink`, `flex-basis`

#### Grid
- `grid-template-columns`, `grid-template-rows`
- `grid-gap`, `grid-column`, `grid-row`

#### Efectos
- `opacity`, `box-shadow`, `transform`, `transition`

### Ejemplos de Estilos Avanzados

```python
# Gradiente de fondo
gradiente = Container(
    style={
        'background': 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        'min-height': '100vh',
        'display': 'flex',
        'align-items': 'center',
        'justify-content': 'center'
    }
)

# Animación de hover (para web)
boton_animado = Button(
    text="Hover me",
    style={
        'background-color': '#3498db',
        'color': 'white',
        'padding': '15px 30px',
        'border': 'none',
        'border-radius': '8px',
        'transition': 'all 0.3s ease',
        'transform': 'translateY(0)',
        'box-shadow': '0 4px 15px rgba(52, 152, 219, 0.3)'
    }
)

# Layout de grid
grid_container = Container(
    style={
        'display': 'grid',
        'grid-template-columns': 'repeat(auto-fit, minmax(250px, 1fr))',
        'grid-gap': '20px',
        'padding': '20px'
    }
)

# Responsive design
responsive_container = Container(
    style={
        'width': '100%',
        'max-width': '1200px',
        'margin': '0 auto',
        'padding': '0 20px'
    }
)
```

## Eventos y Interactividad

Los componentes pueden responder a eventos del usuario:

```python
def manejar_click():
    print("Botón presionado")

def manejar_cambio(valor):
    print(f"Nuevo valor: {valor}")

boton = Button(
    text="Presionar",
    on_click=manejar_click
)

entrada = Input(
    placeholder="Escribe algo",
    on_change=manejar_cambio,
    on_focus=lambda: print("Campo enfocado"),
    on_blur=lambda: print("Campo desenfocado")
)
```

## Mejores Prácticas

### Organización de Componentes

```python
def crear_header():
    return Container(
        children=[
            Text("Mi Aplicación", style={'font-size': '24px', 'font-weight': 'bold'}),
            Text("Subtítulo descriptivo", style={'color': '#666'})
        ],
        style={
            'padding': '20px',
            'background-color': '#f8f9fa',
            'border-bottom': '1px solid #dee2e6'
        }
    )

def crear_formulario():
    return Container(
        children=[
            Text("Formulario de Contacto", style={'font-size': '20px', 'margin-bottom': '20px'}),
            Input(placeholder="Nombre", style={'margin-bottom': '10px'}),
            Input(placeholder="Email", input_type="email", style={'margin-bottom': '10px'}),
            Button("Enviar", style={'background-color': '#007bff', 'color': 'white'})
        ],
        style={
            'max-width': '400px',
            'margin': '20px auto',
            'padding': '20px'
        }
    )
```

### Reutilización de Estilos

```python
# Definir estilos comunes
ESTILOS_BOTON_BASE = {
    'padding': '10px 20px',
    'border': 'none',
    'border-radius': '4px',
    'font-size': '14px',
    'cursor': 'pointer'
}

ESTILOS_BOTON_PRIMARIO = {
    **ESTILOS_BOTON_BASE,
    'background-color': '#007bff',
    'color': 'white'
}

ESTILOS_BOTON_SECUNDARIO = {
    **ESTILOS_BOTON_BASE,
    'background-color': '#6c757d',
    'color': 'white'
}

# Usar en componentes
boton_guardar = Button("Guardar", style=ESTILOS_BOTON_PRIMARIO)
boton_cancelar = Button("Cancelar", style=ESTILOS_BOTON_SECUNDARIO)
```

Los componentes de Dars proporcionan una base sólida para crear interfaces de usuario modernas y responsivas que pueden exportarse a múltiples plataformas manteniendo consistencia y funcionalidad.

