"""Desktop helper shim for Dars.

Exports a small FileSystem API usable from Python (`dars.desktop.read_text` / `write_text`)
and also registers those functions in the desktop API registry so the Electron exporter
can generate the preload/stub bridge automatically.

This module is intentionally very small and local-file-system based. The electron
backend (main.js) also implements the same channels so renderer code can call
`window.DarsDesktopAPI.FileSystem.read_text(...)` and the Node side will handle it.

Note: these functions are intended for desktop-only use. The CLI's generated
`main.py` template will import `from dars.desktop import *` only when creating a
`desktop` project scaffold.
"""
from __future__ import annotations
from typing import Optional
import os
from . import api as _api
from dars.scripts.dscript import dScript
import json

# Internal list of dScripts automatically created by desktop helpers.
# Exporter will attempt to include these when building pages for desktop targets.
_auto_scripts = []  # type: list[dScript]

__all__ = ["read_text", "write_text"]


def read_text(file_path: str, encoding: str = 'utf-8', then: Optional[str] = None, autoinclude: bool = False, import_stub: bool = True) -> dScript:
    """Create a dScript that will call the desktop FileSystem.read_text.

    This returns a dScript suitable to be added to `app.scripts`/`page.scripts`
    or assigned to event handlers. The optional `then` string will be executed
    in a `.then(function(result){ ... })` callback.
    """
    return _call_as_dscript('FileSystem', 'read_text', file_path, encoding, then=then, autoinclude=autoinclude, import_stub=import_stub)


def write_text(file_path: str, data: str, encoding: str = 'utf-8', then: Optional[str] = None, autoinclude: bool = False, import_stub: bool = True) -> dScript:
    """Create a dScript that will call the desktop FileSystem.write_text.

    Returns a dScript suitable to be added to `app.scripts`/`page.scripts` or
    used as an event handler. Optionally provide `then` JS to handle the
    promise result.
    """
    return _call_as_dscript('FileSystem', 'write_text', file_path, data, encoding, then=then, autoinclude=autoinclude, import_stub=import_stub)


# Note: no Python-exec filesystem helpers are exposed by default. The
# desktop API helpers are JS-first factories (read_text/write_text) which
# return dScript objects to be executed in the renderer. The API schema
# (in dars.desktop.api) already contains placeholders used by the generator.


# ---- dScript factory helpers ----
def _serialize_arg(arg):
    # Try to serialize basic types to JS literal safely
    try:
        return json.dumps(arg)
    except Exception:
        return json.dumps(str(arg))


def _call_as_dscript(namespace: str, method: str, *args, then: Optional[str] = None, autoinclude: bool = False, import_stub: bool = True) -> dScript:
    """Create a dScript that calls the desktop bridge and optionally runs `then` JS with the result.

    The created dScript is appended to _auto_scripts so exporters can include it automatically.
    """
    js_args = ", ".join(_serialize_arg(a) for a in args)
    # Use DarsDesktopAPI directly; the renderer stub file (`dars_desktop_stub.js`) exposes
    # a top-level `DarsDesktopAPI` binding. Avoid using `window.` so module imports
    # or bundlers that export the stub will work as expected.
    call = f"DarsDesktopAPI.{namespace}.{method}({js_args})"
    if then:
        body = f"{call}.then(function(result){{ {then} }}).catch(function(e){{ console.error(e); }});"
    else:
        # Default: log the result to console to make the call visible in desktop builds
        body = f"{call}.then(function(result){{ console.log(result); }}).catch(function(e){{ console.error(e); }});"

    if import_stub:
        # Use a dynamic import with fallback to a global DarsIPC bridge if the
        # stub file is missing (dev preview). This avoids silent failures when
        # './lib/dars_desktop_stub.js' isn't present.
        code = (
            "(async () => {\n"
            "  try {\n"
            "    const m = await import('./lib/dars_desktop_stub.js');\n"
            "    return m.DarsDesktopAPI.%s;\n"
            "  } catch (e) {\n"
            "    try {\n"
            "      if (typeof globalThis !== 'undefined' && globalThis.DarsIPC && typeof globalThis.DarsIPC.invoke === 'function') {\n"
            "        return globalThis.DarsIPC.invoke('dars::%s::%s', %s);\n"
            "      }\n"
            "    } catch(_) {}\n"
            "    throw e;\n"
            "  }\n"
            "})().then(r => r).catch(e => { console.error(e); });\n"
        )
        # The placeholders below will be formatted with namespace/method/args
        # but we need to inject the real body call rather than just returning m.DarsDesktopAPI.
        # To keep consistent behavior (then/catch wrappers), build an IIFE that calls the method.
        ns = namespace
        meth = method
        # Escape the js_args as provided (already JSON-encoded literals)
        args_literal = js_args
        dynamic_code = (
            "(async () => {\n"
            "  try {\n"
            "    const m = await import('./lib/dars_desktop_stub.js');\n"
            f"    return m.DarsDesktopAPI.{ns}.{meth}({args_literal});\n"
            "  } catch (e) {\n"
            "    try {\n"
            "      if (typeof globalThis !== 'undefined' && globalThis.DarsIPC && typeof globalThis.DarsIPC.invoke === 'function') {\n"
            f"        return globalThis.DarsIPC.invoke('dars::{ns}::{meth}', {args_literal});\n"
            "      }\n"
            "    } catch(_) {}\n"
            "    throw e;\n"
            "  }\n"
            "})()"
        )
        # Attach then/catch handlers similar to previous `body` variable
        if then:
            code = f"{dynamic_code}.then(function(result){{ {then} }}).catch(function(e){{ console.error(e); }});"
        else:
            code = f"{dynamic_code}.then(function(result){{ console.log(result); }}).catch(function(e){{ console.error(e); }});"
        ds = dScript(code=code, module=True)
    else:
        code = body
        ds = dScript(code=code)
    # Only append to automatic list if explicitly requested. This avoids
    # duplicating the same dScript when callers do `app.add_script(write_text(...))`.
    if autoinclude:
        try:
            _auto_scripts.append(ds)
        except Exception:
            pass
    return ds

