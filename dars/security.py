# Dars Framework - Core Source File
#
# This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0.
# If a copy of the MPL was not distributed with this file, You can obtain one at
# https://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2025 ZtaDev
import os
import re
import subprocess
import sys
import shutil
from typing import Iterable, Optional, Set

SAFE_JS_EXT = {'.js', '.mjs', '.cjs'}
SAFE_CSS_EXT = {'.css'}
SAFE_HTML_EXT = {'.html', '.htm'}

SKIP_PATTERNS = (
    r'^snapshot.*\.json$',
    r'^version.*\.txt$',
)

_pat_compiled = [re.compile(p) for p in SKIP_PATTERNS]


def _should_skip(filename: str) -> bool:
    base = os.path.basename(filename)
    for p in _pat_compiled:
        if p.match(base):
            return True
    return False


_html_comments = re.compile(r"<!--(?!\s*\[if).*?-->", re.DOTALL)
_html_between_tags = re.compile(r">\s+<")


_PROTECT_TAGS = ("pre", "code", "textarea", "script", "style")

def _protect_html_blocks(src: str):
    """Replace whitespace-sensitive blocks with tokens to avoid minifying their contents."""
    tokens = []

    def _make_repl(match):
        tokens.append(match.group(0))
        return f"__DARS_PROTECT_{len(tokens) - 1}__"

    s = src
    for tag in _PROTECT_TAGS:
        pat = re.compile(rf"<\s*{tag}\b[^>]*?>.*?<\s*/\s*{tag}\s*>", re.IGNORECASE | re.DOTALL)
        s = pat.sub(_make_repl, s)
    return s, tokens

def _restore_html_blocks(src: str, tokens):
    s = src
    for i, block in enumerate(tokens):
        s = s.replace(f"__DARS_PROTECT_{i}__", block)
    return s


# ─── Dars Bundler Integration ─────────────────────────────────────────────────

def _find_dars_bundler() -> Optional[str]:
    """Locate the dars-bundler binary.

    Search order:
    1. DARS_BUNDLER_PATH environment variable (user override)
    2. Same directory as the running Python executable (venv/bundler co-install)
    3. PATH via shutil.which
    4. dars/bundler/ subdirectory (shipped with the framework, named by GH Action convention)
    5. Adjacent debug/release build in DarsBundler repo (dev mode)
    """
    # 1. Env override
    env_path = os.environ.get('DARS_BUNDLER_PATH', '')
    if env_path and os.path.isfile(env_path):
        return env_path

    generic = 'dars-bundler.exe' if sys.platform == 'win32' else 'dars-bundler'

    # Exact artifact_name values produced by release.yml (what lands in dars/bundler/)
    if sys.platform == 'win32':
        platform_names = ['dars-bundler-windows.exe', generic]
    elif sys.platform == 'darwin':
        import platform as _pl
        # mac-arm for Apple Silicon, mac for Intel
        if _pl.machine() == 'arm64':
            platform_names = ['dars-bundler-mac-arm', 'dars-bundler-mac', generic]
        else:
            platform_names = ['dars-bundler-mac', generic]
    else:
        platform_names = ['dars-bundler-linux', generic]

    # 2. Alongside Python executable (covers venv installs)
    py_dir = os.path.dirname(sys.executable)
    for name in platform_names:
        candidate = os.path.join(py_dir, name)
        if os.path.isfile(candidate):
            return candidate

    # 3. PATH
    for name in platform_names:
        in_path = shutil.which(name)
        if in_path:
            return in_path

    # 4. dars/bundler/ shipped with the framework
    try:
        pkg_dir = os.path.dirname(os.path.abspath(__file__))
        bundler_dir = os.path.join(pkg_dir, 'bundler')
        for name in platform_names:
            candidate = os.path.join(bundler_dir, name)
            if os.path.isfile(candidate):
                return candidate
    except Exception:
        pass

    # 5. Dev: DarsBundler repo debug/release build
    try:
        pkg_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(pkg_dir)
        bundler_repo = os.path.join(os.path.dirname(project_root), 'DarsBundler', 'dars-bundler')
        for sub in (os.path.join('target', 'release'), os.path.join('target', 'debug')):
            candidate = os.path.join(bundler_repo, sub, generic)
            if os.path.isfile(candidate):
                return candidate
    except Exception:
        pass

    return None


def dars_bundler_minify(output_dir: str, progress_cb=None) -> bool:
    """Run the dars-bundler binary on the given output directory.

    Returns True if the bundler ran successfully, False otherwise.
    """
    bundler = _find_dars_bundler()
    if not bundler:
        return False

    cmd = [bundler, '--input', output_dir]
    try:
        p = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
        )
        lines = []
        for line in iter(p.stdout.readline, ''):
            line = line.rstrip()
            if line:
                lines.append(line)
                if progress_cb:
                    try:
                        progress_cb(0, 1)   # indeterminate tick
                    except Exception:
                        pass
        p.wait()
        if progress_cb:
            try:
                progress_cb(1, 1)
            except Exception:
                pass
        return p.returncode == 0
    except Exception:
        return False


# ─── Per-string helpers (kept for in-memory use in the exporter) ───────────────

def minify_js(src: str) -> str:
    """Minify a JS source string using dars-bundler (file-level) or fall back gracefully."""
    # dars-bundler operates on files/dirs; for in-memory strings we write a temp file.
    bundler = _find_dars_bundler()
    if bundler:
        import tempfile
        try:
            with tempfile.TemporaryDirectory() as td:
                in_path = os.path.join(td, '_input.js')
                with open(in_path, 'w', encoding='utf-8') as f:
                    f.write(src)
                ret = subprocess.run(
                    [bundler, '--input', td],
                    capture_output=True, text=True
                )
                if ret.returncode == 0:
                    with open(in_path, 'r', encoding='utf-8') as f:
                        result = f.read()
                    if result:
                        return result
        except Exception:
            pass

    # Graceful no-op if bundler not available
    return src


def minify_css(src: str) -> str:
    """Minify a CSS source string using dars-bundler or fall back gracefully."""
    bundler = _find_dars_bundler()
    if bundler:
        import tempfile
        try:
            with tempfile.TemporaryDirectory() as td:
                in_path = os.path.join(td, '_input.css')
                with open(in_path, 'w', encoding='utf-8') as f:
                    f.write(src)
                ret = subprocess.run(
                    [bundler, '--input', td],
                    capture_output=True, text=True
                )
                if ret.returncode == 0:
                    with open(in_path, 'r', encoding='utf-8') as f:
                        result = f.read()
                    if result:
                        return result
        except Exception:
            pass

    return src


def minify_html(src: str) -> str:
    """Conservative HTML minifier (whitespace collapse only — no external tool needed)."""
    try:
        protected_src, tokens = _protect_html_blocks(src)
        s = _html_comments.sub("", protected_src)
        s = _html_between_tags.sub("><", s)
        s = s.strip()
        s = _restore_html_blocks(s, tokens)
        return s
    except Exception:
        return src


def minify_output_dir(output_dir: str, extra_skip: Iterable[str] = None, progress_cb=None) -> int:
    """
    Minify JS and CSS files in-place under output_dir using dars-bundler.

    If dars-bundler is not available, returns 0 (no files minified) without error.
    HTML minification is always handled by BeautifulSoup in the exporter.

    Returns: number of files minified (approximate when using bundler).
    """
    # Check if minification is enabled
    minify_enabled = os.environ.get('DARS_MINIFY', '1') != '0'
    if not minify_enabled:
        return 0

    # Try dars-bundler first (preferred, fast, correct)
    ok = dars_bundler_minify(output_dir, progress_cb=progress_cb)
    if ok:
        # Count JS+CSS files as "processed" for UI feedback
        count = 0
        for root, _dirs, files in os.walk(output_dir):
            for name in files:
                ext = os.path.splitext(name)[1].lower()
                if ext in SAFE_JS_EXT or ext in SAFE_CSS_EXT:
                    count += 1
        return count

    # Bundler not available — silently skip (no rjsmin/rcssmin fallback)
    return 0
