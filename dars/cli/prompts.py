import sys
from rich.console import Console
from rich.live import Live
from rich.table import Table
from rich.panel import Panel

console = Console()

def select_prompt(question: str, choices: list, default_idx: int = 0):
    """
    Interactive selection prompt using arrow keys.
    Works on Windows via msvcrt and falls back to numeric input on other platforms.
    """
    if sys.platform != "win32":
        # Fallback for non-windows platforms (standard rich prompt with numbers)
        console.print(f"[bold cyan]? [/bold cyan][bold]{question}[/bold]")
        for i, choice in enumerate(choices):
            console.print(f"  [green]{i+1})[/green] {choice}")
        
        from rich.prompt import IntPrompt
        val = IntPrompt.ask("Select an option", choices=[str(i+1) for i in range(len(choices))], default=default_idx+1)
        return choices[val-1]

    import msvcrt
    
    current_idx = default_idx
    
    def generate_menu():
        table = Table.grid(padding=(0, 1))
        table.add_column()
        for i, choice in enumerate(choices):
            if i == current_idx:
                table.add_row(f"[bold cyan]>[/bold cyan] [reverse bold cyan] {choice} [/reverse bold cyan]")
            else:
                table.add_row(f"  [white]{choice}[/white]")
        return table

    console.print(f"[bold cyan]? [/bold cyan][bold]{question}[/bold] [dim](Use arrow keys, Enter to confirm)[/dim]")
    
    with Live(generate_menu(), refresh_per_second=20, transient=True) as live:
        while True:
            if msvcrt.kbhit():
                key = msvcrt.getch()
                
                # Check for Ctrl+C (ASCII 3)
                if key == b'\x03':
                    raise KeyboardInterrupt
                
                if key == b'\r': # Enter
                    return choices[current_idx]
                elif key == b'\xe0': # Special keys prefix
                    key = msvcrt.getch()
                    if key == b'H': # Up arrow
                        current_idx = (current_idx - 1) % len(choices)
                    elif key == b'P': # Down arrow
                        current_idx = (current_idx + 1) % len(choices)
                elif key in (b'j', b'J'): # Vim-like down
                    current_idx = (current_idx + 1) % len(choices)
                elif key in (b'k', b'K'): # Vim-like up
                    current_idx = (current_idx - 1) % len(choices)
                
                live.update(generate_menu())
            sys.stdout.flush()

def confirm_prompt(question: str, default: bool = True) -> bool:
    """Wrapper for rich Confirm prompt with consistent styling"""
    from rich.prompt import Confirm
    return Confirm.ask(f"[bold cyan]? [/bold cyan]{question}", default=default)
