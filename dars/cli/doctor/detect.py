import os, subprocess, sys, re
from typing import Tuple, Optional, List, Dict
from dars.core.js_bridge import has_bun, has_node, _run as js_run

SEMVER_RE = re.compile(r"v?(\d+)\.(\d+)\.(\d+)")


def _run(cmd: List[str]) -> Tuple[int, str, str]:
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, shell=False)
        return p.returncode, p.stdout.strip(), p.stderr.strip()
    except Exception as e:
        return 1, "", str(e)


def which(bin_name: str) -> Optional[str]:
    if os.name == 'nt':
        code, out, _ = _run(["where", bin_name])
    else:
        code, out, _ = _run(["which", bin_name])
    if code == 0 and out:
        return out.splitlines()[0].strip()
    return None


def parse_semver(s: str) -> Optional[str]:
    m = SEMVER_RE.search(s or "")
    if not m:
        return None
    return f"{m.group(1)}.{m.group(2)}.{m.group(3)}"


def detect_node() -> Dict[str, Optional[str]]:
    path = which("node")
    if not path:
        return {"ok": False, "version": None, "path": None}
    code, out, _ = _run([path, "--version"])  # prints like v18.19.1
    ver = parse_semver(out)
    return {"ok": bool(ver), "version": ver, "path": path}


def detect_electron() -> Dict[str, Optional[str]]:
    # Prefer bun x electron --version
    if has_bun():
        code, out, err = js_run(["bun", "x", "electron", "--version"])  # type: ignore
        if code == 0:
            ver = parse_semver(out) or out.strip()
            return {"ok": True, "version": ver, "path": "bun x electron"}
    if has_node():
        code, out, err = js_run(["npx", "--yes", "electron", "--version"])  # type: ignore
        if code == 0:
            ver = parse_semver(out) or out.strip()
            return {"ok": True, "version": ver, "path": "npx electron"}
    return {"ok": False, "version": None, "path": None}


def detect_electron_builder() -> Dict[str, Optional[str]]:
    # Prefer bun x electron-builder --version
    if has_bun():
        code, out, err = js_run(["bun", "x", "electron-builder", "--version"])  # type: ignore
        if code == 0:
            ver = parse_semver(out) or out.strip()
            return {"ok": True, "version": ver, "path": "bun x electron-builder"}
    if has_node():
        code, out, err = js_run(["npx", "--yes", "electron-builder", "--version"])  # type: ignore
        if code == 0:
            ver = parse_semver(out) or out.strip()
            return {"ok": True, "version": ver, "path": "npx electron-builder"}
    return {"ok": False, "version": None, "path": None}
    


def detect_esbuild() -> Dict[str, Optional[str]]:
    # Prefer bun x esbuild --version
    if has_bun():
        code, out, err = js_run(["bun", "x", "esbuild", "--version"])  # type: ignore
        if code == 0:
            return {"ok": True, "version": out.strip() or "unknown", "path": "bun x esbuild"}
    # Node fallback
    if has_node():
        code, out, err = js_run(["npx", "--yes", "esbuild", "--version"])  # type: ignore
        if code == 0:
            return {"ok": True, "version": out.strip() or "unknown", "path": "npx esbuild"}
    return {"ok": False, "version": None, "path": None}


def detect_vite() -> Dict[str, Optional[str]]:
    # Prefer bun x vite --version
    if has_bun():
        code, out, err = js_run(["bun", "x", "vite", "--version"])  # type: ignore
        if code == 0:
            return {"ok": True, "version": out.strip() or "unknown", "path": "bun x vite"}
    if has_node():
        code, out, err = js_run(["npx", "--yes", "vite", "--version"])  # type: ignore
        if code == 0:
            return {"ok": True, "version": out.strip() or "unknown", "path": "npx vite"}
    return {"ok": False, "version": None, "path": None}


def detect_electron() -> Dict[str, Optional[str]]:
    # Prefer bun x electron --version
    if has_bun():
        code, out, err = js_run(["bun", "x", "electron", "--version"])  # type: ignore
        if code == 0:
            ver = parse_semver(out) or out.strip()
            return {"ok": True, "version": ver, "path": "bun x electron"}
    if has_node():
        code, out, err = js_run(["npx", "--yes", "electron", "--version"])  # type: ignore
        if code == 0:
            ver = parse_semver(out) or out.strip()
            return {"ok": True, "version": ver, "path": "npx electron"}
    return {"ok": False, "version": None, "path": None}


def detect_electron_builder() -> Dict[str, Optional[str]]:
    # Prefer bun x electron-builder --version
    if has_bun():
        code, out, err = js_run(["bun", "x", "electron-builder", "--version"])  # type: ignore
        if code == 0:
            ver = parse_semver(out) or out.strip()
            return {"ok": True, "version": ver, "path": "bun x electron-builder"}
    if has_node():
        code, out, err = js_run(["npx", "--yes", "electron-builder", "--version"])  # type: ignore
        if code == 0:
            ver = parse_semver(out) or out.strip()
            return {"ok": True, "version": ver, "path": "npx electron-builder"}
    return {"ok": False, "version": None, "path": None}


def detect_bun() -> Dict[str, Optional[str]]:
    path = which("bun")
    if not path:
        return {"ok": False, "version": None, "path": None}
    code, out, _ = _run([path, "--version"])  # prints like 1.1.24
    ver = parse_semver(out) or out.strip()
    return {"ok": bool(ver), "version": ver, "path": path}


def read_pyproject_deps(pyproject_path: Optional[str] = None) -> List[str]:
    """Extract [project].dependencies items as a list of requirement strings.
    Avoids pulling unrelated keys (e.g., license).
    """
    path = pyproject_path or os.path.join(os.getcwd(), "pyproject.toml")
    if not os.path.isfile(path):
        return []
    try:
        with open(path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        reqs: List[str] = []
        in_project = False
        in_array = False
        buf: List[str] = []
        for raw in lines:
            l = raw.strip()
            # Track project table
            if l.startswith('['):
                in_project = (l == '[project]')
                # leaving dependencies array if we hit a new table
                if l != '[project]':
                    in_array = False
                continue
            if not in_project:
                continue
            # Find dependencies array start
            if not in_array and l.startswith('dependencies') and '=' in l:
                # Could be inline or multiline
                # Normalize to everything after '='
                after = l.split('=', 1)[1].strip()
                if after.startswith('[') and after.endswith(']'):
                    # Inline array
                    buf = [after]
                    in_array = False
                elif after.startswith('['):
                    buf = [after]
                    in_array = True
                else:
                    # Malformed; skip
                    buf = []
                    in_array = False
                # If inline, fall-through to extraction below
            elif in_array:
                buf.append(l)
                if ']' in l:
                    in_array = False
            # When we have a complete buffer (inline or closed multiline), extract
            if buf and not in_array:
                content = ' '.join(buf)
                # Extract quoted items within brackets
                m = re.findall(r'"([^"\\]*(?:\\.[^"\\]*)*)"', content)
                for item in m:
                    if item:
                        reqs.append(item)
                buf = []
        return reqs
    except Exception:
        return []


def check_python_deps(requirements: List[str]) -> Dict[str, List[str]]:
    missing: List[str] = []
    try:
        try:
            import importlib.metadata as md  # py3.8+
        except Exception:
            import importlib_metadata as md  # type: ignore
        for spec in requirements:
            name = spec.split("==")[0].split(">=")[0].split("<=")[0]
            try:
                md.version(name)
            except Exception:
                missing.append(spec)
    except Exception:
        # if detection fails, don't block
        pass
    return {"missing": missing}
