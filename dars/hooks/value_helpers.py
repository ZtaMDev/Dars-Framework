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
        
        # Detect if this is string concatenation vs math operation
        # Math operations are indicated by .int() or .float() transformations
        # If operator is '+' and neither operand has numeric transformation, it's string concat
        is_math_operation = False
        
        if self.operator == '+':
            # Helper function to check if an expression is a math operation
            def is_math_expr(expr):
                """Recursively check if expression is a math operation."""
                if isinstance(expr, ValueRef):
                    # Check if it has numeric transformation
                    if expr._transform is not None:
                        transform_str = str(expr._transform('x'))
                        return 'parseInt' in transform_str or 'parseFloat' in transform_str
                    return False
                elif isinstance(expr, MathExpression):
                    # For nested MathExpression, check if it's a math operation
                    # If operator is not '+', it's always math
                    if expr.operator != '+':
                        return True
                    # If operator is '+', recursively check operands
                    return is_math_expr(expr.left) or is_math_expr(expr.right)
                return False
            
            # Check if either operand indicates a math operation
            is_math_operation = is_math_expr(self.left) or is_math_expr(self.right)
        else:
            # All other operators (-, *, /, %, **) are always math operations
            is_math_operation = True
        
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
        
        # Only validate for NaN if this is a math operation
        if is_math_operation:
            # Validate inputs for math operations
            code_parts.append("    if (isNaN(left) || isNaN(right)) {")
            code_parts.append("        console.warn('[Dars] Invalid input: one or more values are NaN. Returning 0.');")
            code_parts.append("        return 0;")
            code_parts.append("    }")
        
        # Return the operation
        code_parts.append(f"    const result = left {self.operator} right;")
        
        # Only validate result for NaN if this is a math operation
        if is_math_operation:
            # Validate result for math operations
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
    
    def _get_code(self) -> str:
        """
        Generate JavaScript code from boolean expression.
        
        Returns:
            JavaScript code string that evaluates the comparison
        """
        left_code = self._get_operand_code(self.left)
        right_code = self._get_operand_code(self.right)
        
        # Check if operands are async (ValueRef or nested expressions)
        left_is_async = isinstance(self.left, (ValueRef, MathExpression, BooleanExpression))
        right_is_async = isinstance(self.right, (ValueRef, MathExpression, BooleanExpression))
        
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
        
        # Return the comparison
        code_parts.append(f"    return left {self.operator} right;")
        code_parts.append("})()")
        
        return "\n".join(code_parts)
    
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
    
    def _get_code(self) -> str:
        """
        Generate JavaScript ternary operator code.
        
        Returns:
            JavaScript code string
        """
        condition_code = self.condition._get_code()
        true_code = self._get_value_code(self.true_value)
        false_code = self._get_value_code(self.false_value)
        
        # Check if any part is async
        condition_is_async = isinstance(self.condition, (BooleanExpression, ValueRef, MathExpression))
        true_is_async = isinstance(self.true_value, (ValueRef, MathExpression, BooleanExpression))
        false_is_async = isinstance(self.false_value, (ValueRef, MathExpression, BooleanExpression))
        
        if not condition_is_async and not true_is_async and not false_is_async:
            return f"{condition_code} ? {true_code} : {false_code}"
        
        # Generate async IIFE
        code_parts = []
        code_parts.append("(async () => {")
        code_parts.append(f"    const cond = await ({condition_code});")
        
        if true_is_async:
            code_parts.append(f"    const trueVal = await ({true_code});")
        else:
            code_parts.append(f"    const trueVal = {true_code};")
        
        if false_is_async:
            code_parts.append(f"    const falseVal = await ({false_code});")
        else:
            code_parts.append(f"    const falseVal = {false_code};")
        
        code_parts.append("    return cond ? trueVal : falseVal;")
        code_parts.append("})()")
        
        return "\n".join(code_parts)
    
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
    
    def _get_code(self) -> str:
        """Generate JavaScript code"""
        left_code = self.left._get_code() if hasattr(self.left, '_get_code') else str(self.left)
        right_code = self.right._get_code() if hasattr(self.right, '_get_code') else str(self.right)
        
        # Check if async
        left_is_async = isinstance(self.left, (BooleanExpression, ValueRef, MathExpression))
        right_is_async = isinstance(self.right, (BooleanExpression, ValueRef, MathExpression))
        
        if not left_is_async and not right_is_async:
            return f"({left_code}) {self.operator} ({right_code})"
        
        # Generate async IIFE
        code_parts = []
        code_parts.append("(async () => {")
        code_parts.append(f"    const left = await ({left_code});")
        code_parts.append(f"    const right = await ({right_code});")
        code_parts.append(f"    return left {self.operator} right;")
        code_parts.append("})()")
        
        return "\n".join(code_parts)
    
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
        # Chain transformations: if there's an existing transform, apply it first
        if self._transform:
            # Apply existing transform, then parseInt
            new_ref._transform = lambda x: f"parseInt({self._transform(x)}, 10)"
        else:
            new_ref._transform = lambda x: f"parseInt({x}, 10)"
        return new_ref
    
    def float(self) -> 'ValueRef':
        """Convert to float"""
        new_ref = ValueRef(self.selector)
        # Chain transformations: if there's an existing transform, apply it first
        if self._transform:
            # Apply existing transform, then parseFloat
            new_ref._transform = lambda x: f"parseFloat({self._transform(x)})"
        else:
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
