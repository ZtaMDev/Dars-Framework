# Guía de Instalación - Dars Framework

## 📋 Requisitos del Sistema

### Requisitos Mínimos

- **Python**: 3.8 o superior
- **Sistema Operativo**: Windows, macOS, Linux
- **RAM**: 512 MB mínimo (2 GB recomendado)
- **Espacio en Disco**: 100 MB para el framework

## 🚀 Instalación Rápida

Para instalar Dars, simplemente usa pip:

```bash
pip install dars-framework
```

Esto instalará Dars y todas sus dependencias automáticamente.

## 🛠️ Uso del CLI

Una vez instalado, el comando `dars` estará disponible en tu terminal. Puedes usarlo para:

### Exportar Aplicaciones

```bash
dars export mi_app.py --format html --output ./mi_app_web
```

### Previsualizar Aplicaciones

```bash
dars preview ./mi_app_web
```

### Inicializar un Nuevo Proyecto

```bash
# Proyecto básico con Hello World
dars init mi_nuevo_proyecto

# Proyecto con una plantilla específica
dars init mi_nuevo_proyecto -t demo/complete_app
```

### Ver Información de una Aplicación

```bash
dars info mi_app.py
```

### Ver Formatos Soportados

```bash
dars formats
```

## ✅ Verificación de Instalación

Para verificar que Dars se ha instalado correctamente, abre tu terminal y ejecuta:

```bash
dars --help
```

Deberías ver la ayuda del comando `dars`, lo que indica que la instalación fue exitosa.

## 🚀 Primeros Pasos Después de la Instalación

### 1. Crear tu Primera Aplicación (mi_primera_app.py)

```python
from dars.core.app import App
from dars.components.basic.text import Text
from dars.components.basic.container import Container

app = App(title="Mi Primera App")
container = Container(style={\'padding\': \'20px\'}) # Usar \' para escapar comillas
texto = Text(text="¡Hola Dars!", style={\'font-size\': \'24px\'}) # Usar \' para escapar comillas

container.add_child(texto)
app.set_root(container)
```

### 2. Exportar la Aplicación

Guarda el código anterior como `mi_primera_app.py` y luego ejecuta:

```bash
dars export mi_primera_app.py --format html --output ./mi_app
```

### 3. Previsualizar

```bash
dars preview ./mi_app
```

## 📚 Recursos Adicionales

### Documentación

- [README Principal](../README.md)
- [Guía de Inicio Rápido](../dars/docs/getting_started.md)
- [Documentación de Componentes](../dars/docs/components.md)
- [Sistema de Scripts](../dars/docs/scripts.md)
- [Guía de Exportadores](../dars/docs/exporters.md)

### Ejemplos

- [Ejemplos Básicos](../dars/templates/examples/basic/)
- [Ejemplos Avanzados](../dars/templates/examples/advanced/)
- [Aplicación de Demostración](../dars/templates/examples/demo/)

### Comandos Útiles

```bash
# Ayuda general
dars --help

# Información de aplicación
dars info mi_app.py

# Formatos disponibles
dars formats

# Preview de aplicación
dars preview ./output_directory
```

## ✅ Lista de Verificación Post-Instalación

- [x] Python 3.8+ instalado
- [x] Dars Framework instalado vía `pip install dars-framework`
- [x] CLI `dars` funciona correctamente (`dars --help`)
- [x] Prueba básica realizada exitosamente
- [x] Ejemplo exportado y previsualizando correctamente
- [x] Documentación revisada

¡Felicidades! Dars está listo para usar. 🎉

---

**Siguiente paso:** [Guía de Inicio Rápido](../dars/docs/getting_started.md)




