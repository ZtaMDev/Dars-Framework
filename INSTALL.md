# Guía de Instalación - Dars Framework

## 📋 Requisitos del Sistema

### Requisitos Mínimos

- **Python**: 3.8 o superior
- **Sistema Operativo**: Windows, macOS, Linux
- **RAM**: 512 MB mínimo (2 GB recomendado)
- **Espacio en Disco**: 100 MB para el framework

### Dependencias de Python

```bash
pip install rich
```

## 🚀 Instalación Rápida

### Opción 1: Descarga Directa

1. Descarga el framework Dars completo
2. Extrae el archivo en tu directorio de trabajo
3. ¡Listo para usar!

### Opción 2: Clonar Repositorio

```bash
git clone <repositorio-pywebui>
cd pywebui-framework
```

## 🔧 Configuración del Entorno

### Estructura Recomendada

```
mi_proyecto/
├── pywebui/                 # Framework Dars
│   ├── core/
│   ├── components/
│   ├── exporters/
│   └── ...
├── mi_app.py               # Tu aplicación
├── scripts/                # Scripts JavaScript (opcional)
└── assets/                 # Recursos (opcional)
```

### Configuración en tu Proyecto

En cada archivo de aplicación, agrega al inicio:

```python
import sys
import os

# Configurar path para Dars
framework_path = os.path.join(os.path.dirname(__file__), 'pywebui')
sys.path.insert(0, framework_path)

# Ahora puedes importar Dars
from pywebui.core.app import App
from pywebui.components.basic.text import Text
# ... otros imports
```

## 🛠️ Configuración del CLI

### Hacer Ejecutable el Exportador

#### En Linux/macOS:

```bash
chmod +x pywebui_exporter
```

#### En Windows:

El archivo ya es ejecutable con Python:

```cmd
python pywebui_exporter
```

### Agregar al PATH (Opcional)

#### Linux/macOS:

```bash
# Agregar al ~/.bashrc o ~/.zshrc
export PATH="$PATH:/ruta/a/pywebui-framework"
```

#### Windows:

1. Abrir "Variables de entorno"
2. Agregar la ruta del framework al PATH
3. Reiniciar terminal

## ✅ Verificación de Instalación

### Prueba Básica

```bash
# Verificar que el CLI funciona
./pywebui_exporter --help

# Verificar formatos disponibles
./pywebui_exporter formats
```

### Prueba con Ejemplo

```bash
# Probar con ejemplo básico
./pywebui_exporter info examples/basic/hello_world.py

# Exportar ejemplo
./pywebui_exporter export examples/basic/hello_world.py --format html --output ./test_output

# Previsualizar
python3 pywebui/cli/preview.py ./test_output
```

## 🎯 Configuración por Plataforma de Exportación

### Para Exportación Web (HTML/React)

No requiere configuración adicional.

### Para React Native

```bash
# Instalar Node.js y npm
# Instalar React Native CLI
npm install -g react-native-cli

# Configurar entorno de desarrollo Android/iOS
# (Seguir guía oficial de React Native)
```

### Para PySide6

```bash
pip install PySide6
```

### Para C#

- Instalar .NET 6.0 o superior
- Visual Studio o Visual Studio Code (opcional)

### Para Kotlin Multiplatform

- Instalar JDK 11 o superior
- Android Studio (para desarrollo Android)
- Xcode (para desarrollo iOS, solo macOS)

## 🔍 Solución de Problemas de Instalación

### Error: "No module named 'pywebui'"

**Solución:**

```python
# Verificar que el path esté configurado correctamente
import sys
import os
framework_path = os.path.join(os.path.dirname(__file__), 'pywebui')
sys.path.insert(0, framework_path)
```

### Error: "rich module not found"

**Solución:**

```bash
pip install rich
```

### Error: "Permission denied" en Linux/macOS

**Solución:**

```bash
chmod +x pywebui_exporter
```

### Error: CLI no funciona en Windows

**Solución:**

```cmd
python pywebui_exporter --help
```

## 🌟 Configuración Avanzada

### Variables de Entorno

```bash
# Opcional: Configurar directorio de templates personalizados
export PYWEBUI_TEMPLATES_PATH="/ruta/a/mis/templates"

# Opcional: Configurar directorio de salida por defecto
export PYWEBUI_OUTPUT_PATH="/ruta/a/salida/por/defecto"
```

### Configuración de Desarrollo

Para desarrollo del framework:

```bash
# Instalar dependencias de desarrollo
pip install -r requirements-dev.txt  # Si existe

# Configurar pre-commit hooks
pre-commit install  # Si se usa pre-commit
```

## 📦 Instalación en Entornos Específicos

### Docker

```dockerfile
FROM python:3.9

# Instalar dependencias
RUN pip install rich

# Copiar framework
COPY pywebui /app/pywebui
COPY pywebui_exporter /app/

WORKDIR /app

# Hacer ejecutable
RUN chmod +x pywebui_exporter
```

### Virtual Environment

```bash
# Crear entorno virtual
python -m venv pywebui_env

# Activar entorno
source pywebui_env/bin/activate  # Linux/macOS
# o
pywebui_env\Scripts\activate     # Windows

# Instalar dependencias
pip install rich

# Usar Dars normalmente
```

### Conda

```bash
# Crear entorno conda
conda create -n pywebui python=3.9

# Activar entorno
conda activate pywebui

# Instalar dependencias
pip install rich
```

## 🚀 Primeros Pasos Después de la Instalación

### 1. Crear tu Primera Aplicación

```python
# mi_primera_app.py
import sys
import os

framework_path = os.path.join(os.path.dirname(__file__), 'pywebui')
sys.path.insert(0, framework_path)

from pywebui.core.app import App
from pywebui.components.basic.text import Text
from pywebui.components.basic.container import Container

app = App(title="Mi Primera App")
container = Container(style={'padding': '20px'})
texto = Text(text="¡Hola Dars!", style={'font-size': '24px'})

container.add_child(texto)
app.set_root(container)
```

### 2. Exportar la Aplicación

```bash
./pywebui_exporter export mi_primera_app.py --format html --output ./mi_app
```

### 3. Previsualizar

```bash
python3 pywebui/cli/preview.py ./mi_app
```

## 📚 Recursos Adicionales

### Documentación

- [README Principal](README.md)
- [Guía de Inicio Rápido](pywebui/docs/getting_started.md)
- [Documentación de Componentes](pywebui/docs/components.md)
- [Sistema de Scripts](pywebui/docs/scripts.md)
- [Guía de Exportadores](pywebui/docs/exporters.md)

### Ejemplos

- [Ejemplos Básicos](examples/basic/)
- [Ejemplos Avanzados](examples/advanced/)
- [Aplicación de Demostración](examples/demo/)

### Comandos Útiles

```bash
# Ayuda general
./pywebui_exporter --help

# Información de aplicación
./pywebui_exporter info mi_app.py

# Formatos disponibles
./pywebui_exporter formats

# Preview de aplicación
python3 pywebui/cli/preview.py ./output_directory
```

## ✅ Lista de Verificación Post-Instalación

- [ ] Python 3.8+ instalado
- [ ] Dependencia `rich` instalada
- [ ] Framework Dars descargado/clonado
- [ ] CLI ejecutable configurado
- [ ] Prueba básica realizada exitosamente
- [ ] Ejemplo exportado y previsualizando correctamente
- [ ] Documentación revisada

¡Felicidades! Dars está listo para usar. 🎉

---

**Siguiente paso:** [Guía de Inicio Rápido](pywebui/docs/getting_started.md)

