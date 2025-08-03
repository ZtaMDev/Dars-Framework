# Dars - Documentación de Exportadores

## Introducción

Los exportadores son el corazón de Dars que permiten transformar aplicaciones escritas en Python a diferentes tecnologías y plataformas. Cada exportador traduce los componentes, estilos y scripts de Dars al código nativo de la plataforma objetivo.

## Arquitectura de Exportadores

### Clase Base Exporter

Todos los exportadores heredan de la clase base `Exporter`:

```python
from abc import ABC, abstractmethod

class Exporter(ABC):
    def __init__(self):
        self.templates_path = "templates/"
        
    @abstractmethod
    def export(self, app: App, output_path: str) -> bool:
        """Exporta la aplicación al formato específico"""
        pass
        
    @abstractmethod
    def render_component(self, component: Component) -> str:
        """Renderiza un componente individual"""
        pass
        
    @abstractmethod
    def get_platform(self) -> str:
        """Retorna el nombre de la plataforma"""
        pass
```

### Flujo de Exportación

1. **Validación**: Verificar que la aplicación sea válida
2. **Preparación**: Crear estructura de directorios
3. **Renderizado**: Convertir componentes al formato objetivo
4. **Generación**: Crear archivos de configuración y dependencias
5. **Finalización**: Escribir archivos al sistema

## Exportadores Web

### HTML/CSS/JavaScript

El exportador HTML genera aplicaciones web estándar que pueden ejecutarse en cualquier navegador.

#### Características

- **Compatibilidad**: Funciona en todos los navegadores modernos
- **Simplicidad**: No requiere herramientas de build
- **Performance**: Carga rápida y ejecución eficiente
- **SEO**: Contenido indexable por motores de búsqueda

#### Uso

```bash
./pywebui_exporter export mi_app.py --format html --output ./dist
```

#### Estructura Generada

```
dist/
├── index.html      # Página principal
├── styles.css      # Estilos CSS
└── script.js       # Lógica JavaScript
```

#### Ejemplo de Salida

**index.html**
```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Mi Aplicación</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <div id="container_123" class="pywebui-container" style="display: flex; flex-direction: column; padding: 20px;">
        <span id="text_456" class="pywebui-text" style="font-size: 24px; color: #333;">¡Hola Dars!</span>
        <button id="button_789" class="pywebui-button" style="background-color: #007bff; color: white;">Hacer clic</button>
    </div>
    <script src="script.js"></script>
</body>
</html>
```

**styles.css**
```css
/* Estilos base */
* {
    box-sizing: border-box;
}

body {
    margin: 0;
    padding: 0;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
}

.pywebui-button {
    display: inline-block;
    padding: 8px 16px;
    border: 1px solid #ccc;
    background-color: #f8f9fa;
    color: #333;
    cursor: pointer;
    border-radius: 4px;
    font-size: 14px;
}

.pywebui-button:hover {
    background-color: #e9ecef;
}
```

#### Ventajas

- **Universalidad**: Funciona en cualquier servidor web
- **Debugging**: Fácil de depurar con herramientas del navegador
- **Personalización**: CSS y JavaScript completamente modificables
- **Hosting**: Puede alojarse en cualquier servicio de hosting estático

#### Casos de Uso

- Sitios web corporativos
- Landing pages
- Aplicaciones web simples
- Prototipos rápidos
- Documentación interactiva

### React

El exportador React genera aplicaciones modernas usando la biblioteca React.

#### Características

- **Componentes**: Arquitectura basada en componentes reutilizables
- **Estado**: Manejo de estado reactivo
- **Ecosistema**: Acceso al vasto ecosistema de React
- **Performance**: Virtual DOM para renderizado eficiente

#### Uso

```bash
./pywebui_exporter export mi_app.py --format react --output ./mi-react-app
```

#### Estructura Generada

```
mi-react-app/
├── package.json
├── public/
│   └── index.html
└── src/
    ├── App.js
    ├── App.css
    └── index.js
```

#### Ejemplo de Salida

**App.js**
```jsx
import React from 'react';
import './App.css';

function App() {
  const scriptFunction0 = () => {
    alert('¡Hola desde Dars!');
  };

  return (
    <div className="App">
      <div id="container_123" className="pywebui-container" style={{display: "flex", flexDirection: "column", padding: "20px"}}>
        <span id="text_456" className="pywebui-text" style={{fontSize: "24px", color: "#333"}}>¡Hola Dars!</span>
        <button id="button_789" className="pywebui-button" onClick={scriptFunction0} style={{backgroundColor: "#007bff", color: "white"}}>Hacer clic</button>
      </div>
    </div>
  );
}

export default App;
```

**package.json**
```json
{
  "name": "mi-aplicacion",
  "version": "0.1.0",
  "private": true,
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-scripts": "5.0.1"
  },
  "scripts": {
    "start": "react-scripts start",
    "build": "react-scripts build",
    "test": "react-scripts test",
    "eject": "react-scripts eject"
  }
}
```

#### Desarrollo y Despliegue

```bash
# Instalar dependencias
cd mi-react-app
npm install

# Desarrollo
npm start

# Build para producción
npm run build
```

#### Ventajas

- **Modularidad**: Componentes reutilizables
- **Herramientas**: Excelente tooling y debugging
- **Comunidad**: Gran comunidad y recursos
- **Performance**: Optimizaciones automáticas

#### Casos de Uso

- Aplicaciones web complejas
- Dashboards interactivos
- SPAs (Single Page Applications)
- Aplicaciones empresariales

### React Native

El exportador React Native genera aplicaciones móviles nativas para iOS y Android.

#### Características

- **Nativo**: Rendimiento nativo en dispositivos móviles
- **Multiplataforma**: Un código para iOS y Android
- **Componentes**: UI components nativos
- **APIs**: Acceso a APIs nativas del dispositivo

#### Uso

```bash
./pywebui_exporter export mi_app.py --format react-native --output ./mi-app-mobile
```

#### Estructura Generada

```
mi-app-mobile/
├── package.json
├── metro.config.js
├── App.js
├── styles.js
└── index.js
```

#### Ejemplo de Salida

**App.js**
```jsx
import React from 'react';
import {
  SafeAreaView,
  ScrollView,
  StatusBar,
  Text,
  View,
  TouchableOpacity,
} from 'react-native';
import styles from './styles';

const App = () => {
  const scriptFunction0 = () => {
    console.log('¡Hola desde Dars!');
  };

  return (
    <SafeAreaView style={styles.container}>
      <StatusBar barStyle="dark-content" />
      <ScrollView contentInsetAdjustmentBehavior="automatic">
        <View style={styles.container}>
          <Text style={styles.text}>¡Hola Dars!</Text>
          <TouchableOpacity style={styles.button} onPress={scriptFunction0}>
            <Text style={styles.buttonText}>Hacer clic</Text>
          </TouchableOpacity>
        </View>
      </ScrollView>
    </SafeAreaView>
  );
};

export default App;
```

**styles.js**
```javascript
import { StyleSheet } from 'react-native';

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
  },
  text: {
    fontSize: 24,
    color: '#333',
    textAlign: 'center',
    margin: 20,
  },
  button: {
    backgroundColor: '#007bff',
    padding: 12,
    borderRadius: 8,
    alignItems: 'center',
    margin: 20,
  },
  buttonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: 'bold',
  },
});

export default styles;
```

#### Desarrollo y Despliegue

```bash
# Instalar dependencias
cd mi-app-mobile
npm install

# Ejecutar en Android
npm run android

# Ejecutar en iOS (solo macOS)
npm run ios

# Iniciar Metro bundler
npm start
```

#### Ventajas

- **Performance**: Rendimiento nativo
- **Experiencia**: UX nativa en cada plataforma
- **Desarrollo**: Hot reloading para desarrollo rápido
- **Distribución**: Publicación en app stores

#### Casos de Uso

- Aplicaciones móviles empresariales
- Apps de productividad
- Aplicaciones de comercio electrónico
- Herramientas de campo

## Exportadores Nativos

### PySide6 (Qt)

El exportador PySide6 genera aplicaciones de escritorio usando Qt for Python.

#### Características

- **Nativo**: Aplicaciones de escritorio nativas
- **Multiplataforma**: Windows, macOS, Linux
- **Rico en características**: Widgets avanzados y APIs del sistema
- **Performance**: Excelente rendimiento

#### Uso

```bash
./pywebui_exporter export mi_app.py --format pyside6 --output ./mi-app-desktop
```

#### Estructura Generada

```
mi-app-desktop/
├── main.py
├── main_window.py
├── styles.py
└── requirements.txt
```

#### Ejemplo de Salida

**main.py**
```python
#!/usr/bin/env python3
import sys
from PySide6.QtWidgets import QApplication
from main_window import MainWindow

def main():
    app = QApplication(sys.argv)
    
    app.setApplicationName("Mi Aplicación")
    app.setApplicationVersion("1.0.0")
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
```

**main_window.py**
```python
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, 
    QLabel, QPushButton
)
from PySide6.QtCore import Qt
from styles import Styles

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mi Aplicación")
        self.setGeometry(100, 100, 800, 600)
        
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        self.main_layout = QVBoxLayout(self.central_widget)
        
        self.setup_ui()
        self.apply_styles()
        
    def setup_ui(self):
        # Componente Text
        text_456 = QLabel("¡Hola Dars!")
        text_456.setStyleSheet("font-size: 24px; color: #333")
        self.main_layout.addWidget(text_456)
        
        # Componente Button
        button_789 = QPushButton("Hacer clic")
        button_789.setStyleSheet("background-color: #007bff; color: white")
        self.main_layout.addWidget(button_789)
        
    def apply_styles(self):
        self.setStyleSheet(Styles.get_main_stylesheet())
```

#### Desarrollo y Ejecución

```bash
# Instalar dependencias
cd mi-app-desktop
pip install -r requirements.txt

# Ejecutar aplicación
python main.py
```

#### Ventajas

- **Integración**: Integración completa con el sistema operativo
- **Widgets**: Amplia gama de widgets nativos
- **APIs**: Acceso a APIs del sistema
- **Distribución**: Empaquetado como ejecutables

#### Casos de Uso

- Herramientas de desarrollo
- Aplicaciones empresariales
- Software de productividad
- Utilidades del sistema

### C# WinForms

El exportador C# genera aplicaciones de escritorio para Windows usando WinForms.

#### Características

- **Windows nativo**: Integración completa con Windows
- **Familiar**: Interfaz familiar para usuarios de Windows
- **Performance**: Excelente rendimiento en Windows
- **.NET**: Acceso al ecosistema .NET

#### Uso

```bash
./pywebui_exporter export mi_app.py --format csharp --output ./mi-app-windows
```

#### Estructura Generada

```
mi-app-windows/
├── MiAplicacion.csproj
├── Program.cs
├── MainForm.cs
└── MainForm.Designer.cs
```

#### Ejemplo de Salida

**Program.cs**
```csharp
using System;
using System.Windows.Forms;

namespace MiAplicacion
{
    internal static class Program
    {
        [STAThread]
        static void Main()
        {
            Application.EnableVisualStyles();
            Application.SetCompatibleTextRenderingDefault(false);
            Application.Run(new MainForm());
        }
    }
}
```

**MainForm.cs**
```csharp
using System;
using System.Drawing;
using System.Windows.Forms;

namespace MiAplicacion
{
    public partial class MainForm : Form
    {
        public MainForm()
        {
            InitializeComponent();
            SetupEventHandlers();
        }
        
        private void SetupEventHandlers()
        {
            // Configurar manejadores de eventos
        }
        
        private void ScriptFunction0()
        {
            MessageBox.Show("¡Hola desde Dars!", "Dars");
        }
    }
}
```

#### Desarrollo y Compilación

```bash
# Restaurar dependencias
cd mi-app-windows
dotnet restore

# Compilar
dotnet build

# Ejecutar
dotnet run
```

#### Ventajas

- **Nativo Windows**: Máxima integración con Windows
- **Herramientas**: Excelente tooling con Visual Studio
- **Ecosistema**: Acceso completo al ecosistema .NET
- **Distribución**: Fácil distribución en Windows

#### Casos de Uso

- Aplicaciones empresariales Windows
- Herramientas administrativas
- Software de gestión
- Utilidades específicas de Windows

### Kotlin Multiplatform

El exportador Kotlin genera aplicaciones multiplataforma usando Kotlin Multiplatform Compose.

#### Características

- **Multiplataforma**: Android, iOS, Desktop, Web
- **Moderno**: Sintaxis moderna y concisa
- **Performance**: Compilación nativa
- **Jetpack Compose**: UI declarativa moderna

#### Uso

```bash
./pywebui_exporter export mi_app.py --format kotlin --output ./mi-app-multiplatform
```

#### Estructura Generada

```
mi-app-multiplatform/
├── build.gradle.kts
├── settings.gradle.kts
└── src/
    ├── commonMain/kotlin/
    │   ├── App.kt
    │   └── MainView.kt
    └── androidMain/kotlin/
        └── MainActivity.kt
```

#### Ejemplo de Salida

**MainView.kt**
```kotlin
import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp

@Composable
fun MainView() {
    fun scriptFunction0() {
        println("¡Hola desde Dars!")
    }
    
    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(16.dp)
    ) {
        Text(
            text = "¡Hola Dars!",
            modifier = Modifier.padding(bottom = 16.dp),
            style = TextStyle(fontSize = 24.sp, color = Color(0xFF333333))
        )
        
        Button(
            onClick = { scriptFunction0() },
            modifier = Modifier.padding(8.dp),
            colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF007BFF))
        ) {
            Text("Hacer clic", color = Color.White)
        }
    }
}
```

#### Desarrollo y Compilación

```bash
# Compilar para escritorio
cd mi-app-multiplatform
./gradlew run

# Compilar para Android
./gradlew installDebug

# Compilar todas las plataformas
./gradlew build
```

#### Ventajas

- **Código compartido**: Un código para múltiples plataformas
- **Performance**: Compilación nativa
- **Moderno**: Tecnologías de vanguardia
- **Futuro**: Tecnología en crecimiento

#### Casos de Uso

- Aplicaciones multiplataforma
- Startups que necesitan presencia en múltiples plataformas
- Proyectos con recursos limitados
- Aplicaciones modernas

## Comparación de Exportadores

### Tabla Comparativa

| Característica | HTML/CSS/JS | React | React Native | PySide6 | C# | Kotlin |
|----------------|-------------|-------|--------------|---------|----|---------| 
| **Plataforma** | Web | Web | Móvil | Escritorio | Windows | Multiplataforma |
| **Complejidad** | Baja | Media | Media | Media | Media | Alta |
| **Performance** | Buena | Excelente | Excelente | Excelente | Excelente | Excelente |
| **Curva de aprendizaje** | Baja | Media | Media | Media | Media | Alta |
| **Ecosistema** | Amplio | Muy amplio | Amplio | Amplio | Muy amplio | Creciente |
| **Distribución** | Fácil | Fácil | App Stores | Ejecutables | Ejecutables | Múltiple |

### Recomendaciones de Uso

#### Para Sitios Web Simples
- **HTML/CSS/JS**: Ideal para sitios estáticos, landing pages, documentación

#### Para Aplicaciones Web Complejas
- **React**: Mejor para SPAs, dashboards, aplicaciones empresariales

#### Para Aplicaciones Móviles
- **React Native**: Excelente para apps móviles multiplataforma

#### Para Aplicaciones de Escritorio
- **PySide6**: Ideal para aplicaciones multiplataforma de escritorio
- **C#**: Mejor para aplicaciones específicas de Windows

#### Para Proyectos Multiplataforma
- **Kotlin**: Futuro prometedor para aplicaciones que necesitan estar en todas las plataformas

## Personalización de Exportadores

### Extender Exportadores Existentes

```python
from pywebui.exporters.web.html_css_js import HTMLCSSJSExporter

class MiExportadorPersonalizado(HTMLCSSJSExporter):
    def generate_css(self, app):
        # CSS personalizado
        css_base = super().generate_css(app)
        css_personalizado = """
        /* Estilos personalizados */
        .mi-clase-especial {
            background: linear-gradient(45deg, #ff6b6b, #4ecdc4);
        }
        """
        return css_base + css_personalizado
        
    def generate_javascript(self, app):
        # JavaScript personalizado
        js_base = super().generate_javascript(app)
        js_personalizado = """
        // Funcionalidad personalizada
        console.log('Exportador personalizado cargado');
        """
        return js_base + js_personalizado
```

### Crear Nuevos Exportadores

```python
from pywebui.exporters.base import Exporter

class MiNuevoExportador(Exporter):
    def get_platform(self):
        return "mi_plataforma"
        
    def export(self, app, output_path):
        # Implementar lógica de exportación
        self.create_output_directory(output_path)
        
        # Generar archivos específicos
        contenido = self.generar_contenido(app)
        self.write_file(f"{output_path}/app.mi_extension", contenido)
        
        return True
        
    def render_component(self, component):
        # Implementar renderizado específico
        return f"<mi_componente>{component.props}</mi_componente>"
        
    def generar_contenido(self, app):
        # Lógica específica de la plataforma
        return "contenido generado"
```

Los exportadores de Dars proporcionan una base sólida para generar aplicaciones en múltiples tecnologías, manteniendo la consistencia y permitiendo la personalización según las necesidades específicas de cada proyecto.

