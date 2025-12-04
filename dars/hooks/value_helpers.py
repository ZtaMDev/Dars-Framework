# Dars Framework - Core Source File
#
# This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0.
# If a copy of the MPL was not distributed with this file, You can obtain one at
# https://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2025 ZtaDev
"""
Pythonic helpers for clean value extraction and manipulation.

These helpers eliminate the need for RawJS by providing a clean,
Pythonic API for DOM value extraction and transformations.
"""

from typing import Optional, Union
from dars.scripts.dscript import dScript, RawJS
import json


class MathExpression:
    """
    Represents a mathematical expression built from ValueRef objects.
    
    This class creates an Abstract Syntax Tree (AST) for mathematical expressions,
    enabling declarative math operations with proper operator precedence.
    
    Example:
        expr = V(".a").float() + V(".b").float() * V(".c").float()
        # Generates: a + (b * c) with correct precedence
    """
    
    def __init__(self, left, operator: str, right):
        """
        Initialize a math expression node.
        
        Args:
            left: Left operand (ValueRef, MathExpression, DynamicOperator, or number)
            operator: Operator string (+, -, *, /, %, **)
            right: Right operand (ValueRef, MathExpression, DynamicOperator, or number)
        """
        self.left = left
        self.operator = operator
        self.right = right
    
    def __add__(self, other):
        """Addition: expr + other"""
        return MathExpression(self, '+', other)
    
    def __radd__(self, other):
        """Reverse addition: other + expr"""
        return MathExpression(other, '+', self)
    
    def __sub__(self, other):
        """Subtraction: expr - other"""
        return MathExpression(self, '-', other)
    
    def __rsub__(self, other):
        """Reverse subtraction: other - expr"""
        return MathExpression(other, '-', self)
    
    def __mul__(self, other):
        """Multiplication: expr * other"""
        return MathExpression(self, '*', other)
    
    def __rmul__(self, other):
        """Reverse multiplication: other * expr"""
        return MathExpression(other, '*', self)
    
    def __truediv__(self, other):
        """Division: expr / other"""
        return MathExpression(self, '/', other)
    
    def __rtruediv__(self, other):
        """Reverse division: other / expr"""
        return MathExpression(other, '/', self)
    
    def __mod__(self, other):
        """Modulo: expr % other"""
        return MathExpression(self, '%', other)
    
    def __rmod__(self, other):
        """Reverse modulo: other % expr"""
        return MathExpression(other, '%', self)
    
    def __pow__(self, other):
        """Power: expr ** other"""
        return MathExpression(self, '**', other)
    
    def __rpow__(self, other):
        """Reverse power: other ** expr"""
        return MathExpression(other, '**', self)
    
    def _get_operand_code(self, operand) -> str:
        """
        Get JavaScript code for an operand.
        
        Args:
            operand: ValueRef, MathExpression, DynamicOperator, or primitive value
            
        Returns:
            JavaScript code string
        """
        if isinstance(operand, (ValueRef, MathExpression, DynamicOperator)):
            return operand._get_code()
        elif isinstance(operand, (int, float)):
            return str(operand)
        else:
            return json.dumps(operand)
    
    def _needs_parens(self, inner_op: str, outer_op: str, position: str) -> bool:
        """
        Determine if parentheses are needed based on operator precedence.
        
        Args:
            inner_op: Operator of the inner expression
            outer_op: Operator of the outer expression
            position: 'left' or 'right' - position of inner expression
            
        Returns:
            True if parentheses are needed
        """
        # Operator precedence (higher number = higher precedence)
        precedence = {'+': 1, '-': 1, '*': 2, '/': 2, '%': 2, '**': 3}
        
        inner_prec = precedence.get(inner_op, 0)
        outer_prec = precedence.get(outer_op, 0)
        
        # Lower precedence needs parens
        if inner_prec < outer_prec:
            return True
        
        # Same precedence: right-associative operators need parens on left
        # For **, a ** b ** c = a ** (b ** c), so left side needs parens
        if inner_prec == outer_prec and position == 'left' and outer_op == '**':
            return True
        
        # For subtraction and division, right side needs parens if same precedence
        # a - (b - c) != a - b - c
        # a / (b / c) != a / b / c
        if inner_prec == outer_prec and position == 'right' and outer_op in ['-', '/']:
            return True
        
        return False
    
    def _get_code(self) -> str:
        """
        Generate JavaScript code from expression tree.
        
        Returns:
            JavaScript code string that evaluates the expression
        """
        # Check if this expression contains a dynamic operator
        has_dynamic_operator = isinstance(self.operator, str) and (
            isinstance(self.left, DynamicOperator) or 
            isinstance(self.right, DynamicOperator)
        )
        
        # Special case: middle operand is a DynamicOperator
        # This happens with: V(".a") + V(".op").operator() + V(".b")
        # We need to detect this pattern
        if isinstance(self.left, MathExpression) and isinstance(self.right, ValueRef):
            # Check if left expression has a DynamicOperator as right operand
            if isinstance(self.left.right, DynamicOperator):
                # Pattern: (num1 + operator()) + num2
                # We need to restructure this as: num1 operator() num2
                num1 = self.left.left
                operator = self.left.right
                num2 = self.right
                
                return self._generate_dynamic_operator_code(num1, operator, num2)
        
        # Generate code that awaits all operands
        left_code = self._get_operand_code(self.left)
        right_code = self._get_operand_code(self.right)
        
        # Check if operands are async (ValueRef or nested MathExpression)
        left_is_async = isinstance(self.left, (ValueRef, MathExpression, DynamicOperator))
        right_is_async = isinstance(self.right, (ValueRef, MathExpression, DynamicOperator))
        
        # If both operands are simple values, return simple expression
        if not left_is_async and not right_is_async:
            return f"{left_code} {self.operator} {right_code}"
        
        # Generate async IIFE that awaits operands
        code_parts = []
        code_parts.append("(async () => {")
        
        # Await left operand if async
        if left_is_async:
            code_parts.append(f"    const left = await ({left_code});")
        else:
            code_parts.append(f"    const left = {left_code};")
        
        # Await right operand if async
        if right_is_async:
            code_parts.append(f"    const right = await ({right_code});")
        else:
            code_parts.append(f"    const right = {right_code};")
        
        # Validate inputs
        code_parts.append("    if (isNaN(left) || isNaN(right)) {")
        code_parts.append("        console.warn('[Dars] Invalid input: one or more values are NaN. Returning 0.');")
        code_parts.append("        return 0;")
        code_parts.append("    }")
        
        # Return the operation
        code_parts.append(f"    const result = left {self.operator} right;")
        
        # Validate result
        code_parts.append("    if (isNaN(result)) {")
        code_parts.append("        console.warn('[Dars] Operation resulted in NaN. Returning 0.');")
        code_parts.append("        return 0;")
        code_parts.append("    }")
        
        code_parts.append("    return result;")
        code_parts.append("})()")
        
        return "\n".join(code_parts)
    
    def _generate_dynamic_operator_code(self, num1, operator, num2) -> str:
        """
        Generate code for dynamic operator evaluation.
        
        Args:
            num1: Left operand (ValueRef or MathExpression)
            operator: DynamicOperator
            num2: Right operand (ValueRef or MathExpression)
        
        Returns:
            JavaScript code that evaluates the dynamic operation
        """
        num1_code = self._get_operand_code(num1)
        operator_code = operator._get_code()
        num2_code = self._get_operand_code(num2)
        
        return f"""(async () => {{
    const n1 = await ({num1_code});
    const op = await ({operator_code});
    const n2 = await ({num2_code});
    
    // Validate inputs
    if (isNaN(n1) || isNaN(n2)) {{
        console.warn('[Dars] Invalid input: one or more values are NaN. Returning 0.');
        return 0;
    }}
    
    // Evaluate based on operator
    let result;
    switch(op) {{
        case '+': result = n1 + n2; break;
        case '-': result = n1 - n2; break;
        case '*': result = n1 * n2; break;
        case '/': result = n2 !== 0 ? n1 / n2 : 0; break;
        case '%': result = n1 % n2; break;
        case '**': result = n1 ** n2; break;
        default: result = n1 + n2; break;
    }}
    
    // Validate result
    if (isNaN(result)) {{
        console.warn('[Dars] Operation resulted in NaN. Returning 0.');
        return 0;
    }}
    
    return result;
}})()"""
    
    def get_code(self) -> str:
        """Public method for dScript compatibility"""
        return self._get_code()
    
    def __repr__(self):
        return f"MathExpression({self.left} {self.operator} {self.right})"


class DynamicOperator:
    """
    Represents a dynamic operator from a Select or Input element.
    
    The value will be validated as a valid operator (+, -, *, /, %, **).
    
    Example:
        # Select with operator options
        Select(class_name="operation", options=["+", "-", "*", "/"])
        
        # Use in expression
        result = V(".num1").float() + V(".operation").operator() + V(".num2").float()
    """
    
    VALID_OPERATORS = ['+', '-', '*', '/', '%', '**']
    
    def __init__(self, value_ref: 'ValueRef'):
        """
        Initialize a dynamic operator.
        
        Args:
            value_ref: ValueRef pointing to the element containing the operator
        """
        self.value_ref = value_ref
    
    def _get_code(self) -> str:
        """
        Generate JavaScript with operator validation.
        
        Returns:
            JavaScript code that validates and returns the operator
        """
        selector_code = self.value_ref._get_code()
        
        # Generate JS that validates the operator
        return f"""(async () => {{
    const op = await {selector_code};
    const validOps = {json.dumps(self.VALID_OPERATORS)};
    if (!validOps.includes(op)) {{
        console.error('[Dars] Invalid operator:', op, '- defaulting to +');
        return '+';
    }}
    return op;
}})()"""
    
    def get_code(self) -> str:
        """Public method for dScript compatibility"""
        return self._get_code()
    
    def __repr__(self):
        return f"DynamicOperator({self.value_ref})"



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
            # State path: extract from state registry via window.Dars.getState
            parts = self.selector.split('.')
            state_id = parts[0]
            prop_name = parts[1]
            
            js_code = f"""
(async () => {{
    try {{
        // Get value directly from state registry
        let value = '';
        if (window.Dars && window.Dars.getState) {{
            const st = window.Dars.getState('{state_id}');
            if (st && st.values && st.values['{prop_name}'] !== undefined) {{
                value = st.values['{prop_name}'];
            }}
        }}
        
        // Fallback to DOM if state not found (legacy support)
        if (value === '') {{
            const el = document.querySelector('[data-dynamic="{self.selector}"]');
            if (el) value = el.textContent || '';
        }}
        
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
    
    def operator(self) -> 'DynamicOperator':
        """
        Mark this ValueRef as a dynamic operator.
        The value will be validated as a valid operator (+, -, *, /, %, **).
        
        Example:
            # Select with operator options
            Select(class_name="operation", options=["+", "-", "*", "/"])
            
            # Use in expression
            result = V(".num1").float() + V(".operation").operator() + V(".num2").float()
        
        Returns:
            DynamicOperator instance
        """
        return DynamicOperator(self)
    
    def _has_numeric_transform(self) -> bool:
        """Check if this ValueRef has a numeric transformation (.int() or .float())"""
        if self._transform is None:
            return False
        # Check if transform contains parseInt or parseFloat
        test_result = self._transform("x")
        return "parseInt" in test_result or "parseFloat" in test_result
    
    # Arithmetic operators - Return MathExpression for composability
    def __add__(self, other) -> 'MathExpression':
        """Addition/Concatenation: val + other"""
        return MathExpression(self, '+', other)
    
    def __radd__(self, other) -> 'MathExpression':
        """Reverse Addition: other + val"""
        return MathExpression(other, '+', self)
    
    def __mul__(self, other) -> 'MathExpression':
        """Multiplication: val * other (requires .int() or .float())"""
        if not self._has_numeric_transform():
            raise TypeError(
                f"Multiplication requires numeric transformation. "
                f"Use V('{self.selector}').int() or V('{self.selector}').float() before multiplying."
            )
        return MathExpression(self, '*', other)
    
    def __rmul__(self, other) -> 'MathExpression':
        """Reverse Multiplication: other * val (requires .int() or .float())"""
        if not self._has_numeric_transform():
            raise TypeError(
                f"Multiplication requires numeric transformation. "
                f"Use V('{self.selector}').int() or V('{self.selector}').float() before multiplying."
            )
        return MathExpression(other, '*', self)
    
    def __truediv__(self, other) -> 'MathExpression':
        """Division: val / other (requires .int() or .float())"""
        if not self._has_numeric_transform():
            raise TypeError(
                f"Division requires numeric transformation. "
                f"Use V('{self.selector}').int() or V('{self.selector}').float() before dividing."
            )
        return MathExpression(self, '/', other)
    
    def __rtruediv__(self, other) -> 'MathExpression':
        """Reverse Division: other / val (requires .int() or .float())"""
        if not self._has_numeric_transform():
            raise TypeError(
                f"Division requires numeric transformation. "
                f"Use V('{self.selector}').int() or V('{self.selector}').float() before dividing."
            )
        return MathExpression(other, '/', self)
    
    def __sub__(self, other) -> 'MathExpression':
        """Subtraction: val - other (requires .int() or .float())"""
        if not self._has_numeric_transform():
            raise TypeError(
                f"Subtraction requires numeric transformation. "
                f"Use V('{self.selector}').int() or V('{self.selector}').float() before subtracting."
            )
        return MathExpression(self, '-', other)
    
    def __rsub__(self, other) -> 'MathExpression':
        """Reverse Subtraction: other - val (requires .int() or .float())"""
        if not self._has_numeric_transform():
            raise TypeError(
                f"Subtraction requires numeric transformation. "
                f"Use V('{self.selector}').int() or V('{self.selector}').float() before subtracting."
            )
        return MathExpression(other, '-', self)
    
    def __mod__(self, other) -> 'MathExpression':
        """Modulo: val % other (requires .int() or .float())"""
        if not self._has_numeric_transform():
            raise TypeError(
                f"Modulo requires numeric transformation. "
                f"Use V('{self.selector}').int() or V('{self.selector}').float() before using modulo."
            )
        return MathExpression(self, '%', other)
    
    def __rmod__(self, other) -> 'MathExpression':
        """Reverse Modulo: other % val (requires .int() or .float())"""
        if not self._has_numeric_transform():
            raise TypeError(
                f"Modulo requires numeric transformation. "
                f"Use V('{self.selector}').int() or V('{self.selector}').float() before using modulo."
            )
        return MathExpression(other, '%', self)
    
    def __pow__(self, other) -> 'MathExpression':
        """Power: val ** other (requires .int() or .float())"""
        if not self._has_numeric_transform():
            raise TypeError(
                f"Power requires numeric transformation. "
                f"Use V('{self.selector}').int() or V('{self.selector}').float() before using power."
            )
        return MathExpression(self, '**', other)
    
    def __rpow__(self, other) -> 'MathExpression':
        """Reverse Power: other ** val (requires .int() or .float())"""
        if not self._has_numeric_transform():
            raise TypeError(
                f"Power requires numeric transformation. "
                f"Use V('{self.selector}').int() or V('{self.selector}').float() before using power."
            )
        return MathExpression(other, '**', self)
    
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
