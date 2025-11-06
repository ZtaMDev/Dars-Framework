import os
import re
from typing import Iterable, Set

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
    try:
        s = _js_block_comments.sub("", src)
        s = _js_line_comments.sub(lambda m: m.group(1), s)
        # Avoid breaking strings by doing space collapsing outside quotes: basic approach
        # Split by quotes and process even indices (outside strings)
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
    try:
        s = _css_comments.sub("", src)
        s = _css_punct_spaces.sub(r"\1", s)
        s = _css_spaces.sub(" ", s)
        return s.strip()
    except Exception:
        return src


def minify_html(src: str) -> str:
    try:
        s = _html_comments.sub("", src)
        # Collapse whitespace between tags only
        s = re.sub(r">\s+<", "><", s)
        # Collapse multiple spaces in text nodes conservatively
        s = re.sub(r"\s{2,}", " ", s)
        return s.strip()
    except Exception:
        return src


def minify_output_dir(output_dir: str, extra_skip: Iterable[str] = None) -> int:
    """
    Minify HTML, CSS, and JS files in-place under output_dir.
    Skips VDOM, snapshot, and version files by default.

    Returns: number of files minified.
    """
    count = 0
    extra_skip_set: Set[str] = set(extra_skip or [])
    for root, _dirs, files in os.walk(output_dir):
        for name in files:
            if name in extra_skip_set:
                continue
            if _should_skip(name):
                continue
            full = os.path.join(root, name)
            ext = os.path.splitext(name)[1].lower()
            try:
                with open(full, 'r', encoding='utf-8') as f:
                    content = f.read()
            except Exception:
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
                    count += 1
                except Exception:
                    pass
    return count
