# Dars - Documentación de Componentes

## Introducción a los Componentes

Los componentes son los elementos fundamentales de Dars que representan elementos de la interfaz de usuario. Cada componente encapsula su apariencia, comportamiento y estado, permitiendo crear interfaces complejas mediante la composición de elementos simples.

## Clase Base Component

Todos los componentes en Dars heredan de la clase base `Component`, que proporciona la funcionalidad común:

```python
from dars.core.component import Component

class Component(ABC):
    def __init__(self, **props):
        self.props = props
        self.children = []
        self.parent = None
        self.id = props.get("id")
        self.class_name = props.get("class_name")
        self.style = props.get("style", {})
        self.events = {}
```

### Propiedades Comunes

Todos los componentes soportan estas propiedades básicas:

- **id**: Identificador único del componente
- **class_name**: Clase CSS para estilos adicionales
- **style**: Diccionario con estilos CSS
- **children**: Lista de componentes hijos (para contenedores)

## Componentes Básicos

## Page (root multipágina)

```python
from dars.components.basic import Page, Text, Button
from dars.scripts.script import InlineScript
page = Page(
    Text("Bienvenido!"),
    Button("Click aquí", id="btn-demo")
)
# Añadir script JS solo a esta página
page.add_script(InlineScript("""
document.addEventListener('DOMContentLoaded', function() {
    var btn = document.getElementById('btn-demo');
    if (btn) btn.onclick = () => alert('¡Botón de esta página!');
});
"""))
```

Usa `Page` como root de cada página en el sistema multipágina. Permite pasar hijos directamente como argumentos y scripts JS por página.

### Text

El componente `Text` muestra texto estático o dinámico.

#### Sintaxis

```python
from dars.components.basic.text import Text

texto = Text(
    text="Contenido del texto",
    id="mi-texto",
    class_name="texto-principal",
    style={
        "font-size": "16px",
        "color": "#333",
        "font-weight": "bold"
    }
)
```

#### Propiedades

| Propiedad | Tipo | Descripción | Ejemplo |
|-----------|------|-------------|---------|
| `text` | str | Contenido del texto | `"Hola mundo"` |
| `id` | str | Identificador único | `"titulo-principal"` |
| `class_name` | str | Clase CSS | `"texto-destacado"` |
| `style` | dict | Estilos CSS | `{"color": "red"}` |

#### Estilos Comunes

```python
# Título principal
titulo = Text(
    text="Título Principal",
    style={
        "font-size": "32px",
        "font-weight": "bold",
        "color": "#2c3e50",
        "margin-bottom": "20px",
        "text-align": "center"
    }
)

# Párrafo de contenido
parrafo = Text(
    text="Este es un párrafo de ejemplo con contenido descriptivo.",
    style={
        "font-size": "16px",
        "line-height": "1.6",
        "color": "#34495e",
        "margin-bottom": "15px"
    }
)

# Texto pequeño
nota = Text(
    text="Nota: Esta información es importante.",
    style={
        "font-size": "12px",
        "color": "#7f8c8d",
        "font-style": "italic"
    }
)
```

### Button

El componente `Button` crea botones interactivos que pueden ejecutar acciones.

#### Sintaxis

```python
from dars.components.basic.button import Button

boton = Button(
    text="Hacer clic",
    button_type="button",  # "button", "submit", "reset"
    disabled=False,
    # on_click=mi_funcion, # Los eventos se manejan con app.add_script o InlineScript
    style={
        "background-color": "#3498db",
        "color": "white",
        "padding": "10px 20px",
        "border": "none",
        "border-radius": "4px"
    }
)
```

#### Propiedades

| Propiedad | Tipo | Descripción | Valores |
|-----------|------|-------------|---------|
| `text` | str | Texto del botón | `"Enviar"` |
| `button_type` | str | Tipo de botón | `"button"`, `"submit"`, `"reset"` |
| `disabled` | bool | Si está deshabilitado | `True`, `False` |

#### Ejemplos de Botones

```python
# Botón primario
boton_primario = Button(
    text="Acción Principal",
    style={
        "background-color": "#007bff",
        "color": "white",
        "padding": "12px 24px",
        "border": "none",
        "border-radius": "6px",
        "font-size": "16px",
        "font-weight": "500",
        "cursor": "pointer",
        "transition": "background-color 0.3s"
    }
)

# Botón secundario
boton_secundario = Button(
    text="Cancelar",
    style={
        "background-color": "transparent",
        "color": "#6c757d",
        "padding": "12px 24px",
        "border": "1px solid #6c757d",
        "border-radius": "6px",
        "font-size": "16px",
        "cursor": "pointer"
    }
)

# Botón de peligro
boton_eliminar = Button(
    text="Eliminar",
    style={
        "background-color": "#dc3545",
        "color": "white",
        "padding": "8px 16px",
        "border": "none",
        "border-radius": "4px",
        "font-size": "14px"
    }
)

# Botón deshabilitado
boton_deshabilitado = Button(
    text="No disponible",
    disabled=True,
    style={
        "background-color": "#e9ecef",
        "color": "#6c757d",
        "padding": "10px 20px",
        "border": "none",
        "border-radius": "4px",
        "cursor": "not-allowed"
    }
)
```

### Input

El componente `Input` permite la entrada de datos del usuario.

#### Sintaxis

```python
from dars.components.basic.input import Input

entrada = Input(
    value="Valor inicial",
    placeholder="Escribe aquí...",
    input_type="text",  # "text", "password", "email", "number", etc.
    disabled=False,
    readonly=False,
    required=False,
    max_length=100,
    # on_change=mi_funcion_cambio, # Los eventos se manejan con app.add_script o InlineScript
    style={
        "width": "300px",
        "padding": "10px",
        "border": "1px solid #ddd",
        "border-radius": "4px"
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
        "width": "100%",
        "padding": "12px",
        "border": "2px solid #e1e5e9",
        "border-radius": "8px",
        "font-size": "16px"
    }
)

# Campo de email
email = Input(
    placeholder="tu@email.com",
    input_type="email",
    required=True,
    style={
        "width": "100%",
        "padding": "12px",
        "border": "2px solid #e1e5e9",
        "border-radius": "8px"
    }
)

# Campo de contraseña
password = Input(
    placeholder="Contraseña",
    input_type="password",
    required=True,
    min_length=8,
    style={
        "width": "100%",
        "padding": "12px",
        "border": "2px solid #e1e5e9",
        "border-radius": "8px"
    }
)

# Campo numérico
edad = Input(
    placeholder="Edad",
    input_type="number",
    style={
        "width": "100px",
        "padding": "8px",
        "border": "1px solid #ccc",
        "border-radius": "4px",
        "text-align": "center"
    }
)

# Campo de búsqueda
busqueda = Input(
    placeholder="Buscar...",
    input_type="search",
    style={
        "width": "300px",
        "padding": "10px 15px",
        "border": "1px solid #ddd",
        "border-radius": "20px",
        "background-color": "#f8f9fa"
    }
)
```

### Container

El componente `Container` es un contenedor que puede albergar otros componentes.

#### Sintaxis

```python
from dars.components.basic.container import Container

contenedor = Container(
    children=[componente1, componente2],
    style={
        "display": "flex",
        "flex-direction": "column",
        "padding": "20px",
        "background-color": "#f8f9fa"
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
        "display": "flex",
        "flex-direction": "column",
        "gap": "15px",
        "padding": "20px"
    }
)

# Layout horizontal (fila)
fila = Container(
    style={
        "display": "flex",
        "flex-direction": "row",
        "gap": "20px",
        "align-items": "center"
    }
)

# Layout centrado
centrado = Container(
    style={
        "display": "flex",
        "justify-content": "center",
        "align-items": "center",
        "min-height": "100vh",
        "background-color": "#f0f2f5"
    }
)

# Card/Tarjeta
tarjeta = Container(
    style={
        "background-color": "white",
        "border-radius": "12px",
        "padding": "24px",
        "box-shadow": "0 2px 10px rgba(0,0,0,0.1)",
        "max-width": "400px",
        "margin": "20px auto"
    }
)

# Sidebar
sidebar = Container(
    style={
        "width": "250px",
        "height": "100vh",
        "background-color": "#2c3e50",
        "padding": "20px",
        "position": "fixed",
        "left": "0",
        "top": "0"
    }
)
```

### Image

El componente `Image` muestra imágenes.

#### Sintaxis

```python
from dars.components.basic.image import Image

imagen = Image(
    src="path/to/your/image.jpg",
    alt="Descripción de la imagen",
    width="300px",
    height="200px",
    class_name="responsive-img",
    style={
        "border-radius": "8px",
        "box-shadow": "0 4px 8px rgba(0,0,0,0.1)"
    }
)
```

#### Propiedades

| Propiedad | Tipo | Descripción | Ejemplo |
|-----------|------|-------------|---------|
| `src` | str | Ruta de la imagen | `"images/logo.png"` |
| `alt` | str | Texto alternativo | `"Logo de la empresa"` |
| `width` | str | Ancho de la imagen (CSS) | `"100%"`, `"200px"` |
| `height` | str | Alto de la imagen (CSS) | `"auto"`, `"150px"` |

### Link

El componente `Link` crea enlaces de navegación.

#### Sintaxis

```python
from dars.components.basic.link import Link

enlace = Link(
    text="Visitar Google",
    href="https://www.google.com",
    target="_blank", # Abre en una nueva pestaña
    class_name="external-link",
    style={
        "color": "#007bff",
        "text-decoration": "none",
        "font-weight": "bold"
    }
)
```

#### Propiedades

| Propiedad | Tipo | Descripción | Valores |
|-----------|------|-------------|---------|
| `text` | str | Texto del enlace | `"Ir a la página"` |
| `href` | str | URL de destino | `"/about"`, `"https://example.com"` |
| `target` | str | Dónde abrir el enlace | `"_self"` (misma pestaña), `"_blank"` (nueva pestaña) |

### Textarea

El componente `Textarea` permite la entrada de texto multilínea.

#### Sintaxis

```python
from dars.components.basic.textarea import Textarea

area_texto = Textarea(
    value="Texto inicial",
    placeholder="Escribe tu mensaje aquí...",
    rows=5,
    cols=40,
    disabled=False,
    readonly=False,
    required=True,
    max_length=500,
    class_name="comment-box",
    style={
        "width": "100%",
        "padding": "10px",
        "border": "1px solid #ccc",
        "border-radius": "5px"
    }
)
```

#### Propiedades

| Propiedad | Tipo | Descripción | Valores |
|-----------|------|-------------|---------|
| `value` | str | Valor inicial | `""` |
| `placeholder` | str | Texto de ayuda | `"Escribe aquí..."` |
| `rows` | int | Número de filas visibles | `4` |
| `cols` | int | Número de columnas visibles | `50` |
| `disabled` | bool | Si está deshabilitado | `True`, `False` |
| `readonly` | bool | Solo lectura | `True`, `False` |
| `required` | bool | Campo obligatorio | `True`, `False` |
| `max_length` | int | Longitud máxima | `500` |

## Componentes Avanzados

### Card

El componente `Card` es un contenedor estilizado para agrupar contenido relacionado, como un título y otros componentes.

#### Sintaxis

```python
from dars.components.advanced.card import Card
from dars.components.basic.text import Text
from dars.components.basic.button import Button

mi_tarjeta = Card(
    title="Título de la Tarjeta",
    children=[
        Text("Este es el contenido de la tarjeta."),
        Button("Ver más")
    ],
    class_name="product-card",
    style={
        "background-color": "#ffffff",
        "border": "1px solid #e0e0e0",
        "border-radius": "10px",
        "padding": "20px",
        "box-shadow": "0 4px 8px rgba(0,0,0,0.05)"
    }
)
```

#### Propiedades

| Propiedad | Tipo | Descripción |
|-----------|------|-------------|
| `title` | str | Título de la tarjeta |
| `children` | list | Lista de componentes hijos |

### Modal

El componente `Modal` crea una ventana emergente que se superpone al contenido principal de la página.

#### Sintaxis

```python
from dars.components.advanced.modal import Modal
from dars.components.basic.text import Text
from dars.components.basic.button import Button

mi_modal = Modal(
    title="Bienvenido al Modal",
    is_open=True, # O False para que esté oculto inicialmente
    children=[
        Text("Este es el contenido de tu ventana modal."),
        Button("Cerrar")
    ],
    class_name="welcome-modal",
    style={
        "background-color": "rgba(0, 0, 0, 0.7)" # Estilo para el overlay
    }
)
```

#### Propiedades

| Propiedad | Tipo | Descripción |
|-----------|------|-------------|
| `title` | str | Título del modal |
| `is_open` | bool | Controla la visibilidad del modal (`True` para mostrar, `False` para ocultar) |
| `children` | list | Lista de componentes hijos (contenido del modal) |

### Navbar

El componente `Navbar` crea una barra de navegación, comúnmente utilizada en la parte superior de las páginas.

#### Sintaxis

```python
from dars.components.advanced.navbar import Navbar
from dars.components.basic.link import Link

mi_navbar = Navbar(
    brand="Mi App",
    children=[
        Link("Inicio", "/"),
        Link("Acerca de", "/about"),
        Link("Contacto", "/contact")
    ],
    class_name="main-nav",
    style={
        "background-color": "#333",
        "color": "white",
        "padding": "15px 20px"
    }
)
```

#### Propiedades

| Propiedad | Tipo | Descripción |
|-----------|------|-------------|
| `brand` | str | Texto o componente para la marca/logo de la navegación |
| `children` | list | Lista de componentes hijos (elementos de navegación, usualmente `Link`s) |

## Componentes Adicionales

### Checkbox

El componente `Checkbox` permite la selección de opciones.

#### Sintaxis

```python
from dars.components.basic.checkbox import Checkbox

mi_checkbox = Checkbox(
    label="Acepto términos",
    checked=True,
    style={
        "margin": "10px"
    }
)
```

#### Propiedades

| Propiedad | Tipo | Descripción | Valores |
|-----------|------|-------------|---------|
| `label` | str | Texto de la etiqueta | `"Acepto términos"` |
| `checked` | bool | Estado de selección | `True`, `False` |

### RadioButton

El componente `RadioButton` permite la selección de una opción entre varias.

#### Sintaxis

```python
from dars.components.basic.radio_button import RadioButton

mi_radio_button = RadioButton(
    label="Opción A",
    name="grupo1",
    checked=False,
    style={
        "margin": "10px"
    }
)
```

#### Propiedades

| Propiedad | Tipo | Descripción | Valores |
|-----------|------|-------------|---------|
| `label` | str | Texto de la etiqueta | `"Opción A"` |
| `name` | str | Nombre del grupo de radio buttons | `"grupo1"` |
| `checked` | bool | Estado de selección | `True`, `False` |

### Select

El componente `Select` permite la selección de una opción de un conjunto de opciones.

#### Sintaxis

```python
from dars.components.basic.select import Select

mi_select = Select(
    options=["Uno", "Dos", "Tres"],
    value="Dos",
    style={
        "width": "200px",
        "padding": "10px",
        "border": "1px solid #ccc"
    }
)
```

#### Propiedades

| Propiedad | Tipo | Descripción | Valores |
|-----------|------|-------------|---------|
| `options` | list | Lista de opciones | `["Uno", "Dos", "Tres"]` |
| `value` | str | Valor seleccionado | `"Dos"` |

### Slider

El componente `Slider` permite la selección de un valor dentro de un rango.

#### Sintaxis

```python
from dars.components.basic.slider import Slider

mi_slider = Slider(
    min_value=0,
    max_value=100,
    value=50,
    show_value=True,
    style={
        "width": "200px",
        "padding": "10px"
    }
)
```

#### Propiedades

| Propiedad | Tipo | Descripción | Valores |
|-----------|------|-------------|---------|
| `min_value` | int | Valor mínimo | `0` |
| `max_value` | int | Valor máximo | `100` |
| `value` | int | Valor seleccionado | `50` |
| `show_value` | bool | Mostrar el valor seleccionado | `True`, `False` |

### DatePicker

El componente `DatePicker` permite la selección de una fecha.

#### Sintaxis

```python
from dars.components.basic.date_picker import DatePicker

mi_date_picker = DatePicker(
    value="2025-08-06",
    style={
        "width": "200px",
        "padding": "10px",
        "border": "1px solid #ccc"
    }
)
```

#### Propiedades

| Propiedad | Tipo | Descripción | Valores |
|-----------|------|-------------|---------|
| `value` | str | Fecha seleccionada | `"2025-08-06"` |

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
        "background": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
        "min-height": "100vh",
        "display": "flex",
        "align-items": "center",
        "justify-content": "center"
    }
)

# Animación de hover (para web)
boton_animado = Button(
    text="Hover me",
    style={
        "background-color": "#3498db",
        "color": "white",
        "padding": "15px 30px",
        "border": "none",
        "border-radius": "8px",
        "transition": "all 0.3s ease",
        "transform": "translateY(0)",
        "box-shadow": "0 4px 15px rgba(52, 152, 219, 0.3)"
    }
)

# Layout de grid
grid_container = Container(
    style={
        "display": "grid",
        "grid-template-columns": "repeat(auto-fit, minmax(250px, 1fr))",
        "grid-gap": "20px",
        "padding": "20px"
    }
)

# Responsive design
responsive_container = Container(
    style={
        "width": "100%",
        "max-width": "1200px",
        "margin": "0 auto",
        "padding": "0 20px"
    }
)
```

## Eventos y Interactividad

Los componentes pueden responder a eventos del usuario. Para manejar eventos, debes usar `InlineScript` o `ExternalScript` para añadir lógica JavaScript que interactúe con los elementos HTML generados. Cada componente tiene un `id` único que puedes usar para seleccionarlo en JavaScript.

```python
from dars.core.app import App
from dars.components.basic.button import Button
from dars.components.basic.text import Text
from dars.scripts.script import InlineScript

app = App(title="App con Eventos")

# Crear un componente de texto para mostrar mensajes
message_text = Text("Esperando interacción...", id="status-message")

# Crear un botón
my_button = Button("Haz clic aquí", id="my-button")

# Añadir un script inline para manejar el evento en el frontend
frontend_script = InlineScript("""
document.getElementById("my-button").addEventListener("click", function() {
    alert("¡Evento de click detectado en el navegador!");
    document.getElementById("status-message").innerText = "¡Botón clickeado!";
});
""")

app.set_root(my_button) # O un contenedor que contenga ambos
app.add_child(message_text) # Asumiendo que App tiene un método add_child o similar para componentes fuera del root
app.add_script(frontend_script)
```

**Tipos de Eventos Comunes:**

Dars soporta una variedad de eventos estándar del navegador, como:

*   **Eventos de Mouse**: `click`, `dblclick`, `mousedown`, `mouseup`, `mouseenter`, `mouseleave`, `mousemove`.
*   **Eventos de Teclado**: `keydown`, `keyup`, `keypress`.
*   **Eventos de Formulario**: `change`, `input`, `submit`, `focus`, `blur`.
*   **Otros**: `load`, `error`, `resize`.

También puedes definir eventos personalizados.

## Mejores Prácticas

### Organización de Componentes

```python
def crear_header():
    return Container(
        children=[
            Text("Mi Aplicación", style={\"font-size\": \"24px\", \"font-weight\": \"bold\"}),
            Text("Subtítulo descriptivo", style={\"color\": \"#666\"})
        ],
        style={
            "padding": "20px",
            "background-color": "#f8f9fa",
            "border-bottom": "1px solid #dee2e6"
        }
    )

def crear_formulario():
    return Container(
        children=[
            Text("Formulario de Contacto", style={\"font-size\": \"20px\", \"margin-bottom\": \"20px\"}),
            Input(placeholder="Nombre", style={\"margin-bottom\": \"10px\"}),
            Input(placeholder="Email", input_type="email", style={\"margin-bottom\": \"10px\"}),
            Button("Enviar", style={\"background-color\": \"#007bff\", \"color\": \"white\"})
        ],
        style={
            "max-width": "400px",
            "margin": "20px auto",
            "padding": "20px"
        }
    )
```

### Reutilización de Estilos

```python
# Definir estilos comunes
ESTILOS_BOTON_BASE = {
    "padding": "10px 20px",
    "border": "none",
    "border-radius": "4px",
    "font-size": "14px",
    "cursor": "pointer"
}

ESTILOS_BOTON_PRIMARIO = {
    **ESTILOS_BOTON_BASE,
    "background-color": "#007bff",
    "color": "white"
}

ESTILOS_BOTON_SECUNDARIO = {
    **ESTILOS_BOTON_BASE,
    "background-color": "#6c757d",
    "color": "white"
}

# Usar en componentes
boton_guardar = Button("Guardar", style=ESTILOS_BOTON_PRIMARIO)
boton_cancelar = Button("Cancelar", style=ESTILOS_BOTON_SECUNDARIO)
```

Los componentes de Dars proporcionan una base sólida para crear interfaces de usuario modernas y responsivas que pueden exportarse a múltiples plataformas manteniendo consistencia y funcionalidad.


