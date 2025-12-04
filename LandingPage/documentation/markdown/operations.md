# Operations in Dars

Dars introduces a powerful, declarative system for mathematical expressions using operator overloading. Write complex calculations in pure Python without any inline JavaScript!

## Overview

The `V()` helper supports:
-  **Operator overloading** - Use Python operators (`+`, `-`, `*`, `/`, `%`, `**`)
-  **Dynamic operators** - Operators from Select/Input elements
-  **Automatic precedence** - Parentheses handled automatically
-  **NaN validation** - Safe handling of empty/invalid inputs
-  **Type safety** - Numeric operations require `.float()` or `.int()`

---

## Basic Operations

### String Concatenation

String concatenation works without any transformations:

```python
from dars.all import *

# Simple concatenation
state.fullname.set(V(".first") + " " + V(".last"))

# With literals
state.message.set("Hello, " + V(".username") + "!")

# Multiple values
state.info.set(V(".name") + " - " + V(".email") + " - " + V(".phone"))
```

### Arithmetic Operations

**IMPORTANT**: Arithmetic operations **require** `.float()` or `.int()` transformations:

```python
# Addition
state.total.set(V(".price").float() + V(".tax").float())

# Subtraction
state.change.set(V(".paid").float() - V(".total").float())

# Multiplication
state.total.set(V(".price").float() * V(".quantity").int())

# Division
state.average.set(V(".sum").float() / V(".count").int())

# Module
state.remainder.set(V(".number").int() % V(".divisor").int())

# Power
state.result.set(V(".base").float() ** V(".exponent").int())
```

**Why transformations are required:**
- Prevents accidental string concatenation (e.g., `"5" * "3"` = `"555"` in JavaScript)
- Ensures type safety
- Makes intent explicit

---

## Complex Expressions

### Operator Precedence

Dars automatically handles operator precedence following standard mathematical rules:

```python
# a + b * c  →  a + (b * c)  ✅ Automatic
state.result.set(
    V(".a").float() + V(".b").float() * V(".c").float()
)

# (a + b) * c  →  (a + b) * c  ✅ Preserved
state.result.set(
    (V(".a").float() + V(".b").float()) * V(".c").float()
)

# a ** b ** c  →  a ** (b ** c)  ✅ Right-associative
state.result.set(
    V(".a").float() ** V(".b").float() ** V(".c").float()
)
```

**Precedence Table:**

| Operator | Precedence | Associativity |
|----------|------------|---------------|
| `**`     | 3 (highest)| Right         |
| `*`, `/`, `%` | 2     | Left          |
| `+`, `-` | 1 (lowest) | Left          |

### Nested Expressions

You can nest expressions infinitely:

```python
# Complex calculation
state.result.set(
    ((V(".a").float() + V(".b").float()) * V(".c").float()) / 
    (V(".d").float() - V(".e").float())
)

# With mixed literals
state.total.set(
    (V(".price").float() * V(".qty").int()) * 1.15  # Add 15% tax
)

# Combining multiple operations
state.score.set(
    (V(".math").int() + V(".science").int() + V(".english").int()) / 3
)
```

---

## Dynamic Operators

**New in v1.6.4**: Use operators from Select or Input elements!

### The `.operator()` Method

Mark a `ValueRef` as a dynamic operator using `.operator()`:

```python
# Select with operator options
Select(
    class_name="operation",
    options=[
        SelectOption("+", "Add"),
        SelectOption("-", "Subtract"),
        SelectOption("*", "Multiply"),
        SelectOption("/", "Divide")
    ]
)

# Use in calculation
Button(
    "Calculate",
    on_click=calc.result.set(
        V(".num1").float() + V(".operation").operator() + V(".num2").float()
    )
)
```

### How It Works

1. **Operator Extraction**: `V(".operation").operator()` extracts the operator value
2. **Validation**: Checks if operator is valid (`+`, `-`, `*`, `/`, `%`, `**`)
3. **Evaluation**: Uses a switch statement to perform the operation
4. **Fallback**: Defaults to `+` if operator is invalid

### Complete Calculator Example

```python
from dars.all import *

app = App("Calculator")

calc = State("calc", operation="+", result=0)

@route("/")
def index():
    return Page(
        # Operation selector
        Select(
            value=useValue("calc.operation", selector=".operation"),
            class_name="operation",
            options=[
                SelectOption("+", "➕ Add"),
                SelectOption("-", "➖ Subtract"),
                SelectOption("*", "✖️ Multiply"),
                SelectOption("/", "➗ Divide")
            ]
        ),
        
        # Number inputs
        Input(class_name="num1", input_type="number", placeholder="First number"),
        Input(class_name="num2", input_type="number", placeholder="Second number"),
        
        # Calculate button - DECLARATIVE!
        Button(
            "Calculate",
            on_click=calc.result.set(
                V(".num1").float() + V(".operation").operator() + V(".num2").float()
            )
        ),
        
        # Result display
        Text(text=useDynamic("calc.result"))
    )

app.add_page("index", index())

if __name__ == "__main__":
    app.rTimeCompile()
```

### Supported Operators

The `.operator()` method validates against this whitelist:

- `+` - Addition
- `-` - Subtraction
- `*` - Multiplication
- `/` - Division
- `%` - Modulo
- `**` - Power

**Invalid operators** automatically fall back to `+` with a console warning.

---

## NaN Validation

**New in v1.6.4**: Automatic NaN handling prevents errors from empty or invalid inputs.

### Automatic Validation

All mathematical expressions include built-in NaN validation:

```python
# If inputs are empty or invalid
Button(
    "Calculate",
    on_click=calc.result.set(
        V(".num1").float() + V(".num2").float()
    )
)
# Empty inputs → Returns 0
# Console: "[Dars] Invalid input: one or more values are NaN. Returning 0."
```

### Validation Points

1. **Input Validation**: Checks operands before calculation
2. **Result Validation**: Checks result after calculation
3. **Console Logging**: Warns when NaN is detected

### Example Scenarios

```python
# Empty inputs
V(".empty-input").float()  # → 0 (with warning)

# Invalid division
V(".num").float() / 0  # → 0 (with warning)

# Invalid operation
V(".text").float()  # → 0 (with warning)
```

---

## State Integration

### Using with State.set()

`MathExpression` objects work seamlessly with `State.set()`:

```python
# Simple expression
calc.result.set(V(".a").float() + V(".b").float())

# Complex expression
calc.total.set(
    (V(".price").float() * V(".qty").int()) * 1.15
)

# With dynamic operator
calc.result.set(
    V(".num1").float() + V(".op").operator() + V(".num2").float()
)
```

### Async Evaluation

All expressions are automatically wrapped in async IIFEs:

```python
# Your code
calc.result.set(V(".a").float() + V(".b").float())

# Generated JavaScript
(async () => {
    const left = await (/* V(".a").float() */);
    const right = await (/* V(".b").float() */);
    
    if (isNaN(left) || isNaN(right)) {
        console.warn('[Dars] Invalid input: one or more values are NaN. Returning 0.');
        return 0;
    }
    
    const result = left + right;
    
    if (isNaN(result)) {
        console.warn('[Dars] Operation resulted in NaN. Returning 0.');
        return 0;
    }
    
    return result;
})()
```

---

## Advanced Examples

### Multi-Step Calculation

```python
# Calculate total with tax and discount
Button(
    "Calculate Total",
    on_click=cart.total.set(
        ((V(".price").float() * V(".qty").int()) * 1.15) - V(".discount").float()
    )
)
```

### Conditional Calculations

```python
# Different calculations based on operator
Select(class_name="calc-type", options=[
    SelectOption("area", "Area"),
    SelectOption("perimeter", "Perimeter")
])

# Area: length * width
# Perimeter: 2 * (length + width)
Button(
    "Calculate",
    on_click=dScript(f"""
        const type = {V(".calc-type").get_code()};
        const length = {V(".length").float().get_code()};
        const width = {V(".width").float().get_code()};
        
        let result;
        if (type === 'area') {{
            result = length * width;
        }} else {{
            result = 2 * (length + width);
        }}
        
        window.Dars.change({{
            id: 'calc',
            dynamic: true,
            result: result
        }});
    """)
)
```

### Scientific Calculator

```python
# Power calculation
calc.result.set(V(".base").float() ** V(".exponent").float())

# Modulo for remainders
calc.remainder.set(V(".dividend").int() % V(".divisor").int())

# Complex formula: (a² + b²)^0.5 (Pythagorean theorem)
calc.hypotenuse.set(
    (V(".a").float() ** 2 + V(".b").float() ** 2) ** 0.5
)
```

---

## Best Practices

### Do

1. **Always use transformations for math**
   ```python
   V(".price").float() * V(".qty").int()  # ✅ Correct
   ```

2. **Use descriptive class names**
   ```python
   Input(class_name="price-input")  # ✅ Clear
   V(".price-input").float()
   ```

3. **Leverage automatic precedence**
   ```python
   V(".a").float() + V(".b").float() * V(".c").float()  # ✅ Auto-parens
   ```

4. **Use dynamic operators for flexibility**
   ```python
   V(".num1").float() + V(".op").operator() + V(".num2").float()  # ✅ Dynamic
   ```

### Don't

1. **Don't use arithmetic without transformations**
   ```python
   V(".price") * V(".qty")  # ❌ TypeError
   ```

2. **Don't rely on implicit type coercion**
   ```python
   V(".number") + 5  # ❌ String concatenation, not addition
   ```

3. **Don't forget NaN is handled automatically**
   ```python
   # No need for manual checks
   if (isNaN(V(".num").float())) { ... }
   
   # Automatic validation
   calc.result.set(V(".num").float() + 10)
   ```

---

## Type Reference

### ValueRef

Created by `V(selector)`:

```python
class ValueRef:
    def int() -> ValueRef          # Convert to integer
    def float() -> ValueRef        # Convert to float
    def upper() -> ValueRef        # Convert to uppercase
    def lower() -> ValueRef        # Convert to lowercase
    def trim() -> ValueRef         # Remove whitespace
    def operator() -> DynamicOperator  # Mark as dynamic operator
    
    # Operators
    def __add__(other) -> MathExpression
    def __sub__(other) -> MathExpression
    def __mul__(other) -> MathExpression
    def __truediv__(other) -> MathExpression
    def __mod__(other) -> MathExpression
    def __pow__(other) -> MathExpression
```

### MathExpression

Created by operator overloading:

```python
class MathExpression:
    # Supports all arithmetic operators
    # Automatically handles precedence
    # Validates NaN
    # Generates async JavaScript
```

### DynamicOperator

Created by `.operator()`:

```python
class DynamicOperator:
    VALID_OPERATORS = ['+', '-', '*', '/', '%', '**']
    # Validates operator at runtime
    # Falls back to '+' if invalid
```

---
