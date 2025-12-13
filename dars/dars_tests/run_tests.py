# Runner that executes the test files and prints a colored report using rich
import runpy, glob, importlib.util, os, sys, traceback, subprocess, time, threading
import requests
import signal
import webbrowser
import shutil
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt

console = Console()

def run_unit_tests(unit_test_paths=None):
    """Run unit test files, optionally from specific paths"""
    if unit_test_paths is None:
        # Default behavior: run all tests in tests directory
        tests = sorted(glob.glob(os.path.join(os.path.dirname(__file__), 'tests', 'test_*.py')))
    else:
        # Use provided test paths
        tests = unit_test_paths
    
    results = []
    for t in tests:
        name = os.path.basename(t)
        try:
            console.print(Panel(f'Running {name}', style='cyan'))
            ns = runpy.run_path(t, run_name='__main__')
            results.append((name, True, None))
            console.print(f'[green]PASS[/green] {name}')
        except Exception as e:
            results.append((name, False, traceback.format_exc()))
            console.print(f'[red]FAIL[/red] {name}')
            console.print(traceback.format_exc())
    return results

def check_server(port=8000, timeout=10):
    """Check if the server is running on the given port"""
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            response = requests.get(f'http://localhost:{port}', timeout=2)
            if response.status_code < 500:
                return True
        except requests.exceptions.RequestException:
            time.sleep(0.5)
    return False

def run_app_with_timeout(app_file, timeout=15):
    """Run a Dars app with rTimeCompile and capture its output with a timeout"""
    try:
        env = os.environ.copy()
        env['PYTHONIOENCODING'] = 'utf-8'

        process = subprocess.Popen(
            [sys.executable, app_file],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=os.path.dirname(app_file) or None,  # evita cwd = "" en Windows
            env=env,
        )
        
        # Esperar a que el servidor se inicie o timeout
        server_started = False
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            if check_server(8000, 2):
                server_started = True
                break
            # Verificar si el proceso ha terminado (lo que indicaría un error)
            if process.poll() is not None:
                break
            time.sleep(1)
        
        # Recoger la salida (aunque no haya terminado, para capturar errores iniciales)
        try:
            stdout, stderr = process.communicate(timeout=2)
        except subprocess.TimeoutExpired:
            stdout, stderr = b"", b""
        
        stdout_str = stdout.decode('utf-8', errors='replace') if stdout else ''
        stderr_str = stderr.decode('utf-8', errors='replace') if stderr else ''
        
        return {
            'success': server_started,
            'process': process,
            'stdout': stdout_str,
            'stderr': stderr_str
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'stdout': '',
            'stderr': ''
        }


def safe_read_file(file_path):
    """Leer un archivo de forma segura manejando diferentes codificaciones"""
    encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
    
    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                return f.read()
        except UnicodeDecodeError:
            continue
    
    # Si todas las codificaciones fallan, usar modo binario con reemplazo de errores
    with open(file_path, 'rb') as f:
        return f.read().decode('utf-8', errors='replace')

def run_app_tests(app_test_paths=None):
    """Run Dars application tests that use rTimeCompile, optionally from specific paths"""
    if app_test_paths is None:
        # Default behavior: run all apps in apps_test directory
        apps_test_dir = os.path.join(os.path.dirname(__file__), 'apps_test')
        if not os.path.exists(apps_test_dir):
            console.print(f"[yellow]apps_test directory not found: {apps_test_dir}[/yellow]")
            return []
        
        apps = sorted(glob.glob(os.path.join(apps_test_dir, '*.py')))
    else:
        # Use provided app paths
        apps = app_test_paths
    
    results = []
    
    for app_file in apps:
        name = os.path.basename(app_file)
        try:
            console.print(Panel(f'Testing Dars App: {name}', style='magenta'))
            
            # Verificar si la aplicación usa rTimeCompile de forma segura
            content = safe_read_file(app_file)
            uses_rTimeCompile = 'rTimeCompile' in content
            
            if not uses_rTimeCompile:
                console.print(f"[yellow]Skipping {name} - does not use rTimeCompile[/yellow]")
                continue
            
            # Ejecutar la aplicación con timeout
            result = run_app_with_timeout(app_file, timeout=20)
            
            if result['success']:
                # Éxito: el servidor se inició correctamente
                results.append((name, True, "App started server successfully on port 8000"))
                console.print(f'[green]PASS[/green] {name}')
                
                # Abrir el navegador para verificación visual
                console.print("[green]Opening browser for visual verification...[/green]")
                webbrowser.open('http://localhost:8000')
                
                # Preguntar al usuario si quiere terminar el proceso
                console.print("\n[bold]Please verify the application in your browser.[/bold]")
                console.print("After verification, you can:")
                console.print("1. Press 'y' to terminate the process and continue with tests")
                console.print("2. Press 'n' to keep the server running and continue")
                
                response = Prompt.ask("\nTerminate process and continue?", choices=["y", "n"], default="y")
                
                if response.lower() == "y":
                    # Terminar el proceso
                    if 'process' in result and result['process'].poll() is None:
                        console.print("[yellow]Terminating app process...[/yellow]")
                        try:
                            # Enviar señal de interrupción (equivalente a Ctrl+C)
                            if os.name == 'nt':  # Windows
                                result['process'].terminate()
                            else:  # Unix
                                result['process'].send_signal(signal.SIGINT)
                            
                            # Esperar a que termine
                            result['process'].wait(timeout=10)
                            console.print("[green]App process terminated successfully[/green]")
                            
                            # Limpiar carpeta dars_preview
                            preview_dir = os.path.join(os.path.dirname(app_file), "dars_preview")
                            if os.path.exists(preview_dir):
                                shutil.rmtree(preview_dir)
                                console.print("[green]Preview directory cleaned up[/green]")
                                
                        except:
                            console.print("[red]Force killing app process...[/red]")
                            result['process'].kill()
                else:
                    console.print("[yellow]Keeping server running...[/yellow]")
            else:
                # Fallo: el servidor no se inició
                error_msg = result['stderr'] or result['stdout'] or "Unknown error"
                results.append((name, False, error_msg))
                console.print(f'[red]FAIL[/red] {name}: {error_msg}')
            
            # Terminar el proceso si todavía está ejecutándose (solo si no elegimos mantenerlo)
            if 'process' in result and result['process'].poll() is None:
                console.print("[yellow]Terminating app process...[/yellow]")
                try:
                    # Enviar señal de interrupción (equivalente a Ctrl+C)
                    if os.name == 'nt':  # Windows
                        result['process'].terminate()
                    else:  # Unix
                        result['process'].send_signal(signal.SIGINT)
                    
                    # Esperar a que termine
                    result['process'].wait(timeout=10)
                    console.print("[green]App process terminated successfully[/green]")
                    
                    # Limpiar carpeta dars_preview
                    preview_dir = os.path.join(os.path.dirname(app_file), "dars_preview")
                    if os.path.exists(preview_dir):
                        shutil.rmtree(preview_dir)
                        console.print("[green]Preview directory cleaned up[/green]")
                        
                except:
                    console.print("[red]Force killing app process...[/red]")
                    result['process'].kill()
                    
        except Exception as e:
            results.append((name, False, str(e)))
            console.print(f'[red]FAIL[/red] {name}: {e}')
    
    return results

def main(unit_test_paths=None, app_test_paths=None):
    """
    Run Dars test suite with optional specific test paths
    
    Args:
        unit_test_paths (list): Optional list of paths to unit test files
        app_test_paths (list): Optional list of paths to application test files
    """
    # Run unit tests
    console.print(Panel("Running Unit Tests", style="cyan"))
    unit_results = run_unit_tests(unit_test_paths)
    
    # Run app tests
    console.print(Panel("Running App Tests (rTimeCompile)", style="magenta"))
    app_results = run_app_tests(app_test_paths)
    
    # Combine results
    all_results = unit_results + app_results
    
    # Print results table
    table = Table(title='Dars Test Suite Results')
    table.add_column('Test File')
    table.add_column('Result')
    table.add_column('Details', overflow='fold')
    
    for name, ok, details in all_results:
        table.add_row(name, '[green]PASS[/green]' if ok else '[red]FAIL[/red]', details or '')
    
    console.print(table)
    
    # Exit code
    any_fail = any(not ok for _, ok, _ in all_results)
    if any_fail:
        console.print('[bold red]Some tests failed.[/bold red]')
        sys.exit(1)
    else:
        console.print('[bold green]All tests passed.[/bold green]')

if __name__ == '__main__':
    # Parse command line arguments for custom test paths
    import argparse
    parser = argparse.ArgumentParser(description='Run Dars Framework tests')
    parser.add_argument('--unit-tests', nargs='+', help='Paths to specific unit test files')
    parser.add_argument('--app-tests', nargs='+', help='Paths to specific application test files')
    
    args = parser.parse_args()
    
    # Run tests with optional paths
    main(unit_test_paths=args.unit_tests, app_test_paths=args.app_tests)