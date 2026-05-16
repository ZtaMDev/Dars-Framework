import os
import re
from rich.console import Console
from rich.prompt import Prompt, Confirm
from dars.cli.prompts import select_prompt, confirm_prompt

console = Console()

def handle_generate(args):
    gen_type = args.type
    if not gen_type:
        gen_type = select_prompt("What do you want to generate?", choices=["component", "page"])
        
    name = args.name
    if not name:
        name = Prompt.ask(f"Enter the name of the {gen_type}")

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
            page_type = select_prompt(f"What type of page is '{name}'?", choices=["static", "spa"])
            
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
        else: # spa
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
