# Plan de Implementación Final: Exportación a Desktop con Electron y Entorno de Desarrollo Adaptado

## 1. Principio Arquitectónico y Rol de Python

El principio se mantiene: **Python es la herramienta de *build* y desarrollo**, y la aplicación final es un *bundle* de Electron (HTML/CSS/JS + Bridge JS).

La novedad es la **adaptación del entorno de desarrollo** para el formato `desktop`, asegurando que `app.rTimeCompile()` y `dars dev` lancen una instancia de Electron que cargue la aplicación Dars.

## 2. Adaptación de la Clase `App` y la Configuración

Para gestionar el tipo de aplicación, se implementará la propiedad `desktop` en la clase `App`.

| Componente | Modificación | Rol |
| :--- | :--- | :--- |
| **`dars/core/app.py`** | Añadir el parámetro `desktop: bool = False` al constructor de `App`. | Permite al desarrollador definir explícitamente el tipo de aplicación. |
| **`dars/cli/main.py`** | La función `init` para `desktop` debe generar un `main.py` que incluya `app = App(..., desktop=True)`. | Configuración automática del proyecto. |
| **`dars/config.py`** | El formato `desktop` en `dars.config.json` debe ser el indicador principal, pero la CLI debe verificar la coherencia con `App.desktop`. | Fuente de verdad para el exportador. |

## 3. Plan de Implementación Detallado (Final)

El plan se expande a cinco fases, con la Fase 5 dedicada a la crucial adaptación del entorno de desarrollo.

### Fase 1: Preparación de la CLI y Estructura

| Paso | Descripción | Archivos a Modificar/Crear |
| :--- | :--- | :--- |
| **1.1. Extender `js_bridge`** | Añadir funciones para instalar paquetes globales de `npm`/`bun` y para ejecutar comandos de *build* de Electron. | `dars/core/js_bridge.py` |
| **1.2. Actualizar `doctor`** | Añadir la verificación para **Electron** y **electron-builder** (o `electron-packager`) como dependencias opcionales. Incluir la lógica de instalación a través del `js_bridge`. | `dars/cli/doctor/doctor.py`, `dars/cli/doctor/ui.py`, `dars/cli/doctor/installers.py` |
| **1.3. Actualizar `dars init`** | Implementar la lógica para `dars init --type desktop`. Generar un `main.py` con `App(..., desktop=True)` y la estructura de carpetas: `backend/` (para archivos de Electron), `main.py`, `lib/`, `public/`. | `dars/cli/main.py` (función `init`), `dars/templates/desktop/` |
| **1.4. Configuración de Formato** | Añadir `desktop` como un formato válido en `dars.config.json` y en la CLI. | `dars/config.py`, `dars/cli/main.py` |

### Fase 2: Definición de la API y Generación del Bridge

| Paso | Descripción | Archivos a Crear |
| :--- | :--- | :--- |
| **2.1. Definición de la API Python** | Crear el módulo Python con las clases y métodos que definen la API de escritorio (e.g., `FileSystem.read_file`). | `dars/desktop/api.py` |
| **2.2. Generador de Código JS** | Crear el generador que produce el código JavaScript necesario para el *Preload Script* y el *stub* de JS para el *runtime* de Dars. | `dars/desktop/js_generator.py` |
| **2.3. Plantillas de Electron** | Crear las plantillas base para los archivos de Electron. | `dars/templates/desktop/backend/package.json.template`, `dars/templates/desktop/backend/main.js.template`, `dars/templates/desktop/backend/preload.js.template` |

### Fase 3: Creación del `ElectronExporter`

| Paso | Descripción | Archivos a Modificar/Crear |
| :--- | :--- | :--- |
| **3.1. Crear `ElectronExporter`** | Implementar la clase `ElectronExporter` que herede de `Exporter`. El método `get_platform()` debe retornar `"desktop"`. | `dars/exporters/desktop/electron.py` |
| **3.2. Lógica de Exportación** | El método `export()` debe: <br> a) **Generar Frontend:** Llamar al `HTMLCSSJSExporter` para generar el HTML/CSS/JS de Dars en una subcarpeta (e.g., `dist/app/`). <br> b) **Generar Bridge:** Usar `dars/desktop/js_generator.py` para crear `preload.js` y el *stub* de JS. <br> c) **Generar Backend:** Rellenar las plantillas de `package.json` y `main.js` y copiarlas a la carpeta de salida. <br> d) **Instalar Dependencias:** Usar el `js_bridge` para ejecutar `bun install` en la carpeta de salida para instalar Electron y sus dependencias. | `dars/exporters/desktop/electron.py` |
| **3.3. Integración del Runtime** | Modificar el `HTMLCSSJSExporter` o el `App` para inyectar el *stub* de JS de la API de escritorio en el `index.html` generado, permitiendo que el código Dars acceda a `window.DarsDesktopAPI`. | `dars/exporters/web/html_css_js.py` (o un nuevo método en `App`) |
| **3.4. Registrar el Exportador** | Registrar el nuevo `ElectronExporter` en la CLI para que esté disponible con `format='desktop'`. | `dars/cli/main.py` (clase `DarsExporter`) |

### Fase 4: Build Nativo y Finalización

| Paso | Descripción | Archivos a Modificar |
| :--- | :--- | :--- |
| **4.1. Implementar el Build Nativo** | Añadir un paso final al `ElectronExporter.export()` que utilice el `js_bridge` para ejecutar el comando de *build* de Electron (e.g., `bun x electron-builder --dir`). Esto generará los ejecutables nativos. | `dars/exporters/desktop/electron.py` |
| **4.2. Documentación** | Crear documentación básica para el nuevo formato de exportación y el uso del `Desktop API`. | `dars/docs/` (archivos de ejemplo) |

### Fase 5: Adaptación del Entorno de Desarrollo (`rTimeCompile` / `dars dev`)

| Paso | Descripción | Archivos a Modificar |
| :--- | :--- | :--- |
| **5.1. Modificar `rTimeCompile()`** | Adaptar la lógica de `app.rTimeCompile()` para que, si `app.desktop` es `True` (o el formato es `desktop`): <br> a) Ejecute el `HTMLCSSJSExporter` en modo *dev* (sin minificación) a una carpeta temporal. <br> b) Lance el *Main Process* de Electron en modo desarrollo, apuntando a la carpeta temporal. <br> c) Use el `js_bridge` para ejecutar Electron (e.g., `bun x electron .` en la carpeta temporal). | `dars/core/app.py` (método `rTimeCompile`) |
| **5.2. Implementar Live Reload** | El *Main Process* de Electron en modo *dev* debe incluir lógica para detectar cambios en los archivos Dars generados (HTML/JS/CSS) y forzar un *reload* de la ventana. Esto se puede hacer con una dependencia JS como `electron-reload` o un *watcher* simple. | `dars/templates/desktop/backend/main.js.template` (solo en modo dev) |
| **5.3. Integración con `dars dev`** | Asegurar que el comando `dars dev` (que probablemente llama a `rTimeCompile`) use la nueva lógica de Electron. | `dars/cli/main.py` (comando `dev`) |

Este plan final cubre el ciclo de vida completo de la aplicación Dars en el formato `desktop`: desde la inicialización del proyecto, pasando por el desarrollo interactivo, hasta la exportación final.
