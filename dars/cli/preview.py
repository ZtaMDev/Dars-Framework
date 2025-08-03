#!/usr/bin/env python3
"""
Dars Preview - Sistema de preview para aplicaciones exportadas
"""

import os
import sys
import webbrowser
import http.server
import socketserver
import threading
import time
from pathlib import Path

from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich import print as rprint

console = Console()

class PreviewServer:
    """Servidor de preview para aplicaciones Dars"""
    
    def __init__(self, directory: str, port: int = 8000):
        self.directory = os.path.abspath(directory)
        self.port = port
        self.server = None
        self.server_thread = None
        
    def start(self):
        """Inicia el servidor de preview"""
        try:
            # Cambiar al directorio de la aplicación
            os.chdir(self.directory)
            
            # Crear el servidor
            handler = http.server.SimpleHTTPRequestHandler
            self.server = socketserver.TCPServer(("", self.port), handler)
            
            # Iniciar en un hilo separado
            self.server_thread = threading.Thread(target=self.server.serve_forever)
            self.server_thread.daemon = True
            self.server_thread.start()
            
            return True
            
        except Exception as e:
            console.print(f"[red]Error al iniciar el servidor: {e}[/red]")
            return False
            
    def stop(self):
        """Detiene el servidor de preview"""
        if self.server:
            self.server.shutdown()
            self.server.server_close()
            
    def get_url(self) -> str:
        """Obtiene la URL del servidor"""
        return f"http://localhost:{self.port}"

def preview_html_app(directory: str, auto_open: bool = True, port: int = 8000):
    """Previsualiza una aplicación HTML exportada"""
    
    # Verificar que existe index.html
    index_path = os.path.join(directory, "index.html")
    if not os.path.exists(index_path):
        console.print(f"[red]Error: No se encontró index.html en {directory}[/red]")
        return False
        
    # Crear y iniciar el servidor
    server = PreviewServer(directory, port)
    
    if not server.start():
        return False
        
    url = server.get_url()
    
    # Mostrar información
    panel_content = f"""
[green]✓[/green] Servidor de preview iniciado

[bold]URL:[/bold] {url}
[bold]Directorio:[/bold] {directory}
[bold]Puerto:[/bold] {port}

[yellow]Presiona Ctrl+C para detener el servidor[/yellow]
"""
    
    console.print(Panel(panel_content, title="Dars Preview", border_style="green"))
    
    # Abrir en navegador si se solicita
    if auto_open:
        try:
            webbrowser.open(url)
            console.print(f"[cyan]Abriendo {url} en el navegador...[/cyan]")
        except Exception as e:
            console.print(f"[yellow]No se pudo abrir automáticamente el navegador: {e}[/yellow]")
            console.print(f"[cyan]Abrir manualmente: {url}[/cyan]")
    
    try:
        # Mantener el servidor corriendo
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        console.print("\n[yellow]Deteniendo servidor...[/yellow]")
        server.stop()
        console.print("[green]Servidor detenido[/green]")
        
    return True

def preview_react_app(directory: str):
    """Previsualiza una aplicación React exportada"""
    
    # Verificar que existe package.json
    package_path = os.path.join(directory, "package.json")
    if not os.path.exists(package_path):
        console.print(f"[red]Error: No se encontró package.json en {directory}[/red]")
        return False
        
    console.print(Panel(
        f"""
Para previsualizar la aplicación React:

1. Navegar al directorio:
   [cyan]cd {directory}[/cyan]

2. Instalar dependencias:
   [cyan]npm install[/cyan]

3. Iniciar el servidor de desarrollo:
   [cyan]npm start[/cyan]

La aplicación se abrirá automáticamente en http://localhost:3000
        """,
        title="Preview de React",
        border_style="blue"
    ))
    
    return True

def preview_react_native_app(directory: str):
    """Previsualiza una aplicación React Native exportada"""
    
    # Verificar que existe package.json
    package_path = os.path.join(directory, "package.json")
    if not os.path.exists(package_path):
        console.print(f"[red]Error: No se encontró package.json en {directory}[/red]")
        return False
        
    console.print(Panel(
        f"""
Para previsualizar la aplicación React Native:

1. Navegar al directorio:
   [cyan]cd {directory}[/cyan]

2. Instalar dependencias:
   [cyan]npm install[/cyan]

3. Para Android:
   [cyan]npm run android[/cyan]

4. Para iOS (solo en macOS):
   [cyan]npm run ios[/cyan]

5. Iniciar Metro bundler:
   [cyan]npm start[/cyan]

[yellow]Nota: Necesitas tener configurado el entorno de desarrollo de React Native[/yellow]
        """,
        title="Preview de React Native",
        border_style="green"
    ))
    
    return True

def preview_pyside6_app(directory: str):
    """Previsualiza una aplicación PySide6 exportada"""
    
    # Verificar que existe main.py
    main_path = os.path.join(directory, "main.py")
    if not os.path.exists(main_path):
        console.print(f"[red]Error: No se encontró main.py en {directory}[/red]")
        return False
        
    console.print(Panel(
        f"""
Para ejecutar la aplicación PySide6:

1. Navegar al directorio:
   [cyan]cd {directory}[/cyan]

2. Instalar dependencias:
   [cyan]pip install -r requirements.txt[/cyan]

3. Ejecutar la aplicación:
   [cyan]python main.py[/cyan]

[yellow]Nota: Asegúrate de tener PySide6 instalado[/yellow]
        """,
        title="Preview de PySide6",
        border_style="magenta"
    ))
    
    return True

def preview_csharp_app(directory: str):
    """Previsualiza una aplicación C# exportada"""
    
    # Buscar archivo .csproj
    csproj_files = list(Path(directory).glob("*.csproj"))
    if not csproj_files:
        console.print(f"[red]Error: No se encontró archivo .csproj en {directory}[/red]")
        return False
        
    csproj_file = csproj_files[0].name
    
    console.print(Panel(
        f"""
Para ejecutar la aplicación C#:

1. Navegar al directorio:
   [cyan]cd {directory}[/cyan]

2. Restaurar dependencias:
   [cyan]dotnet restore[/cyan]

3. Compilar la aplicación:
   [cyan]dotnet build[/cyan]

4. Ejecutar la aplicación:
   [cyan]dotnet run[/cyan]

[yellow]Nota: Necesitas tener .NET 6.0 o superior instalado[/yellow]
        """,
        title="Preview de C#",
        border_style="red"
    ))
    
    return True

def preview_kotlin_app(directory: str):
    """Previsualiza una aplicación Kotlin exportada"""
    
    # Verificar que existe build.gradle.kts
    gradle_path = os.path.join(directory, "build.gradle.kts")
    if not os.path.exists(gradle_path):
        console.print(f"[red]Error: No se encontró build.gradle.kts en {directory}[/red]")
        return False
        
    console.print(Panel(
        f"""
Para ejecutar la aplicación Kotlin Multiplatform:

1. Navegar al directorio:
   [cyan]cd {directory}[/cyan]

2. Para escritorio:
   [cyan]./gradlew run[/cyan]

3. Para Android (con emulador/dispositivo):
   [cyan]./gradlew installDebug[/cyan]

4. Para compilar todas las plataformas:
   [cyan]./gradlew build[/cyan]

[yellow]Nota: Necesitas tener JDK 11+ y Android SDK configurados[/yellow]
        """,
        title="Preview de Kotlin Multiplatform",
        border_style="yellow"
    ))
    
    return True

def auto_detect_format(directory: str) -> str:
    """Detecta automáticamente el formato de la aplicación exportada"""
    
    if os.path.exists(os.path.join(directory, "index.html")):
        return "html"
    elif os.path.exists(os.path.join(directory, "package.json")):
        # Leer package.json para distinguir entre React y React Native
        try:
            import json
            with open(os.path.join(directory, "package.json"), 'r') as f:
                package_data = json.load(f)
                
            if "react-native" in package_data.get("dependencies", {}):
                return "react-native"
            else:
                return "react"
        except:
            return "react"
    elif os.path.exists(os.path.join(directory, "main.py")):
        return "pyside6"
    elif list(Path(directory).glob("*.csproj")):
        return "csharp"
    elif os.path.exists(os.path.join(directory, "build.gradle.kts")):
        return "kotlin"
    else:
        return "unknown"

def preview_app(directory: str, format_name: str = None, auto_open: bool = True, port: int = 8000):
    """Previsualiza una aplicación exportada"""
    
    if not os.path.exists(directory):
        console.print(f"[red]Error: El directorio {directory} no existe[/red]")
        return False
        
    # Detectar formato automáticamente si no se especifica
    if format_name is None:
        format_name = auto_detect_format(directory)
        
    if format_name == "unknown":
        console.print(f"[red]Error: No se pudo detectar el formato de la aplicación en {directory}[/red]")
        return False
        
    console.print(f"[cyan]Formato detectado: {format_name}[/cyan]")
    
    # Llamar al previsualizador correspondiente
    preview_functions = {
        "html": lambda: preview_html_app(directory, auto_open, port),
        "react": lambda: preview_react_app(directory),
        "react-native": lambda: preview_react_native_app(directory),
        "pyside6": lambda: preview_pyside6_app(directory),
        "csharp": lambda: preview_csharp_app(directory),
        "kotlin": lambda: preview_kotlin_app(directory)
    }
    
    preview_function = preview_functions.get(format_name)
    if preview_function:
        return preview_function()
    else:
        console.print(f"[red]Error: Formato '{format_name}' no soportado para preview[/red]")
        return False

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Dars Preview - Sistema de preview")
    parser.add_argument("directory", help="Directorio con la aplicación exportada")
    parser.add_argument("--format", "-f", help="Formato de la aplicación (auto-detectado si no se especifica)")
    parser.add_argument("--no-open", action="store_true", help="No abrir automáticamente el navegador")
    parser.add_argument("--port", "-p", type=int, default=8000, help="Puerto para el servidor (solo HTML)")
    
    args = parser.parse_args()
    
    success = preview_app(
        args.directory, 
        args.format, 
        not args.no_open, 
        args.port
    )
    
    sys.exit(0 if success else 1)

