from dars.scripts.dscript import dScript, RawJS
from typing import Any, Union
import json as _json

def stringify(data: Any, pretty: bool = False) -> RawJS:
    """
    JSON.stringify wrapper for use in dScripts.
    
    Args:
        data: Data to stringify (can be RawJS, dict, list, etc.)
        pretty: Pretty-print with indentation
    
    Returns:
        RawJS expression
    """
    # Import locally to avoid circular imports if any
    from dars.backend.data import DataAccessor
    
    if isinstance(data, RawJS):
        if pretty:
            return RawJS(f"JSON.stringify({data.code}, null, 2)")
        return RawJS(f"JSON.stringify({data.code})")
    elif isinstance(data, DataAccessor):
        # Treat DataAccessor as RawJS (it represents window.someId)
        # We use .get() to get the RawJS representation
        raw = data.get()
        if pretty:
            return RawJS(f"JSON.stringify({raw.code}, null, 2)")
        return RawJS(f"JSON.stringify({raw.code})")
    else:
        # Python object - pre-stringify
        json_str = _json.dumps(data, indent=2 if pretty else None)
        return RawJS(f"'{json_str}'")


def parse(json_string: Union[str, RawJS]) -> RawJS:
    """
    JSON.parse wrapper.
    
    Args:
        json_string: JSON string to parse
    
    Returns:
        RawJS expression
    """
    if isinstance(json_string, RawJS):
        return RawJS(f"JSON.parse({json_string.code})")
    return RawJS(f"JSON.parse('{json_string}')")


def get_value(obj: RawJS, path: str, default: Any = None) -> RawJS:
    """
    Safely get a nested value from an object.
    
    Args:
        obj: Object to access (RawJS expression)
        path: Dot-notation path (e.g., "user.profile.name")
        default: Default value if path doesn't exist
    
    Returns:
        RawJS expression
    """
    parts = path.split(".")
    accessor = obj.code
    for part in parts:
        accessor = f"({accessor}?.{part})"
    
    if default is not None:
        default_str = _json.dumps(default) if not isinstance(default, RawJS) else default.code
        return RawJS(f"({accessor} ?? {default_str})")
    
    return RawJS(accessor)
