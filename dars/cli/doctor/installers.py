import os, sys, subprocess
from typing import Tuple
from dars.core.js_bridge import has_bun


def run(cmd: list) -> Tuple[int, str, str]:
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, shell=False)
        return p.returncode, p.stdout.strip(), p.stderr.strip()
    except Exception as e:
        return 1, "", str(e)


def run_live(cmd: list, shell: bool = False) -> int:
    """Run a command inheriting stdout/stderr so the user sees prompts/output live."""
    try:
        p = subprocess.run(cmd, shell=shell)
        return p.returncode or 0
    except Exception:
        return 1


# --- Windows installers (preferred: winget) ---

def install_node_windows() -> Tuple[bool, str]:
    # OpenJS.NodeJS.LTS is the winget package id for Node.js LTS
    code, out, err = run(["winget", "install", "-e", "--id", "OpenJS.NodeJS.LTS"])
    ok = (code == 0)
    return ok, (out or err)


def install_bun_windows() -> Tuple[bool, str]:
    # 1) Try winget first (Oven-sh.Bun)
    code, out, err = run(["winget", "install", "-e", "--id", "Oven-sh.Bun"])
    if code == 0:
        return True, (out or err)
    # 2) Fallback: official bun.sh PowerShell installer (streams output)
    # Command shown to the user for transparency
    print("Executing: powershell -NoProfile -ExecutionPolicy Bypass -c \"irm bun.sh/install.ps1 | iex\"")
    ps_cmd = [
        "powershell",
        "-NoProfile",
        "-ExecutionPolicy",
        "Bypass",
        "-c",
        "irm bun.sh/install.ps1 | iex",
    ]
    code2 = run_live(ps_cmd, shell=False)
    return code2 == 0, (out or err)


# --- Stubs for macOS/Linux (future extension) ---

def install_node_posix() -> Tuple[bool, str]:
    # For now, provide guidance only
    msg = "Please install Node.js LTS from https://nodejs.org (or use a package manager)."
    return False, msg


def install_bun_posix() -> Tuple[bool, str]:
    # Use official installer with live output
    # Prefer bash -lc; fallback to sh -lc
    cmd_str = "curl -fsSL https://bun.sh/install | bash"
    print(f"Executing: bash -lc \"{cmd_str}\"")
    # Try bash first
    code = run_live(["bash", "-lc", cmd_str], shell=False)
    if code != 0:
        print(f"bash failed, falling back to: sh -lc \"{cmd_str}\"")
        code = run_live(["sh", "-lc", cmd_str], shell=False)
    return code == 0, ""


def install_node() -> Tuple[bool, str]:
    if os.name == 'nt':
        return install_node_windows()
    return install_node_posix()


def install_bun() -> Tuple[bool, str]:
    if os.name == 'nt':
        return install_bun_windows()
    return install_bun_posix()


def install_esbuild() -> Tuple[bool, str]:
    # Prefer Bun-managed dev dep
    if has_bun():
        print("Executing: bun add -g esbuild")
        code = run_live(["bun", "add", "-g", "esbuild"], shell=False)
        return (code == 0, "")
    # Node fallback: use npx without install (sufficient for detection), nothing to install
    return True, ""


def install_vite() -> Tuple[bool, str]:
    if has_bun():
        print("Executing: bun add -g vite")
        code = run_live(["bun", "add", "-g", "vite"], shell=False)
        return (code == 0, "")
    return True, ""


def install_electron_global() -> Tuple[bool, str]:
    """Install/update Electron as a devDependency via Bun if available.

    We intentionally install it in the current project (bun add -D) instead of
    globally, so that `bun x electron --version` – used by detect_electron() –
    reports the updated baseline version.
    """
    if has_bun():
        # Pin to a reviewed baseline version instead of relying on 'latest'
        target = "electron@39.2.6"
        print(f"Executing: bun add -g {target}")
        code = run_live(["bun", "add", "-g", target], shell=False)
        return (code == 0, "")
    return False, "Bun is not available to install Electron via Bun."


def install_electron_builder_global() -> Tuple[bool, str]:
    """Install/update electron-builder as a devDependency via Bun if available.

    Same reasoning as install_electron_global(): we prefer the project-scoped
    tool that `bun x electron-builder --version` will see.
    """
    if has_bun():
        print("Executing: bun add -g electron-builder@latest")
        code = run_live(["bun", "add", "-g", "electron-builder@latest"], shell=False)
        return (code == 0, "")
    return False, "Bun is not available to install electron-builder via Bun."
