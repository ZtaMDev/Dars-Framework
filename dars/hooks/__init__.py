# Dars Framework - Core Source File
#
# This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0.
# If a copy of the MPL was not distributed with this file, You can obtain one at
# https://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2025 ZtaDev
"""
# Hooks System

Dars Framework introduces a **Hooks system** inspired by React, enabling reactive and stateful behavior in both FunctionComponents and built-in components.

The reactivity system in Dars is divided into the following sections:

1. **Pythonic Value Helpers**: The `V()` helper and expression system used throughout all hooks.
2. **Component-Level State (VRefs)**: Lightweight, fast, and DOM-bound reactive state.
3. **Global Application State**: Structured `State` objects for shared application logic.
4. **Forms & Validation**: Hooks for form collection and client-side validation.
5. **Network & Async Operations**: Data fetching and chained actions.
6. **Best Practices**: Guidelines and tips.
"""

from .use_dynamic import useDynamic
from .form_helpers import FormData, collect_form
from .set_vref import setVRef
from .update_vref import updateVRef
from .use_fetch import useFetch
from .form_validator import (
    FormValidator,
    required, min_length, max_length, pattern, email, min_value, max_value, custom,
)

__all__ = [
    'useDynamic', 'FormData', 'collect_form', 'setVRef', 'updateVRef',
    'useFetch',
    'FormValidator', 'required', 'min_length', 'max_length', 'pattern',
    'email', 'min_value', 'max_value', 'custom',
]
