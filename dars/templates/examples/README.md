# Dars - Ejemplos

Esta carpeta contiene ejemplos que demuestran las capacidades del framework Dars.

## Estructura de Ejemplos

### Básicos (`basic/`)

Ejemplos simples que muestran conceptos fundamentales:

#### `hello_world.py`
- **Descripción**: Aplicación básica con texto y botón
- **Conceptos**: Componentes básicos, estilos, scripts simples
- **Exportar**: `dars export examples/basic/hello_world.py --format html --output ./hello_world_output`

#### `simple_form.py`
- **Descripción**: Formulario de contacto con validación
- **Conceptos**: Inputs, validación, manejo de eventos
- **Exportar**: `dars export examples/basic/simple_form.py --format html --output ./form_output`

#### `form_components.py` ⭐ **NUEVO 2024**
- **Descripción**: Template oficial con todos los nuevos componentes de formulario
- **Conceptos**: Checkbox, RadioButton, Select, Slider, DatePicker, interactividad
- **Inicializar**: `dars init mi_formulario -t basic/form_components`
- **Exportar**: `dars export mi_formulario.py --format html --output ./mi_formulario`
- **Incluye**: Ejemplos interactivos de todos los componentes nuevos con JavaScript

## Ejemplos Multipágina

Los ejemplos multipágina ahora usan el componente `Page` como root de cada página y permiten añadir scripts por página:

```python
from dars.components.basic import Page, Text, Button
from dars.scripts.script import InlineScript
home = Page(
    Text("Bienvenido!"),
    Button("Ir a About", id="btn-about")
)
home.add_script(InlineScript("""
document.addEventListener('DOMContentLoaded', function() {
    var btn = document.getElementById('btn-about');
    if (btn) btn.onclick = () => window.location.href = 'about.html';
});
"""))
```

Los scripts globales añadidos a la App se combinan automáticamente con los de cada página al exportar.

### Avanzados (`advanced/`)

Ejemplos que demuestran características más complejas:

#### `dashboard.py`
- **Descripción**: Dashboard empresarial con navegación y estadísticas
- **Conceptos**: Layouts complejos, navegación, datos dinámicos
- **Exportar**: `dars export examples/advanced/dashboard.py --format html --output ./dashboard_output`

#### `modern_web_app.py` ⭐ **NUEVO 2024**
- **Descripción**: Template oficial de aplicación web moderna con todas las características avanzadas
- **Conceptos**: SEO completo, Open Graph, Twitter Cards, PWA, favicon, nuevos componentes
- **Inicializar**: `dars init mi_app_moderna -t advanced/modern_web_app`
- **Exportar**: `dars export mi_app_moderna.py --format html --output ./mi_app_moderna`
- **Incluye**: 
  - Meta tags SEO completos
  - Open Graph para redes sociales
  - Twitter Cards optimizadas
  - Progressive Web App (PWA) con manifest
  - Favicon y iconos multi-dispositivo
  - Todos los nuevos componentes de formulario
  - JavaScript interactivo y PWA installation

### Demostración (`demo/`)

Aplicación completa que muestra todas las características:

#### `complete_app.py`
- **Descripción**: Aplicación de demostración completa con todas las características
- **Conceptos**: Todos los conceptos del framework
- **Exportar**: `dars export examples/demo/complete_app.py --format html --output ./demo_output`

## Cómo Usar los Ejemplos

### 1. Inicializar Proyecto con Template

```bash
# Template básico con nuevos componentes
dars init mi_proyecto -t basic/form_components

# Template avanzado con SEO, PWA y Open Graph
dars init mi_app_moderna -t advanced/modern_web_app

# También funciona la forma corta
dars init mi_proyecto -t basic/form_components
```

### 2. Información de la Aplicación

```bash
dars info mi_proyecto.py
```

### 3. Exportar a HTML

```bash
dars export mi_proyecto.py --format html --output ./mi_proyecto_web
```

### 3. Exportar a React

```bash
dars export examples/basic/hello_world.py --format react --output ./react_app
```

### 4. Exportar a PySide6

```bash
dars export examples/basic/hello_world.py --format pyside6 --output ./desktop_app
```

### 5. Previsualizar

```bash
# Para aplicaciones HTML
python3 pywebui/cli/preview.py ./output

# Para aplicaciones React
cd ./react_app
npm install
npm start
```

## Formatos Soportados

- **html**: HTML/CSS/JavaScript estándar
- **react**: Aplicación React
- **react-native**: Aplicación React Native
- **pyside6**: Aplicación de escritorio PySide6
- **csharp**: Aplicación C# WinForms
- **kotlin**: Aplicación Kotlin Multiplatform

## Comandos Útiles

### Ver Formatos Disponibles

```bash
dars formats
```

### Ayuda del CLI

```bash
dars --help
```

### Información Detallada

```bash
dars info <archivo.py>
```

## Estructura de un Ejemplo Típico

```python
#!/usr/bin/env python3
import sys
import os

# Configurar path para importar Dars
framework_path = os.path.join(os.path.dirname(__file__), '..', '..')
sys.path.insert(0, framework_path)

from pywebui.core.app import App
from pywebui.components.basic.text import Text
from pywebui.components.basic.button import Button
from pywebui.components.basic.container import Container
from pywebui.scripts.script import InlineScript

# Crear aplicación
app = App(title="Mi Aplicación")

# Crear componentes
container = Container(style={'padding': '20px'})
texto = Text(text="¡Hola Dars!", style={'font-size': '24px'})
boton = Button(text="Hacer clic", style={'background-color': '#007bff'})

# Script para interactividad
script = InlineScript(\"\"\"
document.addEventListener('DOMContentLoaded', function() {
    // Tu código JavaScript aquí
});
\"\"\")

# Ensamblar aplicación
container.add_child(texto)
container.add_child(boton)
app.set_root(container)
app.add_script(script)
```

## Mejores Prácticas

1. **Organización**: Mantén los componentes organizados en contenedores lógicos
2. **Estilos**: Usa estilos consistentes y reutilizables
3. **Scripts**: Separa la lógica en funciones claras
4. **Validación**: Siempre valida los datos de entrada del usuario
5. **Responsive**: Considera diferentes tamaños de pantalla
6. **Accesibilidad**: Usa IDs y clases descriptivas

## Solución de Problemas

### Error de Importación

Si obtienes errores de importación, asegúrate de que el path al framework esté configurado correctamente:

```python
framework_path = os.path.join(os.path.dirname(__file__), '..', '..')
sys.path.insert(0, framework_path)
```

### Error de Exportación

Verifica que la variable `app` esté definida en tu archivo:

```python
app = App(title="Mi Aplicación")
# ... resto del código
```

### Problemas de Preview

Para aplicaciones HTML, usa el sistema de preview integrado:

```bash
python3 dars preview ./output_directory
```

¡Explora los ejemplos y experimenta con diferentes combinaciones de componentes y estilos!

