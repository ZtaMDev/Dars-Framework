#!/usr/bin/env python3
"""
Dars Preview - Preview system for exported applications
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
from rich.table import Table
from rich import print as rprint

from dars.cli.translations import translator

console = Console()

class PreviewServer:
    """Preview server for Dars applications"""
    
    class DarsRequestHandler(http.server.SimpleHTTPRequestHandler):
        def end_headers(self):
            # CORS para desarrollo PWA si es necesario
            self.send_header('Access-Control-Allow-Origin', '*')
            super().end_headers()
        def guess_type(self, path):
            if path.endswith('sw.js'):
                return 'application/javascript'
            return super().guess_type(path)
    
    def __init__(self, directory: str, port: int = 8000):
        self.directory = os.path.abspath(directory)
        self.port = port
        self.server = None
        self.server_thread = None
        
    def start(self):
        """Starts the preview server"""
        try:
            # Change to the application directory
            os.chdir(self.directory)
            
            # Create the server
            handler = self.DarsRequestHandler
            self.server = socketserver.TCPServer(("", self.port), handler)
            
            # Start in a separate thread
            self.server_thread = threading.Thread(target=self.server.serve_forever)
            self.server_thread.daemon = True
            self.server_thread.start()
            
            return True
            
        except Exception as e:
            console.print(f"[red]{translator.get('server_start_error')}: {e}[/red]")
            return False
            
    def stop(self):
        """Stops the preview server"""
        if self.server:
            self.server.shutdown()
            self.server.server_close()
            
    def get_url(self) -> str:
        """Gets the server URL"""
        return f"http://localhost:{self.port}"

def preview_html_app(directory: str, auto_open: bool = True, port: int = 8000):
    """Previews an exported HTML application"""
    
    import signal
    
    # Verify that index.html exists
    index_path = os.path.join(directory, "index.html")
    if not os.path.exists(index_path):
        console.print(f"[red]{translator.get('index_html_missing')} {directory}[/red]")
        return False
        
    # Create and start the server
    server = PreviewServer(directory, port)
    
    if not server.start():
        return False
        
    url = server.get_url()
    
    # Show information
    panel_content = f"""
[green]✓[/green] {translator.get('preview_server_started')}

[bold]URL:[/bold] {url}
[bold]{translator.get('directory')}:[/bold] {directory}
[bold]{translator.get('port')}:[/bold] {port}

[yellow]{translator.get('press_ctrl_c')}[/yellow]
"""
    
    console.print(Panel(panel_content, title="Dars Preview", border_style="green"))
    
    # Open in browser if requested
    if auto_open:
        try:
            webbrowser.open(url)
            console.print(f"[cyan]{translator.get('opening_in_browser').format(url=url)}[/cyan]")
        except Exception as e:
            console.print(f"[yellow]{translator.get('browser_open_error')}: {e}[/yellow]")
            console.print(f"[cyan]{translator.get('open_manually')}: {url}[/cyan]")

    import threading
    import signal

    shutdown_event = threading.Event()

    try:
        while not shutdown_event.is_set():
            shutdown_event.wait(timeout=1)  # Espera hasta que se pida cerrar, sin consumir CPU
    except KeyboardInterrupt:
        shutdown_event.set()
    finally:
        console.print(f"\n[yellow]{translator.get('stopping_server')}[/yellow]")
        server.stop()
        console.print(f"[green]{translator.get('server_stopped')}[/green]")

    return True

def preview_react_app(directory: str):
    """Previews an exported React application"""
    
    # Verify that package.json exists
    package_path = os.path.join(directory, "package.json")
    if not os.path.exists(package_path):
        console.print(f"[red]{translator.get('package_json_not_found')} {directory}[/red]")
        return False
        
    console.print(Panel(
        f"""
{translator.get('preview_react_instructions')}:

1. {translator.get('navigate_to_directory')}:
   [cyan]cd {directory}[/cyan]

2. {translator.get('install_dependencies')}:
   [cyan]npm install[/cyan]

3. {translator.get('start_dev_server')}:
   [cyan]npm start[/cyan]

{translator.get('app_will_open')} http://localhost:3000
        """,
        title=translator.get('react_preview'),
        border_style="blue"
    ))
    
    return True

def preview_react_native_app(directory: str):
    """Previews an exported React Native application"""
    
    # Verify that package.json exists
    package_path = os.path.join(directory, "package.json")
    if not os.path.exists(package_path):
        console.print(f"[red]{translator.get('package_json_not_found')} {directory}[/red]")
        return False
        
    console.print(Panel(
        f"""
{translator.get('preview_react_native_instructions')}:

1. {translator.get('navigate_to_directory')}:
   [cyan]cd {directory}[/cyan]

2. {translator.get('install_dependencies')}:
   [cyan]npm install[/cyan]

3. {translator.get('for_android')}:
   [cyan]npm run android[/cyan]

4. {translator.get('for_ios')}:
   [cyan]npm run ios[/cyan]

5. {translator.get('start_metro')}:
   [cyan]npm start[/cyan]

[yellow]{translator.get('react_native_note')}[/yellow]
        """,
        title=translator.get('react_native_preview'),
        border_style="green"
    ))
    
    return True

def preview_pyside6_app(directory: str):
    """Previews an exported PySide6 application"""
    
    # Verify that main.py exists
    main_path = os.path.join(directory, "main.py")
    if not os.path.exists(main_path):
        console.print(f"[red]{translator.get('main_py_not_found')} {directory}[/red]")
        return False
        
    console.print(Panel(
        f"""
{translator.get('run_pyside6_app')}:

1. {translator.get('navigate_to_directory')}:
   [cyan]cd {directory}[/cyan]

2. {translator.get('install_dependencies')}:
   [cyan]pip install -r requirements.txt[/cyan]

3. {translator.get('run_application')}:
   [cyan]python main.py[/cyan]

[yellow]{translator.get('pyside6_note')}[/yellow]
        """,
        title=translator.get('pyside6_preview'),
        border_style="magenta"
    ))
    
    return True

def preview_csharp_app(directory: str):
    """Previews an exported C# application"""
    
    # Search for .csproj file
    csproj_files = list(Path(directory).glob("*.csproj"))
    if not csproj_files:
        console.print(f"[red]{translator.get('csproj_not_found')} {directory}[/red]")
        return False
        
    csproj_file = csproj_files[0].name
    
    console.print(Panel(
        f"""
{translator.get('run_csharp_app')}:

1. {translator.get('navigate_to_directory')}:
   [cyan]cd {directory}[/cyan]

2. {translator.get('restore_dependencies')}:
   [cyan]dotnet restore[/cyan]

3. {translator.get('build_application')}:
   [cyan]dotnet build[/cyan]

4. {translator.get('run_application')}:
   [cyan]dotnet run[/cyan]

[yellow]{translator.get('dotnet_note')}[/yellow]
        """,
        title=translator.get('csharp_preview'),
        border_style="red"
    ))
    
    return True

def preview_kotlin_app(directory: str):
    """Previews an exported Kotlin application"""
    
    # Verify that build.gradle.kts exists
    gradle_path = os.path.join(directory, "build.gradle.kts")
    if not os.path.exists(gradle_path):
        console.print(f"[red]{translator.get('gradle_not_found')} {directory}[/red]")
        return False
        
    console.print(Panel(
        f"""
{translator.get('run_kotlin_app')}:

1. {translator.get('navigate_to_directory')}:
   [cyan]cd {directory}[/cyan]

2. {translator.get('for_desktop')}:
   [cyan]./gradlew run[/cyan]

3. {translator.get('for_android')}:
   [cyan]./gradlew installDebug[/cyan]

4. {translator.get('build_all_platforms')}:
   [cyan]./gradlew build[/cyan]

[yellow]{translator.get('kotlin_note')}[/yellow]
        """,
        title=translator.get('kotlin_preview'),
        border_style="yellow"
    ))
    
    return True

def auto_detect_format(directory: str) -> str:
    """Automatically detects the format of the exported application"""
    
    if os.path.exists(os.path.join(directory, "index.html")):
        return "html"
    elif os.path.exists(os.path.join(directory, "package.json")):
        # Read package.json to distinguish between React and React Native
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
    """Previews an exported application"""
    
    if not os.path.exists(directory):
        console.print(f"[red]{translator.get('directory_not_exists').format(directory=directory)}[/red]")
        return False
        
    # Automatically detect format if not specified
    if format_name is None:
        format_name = auto_detect_format(directory)
        
    if format_name == "unknown":
        console.print(f"[red]{translator.get('format_not_detected').format(directory=directory)}[/red]")
        return False
        
    console.print(f"[cyan]{translator.get('detected_format')}: {format_name}[/cyan]")
    
    # Call the corresponding previewer
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
        console.print(f"[red]{translator.get('format_not_supported').format(format=format_name)}[/red]")
        return False

if __name__ == "__main__":
    import argparse
    import sys
    
    # First, create a simple parser just to extract the language
    pre_parser = argparse.ArgumentParser(add_help=False)
    pre_parser.add_argument("--lang", "-l", choices=["en", "es"], default="en")
    
    # Parse known args to get language without triggering errors on other args
    pre_args, _ = pre_parser.parse_known_args()
    
    # Set language before creating the main parser and save preference if specified
    # If --lang is in sys.argv, it means the user explicitly specified it
    save_preference = "--lang" in sys.argv or "-l" in sys.argv
    translator.set_language(pre_args.lang, save=save_preference)
    
    # Check for help before parsing arguments to show Rich-styled help
    if '-h' in sys.argv or '--help' in sys.argv:
        # Show banner
        console.print(Panel(
            Text("Dars Preview", style="bold cyan", justify="center"),
            subtitle=translator.get('preview_description'),
            border_style="cyan"
        ))
        
        # Show usage
        console.print(f"\n[bold cyan]{translator.get('usage')}:[/bold cyan]")
        console.print("preview.py [-h] [--format FORMAT] [--no-open] [--port PORT] [--lang {en,es}] directory")
        
        # Show positional arguments
        console.print(f"\n[bold cyan]{translator.get('positional_arguments')}:[/bold cyan]")
        pos_table = Table(show_header=False, box=None, padding=(0, 2, 0, 0), expand=True)
        pos_table.add_column("Argument", style="bold green", width=20, no_wrap=True)
        pos_table.add_column("Description", style="dim white", overflow="fold")
        pos_table.add_row("directory", translator.get('directory_help'))
        console.print(pos_table)
        
        # Show options
        console.print(f"\n[bold cyan]{translator.get('options')}:[/bold cyan]")
        opt_table = Table(show_header=False, box=None, padding=(0, 2, 0, 0), expand=True)
        opt_table.add_column("Option", style="bold green", width=30, no_wrap=True)
        opt_table.add_column("Description", style="dim white", overflow="fold")
        opt_table.add_row("-h, --help", "show this help message and exit")
        opt_table.add_row("--format FORMAT, -f FORMAT", translator.get('format_help'))
        opt_table.add_row("--no-open", translator.get('no_open_help'))
        opt_table.add_row("--port PORT, -p PORT", translator.get('port_help'))
        opt_table.add_row("--lang {en,es}, -l {en,es}", translator.get('lang_help'))
        console.print(opt_table)
        
        sys.exit(0)
    
    # Now create the full parser with translated help text
    parser = argparse.ArgumentParser(description=translator.get('preview_description'))
    parser.add_argument("directory", help=translator.get('directory_help'))
    parser.add_argument("--format", "-f", help=translator.get('format_help'))
    parser.add_argument("--no-open", action="store_true", help=translator.get('no_open_help'))
    parser.add_argument("--port", "-p", type=int, default=8000, help=translator.get('port_help'))
    parser.add_argument("--lang", "-l", choices=["en", "es"], default="en", help=translator.get('lang_help'))
    
    args = parser.parse_args()
    
    success = preview_app(
        args.directory, 
        args.format, 
        not args.no_open, 
        args.port
    )
    
    sys.exit(0 if success else 1)

