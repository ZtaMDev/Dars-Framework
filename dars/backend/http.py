from typing import Optional, Dict, Any, Union, Callable
from dars.scripts.dscript import dScript, RawJS
import json

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
    
    Args:
        id: Operation ID (NOT HTML ID) - names the variable storing the result
        url: The URL to fetch from
        method: HTTP method (GET, POST, PUT, DELETE, etc.)
        headers: HTTP headers dict
        body: Request body (auto-stringified if dict/list)
        callback: Function/dScript to process successful response
        on_error: Function/dScript to handle errors
        parse_json: Auto-parse JSON responses (default: True)
        timeout: Request timeout in milliseconds
        retry: Number of retry attempts
        retry_delay: Delay between retries in milliseconds
    
    Returns:
        dScript that performs the fetch operation
    """
    
    # Build fetch configuration
    config = {
        "method": method.upper(),
        "headers": headers or {},
    }
    
    if body is not None:
        if isinstance(body, (dict, list)):
            config["body"] = json.dumps(body)
            # Only set Content-Type if not already set
            if "Content-Type" not in config["headers"]:
                config["headers"]["Content-Type"] = "application/json"
        else:
            config["body"] = str(body)
    
    # Build JavaScript code
    js_code = f"""
(async () => {{
    const _op_{id} = {{
        id: '{id}',
        status: 'pending',
        data: null,
        error: null
    }};
    
    // Store operation globally
    if (!window.__DARS_HTTP_OPS) window.__DARS_HTTP_OPS = {{}};
    window.__DARS_HTTP_OPS['{id}'] = _op_{id};
    
    try {{
        const config = {json.dumps(config)};
        {'config.timeout = ' + str(timeout) + ';' if timeout else ''}
        
        const response = await fetch('{url}', config);
        
        if (!response.ok) {{
            throw new Error(`HTTP ${{response.status}}: ${{response.statusText}}`);
        }}
        
        let data = await {'response.json()' if parse_json else 'response.text()'};
        
        // Store result
        _op_{id}.status = 'success';
        _op_{id}.data = data;
        window.{id} = data;  // Also make directly accessible
        
        // Execute callback if provided
        {_generate_callback_code(callback, 'data') if callback else ''}
        
    }} catch (error) {{
        _op_{id}.status = 'error';
        _op_{id}.error = error;
        console.error('[Dars HTTP] Error in operation {id}:', error);
        
        // Execute error handler if provided
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
