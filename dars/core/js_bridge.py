import os
import subprocess
import tempfile
from typing import List, Optional, Tuple


def _run(cmd: List[str], cwd: Optional[str] = None, live: bool = False) -> Tuple[int, str, str]:
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


def bun_add(packages: List[str], dev: bool = True, cwd: Optional[str] = None) -> bool:
    if not has_bun():
        return False
    args = ["bun", "add"]
    if dev:
        args.append("-d")
    args.extend(packages)
    code, _, _ = _run(args, cwd=cwd, live=True)
    return code == 0


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
        code, _, _ = _run(["bun", "x", "esbuild", src_path, "--minify", "--legal-comments=none", "--platform=browser", "--format=esm", f"--outfile={out}"])
        return code == 0
    # Node fallback via npx
    code, _, _ = _run(["npx", "--yes", "esbuild", src_path, "--minify", "--legal-comments=none", "--platform=browser", "--format=esm", f"--outfile={out}"])
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
                "    rollupOptions: { input: ['" + abs_src.replace('\\', '\\\\') + "'] },\n"
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
