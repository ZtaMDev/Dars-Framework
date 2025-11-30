"""
Pythonic helpers for clean value extraction and manipulation.

These helpers eliminate the need for RawJS by providing a clean,
Pythonic API for DOM value extraction and transformations.
"""

from typing import Optional, Union
from dars.scripts.dscript import dScript, RawJS
import json


class ValueRef:
    """
    Pythonic wrapper for DOM value extraction with transformations.
    
    Enables clean operations without RawJS:
        val = V(".username")  # Short alias
        url = f"/api/users/{val}"  # Clean string interpolation
        upper = val.upper()  # String transformations
        combined = val + " " + V(".lastname")  # Concatenation
    
    This class is designed to be used with the V() short alias.
    """
    
    def __init__(self, selector: str):
        """
        Initialize a ValueRef.
        
        Args:
            selector: CSS selector for the target element
        """
        self.selector = selector
        self._transform = None  # Optional transformation function
        self._custom_code = None  # For complex operations like concatenation chains
    
    def _get_code(self) -> str:
        """
        Generate JavaScript code to get the value.
        
        Returns:
            JavaScript code string that returns a Promise
        """
        # If there's custom code (from concatenation), use it
        if self._custom_code:
            return self._custom_code
        
        # Generate a simple async IIFE that returns the value
        # The caller is responsible for awaiting this
        js_code = f"""
(async () => {{
    try {{
        const el = document.querySelector('{self.selector}');
        if (!el) {{
            console.warn('ValueRef: Element not found for selector: {self.selector}');
            return '';
        }}
        
        // Get the value
        let value;
        if (el.tagName === 'INPUT' || el.tagName === 'TEXTAREA') {{
            value = el.value || '';
        }} else if (el.tagName === 'SELECT') {{
            value = el.value || '';
        }} else if (el.type === 'checkbox') {{
            value = el.checked;
        }} else {{
            value = el.textContent || '';
        }}
        
        // Apply transformation if any
        {f'return {self._transform("value")};' if self._transform else 'return value;'}
    }} catch (e) {{
        console.error('ValueRef error:', e);
        return '';
    }}
}})()
        """.strip()
        
        return js_code
    
    # String operations
    def upper(self) -> 'ValueRef':
        """Convert to uppercase"""
        new_ref = ValueRef(self.selector)
        new_ref._transform = lambda x: f"String({x}).toUpperCase()"
        return new_ref
    
    def lower(self) -> 'ValueRef':
        """Convert to lowercase"""
        new_ref = ValueRef(self.selector)
        new_ref._transform = lambda x: f"String({x}).toLowerCase()"
        return new_ref
    
    def trim(self) -> 'ValueRef':
        """Trim whitespace"""
        new_ref = ValueRef(self.selector)
        new_ref._transform = lambda x: f"String({x}).trim()"
        return new_ref
    
    def strip(self) -> 'ValueRef':
        """Alias for trim() (Pythonic name)"""
        return self.trim()
    
    # Numeric operations
    def int(self) -> 'ValueRef':
        """Convert to integer"""
        new_ref = ValueRef(self.selector)
        new_ref._transform = lambda x: f"parseInt({x}, 10)"
        return new_ref
    
    def float(self) -> 'ValueRef':
        """Convert to float"""
        new_ref = ValueRef(self.selector)
        new_ref._transform = lambda x: f"parseFloat({x})"
        return new_ref
    
    # Operators
    def __add__(self, other) -> 'ValueRef':
        """
        Concatenation or Addition: val + other
        
        Args:
            other: String, Number, or ValueRef to add/concatenate
        
        Returns:
            New ValueRef with operation applied
        """
        new_ref = ValueRef(self.selector)
        
        # Get the code for self (which may already have transformations)
        self_code = self._get_code()
        
        if isinstance(other, ValueRef):
            # Both are ValueRefs - need to await both and add
            other_code = other._get_code()
            # Create a new async IIFE that awaits both and adds
            new_ref._transform = None  # Clear transform, we'll override _get_code
            new_ref._custom_code = f"""
(async () => {{
    try {{
        const left = await {self_code};
        const right = await {other_code};
        return left + right;
    }} catch (e) {{
        console.error('ValueRef op error:', e);
        return '';
    }}
}})()
            """.strip()
        else:
            # Other is a literal (string/number)
            # Create a new async IIFE that awaits self and adds the literal
            new_ref._transform = None  # Clear transform
            new_ref._custom_code = f"""
(async () => {{
    try {{
        const left = await {self_code};
        return left + {json.dumps(other)};
    }} catch (e) {{
        console.error('ValueRef op error:', e);
        return '';
    }}
}})()
            """.strip()
        return new_ref
    
    def __radd__(self, other) -> 'ValueRef':
        """
        Reverse Concatenation/Addition: other + val
        
        Args:
            other: String or Number to prepend/add
        
        Returns:
            New ValueRef with operation applied
        """
        new_ref = ValueRef(self.selector)
        self_code = self._get_code()
        
        # Create a new async IIFE that awaits self and adds the literal
        new_ref._transform = None
        new_ref._custom_code = f"""
(async () => {{
    try {{
        const right = await {self_code};
        return {json.dumps(other)} + right;
    }} catch (e) {{
        console.error('ValueRef op error:', e);
        return '';
    }}
}})()
        """.strip()
        return new_ref
    
    def __str__(self):
        """String representation for f-strings"""
        # For f-strings, we return the code wrapped in ${} so it works in template literals
        # But we need to be careful not to double-wrap in url()
        return f"${{await {self._get_code()}}}"
    
    def __format__(self, format_spec):
        """Support for f-string formatting"""
        return f"${{await {self._get_code()}}}"
    
    def __repr__(self):
        return f"ValueRef('{self.selector}')"
    
    def to_dscript(self) -> dScript:
        """
        Convert this ValueRef to a dScript.
        
        This is called automatically when ValueRef is used in event handlers
        or other contexts that expect dScript.
        
        Returns:
            dScript that extracts and transforms the value
        """
        return dScript(self._get_code())


def V(selector: str) -> ValueRef:
    """
    Short alias for ValueRef - creates a reference to a DOM element's value.
    
    Args:
        selector: CSS selector for the target element
    
    Returns:
        ValueRef instance
    
    Example:
        # Basic usage
        username = V(".username-input")
        
        # With transformations
        upper_name = V(".name").upper()
        
        # Concatenation
        full_name = V(".first") + " " + V(".last")
        
        # In state updates
        userState.name.set(V(".input"))
    """
    return ValueRef(selector)


def url(template: str, **kwargs) -> str:
    """
    Build dynamic URLs with clean syntax.
    
    Replaces placeholders in the template with ValueRef or string values,
    generating a JavaScript template literal.
    
    Args:
        template: URL template with {placeholders}
        **kwargs: ValueRef or string values for placeholders
    
    Returns:
        Template literal string for use in backend API
    
    Example:
        # With ValueRef
        url("/api/users/{username}", username=V(".username-input"))
        # Generates: `/api/users/${(await ...)}`
        
        # With string
        url("/api/users/{id}", id="123")
        # Generates: `/api/users/123`
        
        # Mixed
        url("/api/{resource}/{id}", resource="users", id=V(".user-id"))
    """
    result = template
    for key, value in kwargs.items():
        placeholder = f"{{{key}}}"
        if isinstance(value, ValueRef):
            # ValueRef.__str__ returns ${await ...}, which is exactly what we want inside a backticked string
            result = result.replace(placeholder, str(value))
        else:
            # Use the string value directly
            result = result.replace(placeholder, str(value))
    
    # If the user provided a template like "${base}/...", we need to make sure we don't double-escape
    # But wait, the user provides "/api/users/{username}", so we replace {username} with ${await ...}
    # The result is "/api/users/${await ...}"
    # Wrapping this in backticks gives `/api/users/${await ...}` which is valid JS.
    
    return RawJS(f"`{result}`")


def transform(selector: str, fn: str) -> dScript:
    """
    Apply a custom JavaScript transformation to a DOM value.
    
    For cases where built-in transformations (upper, lower, etc.) are not enough,
    this allows you to write custom JavaScript transformations.
    
    Args:
        selector: CSS selector for the target element
        fn: JavaScript expression using 'value' as the variable name
    
    Returns:
        dScript that extracts and transforms the value
    
    Example:
        # Remove non-alphabetic characters
        transform(".input", "value.replace(/[^a-zA-Z]/g, '')")
        
        # Complex transformation
        transform(".email", "value.toLowerCase().trim().replace(/\\s+/g, '')")
        
        # With state update
        userState.processed.set(
            transform(".input", "value.toUpperCase().slice(0, 10)")
        )
    """
    # Generate JS extraction code directly
    js_extraction = f"""
(async () => {{
    try {{
        const el = document.querySelector('{selector}');
        if (!el) {{
            console.warn('transform: Element not found for selector: {selector}');
            return '';
        }}
        
        // Handle different element types
        let value;
        if (el.tagName === 'INPUT' || el.tagName === 'TEXTAREA') {{
            value = el.value || '';
        }} else if (el.tagName === 'SELECT') {{
            value = el.value || '';
        }} else if (el.type === 'checkbox') {{
            value = el.checked;
        }} else {{
            value = el.textContent || '';
        }}
        
        // Apply transformation
        return {fn};
    }} catch (e) {{
        console.error('transform error:', e);
        return '';
    }}
}})()
    """
    return dScript(js_extraction.strip())
