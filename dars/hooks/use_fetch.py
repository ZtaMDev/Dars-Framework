# Dars Framework - Core Source File
#
# This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0.
# If a copy of the MPL was not distributed with this file, You can obtain one at
# https://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2025 ZtaDev
"""
useFetch — declarative data-fetching hook.

Returns a 4-tuple of ``(trigger_script, loading_vref, data_vref, error_vref)``
that wires a ``network_request`` DAP action to three VRef selectors so the UI
can react to loading state, response data, and errors without boilerplate.

Example::

    from dars.all import *

    trigger, loading, data, error = useFetch("/api/users")

    Page(
        Show(condition=loading, Spinner()),
        Show(condition=error,   Text(error)),
        Text(data),
        Button("Reload", on_click=trigger),
    )
"""

import uuid
from typing import Any, Optional, Tuple

from dars.scripts.dscript import dScript
from dars.hooks.set_vref import setVRef, VRefValue


def useFetch(
    url: str,
    method: str = "GET",
    body: Optional[Any] = None,
    headers: Optional[dict] = None,
    on_success: Optional[dScript] = None,
    on_error: Optional[dScript] = None,
) -> Tuple[dScript, VRefValue, VRefValue, VRefValue]:
    """
    Declarative data-fetching hook.

    Creates three VRef values (loading, data, error) and a trigger dScript
    that dispatches a ``network_request`` DAP action.  When ``auto_run=True``
    the trigger is embedded in the page's onload sequence automatically.

    Args:
        url: Endpoint to fetch.
        method: HTTP method (default ``"GET"``).
        body: Optional request body (dict auto-serialised to JSON).
        headers: Optional extra request headers.
        on_success: Optional dScript executed after ``data_vref`` is populated.
        on_error: Optional dScript executed after ``error_vref`` is populated.

    Returns:
        ``(trigger_script, loading_vref, data_vref, error_vref)``

        - ``trigger_script`` — :class:`~dars.scripts.dscript.dScript` that
          initiates the fetch (use as ``on_click`` handler or in sequences).
        - ``loading_vref`` — :class:`~dars.hooks.set_vref.VRefValue` that is
          ``True`` while the request is in flight.
        - ``data_vref`` — :class:`~dars.hooks.set_vref.VRefValue` that holds
          the parsed response on success.
        - ``error_vref`` — :class:`~dars.hooks.set_vref.VRefValue` that holds
          the error message on failure.
    """
    uid = uuid.uuid4().hex[:12]

    loading_selector = f".dars-fetch-loading-{uid}"
    data_selector = f".dars-fetch-data-{uid}"
    error_selector = f".dars-fetch-error-{uid}"

    # Create VRef values with sensible initial states
    loading_vref = setVRef(False, loading_selector)
    data_vref = setVRef(None, data_selector)
    error_vref = setVRef(None, error_selector)

    # Build the network_request DAP action
    action: dict = {
        "op": "network_request",
        "args": {
            "url": url,
            "method": method.upper(),
            "loading_selector": loading_selector,
            "data_selector": data_selector,
            "error_selector": error_selector,
        },
    }

    if headers:
        action["args"]["headers"] = headers

    if body is not None:
        action["args"]["body"] = body

    if on_success:
        action["args"]["on_success"] = (
            on_success.get_action() if hasattr(on_success, "get_action") else on_success
        )

    if on_error:
        action["args"]["on_error"] = (
            on_error.get_action() if hasattr(on_error, "get_action") else on_error
        )

    trigger_script = dScript(data=action)


    return trigger_script, loading_vref, data_vref, error_vref


# ---------------------------------------------------------------------------
# Auto-run registry
# ---------------------------------------------------------------------------
# Stores (page_slug, trigger_script) pairs.
# page_slug=None means "register for the current page being built".
# The HTML exporter reads this registry per-page slug.

_AUTO_FETCH_REGISTRY: list = []  # list of (slug_or_none, dScript)
_CURRENT_PAGE_SLUG: str = None   # set by the exporter before calling page functions


def _set_current_page_slug(slug: str) -> None:
    """Called by the exporter to track which page is being built."""
    global _CURRENT_PAGE_SLUG
    _CURRENT_PAGE_SLUG = slug


def _register_auto_fetch(trigger) -> None:
    """Register a fetch trigger to run automatically on page load."""
    _AUTO_FETCH_REGISTRY.append((_CURRENT_PAGE_SLUG, trigger))


def _get_auto_fetch_registry() -> list:
    """Return the current auto-fetch registry."""
    return list(_AUTO_FETCH_REGISTRY)


def _get_auto_fetches_for_page(slug: str) -> list:
    """Return triggers registered for a specific page slug (or None-slug entries)."""
    return [t for (s, t) in _AUTO_FETCH_REGISTRY if s == slug or s is None]


def _clear_auto_fetch_registry() -> None:
    """Clear the registry."""
    _AUTO_FETCH_REGISTRY.clear()
