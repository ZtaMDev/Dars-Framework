# Minimal Desktop API registry for Electron bridge (Phase 2)
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


# Example placeholder API (no-op implementations for Phase 2)
# Users will replace with real functions in Phase 3.

def _not_implemented(*_args, **_kwargs):
    raise NotImplementedError("Desktop API method not implemented")

# Pre-register a simple namespace to demonstrate generator output
register("FileSystem", "read_text", _not_implemented)
register("FileSystem", "write_text", _not_implemented)
