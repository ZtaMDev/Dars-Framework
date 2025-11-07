from typing import Dict, List
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt, Confirm

console = Console()

def render_report(node: Dict, bun: Dict, py: Dict, esb: Dict = None, vit: Dict = None):
    table = Table(title="Dars Doctor — Environment Report", box=None)
    table.add_column("Component", style="cyan")
    table.add_column("Required", style="white")
    table.add_column("Detected", style="green")
    table.add_column("Status", style="bold")

    n_status = "OK" if node.get("ok") else "MISSING"
    b_status = "OK" if bun.get("ok") else "MISSING"
    p_missing = py.get("missing", [])
    p_status = "OK" if not p_missing else f"Missing: {len(p_missing)}"

    table.add_row("Node.js", "LTS (stable)", node.get("version") or "-", n_status)
    table.add_row("Bun", "Stable", bun.get("version") or "-", b_status)
    table.add_row("Python deps", "pyproject.toml", "-", p_status)
    if esb is not None:
        table.add_row("esbuild", "optional", (esb.get("version") if esb else "-") or "-", "OK" if esb and esb.get("ok") else "MISSING")
    if vit is not None:
        table.add_row("vite", "optional", (vit.get("version") if vit else "-") or "-", "OK" if vit and vit.get("ok") else "MISSING")

    console.print(table)
    if p_missing:
        bullets = "\n".join([f" • {req}" for req in p_missing])
        console.print(Panel(bullets or "", title="Missing Python packages", border_style="yellow"))


def prompt_action(has_missing: bool) -> str:
    console.print(Panel("Select an action", border_style="cyan"))
    if has_missing:
        console.print("[1] Install ALL missing\n[2] Re-run checks\n[3] Quit")
        choices = ["1","2","3"]
        default = "1"
    else:
        console.print("[1] Re-run checks\n[2] Quit")
        choices = ["1","2"]
        default = "1"
    while True:
        choice = Prompt.ask("Choice", choices=choices, default=default)
        return choice


def confirm_install(summary_lines: List[str]) -> bool:
    console.print(Panel("The following will be installed:", border_style="yellow"))
    for line in summary_lines:
        console.print(f" • {line}")
    return Confirm.ask("Proceed with installation?", default=True)
