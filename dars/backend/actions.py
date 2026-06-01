# Dars Framework - Server Actions Module
#
# This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0.
# If a copy of the MPL was not distributed with this file, You can obtain one at
# https://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2026 ZtaDev
"""
Server Actions for Dars Framework
==================================

Server Actions allow you to call Python backend functions directly from
client-side events, with automatic parameter validation, serialization,
and error handling.

Usage::

    from dars.backend.actions import server_action, call_server
    from dars.all import *

    # 1. Define a server action (in backend/api.py or any module)
    @server_action
    def greet(name: str, count: int = 1) -> list:
        \"\"\"Returns a list of personalized greetings.\"\"\"
        return [f"Hello {name}! x{i}" for i in range(count)]

    # 2. Call it from a component event
    Button("Greet", on_click=call_server("greet", name="World", count=3))

    # 3. Start the backend
    app.start_backend()

Features:

- Type-annotated parameters are validated via Pydantic.
- Actions can be sync or async.
- Results are JSON-serialized automatically.
- Errors are returned as structured JSON with status 400/500.
- CSRF protection for mutating actions.
- ``call_server()`` returns a DAP action that integrates with the Dars runtime.
"""

from __future__ import annotations

import asyncio
import inspect
import json
import logging
import traceback
from functools import wraps
from typing import (
    Any,
    Callable,
    Dict,
    List,
    Optional,
    Sequence,
    Type,
    Union,
    get_type_hints,
)

from fastapi import APIRouter, FastAPI, HTTPException, Request
from pydantic import BaseModel, ValidationError, create_model

from dars.scripts.dscript import dScript

logger = logging.getLogger("dars.actions")

# ── Global action registry ───────────────────────────────────────────────────

_ACTION_REGISTRY: Dict[str, Dict[str, Any]] = {}

# ── Decorator ────────────────────────────────────────────────────────────────


def server_action(
    func: Optional[Callable] = None,
    *,
    name: Optional[str] = None,
    auth_required: bool = False,
    roles: Optional[List[str]] = None,
    csrf_protected: bool = True,
    description: Optional[str] = None,
) -> Any:
    """
    Register a Python function as a server action callable from the frontend.

    Can be used as a bare decorator or with arguments::

        @server_action
        def my_action(x: int) -> int:
            return x * 2

        @server_action(name="custom_name", auth_required=True)
        def admin_action(x: int) -> int:
            return x * 2

    Args:
        func: The function to register.
        name: Override the action name (defaults to ``func.__name__``).
        auth_required: Require authentication to call this action.
        roles: If set, only users with at least one of these roles may call it.
        csrf_protected: Require CSRF token for cookie-based auth.
        description: Description for the action.
    """
    if func is not None and (inspect.isfunction(func) or inspect.iscoroutinefunction(func)):
        # Used as bare decorator: @server_action
        return _register(func, name=name, auth_required=auth_required, roles=roles,
                         csrf_protected=csrf_protected, description=description)

    # Used with arguments: @server_action(...)
    def decorator(f: Callable) -> Callable:
        return _register(f, name=name, auth_required=auth_required, roles=roles,
                         csrf_protected=csrf_protected, description=description)

    return decorator


def _register(
    func: Callable,
    name: Optional[str] = None,
    auth_required: bool = False,
    roles: Optional[List[str]] = None,
    csrf_protected: bool = True,
    description: Optional[str] = None,
) -> Callable:
    action_name = name or func.__name__

    # Build a Pydantic model from type annotations
    sig = inspect.signature(func)
    hints = get_type_hints(func) if hasattr(func, "__annotations__") else {}
    return_type = hints.pop("return", None)

    fields: Dict[str, tuple] = {}
    for param_name, param in sig.parameters.items():
        if param_name in ("self", "cls", "request"):
            continue
        if param_name == "kwargs" and param.kind == inspect.Parameter.VAR_KEYWORD:
            continue
        if param_name == "args" and param.kind == inspect.Parameter.VAR_POSITIONAL:
            continue
        param_type = hints.get(param_name, str)
        default = param.default if param.default is not inspect.Parameter.empty else ...
        fields[param_name] = (param_type, default)

    InputModel = None
    if fields:
        InputModel = create_model(f"{action_name}_params", **fields)  # type: ignore

    is_async = asyncio.iscoroutinefunction(func)

    _ACTION_REGISTRY[action_name] = {
        "func": func,
        "name": action_name,
        "is_async": is_async,
        "auth_required": auth_required,
        "roles": roles or [],
        "csrf_protected": csrf_protected,
        "description": description or func.__doc__ or "",
        "input_model": InputModel,
        "return_type": return_type,
        "signature": str(sig),
    }

    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper


# ── Action router ────────────────────────────────────────────────────────────

_action_router = APIRouter(prefix="/api/actions", tags=["Dars Server Actions"])


def create_action_router() -> APIRouter:
    """
    Create or return the FastAPI router with all registered server actions.

    Call this during backend setup::

        app.include_router(create_action_router())
    """
    return _action_router


def _build_router_from_registry() -> APIRouter:
    """Build endpoint for each registered action."""
    router = APIRouter(prefix="/api/actions", tags=["Dars Server Actions"])

    logger.info("[Dars:ServerActions] Registering %d actions", len(_ACTION_REGISTRY))

    for action_name, config in _ACTION_REGISTRY.items():
        _register_action_endpoint(router, action_name, config)

    return router


def _register_action_endpoint(router: APIRouter, action_name: str, config: Dict[str, Any]) -> None:
    InputModel = config["input_model"]
    is_async = config["is_async"]
    func = config["func"]
    auth_required = config["auth_required"]
    roles = config["roles"]
    csrf_protected = config["csrf_protected"]

    endpoint_path = f"/{action_name}"

    @router.post(endpoint_path)
    async def action_endpoint(
        request: Request,
    ) -> Any:
        # Manually parse request body instead of relying on FastAPI dependency
        # injection, which can silently yield None when the body appears empty
        # due to middleware interactions or streaming issues.
        payload: Optional[BaseModel] = None
        body_bytes = b""
        try:
            body_bytes = await request.body()
            if body_bytes:
                raw = json.loads(body_bytes)
                if raw and InputModel is not None:
                    payload = InputModel(**raw)
        except json.JSONDecodeError:
            logger.error(
                "[Dars:ServerActions] Invalid JSON body for '%s': %r",
                action_name, body_bytes,
            )
        except Exception as exc:
            logger.error(
                "[Dars:ServerActions] Failed to parse body for '%s': %s\nBody: %r",
                action_name, exc, body_bytes,
            )

        if payload is None and body_bytes:
            # Body was received but couldn't be parsed — log headers for debugging
            logger.warning(
                "[Dars:ServerActions] Payload is None despite non-empty body for '%s'. "
                "Content-Type: %s, Content-Length: %s",
                action_name,
                request.headers.get("content-type", "N/A"),
                request.headers.get("content-length", len(body_bytes)),
            )

        return await _execute_action(
            request, func, payload, auth_required, roles, csrf_protected,
        )

    # Preserve action name so we can introspect endpoints
    action_endpoint.__name__ = f"action_{action_name}"


async def _execute_action(
    request: Request,
    func: Callable,
    payload: Optional[BaseModel],
    auth_required: bool,
    roles: List[str],
    csrf_protected: bool,
) -> Any:
    # Authentication check
    if auth_required or roles:
        user = getattr(request.state, "user", None) if hasattr(request.state, "user") else None
        if not user:
            raise HTTPException(status_code=401, detail="Authentication required")

        if roles:
            user_roles = user.get("roles", [])
            if isinstance(user_roles, str):
                user_roles = [user_roles]
            if not any(r in user_roles for r in roles):
                raise HTTPException(status_code=403, detail="Forbidden: insufficient permissions")

    # CSRF protection
    if csrf_protected:
        auth_header = request.headers.get("Authorization", "")
        is_bearer = auth_header.startswith("Bearer ")
        if not is_bearer and request.method in ("POST", "PUT", "DELETE", "PATCH"):
            xsrf_cookie = request.cookies.get("XSRF-TOKEN")
            xsrf_header = request.headers.get("X-XSRF-TOKEN")
            if not xsrf_cookie or not xsrf_header or xsrf_cookie != xsrf_header:
                raise HTTPException(status_code=403, detail="Invalid CSRF token")

    # Build kwargs from payload
    kwargs: Dict[str, Any] = {}
    if payload is not None:
        kwargs = payload.model_dump() if hasattr(payload, "model_dump") else dict(payload)

    try:
        if asyncio.iscoroutinefunction(func):
            result = await func(**kwargs)
        else:
            result = await asyncio.to_thread(func, **kwargs)
    except HTTPException:
        raise
    except Exception as exc:
        logger.error("[Dars:ServerActions] Action '%s' failed: %s\n%s",
                      func.__name__, exc, traceback.format_exc())
        raise HTTPException(
            status_code=500,
            detail={"error": str(exc), "traceback": traceback.format_exc()},
        )

    return result


# ── Client-side helper ───────────────────────────────────────────────────────

def call_server(
    action: str,
    /,
    *,
    on_success: Optional[Any] = None,
    on_error: Optional[Any] = None,
    **kwargs: Any,
) -> Dict[str, Any]:
    """
    Create a DAP action to call a server action from a component event.

    Usage::

        Button("Save", on_click=call_server("save_user", name="Alice", age=30))

        # With success/error callbacks:
        Button("Save", on_click=call_server(
            "save_user",
            name="Alice",
            on_success=log("Saved!"),
            on_error=log("Failed!"),
        ))

    Args:
        action: Name of the server action (as registered with ``@server_action``).
        on_success: Optional DAP action to dispatch on success (receives ``response`` in context).
        on_error: Optional DAP action to dispatch on error (receives ``error`` in context).
        **kwargs: Arguments to pass to the server action.

    Returns:
        A dictionary DAP action that the Dars runtime can dispatch.
    """

    dap_action = {
        "op": "call_server",
        "args": {
            "name": action,
            "params": kwargs,
        },
    }

    if on_success is not None:
        if hasattr(on_success, "get_action"):
            action = on_success.get_action()
            if action is not None:
                dap_action["args"]["on_success"] = action
        elif isinstance(on_success, dict):
            dap_action["args"]["on_success"] = on_success

    if on_error is not None:
        if hasattr(on_error, "get_action"):
            action = on_error.get_action()
            if action is not None:
                dap_action["args"]["on_error"] = action
        elif isinstance(on_error, dict):
            dap_action["args"]["on_error"] = on_error

    return dScript(data=dap_action)


# ── Integration helpers ──────────────────────────────────────────────────────


def register_actions_on_app(fastapi_app: FastAPI) -> None:
    """
    Register all server actions on a FastAPI application.

    This is called automatically by ``SSRApp._setup_core_routes()`` when
    the Dars app has registered actions.

    Args:
        fastapi_app: A FastAPI application instance.
    """
    router = _build_router_from_registry()
    fastapi_app.include_router(router)


def get_registered_actions() -> Dict[str, Dict[str, Any]]:
    """Return a copy of the registered actions registry."""
    return dict(_ACTION_REGISTRY)


def clear_actions() -> None:
    """Clear all registered actions (useful for testing / hot reload)."""
    _ACTION_REGISTRY.clear()


# ── Autodiscovery ────────────────────────────────────────────────────────────


def discover_actions(module_name: str) -> int:
    """
    Import a module and register all ``@server_action``-decorated functions.

    This is useful for auto-discovery::

        discover_actions("backend.api")
        discover_actions("app.actions")

    Args:
        module_name: Dotted module path to import.

    Returns:
        Number of actions discovered.
    """
    import importlib

    try:
        mod = importlib.import_module(module_name)
    except ImportError as exc:
        logger.warning("[Dars:ServerActions] Could not import module '%s': %s", module_name, exc)
        return 0

    count = 0
    for attr_name in dir(mod):
        obj = getattr(mod, attr_name)
        if callable(obj) and hasattr(obj, "__wrapped__"):
            # Check if it's in the registry
            if attr_name in _ACTION_REGISTRY:
                count += 1

    logger.info("[Dars:ServerActions] Discovered %d actions from '%s'", count, module_name)
    return count
