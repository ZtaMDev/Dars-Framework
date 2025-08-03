#!/usr/bin/env python3
"""
Dars Exporter - Herramienta de línea de comandos para exportar aplicaciones Dars
"""
import shutil
import subprocess
import venv
from rich.prompt import Confirm
from rich.syntax import Syntax
import argparse
import os
import sys
import time
import importlib.util
from pathlib import Path
from typing import Optional, Dict, Any

from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich import print as rprint
from importlib import resources

# Importar exportadores
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dars.core.app import App
from dars.exporters.web.html_css_js import HTMLCSSJSExporter

console = Console()

class DarsExporter:
    """Exportador principal de Dars"""
    
    def __init__(self):
        self.exporters = {
            'html': HTMLCSSJSExporter()
        }
        
    def load_app_from_file(self, file_path: str) -> Optional[App]:
        """Carga una aplicación Dars desde un archivo Python"""
        try:
            # Verificar que el archivo existe
            if not os.path.exists(file_path):
                console.print(f"[red]Error: El archivo {file_path} no existe[/red]")
                return None
                
            # Cargar el módulo dinámicamente
            spec = importlib.util.spec_from_file_location("user_app", file_path)
            if spec is None or spec.loader is None:
                console.print(f"[red]Error: No se pudo cargar el archivo {file_path}[/red]")
                return None
                
            module = importlib.util.module_from_spec(spec)
            
            # Agregar el directorio del archivo al path para imports relativos
            file_dir = os.path.dirname(os.path.abspath(file_path))
            if file_dir not in sys.path:
                sys.path.insert(0, file_dir)
                
            spec.loader.exec_module(module)
            
            # Buscar la variable 'app' en el módulo
            if hasattr(module, 'app') and isinstance(module.app, App):
                return module.app
            else:
                console.print(f"[red]Error: No se encontró una variable 'app' de tipo App en {file_path}[/red]")
                return None
                
        except Exception as e:
            console.print(f"[red]Error al cargar el archivo: {e}[/red]")
            return None
            
    def validate_app(self, app: App) -> bool:
        """Valida una aplicación Dars"""
        errors = app.validate()
        
        if errors:
            console.print("[red]Errores de validación encontrados:[/red]")
            for error in errors:
                console.print(f"  • {error}")
            return False
            
        return True
        
    def export_app(self, app: App, format_name: str, output_path: str, show_preview: bool = False) -> bool:
        """Exporta una aplicación al formato especificado"""
        
        if format_name not in self.exporters:
            console.print(f"[red]Error: Formato '{format_name}' no soportado[/red]")
            self.show_supported_formats()
            return False
            
        exporter = self.exporters[format_name]
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            console=console
        ) as progress:
            
            # Tarea de validación
            task1 = progress.add_task("Validando aplicación...", total=100)
            progress.update(task1, advance=30)
            
            if not self.validate_app(app):
                progress.update(task1, completed=100)
                return False
                
            progress.update(task1, advance=70)
            
            # Tarea de exportación
            task2 = progress.add_task(f"Exportando a {format_name}...", total=100)
            progress.update(task2, advance=20)
            
            try:
                success = exporter.export(app, output_path)
                progress.update(task2, advance=80)
                
                if success:
                    progress.update(task1, completed=100)
                    progress.update(task2, completed=100)
                    
                    # Mostrar información de éxito
                    self.show_export_success(app, format_name, output_path)
                    
                    if show_preview and format_name == 'html':
                        self.show_preview_info(output_path)
                        
                    return True
                else:
                    console.print(f"[red]Error durante la exportación a {format_name}[/red]")
                    return False
                    
            except Exception as e:
                console.print(f"[red]Error durante la exportación: {e}[/red]")
                return False
                
    def show_supported_formats(self):
        """Muestra los formatos soportados"""
        table = Table(title="Formatos de Exportación Soportados")
        table.add_column("Formato", style="cyan")
        table.add_column("Descripción", style="white")
        table.add_column("Plataforma", style="green")
        
        formats_info = {
            'html': ('HTML/CSS/JavaScript', 'Web'),
        }
        
        for format_name, (description, platform) in formats_info.items():
            table.add_row(format_name, description, platform)
            
        console.print(table)
        
    def show_export_success(self, app: App, format_name: str, output_path: str):
        """Muestra información de éxito de exportación"""
        stats = app.get_stats()
        
        panel_content = f"""
[green]✓[/green] Exportación completada exitosamente

[bold]Aplicación:[/bold] {app.title}
[bold]Formato:[/bold] {format_name}
[bold]Directorio de salida:[/bold] {output_path}

[bold]Estadísticas:[/bold]
• Componentes totales: {stats['total_components']}
• Profundidad máxima: {stats['max_depth']}
• Scripts: {stats['scripts_count']}
• Estilos globales: {stats['global_styles_count']}
"""
        
        console.print(Panel(panel_content, title="Exportación Exitosa", border_style="green"))
        
    def show_preview_info(self, output_path: str):
        """Muestra información sobre cómo previsualizar la aplicación"""
        index_path = os.path.join(output_path, "index.html")
        
        if os.path.exists(index_path):
            console.print(f"\n[bold cyan]Para previsualizar la aplicación:[/bold cyan]")
            console.print(f"  Abrir en navegador: file://{os.path.abspath(index_path)}")
            console.print(f"  O usar: dars preview {output_path}")
            
    def show_app_info(self, app: App):
        """Muestra información detallada de la aplicación"""
        stats = app.get_stats()
        
        # Información básica
        info_table = Table(title=f"Información de la Aplicación: {app.title}")
        info_table.add_column("Propiedad", style="cyan")
        info_table.add_column("Valor", style="white")
        
        info_table.add_row("Título", app.title)
        info_table.add_row("Componentes totales", str(stats['total_components']))
        info_table.add_row("Profundidad máxima", str(stats['max_depth']))
        info_table.add_row("Scripts", str(stats['scripts_count']))
        info_table.add_row("Estilos globales", str(stats['global_styles_count']))
        info_table.add_row("Tema", app.config.get('theme', 'light'))
        info_table.add_row("Responsive", str(app.config.get('responsive', True)))
        
        console.print(info_table)
        
        # Árbol de componentes
        if app.root:
            console.print("\n[bold]Estructura de Componentes:[/bold]")
            self.print_component_tree(app.root)
            
    def print_component_tree(self, component, level: int = 0):
        """Imprime el árbol de componentes"""
        indent = "  " * level
        component_name = component.__class__.__name__
        component_id = f" (id: {component.id})" if component.id else ""
        
        console.print(f"{indent}├─ {component_name}{component_id}")
        
        for child in component.children:
            self.print_component_tree(child, level + 1)
    

    def init_project(self, name: str, template: Optional[str] = None):
        # 2. Crear main.py con ejemplo
        HELLO_WORLD_CODE = """
from dars.core.app import App
from dars.components.basic.text import Text
from dars.components.basic.button import Button
from dars.components.basic.container import Container
from dars.scripts.script import InlineScript

app = App(title="Hello World - Dars")

container = Container(style={
    'display': 'flex',
    'flex-direction': 'column',
    'align-items': 'center',
    'justify-content': 'center',
    'min-height': '100vh',
    'background-color': '#f0f2f5',
    'font-family': 'Arial, sans-serif'
})

titulo = Text("¡Hola Mundo!", style={'font-size': '48px', 'color': '#2c3e50'})
subtitulo = Text("Tu primera aplicación con Dars", style={'font-size': '20px', 'color': '#7f8c8d'})
boton = Button("¡Hacer clic aquí!", style={'background-color': '#3498db', 'color': 'white'})

script = InlineScript(\"""
document.querySelector('button')?.addEventListener('click', () => {
    alert('¡Felicidades! Has creado tu primera aplicación Dars');
});
\""")

container.add_child(titulo)
container.add_child(subtitulo)
container.add_child(boton)
app.set_root(container)
app.add_script(script)
"""
        """Inicializa un proyecto base Dars, opcionalmente usando un template"""
        if os.path.exists(name):
            console.print(f"[red]❌ El directorio '{name}' ya existe. Elige otro nombre.[/red]")
            return

        # 1. Crear directorio del proyecto
        os.makedirs(name)
        console.print(f"[green]✔ Directorio '{name}' creado[/green]")


        # 4. Generar main.py
        main_py = Path(name) / "main.py"
        if template:
            templates = list_templates()
            src = templates[template]
            shutil.copy(src, main_py)
            console.print(f"[green]✔ Template '{template}' copiado como main.py[/green]")
        else:
            # código hello world embebido...
            main_py.write_text(HELLO_WORLD_CODE, encoding="utf-8")
            console.print(f"[green]✔ Archivo main.py creado (Hello World por defecto)[/green]")

        # 5. Instrucciones finales
        console.print("\n[bold cyan]🎉 Proyecto Dars inicializado exitosamente[/bold cyan]")
        console.print(Syntax(f"cd {name}", "bash"))
        console.print(Syntax(f"\nPara exportar el template usa:", "bash"))
        console.print(Syntax(f"dars export main.py --format html --output build", "bash"))
        console.print(Syntax(f"\nPara ver el proyecto en un navegador usa:", "bash"))
        console.print(Syntax(f"dars preview build", "bash")) 
    

def create_parser() -> argparse.ArgumentParser:
    """Crea el parser de argumentos de línea de comandos"""
    parser = argparse.ArgumentParser(
        description="Dars Exporter - Exporta aplicaciones Dars a Web",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:
  dars export app.py --format html --output ./dist
  dars info app.py
  dars preview ./dist
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Comandos disponibles')
    
    # Comando export
    export_parser = subparsers.add_parser('export', help='Exportar aplicación')
    export_parser.add_argument('file', help='Archivo Python con la aplicación Dars')
    export_parser.add_argument('--format', '-f', required=True, 
                              choices=["html"],
                              help='Formato de exportación')
    export_parser.add_argument('--output', '-o', required=True,
                              help='Directorio de salida')
    export_parser.add_argument('--preview', '-p', action='store_true',
                              help='Mostrar información de preview (solo para HTML)')
    
    # Comando info
    info_parser = subparsers.add_parser('info', help='Mostrar información de la aplicación')
    info_parser.add_argument('file', help='Archivo Python con la aplicación Dars')
    
    # Comando formats
    formats_parser = subparsers.add_parser('formats', help='Mostrar formatos soportados')
    
    # Comando preview
    preview_parser = subparsers.add_parser('preview', help='Información de preview')
    preview_parser.add_argument('path', help='Directorio con la aplicación exportada')

    # Comando init
    init_parser = subparsers.add_parser('init', help='Crea un proyecto Dars')
    init_parser.add_argument('name', help='Nombre del proyecto')
    tmpl_choices = list_templates().keys()
    init_parser.add_argument(
        '-t', '--template',
        choices=tmpl_choices,
        help='Plantilla inicial: categoría/nombre (por ejemplo basic/hello_world)'
   )
    
    return parser
def list_templates() -> Dict[str, Path]:
        """
        Busca carpetas dentro de dars/templates/examples y devuelve un dict
        { "basic/hello_world.py": Path(...), ... }
        """
        tmpl_root = Path(resources.files("dars.templates") / "examples")
        templates = {}
        for category in tmpl_root.iterdir():
            if category.is_dir():
                for py in category.glob("*.py"):
                    key = f"{category.name}/{py.stem}"
                    templates[key] = py
        return templates
def main():
    """Función principal del CLI"""
    parser = create_parser()
    args = parser.parse_args()
    
    # Mostrar banner
    console.print(Panel(
        Text("Dars Exporter", style="bold cyan", justify="center"),
        subtitle="Framework de UI multiplataforma en Python",
        border_style="cyan"
    ))
    
    exporter = DarsExporter()
    
    if args.command == 'export':
        # Cargar aplicación
        app = exporter.load_app_from_file(args.file)
        if app is None:
            sys.exit(1)
            
        # Exportar
        success = exporter.export_app(app, args.format, args.output, args.preview)
        sys.exit(0 if success else 1)
        
    elif args.command == 'info':
        # Mostrar información
        app = exporter.load_app_from_file(args.file)
        if app is None:
            sys.exit(1)
            
        exporter.show_app_info(app)
        
    elif args.command == 'formats':
        # Mostrar formatos
        exporter.show_supported_formats()
    
    elif args.command == 'init':
        exporter.init_project(args.name, template=args.template)

        
    elif args.command == 'preview':
        index_path = os.path.join(args.path, "index.html")
        if os.path.exists(index_path):
            console.print(f"[green]Aplicación encontrada en: {args.path} [/green]")
            console.print(f"Abrir en navegador: file://{os.path.abspath(index_path)}")
            console.print("¿Quieres ver la preview? [green]y[/green] / [red]n[/red] [y/n] ")
            if input().lower() == 'y':
                os.system(f"{sys.executable} -m dars.cli.preview {args.path}")
        else:
            console.print(f"[red]No se encontró index.html en {args.path}[/red]")

            
    else:
        parser.print_help()

if __name__ == "__main__":
    main()

