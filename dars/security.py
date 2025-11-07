import os
import re
from typing import Iterable, Set
from dars.core.js_bridge import esbuild_minify_js as _esbuild_minify_js, esbuild_minify_css as _esbuild_minify_css, esbuild_available as _esbuild_available

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


# --- Minifiers (conservative) ---
_js_block_comments = re.compile(r"/\*.*?\*/", re.DOTALL)
_js_line_comments = re.compile(r"(^|[^:\\])//.*?$", re.MULTILINE)
_js_spaces = re.compile(r"\s+")
_js_punct_spaces = re.compile(r"\s*([{}\[\](),;:<>+=\-*/%&|^!?])\s*")

_css_comments = re.compile(r"/\*.*?\*/", re.DOTALL)
_css_spaces = re.compile(r"\s+")
_css_punct_spaces = re.compile(r"\s*([{}:;,>~+])\s*")

_html_comments = re.compile(r"<!--(?!\s*\[if).*?-->", re.DOTALL)
_html_between_tags = re.compile(r">\s+<")
_js_string_splitter = re.compile(r'(".*?"|\'.*?\'|`.*?`)', re.DOTALL)


def minify_js(src: str) -> str:
    """Minify a JS source string. Uses esbuild if available; otherwise Python fallback."""
    # Fast path: dump to temp file and use esbuild when available
    if _esbuild_available():
        try:
            import tempfile
            with tempfile.NamedTemporaryFile('w', delete=False, suffix='.js', encoding='utf-8') as tf_in:
                tf_in.write(src)
                in_path = tf_in.name
            with tempfile.NamedTemporaryFile('r', delete=False, suffix='.js', encoding='utf-8') as tf_out:
                out_path = tf_out.name
            if _esbuild_minify_js(in_path, out_path):
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
    # Prefer fast/robust rjsmin if available
    try:
        import rjsmin  # type: ignore
        return rjsmin.jsmin(src)
    except Exception:
        pass
    # Conservative regex fallback
    try:
        s = _js_block_comments.sub("", src)
        s = _js_line_comments.sub(lambda m: m.group(1), s)
        parts = _js_string_splitter.split(s)
        for i in range(0, len(parts), 2):
            p = parts[i]
            p = _js_punct_spaces.sub(r"\1", p)
            p = _js_spaces.sub(" ", p)
            parts[i] = p
        s = "".join(parts)
        return s.strip()
    except Exception:
        return src


def minify_css(src: str) -> str:
    """Minify a CSS source string. Uses esbuild if available; otherwise Python fallback."""
    if _esbuild_available():
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
    # Prefer rcssmin if available
    try:
        import rcssmin  # type: ignore
        return rcssmin.cssmin(src)
    except Exception:
        pass
    try:
        s = _css_comments.sub("", src)
        s = _css_punct_spaces.sub(r"\1", s)
        s = _css_spaces.sub(" ", s)
        return s.strip()
    except Exception:
        return src


def minify_html(src: str) -> str:
    # Prefer htmlmin if available
    try:
        import htmlmin  # type: ignore
        return htmlmin.minify(src, remove_comments=True, remove_empty_space=True, reduce_boolean_attributes=True)
    except Exception:
        pass
    try:
        s = _html_comments.sub("", src)
        s = re.sub(r">\s+<", "><", s)
        s = re.sub(r"\s{2,}", " ", s)
        return s.strip()
    except Exception:
        return src


def minify_output_dir(output_dir: str, extra_skip: Iterable[str] = None, progress_cb=None) -> int:
    """
    Minify HTML, CSS, and JS files in-place under output_dir.
    Skips VDOM, snapshot, and version files by default.

    Returns: number of files minified.
    """
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
    for full in candidates:
        ext = os.path.splitext(full)[1].lower()
        try:
            with open(full, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception:
            processed += 1
            if progress_cb:
                try: progress_cb(processed, total)
                except Exception: pass
            continue

        new_content = None
        if ext in SAFE_JS_EXT:
            new_content = minify_js(content)
        elif ext in SAFE_CSS_EXT:
            new_content = minify_css(content)
        elif ext in SAFE_HTML_EXT:
            new_content = minify_html(content)

        if new_content is not None and new_content != content:
            try:
                with open(full, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                written += 1
            except Exception:
                pass

        processed += 1
        if progress_cb:
            try:
                progress_cb(processed, total)
            except Exception:
                pass

    return written
