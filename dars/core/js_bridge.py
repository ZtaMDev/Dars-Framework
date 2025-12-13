# Dars Framework - Core Source File
#
# This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0.
# If a copy of the MPL was not distributed with this file, You can obtain one at
# https://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2025 ZtaDev
import os
import subprocess
import tempfile
from typing import List, Optional, Tuple


def _run(cmd: List[str], cwd: Optional[str] = None, live: bool = False) -> Tuple[int, str, str]:
    """Small wrapper around subprocess.run used by JS tooling helpers.

    Note: this function is generic and MUST NOT rely on Electron-specific env vars.
    Electron-specific tweaks (like ELECTRON_DISABLE_SECURITY_WARNINGS) are handled
    in electron_dev_spawn, which is only used for desktop dev.
    """
    try:
        if live:
            p = subprocess.run(cmd, cwd=cwd)
            return (p.returncode or 0, "", "")
        p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
        return p.returncode, (p.stdout or ""), (p.stderr or "")
    except Exception as e:
        return 1, "", str(e)


def which(name: str) -> Optional[str]:
    cmd = ["where", name] if os.name == 'nt' else ["which", name]
    code, out, _ = _run(cmd)
    if code == 0 and out:
        return out.strip().splitlines()[0]
    return None


def has_node() -> bool:
    return which("node") is not None


def has_bun() -> bool:
    return which("bun") is not None


def vite_available() -> bool:
    # Prefer bun x vite
    if has_bun():
        code, out, _ = _run(["bun", "x", "vite", "--version"])
        if code == 0:
            return True
    # Fallback to npx vite
    code, out, _ = _run(["npx", "--yes", "vite", "--version"])
    return code == 0


def has_npm() -> bool:
    return which("npm") is not None


def npm_install_global(packages: List[str]) -> bool:
    # Deprecated path for performance reasons; prefer Bun installs
    return False


def bun_add(packages: List[str], dev: bool = True, cwd: Optional[str] = None) -> bool:
    if not has_bun():
        return False
    args = ["bun", "add"]
    if dev:
        args.append("-d")
    args.extend(packages)
    code, _, _ = _run(args, cwd=cwd, live=True)
    return code == 0


def electron_available() -> bool:
    # Prefer bun x electron
    if has_bun():
        code, _, _ = _run(["bun", "x", "electron", "--version"])
        if code == 0:
            return True
    # Try direct binary
    if which("electron"):
        return True
    # Fallback npx
    code, _, _ = _run(["npx", "--yes", "electron", "--version"])
    return code == 0


def electron_builder_available() -> bool:
    if has_bun():
        code, _, _ = _run(["bun", "x", "electron-builder", "--version"])
        if code == 0:
            return True
    if which("electron-builder"):
        return True
    code, _, _ = _run(["npx", "--yes", "electron-builder", "--version"])
    return code == 0


def ensure_electron(cwd: Optional[str] = None) -> bool:
    # If any runner works, consider available
    if electron_available():
        return True
    # Try to add as dev dependency with Bun in the working directory
    workdir = cwd or os.getcwd()
    if has_bun():
        ok = bun_add(["electron"], dev=True, cwd=workdir)
        return ok and electron_available()
    return False


def ensure_electron_builder(cwd: Optional[str] = None) -> bool:
    if electron_builder_available():
        return True
    workdir = cwd or os.getcwd()
    if has_bun():
        ok = bun_add(["electron-builder"], dev=True, cwd=workdir)
        return ok and electron_builder_available()
    return False


def electron_dev(cwd: Optional[str] = None) -> Tuple[int, str, str]:
    """Run Electron in dev mode (expects package.json/main.js present in cwd)."""
    if has_bun():
        # Prefer 'bun x' to avoid missing bunx shim on Windows
        return _run(["bun", "x", "electron", "."], cwd=cwd)
    # Resolve npx path robustly on Windows
    npx = which("npx.cmd") or which("npx") or "npx"
    return _run([npx, "--yes", "electron", "."], cwd=cwd)


def electron_dev_spawn(cwd: Optional[str] = None, env: Optional[dict] = None):
    """Spawn Electron in dev mode and return (Popen, cmd).

    The caller is responsible for reading stdout/stderr and terminating the process.
    """
    # Prefer direct electron binary when available so the spawned Popen is the electron process
    electron_bin = which("electron") or which("electron.cmd")
    if electron_bin:
        cmd = [electron_bin, "."]
    elif has_bun():
        cmd = ["bun", "x", "electron", "."]
    else:
        npx = which("npx.cmd") or which("npx") or "npx"
        cmd = [npx, "--yes", "electron", "."]

    try:
        # Prepare environment for Electron dev runs
        if env is None:
            env = os.environ.copy()
        # Disable noisy security warnings in dev; Dars controls CSP explicitly.
        env.setdefault("ELECTRON_DISABLE_SECURITY_WARNINGS", "true")

        # On Windows create a new process group so we can terminate the whole tree; on POSIX use setsid
        kwargs = dict(cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        kwargs['env'] = env
        if os.name == 'nt':
            kwargs['creationflags'] = subprocess.CREATE_NEW_PROCESS_GROUP
        else:
            kwargs['preexec_fn'] = os.setsid
        p = subprocess.Popen(cmd, **kwargs)
        return p, cmd
    except Exception:
        return None, cmd


def electron_build(cwd: Optional[str] = None, extra_args: Optional[List[str]] = None, progress_callback=None) -> Tuple[int, str, str]:
    """Run electron-builder build in cwd.
    
    Args:
        cwd: Working directory
        extra_args: Additional arguments for electron-builder (default: empty, uses package.json config)
        progress_callback: Optional callback function(message: str) to receive progress updates
    """
    args = extra_args or []
    cmd = None
    
    # Prefer npx; fallback to bun x if npx not available in PATH
    npx = which("npx.cmd") or which("npx")
    if npx:
        cmd = [npx, "--yes", "electron-builder", *args]
    elif has_bun():
        cmd = ["bun", "x", "electron-builder", *args]
    else:
        # Last resort: try plain electron-builder if present
        eb = which("electron-builder") or "electron-builder"
        cmd = [eb, *args]
    if progress_callback:
        # Run with live output for progress updates
        try:
            import subprocess
            p = subprocess.Popen(
                cmd,
                cwd=cwd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
            
            stdout_lines = []
            for line in iter(p.stdout.readline, ''):
                if not line:
                    break
                line = line.rstrip()
                stdout_lines.append(line)
                # Call progress callback with the line
                if progress_callback:
                    progress_callback(line)
            
            p.wait()
            return p.returncode, '\n'.join(stdout_lines), ''
        except Exception as e:
            return 1, '', str(e)
    else:
        # Fallback to original behavior
        return _run(cmd, cwd=cwd)


def node_run(code: str) -> Tuple[int, str, str]:
    if not has_node():
        return 1, "", "node not found"
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mjs", mode="w", encoding="utf-8") as tf:
        tf.write(code)
        temp = tf.name
    try:
        return _run(["node", temp])
    finally:
        try:
            os.remove(temp)
        except Exception:
            pass


def esbuild_available() -> bool:
    # Prefer bun esbuild
    if has_bun():
        # bun x esbuild --version
        code, out, _ = _run(["bun", "x", "esbuild", "--version"])
        if code == 0:
            return True
    # Node npx fallback
    if has_node():
        code, out, _ = _run(["npx", "--yes", "esbuild", "--version"])  # --yes to avoid prompt
        if code == 0:
            return True
    return False


def ensure_esbuild(cwd: Optional[str] = None) -> bool:
    if esbuild_available():
        return True
    # Try to add via bun (dev dep)
    if has_bun():
        ok = bun_add(["esbuild"], dev=True, cwd=cwd)
        return ok and esbuild_available()
    return False


def esbuild_minify_js(src_path: str, out_path: Optional[str] = None) -> bool:
    if not esbuild_available() and not ensure_esbuild(os.path.dirname(src_path)):
        return False
    out = out_path or src_path
    if has_bun():
        code, _, _ = _run(["bun", "x", "esbuild", src_path, "--minify", "--legal-comments=none", "--platform=browser", "--format=iife", f"--outfile={out}"])
        return code == 0
    # Node fallback via npx
    code, _, _ = _run(["npx", "--yes", "esbuild", src_path, "--minify", "--legal-comments=none", "--platform=browser", "--format=iife", f"--outfile={out}"])
    return code == 0


def esbuild_minify_css(src_path: str, out_path: Optional[str] = None) -> bool:
    # esbuild can minify CSS if input is CSS
    return esbuild_minify_js(src_path, out_path)


def vite_minify_js(src_path: str, out_path: Optional[str] = None) -> bool:
    """Use Vite build (Rollup) to minify a single JS entry file.
    Creates a temp vite.config.mjs pointing to the absolute src_path, builds to a temp outDir, and copies the result to out_path.
    """
    if not vite_available():
        return False
    try:
        import json
        import shutil
        workdir = tempfile.mkdtemp(prefix="dars_vite_")
        outdir = os.path.join(workdir, "out")
        os.makedirs(outdir, exist_ok=True)
        abs_src = os.path.abspath(src_path)
        vite_config = os.path.join(workdir, "vite.config.mjs")
        with open(vite_config, "w", encoding="utf-8") as f:
            f.write(
                "export default {\n" 
                "  build: {\n"
                "    minify: 'esbuild',\n"
                "    sourcemap: false,\n"
                "    rollupOptions: { input: ['" + abs_src.replace('\\', '\\\\') + "'], output: { format: 'iife' } },\n"
                "    outDir: 'out',\n"
                "    emptyOutDir: true\n"
                "  }\n"
                "};\n"
            )
        # Run vite build
        cmd = ["bun", "x", "vite", "build", "--config", vite_config] if has_bun() else ["npx", "--yes", "vite", "build", "--config", vite_config]
        code, _out, _err = _run(cmd, cwd=workdir)
        if code != 0:
            shutil.rmtree(workdir, ignore_errors=True)
            return False
        # Find a single .js in outdir
        chosen = None
        for name in os.listdir(outdir):
            if name.endswith(".js"):
                chosen = os.path.join(outdir, name)
                break
        if not chosen:
            shutil.rmtree(workdir, ignore_errors=True)
            return False
        target = out_path or src_path
        shutil.copyfile(chosen, target)
        shutil.rmtree(workdir, ignore_errors=True)
        return True
    except Exception:
        return False
