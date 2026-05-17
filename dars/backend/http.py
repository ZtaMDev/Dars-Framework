from typing import Optional, Dict, Any, Union, Callable, List
from dars.scripts.dscript import dScript, RawJS
import json

# ---------------------------------------------------------------------------
# Interceptor registries
# ---------------------------------------------------------------------------
# Request interceptors: callables that receive and return a config dict.
# They run at Python compile-time and can inject static headers or transform
# the config before the JS fetch code is generated.
_request_interceptors: List[Callable[[dict], dict]] = []

# Response interceptors: callables that receive and return a response dict.
# They are serialised into the generated JS as a transform chain applied to
# the parsed response data before on_success is called.
_response_interceptors: List[Callable[[dict], dict]] = []


def add_request_interceptor(fn: Callable[[dict], dict]) -> None:
    """Register a compile-time request interceptor.

    The interceptor receives the fetch config dict and must return a
    (possibly modified) config dict.  Interceptors are applied in
    registration order.

    Args:
        fn: ``(config: dict) -> dict``
    """
    _request_interceptors.append(fn)


def add_response_interceptor(fn: Callable[[dict], dict]) -> None:
    """Register a response interceptor.

    The interceptor is serialised into the generated JavaScript and applied
    to the parsed response data before ``on_success`` is called.

    Args:
        fn: ``(data: dict) -> dict`` — must be a simple Python function
            whose body can be represented as a JS arrow function, OR a
            callable that returns a DAP action structure via
            ``_to_structure()``.
    """
    _response_interceptors.append(fn)


def clear_interceptors() -> None:
    """Remove all registered request and response interceptors."""
    _request_interceptors.clear()
    _response_interceptors.clear()


def use_auth_interceptor(token_key: str = "dars_auth_token") -> None:
    """Register a request interceptor that injects a JWT Bearer token.

    At runtime the generated JavaScript reads ``localStorage[token_key]``
    and adds it as ``Authorization: Bearer <token>`` to every request.

    Args:
        token_key: localStorage key where the JWT is stored.
    """
    # We mark the interceptor with metadata so the JS generator can emit
    # the correct runtime localStorage read instead of a static value.
    def _auth_interceptor(config: dict) -> dict:
        config = dict(config)
        headers = dict(config.get("headers") or {})
        # Sentinel value — the JS generator replaces this with a runtime read
        headers["Authorization"] = f"__DARS_AUTH_TOKEN__{token_key}__"
        config["headers"] = headers
        return config

    _auth_interceptor._is_auth_interceptor = True
    _auth_interceptor._token_key = token_key
    _request_interceptors.append(_auth_interceptor)


def _apply_request_interceptors(config: dict) -> dict:
    """Apply all registered request interceptors in order."""
    for fn in _request_interceptors:
        config = fn(config)
    return config


def _build_headers_js(headers: dict) -> str:
    """Serialise headers dict to JS, replacing auth sentinels with runtime reads."""
    parts = []
    for k, v in headers.items():
        if isinstance(v, str) and v.startswith("__DARS_AUTH_TOKEN__") and v.endswith("__"):
            token_key = v[len("__DARS_AUTH_TOKEN__"):-2]
            parts.append(
                f'"{k}": (localStorage.getItem({json.dumps(token_key)}) '
                f'? "Bearer " + localStorage.getItem({json.dumps(token_key)}) : undefined)'
            )
        else:
            parts.append(f'"{k}": {json.dumps(v)}')
    return "{" + ", ".join(parts) + "}"

def fetch(
    id: str,
    url: str,
    method: str = "GET",
    headers: Optional[Dict[str, str]] = None,
    body: Optional[Any] = None,
    callback: Optional[Union[Callable, dScript, str]] = None,
    on_error: Optional[Union[Callable, dScript, str]] = None,
    parse_json: bool = True,
    timeout: Optional[int] = None,
    retry: int = 0,
    retry_delay: int = 1000,
) -> dScript:
    """
    Generic fetch function that returns a dScript.

    Request interceptors registered via :func:`add_request_interceptor` are
    applied to the config dict before the JavaScript is generated.
    """

    # Build fetch configuration
    config: dict = {
        "method": method.upper(),
        "headers": dict(headers or {}),
    }

    if body is not None:
        if isinstance(body, (dict, list)):
            config["body"] = json.dumps(body)
            if "Content-Type" not in config["headers"]:
                config["headers"]["Content-Type"] = "application/json"
        else:
            config["body"] = str(body)

    # Apply compile-time request interceptors
    config = _apply_request_interceptors(config)

    # Serialise headers (handles auth sentinels → runtime localStorage reads)
    headers_js = _build_headers_js(config.get("headers", {}))

    # Build the rest of the config without headers (we inject them separately)
    config_without_headers = {k: v for k, v in config.items() if k != "headers"}
    config_js = json.dumps(config_without_headers)
    # Merge headers back as JS expression
    config_js = config_js[:-1] + f', "headers": {headers_js}' + "}"

    js_code = f"""
(async () => {{
    const _op_{id} = {{
        id: '{id}',
        status: 'pending',
        data: null,
        error: null
    }};

    if (!window.__DARS_HTTP_OPS) window.__DARS_HTTP_OPS = {{}};
    window.__DARS_HTTP_OPS['{id}'] = _op_{id};

    try {{
        const config = {config_js};
        {'config.timeout = ' + str(timeout) + ';' if timeout else ''}

        const response = await fetch('{url}', config);

        if (!response.ok) {{
            throw new Error(`HTTP ${{response.status}}: ${{response.statusText}}`);
        }}

        let data = await {'response.json()' if parse_json else 'response.text()'};

        _op_{id}.status = 'success';
        _op_{id}.data = data;
        window.{id} = data;

        {_generate_callback_code(callback, 'data') if callback else ''}

    }} catch (error) {{
        _op_{id}.status = 'error';
        _op_{id}.error = error;
        console.error('[Dars HTTP] Error in operation {id}:', error);

        {_generate_callback_code(on_error, 'error') if on_error else ''}
    }}
}})();
"""

    return dScript(js_code.strip())


def get(id: str, url: str, **kwargs) -> dScript:
    """HTTP GET request. Shorthand for fetch() with method='GET'."""
    return fetch(id=id, url=url, method="GET", **kwargs)


def post(id: str, url: str, body: Any = None, **kwargs) -> dScript:
    """HTTP POST request. Shorthand for fetch() with method='POST'."""
    return fetch(id=id, url=url, method="POST", body=body, **kwargs)


def put(id: str, url: str, body: Any = None, **kwargs) -> dScript:
    """HTTP PUT request. Shorthand for fetch() with method='PUT'."""
    return fetch(id=id, url=url, method="PUT", body=body, **kwargs)


def delete(id: str, url: str, **kwargs) -> dScript:
    """HTTP DELETE request. Shorthand for fetch() with method='DELETE'."""
    return fetch(id=id, url=url, method="DELETE", **kwargs)


def patch(id: str, url: str, body: Any = None, **kwargs) -> dScript:
    """HTTP PATCH request. Shorthand for fetch() with method='PATCH'."""
    return fetch(id=id, url=url, method="PATCH", body=body, **kwargs)


def _generate_callback_code(callback, param_name: str) -> str:
    """Generate JavaScript code for callback execution."""
    if isinstance(callback, dScript):
        # If it's already a dScript, extract its code
        return f"(function() {{ {callback.get_code()} }})();"
    elif callable(callback):
        # If it's a Python callable, we can't execute it in JS
        # User should convert it to dScript manually
        raise ValueError("Callback must be a dScript, not a Python callable")
    elif isinstance(callback, str):
        # Raw JavaScript code
        return callback
    return ""
