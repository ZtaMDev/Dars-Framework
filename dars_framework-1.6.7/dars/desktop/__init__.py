# Dars Framework - Core Source File
#
# This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0.
# If a copy of the MPL was not distributed with this file, You can obtain one at
# https://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2025 ZtaDev
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

from typing import Union, Optional
# Internal list of dScripts automatically created by desktop helpers.
# Exporter will attempt to include these when building pages for desktop targets.
_auto_scripts = []  # type: list[dScript]

__all__ = ["read_text", "write_text", "read_file", "write_file", "get_value", "list_directory"]


def get_value(element_id: str):
    """Get the value of an input element as a RawJS variable.
    
    This allows using dynamic values from inputs, textareas, etc. in file operations.
    
    Args:
        element_id: The ID of the element to get the value from
        
    Returns:
        RawJS object containing JavaScript to access the element's value
        
    Example:
        ```python
        path_input = Input(id="file_path")
        save_btn = Button("Save",
            on_click=write_text(
                get_value("file_path"),  # Dynamic path from input
                get_value("editor")      # Dynamic content
            )
        )
        ```
    """
    from dars.scripts.dscript import RawJS
    return RawJS(f"document.getElementById('{element_id}').value")


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


def read_file(file_path: str, then: Optional[str] = None,
              autoinclude: bool = False, import_stub: bool = True,
              as_data_url: bool = False) -> dScript:

    var_name = f"_dars_fs_{abs(hash(file_path))}"

    if then is None:
        then = f"console.log('Read {file_path}, bytes:', value.byteLength);"

    # DESKTOP JS
    desktop_js = f"""
(async () => {{
    try {{
        const raw = await DarsDesktopAPI.FileSystem.read_file({json.dumps(file_path)});
        const {var_name} = new Uint8Array(raw.data);
        const value = {var_name};
        {then}
        return value;
    }} catch (e) {{
        console.error("Desktop read_file error:", e);
        throw e;
    }}
}})()
""".strip()

    # STATIC JS
    converter = "readAsDataURL" if as_data_url else "readAsArrayBuffer"

    static_js = f"""
(async () => {{
    try {{
        const response = await fetch({json.dumps(file_path)});
        if (!response.ok) throw new Error("HTTP " + response.status);
        const blob = await response.blob();

        const reader = new FileReader();

        return new Promise((resolve, reject) => {{
            reader.onload = e => {{
                const {var_name} = e.target.result;
                const value = {var_name};
                {then}
                resolve(value);
            }};
            reader.onerror = reject;
            reader.{converter}(blob);
        }});
    }} catch (e) {{
        console.error("Static read_file error:", e);
        throw e;
    }}
}})()
""".strip()

    final_js = f"""
(() => {{
    if (typeof DarsDesktopAPI !== "undefined" && DarsDesktopAPI.FileSystem) {{
        return {desktop_js};
    }}
    return {static_js};
}})()
""".strip()

    return dScript(code=final_js)


def write_file(file_path: str, data: Union[bytes, str, dScript], 
              then: Optional[str] = None, autoinclude: bool = False, 
              import_stub: bool = True) -> dScript:
    """Write data to a file.
    
    In desktop: Writes directly to the filesystem
    In browser: Triggers a download
    
    Args:
        file_path: Path where to save the file
        data: Data to write (bytes, string, or dScript that evaluates to data)
        then: JavaScript code to execute after writing
        autoinclude: If True, automatically include this script in the page
        import_stub: If True, include the desktop API stub
    """
    if isinstance(data, (bytes, bytearray)):
        data = list(data)
    return _call_as_dscript('FileSystem', 'write_file', file_path, data,
                          then=then, autoinclude=autoinclude, import_stub=import_stub)


def list_directory(directory_path: str, pattern: str = "*", include_size: bool = False,
                   then: Optional[str] = None, autoinclude: bool = False,
                   import_stub: bool = True) -> dScript:
    """List files and folders in a directory.
    
    Returns an array of objects with: {name, isDirectory, size (optional)}
    
    Args:
        directory_path: Path to the directory to list (supports get_value() for dynamic paths)
        pattern: Glob pattern to filter results (default: "*" for all)
        include_size: Whether to include file sizes in bytes (default: False)
        then: JavaScript code to execute with the result (use 'value' to access result)
        autoinclude: If True, automatically include this script in the page
        import_stub: If True, include the desktop API stub
        
    Returns:
        dScript that when executed returns an array of file/folder objects
        
    Example with this() state update:
        ```python
        from dars.desktop import list_directory, get_value
        from dars.core.state import this
        
        # Simple list - just names
        Button("List", 
            on_click=list_directory(get_value("path")).then(
                this().state(id="output", text=RawJS("value.map(f => f.name).join('\\\\n')"))
            )
        )
        
        # Filter by pattern
        Button("List Python Files",
            on_click=list_directory(".", "*.py").then(
                this().state(id="count", text=RawJS("`Found ${value.length} files`"))
            )
        )
        ```
        
    Example with Arg helper (Pythonic):
        ```python
        from dars.scripts.dscript import Arg
        
        # Using Arg for cleaner syntax (coming soon - currently use 'value' directly)
        list_directory(".").then(
            this().state(id="files", text=Arg.map("f => f.name").join("\\\\n"))
        )
        ```
    """
    return _call_as_dscript('FileSystem', 'list_directory', directory_path, pattern, include_size,
                          then=then, autoinclude=autoinclude, import_stub=import_stub)


# Note: no Python-exec filesystem helpers are exposed by default. The
# desktop API helpers are JS-first factories (read_text/write_text) which
# return dScript objects to be executed in the renderer. The API schema
# (in dars.desktop.api) already contains placeholders used by the generator.


# ---- dScript factory helpers ----
def _serialize_arg(arg):
    """Serialize Python arguments to JavaScript code.
    
    Handles RawJS objects for dynamic values (e.g., from get_value()).
    """
    from dars.scripts.dscript import RawJS
    
    # If it's a RawJS object, use the raw code directly
    if isinstance(arg, RawJS):
        return arg.code
    
    # Try to serialize basic types to JS literal safely
    try:
        return json.dumps(arg)
    except Exception:
        return json.dumps(str(arg))


def _call_as_dscript(namespace: str, method: str, *args,
                     then: Optional[str] = None,
                     autoinclude: bool = False,
                     import_stub: bool = True) -> dScript:

    js_args = ", ".join([_serialize_arg(arg) for arg in args])
    api_call = f"DarsDesktopAPI.{namespace}.{method}({js_args})"

    js = f"""
(async () => {{
    try {{
        const result = await {api_call};
        {then or ""}
        return result;
    }} catch (e) {{
        console.error("Desktop API error:", e);
        throw e;
    }}
}})()
""".strip()

    ds = dScript(code=js)
    if autoinclude:
        _auto_scripts.append(ds)

    return ds


