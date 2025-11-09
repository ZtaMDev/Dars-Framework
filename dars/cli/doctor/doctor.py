import os, sys
from typing import Dict, List
from .detect import (
    detect_node,
    detect_bun,
    detect_esbuild,
    detect_vite,
    detect_electron,
    detect_electron_builder,
    read_pyproject_deps,
    check_python_deps,
)
from .installers import install_bun
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
        elec = detect_electron()
        builder = detect_electron_builder()
        reqs = read_pyproject_deps()
        py = check_python_deps(reqs)

    render_report(node, bun, py, esb, vit, elec, builder)

    # Mandatory only for doctor purposes: Python deps
    missing_items: List[str] = []
    if py.get('missing'): missing_items.append('Python deps')
    # Node, Bun, esbuild, vite treated as optional. Bun can be auto-installed if user wants.
    optional_missing: List[str] = []
    if not node.get('ok'): optional_missing.append('Node.js (optional)')
    if not bun.get('ok'): optional_missing.append('Bun (optional)')
    if not esb.get('ok'): optional_missing.append('esbuild (optional)')
    if not vit.get('ok'): optional_missing.append('vite (optional)')
    if not elec.get('ok'): optional_missing.append('Electron (optional)')
    if not builder.get('ok'): optional_missing.append('electron-builder (optional)')

    if check_only:
        # Fail if Python deps missing OR Electron tooling missing
        return 0 if (not missing_items and elec.get('ok') and builder.get('ok')) else 1

    # Decide next steps
    has_missing = bool(missing_items)

    # Always show a small action menu; if nothing missing, offer re-run/quit
    if not check_only:
        # Show menu; do not auto-install after exit
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

    # choice == '1' => Install ALL missing (and optional desktop tooling if requested via --all)
    summary: List[str] = []
    # Installers: Bun, Python deps; desktop tooling via Bun
    if not bun.get('ok'): summary.append('Bun (winget/installer)')
    if py.get('missing'): summary.append(f"Python deps: {', '.join(py['missing'])}")
    if install_all:
        if not elec.get('ok'): summary.append('Electron (bun add -d electron)')
        if not builder.get('ok'): summary.append('electron-builder (bun add -d electron-builder)')

    if not auto_yes:
        if not confirm_install(summary):
            return 1

    # Installers: Bun, optionally Python deps and desktop tooling
    with console.status("[cyan]Installing selected items...[/cyan]"):
        try:
            install_bun()
        except Exception:
            pass
        # Install desktop tooling via Bun if requested and available
        if install_all:
            try:
                from dars.core.js_bridge import ensure_electron, ensure_electron_builder, bun_add
                if not elec.get('ok'):
                    ensure_electron()
                if not builder.get('ok'):
                    ensure_electron_builder()
                # Pin Electron version in project package.json if needed
                try:
                    import os, json
                    proj = os.getcwd()
                    pkg_dir = proj
                    # Prefer backend/package.json if exists
                    if os.path.isfile(os.path.join(proj, 'backend', 'package.json')):
                        pkg_dir = os.path.join(proj, 'backend')
                    pkg_path = os.path.join(pkg_dir, 'package.json')
                    if os.path.isfile(pkg_path):
                        with open(pkg_path, 'r', encoding='utf-8') as pf:
                            data = json.load(pf)
                        devd = data.get('devDependencies') or {}
                        ev = (devd.get('electron') or '').strip().lower()
                        needs_pin = (not ev) or ev.startswith(('^','~')) or ev == 'latest'
                        if needs_pin:
                            console.print("[cyan]Pinning Electron version (39.1.1) in project devDependencies...[/cyan]")
                            bun_add(["electron@39.1.1"], dev=True, cwd=pkg_dir)
                except Exception:
                    pass
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
        elec2 = detect_electron()
        builder2 = detect_electron_builder()
        py2 = check_python_deps(read_pyproject_deps())

    render_report(node2, bun2, py2, esb2, vit2, elec2, builder2)

    # Consider satisfied if Python deps OK; optional tools do not gate satisfaction
    all_ok = not py2.get('missing')

    cfg['requirements']['node'].update({'ok': bool(node2.get('ok')), 'version': node2.get('version')})
    cfg['requirements']['bun'].update({'ok': bool(bun2.get('ok')), 'version': bun2.get('version')})
    cfg['python_deps'] = {'ok': not bool(py2.get('missing')), 'missing': py2.get('missing') or []}
    # doctor satisfaction now tied only to Python deps
    cfg['satisfied'] = bool(all_ok)
    save_config(cfg)

    return 0 if all_ok else 1


def run_forcedev() -> int:
    """Force-install everything without initial verification or prompts.
    - Attempts Bun installer unconditionally (best-effort)
    - Installs/updates all Python deps from pyproject.toml
    - Re-checks and persists satisfied state
    Returns 0 if environment ends OK, else 1.
    """
    # Best-effort installs (no UI)
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
    bun2 = detect_bun()
    py2 = check_python_deps(read_pyproject_deps())
    all_ok = bun2.get('ok') and not py2.get('missing')

    # keep node state updated for UI even if not installed by forcedev
    node2 = detect_node()
    cfg['requirements']['node'].update({'ok': bool(node2.get('ok')), 'version': node2.get('version')})
    cfg['requirements']['bun'].update({'ok': bool(bun2.get('ok')), 'version': bun2.get('version')})
    cfg['python_deps'] = {'ok': not bool(py2.get('missing')), 'missing': py2.get('missing') or []}
    cfg['satisfied'] = bool(all_ok)
    save_config(cfg)
    return 0 if all_ok else 1
