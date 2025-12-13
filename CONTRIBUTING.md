# Contributing to Dars Framework

First off, thank you for considering contributing to Dars Framework! It's people like you that make Dars such a great tool for building modern web applications with Python.

## Table of Contents

- [How Can I Contribute?](#how-can-i-contribute)
  - [Reporting Bugs](#reporting-bugs)
- [Development Setup](#development-setup)
- [Project Structure](#project-structure)
- [Coding Guidelines](#coding-guidelines)
- [Testing](#testing)
- [Documentation](#documentation)
- [Community](#community)

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the [issue tracker](https://github.com/ZtaMDev/Dars-Framework/issues) as you might find out that you don't need to create one. When you are creating a bug report, please include as many details as possible:

**Bug Report Template:**

```markdown
**Describe the bug**
A clear and concise description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Create a component with '...'
2. Run the app with '...'
3. See error

**Expected behavior**
A clear and concise description of what you expected to happen.

**Code Example**
```python
# Minimal reproducible example
from dars.all import *
# ...
```

**Environment:**
- Dars Framework version: [e.g., 1.6.4]
- Python version: [e.g., 3.10.0]
- Operating System: [e.g., Windows 11, macOS 13, Ubuntu 22.04]
- Browser (if applicable): [e.g., Chrome 120, Firefox 121]

**Additional context**
Add any other context about the problem here.
```

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, please include:

- **Use a clear and descriptive title**
- **Provide a detailed description** of the suggested enhancement
- **Explain why this enhancement would be useful** to most Dars users
- **Provide code examples** showing how the feature would be used
- **List any alternatives** you've considered

**Enhancement Template:**

```markdown
**Is your feature request related to a problem?**
A clear and concise description of what the problem is. Ex. I'm always frustrated when [...]

**Describe the solution you'd like**
A clear and concise description of what you want to happen.

**Code Example**
```python
# How you envision using this feature
from dars.all import *
# ...
```

**Describe alternatives you've considered**
A clear and concise description of any alternative solutions or features you've considered.

**Additional context**
Add any other context or screenshots about the feature request here.
```

### Pull Requests

We actively welcome your pull requests! Here's the process:

1. **Fork the repository** and create your branch from `main`
2. **Make your changes** following our [coding guidelines](#coding-guidelines)
3. **Add tests** if you've added code that should be tested
4. **Update documentation** if you've changed APIs or added features
5. **Ensure the test suite passes** (`pytest`)
6. **Make sure your code lints** (follow PEP 8)
7. **Submit your pull request**

**Pull Request Guidelines:**

- **One feature per PR** - Keep pull requests focused on a single feature or bug fix
- **Write clear commit messages** - Use present tense ("Add feature" not "Added feature")
- **Reference issues** - Link to related issues in your PR description
- **Update CHANGELOG** - Add your changes to the unreleased section
- **Be patient** - Maintainers will review your PR as soon as possible

**Commit Message Format:**

<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat`: A new feature
- `fix`: A bug fix
- `docs`: Documentation only changes
- `style`: Changes that don't affect code meaning (formatting, etc.)
- `refactor`: Code change that neither fixes a bug nor adds a feature
- `perf`: Performance improvement
- `test`: Adding missing tests
- `chore`: Changes to build process or auxiliary tools

**Examples:**
```
feat(components): add Carousel component

Add a new Carousel component with auto-play and navigation controls.
Includes full documentation and examples.

Closes #123
```

```
fix(state): resolve useDynamic numeric value display

Fixed issue where useDynamic would display marker strings instead
of actual numeric values, especially for 0.

Fixes #456
```

## Development Setup

### Prerequisites

- Python 3.11 or higher
- pip (Python package installer)
- Git

### Setup Steps

1. **Clone your fork:**
   ```bash
   git clone https://github.com/ZtaMDev/Dars-Framework.git
   cd Dars-Framework
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
   
5. **Install in editable mode using PyDepM:**
   ```bash
   pydep install -e
   ```

6. **Create a branch for your changes:**
   ```bash
   git checkout -b feature/my-new-feature
   ```

## Project Structure

```
Dars-Framework/
├── dars/                      # Main package
│   ├── components/            # Built-in components
│   │   ├── basic/            # Basic components (Text, Button, Input, etc.)
│   │   ├── layout/           # Layout components (Container, Grid, Flex)
│   │   └── advanced/         # Advanced components (Modal, Tabs, etc.)
│   ├── core/                 # Core framework functionality
│   │   ├── app.py           # App class
│   │   ├── component.py     # Base Component class
│   │   ├── state_v2.py      # State management
│   │   └── utilities.py     # Tailwind-like utilities
│   ├── hooks/                # Hooks system
│   │   ├── use_dynamic.py   # useDynamic hook
│   │   ├── use_value.py     # useValue hook
│   │   ├── use_watch.py     # useWatch hook
│   │   └── value_helpers.py # V() helper and MathExpression
│   ├── scripts/              # dScript system
│   │   ├── dscript.py       # dScript class
│   │   └── utils_ds.py      # Utility functions
│   ├── exporters/            # Export systems
│   │   └── web/             # Web exporter (HTML/CSS/JS)
│   └── cli/                  # CLI tools
├── LandingPage/             # Documentation site
│   ├── documentation/       # Markdown documentation
│   └── releases/            # Release notes
├── README.md
├── CONTRIBUTING.md          # This file
├── LICENSE
└── pypackage.json           # Package configuration
```

## Coding Guidelines

### Python Style

- **Follow PEP 8** - Use 4 spaces for indentation, not tabs
- **Maximum line length** - 100 characters (soft limit), 120 (hard limit)
- **Naming conventions:**
  - Classes: `PascalCase` (e.g., `Button`, `StateManager`)
  - Functions/methods: `snake_case` (e.g., `render_component`, `get_value`)
  - Constants: `UPPER_SNAKE_CASE` (e.g., `DEFAULT_PORT`, `MAX_RETRIES`)
  - Private members: `_leading_underscore` (e.g., `_internal_method`)

### Code Quality

- **Type hints** - Use type hints for function parameters and return values
  ```python
  def render_component(component: Component, context: Dict[str, Any]) -> str:
      ...
  ```

- **Docstrings** - Use Google-style docstrings for all public APIs
  ```python
  def create_button(text: str, on_click: Optional[Callable] = None) -> Button:
      """
      Create a button component.
      
      Args:
          text: The button text
          on_click: Optional click handler
          
      Returns:
          Button component instance
          
      Example:
          >>> btn = create_button("Click me", on_click=my_handler)
      """
      ...
  ```

- **Comments** - Write clear, concise comments for complex logic
- **DRY principle** - Don't repeat yourself; extract common code into functions
- **SOLID principles** - Follow object-oriented design principles

### Component Development

When creating new components:

1. **Inherit from `Component`** - All components should extend the base `Component` class
2. **Define clear props** - Use type hints for all component properties
3. **Implement `render()`** - Abstract method that exporters will implement
4. **Add examples** - Include usage examples in docstrings

**Example:**

```python
from dars.core.component import Component
from typing import Optional

class MyComponent(Component):
    """
    A custom component that does something awesome.
    
    Example:
        >>> comp = MyComponent(title="Hello", value=42)
        >>> page.add(comp)
    """
    
    def __init__(
        self,
        title: str,
        value: int = 0,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.title = title
        self.value = value
    
    def render(self):
        """Render method implemented by exporters"""
        raise NotImplementedError("Render must be implemented by exporter")
```

## Testing

### Writing Tests

- **Use pytest** - All tests should use pytest framework
- **Test file naming** - `test_*.py` or `*_test.py`
- **Test function naming** - `test_<what_is_being_tested>`
- **Arrange-Act-Assert** - Structure tests clearly

**Example:**

```python
import pytest
from dars.components.basic import Button

def test_button_creation():
    # Arrange
    text = "Click me"
    
    # Act
    button = Button(text)
    
    # Assert
    assert button.text == text
    assert button.disabled == False

def test_button_with_click_handler():
    # Arrange
    handler = lambda: print("clicked")
    
    # Act
    button = Button("Test", on_click=handler)
    
    # Assert
    assert button.on_click == handler

@pytest.mark.parametrize("text,expected", [
    ("Hello", "Hello"),
    ("", ""),
    ("Test 123", "Test 123"),
])
def test_button_text_variations(text, expected):
    button = Button(text)
    assert button.text == expected
```

### Test Coverage

- **Aim for 80%+ coverage** - New features should include tests
- **Test edge cases** - Don't just test the happy path
- **Test error handling** - Ensure errors are handled gracefully

## Documentation

### Code Documentation

- **Docstrings** - All public classes, methods, and functions must have docstrings
- **Type hints** - Use type hints consistently
- **Examples** - Include usage examples in docstrings

### User Documentation

When adding features, update:

1. **README.md** - If it affects getting started or core features
2. **Documentation markdown** - Add/update files in `LandingPage/documentation/markdown/`

### Documentation Style

- **Be concise** - Clear and to the point
- **Use examples** - Show, don't just tell
- **Be consistent** - Follow existing documentation patterns
- **Use proper markdown** - Headers, code blocks, lists, etc.

## Community

### Getting Help

- **GitHub Issues** - For bugs and feature requests
- **Discussions** - For questions and general discussion

### Recognition

Contributors will be:
- Listed in the project's contributors page
- Mentioned in release notes for significant contributions
- Invited to join the core team for sustained contributions

## License

By contributing to Dars Framework, you agree that your contributions will be licensed under the [Mozilla Public License 2.0](LICENSE).

---

Thank you for contributing to Dars Framework! 🎉
