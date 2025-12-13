#!/usr/bin/env python3
"""
Dars Exporter - Command line tool for exporting Dars applications
"""
import argparse
import importlib.util
import os
import shutil
import sys
from typing import Optional

from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
from rich.prompt import Confirm
from rich.syntax import Syntax
from rich.table import Table
from rich.text import Text

# Importar exportadores
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dars.core.app import App
from dars.exporters.web.html_css_js import HTMLCSSJSExporter
from dars.exporters.desktop.electron import ElectronExporter
from dars.cli.translations import translator
from dars.config import load_config, resolve_paths, write_default_config, update_config
from dars.cli.doctor.doctor import run_doctor, run_forcedev

console = Console()

class RichHelpFormatter(argparse.HelpFormatter):
    """Custom formatter for argparse help using Rich"""
    
    def __init__(self, prog, indent_increment=2, max_help_position=24, width=None):
        super().__init__(prog, indent_increment, max_help_position, width)
        
    def format_help(self):
        # Call the original method to get the help text
        help_text = super().format_help()
        return help_text
        
    def add_text(self, text):
        # Override this method to prevent the epilog from being shown in the options section
        if text and (text.startswith('\nEjemplos de uso:') or text.startswith('\nUsage examples:')):
            return
        return super().add_text(text)

    def _format_action(self, action):
        # Check if this is the help action and replace its help message with the translated one
        if action.option_strings and ('-h' in action.option_strings or '--help' in action.option_strings):
            action.help = translator.get('help_arg_message')
        return super()._format_action(action)
    
    @classmethod
    def rich_print_help(cls, parser, console=console):
        # Get the standard help text
        help_text = parser.format_help()
        
        # Extract the main sections
        sections = {}
        current_section = None
        lines = help_text.split('\n')
        section_content = []
        
        for line in lines:
            if line and not line.startswith(' ') and line.endswith(':'):
                # It's a section header
                if current_section:
                    sections[current_section] = '\n'.join(section_content)
                current_section = line[:-1]  # Remove the colon
                section_content = []
            elif current_section:
                section_content.append(line)
        
        # Add the last section
        if current_section and section_content:
            sections[current_section] = '\n'.join(section_content)
        
        # Show the program title
        prog_name = parser.prog
        description = parser.description
        
        # Main panel
        console.print(Panel(
            Text(prog_name, style="bold cyan", justify="center"),
            subtitle=translator.get('cli_subtitle'),
            border_style="cyan"
        ))
        
        # Check if there are examples in the epilog
        epilog_content = ""
        if parser.epilog:
            epilog_content = parser.epilog.strip()
        
        # Show each section with style
        for section, content in sections.items():
            if section == 'usage':
                # Usage section
                usage = content.strip()
                console.print(f"\n[bold cyan]{translator.get('usage')}:[/bold cyan]")
                console.print(Syntax(usage, "bash", theme="monokai", word_wrap=True))
            elif 'positional arguments' in section.lower():
                # Positional arguments
                console.print(f"\n[bold cyan]{translator.get('positional_arguments')}:[/bold cyan]")
                _print_arguments_table(content)
            elif 'optional arguments' in section.lower() or 'options' in section.lower():
                # Optional arguments
                console.print(f"\n[bold cyan]{translator.get('options')}:[/bold cyan]")
                _print_arguments_table(content)
            elif section.lower() == 'commands' or 'subcommands' in section.lower():
                # Subcommands
                console.print(f"\n[bold cyan]{translator.get('commands')}:[/bold cyan]")
                _print_arguments_table(content)
            elif 'examples' in section.lower() or section.lower() == 'epilog':
                # We don't process examples here to avoid duplication
                pass
            elif section.lower() != 'usage examples':
                # Other sections (skip 'usage examples' to avoid duplication)
                console.print(f"\n[bold cyan]{section.upper()}:[/bold cyan]")
                console.print(content.strip())
        
        # Always show examples at the end
        console.print(f"\n[bold cyan]{translator.get('examples')}:[/bold cyan]")
        # Get the actual examples from translations
        examples_text = translator.get('examples_text')
        examples = [line.strip() for line in examples_text.strip().split('\n') if line.strip()]
        
        examples_table = Table(box=None, expand=True, show_header=False, padding=(0, 1, 0, 1))
        examples_table.add_column("Example", overflow="fold")
        
        for example in examples:
            if example.strip():
                examples_table.add_row(Syntax(example.strip(), "bash", theme="monokai"))
        
        console.print(Panel(examples_table, border_style="cyan", padding=(1, 2)))

def pretty_print_help(parser: argparse.ArgumentParser) -> None:
    # Just print argparse help (no custom header)
    parser.print_help()

def _print_arguments_table(content):
    """Prints a table of arguments from the text content"""
    table = Table(show_header=False, box=None, padding=(0, 2, 0, 0), expand=True)
    table.add_column(translator.get('argument_column'), style="bold green", width=30, no_wrap=True)
    table.add_column(translator.get('description_column'), style="dim white", overflow="fold")
    
    lines = content.strip().split('\n')
    current_arg = None
    current_desc = []
    
    for line in lines:
        if line.strip():
            if not line.startswith('  '):
                # Es un nuevo argumento
                if current_arg:
                    # Estilizar el argumento
                    styled_arg = current_arg
                    if '-' in styled_arg:
                        # Resaltar las opciones cortas y largas
                        parts = styled_arg.split(', ')
                        styled_parts = []
                        for part in parts:
                            if part.startswith('--'):
                                styled_parts.append(f"[cyan]{part}[/cyan]")
                            elif part.startswith('-'):
                                styled_parts.append(f"[green]{part}[/green]")
                            else:
                                styled_parts.append(part)
                        styled_arg = ", ".join(styled_parts)
                    
                    table.add_row(styled_arg, '\n'.join(current_desc))
                
                parts = line.strip().split('  ', 1)
                current_arg = parts[0].strip()
                current_desc = [parts[1].strip()] if len(parts) > 1 else []
            else:
                # Es continuación de la descripción
                current_desc.append(line.strip())
    
    # Añadir el último argumento
    if current_arg:
        # Estilizar el último argumento
        styled_arg = current_arg
        if '-' in styled_arg:
            # Resaltar las opciones cortas y largas
            parts = styled_arg.split(', ')
            styled_parts = []
            for part in parts:
                if part.startswith('--'):
                    styled_parts.append(f"[cyan]{part}[/cyan]")
                elif part.startswith('-'):
                    styled_parts.append(f"[green]{part}[/green]")
                else:
                    styled_parts.append(part)
            styled_arg = ", ".join(styled_parts)
        
        table.add_row(styled_arg, '\n'.join(current_desc))
    
    console.print(table)

class DarsExporter:
    """Exportador principal de Dars"""
    
    def __init__(self):
        self.exporters = {
            'html': HTMLCSSJSExporter(),  # legacy alias
            'web': HTMLCSSJSExporter(),   # preferred alias
            'desktop': ElectronExporter(),
        }
        
    def load_app_from_file(self, file_path: str) -> Optional[App]:
        """Loads a Dars application from a Python file"""
        try:
            # Verify that the file exists
            if not os.path.exists(file_path):
                console.print(f"[red]{translator.get('error_file_not_exists')} {file_path}[/red]")
                return None
                
            # Add the application's root directory to sys.path
            file_dir = os.path.dirname(os.path.abspath(file_path))
            if file_dir not in sys.path:
                sys.path.insert(0, file_dir)
                
            # Load the module dynamically
            spec = importlib.util.spec_from_file_location("user_app", file_path)
            if spec is None or spec.loader is None:
                console.print(f"[red]{translator.get('error_file_load')} {file_path}[/red]")
                return None
                
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            # Look for the 'app' variable in the module
            if hasattr(module, 'app') and isinstance(module.app, App):
                return module.app
            else:
                console.print(f"[red]{translator.get('error_no_app_var')} {file_path}[/red]")
                return None
                
        except Exception as e:
            console.print(f"[red]{translator.get('error_loading_file')}: {e}[/red]")
            return None
            
    def validate_app(self, app: App) -> bool:
        """Validates a Dars application"""
        errors = app.validate()
        
        if errors:
            console.print(f"[red]{translator.get('validation_errors')}[/red]")
            for error in errors:
                console.print(f"  • {error}")
            return False
            
        return True
        
    def export_app(self, app: App, format_name: str, output_path: str, show_preview: bool = False, bundle: Optional[bool] = None) -> bool:
        """Exports an application to the specified format"""
        # Normalize early so availability check works
        if format_name == 'html':
            format_name = 'web'

        if format_name not in self.exporters:
            console.print(f"[red]{translator.get('error_format_not_supported')} '{format_name}'[/red]")
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
            
            # Validation task
            task1 = progress.add_task(translator.get('validating_app'), total=100)
            progress.update(task1, advance=30)
            
            if not self.validate_app(app):
                progress.update(task1, completed=100)
                return False
                
            progress.update(task1, advance=70)
            
            # Export task
            task2 = progress.add_task(f"{translator.get('exporting_to')} {format_name}...", total=100)
            progress.update(task2, advance=20)
            
            try:
                # Determine effective bundle behavior: explicit param overrides default
                effective_bundle = True if bundle is None else bool(bundle)
                # En CLI 'dars export' default is to generate a bundle (bundle=True)
                success = exporter.export(app, output_path, bundle=effective_bundle)
                progress.update(task2, advance=80)
                
                if success:
                    # Minification progress display: prefer precomputed label
                    try:
                        from dars.security import minify_output_dir
                        label_key = os.environ.get('DARS_MINIFY_LABEL', '')
                        label = None
                        if label_key == 'default+vite':
                            label = "Applying minification (default + vite)"
                        elif label_key == 'default':
                            label = "Applying minification (default)"
                        elif label_key == 'vite':
                            label = "Applying minification (vite)"
                        if label is None:
                            # Fallback detection
                            default_min = os.environ.get('DARS_DEFAULT_MINIFY', '1') != '0'
                            vite_enabled_env = os.environ.get('DARS_VITE_MINIFY', '1') == '1'
                            use_vite = False
                            try:
                                from dars.core.js_bridge import vite_available as _vite_available, esbuild_available as _esbuild_available
                                use_vite = vite_enabled_env and (_vite_available() or _esbuild_available())
                            except Exception:
                                use_vite = False
                            if default_min and use_vite:
                                label = "Applying minification (default + vite)"
                            elif default_min:
                                label = "Applying minification (default)"
                            elif use_vite:
                                label = "Applying minification (vite)"

                        default_min_run = os.environ.get('DARS_DEFAULT_MINIFY', '1') != '0'
                        if default_min_run and label:
                            task3 = progress.add_task(label, total=1)
                            totals = {"total": 1, "inited": False}
                            def _cb(done, total):
                                if not totals["inited"] and total > 0:
                                    progress.update(task3, total=total)
                                    totals["total"] = total
                                    totals["inited"] = True
                                progress.update(task3, completed=done)
                            _ = minify_output_dir(output_path, progress_cb=_cb)
                            progress.update(task3, completed=totals.get("total", 1))
                        elif label == "Applying minification (vite)":
                            # Run vite-only minification over JS/CSS via security (HTML will be skipped)
                            task3 = progress.add_task(label, total=1)
                            totals = {"total": 1, "inited": False}
                            def _cb(done, total):
                                if not totals["inited"] and total > 0:
                                    progress.update(task3, total=total)
                                    totals["total"] = total
                                    totals["inited"] = True
                                progress.update(task3, completed=done)
                            _ = minify_output_dir(output_path, progress_cb=_cb)
                            progress.update(task3, completed=totals.get("total", 1))
                    except Exception:
                        pass
                    progress.update(task1, completed=100)
                    progress.update(task2, completed=100)
                    
                    # Show success information
                    self.show_export_success(app, format_name, output_path)
                    
                    if show_preview and format_name == 'html':
                        self.show_preview_info(output_path)
                        
                    return True
                else:
                    console.print(f"[red]{translator.get('error_during_export')} {format_name}[/red]")
                    return False
                    
            except Exception as e:
                console.print(f"[red]{translator.get('error_during_export_exception')}: {e}[/red]")
                return False
                
    def show_supported_formats(self):
        """Shows supported formats"""
        table = Table(title=translator.get('supported_export_formats'))
        table.add_column(translator.get('format_name'), style="cyan")
        table.add_column(translator.get('format_description'), style="white")
        table.add_column(translator.get('html_description'), style="green")
        
        formats_info = {
            'web': ('HTML/CSS/JavaScript', 'Web'),
            'html': ('HTML/CSS/JavaScript (legacy alias)', 'Web'),
            'desktop': ('Electron (HTML/CSS/JS + Bridge)', 'Desktop'),
        }
        
        for format_name, (description, platform) in formats_info.items():
            table.add_row(format_name, description, platform)
            
        console.print(table)
        
    def show_export_success(self, app: App, format_name: str, output_path: str):
        """Shows export success information"""
        stats = app.get_stats()
        
        panel_content = f"""
[green]✓[/green] {translator.get('export_completed_successfully')}

[bold]{translator.get('application')}:[/bold] {app.title}
[bold]{translator.get('format')}:[/bold] {format_name}
[bold]{translator.get('output_directory')}:[/bold] {output_path}

[bold]{translator.get('statistics')}:[/bold]
• {translator.get('total_components')}: {stats['total_components']}
• {translator.get('total_pages')}: {stats.get('total_pages', 1)}
• {translator.get('max_depth')}: {stats['max_depth']}
• {translator.get('scripts')}: {stats['scripts_count']}
• {translator.get('global_styles')}: {stats['global_styles_count']}
"""
        
        console.print(Panel(panel_content, title=translator.get('export_successful'), border_style="green"))
        
    def show_preview_info(self, output_path: str):
        """Shows information about how to preview the application"""
        index_path = os.path.join(output_path, "index.html")
        
        if os.path.exists(index_path):
            console.print(f"\n[bold cyan]{translator.get('to_preview_app')}:[/bold cyan]")
            console.print(f"  {translator.get('open_in_browser')}: file://{os.path.abspath(index_path)}")
            console.print(f"  {translator.get('or_use')}: dars preview {output_path}")
            
    def show_app_info(self, app: App):
        """Shows detailed information about the application"""
        stats = app.get_stats()
        
        # Basic information
        info_table = Table(title=f"{translator.get('app_information')}: {app.title}")
        info_table.add_column(translator.get('property_column'), style="cyan")
        info_table.add_column(translator.get('value_column'), style="white")
        
        info_table.add_row(translator.get('title'), app.title)
        info_table.add_row(translator.get('total_components'), str(stats['total_components']))
        info_table.add_row(translator.get('max_depth'), str(stats['max_depth']))
        info_table.add_row(translator.get('scripts'), str(stats['scripts_count']))
        info_table.add_row(translator.get('global_styles'), str(stats['global_styles_count']))
        info_table.add_row(translator.get('theme'), app.config.get('theme', 'light'))
        
        console.print(info_table)
        
        # Component tree
        if app.root:
            console.print(f"\n[bold]{translator.get('component_structure')}:[/bold]")
            self.print_component_tree(app.root)
            
    def print_component_tree(self, component, level: int = 0):
        """Prints the component tree"""
        indent = "  " * level
        component_name = component.__class__.__name__
        component_id = f" (id: {component.id})" if component.id else ""
        
        console.print(f"{indent}├─ {component_name}{component_id}")
        
        for child in component.children:
            self.print_component_tree(child, level + 1)
    

    def init_project(self, name: str, template: Optional[str] = None, proj_type: str = 'web'):
        """Initializes a base Dars project, optionally using a template"""
        if os.path.exists(name):
            console.print(f"[red]❌ {translator.get('directory_exists').format(name=name)}[/red]")
            return

        # Create project directory
        os.makedirs(name)
        console.print(f"[green]✔ {translator.get('directory_created').format(name=name)}[/green]")

        if template:
            # Get template information
            templates = list_templates()
            if template not in templates:
                console.print(f"[red]❌ {translator.get('template_not_found').format(template=template)}[/red]")
                return
                
            template_info = templates[template]
            template_dir = template_info['template_dir']
            extra_files = template_info['extra_files']

            if not extra_files:
                console.print(f"[yellow]⚠ {translator.get('template_empty').format(template=template)}[/yellow]")
                return

            # Copy ALL files (no main_file anymore)
            for extra_file in extra_files:
                src_file = template_dir / extra_file
                dest_file = os.path.join(name, extra_file)
                
                # Create directories if needed
                os.makedirs(os.path.dirname(dest_file), exist_ok=True)
                
                if src_file.exists():
                    shutil.copy2(src_file, dest_file)
                    console.print(f"[green]✔ {translator.get('extra_file_copied').format(file=extra_file)}[/green]")

            console.print(f"[green]✔ {translator.get('template_copied').format(template=template)}[/green]")
        elif str(proj_type).lower() == 'desktop':
            # Use the default desktop template from dars/templates/desktop/template/
            try:
                current_file = Path(__file__).resolve()
                template_dir = current_file.parent.parent / "templates" / "desktop" / "template"
                
                if not template_dir.exists():
                    console.print(f"[yellow]⚠ Desktop template directory not found, using default scaffold[/yellow]")
                    # Fall back to default hello world
                    HELLO_WORLD_CODE = """
from dars.all import *

app = App(title="Hello World", theme="dark", desktop=True)
# Crear componentes
index = Page(
    Text(
        text="Hello World",
        style={
            'font-size': '48px',
            'color': '#2c3e50',
            'margin-bottom': '20px',
            'font-weight': 'bold',
            'text-align': 'center'
        }
    ),
    Text(
        text="Hello World",
        style={
            'font-size': '20px',
            'color': '#7f8c8d',
            'margin-bottom': '40px',
            'text-align': 'center'
        }
    ),

    Button(
        text="Click Me!",
        on_click= dScript("alert('Hello World')"),
        on_mouse_enter=dScript("this.style.backgroundColor = '#2980b9';"),
        on_mouse_leave=dScript("this.style.backgroundColor = '#3498db';"),
        style={
            'background-color': '#3498db',
            'color': 'white',
            'padding': '15px 30px',
            'border': 'none',
            'border-radius': '8px',
            'font-size': '18px',
            'cursor': 'pointer',
            'transition': 'background-color 0.3s'
        }
    ),
    style={
        'display': 'flex',
        'flex-direction': 'column',
        'align-items': 'center',
        'justify-content': 'center',
        'min-height': '100vh',
        'background-color': '#f0f2f5',
        'font-family': 'Arial, sans-serif'
    }
) 

app.add_page("index", index, title="Hello World", index=True)

if __name__ == "__main__":
    app.rTimeCompile()
"""
                    main_py = Path(name) / "main.py"
                    main_py.write_text(HELLO_WORLD_CODE.strip(), encoding="utf-8")
                    console.print(f"[green]✔ {translator.get('main_py_created')}[/green]")
                else:
                    # Copy all files from template directory, excluding __pycache__ and dars_preview
                    excluded_dirs = {'__pycache__', 'dars_preview'}
                    excluded_files = {'.pyc', '.pyo'}
                    
                    def should_copy(item_path: Path) -> bool:
                        """Check if a file/directory should be copied"""
                        # Skip excluded directories
                        if item_path.name in excluded_dirs:
                            return False
                        # Skip excluded file extensions
                        if item_path.suffix in excluded_files:
                            return False
                        return True
                    
                    def copy_template_recursive(src: Path, dst: Path):
                        """Recursively copy template files"""
                        if not should_copy(src):
                            return
                        
                        if src.is_dir():
                            dst.mkdir(parents=True, exist_ok=True)
                            for item in src.iterdir():
                                copy_template_recursive(item, dst / item.name)
                        else:
                            dst.parent.mkdir(parents=True, exist_ok=True)
                            shutil.copy2(src, dst)
                            # Show relative path from template dir
                            rel_path = src.relative_to(template_dir)
                            console.print(f"[green]✔ {rel_path} copied[/green]")
                    
                    # Copy all files from template
                    for item in template_dir.iterdir():
                        if should_copy(item):
                            dest_item = Path(name) / item.name
                            copy_template_recursive(item, dest_item)
                    
                    console.print("[green]✔ Desktop template copied[/green]")
            except Exception as e:
                console.print(f"[yellow]⚠ Could not copy desktop template: {e}, using default scaffold[/yellow]")
                # Fall back to default hello world
                HELLO_WORLD_CODE = """
from dars.all import *

app = App(title="Hello World", theme="dark", desktop=True)
# Crear componentes
index = Page(
    Text(
        text="Hello World",
        style={
            'font-size': '48px',
            'color': '#2c3e50',
            'margin-bottom': '20px',
            'font-weight': 'bold',
            'text-align': 'center'
        }
    ),
    Text(
        text="Hello World",
        style={
            'font-size': '20px',
            'color': '#7f8c8d',
            'margin-bottom': '40px',
            'text-align': 'center'
        }
    ),

    Button(
        text="Click Me!",
        on_click= dScript("alert('Hello World')"),
        on_mouse_enter=dScript("this.style.backgroundColor = '#2980b9';"),
        on_mouse_leave=dScript("this.style.backgroundColor = '#3498db';"),
        style={
            'background-color': '#3498db',
            'color': 'white',
            'padding': '15px 30px',
            'border': 'none',
            'border-radius': '8px',
            'font-size': '18px',
            'cursor': 'pointer',
            'transition': 'background-color 0.3s'
        }
    ),
    style={
        'display': 'flex',
        'flex-direction': 'column',
        'align-items': 'center',
        'justify-content': 'center',
        'min-height': '100vh',
        'background-color': '#f0f2f5',
        'font-family': 'Arial, sans-serif'
    }
) 

app.add_page("index", index, title="Hello World", index=True)

if __name__ == "__main__":
    app.rTimeCompile()
"""
                main_py = Path(name) / "main.py"
                main_py.write_text(HELLO_WORLD_CODE.strip(), encoding="utf-8")
                console.print(f"[green]✔ {translator.get('main_py_created')}[/green]")
        else:
            # Default Web/Fullstack Scaffold (based on initexample)
            
            # 1. apiConfig.py
            API_CONFIG_PY_CODE = """import os
import sys

class DarsEnv:
    # Set this to "production" when deploying
    MODE = "development" 
    
    DEV = "development"
    BUILD = "production"
    
    @staticmethod
    def get_env():
        return DarsEnv.MODE

    @staticmethod
    def is_dev():
        return DarsEnv.get_env() == DarsEnv.DEV

    @staticmethod
    def get_urls():
        # Configuration for URLs
        if DarsEnv.is_dev():
            return {
                "backend": "http://localhost:3000", # SSR/API Server
                "frontend": "http://localhost:8000" # Dev Server
            }
        return {
            "backend": "/", # Production: Same origin
            "frontend": "/"
        }
"""

            # 2. backend/api.py (No sys.path hacks, relies on python -m module execution)
            API_PY_CODE = """\"""
SSR Backend - Dars Framework
Run with: python -m backend.api
\"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dars.backend.ssr import create_ssr_app
import sys
import os
from backend.apiConfig import DarsEnv

# Import the Dars app
import sys
sys.path.insert(0, '.')
from main import app as dars_app


# Create FastAPI app with SSR support
app = create_ssr_app(dars_app)

# Enable CORS for local development
if DarsEnv.is_dev():
    urls = DarsEnv.get_urls()
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[urls['frontend'], "http://127.0.0.1:3000"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

if __name__ == "__main__":
    import uvicorn
    urls = DarsEnv.get_urls()
    print(" " + "="*60)
    print("Dars SSR Backend")
    print("="*60)
    print(f"Endpoints:")
    print(f" • {urls['backend']}/              - API info")
    print(f" • {urls['backend']}/api/ssr/*     - SSR routes")
    print(f"Frontend: {urls['frontend']}")
    print("="*60 + " ")
    
    uvicorn.run(app, host="127.0.0.1", port=3000)
"""

            # 3. separate templates logic
            
            # Template for 'ssr' type
            SSR_TEMPLATE_CODE = """from dars.all import *
from backend.apiConfig import DarsEnv

# Configure SSR URL
# In dev: http://localhost:8000
# In prod: / (same origin)
ssr_url = DarsEnv.get_urls()['backend']

app = App(title="Hello World", theme="dark", ssr_url=ssr_url)

# 1. Define State
state = State("app", title_val="Simple Counter", count=0)

# 2. Define Route
@route("/", route_type=RouteType.SSR)
def index(): 
    return Page(
        # 3. Use useValue for app text
        Text(
            text=useValue("app.title_val"),
            style="fs-[33px] text-black font-bold mb-[5x] ",
        ),

        # 4. Display reactive count
        Text(
            text=useDynamic("app.count"),
            style="fs-[48px] mt-5 mb-[12px]"
        ),
        # 5. Interactive Button
        Button(
            text="+1",
            on_click=(
                state.count.increment(1)
            ),
            style="bg-[#3498db] text-white p-[15px] px-[30px] rounded-[8px] border-none cursor-pointer fs-[18px]",
        ),

        # 6. Interactive Button
        Button(
            text="-1",
            on_click=(
                state.count.decrement(1)
            ),
            style="bg-[#3498db] text-white p-[15px] px-[30px] rounded-[8px] border-none cursor-pointer fs-[18px] mt-[5px]",
        ),
        # 7. Interactive Button
        Button(
            text="Reset",
            on_click=(
                state.reset()
            ),
            style="bg-[#3498db] text-white p-[15px] px-[30px] rounded-[8px] border-none cursor-pointer fs-[18px] mt-[5px]",
        ),
        style="flex flex-col items-center justify-center h-[100vh] ffam-[Arial] bg-[#f0f2f5]",

    ) 

# 8. Add page
app.add_page("index", index(), title="index")

# 9. Run app with preview
if __name__ == "__main__":
    app.rTimeCompile()
"""

            # Template for 'web' type (default SPA)
            SPA_TEMPLATE_CODE = """from dars.all import *

app = App(title="Hello World", theme="dark")

# 1. Define State
state = State("app", title_val="Simple Counter", count=0)

# 2. Define Route
@route("/")
def index(): 
    return Page(
        # 3. Use useValue for app text
        Text(
            text=useValue("app.title_val"),
            style="fs-[33px] text-black font-bold mb-[5x] ",
        ),

        # 4. Display reactive count
        Text(
            text=useDynamic("app.count"),
            style="fs-[48px] mt-5 mb-[12px]"
        ),
        # 5. Interactive Button
        Button(
            text="+1",
            on_click=(
                state.count.increment(1)
            ),
            style="bg-[#3498db] text-white p-[15px] px-[30px] rounded-[8px] border-none cursor-pointer fs-[18px]",
        ),

        # 6. Interactive Button
        Button(
            text="-1",
            on_click=(
                state.count.decrement(1)
            ),
            style="bg-[#3498db] text-white p-[15px] px-[30px] rounded-[8px] border-none cursor-pointer fs-[18px] mt-[5px]",
        ),
        # 7. Interactive Button
        Button(
            text="Reset",
            on_click=(
                state.reset()
            ),
            style="bg-[#3498db] text-white p-[15px] px-[30px] rounded-[8px] border-none cursor-pointer fs-[18px] mt-[5px]",
        ),
        style="flex flex-col items-center justify-center h-[100vh] ffam-[Arial] bg-[#f0f2f5]",

    ) 

# 8. Add page
app.add_page("index", index(), title="index")

# 9. Run app with preview
if __name__ == "__main__":
    app.rTimeCompile()
"""
            
            # 4. dars.config.json
            # Default config for SPA / desktop projects
            DARS_CONFIG_JSON_CODE = """{
  "entry": "main.py",
  "format": "web",
  "outdir": "dist",
  "include": [],
  "exclude": [
    "**/__pycache__",
    ".git",
    ".venv",
    "node_modules"
  ],
  "bundle": true,
  "defaultMinify": true,
  "viteMinify": true,
  "markdownHighlight": true,
  "markdownHighlightTheme": "auto",
  "utility_styles": {}
}"""

            # Config template for SSR projects: includes backendEntry pointing to the default backend
            DARS_CONFIG_JSON_SSR_CODE = """{
  "entry": "main.py",
  "format": "web",
  "outdir": "dist",
  "include": [],
  "exclude": [
    "**/__pycache__",
    ".git",
    ".venv",
    "node_modules"
  ],
  "bundle": true,
  "defaultMinify": true,
  "viteMinify": true,
  "markdownHighlight": true,
  "markdownHighlightTheme": "auto",
  "utility_styles": {},
  "backendEntry": "backend.api:app"
}"""

            # Write Initial Files
            root_path = Path(name)
            
            if proj_type == 'ssr':
                # write SSR template
                (root_path / "main.py").write_text(SSR_TEMPLATE_CODE.strip(), encoding="utf-8")
                console.print(f"[green]✔ {translator.get('main_py_created')} (SSR Mode)[/green]")
                
                # Create config json for SSR projects, including backendEntry pointing to backend/api.py
                (root_path / "dars.config.json").write_text(DARS_CONFIG_JSON_SSR_CODE.strip(), encoding="utf-8")
                
                # Backend Directory (Only for SSR)
                backend_dir = root_path / "backend"
                backend_dir.mkdir(exist_ok=True)
                (backend_dir / "__init__.py").touch()
                (backend_dir / "api.py").write_text(API_PY_CODE.strip(), encoding="utf-8")
                (backend_dir / "apiConfig.py").write_text(API_CONFIG_PY_CODE.strip(), encoding="utf-8")
                console.print(f"[green]✔ Fullstack scaffold created (backend, apiConfig, main.py)[/green]")
            else:
                # Default Web/SPA
                (root_path / "main.py").write_text(SPA_TEMPLATE_CODE.strip(), encoding="utf-8")
                console.print(f"[green]✔ {translator.get('main_py_created')} (SPA Mode)[/green]")
                (root_path / "dars.config.json").write_text(DARS_CONFIG_JSON_CODE.strip(), encoding="utf-8")


        # Create default dars.config.json for the new project
        try:
            project_root = os.path.abspath(name)
            write_default_config(project_root, overwrite=False)
            if str(proj_type).lower() == 'desktop':
                try:
                    update_config(project_root, {"format": "desktop"})
                except Exception:
                    pass
            console.print("[green]✔ dars.config.json created[/green]")
        except Exception:
            # Non-fatal; keep init working even if config write fails
            pass

        # Desktop backend scaffold (only if template was not used, as template already includes backend)
        if str(proj_type).lower() == 'desktop' and template is None:
            try:
                backend_dir = Path(name) / 'backend'
                # Check if backend already exists (from template)
                if not backend_dir.exists():
                    backend_dir.mkdir(parents=True, exist_ok=True)
                    # package.json (CJS)
                    backend_pkg = '{\n' + \
                        '  "name": "dars-electron-backend",\n' + \
                        '  "private": true,\n' + \
                        '  "main": "main.js",\n' + \
                        '  "scripts": {"start": "electron ."},\n' + \
                        '  "devDependencies": {"electron": "39.2.6"}\n' + \
                    '}\n'
                    (backend_dir / 'package.json').write_text(backend_pkg, encoding='utf-8')
                    # main.js
                    backend_main = "const { app, BrowserWindow, Menu, ipcMain } = require('electron');\n" + \
                        "const path = require('path');\n" + \
                        "const fs = require('fs').promises;\n" + \
                        "const http = require('http');\n\n" + \
                        "function createWindow() {\n" + \
                        "  const win = new BrowserWindow({\n" + \
                        "    width: 1000, height: 700,\n" + \
                        "    webPreferences: {\n" + \
                        "      contextIsolation: true,\n" + \
                        "      preload: path.join(__dirname, 'preload.js')\n" + \
                        "    }\n" + \
                        "  });\n" + \
                        "  Menu.setApplicationMenu(null);\n" + \
                        "  win.loadFile(path.join(__dirname, 'app', 'index.html'));\n" + \
                        "}\n\n" + \
                        "app.whenReady().then(() => {\n" + \
                        "  createWindow();\n" + \
                        "  app.on('activate', function () {\n" + \
                        "    if (BrowserWindow.getAllWindows().length === 0) createWindow();\n" + \
                        "  });\n" + \
                        "});\n\n" + \
                                        "// Utility to resolve paths: absolute paths are used as-is; relative paths resolve against process.cwd()\n" + \
                                        "function resolvePath(p) {\n" + \
                                        "  if (!p || typeof p !== 'string') throw new Error('filePath must be a string');\n" + \
                                        "  if (path.isAbsolute(p)) return p;\n" + \
                                        "  return path.resolve(process.cwd(), p);\n" + \
                                        "}\n\n" + \
                                        "function closeAllAndExit() {\n" + \
                                        "  try {\n" + \
                                        "    const wins = BrowserWindow.getAllWindows();\n" + \
                                        "    wins.forEach(w => { try { w.close(); } catch(e) {} });\n" + \
                                        "  } catch (e) {}\n" + \
                                        "  setTimeout(() => { try { app.quit(); } catch(e) {} }, 300);\n" + \
                                        "}\n\n" + \
                                        "// Allow renderer to request graceful shutdown\n" + \
                                        "ipcMain.handle('dars::dev::shutdown', async () => {\n" + \
                                        "  closeAllAndExit();\n" + \
                                        "  return true;\n" + \
                                        "});\n\n" + \
                                        "// HTTP control server for external processes (e.g., Python dev launcher)\n" + \
                                        "const controlPort = process.env.DARS_CONTROL_PORT;\n" + \
                                        "if (controlPort) {\n" + \
                                        "  try {\n" + \
                                        "    const server = http.createServer((req, res) => {\n" + \
                                        "      if (req.method === 'POST' && req.url === '/__dars_shutdown') {\n" + \
                                        "        closeAllAndExit();\n" + \
                                        "        res.writeHead(200); res.end('ok');\n" + \
                                        "        return;\n" + \
                                        "      }\n" + \
                                        "      res.writeHead(404); res.end('not-found');\n" + \
                                        "    });\n" + \
                                        "    server.listen(Number(controlPort), '127.0.0.1');\n" + \
                                        "  } catch (e) { /* ignore */ }\n" + \
                                        "}\n\n" + \
                                        "// IPC handlers for Dars desktop API\n" + \
                                        "ipcMain.handle('dars::FileSystem::read_text', async (_e, filePath, encoding = 'utf-8') => {\n" + \
                                        "  const resolved = resolvePath(filePath);\n" + \
                                        "  const content = await fs.readFile(resolved, { encoding });\n" + \
                                        "  return content;\n" + \
                                        "});\n\n" + \
                                        "ipcMain.handle('dars::FileSystem::write_text', async (_e, filePath, data, encoding = 'utf-8') => {\n" + \
                                        "  const resolved = resolvePath(filePath);\n" + \
                                        "  if (typeof data !== 'string') data = String(data ?? '');\n" + \
                                        "  await fs.writeFile(resolved, data, { encoding });\n" + \
                                        "  return true;\n" + \
                                        "});\n\n" + \
                                        "ipcMain.on('dars::console', (event, type, ...args) => {\n" + \
                                        "  console.log(`[Renderer ${type.toUpperCase()}]`, ...args);\n" + \
                                        "});\n\n" + \
                                        "app.on('window-all-closed', function () {\n" + \
                                        "  if (process.platform !== 'darwin') app.quit();\n" + \
                                        "});\n"
                (backend_dir / 'main.js').write_text(backend_main, encoding='utf-8')
                # preload.js
                backend_preload = "const { contextBridge, ipcRenderer } = require('electron');\n" + \
                    "\n" + \
                    "// Override console to send logs to main process\n" + \
                    "const methods = ['log', 'warn', 'error', 'info', 'debug'];\n" + \
                    "methods.forEach(method => {\n" + \
                    "    const original = console[method];\n" + \
                    "    console[method] = (...args) => {\n" + \
                    "        original(...args);\n" + \
                    "        try {\n" + \
                    "            ipcRenderer.send('dars::console', method, ...args.map(a => {\n" + \
                    "                try {\n" + \
                    "                    return typeof a === 'object' ? JSON.stringify(a) : String(a);\n" + \
                    "                } catch(e) {\n" + \
                    "                    return String(a);\n" + \
                    "                }\n" + \
                    "            }));\n" + \
                    "        } catch(e) {}\n" + \
                    "    };\n" + \
                    "});\n\n" + \
                    "contextBridge.exposeInMainWorld('DarsIPC', {\n" + \
                    "  invoke: (channel, ...args) => ipcRenderer.invoke(channel, ...args)\n" + \
                    "});\n" + \
                    "// Also expose a minimal DarsDesktopAPI for renderer convenience\n" + \
                    "contextBridge.exposeInMainWorld('DarsDesktopAPI', {\n" + \
                    "  FileSystem: {\n" + \
                    "    read_text: (...args) => ipcRenderer.invoke('dars::FileSystem::read_text', ...args),\n" + \
                    "    write_text: (...args) => ipcRenderer.invoke('dars::FileSystem::write_text', ...args)\n" + \
                    "  }\n" + \
                    "});\n" + \
                    "// Dev helpers: request graceful shutdown from Python dev launcher\n" + \
                    "contextBridge.exposeInMainWorld('DarsDev', {\n" + \
                    "  shutdown: () => ipcRenderer.invoke('dars::dev::shutdown')\n" + \
                    "});\n"
                (backend_dir / 'preload.js').write_text(backend_preload, encoding='utf-8')
                console.print("[green]✔ backend/ scaffold created[/green]")
                
                # Copy default icon to icons/ directory (only if not already exists from template)
                try:
                    icons_dir = Path(name) / 'icons'
                    icons_dir.mkdir(parents=True, exist_ok=True)
                    # Get path to default icon in templates/desktop
                    current_file = Path(__file__).resolve()
                    default_icon_src = current_file.parent.parent / "templates" / "desktop" / "icon.png"
                    if default_icon_src.exists():
                        default_icon_dest = icons_dir / "icon.png"
                        if not default_icon_dest.exists():
                            shutil.copy2(default_icon_src, default_icon_dest)
                            console.print("[green]✔ icons/icon.png created[/green]")
                except Exception as e:
                    console.print(f"[yellow]Warning: could not copy default icon: {e}[/yellow]")
            except Exception as e:
                console.print(f"[yellow]Warning: could not create backend scaffold: {e}[/yellow]")

        # Final instructions removed per request

def print_version_info():
    import importlib.util
    import os
    from rich.panel import Panel
    from rich.console import Console
    console = Console()
    version_path = os.path.join(os.path.dirname(__file__), '../version.py')
    spec = importlib.util.spec_from_file_location("dars.version", version_path)
    version_mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(version_mod)
    version = getattr(version_mod, "__version__", "unknown")
    release_url = getattr(version_mod, "__release_url__", "https://github.com/ZtaMDev/Dars-Framework/releases")
    panel_content = f"[bold cyan]Dars Framework[/bold cyan]\n\n[green]Version:[/green] {version}\n[green]Release notes:[/green] [link={release_url}]{release_url}[/link]"
    console.print(Panel(panel_content, title="Dars Version", border_style="cyan"))

def create_parser(include_hidden: bool = True) -> argparse.ArgumentParser:
    """Creates the command line argument parser"""
    parser = argparse.ArgumentParser(
        description=translator.get('main_description'),
        formatter_class=argparse.HelpFormatter,
        epilog=""
    )
    parser.add_argument('-v', '--version', action='store_true', help='Show Dars version and release link')
    
    # English-only: no language flag
    
    subparsers = parser.add_subparsers(
        dest='command',
        help=translator.get('available_commands'),
        metavar='{export,info,formats,preview,init,build,config,dev,doctor}'
    )
    
    # Export command
    export_parser = subparsers.add_parser('export', help=translator.get('export_help'))
    export_parser.add_argument('file', help=translator.get('file_help'))

    # --format opcional (default: html)
    export_parser.add_argument(
        '--format', '-f',
        choices=["web", "html", "desktop"],
        default="web",
        help=translator.get('format_help') + " (default: web)"
    )

    # --output opcional (default: ./dist)
    export_parser.add_argument(
        '--output', '-o',
        default="./dist",
        help=translator.get('output_help') + " (default: ./dist)"
    )

    export_parser.add_argument('--preview', '-p', action='store_true',
                            help=translator.get('preview_help'))
    # disable python-side default minifier
    export_parser.add_argument('--no-minify', action='store_true', help='Disable default Python minifier for this run')

    
    # Info command
    info_parser = subparsers.add_parser('info', help=translator.get('info_help'))
    info_parser.add_argument('file', help=translator.get('file_help'))
    
    # Formats command
    formats_parser = subparsers.add_parser('formats', help=translator.get('formats_help'))
    
    # Preview command
    preview_parser = subparsers.add_parser('preview', help=translator.get('preview_cmd_help'))
    preview_parser.add_argument('path', help=translator.get('path_help'))
    
    init_parser = subparsers.add_parser('init', help=translator.get('init_help'))
    init_parser.add_argument('name', nargs='?', help=translator.get('name_help'))
    init_parser.add_argument(
        '--list-templates', '-L',  # Cambia -l por -L
        action='store_true',
        help=translator.get('list_templates_help')
    )
    init_parser.add_argument(
        '--template', '-t',
        help=translator.get('template_help')
    )
    init_parser.add_argument(
        '--update', '-u',
        action='store_true',
        help='Create or update dars.config.json in the target (or current) directory'
    )
    init_parser.add_argument(
        '--type', '-T', choices=['web', 'desktop', 'ssr'], default='web',
        help='Project type scaffold (web | desktop | ssr). Default: web'
    )

    # Build command (config-driven)
    build_parser = subparsers.add_parser('build', help='Build using dars.config.json')
    build_parser.add_argument(
        '--project', '-p', default='.', help='Project root where dars.config.json resides (default: .)'
    )
    # disable python-side default minifier
    build_parser.add_argument('--no-minify', action='store_true', help='Disable default Python minifier for this build')

    # Config command (validate)
    config_parser = subparsers.add_parser('config', help='Manage and validate dars.config.json')
    cfg_subparsers = config_parser.add_subparsers(dest='config_command')
    cfg_validate = cfg_subparsers.add_parser('validate', help='Validate dars.config.json in a project')
    cfg_validate.add_argument('--project', '-p', default='.', help='Project root (default: .)')

    # Dev command (run entry in dev mode)
    dev_parser = subparsers.add_parser('dev', help='Run the configured entry file in development mode')
    dev_parser.add_argument('--project', '-p', default='.', help='Project root where dars.config.json resides (default: .)')
    dev_parser.add_argument('--backend', action='store_true', help='Run only the configured backendEntry (SSR/API) instead of the frontend entry')
    # English-only: no language option on subparsers
    
    # Doctor command
    doctor_parser = subparsers.add_parser('doctor', help='Check and install required external tools (Node LTS, Bun) and Python deps')
    doctor_parser.add_argument('--check', action='store_true', help='Only verify environment and exit non-zero if missing')
    doctor_parser.add_argument('--yes', '-y', action='store_true', help='Assume yes for all prompts')
    doctor_parser.add_argument('--all', action='store_true', help='Install all missing items (with --yes for non-interactive)')
    doctor_parser.add_argument('--force', action='store_true', help='Re-run checks even if environment was previously satisfied')

    # Hidden forced installer (conditionally added to avoid appearing in help)
    if include_hidden:
        forcedev_parser = subparsers.add_parser('forcedev', help=argparse.SUPPRESS)

    return parser


from pathlib import Path
from typing import Dict

def list_templates(debug: bool = False) -> Dict[str, Dict]:
    """
    Descubre templates:
    - ignora dirs en IGNORED_DIRS (ej: __pycache__, .git, node_modules)
    - ignora extensiones compiladas ('.pyc', '.pyo', '.pyd')
    - ignora solo archivos ocultos que empiezan con '.' (ej: .env)
    - incluye TODOS los demás archivos ('.py', '.md', '.png', '.json', etc.)
    - salida determinista (ordenada)
    """
    current_file = Path(__file__).resolve()
    templates_base = current_file.parent.parent / "templates" / "examples"

    if not templates_base.exists():
        # usa console.print si tienes rich.console; aquí dejo print para compatibilidad
        print(f"[red]Error: Template directory not found: {templates_base}[/red]")
        return {}

    IGNORED_DIRS = {'__pycache__', '.git', '.venv', 'node_modules', '.pytest_cache'}
    IGNORE_EXTS = {'.pyc', '.pyo', '.pyd'}

    templates: Dict[str, Dict] = {}

    for category_dir in sorted(templates_base.iterdir()):
        if not (category_dir.is_dir() and not category_dir.name.startswith('__')):
            continue

        for template_dir in sorted(category_dir.iterdir()):
            if not (template_dir.is_dir() and not template_dir.name.startswith('__')):
                continue

            found_files = []
            for file_path in sorted(template_dir.rglob('*')):
                # 1) archivo
                if not file_path.is_file():
                    if debug: print(f"SKIP (not file): {file_path}")
                    continue

                # 2) si alguna parte del path es una carpeta ignorada
                intersect = set(file_path.parts) & IGNORED_DIRS
                if intersect:
                    if debug: print(f"SKIP (ignored dir {intersect}): {file_path}")
                    continue

                # 3) extensiones compiladas
                if file_path.suffix.lower() in IGNORE_EXTS:
                    if debug: print(f"SKIP (ignored ext): {file_path}")
                    continue

                # 4) solo ocultos que empiezan con '.' (por ejemplo .gitignore, .env)
                if file_path.name.startswith('.'):
                    if debug: print(f"SKIP (hidden file): {file_path}")
                    continue

                # si pasó todos los filtros, lo guardamos (ruta relativa al template)
                rel = str(file_path.relative_to(template_dir))
                if debug: print(f"INCLUDE: {rel}")
                found_files.append(rel)

            found_files = sorted(found_files)

            template_key = f"{category_dir.name}/{template_dir.name}"
            templates[template_key] = {
                'main_file': None,            # ya no usamos main_file
                'extra_files': found_files,
                'category': category_dir.name,
                'template_dir': template_dir,
                'all_files': found_files
            }

    return templates



                    
def list_templates_detailed():
    """Muestra información detallada de los templates disponibles"""
    templates = list_templates()
    
    if not templates:
        console.print("[yellow]No templates found[/yellow]")
        return
    
    table = Table(title="Available Templates")
    table.add_column("Template", style="cyan")
    table.add_column("Category", style="green")
    table.add_column("Extra Files", style="white")
    table.add_column("Description", style="dim")
    
    for template_name, template_info in templates.items():
        extra_files = ", ".join(template_info['extra_files']) if template_info['extra_files'] else "None"
        table.add_row(
            template_name,
            template_info['category'],
            extra_files,
            f"Template with {len(template_info['extra_files'])} extra files"
        )
    
    console.print(table)
def main():
    """Main CLI function"""
    # English-only: no language parameter pre-scan
    
    # Intercept only when no args provided; otherwise let argparse show the correct subcommand help
    if len(sys.argv) == 1:
        parser = create_parser(include_hidden=False)
        pretty_print_help(parser)
        return
    
    # Continue with normal flow if not help
    # If user asked for top-level help (no subcommand), build parser without hidden commands
    known_cmds = ['export','info','formats','preview','init','build','config','dev','doctor']
    top_level_help = ('-h' in sys.argv or '--help' in sys.argv) and not any(cmd in sys.argv for cmd in known_cmds)
    parser = create_parser(include_hidden=not top_level_help)
    if top_level_help:
        pretty_print_help(create_parser(include_hidden=False))
        return
    args = parser.parse_args()
    
    # Set language from args only if explicitly provided
    # This is already handled in the pre-parsing step above, so we don't need to do it again
    # The translator will already have the correct language set
    
    # Show version and exit if -v/--version is passed
    if getattr(args, 'version', False):
        print_version_info()
        sys.exit(0)

    # No banner for normal commands; keep output minimal
    
    exporter = DarsExporter()
    
    
    if args.command == 'export':
        # If file points to config, resolve from dars.config.json
        file_arg = args.file
        if file_arg in ('.', 'config', 'cfg'):
            project_root = os.getcwd()
            cfg, _found = load_config(project_root)
            resolved = resolve_paths(cfg, project_root)
            file_arg = resolved.get('entry_abs') or os.path.join(project_root, cfg.get('entry', 'main.py'))

        # Validate entry file exists
        if not os.path.exists(file_arg):
            console.print(f"[red]{translator.get('error_entry_not_found_in_config')}: {file_arg}[/red]")
            console.print(f"[yellow]{translator.get('edit_config_hint')}[/yellow]")
            sys.exit(1)

        # Load application
        app = exporter.load_app_from_file(file_arg)
        if app is None:
            sys.exit(1)
            
        # Export
        # If config exists and user didn't override output explicitly, use cfg.outdir
        project_root = os.path.dirname(os.path.abspath(file_arg))
        cfg, cfg_found = load_config(project_root)
        # Apply viteMinify setting to env for downstream minifier
        try:
            vite_flag = cfg.get('viteMinify', True)
            os.environ['DARS_VITE_MINIFY'] = '1' if vite_flag else '0'
        except Exception:
            pass
        # Apply defaultMinify from config and CLI override
        try:
            default_min = cfg.get('defaultMinify', True)
            if getattr(args, 'no_minify', False):
                os.environ['DARS_DEFAULT_MINIFY'] = '0'
            else:
                os.environ['DARS_DEFAULT_MINIFY'] = '1' if default_min else '0'
        except Exception:
            pass
        # Ensure default minifier uses fallback-only (no external tools) when enabled
        try:
            os.environ['DARS_DEFAULT_MINIFY_ONLY_FALLBACK'] = '1' if os.environ.get('DARS_DEFAULT_MINIFY', '1') != '0' else '0'
        except Exception:
            pass
        # Precompute label for exporter
        try:
            from dars.core.js_bridge import vite_available as _vite_available, esbuild_available as _esbuild_available
            use_vite = (os.environ.get('DARS_VITE_MINIFY', '1') == '1') and (_vite_available() or _esbuild_available())
            use_default = (os.environ.get('DARS_DEFAULT_MINIFY', '1') != '0')
            if use_default and use_vite:
                os.environ['DARS_MINIFY_LABEL'] = 'default+vite'
            elif use_default:
                os.environ['DARS_MINIFY_LABEL'] = 'default'
            elif use_vite:
                os.environ['DARS_MINIFY_LABEL'] = 'vite'
            else:
                os.environ['DARS_MINIFY_LABEL'] = ''
        except Exception:
            os.environ['DARS_MINIFY_LABEL'] = ''
        # Apply defaultMinify from config and CLI override
        try:
            default_min = cfg.get('defaultMinify', True)
            if getattr(args, 'no_minify', False):
                os.environ['DARS_DEFAULT_MINIFY'] = '0'
            else:
                os.environ['DARS_DEFAULT_MINIFY'] = '1' if default_min else '0'
        except Exception:
            pass
        # Ensure default minifier uses fallback-only (no external tools) when enabled
        try:
            os.environ['DARS_DEFAULT_MINIFY_ONLY_FALLBACK'] = '1' if os.environ.get('DARS_DEFAULT_MINIFY', '1') != '0' else '0'
        except Exception:
            pass
        # Precompute label for exporter
        try:
            from dars.core.js_bridge import vite_available as _vite_available, esbuild_available as _esbuild_available
            use_vite = (os.environ.get('DARS_VITE_MINIFY', '1') == '1') and (_vite_available() or _esbuild_available())
            use_default = (os.environ.get('DARS_DEFAULT_MINIFY', '1') != '0')
            if use_default and use_vite:
                os.environ['DARS_MINIFY_LABEL'] = 'default+vite'
            elif use_default:
                os.environ['DARS_MINIFY_LABEL'] = 'default'
            elif use_vite:
                os.environ['DARS_MINIFY_LABEL'] = 'vite'
            else:
                os.environ['DARS_MINIFY_LABEL'] = ''
        except Exception:
            os.environ['DARS_MINIFY_LABEL'] = ''
        # Apply defaultMinify from config and CLI override
        try:
            default_min = cfg.get('defaultMinify', True)
            if getattr(args, 'no_minify', False):
                os.environ['DARS_DEFAULT_MINIFY'] = '0'
            else:
                os.environ['DARS_DEFAULT_MINIFY'] = '1' if default_min else '0'
        except Exception:
            pass
        # Precompute label for exporter
        try:
            from dars.core.js_bridge import vite_available as _vite_available, esbuild_available as _esbuild_available
            use_vite = (os.environ.get('DARS_VITE_MINIFY', '1') == '1') and (_vite_available() or _esbuild_available())
            use_default = (os.environ.get('DARS_DEFAULT_MINIFY', '1') != '0')
            use_vite = (os.environ.get('DARS_VITE_MINIFY', '1') == '1') and (_vite_available() or _esbuild_available())
            use_default = (os.environ.get('DARS_DEFAULT_MINIFY', '1') != '0')
            if use_default and use_vite:
                os.environ['DARS_MINIFY_LABEL'] = 'default+vite'
            elif use_default:
                os.environ['DARS_MINIFY_LABEL'] = 'default'
            elif use_vite:
                os.environ['DARS_MINIFY_LABEL'] = 'vite'
            else:
                os.environ['DARS_MINIFY_LABEL'] = ''
        except Exception:
            os.environ['DARS_MINIFY_LABEL'] = ''
        outdir = args.output
        if cfg_found and (args.output == './dist' or args.output == 'dist'):
            resolved = resolve_paths(cfg, project_root)
            outdir = resolved.get('outdir_abs') or outdir

        # Normalize format aliases
        fmt_cli = args.format
        if fmt_cli == 'html':
            fmt_cli = 'web'
        # Validate format
        if fmt_cli not in ['web', 'desktop']:
            console.print(f"[red]{translator.get('error_format_only_html')}[/red]")
            sys.exit(1)
        # proceed (desktop is implemented)

        # Ensure outdir can be created
        try:
            os.makedirs(outdir, exist_ok=True)
        except Exception as e:
            console.print(f"[red]{translator.get('error_output_create')}: {outdir} -> {e}[/red]")
            sys.exit(1)

        success = exporter.export_app(app, args.format, outdir, args.preview)
        sys.exit(0 if success else 1)
        
    elif args.command == 'info':
        # Show information
        app = exporter.load_app_from_file(args.file)
        if app is None:
            sys.exit(1)
            
        exporter.show_app_info(app)
        
    elif args.command == 'formats':
        # Show formats
        exporter.show_supported_formats()
    
    elif args.command == 'init':
        if args.list_templates:
            list_templates_detailed()
        elif args.update:
            # Update or create config in provided name or current directory
            target_dir = args.name or '.'
            project_root = os.path.abspath(target_dir)
            os.makedirs(project_root, exist_ok=True)
            # Merge with DEFAULT_CONFIG and write back to ensure new keys (e.g., viteMinify)
            update_config(project_root, {})
            # Migrate legacy format html -> web (idempotente)
            try:
                cfg, _ = load_config(project_root)
                if str(cfg.get('format', '')).lower() == 'html':
                    update_config(project_root, {"format": "web"})
            except Exception:
                pass
            console.print("[green]✔ dars.config.json created/updated[/green]")
            # If desktop format, ensure backend scaffold exists
            try:
                cfg2, _ = load_config(project_root)
                if str(cfg2.get('format', '')).lower() == 'desktop':
                    backend_dir = Path(project_root) / 'backend'
                    backend_dir.mkdir(parents=True, exist_ok=True)
                    # package.json (CJS)
                    pkg_path = backend_dir / 'package.json'
                    if not pkg_path.exists():
                        pkg_path.write_text('{\n' +
                                            '  "name": "dars-electron-backend",\n' +
                                            '  "private": true,\n' +
                                            '  "main": "main.js",\n' +
                                            '  "scripts": {"start": "electron ."},\n' +
                                            '  "devDependencies": {"electron": "39.2.6"}\n' +
                                            '}\n', encoding='utf-8')
                    # main.js
                    main_js_path = backend_dir / 'main.js'
                    if not main_js_path.exists():
                        main_js_path.write_text(
                    "const { app, BrowserWindow, Menu, ipcMain } = require('electron');\n" +
                    "const path = require('path');\n" +
                    "const fs = require('fs').promises;\n" +
                    "const http = require('http');\n\n" +
                    "function createWindow() {\n" +
                    "  const win = new BrowserWindow({\n" +
                    "    width: 1000, height: 700,\n" +
                    "    webPreferences: {\n" +
                    "      contextIsolation: true,\n" +
                    "      preload: path.join(__dirname, 'preload.js')\n" +
                    "    }\n" +
                    "  });\n" +
                    "  Menu.setApplicationMenu(null);\n" +
                    "  win.loadFile(path.join(__dirname, 'app', 'index.html'));\n" +
                    "  // Open DevTools in development mode if enabled\n" +
                    "  if (process.env.DARS_DEV === '1' && process.env.DARS_DEVTOOLS !== '0') {\n" +
                    "    win.webContents.openDevTools();\n" +
                    "  }\n" +
                    "}\n\n" +
                    "app.whenReady().then(() => {\n" +
                    "  createWindow();\n" +
                    "  app.on('activate', function () {\n" +
                    "    if (BrowserWindow.getAllWindows().length === 0) createWindow();\n" +
                    "  });\n" +
                    "});\n\n" +
                    "// Utility to resolve paths: absolute paths are used as-is; relative paths resolve against process.cwd()\n" +
                    "function resolvePath(p) {\n" +
                    "  if (!p || typeof p !== 'string') throw new Error('filePath must be a string');\n" +
                    "  if (path.isAbsolute(p)) return p;\n" +
                    "  return path.resolve(process.cwd(), p);\n" +
                    "}\n\n" +
                    "function closeAllAndExit() {\n" +
                    "  try {\n" +
                    "    const wins = BrowserWindow.getAllWindows();\n" +
                    "    wins.forEach(w => { try { w.close(); } catch(e) {} });\n" +
                    "  } catch (e) {}\n" +
                    "  setTimeout(() => { try { app.quit(); } catch(e) {} }, 300);\n" +
                    "}\n\n" +
                    "ipcMain.handle('dars::dev::shutdown', async () => {\n" +
                    "  closeAllAndExit();\n" +
                    "  return true;\n" +
                    "});\n\n" +
                    "const controlPort = process.env.DARS_CONTROL_PORT;\n" +
                    "if (controlPort) {\n" +
                    "  try {\n" +
                    "    const server = http.createServer((req, res) => {\n" +
                    "      if (req.method === 'POST' && req.url === '/__dars_shutdown') {\n" +
                    "        closeAllAndExit();\n" +
                    "        res.writeHead(200); res.end('ok');\n" +
                    "        return;\n" +
                    "      }\n" +
                    "      res.writeHead(404); res.end('not-found');\n" +
                    "    });\n" +
                    "    server.listen(Number(controlPort), '127.0.0.1');\n" +
                    "  } catch (e) { /* ignore */ }\n" +
                    "}\n\n" +
                    "// IPC handlers for Dars desktop API\n" +
                    "ipcMain.handle('dars::FileSystem::read_text', async (_e, filePath, encoding = 'utf-8') => {\n" +
                    "  const resolved = resolvePath(filePath);\n" +
                    "  const content = await fs.readFile(resolved, { encoding });\n" +
                    "  return content;\n" +
                    "});\n\n" +
                    "ipcMain.handle('dars::FileSystem::write_text', async (_e, filePath, data, encoding = 'utf-8') => {\n" +
                    "  const resolved = resolvePath(filePath);\n" +
                    "  if (typeof data !== 'string') data = String(data ?? '');\n" +
                    "  await fs.mkdir(path.dirname(resolved), { recursive: true });\n" +
                    "  await fs.writeFile(resolved, data, { encoding });\n" +
                    "  return true;\n" +
                    "});\n\n" +
                    "ipcMain.handle('dars::FileSystem::read_file', async (_e, filePath) => {\n" +
                    "  const resolved = resolvePath(filePath);\n" +
                    "  try {\n" +
                    "    const data = await fs.readFile(resolved);\n" +
                    "    // Convert to array for JSON serialization\n" +
                    "    return { data: Array.from(data) };\n" +
                    "  } catch (error) {\n" +
                    "    console.error('Error reading file:', error);\n" +
                    "    throw error;\n" +
                    "  }\n" +
                    "});\n\n" +
                    "ipcMain.handle('dars::FileSystem::write_file', async (_e, filePath, data) => {\n" +
                    "  const resolved = resolvePath(filePath);\n" +
                    "  try {\n" +
                    "    await fs.mkdir(path.dirname(resolved), { recursive: true });\n" +
                    "    await fs.writeFile(resolved, Buffer.from(data));\n" +
                    "    return true;\n" +
                    "  } catch (error) {\n" +
                    "    console.error('Error writing file:', error);\n" +
                    "    throw error;\n" +
                    "  }\n" +
                    "});\n\n" +
                    "ipcMain.handle('dars::FileSystem::list_directory', async (_e, dirPath, pattern = '*', includeSize = false) => {\n" +
                    "  const resolved = resolvePath(dirPath);\n" +
                    "  try {\n" +
                    "    const entries = await fs.readdir(resolved, { withFileTypes: true });\n" +
                    "    const result = [];\n" +
                    "    for (const entry of entries) {\n" +
                    "      // Simple pattern matching (supports * wildcard)\n" +
                    "      if (pattern !== '*') {\n" +
                    "        const regex = new RegExp('^' + pattern.replace(/\\*/g, '.*') + '$');\n" +
                    "        if (!regex.test(entry.name)) continue;\n" +
                    "      }\n" +
                    "      const obj = {\n" +
                    "        name: entry.name,\n" +
                    "        isDirectory: entry.isDirectory()\n" +
                    "      };\n" +
                    "      if (includeSize) {\n" +
                    "        const stats = await fs.stat(path.join(resolved, entry.name));\n" +
                    "        obj.size = stats.size;\n" +
                    "      }\n" +
                    "      result.push(obj);\n" +
                    "    }\n" +
                    "    return result;\n" +
                    "  } catch (error) {\n" +
                    "    console.error('Error listing directory:', error);\n" +
                    "    throw error;\n" +
                    "  }\n" +
                    "});\n\n" +
                    "app.on('window-all-closed', function () {\n" +
                    "  if (process.platform !== 'darwin') app.quit();\n" +
                    "});\n", encoding='utf-8')
                    # preload.js
                    preload_path = backend_dir / 'preload.js'
                    if not preload_path.exists():
                        preload_path.write_text(
                            "const { contextBridge, ipcRenderer } = require('electron');\n" +
                            "contextBridge.exposeInMainWorld('DarsIPC', {\n" +
                            "  invoke: (channel, ...args) => ipcRenderer.invoke(channel, ...args)\n" +
                            "});\n" +
                            "// Also expose a minimal DarsDesktopAPI for renderer convenience\n" +
                            "contextBridge.exposeInMainWorld('DarsDesktopAPI', {\n" +
                            "  FileSystem: {\n" +
                            "    read_text: (...args) => ipcRenderer.invoke('dars::FileSystem::read_text', ...args),\n" +
                            "    write_text: (...args) => ipcRenderer.invoke('dars::FileSystem::write_text', ...args),\n" +
                            "    read_file: (...args) => ipcRenderer.invoke('dars::FileSystem::read_file', ...args),\n" +
                            "    write_file: (...args) => ipcRenderer.invoke('dars::FileSystem::write_file', ...args),\n" +
                            "    list_directory: (...args) => ipcRenderer.invoke('dars::FileSystem::list_directory', ...args)\n" +
                            "  }\n" +
                            "});\n" +
                            "// Dev helpers: request graceful shutdown from Python dev launcher\n" +
                            "contextBridge.exposeInMainWorld('DarsDev', {\n" +
                            "  shutdown: () => ipcRenderer.invoke('dars::dev::shutdown')\n" +
                            "});\n",
                            encoding='utf-8')
                    console.print("[green]✔ backend/ scaffold ensured[/green]")
                    
                    # Ensure default icon exists in icons/ directory
                    try:
                        icons_dir = Path(project_root) / 'icons'
                        icons_dir.mkdir(parents=True, exist_ok=True)
                        # Get path to default icon in templates/desktop
                        current_file = Path(__file__).resolve()
                        default_icon_src = current_file.parent.parent / "templates" / "desktop" / "icon.png"
                        if default_icon_src.exists():
                            default_icon_dest = icons_dir / "icon.png"
                            if not default_icon_dest.exists():
                                shutil.copy2(default_icon_src, default_icon_dest)
                                console.print("[green]✔ icons/icon.png created[/green]")
                    except Exception as e:
                        console.print(f"[yellow]Warning: could not copy default icon: {e}[/yellow]")
            except Exception:
                pass
        elif not args.name:
            console.print("[red]Error: Project name is required[/red]")
            parser.parse_args(['init', '--help'])
        else:
            exporter.init_project(args.name, template=args.template, proj_type=getattr(args, 'type', 'web'))

        
    elif args.command == 'build':
        project_root = os.path.abspath(getattr(args, 'project', '.'))
        cfg, found = load_config(project_root)
        if not found:
            console.print("[yellow][Dars] Warning: dars.config.json not found. Run 'dars init --update' to create it.[/yellow]")
        resolved = resolve_paths(cfg, project_root)
        # Apply viteMinify setting to env for downstream minifier
        try:
            vite_flag = cfg.get('viteMinify', True)
            os.environ['DARS_VITE_MINIFY'] = '1' if vite_flag else '0'
        except Exception:
            pass
        # Apply defaultMinify from config and CLI override
        try:
            default_min = cfg.get('defaultMinify', True)
            if getattr(args, 'no_minify', False):
                os.environ['DARS_DEFAULT_MINIFY'] = '0'
            else:
                os.environ['DARS_DEFAULT_MINIFY'] = '1' if default_min else '0'
        except Exception:
            pass
        # Ensure default minifier uses fallback-only (no external tools) when enabled
        try:
            os.environ['DARS_DEFAULT_MINIFY_ONLY_FALLBACK'] = '1' if os.environ.get('DARS_DEFAULT_MINIFY', '1') != '0' else '0'
        except Exception:
            pass
        # Precompute label for exporter
        try:
            from dars.core.js_bridge import vite_available as _vite_available, esbuild_available as _esbuild_available
            use_vite = (os.environ.get('DARS_VITE_MINIFY', '1') == '1') and (_vite_available() or _esbuild_available())
            use_default = (os.environ.get('DARS_DEFAULT_MINIFY', '1') != '0')
            if use_default and use_vite:
                os.environ['DARS_MINIFY_LABEL'] = 'default+vite'
            elif use_default:
                os.environ['DARS_MINIFY_LABEL'] = 'default'
            elif use_vite:
                os.environ['DARS_MINIFY_LABEL'] = 'vite'
            else:
                os.environ['DARS_MINIFY_LABEL'] = ''
        except Exception:
            os.environ['DARS_MINIFY_LABEL'] = ''
        entry = resolved.get('entry_abs') or os.path.join(project_root, cfg.get('entry', 'main.py'))
        format_name = cfg.get('format', 'html')
        outdir = resolved.get('outdir_abs') or os.path.join(project_root, 'dist')

        # Build-only heads-up: esbuild optional, but recommended for better bundling
        try:
            from dars.core.js_bridge import esbuild_available as _esb_ok
            if not _esb_ok():
                console.print("[yellow][Dars] Notice: esbuild no está disponible. El bundle se hará con minificación básica. Ejecuta 'dars doctor' para ver requerimientos opcionales.[/yellow]")
        except Exception:
            pass

        # Validate entry file exists
        if not os.path.exists(entry):
            console.print(f"[red]{translator.get('error_entry_not_found_in_config')}: {entry}[/red]")
            console.print(f"[yellow]{translator.get('edit_config_hint')}[/yellow]")
            sys.exit(1)

        # Normalize alias
        if format_name == 'html':
            format_name = 'web'
        # Validate format
        if format_name not in ['web', 'desktop']:
            console.print(f"[red]{translator.get('error_format_only_html')}[/red]")
            sys.exit(1)
        # proceed (desktop is implemented)

        # Ensure outdir can be created
        try:
            os.makedirs(outdir, exist_ok=True)
        except Exception as e:
            console.print(f"[red]{translator.get('error_output_create')}: {outdir} -> {e}[/red]")
            sys.exit(1)

        app = exporter.load_app_from_file(entry)
        if app is None:
            sys.exit(1)
        # Warn if desktop and no app.version set
        if format_name == 'desktop':
            try:
                if not getattr(app, 'version', ''):
                    console.print("[yellow][Dars] Notice: no App.version set. Using default 0.1.0 for desktop package.json. It's recommended to set and increment version for production builds.[/yellow]")
            except Exception:
                pass
        # Respect bundle flag for web; force bundle for desktop to generate source-electron
        bundle_flag = True
        try:
            bundle_flag = bool(cfg.get('bundle', True))
        except Exception:
            bundle_flag = True
        if format_name == 'desktop':
            bundle_flag = True
        try:
            success = exporter.export_app(app, format_name, outdir, show_preview=False, bundle=bundle_flag)
        except KeyboardInterrupt:
            console.print("[yellow]Process interrupted by user during build[/yellow]")
            sys.exit(1)
        if not success:
            sys.exit(1)

        # If desktop, run electron-builder to generate executable according to targetPlatform
        if format_name == 'desktop':
            try:
                import sys as _sys
                from dars.core import js_bridge as jsb
                # Determine platform target
                target = str(cfg.get('targetPlatform', 'auto')).lower()
                if target not in ('auto', 'windows', 'linux', 'macos'):
                    console.print("[yellow][Dars] Warning: invalid targetPlatform. Using 'auto'.[/yellow]")
                    target = 'auto'
                if target == 'auto':
                    if _sys.platform.startswith('win'):
                        target = 'windows'
                    elif _sys.platform.startswith('linux'):
                        target = 'linux'
                    elif _sys.platform == 'darwin':
                        target = 'macos'
                    else:
                        target = 'windows'
                if target == 'macos' and _sys.platform != 'darwin':
                    console.print("[red]✖ Cannot build macOS from a non-mac host. Use a macOS machine.[/red]")
                    sys.exit(1)
                # Guard: Linux targets from non-Linux hosts require Docker
                if target == 'linux' and not _sys.platform.startswith('linux'):
                    try:
                        import shutil as _shutil
                        has_docker = _shutil.which('docker') is not None
                    except Exception:
                        has_docker = False
                    if not has_docker:
                        console.print("[red]✖ Cannot build Linux targets from a non-Linux host without Docker.[/red]")
                        console.print("[yellow]Tip: Install Docker Desktop (enable WSL integration) or build on a Linux/WSL environment, then run dars build again.[/yellow]")
                        sys.exit(1)

                # Ensure electron-builder available (best effort)
                if not jsb.electron_builder_available():
                    console.print("[yellow][Dars] electron-builder not found. Attempting to use Bun runner...[/yellow]")
                # Compute cwd where package.json lives
                src_dir = os.path.join(outdir, 'source-electron')
                if not os.path.isdir(src_dir):
                    src_dir = outdir
                # Ensure production deps. Prefer npm; fallback to bun if npm not present
                try:
                    from dars.core.js_bridge import has_node, has_npm, has_bun, which, _run as _jsrun
                    ran_installer = False
                    if has_node() and has_npm():
                        npm_bin = which("npm.cmd") or which("npm") or "npm"
                        console.print("[cyan][Dars] Installing production dependencies in source-electron (npm) ...[/cyan]")
                        _jsrun([npm_bin, "install", "--production"], cwd=src_dir)
                        ran_installer = True
                    if not ran_installer and has_bun():
                        console.print("[cyan][Dars] Installing production dependencies in source-electron (bun) ...[/cyan]")
                        _jsrun(["bun", "install", "--production"], cwd=src_dir)
                except Exception:
                    pass
                # Build args - use --dir to generate unpacked directory (not installer)
                # Target is also configured in package.json, but --dir flag ensures it
                build_args = ["--dir"]
                if target == 'windows':
                    build_args.append("--win")
                elif target == 'linux':
                    build_args.append("--linux")
                elif target == 'macos':
                    build_args.append("--mac")

                # Show progress with Rich Progress bar
                from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn
                import time
                import threading
                
                progress_messages = []
                last_message = ""
                current_progress = 10
                build_complete = False
                
                def progress_callback(line: str):
                    nonlocal last_message, current_progress
                    # Filter and format electron-builder output
                    line_lower = line.lower()
                    if any(keyword in line_lower for keyword in ['packaging', 'building', 'compiling', 'copying', 'writing', 'done', 'error', 'warning']):
                        # Clean up the message
                        clean_msg = line.strip()
                        if clean_msg and clean_msg != last_message:
                            progress_messages.append(clean_msg)
                            last_message = clean_msg
                            # Increment progress based on keywords
                            if 'packaging' in line_lower:
                                current_progress = min(current_progress + 15, 90)
                            elif 'building' in line_lower or 'compiling' in line_lower:
                                current_progress = min(current_progress + 10, 90)
                            elif 'copying' in line_lower or 'writing' in line_lower:
                                current_progress = min(current_progress + 5, 90)
                            elif 'done' in line_lower:
                                current_progress = 95
                
                def update_progress_bar(progress, task):
                    """Gradually update progress bar while building"""
                    nonlocal current_progress, build_complete
                    while not build_complete:
                        if current_progress < 90:
                            # Gradually increase progress over time (simulated)
                            current_progress = min(current_progress + 1, 90)
                        progress.update(task, completed=current_progress)
                        time.sleep(0.5)  # Update every 0.5 seconds
                
                with Progress(
                    SpinnerColumn(),
                    TextColumn("[progress.description]{task.description}"),
                    BarColumn(),
                    TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
                    TimeElapsedColumn(),
                    console=console
                ) as progress:
                    task = progress.add_task(f"[cyan]Packaging Electron app for {target}...", total=100)
                    
                    # Start with some progress
                    progress.update(task, advance=10)
                    
                    # Start progress updater thread
                    progress_thread = threading.Thread(target=update_progress_bar, args=(progress, task), daemon=True)
                    progress_thread.start()
                    
                    # Run electron-builder with progress callback
                    start_time = time.time()
                    code, _out, err = jsb.electron_build(cwd=src_dir, extra_args=build_args, progress_callback=progress_callback)
                    elapsed = time.time() - start_time
                    
                    # Mark build as complete
                    build_complete = True
                    progress_thread.join(timeout=1.0)
                    
                if code != 0:
                        progress.update(task, completed=100)
                        console.print(f"[red]✖ electron-builder failed after {elapsed:.1f}s[/red]")
                        if _out:
                            # Show last few error messages
                            error_lines = [line for line in _out.split('\n') if any(kw in line.lower() for kw in ['error', 'failed', 'exception'])]
                            if error_lines:
                                console.print("[red]Error details:[/red]")
                                for err_line in error_lines[-5:]:  # Last 5 error lines
                                    console.print(f"  [red]{err_line}[/red]")
                        if err:
                            console.print(f"[red]STDERR: {err}[/red]")
                        sys.exit(1)
                    
                    # Complete the progress bar
                progress.update(task, completed=100, description=f"[green]✓ Packaging completed in {elapsed:.1f}s[/green]")
                    
                    # Show summary of what was built
                if progress_messages:
                        # Filter for important messages
                    important = [msg for msg in progress_messages if any(kw in msg.lower() for kw in ['packaging', 'building', 'done', 'created'])]
                    if important:
                        console.print(f"\n[dim]Build output:[/dim]")
                        for msg in important[-3:]:  # Last 3 important messages
                            console.print(f"  [dim]{msg}[/dim]")
                
                console.print(f"[green]✔ Electron package created in dist/ (took {elapsed:.1f}s)[/green]")
            except Exception as e:
                console.print(f"[red]Desktop build failed: {e}[/red]")
                sys.exit(1)

        sys.exit(0)

    elif args.command == 'preview':
        index_path = os.path.join(args.path, "index.html")
        if os.path.exists(index_path):
            console.print(f"[green]{translator.get('app_found')}: {args.path} [/green]")
            console.print(f"{translator.get('open_in_browser')}: file://{os.path.abspath(index_path)}")
            console.print(f"{translator.get('view_preview')} [green]y[/green] / [red]n[/red] [y/n] ")
            if input().lower() == 'y':
                # Pass the current language to preview.py
                
                import subprocess
                process = None
                try:
                    process = subprocess.Popen([sys.executable, '-m', 'dars.cli.preview', args.path])
                    process.wait()
                except KeyboardInterrupt:
                    if process:
                        process.terminate()
                        process.wait()
                finally:
                    if process and process.poll() is None:
                        process.terminate()
                        process.wait()
        else:
            console.print(f"[red]{translator.get('index_not_found')} {args.path}[/red]")

            
    elif args.command == 'config':
        if getattr(args, 'config_command', None) == 'validate':
            project_root = os.path.abspath(getattr(args, 'project', '.'))
            cfg, found = load_config(project_root)
            resolved = resolve_paths(cfg, project_root)

            issues = []
            def ok(msg):
                return f"[green]✔ {msg}[/green]"
            def warn(msg):
                return f"[yellow]⚠ {msg}[/yellow]"
            def err(msg):
                return f"[red]✖ {msg}[/red]"

            if not found:
                issues.append(warn(translator.get('cfg_not_found_warn')))

            # entry validation
            entry = resolved.get('entry_abs')
            if not entry or not os.path.isfile(entry):
                issues.append(err(translator.get('cfg_entry_missing').format(path=cfg.get('entry'))))
            else:
                issues.append(ok(translator.get('cfg_entry_ok').format(path=cfg.get('entry'))))

            # format validation: accept 'web', legacy 'html' and 'desktop'.
            fmt = cfg.get('format')
            if fmt == 'web' or fmt == 'html':
                issues.append(ok(translator.get('cfg_format_ok').format(fmt=fmt)))
            elif fmt == 'desktop':
                issues.append(ok(translator.get('cfg_format_ok').format(fmt=fmt)))
            else:
                issues.append(err(translator.get('cfg_format_only_html').format(fmt=fmt)))

            # outdir validation (creatable)
            outdir_abs = resolved.get('outdir_abs')
            try:
                os.makedirs(outdir_abs, exist_ok=True)
                issues.append(ok(translator.get('cfg_outdir_ok').format(path=cfg.get('outdir'))))
            except Exception as e:
                issues.append(err(translator.get('cfg_outdir_error').format(path=cfg.get('outdir'), error=str(e))))

            # publicDir (if set) existence
            pub = cfg.get('publicDir')
            if pub:
                pub_abs = resolved.get('public_abs')
                if not pub_abs or not os.path.isdir(pub_abs):
                    issues.append(err(translator.get('cfg_public_missing').format(path=pub)))
                else:
                    issues.append(ok(translator.get('cfg_public_ok').format(path=pub)))
            else:
                issues.append(warn(translator.get('cfg_public_autodetect')))

            # include/exclude types
            if not isinstance(cfg.get('include', []), list):
                issues.append(err(translator.get('cfg_include_type')))
            if not isinstance(cfg.get('exclude', []), list):
                issues.append(err(translator.get('cfg_exclude_type')))

            # bundle is bool
            if not isinstance(cfg.get('bundle', False), bool):
                issues.append(err(translator.get('cfg_bundle_type')))
            # defaultMinify is bool
            if not isinstance(cfg.get('defaultMinify', True), bool):
                issues.append(err('defaultMinify must be a boolean'))

            # utility_styles must be a dict if present
            if 'utility_styles' in cfg and cfg['utility_styles'] is not None and not isinstance(cfg['utility_styles'], dict):
                issues.append(err(translator.get('cfg_utility_styles_type')))

            # If the entry defines any SSR routes (SPA or multipage), backendEntry must be configured
            has_ssr_routes = False
            backend_entry = cfg.get('backendEntry')
            try:
                if entry and os.path.isfile(entry):
                    # Import the entry module safely (so __name__ != '__main__')
                    import importlib.util

                    module_name = os.path.splitext(os.path.basename(entry))[0]
                    spec = importlib.util.spec_from_file_location(module_name, entry)
                    module = importlib.util.module_from_spec(spec) if spec else None
                    if spec and module:
                        sys.modules[module_name] = module
                        spec.loader.exec_module(module)  # type: ignore[union-attr]

                        app_obj = getattr(module, 'app', None)
                        # Detect SSR routes only if this looks like a Dars App
                        if app_obj is not None:
                            try:
                                from dars.core.route_types import RouteType
                            except Exception:
                                RouteType = None  # type: ignore

                            if RouteType is not None:
                                # 1) SPA / SSR routes via _spa_routes
                                if hasattr(app_obj, 'has_spa_routes') and callable(getattr(app_obj, 'has_spa_routes')):
                                    if app_obj.has_spa_routes():
                                        for spa_route in getattr(app_obj, '_spa_routes', {}).values():
                                            root = getattr(spa_route, 'root', None)
                                            meta = getattr(root, '__dars_route_metadata__', None)
                                            if getattr(meta, 'route_type', None) == RouteType.SSR:
                                                has_ssr_routes = True
                                                break

                                # 2) Multipage apps via _pages (Page roots with RouteType.SSR)
                                if not has_ssr_routes and hasattr(app_obj, 'is_multipage') and callable(getattr(app_obj, 'is_multipage')):
                                    if app_obj.is_multipage():
                                        for page in getattr(app_obj, '_pages', {}).values():
                                            root = getattr(page, 'root', None)
                                            meta = getattr(root, '__dars_route_metadata__', None)
                                            if getattr(meta, 'route_type', None) == RouteType.SSR:
                                                has_ssr_routes = True
                                                break
            except Exception:
                # Best-effort: if we can't introspect the app, don't block config validation here
                pass

            # Fallback: if we still don't know but the entry file clearly uses RouteType.SSR,
            # assume there are SSR routes so we can warn about missing backendEntry.
            if not has_ssr_routes and entry and os.path.isfile(entry):
                try:
                    with open(entry, 'r', encoding='utf-8') as f:
                        src = f.read()
                    if 'RouteType.SSR' in src:
                        has_ssr_routes = True
                except Exception:
                    pass

            if has_ssr_routes and not backend_entry:
                issues.append(err(translator.get('cfg_backend_entry_missing')))

            # Print report
            report = Table(title=translator.get('cfg_validation_title'))
            report.add_column(translator.get('cfg_item'), style="cyan")
            report.add_column(translator.get('cfg_result'), style="white")

            report.add_row('config', translator.get('cfg_found') if found else translator.get('cfg_not_found'))
            for msg in issues:
                if 'entry' in msg:
                    report.add_row('entry', msg)
                elif 'format' in msg:
                    report.add_row('format', msg)
                elif 'outdir' in msg:
                    report.add_row('outdir', msg)
                elif 'public' in msg or 'publicDir' in msg:
                    report.add_row('publicDir', msg)
                elif 'include' in msg:
                    report.add_row('include', msg)
                elif 'exclude' in msg:
                    report.add_row('exclude', msg)
                elif 'bundle' in msg:
                    report.add_row('bundle', msg)
                else:
                    report.add_row('note', msg)

            console.print(report)
            has_errors = any(msg.startswith('[red]') for msg in issues)
            sys.exit(1 if has_errors else 0)
        else:
            # Show help for config subcommands
            parser = create_parser(include_hidden=False)
            subparsers_actions = [action for action in parser._actions if isinstance(action, argparse._SubParsersAction)]
            for subparsers_action in subparsers_actions:
                if 'config' in subparsers_action.choices:
                    pretty_print_help(subparsers_action.choices['config'])
                    return

    elif args.command == 'dev':
        # Resolve project and config
        project_root = os.path.abspath(getattr(args, 'project', '.'))
        cfg, found = load_config(project_root)
        if not found:
            console.print("[yellow][Dars] Warning: dars.config.json not found. Run 'dars init --update' to create it.[/yellow]")
        resolved = resolve_paths(cfg, project_root)
        entry = resolved.get('entry_abs') or os.path.join(project_root, cfg.get('entry', 'main.py'))

        # If this is a desktop project and Electron is below the recommended baseline,
        # emit a non-fatal security warning so users know they should update it.
        try:
            fmt = str(cfg.get('format', '')).lower() if cfg else ''
        except Exception:
            fmt = ''
        if fmt == 'desktop':
            try:
                from dars.cli.doctor.detect import detect_electron
                from dars.cli.doctor.doctor import MIN_SAFE_ELECTRON, _is_version_less

                elec = detect_electron()
                ver = elec.get('version') or None
                if ver and _is_version_less(str(ver), MIN_SAFE_ELECTRON):
                    console.print(
                        f"[yellow][Dars] Warning: Electron {ver} is below the recommended security baseline ({MIN_SAFE_ELECTRON}). "
                        "Run 'dars doctor --all --yes' to update Electron/electron-builder via Bun.[/yellow]"
                    )
            except Exception:
                # Best-effort only; don't block dev if detection fails
                pass

        if not os.path.exists(entry):
            console.print(f"[red]{translator.get('error_entry_not_found_in_config')}: {entry}[/red]")
            console.print(f"[yellow]{translator.get('edit_config_hint')}[/yellow]")
            sys.exit(1)

        import subprocess

        # If --backend is set, run only the backendEntry (SSR/API) via uvicorn
        if getattr(args, 'backend', False):
            backend_entry = cfg.get('backendEntry')
            if not backend_entry:
                # Reuse the same message used in config validate
                console.print(f"[red]{translator.get('cfg_backend_entry_missing')}[/red]")
                sys.exit(1)

            uvicorn_target = str(backend_entry)

            # Resolve host/port from backend.apiConfig.DarsEnv if available
            host = '127.0.0.1'
            port = 3000
            try:
                import importlib

                # Ensure project_root is on sys.path so `backend` package is importable
                if project_root not in sys.path:
                    sys.path.insert(0, project_root)

                from urllib.parse import urlparse

                api_cfg = importlib.import_module('backend.apiConfig')
                DarsEnv = getattr(api_cfg, 'DarsEnv', None)
                if DarsEnv is not None and hasattr(DarsEnv, 'get_urls') and callable(getattr(DarsEnv, 'get_urls')):
                    urls = DarsEnv.get_urls()
                    backend_url = urls.get('backend')
                    if isinstance(backend_url, str):
                        # Try stdlib parsing first
                        parsed = urlparse(backend_url)
                        if parsed.hostname:
                            host = parsed.hostname
                        if parsed.port:
                            port = parsed.port
                        # Fallback manual parse if urlparse didn't give a port
                        if parsed.port is None and ':' in backend_url.rsplit('/', 1)[-1]:
                            tail = backend_url.rsplit('/', 1)[-1]
                            parts = tail.split(':')
                            if len(parts) == 2 and parts[1].isdigit():
                                port = int(parts[1])
            except Exception:
                # Fallback to default host/port if anything fails
                pass

            backend_cmd = [
                sys.executable,
                '-m', 'uvicorn',
                uvicorn_target,
                '--reload',
                '--host', str(host),
                '--port', str(port),
            ]
            process = None
            try:
                process = subprocess.Popen(backend_cmd, cwd=project_root)
                process.wait()
                sys.exit(process.returncode or 0)
            except KeyboardInterrupt:
                if process and process.poll() is None:
                    process.terminate()
                    process.wait()
                sys.exit(0)
            except Exception as e:
                console.print(f"[red]Failed to start backend dev process: {e}[/red]")
                sys.exit(1)

        # Default: Run entry in development mode (the entry typically calls app.rTimeCompile()).
        # Backend/SSR server can be started in a separate terminal with `dars dev --backend` if needed.
        process = None
        try:
            process = subprocess.Popen([sys.executable, entry], cwd=os.path.dirname(entry))
            process.wait()
            sys.exit(process.returncode or 0)
        except KeyboardInterrupt:
            if process and process.poll() is None:
                process.terminate()
                process.wait()
            sys.exit(0)
        except Exception as e:
            console.print(f"[red]Failed to start dev process: {e}[/red]")
            sys.exit(1)

    elif args.command == 'doctor':
        try:
            from dars.core.js_bridge import electron_available, electron_builder_available, ensure_electron, ensure_electron_builder
        except Exception:
            # If js bridge is not available, fall back to base doctor
            code = run_doctor(
                check_only=getattr(args, 'check', False),
                auto_yes=getattr(args, 'yes', False),
                install_all=getattr(args, 'all', False),
                force=getattr(args, 'force', False)
            )
            sys.exit(code)

        check_only = bool(getattr(args, 'check', False))
        wants_install = bool(getattr(args, 'all', False))
        auto_yes = bool(getattr(args, 'yes', False))

        # Non-interactive: --check => print Electron status and return combined code
        if check_only:
            elec_ok = electron_available()
            builder_ok = electron_builder_available()
            # Pretty status lines to match doctor style
            console.print("[bold]Electron (optional):[/bold] " + ("[green]OK[/green]" if elec_ok else "[yellow]MISSING[/yellow]"))
            console.print("[bold]electron-builder (optional):[/bold] " + ("[green]OK[/green]" if builder_ok else "[yellow]MISSING[/yellow]"))
            base = run_doctor(check_only=True, auto_yes=auto_yes, install_all=False, force=getattr(args, 'force', False))
            missing = not (elec_ok and builder_ok)
            sys.exit(1 if (base != 0 or missing) else 0)

        # Non-interactive: --all (optionally with --yes) => install Electron tools up-front, then run base doctor
        if wants_install:
            elec_ok = electron_available()
            if not elec_ok:
                if auto_yes or Confirm.ask("¿Instalar Electron con Bun (devDependency)?", default=True):
                    ensure_electron()
            builder_ok = electron_builder_available()
            if not builder_ok:
                if auto_yes or Confirm.ask("¿Instalar electron-builder con Bun (devDependency)?", default=True):
                    ensure_electron_builder()
            # After attempting installs, run base doctor (which may show interactive UI)
            code = run_doctor(check_only=False, auto_yes=auto_yes, install_all=True, force=getattr(args, 'force', False))
            sys.exit(code)

        # Interactive mode: delegate entirely to base doctor; no extra prints or installs
        code = run_doctor(
            check_only=False,
            auto_yes=auto_yes,
            install_all=False,
            force=getattr(args, 'force', False)
        )
        sys.exit(code)

    elif args.command == 'forcedev':
        # Hidden: force-install Node, Bun, and all Python deps without prompts
        code = run_forcedev()
        sys.exit(code)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("[yellow]Process interrupted by user[/yellow]")
        sys.exit(1)
    except Exception as e:
        # If DARS_DEBUG=1, re-raise to show full traceback
        if os.environ.get("DARS_DEBUG") == "1":
            raise
        console.print(f"[red]Process failed: {e}[/red]")
        sys.exit(1)
