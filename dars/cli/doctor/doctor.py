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
    parse_semver,
)
from .installers import (
    install_bun,
    install_esbuild,
    install_vite,
    install_electron_global,
    install_electron_builder_global,
)
from .persist import load_config, save_config
from .ui import render_report, prompt_action, confirm_install
from rich.console import Console

console = Console()

# Minimum Electron version recommended by Dars (security baseline)
MIN_SAFE_ELECTRON = "39.2.6"


def _is_version_less(v: str, minimum: str) -> bool:
    """Return True if semantic version v < minimum.

    Expects plain "MAJOR.MINOR.PATCH" strings. If parsing fails, be conservative (no warning).
    """
    try:
        def _split(ver: str):
            parts = (ver or "0.0.0").split(".")
            parts = (parts + ["0", "0", "0"])[:3]
            return [int(x) for x in parts]

        v_parts = _split(v)
        m_parts = _split(minimum)
        return v_parts < m_parts
    except Exception:
        return False


def run_doctor(check_only: bool = False, auto_yes: bool = False, install_all: bool = False, force: bool = False) -> int:
    cfg = load_config()

    # Single detection pass with spinner
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

    # Critical requirements for Dars itself: Python deps
    missing_items: List[str] = []
    if py.get('missing'):
        missing_items.append('Python deps')

    # Optional tooling (recommended but not required)
    optional_missing: List[str] = []
    if not node.get('ok'):
        optional_missing.append('Node.js (optional)')
    if not bun.get('ok'):
        optional_missing.append('Bun (optional)')
    if not esb.get('ok'):
        optional_missing.append('esbuild (optional)')
    if not vit.get('ok'):
        optional_missing.append('vite (optional)')
    if not elec.get('ok'):
        optional_missing.append('Electron (optional)')
    if not builder.get('ok'):
        optional_missing.append('electron-builder (optional)')

    # Fast non-interactive mode: only check and exit
    if check_only:
        return 0 if not missing_items else 1

    # Decide installation strategy
    summary: List[str] = []
    if not bun.get('ok'):
        summary.append('Bun (official installer)')
    if py.get('missing'):
        summary.append(f"Python deps: {', '.join(py['missing'])}")

    # Track whether optional tooling needs work when install_all=True
    elec_needs_update = False
    builder_needs_update = False

    if install_all:
        if not esb.get('ok'):
            summary.append('esbuild (bun add -g esbuild)')
        if not vit.get('ok'):
            summary.append('vite (bun add -g vite)')

        # Electron/electron-builder: treat missing OR outdated as candidates for update
        elec_ver = elec.get('version') or None
        elec_needs_update = (not elec.get('ok')) or (
            elec_ver is not None and _is_version_less(str(elec_ver), MIN_SAFE_ELECTRON)
        )
        if elec_needs_update:
            summary.append(f"Electron (bun add -D electron@{MIN_SAFE_ELECTRON})")

        builder_ver = builder.get('version') or None
        # For electron-builder we don't enforce a specific minimum; allow explicit update when missing
        builder_needs_update = not builder.get('ok')
        if builder_needs_update:
            summary.append('electron-builder (bun add -D electron-builder@latest)')

    # Only treat environment as fully satisfied (and exit early) when there is truly
    # nothing to install or update. When install_all=True, outdated Electron/electron-builder
    # should still trigger the install phase even if they were previously marked OK.
    has_missing = bool(missing_items or optional_missing or (install_all and (elec_needs_update or builder_needs_update)))
    if not has_missing:
        cfg['requirements']['node'].update({'ok': bool(node.get('ok')), 'version': node.get('version')})
        cfg['requirements']['bun'].update({'ok': bool(bun.get('ok')), 'version': bun.get('version')})
        cfg['python_deps'] = {'ok': True, 'missing': []}
        cfg['satisfied'] = True
        save_config(cfg)
        return 0

    # In interactive mode, confirm before installing
    if not auto_yes:
        if not confirm_install(summary):
            return 1

    # Perform installations (best-effort)
    # Note: when install_all=True we call Bun with live output (run_live), so we
    # avoid wrapping that in a Rich spinner to prevent overlapping text.
    if install_all:
        try:
            if not bun.get('ok'):
                install_bun()
        except Exception:
            pass

        try:
            if not esb.get('ok'):
                install_esbuild()
            if not vit.get('ok'):
                install_vite()

            # Electron: always attempt to install/update when install_all=True
            install_electron_global()

            # electron-builder: keep behaviour similar (upgrade when requested)
            install_electron_builder_global()
        except Exception:
            pass
    else:
        # For non-install_all flows, keep the spinner UX around any installs.
        with console.status("[cyan]Installing selected items...[/cyan]"):
            try:
                if not bun.get('ok'):
                    install_bun()
            except Exception:
                pass

            try:
                if not esb.get('ok'):
                    install_esbuild()
                if not vit.get('ok'):
                    install_vite()
            except Exception:
                pass

    # Python deps via pip (always try if missing)
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

    # Environment considered satisfied if Python deps are OK; optional tools do not gate satisfaction
    all_ok = not py2.get('missing')

    cfg['requirements']['node'].update({'ok': bool(node2.get('ok')), 'version': node2.get('version')})
    cfg['requirements']['bun'].update({'ok': bool(bun2.get('ok')), 'version': bun2.get('version')})
    cfg['python_deps'] = {'ok': not bool(py2.get('missing')), 'missing': py2.get('missing') or []}
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
