import os
import re
from rich.console import Console
from rich.prompt import Prompt, Confirm
from dars.cli.prompts import select_prompt, confirm_prompt

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

console = Console()

def handle_generate(args):
    gen_type = args.type
    if not gen_type:
        gen_type = select_prompt("What do you want to generate?", choices=["component", "page"])
        
    name = args.name
    if not name:
        while True:
            name = Prompt.ask(f"Enter the name of the {gen_type}")
            if name and name.strip():
                break
            console.print(f"[red]Error: {gen_type.capitalize()} name cannot be empty.[/red]")

    # Ensure it's a valid python identifier
    safe_name = re.sub(r'[^a-zA-Z0-9_]', '_', name)
    # Avoid python keywords or starting with numbers
    if safe_name and safe_name[0].isdigit():
        safe_name = "_" + safe_name

    if gen_type == "component":
        os.makedirs("components", exist_ok=True)
        file_path = f"components/{name}.py"
        if os.path.exists(file_path):
            console.print(f"[red]Error: Component {file_path} already exists.[/red]")
            return
            
        content = f"""from dars.all import *

@FunctionComponent
def {safe_name}(props):
    return Container(
        Text("{name} Component works!")
    )
"""
        with open(file_path, "w") as f:
            f.write(content)
        console.print(f"[green]SUCCESS: Component {name} generated successfully at {file_path}[/green]")
        console.print("[yellow]Note: Remember to import and use it in your main application.[/yellow]")
        
    elif gen_type == "page":
        page_type = args.page_type
        if not page_type:
            page_type = select_prompt(f"What type of page is '{name}'?", choices=["static", "spa", "ssr"])
            
        os.makedirs("pages", exist_ok=True)
        file_path = f"pages/{name}.py"
        if os.path.exists(file_path):
            console.print(f"[red]Error: Page {file_path} already exists.[/red]")
            return
            
        if page_type == "static":
            content = f"""from dars.all import *

{safe_name} = Page(
    Container(
        Text("{name} Static Page works!")
    )
)
"""
            import_statement = f"from pages.{name} import {safe_name}"
            inject_statement = f"app.add_page('{name}', {safe_name})"
        elif page_type == "spa":
            content = f"""from dars.all import *

@route("/{name}")
def {safe_name}():
    return Page(
        Container(
            Text("{name} SPA Page works!")
        )
    )
"""
            import_statement = f"from pages.{name} import {safe_name}"
            inject_statement = f"app.add_page('{name}', {safe_name}())"
        else: # ssr
            content = f"""from dars.all import *

@route("/{name}", route_type=RouteType.SSR)
def {safe_name}():
    return Page(
        Container(
            Text("{name} SSR Page works!")
        )
    )
"""
            import_statement = f"from pages.{name} import {safe_name}"
            inject_statement = f"app.add_page('{name}', {safe_name}())"

            # Check for backend files
            if not os.path.exists("backend"):
                console.print("\n[bold yellow]⚠ WARNING: SSR routes require a backend configuration.[/bold yellow]")
                console.print("[yellow]It seems your project doesn't have the '/backend' directory required for Dars SSR.[/yellow]")
                
                if confirm_prompt("Do you want to automatically scaffold the SSR backend now?"):
                    os.makedirs("backend", exist_ok=True)
                    with open("backend/__init__.py", "w") as f: pass
                    
                    with open("backend/apiConfig.py", "w") as f:
                        f.write(API_CONFIG_PY_CODE.strip())
                    
                    with open("backend/api.py", "w") as f:
                        f.write(API_PY_CODE.strip())
                    
                    # Update config
                    if os.path.exists("dars.config.json"):
                        import json
                        try:
                            with open("dars.config.json", "r") as f:
                                config = json.load(f)
                            if "backendEntry" not in config:
                                config["backendEntry"] = "backend.api:app"
                                with open("dars.config.json", "w") as f:
                                    json.dump(config, f, indent=2)
                                console.print("[green]SUCCESS: Updated dars.config.json with backendEntry.[/green]")
                        except:
                            pass
                    
                    console.print("[green]SUCCESS: SSR Backend scaffolded at /backend[/green]")
                    console.print("[yellow]Note: Remember to run 'dars dev --backend' to start the SSR server.[/yellow]")
            
        with open(file_path, "w") as f:
            f.write(content)
        console.print(f"[green]SUCCESS: Page {name} generated successfully at {file_path}[/green]")
        
        # Inject to main.py
        auto_inject = args.yes
        if not auto_inject:
            auto_inject = confirm_prompt(f"Do you want to automatically add this page to your main app file?")
            
        if auto_inject:
            entry_file = "main.py"
            if os.path.exists("dars.config.json"):
                import json
                try:
                    with open("dars.config.json", "r") as f:
                        config = json.load(f)
                    entry_file = config.get("entry", "main.py")
                except:
                    pass
                    
            if not os.path.exists(entry_file):
                if os.path.exists("index.py"):
                    entry_file = "index.py"
                else:
                    console.print(f"[red]Error: Could not find main application file ({entry_file}). Please add the page manually.[/red]")
                    console.print(f"[cyan]{import_statement}[/cyan]")
                    console.print(f"[cyan]{inject_statement}[/cyan]")
                    return
            
            try:
                with open(entry_file, "r") as f:
                    lines = f.readlines()
                
                content_all = "".join(lines)
                
                # Default app variable name might be different
                app_var_match = re.search(r'([a-zA-Z0-9_]+)\s*=\s*App\(', content_all)
                app_var = app_var_match.group(1) if app_var_match else "app"
                
                if app_var != "app":
                    inject_statement = inject_statement.replace("app.", f"{app_var}.")

                # 1. Inject Import
                last_import_line = -1
                for i, line in enumerate(lines):
                    if line.strip().startswith(("import ", "from ")):
                        last_import_line = i
                
                if last_import_line != -1:
                    lines.insert(last_import_line + 1, import_statement + "\n")
                else:
                    lines.insert(0, import_statement + "\n")
                    
                # 2. Inject add_page
                last_add_page_line = -1
                for i, line in enumerate(lines):
                    if f"{app_var}.add_page(" in line:
                        last_add_page_line = i
                
                if last_add_page_line != -1:
                    lines.insert(last_add_page_line + 1, inject_statement + "\n")
                else:
                    # Fallback: after app = App(...)
                    app_def_line = -1
                    for i, line in enumerate(lines):
                        if f"{app_var} = App(" in line:
                            app_def_line = i
                            break
                    if app_def_line != -1:
                        lines.insert(app_def_line + 1, "\n" + inject_statement + "\n")
                    else:
                        lines.append("\n" + inject_statement + "\n")
                
                with open(entry_file, "w") as f:
                    f.writelines(lines)
                
                console.print(f"[green]SUCCESS: Successfully added {name} to {entry_file}[/green]")
            except Exception as e:
                console.print(f"[red]Failed to auto-inject: {str(e)}[/red]")
                console.print(f"[yellow]Please add manually:[/yellow]")
                console.print(f"[cyan]{import_statement}[/cyan]")
                console.print(f"[cyan]{inject_statement}[/cyan]")
