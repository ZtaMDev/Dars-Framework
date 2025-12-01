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
            selector: CSS selector OR state path (e.g., ".class", "#id", "cart.total")
        """
        self.selector = selector
        self._transform = None  # Optional transformation function
        self._custom_code = None  # For complex operations like concatenation chains
    
    def _is_state_path(self) -> bool:
        """
        Check if selector is a state path (e.g., "cart.total") vs CSS selector.
        
        State paths:
        - Don't start with . or # or [
        - Contain exactly one dot
        - Match pattern: word.word
        
        Returns:
            True if selector is a state path, False if CSS selector
        """
        # CSS selectors start with special characters
        if self.selector.startswith(('.', '#', '[')):
            return False
        
        # State paths have format: stateName.property
        parts = self.selector.split('.')
        if len(parts) == 2 and parts[0] and parts[1]:
            # Both parts should be valid identifiers (alphanumeric + underscore)
            return parts[0].replace('_', '').isalnum() and parts[1].replace('_', '').isalnum()
        
        return False
    
    def _get_code(self) -> str:
        """
        Generate JavaScript code to get the value.
        
        Returns:
            JavaScript code string that returns a Promise
        """
        # If there's custom code (from concatenation), use it
        if self._custom_code:
            return self._custom_code
        
        # Check if this is a state path or CSS selector
        if self._is_state_path():
            # State path: extract from reactive element created by useDynamic
            # useDynamic creates elements with data-dynamic="stateName.property"
            js_code = f"""
(async () => {{
    try {{
        // Get value from reactive element (created by useDynamic)
        const el = document.querySelector('[data-dynamic="{self.selector}"]');
        if (!el) {{
            console.warn('ValueRef: No reactive element found for state path: {self.selector}');
            return '';
        }}
        
        // Get the text content (which is the current state value)
        let value = el.textContent || '';
        
        // Apply transformation if any
        {f'return {self._transform("value")};' if self._transform else 'return value;'}
    }} catch (e) {{
        console.error('ValueRef state error:', e);
        return '';
    }}
}})()
            """.strip()
        else:
            # CSS selector: extract from DOM element
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
    
    def _has_numeric_transform(self) -> bool:
        """Check if this ValueRef has a numeric transformation (.int() or .float())"""
        if self._transform is None:
            return False
        # Check if transform contains parseInt or parseFloat
        test_result = self._transform("x")
        return "parseInt" in test_result or "parseFloat" in test_result
    
    # Arithmetic operators
    def __add__(self, other) -> 'ValueRef':
        """Addition/Concatenation: val + other (always allowed)"""
        return self._binary_op(other, '+', '')
    
    def __radd__(self, other) -> 'ValueRef':
        """Reverse Addition: other + val (always allowed)"""
        return self._rbinary_op(other, '+', '')
    
    def __mul__(self, other) -> 'ValueRef':
        """Multiplication: val * other (requires .int() or .float())"""
        if not self._has_numeric_transform():
            raise TypeError(
                f"Multiplication requires numeric transformation. "
                f"Use V('{self.selector}').int() or V('{self.selector}').float() before multiplying."
            )
        return self._binary_op(other, '*', 0)
    
    def __rmul__(self, other) -> 'ValueRef':
        """Reverse Multiplication: other * val (requires .int() or .float())"""
        if not self._has_numeric_transform():
            raise TypeError(
                f"Multiplication requires numeric transformation. "
                f"Use V('{self.selector}').int() or V('{self.selector}').float() before multiplying."
            )
        return self._rbinary_op(other, '*', 0)
    
    def __truediv__(self, other) -> 'ValueRef':
        """Division: val / other (requires .int() or .float())"""
        if not self._has_numeric_transform():
            raise TypeError(
                f"Division requires numeric transformation. "
                f"Use V('{self.selector}').int() or V('{self.selector}').float() before dividing."
            )
        return self._binary_op(other, '/', 0)
    
    def __rtruediv__(self, other) -> 'ValueRef':
        """Reverse Division: other / val (requires .int() or .float())"""
        if not self._has_numeric_transform():
            raise TypeError(
                f"Division requires numeric transformation. "
                f"Use V('{self.selector}').int() or V('{self.selector}').float() before dividing."
            )
        return self._rbinary_op(other, '/', 0)
    
    def __sub__(self, other) -> 'ValueRef':
        """Subtraction: val - other (requires .int() or .float())"""
        if not self._has_numeric_transform():
            raise TypeError(
                f"Subtraction requires numeric transformation. "
                f"Use V('{self.selector}').int() or V('{self.selector}').float() before subtracting."
            )
        return self._binary_op(other, '-', 0)
    
    def __rsub__(self, other) -> 'ValueRef':
        """Reverse Subtraction: other - val (requires .int() or .float())"""
        if not self._has_numeric_transform():
            raise TypeError(
                f"Subtraction requires numeric transformation. "
                f"Use V('{self.selector}').int() or V('{self.selector}').float() before subtracting."
            )
        return self._rbinary_op(other, '-', 0)
    
    def __mod__(self, other) -> 'ValueRef':
        """Modulo: val % other (requires .int() or .float())"""
        if not self._has_numeric_transform():
            raise TypeError(
                f"Modulo requires numeric transformation. "
                f"Use V('{self.selector}').int() or V('{self.selector}').float() before using modulo."
            )
        return self._binary_op(other, '%', 0)
    
    def __rmod__(self, other) -> 'ValueRef':
        """Reverse Modulo: other % val (requires .int() or .float())"""
        if not self._has_numeric_transform():
            raise TypeError(
                f"Modulo requires numeric transformation. "
                f"Use V('{self.selector}').int() or V('{self.selector}').float() before using modulo."
            )
        return self._rbinary_op(other, '%', 0)
    
    def __pow__(self, other) -> 'ValueRef':
        """Power: val ** other (requires .int() or .float())"""
        if not self._has_numeric_transform():
            raise TypeError(
                f"Power requires numeric transformation. "
                f"Use V('{self.selector}').int() or V('{self.selector}').float() before using power."
            )
        return self._binary_op(other, '**', 0)
    
    def __rpow__(self, other) -> 'ValueRef':
        """Reverse Power: other ** val (requires .int() or .float())"""
        if not self._has_numeric_transform():
            raise TypeError(
                f"Power requires numeric transformation. "
                f"Use V('{self.selector}').int() or V('{self.selector}').float() before using power."
            )
        return self._rbinary_op(other, '**', 0)
    
    def _binary_op(self, other, operator: str, error_return) -> 'ValueRef':
        """Helper for binary operations: self op other"""
        new_ref = ValueRef(self.selector)
        self_code = self._get_code()
        
        if isinstance(other, ValueRef):
            other_code = other._get_code()
            new_ref._transform = None
            new_ref._custom_code = f"""
(async () => {{
    try {{
        const left = await {self_code};
        const right = await {other_code};
        return left {operator} right;
    }} catch (e) {{
        console.error('ValueRef op error:', e);
        return {json.dumps(error_return)};
    }}
}})()
            """.strip()
        else:
            new_ref._transform = None
            new_ref._custom_code = f"""
(async () => {{
    try {{
        const left = await {self_code};
        return left {operator} {json.dumps(other)};
    }} catch (e) {{
        console.error('ValueRef op error:', e);
        return {json.dumps(error_return)};
    }}
}})()
            """.strip()
        return new_ref
    
    def _rbinary_op(self, other, operator: str, error_return) -> 'ValueRef':
        """Helper for reverse binary operations: other op self"""
        new_ref = ValueRef(self.selector)
        self_code = self._get_code()
        new_ref._transform = None
        new_ref._custom_code = f"""
(async () => {{
    try {{
        const right = await {self_code};
        return {json.dumps(other)} {operator} right;
    }} catch (e) {{
        console.error('ValueRef op error:', e);
        return {json.dumps(error_return)};
    }}
}})()
        """.strip()
        return new_ref
    
    def __str__(self):
        """String representation for f-strings"""
        return f"${{await {self._get_code()}}}"
    
    def __format__(self, format_spec):
        """Support for f-string formatting"""
        return f"${{await {self._get_code()}}}"
    
    def __repr__(self):
        return f"ValueRef('{self.selector}')"
    
    def to_dscript(self) -> dScript:
        """Convert this ValueRef to a dScript"""
        return dScript(self._get_code())


def V(selector: str) -> ValueRef:
    """
    Short alias for ValueRef - creates a reference to a value (DOM element or state).
    
    Args:
        selector: CSS selector OR state path
            - CSS selector: ".class", "#id", "[attr]", etc.
            - State path: "stateName.property" (e.g., "cart.total", "user.name")
    
    Returns:
        ValueRef instance
    
    Example:
        # CSS selectors (DOM elements)
        username = V(".username-input")
        email = V("#email-field")
        
        # State paths (reactive state)
        cartTotal = V("cart.total")
        userName = V("user.name")
        
        # String concatenation (always works)
        full_name = V(".first") + " " + V(".last")
        message = "Total: $" + V("cart.total")
        
        # Math operations (requires .int() or .float())
        result = V(".qty").int() * V("product.price").float()
        discount = V(".price").float() * 0.9
        total = V("cart.total").float() + 10
        
        # In state updates
        userState.name.set(V(".input"))
        cartState.total.set(V("cart.total").float() + 10)
    """
    return ValueRef(selector)


def url(template: str, **kwargs) -> str:
    """Build dynamic URLs with clean syntax"""
    result = template
    for key, value in kwargs.items():
        placeholder = f"{{{key}}}"
        if isinstance(value, ValueRef):
            result = result.replace(placeholder, str(value))
        else:
            result = result.replace(placeholder, str(value))
    return RawJS(f"`{result}`")


def transform(selector: str, fn: str) -> dScript:
    """Apply a custom JavaScript transformation to a DOM value"""
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
