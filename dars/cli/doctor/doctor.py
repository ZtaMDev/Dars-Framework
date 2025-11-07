import os, sys
from typing import Dict, List
from .detect import detect_node, detect_bun, detect_esbuild, detect_vite, read_pyproject_deps, check_python_deps
from .installers import install_node, install_bun, install_esbuild, install_vite
from .persist import load_config, save_config
from .ui import render_report, prompt_action, confirm_install
from rich.console import Console

console = Console()


def run_doctor(check_only: bool = False, auto_yes: bool = False, install_all: bool = False, force: bool = False) -> int:
    cfg = load_config()

    # Detect with spinner
    with console.status("[cyan]Checking environment...[/cyan]"):
        node = detect_node()
        bun = detect_bun()
        esb = detect_esbuild()
        vit = detect_vite()
        reqs = read_pyproject_deps()
        py = check_python_deps(reqs)

    render_report(node, bun, py, esb, vit)

    missing_items: List[str] = []
    if not node.get('ok'): missing_items.append('Node.js LTS')
    if not bun.get('ok'): missing_items.append('Bun stable')
    if py.get('missing'): missing_items.append('Python deps')
    optional_missing: List[str] = []
    if not esb.get('ok'): optional_missing.append('esbuild (optional)')
    if not vit.get('ok'): optional_missing.append('vite (optional)')

    if check_only:
        return 0 if not missing_items else 1

    # Decide next steps
    has_missing = bool(missing_items)

    # Always show a small action menu; if nothing missing, offer re-run/quit
    if not check_only:
        choice = '1' if (auto_yes and install_all and has_missing) else prompt_action(has_missing)
        if has_missing:
            if choice == '3':
                return 1
            if choice == '2':
                return run_doctor(check_only=False, auto_yes=auto_yes, install_all=install_all, force=True)
        else:
            # No missing: '1' => re-run, '2' => quit
            if choice == '2':
                return 0
            if choice == '1':
                return run_doctor(check_only=False, auto_yes=auto_yes, install_all=install_all, force=True)

    if not has_missing:
        cfg['requirements']['node'].update({'ok': True, 'version': node.get('version')})
        cfg['requirements']['bun'].update({'ok': True, 'version': bun.get('version')})
        cfg['python_deps'] = {'ok': True, 'missing': []}
        cfg['satisfied'] = True
        save_config(cfg)
        return 0

    if auto_yes and install_all:
        choice = '1'
    else:
        choice = prompt_action()
    if choice == '3':
        return 1

    if choice == '2':
        # Re-run immediately
        return run_doctor(check_only=False, auto_yes=auto_yes, install_all=install_all, force=True)

    # choice == '1' => Install ALL missing
    summary: List[str] = []
    if not node.get('ok'): summary.append('Node.js LTS (winget)')
    if not bun.get('ok'): summary.append('Bun (winget)')
    if py.get('missing'): summary.append(f"Python deps: {', '.join(py['missing'])}")
    if optional_missing:
        summary.extend(optional_missing)

    if not auto_yes:
        if not confirm_install(summary):
            return 1

    # Installers: always run Node then Bun sequentially (idempotent if already installed)
    with console.status("[cyan]Installing selected items...[/cyan]"):
        try:
            install_node()
        except Exception:
            pass
        try:
            install_bun()
        except Exception:
            pass
        # Optional developer tools
        try:
            if not esb.get('ok'):
                install_esbuild()
        except Exception:
            pass
        try:
            if not vit.get('ok'):
                install_vite()
        except Exception:
            pass

    # Python deps via pip
    if py.get('missing'):
        try:
            import subprocess
            cmd = [sys.executable, '-m', 'pip', 'install', '--upgrade'] + py['missing']
            subprocess.run(cmd, check=False)
        except Exception:
            pass

    # Re-check after attempted install
    with console.status("[cyan]Re-checking...[/cyan]"):
        node2 = detect_node()
        bun2 = detect_bun()
        esb2 = detect_esbuild()
        vit2 = detect_vite()
        py2 = check_python_deps(read_pyproject_deps())

    render_report(node2, bun2, py2, esb2, vit2)

    all_ok = node2.get('ok') and bun2.get('ok') and not py2.get('missing')

    cfg['requirements']['node'].update({'ok': bool(node2.get('ok')), 'version': node2.get('version')})
    cfg['requirements']['bun'].update({'ok': bool(bun2.get('ok')), 'version': bun2.get('version')})
    cfg['python_deps'] = {'ok': not bool(py2.get('missing')), 'missing': py2.get('missing') or []}
    cfg['satisfied'] = bool(all_ok)
    save_config(cfg)

    return 0 if all_ok else 1


def run_forcedev() -> int:
    """Force-install everything without initial verification or prompts.
    - Attempts Node LTS and Bun installers unconditionally (best-effort)
    - Installs/updates all Python deps from pyproject.toml
    - Re-checks and persists satisfied state
    Returns 0 if environment ends OK, else 1.
    """
    # Best-effort installs (no UI)
    try:
        install_node()
    except Exception:
        pass
    try:
        install_bun()
    except Exception:
        pass

    reqs = read_pyproject_deps()
    if reqs:
        try:
            import subprocess, sys as _sys
            cmd = [_sys.executable, '-m', 'pip', 'install', '--upgrade'] + reqs
            subprocess.run(cmd, check=False)
        except Exception:
            pass

    # Re-check and persist
    cfg = load_config()
    node2 = detect_node()
    bun2 = detect_bun()
    py2 = check_python_deps(read_pyproject_deps())
    all_ok = node2.get('ok') and bun2.get('ok') and not py2.get('missing')

    cfg['requirements']['node'].update({'ok': bool(node2.get('ok')), 'version': node2.get('version')})
    cfg['requirements']['bun'].update({'ok': bool(bun2.get('ok')), 'version': bun2.get('version')})
    cfg['python_deps'] = {'ok': not bool(py2.get('missing')), 'missing': py2.get('missing') or []}
    cfg['satisfied'] = bool(all_ok)
    save_config(cfg)
    return 0 if all_ok else 1
