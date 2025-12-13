# Dars Framework - Core Source File
#
# This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0.
# If a copy of the MPL was not distributed with this file, You can obtain one at
# https://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2025 ZtaDev
# Minimal Desktop API registry for Electron bridge
# This module defines a simple API schema that the JS generator can use
# to emit a preload script and a JS stub exposed on window.DarsDesktopAPI.

from typing import Dict, Callable, Any

# Registry maps namespace -> method -> callable (placeholder signatures)
_API_REGISTRY: Dict[str, Dict[str, Callable[..., Any]]] = {}


def register(namespace: str, name: str, func: Callable[..., Any]) -> None:
    """Register a Python function under a desktop API namespace."""
    if namespace not in _API_REGISTRY:
        _API_REGISTRY[namespace] = {}
    _API_REGISTRY[namespace][name] = func


def get_schema() -> Dict[str, Dict[str, str]]:
    """Return a minimal schema of available API methods for codegen.
    Values are string signatures (placeholder), keeping it simple for Phase 2.
    """
    schema: Dict[str, Dict[str, str]] = {}
    for ns, methods in _API_REGISTRY.items():
        schema[ns] = {m: "(...args)" for m in methods.keys()}
    return schema


def _not_implemented(*_args, **_kwargs):
    raise NotImplementedError("Desktop API method not implemented")

# Register FileSystem API methods
register("FileSystem", "read_text", _not_implemented)
register("FileSystem", "write_text", _not_implemented)
register("FileSystem", "read_file", _not_implemented)
register("FileSystem", "write_file", _not_implemented)
register("FileSystem", "list_directory", _not_implemented)
