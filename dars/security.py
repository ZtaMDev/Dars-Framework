# Dars Framework - Core Source File
#
# This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0.
# If a copy of the MPL was not distributed with this file, You can obtain one at
# https://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2025 ZtaDev
import os
import re
import shutil
import subprocess
from typing import Iterable, Set
from dars.core.js_bridge import (
    esbuild_minify_js as _esbuild_minify_js,
    esbuild_minify_css as _esbuild_minify_css,
    esbuild_available as _esbuild_available,
    vite_minify_js as _vite_minify_js,
    vite_available as _vite_available,
)

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
        # Match opening tag with attributes, non-greedy content, then closing tag
        pat = re.compile(rf"<\s*{tag}\b[^>]*?>.*?<\s*/\s*{tag}\s*>", re.IGNORECASE | re.DOTALL)
        s = pat.sub(_make_repl, s)
    return s, tokens

def _restore_html_blocks(src: str, tokens):
    s = src
    for i, block in enumerate(tokens):
        s = s.replace(f"__DARS_PROTECT_{i}__", block)
    return s


def minify_js(src: str) -> str:
    """Minify a JS source string.

    Default: Python-native rjsmin.
    Optional: when DARS_VITE_MINIFY=1 and the toolchain is available, use Vite/esbuild.
    """
    _vite_enabled = os.getenv('DARS_VITE_MINIFY', '1') == '1'

    def _node_check_js(path: str) -> bool:
        try:
            node = shutil.which('node') or shutil.which('node.exe')
            if not node:
                return True
            p = subprocess.run([node, '--check', path], capture_output=True, text=True)
            return p.returncode == 0
        except Exception:
            return True

    if _vite_enabled:
        try:
            import tempfile
            with tempfile.NamedTemporaryFile('w', delete=False, suffix='.js', encoding='utf-8') as tf_in:
                tf_in.write(src)
                in_path = tf_in.name
            with tempfile.NamedTemporaryFile('r', delete=False, suffix='.js', encoding='utf-8') as tf_out:
                out_path = tf_out.name

            ok = False
            if _vite_available():
                ok = _vite_minify_js(in_path, out_path)
                if ok and not _node_check_js(out_path):
                    ok = False

            if not ok and _esbuild_available():
                ok = _esbuild_minify_js(in_path, out_path)

            if ok:
                try:
                    with open(out_path, 'r', encoding='utf-8') as fr:
                        return fr.read()
                finally:
                    try:
                        os.remove(in_path)
                    except Exception:
                        pass
                    try:
                        os.remove(out_path)
                    except Exception:
                        pass
        except Exception:
            pass

    # Default Python-native minifier
    try:
        import rjsmin  # type: ignore
        return rjsmin.jsmin(src)
    except Exception:
        return src


def minify_css(src: str) -> str:
    """Minify a CSS source string.

    Default: Python-native rcssmin.
    Optional: when DARS_VITE_MINIFY=1 and esbuild is available, use esbuild.
    """
    _vite_enabled = os.getenv('DARS_VITE_MINIFY', '1') == '1'
    if _vite_enabled and _esbuild_available():
        try:
            import tempfile
            with tempfile.NamedTemporaryFile('w', delete=False, suffix='.css', encoding='utf-8') as tf_in:
                tf_in.write(src)
                in_path = tf_in.name
            with tempfile.NamedTemporaryFile('r', delete=False, suffix='.css', encoding='utf-8') as tf_out:
                out_path = tf_out.name
            if _esbuild_minify_css(in_path, out_path):
                try:
                    with open(out_path, 'r', encoding='utf-8') as fr:
                        return fr.read()
                finally:
                    try: os.remove(in_path)
                    except Exception: pass
                    try: os.remove(out_path)
                    except Exception: pass
        except Exception:
            pass
    try:
        import rcssmin  # type: ignore
        return rcssmin.cssmin(src)
    except Exception:
        return src


def minify_html(src: str) -> str:
    """Conservative HTML minifier that preserves formatting-sensitive blocks.

    Behavior:
    - Always remove non-conditional HTML comments and collapse only inter-tag
      whitespace outside protected blocks (<pre>, <code>, <textarea>, <script>, <style>).
    - Does not collapse text-node spaces.
    """
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
    Minify HTML, CSS, and JS files in-place under output_dir.
    Skips VDOM, snapshot, and version files by default.

    Returns: number of files minified.
    """
    # Determine modes
    default_on = True
    vite_on = False
    try:
        default_on = os.environ.get('DARS_DEFAULT_MINIFY', '1') != '0'
        vite_on = os.environ.get('DARS_VITE_MINIFY', '1') == '1'
    except Exception:
        default_on = True
        vite_on = False
    
    # Gather candidates first to allow accurate progress reporting
    extra_skip_set: Set[str] = set(extra_skip or [])
    candidates = []
    for root, _dirs, files in os.walk(output_dir):
        for name in files:
            if name in extra_skip_set:
                continue
            if _should_skip(name):
                continue
            ext = os.path.splitext(name)[1].lower()
            if ext in SAFE_JS_EXT or ext in SAFE_CSS_EXT or ext in SAFE_HTML_EXT:
                candidates.append(os.path.join(root, name))

    total = len(candidates)
    processed = 0
    written = 0

    # Optional parallel minification (spawns external tools in parallel).
    # Keep workers conservative to avoid saturating the system.
    parallel_on = False
    workers = 1
    try:
        parallel_on = os.environ.get('DARS_MINIFY_PARALLEL', '0') == '1'
        workers = int(os.environ.get('DARS_MINIFY_WORKERS', '') or '0')
    except Exception:
        parallel_on = False
        workers = 1
    if workers <= 0:
        try:
            workers = max(1, min(4, (os.cpu_count() or 2)))
        except Exception:
            workers = 2
    
    # NUEVO: Priorizar archivos combinados (app.js) sobre archivos individuales
    # Cuando viteMinify está activado, solo minificar archivos app.js y ignorar los individuales
    if vite_on:
        # Filtrar candidatos: mantener solo app.js y eliminar archivos individuales que están combinados
        filtered_candidates = []
        individual_files_to_skip = set()
        
        # Identificar archivos app.js existentes
        app_js_files = [c for c in candidates if 'app.js' in c or 'app_' in c]
        
        # Para cada app.js, identificar los archivos individuales que reemplaza
        for app_js in app_js_files:
            app_js_name = os.path.basename(app_js)
            if app_js_name == 'app.js':
                # En single-page, reemplaza runtime_dars.js, script.js, vdom_tree.js
                individual_files_to_skip.update(['runtime_dars.js', 'script.js', 'vdom_tree.js'])
            elif app_js_name.startswith('app_') and app_js_name.endswith('.js'):
                # En multipágina, reemplaza los archivos correspondientes a esa página
                slug = app_js_name[4:-3]  # Extraer slug de app_{slug}.js
                individual_files_to_skip.update([
                    f'runtime_dars_{slug}.js',
                    f'script_{slug}.js', 
                    f'vdom_tree_{slug}.js'
                ])
        
        # Filtrar candidatos: mantener solo app.js y otros archivos que no sean individuales
        for candidate in candidates:
            candidate_name = os.path.basename(candidate)
            if candidate_name in individual_files_to_skip:
                continue  # Saltar archivos individuales que están combinados
            filtered_candidates.append(candidate)
        
        candidates = filtered_candidates
        total = len(candidates)

    def _minify_one(full_path: str):
        nonlocal written
        ext0 = os.path.splitext(full_path)[1].lower()

        # Skip HTML minification completely
        if ext0 in SAFE_HTML_EXT:
            return False

        # Embedded core runtime bundle: never run Vite/esbuild on it.
        # It is already minified and toolchains can corrupt it (e.g. emit ESM exports).
        # If you still want to re-minify it, do it with Python-only rjsmin.
        base0 = os.path.basename(full_path)
        if ext0 in SAFE_JS_EXT and base0 == 'dars.min.js':
            # Fall back to Python-only rjsmin (never run Vite on this file)
            try:
                with open(full_path, 'r', encoding='utf-8') as f:
                    content0 = f.read()
                try:
                    import rjsmin  # type: ignore
                    new_content0 = rjsmin.jsmin(content0)
                except Exception:
                    new_content0 = content0
                if new_content0 is not None and new_content0 != content0:
                    with open(full_path, 'w', encoding='utf-8') as f:
                        f.write(new_content0)
                    return True
            except Exception:
                return False
            return False

        try:
            with open(full_path, 'r', encoding='utf-8') as f:
                content0 = f.read()
        except Exception:
            return False

        new_content0 = None
        if ext0 in SAFE_JS_EXT:
            if default_on or vite_on:
                new_content0 = minify_js(content0)
        elif ext0 in SAFE_CSS_EXT:
            if default_on or vite_on:
                new_content0 = minify_css(content0)

        if new_content0 is not None and new_content0 != content0:
            try:
                with open(full_path, 'w', encoding='utf-8') as f:
                    f.write(new_content0)
                return True
            except Exception:
                return False
        return False

    if parallel_on and total > 1:
        import threading
        from concurrent.futures import ThreadPoolExecutor, as_completed

        lock = threading.Lock()

        with ThreadPoolExecutor(max_workers=workers) as ex:
            futures = {ex.submit(_minify_one, p): p for p in candidates}
            for fut in as_completed(futures):
                changed = False
                try:
                    changed = bool(fut.result())
                except Exception:
                    changed = False
                with lock:
                    processed += 1
                    if changed:
                        written += 1
                    if progress_cb:
                        try:
                            progress_cb(processed, total)
                        except Exception:
                            pass
    else:
        for full in candidates:
            changed = False
            try:
                changed = _minify_one(full)
            except Exception:
                changed = False

            processed += 1
            if changed:
                written += 1
            if progress_cb:
                try:
                    progress_cb(processed, total)
                except Exception:
                    pass

    return written
