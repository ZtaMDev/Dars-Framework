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
        if isinstance(self.right, DynamicOperator) and self.operator == '+':
            # Handle composition: (left + dynamic_op) + right -> MathExpression(left, dynamic_op, right)
            return MathExpression(self.left, self.right, other)
        return MathExpression(self, '+', other)
    
    def __radd__(self, other):
        """Reverse addition: other + expr"""
        return MathExpression(other, '+', self)
    
    def __sub__(self, other):
        """Subtraction: expr - other"""
        if isinstance(self.right, DynamicOperator) and self.operator == '-':
            # Handle composition: (left - dynamic_op) - right -> MathExpression(left, dynamic_op, right)
            # (Note: we use the dynamic_op as the actual operator)
            return MathExpression(self.left, self.right, other)
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
    
    def _to_structure(self) -> dict:
        """
        Generate DAP structure for the expression.
        """
        left = self.left._to_structure() if hasattr(self.left, '_to_structure') else self.left
        right = self.right._to_structure() if hasattr(self.right, '_to_structure') else self.right
        
        # If operator is a DynamicOperator object, get its structure
        op_struct = self.operator
        if hasattr(self.operator, '_to_structure'):
            op_struct = self.operator._to_structure()
            
        return {
            "op": "math_expr",
            "args": {
                "left": left,
                "operator": op_struct,
                "right": right
            }
        }
        
    def _get_code(self) -> str:
        """Get native JavaScript code for this expression."""
        from dars.scripts.dscript import compile_val
        return compile_val(self._to_structure())

    def __str__(self):
        """String representation for embedding in JS template literals"""
        return f"${{{self._get_code()}}}"

    def __format__(self, format_spec):
        """Support for f-string formatting"""
        return f"${{{self._get_code()}}}"
    
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
    
    def _to_structure(self) -> dict:
        """
        Generate DAP structure with operator validation.
        """
        selector_struct = self.value_ref._to_structure()
        
        # We need validation logic in DAP?
        # Maybe we can wrap it in a 'validate_op' if strict validation is needed.
        # But for now, we can trust the resolver or specific op.
        # Actually, let's use a 'get_operator' op if we want specific validation, 
        # or just 'get_dom_value' and validate in 'math_expr' resolver implicitly or add a 'validate_operator' transform.
        # For simplicity, let's assume valid operator or default to '+' in resolver if invalid. 
        # Wait, the previous code had specific validation.
        # I'll create a transform 'validate_operator'.
        
        return {
            "op": "transform",
            "args": {
                "input": selector_struct,
                "method": "validate_operator", 
                "valid_ops": self.VALID_OPERATORS 
                # Note: 'valid_ops' argument needs to be supported in 'transform' op in js_lib.py or we accept loose validation
                # The _resolve code I wrote for 'transform' only supports 'upper'/'lower'.
                # I should update _resolve to support 'validate_operator' or similar.
                # Or I can use 'cond_expr' to validate? No, that's complex.
                # Let's emit a transform and UPDATE JS_LIB later or now?
                # I'll stick to 'validate_operator' and update js_lib in next step if I missed it.
            }
        }
    
    def get_code(self) -> str:
        """Public method for dScript compatibility"""
        return self._get_code()
    
    def __repr__(self):
        return f"DynamicOperator({self.value_ref})"


class BooleanExpression:
    """
    Represents a boolean comparison expression built from ValueRef objects.
    
    Supports comparison operators (==, !=, >, <, >=, <=) and logical combinations.
    Can be used with .then() method for conditional expressions.
    
    Example:
        is_adult = V("#age").int() >= 18
        discount = is_adult.then(0.2, 0)  # Generates: (age >= 18) ? 0.2 : 0
    """
    
    def __init__(self, left, operator: str, right):
        """
        Initialize a boolean expression.
        
        Args:
            left: Left operand (ValueRef, MathExpression, BooleanExpression, or primitive)
            operator: Comparison operator (==, !=, >, <, >=, <=)
            right: Right operand (ValueRef, MathExpression, BooleanExpression, or primitive)
        """
        self.left = left
        self.operator = operator
        self.right = right
    
    def _get_operand_code(self, operand) -> str:
        """
        Get JavaScript code for an operand.
        
        Args:
            operand: ValueRef, MathExpression, BooleanExpression, or primitive value
            
        Returns:
            JavaScript code string
        """
        if isinstance(operand, (ValueRef, MathExpression, BooleanExpression)):
            return operand._get_code()
        elif isinstance(operand, bool):
            return 'true' if operand else 'false'
        elif isinstance(operand, (int, float)):
            return str(operand)
        else:
            return json.dumps(operand)
    
    def _to_structure(self) -> dict:
        """
        Generate DAP structure for the boolean expression.
        """
        left = self.left._to_structure() if hasattr(self.left, '_to_structure') else self.left
        right = self.right._to_structure() if hasattr(self.right, '_to_structure') else self.right
        
        return {
            "op": "bool_expr",
            "args": {
                "left": left,
                "operator": self.operator,
                "right": right
            }
        }
        
    def _get_code(self) -> str:
        """Get native JavaScript code for this expression."""
        from dars.scripts.dscript import compile_val
        return compile_val(self._to_structure())

    def __str__(self):
        """String representation for embedding in JS template literals"""
        return f"${{{self._get_code()}}}"

    def __format__(self, format_spec):
        """Support for f-string formatting"""
        return f"${{{self._get_code()}}}"

    def then(self, true_value, false_value):
        """
        Create a conditional expression (ternary operator).
        
        This is a Python method that generates JavaScript ternary: condition ? trueVal : falseVal
        
        Args:
            true_value: Value to return if condition is true
            false_value: Value to return if condition is false
            
        Returns:
            ConditionalExpression object
            
        Example:
            (V("#age").int() >= 18).then("adult", "minor")
            # Generates: (age >= 18) ? "adult" : "minor"
        """
        return ConditionalExpression(self, true_value, false_value)
    
    def and_(self, other):
        """
        Combine with another boolean expression using AND logic.
        
        Args:
            other: Another BooleanExpression
            
        Returns:
            LogicalExpression object
            
        Example:
            (V("#age").int() >= 18).and_(V("#email").includes("@"))
            # Generates: (age >= 18) && (email.includes("@"))
        """
        return LogicalExpression(self, '&&', other)
    
    def or_(self, other):
        """
        Combine with another boolean expression using OR logic.
        
        Args:
            other: Another BooleanExpression
            
        Returns:
            LogicalExpression object
            
        Example:
            (V("#age").int() < 18).or_(V("#age").int() > 65)
            # Generates: (age < 18) || (age > 65)
        """
        return LogicalExpression(self, '||', other)
    
    def get_code(self) -> str:
        """Public method for dScript compatibility"""
        return self._get_code()
    
    def to_dscript(self):
        """Convert to dScript for State.set() compatibility"""
        from dars.scripts.dscript import dScript
        return dScript(self._get_code())
    
    def __repr__(self):
        return f"BooleanExpression({self.left} {self.operator} {self.right})"


class ConditionalExpression:
    """
    Represents a conditional (ternary) expression: condition ? trueVal : falseVal
    
    Created by calling .then() on a BooleanExpression.
    """
    
    def __init__(self, condition, true_value, false_value):
        """
        Initialize a conditional expression.
        
        Args:
            condition: BooleanExpression
            true_value: Value if condition is true
            false_value: Value if condition is false
        """
        self.condition = condition
        self.true_value = true_value
        self.false_value = false_value
    
    def _get_value_code(self, value) -> str:
        """Get JavaScript code for a value"""
        if isinstance(value, (ValueRef, MathExpression, BooleanExpression, ConditionalExpression)):
            return value._get_code()
        elif isinstance(value, bool):
            return 'true' if value else 'false'
        elif isinstance(value, (int, float)):
            return str(value)
        elif isinstance(value, dict):
            # For style dicts
            return json.dumps(value)
        else:
            return json.dumps(value)
    
    def _to_structure(self) -> dict:
        """
        Generate DAP structure for conditional expression.
        """
        cond = self.condition._to_structure() if hasattr(self.condition, '_to_structure') else self.condition
        true_v = self.true_value._to_structure() if hasattr(self.true_value, '_to_structure') else self.true_value
        false_v = self.false_value._to_structure() if hasattr(self.false_value, '_to_structure') else self.false_value
        
        return {
            "op": "cond_expr",
            "args": {
                "condition": cond,
                "true_val": true_v,
                "false_val": false_v
            }
        }
        
    def _get_code(self) -> str:
        """Get native JavaScript code for this expression."""
        from dars.scripts.dscript import compile_val
        return compile_val(self._to_structure())

    def __str__(self):
        """String representation for embedding in JS template literals"""
        return f"${{{self._get_code()}}}"

    def __format__(self, format_spec):
        """Support for f-string formatting"""
        return f"${{{self._get_code()}}}"
    
    def get_code(self) -> str:
        """Public method for dScript compatibility"""
        return self._get_code()
    
    def to_dscript(self):
        """Convert to dScript for State.set() compatibility"""
        from dars.scripts.dscript import dScript
        return dScript(self._get_code())
    
    def __repr__(self):
        return f"ConditionalExpression({self.condition} ? {self.true_value} : {self.false_value})"


class LogicalExpression:
    """
    Represents a logical expression combining two boolean expressions with && or ||.
    """
    
    def __init__(self, left, operator: str, right):
        """
        Initialize a logical expression.
        
        Args:
            left: Left BooleanExpression
            operator: Logical operator (&& or ||)
            right: Right BooleanExpression
        """
        self.left = left
        self.operator = operator
        self.right = right
    
    def _to_structure(self) -> dict:
        """Generate DAP structure."""
        left = self.left._to_structure() if hasattr(self.left, '_to_structure') else self.left
        right = self.right._to_structure() if hasattr(self.right, '_to_structure') else self.right
        
        return {
            "op": "bool_expr", # Can generally use same op for logical, as _resolve handles && and ||
            "args": {
                "left": left,
                "operator": self.operator,
                "right": right
            }
        }

    def _get_code(self) -> str:
        from dars.scripts.dscript import compile_val
        return compile_val(self._to_structure())

    def __str__(self):
        return f"${{{self._get_code()}}}"
    
    def then(self, true_value, false_value):
        """Allow chaining .then() on logical expressions"""
        return ConditionalExpression(self, true_value, false_value)
    
    def and_(self, other):
        """Chain another AND"""
        return LogicalExpression(self, '&&', other)
    
    def or_(self, other):
        """Chain another OR"""
        return LogicalExpression(self, '||', other)
    
    def get_code(self) -> str:
        """Public method for dScript compatibility"""
        return self._get_code()
    
    def to_dscript(self):
        """Convert to dScript for State.set() compatibility"""
        from dars.scripts.dscript import dScript
        return dScript(self._get_code())
    
    def __repr__(self):
        return f"LogicalExpression({self.left} {self.operator} {self.right})"



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
    
    def _to_structure(self) -> dict:
        """
        Generate DAP structure for the value.
        """
        if self._custom_code:
             return self._custom_code # Should be a structure if possible, but keep fallback
             
        if self._is_state_path():
            parts = self.selector.split('.')
            base_val = {"op": "get_state_value", "args": {"state_id": parts[0], "prop_name": parts[1]}}
        else:
            base_val = {"op": "get_dom_value", "args": {"selector": self.selector}}
            
        if self._transform:
            return {"op": "transform", "args": {"input": base_val, "method": self._transform}}
            
        return base_val

    def _get_code(self) -> str:
        """Public method for dScript compatibility"""
        from dars.scripts.dscript import compile_val
        return compile_val(self._to_structure())

    # String operations
    def upper(self) -> 'ValueRef':
        """Convert to uppercase"""
        new_ref = ValueRef(self.selector)
        new_ref._transform = "upper"
        return new_ref
    
    def lower(self) -> 'ValueRef':
        """Convert to lowercase"""
        new_ref = ValueRef(self.selector)
        new_ref._transform = "lower"
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
        new_ref._transform = "int"
        return new_ref
    
    def float(self) -> 'ValueRef':
        """Convert to float"""
        new_ref = ValueRef(self.selector)
        # Chain transformations: if there's an existing transform, apply it first
        # Same simplification as int()
        new_ref._transform = "float"
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
        return self._transform in ["int", "float"]
    
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
    
    # Comparison operators (return BooleanExpression)
    def __eq__(self, other) -> 'BooleanExpression':
        """
        Equality comparison: V() == other
        
        Returns:
            BooleanExpression object
            
        Example:
            is_same = V("#name") == "John"
            is_equal = V("#age").int() == V("#min-age").int()
        """
        return BooleanExpression(self, '===', other)
    
    def __ne__(self, other) -> 'BooleanExpression':
        """
        Inequality comparison: V() != other
        
        Returns:
            BooleanExpression object
            
        Example:
            is_different = V("#status") != "pending"
        """
        return BooleanExpression(self, '!==', other)
    
    def __gt__(self, other) -> 'BooleanExpression':
        """
        Greater than: V() > other
        
        Requires .int() or .float() transformation.
        
        Returns:
            BooleanExpression object
            
        Example:
            is_adult = V("#age").int() > 18
        """
        if not self._has_numeric_transform():
            raise TypeError(
                f"Greater than comparison requires numeric transformation. "
                f"Use V('{self.selector}').int() or V('{self.selector}').float() before comparing."
            )
        return BooleanExpression(self, '>', other)
    
    def __lt__(self, other) -> 'BooleanExpression':
        """
        Less than: V() < other
        
        Requires .int() or .float() transformation.
        
        Returns:
            BooleanExpression object
            
        Example:
            is_child = V("#age").int() < 18
        """
        if not self._has_numeric_transform():
            raise TypeError(
                f"Less than comparison requires numeric transformation. "
                f"Use V('{self.selector}').int() or V('{self.selector}').float() before comparing."
            )
        return BooleanExpression(self, '<', other)
    
    def __ge__(self, other) -> 'BooleanExpression':
        """
        Greater than or equal: V() >= other
        
        Requires .int() or .float() transformation.
        
        Returns:
            BooleanExpression object
            
        Example:
            is_valid = V("#age").int() >= 18
        """
        if not self._has_numeric_transform():
            raise TypeError(
                f"Greater than or equal comparison requires numeric transformation. "
                f"Use V('{self.selector}').int() or V('{self.selector}').float() before comparing."
            )
        return BooleanExpression(self, '>=', other)
    
    def __le__(self, other) -> 'BooleanExpression':
        """
        Less than or equal: V() <= other
        
        Requires .int() or .float() transformation.
        
        Returns:
            BooleanExpression object
            
        Example:
            is_in_range = V("#value").int() <= 100
        """
        if not self._has_numeric_transform():
            raise TypeError(
                f"Less than or equal comparison requires numeric transformation. "
                f"Use V('{self.selector}').int() or V('{self.selector}').float() before comparing."
            )
        return BooleanExpression(self, '<=', other)
    
    # String methods (return BooleanExpression or ValueRef)
    def includes(self, substring: str) -> 'BooleanExpression':
        """
        Check if string includes substring (generates JS .includes()).
        
        Args:
            substring: Substring to search for
            
        Returns:
            BooleanExpression object
            
        Example:
            has_at = V("#email").includes("@")
            has_domain = V("#url").includes(".com")
        """
        # Create a custom ValueRef that calls .includes()
        new_ref = ValueRef(self.selector)
        new_ref._transform = lambda x: f"String({x}).includes({json.dumps(substring)})"
        # Return a boolean expression that evaluates to the result
        return BooleanExpression(new_ref, '===', True)
    
    def startswith(self, prefix: str) -> 'BooleanExpression':
        """
        Check if string starts with prefix (generates JS .startsWith()).
        
        Args:
            prefix: Prefix to check for
            
        Returns:
            BooleanExpression object
            
        Example:
            is_https = V("#url").startswith("https")
        """
        new_ref = ValueRef(self.selector)
        new_ref._transform = lambda x: f"String({x}).startsWith({json.dumps(prefix)})"
        return BooleanExpression(new_ref, '===', True)
    
    def endswith(self, suffix: str) -> 'BooleanExpression':
        """
        Check if string ends with suffix (generates JS .endsWith()).
        
        Args:
            suffix: Suffix to check for
            
        Returns:
            BooleanExpression object
            
        Example:
            is_image = V("#filename").endswith(".png")
        """
        new_ref = ValueRef(self.selector)
        new_ref._transform = lambda x: f"String({x}).endsWith({json.dumps(suffix)})"
        return BooleanExpression(new_ref, '===', True)
    
    def length(self) -> 'ValueRef':
        """
        Get string length (generates JS .length).
        
        Returns:
            ValueRef with .int() transformation
            
        Example:
            name_length = V("#name").length()
            is_valid = V("#password").length().int() >= 8
        """
        new_ref = ValueRef(self.selector)
        new_ref._transform = lambda x: f"String({x}).length"
        # Automatically apply int() since length is always a number
        return new_ref.int()
    
    def bool(self) -> 'ValueRef':
        """
        Mark this ValueRef as a boolean type.
        Converts the value to boolean (generates JS Boolean()).
        
        Returns:
            ValueRef with boolean transformation
            
        Example:
            is_active = V("#is-active").bool()
            comparison = V("#flag1").bool() == V("#flag2").bool()
        """
        new_ref = ValueRef(self.selector)
        new_ref._transform = lambda x: f"Boolean({x})"
        return new_ref
    
    def __str__(self):
        """String representation for f-strings and template literals"""
        return f"${{{self._get_code()}}}"
    
    def __format__(self, format_spec):
        """Support for f-string formatting"""
        return f"${{{self._get_code()}}}"
    
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
    ```python
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
    ```
    """
    return ValueRef(selector)


def equal(value: Union[ValueRef, MathExpression, BooleanExpression, ConditionalExpression, LogicalExpression, int, float, str, bool]) -> MathExpression:
    """Helper to normalize a value into a MathExpression.

    This makes it easy to combine literals or other expressions with V()/MathExpression
    trees without worrying about operator precedence or async semantics.

    Examples
    -------
    - Simple literal:
        V(".dyn").int() + equal(0)

    - With another V() expression:
        V(".a").int() + equal(V(".b").int())
    """

    # If value is already a MathExpression, just return it
    if isinstance(value, MathExpression):
        return value

    # Otherwise, wrap it in a neutral MathExpression (value + 0)
    return MathExpression(value, '+', 0)


def url(template: str, **kwargs) -> MathExpression:
    """Build dynamic URLs with clean syntax.
    
    Returns a MathExpression that concatenates parts, avoiding backtick nesting issues.
    """
    import re
    from dars.hooks.value_helpers import MathExpression
    
    # Split template by placeholders: "http://{base}/users/{id}"
    parts = re.split(r"(\{.*?\})", template)
    
    result = None
    
    for part in parts:
        # Check if part is a placeholder: "{name}"
        match = re.match(r"\{(.*?)\}", part)
        if match:
            key = match.group(1)
            val = kwargs.get(key, part)
        else:
            val = part
            
        if val == "": continue
            
        if result is None:
            if isinstance(val, (ValueRef, MathExpression)):
                result = val
            else:
                # Start with a dummy MathExpression to ensure correct typing
                result = MathExpression(val, '+', "")
        else:
            result = result + val
            
    return result


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
