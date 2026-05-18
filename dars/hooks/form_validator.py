# Dars Framework - Core Source File
#
# This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0.
# If a copy of the MPL was not distributed with this file, You can obtain one at
# https://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2025 ZtaDev
"""
FormValidator — declarative form validation with dual client/server enforcement.

Rules are declared once in Python and evaluated both server-side (via
:meth:`FormValidator.validate_server`) and client-side (via
:meth:`FormValidator.validate_client`, which returns a DAP dScript).

Example::

    from dars.hooks.form_validator import FormValidator, required, email, min_length
    from dars.hooks.form_helpers import collect_form

    validator = FormValidator({
        "email":    [required(), email()],
        "password": [required(), min_length(8)],
    })

    form = collect_form(email=V("#email"), password=V("#password"))

    Button("Submit", on_click=validator.validated_submit("/api/login", form))
"""

import json
import re as _re
from abc import ABC, abstractmethod
from typing import Any, Callable, Dict, List, Optional

from dars.scripts.dscript import dScript


# ---------------------------------------------------------------------------
# Rule base class
# ---------------------------------------------------------------------------

class Rule(ABC):
    """Abstract base for all validation rules."""

    @abstractmethod
    def validate(self, value: Any) -> Optional[str]:
        """Return an error message string, or ``None`` if the value is valid."""

    @abstractmethod
    def to_dict(self) -> dict:
        """Serialise the rule to a JSON-compatible dict (for ``get_rules_json``)."""


# ---------------------------------------------------------------------------
# Concrete rule classes
# ---------------------------------------------------------------------------

class RequiredRule(Rule):
    def validate(self, value: Any) -> Optional[str]:
        if value is None or str(value).strip() == "":
            return "This field is required."
        return None

    def to_dict(self) -> dict:
        return {"type": "required"}


class MinLengthRule(Rule):
    def __init__(self, n: int) -> None:
        self.n = n

    def validate(self, value: Any) -> Optional[str]:
        if value is not None and len(str(value)) < self.n:
            return f"Must be at least {self.n} characters."
        return None

    def to_dict(self) -> dict:
        return {"type": "min_length", "n": self.n}


class MaxLengthRule(Rule):
    def __init__(self, n: int) -> None:
        self.n = n

    def validate(self, value: Any) -> Optional[str]:
        if value is not None and len(str(value)) > self.n:
            return f"Must be at most {self.n} characters."
        return None

    def to_dict(self) -> dict:
        return {"type": "max_length", "n": self.n}


class PatternRule(Rule):
    def __init__(self, regex: str) -> None:
        self.regex = regex
        self._compiled = _re.compile(regex)

    def validate(self, value: Any) -> Optional[str]:
        if value is not None and not self._compiled.match(str(value)):
            return f"Does not match required pattern."
        return None

    def to_dict(self) -> dict:
        return {"type": "pattern", "regex": self.regex}


class EmailRule(Rule):
    _EMAIL_RE = _re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

    def validate(self, value: Any) -> Optional[str]:
        if value is not None and not self._EMAIL_RE.match(str(value)):
            return "Must be a valid email address."
        return None

    def to_dict(self) -> dict:
        return {"type": "email"}


class MinValueRule(Rule):
    def __init__(self, n: float) -> None:
        self.n = n

    def validate(self, value: Any) -> Optional[str]:
        try:
            if float(value) < self.n:
                return f"Must be at least {self.n}."
        except (TypeError, ValueError):
            return f"Must be a number >= {self.n}."
        return None

    def to_dict(self) -> dict:
        return {"type": "min_value", "n": self.n}


class MaxValueRule(Rule):
    def __init__(self, n: float) -> None:
        self.n = n

    def validate(self, value: Any) -> Optional[str]:
        try:
            if float(value) > self.n:
                return f"Must be at most {self.n}."
        except (TypeError, ValueError):
            return f"Must be a number <= {self.n}."
        return None

    def to_dict(self) -> dict:
        return {"type": "max_value", "n": self.n}


class CustomRule(Rule):
    """Python-only rule; omitted from ``get_rules_json`` output."""

    def __init__(self, fn: Callable[[Any], Optional[str]]) -> None:
        self._fn = fn

    def validate(self, value: Any) -> Optional[str]:
        try:
            return self._fn(value)
        except Exception:
            return "Validation error."

    def to_dict(self) -> dict:
        # Custom rules cannot be serialised to JSON
        return {}


# ---------------------------------------------------------------------------
# Convenience constructors
# ---------------------------------------------------------------------------

def required() -> RequiredRule:
    return RequiredRule()

def min_length(n: int) -> MinLengthRule:
    return MinLengthRule(n)

def max_length(n: int) -> MaxLengthRule:
    return MaxLengthRule(n)

def pattern(regex: str) -> PatternRule:
    return PatternRule(regex)

def email() -> EmailRule:
    return EmailRule()

def min_value(n: float) -> MinValueRule:
    return MinValueRule(n)

def max_value(n: float) -> MaxValueRule:
    return MaxValueRule(n)

def custom(fn: Callable[[Any], Optional[str]]) -> CustomRule:
    return CustomRule(fn)


# ---------------------------------------------------------------------------
# FormValidator
# ---------------------------------------------------------------------------

class FormValidator:
    """
    Declarative form validator with dual client/server enforcement.

    Args:
        fields: ``{"field_name": [rule1, rule2, ...], ...}``
    """

    def __init__(self, fields: Dict[str, List[Rule]]) -> None:
        self.fields = fields

    # ------------------------------------------------------------------
    # Server-side validation
    # ------------------------------------------------------------------

    def validate_server(self, data: dict) -> dict:
        """
        Run all rules against *data* server-side.

        Args:
            data: ``{"field_name": value, ...}``

        Returns:
            ``{"field_name": ["error msg", ...], ...}`` or ``{}`` if all pass.
        """
        errors: Dict[str, List[str]] = {}
        for field, rules in self.fields.items():
            value = data.get(field)
            field_errors: List[str] = []
            for rule in rules:
                msg = rule.validate(value)
                if msg:
                    field_errors.append(msg)
            if field_errors:
                errors[field] = field_errors
        return errors

    # ------------------------------------------------------------------
    # Client-side validation (DAP dScript)
    # ------------------------------------------------------------------

    def validate_client(self, form_data) -> 'dScript':
        """
        Generate a dScript that runs client-side validation.

        On failure: sets ``textContent`` of ``#{field_name}-error`` elements.
        On all-pass: clears all error elements.

        Args:
            form_data: :class:`~dars.hooks.form_helpers.FormData` instance.

        Returns:
            :class:`~dars.scripts.dscript.dScript` encoding a DAP ``sequence``.
        """
        actions = []

        for field, rules in self.fields.items():
            error_id = f"{field}-error"
            for rule in rules:
                rule_dict = rule.to_dict()
                if not rule_dict:
                    continue  # skip CustomRule (not serialisable)

                rule_type = rule_dict.get("type")
                field_selector = f"#{field}"
                get_val = {
                    "op": "get_dom_value",
                    "args": {"selector": field_selector},
                }

                if rule_type == "required":
                    condition = {
                        "op": "bool_expr",
                        "args": {
                            "left": {"op": "transform", "args": {"input": get_val, "method": "lower"}},
                            "right": "",
                            "operator": "==",
                        },
                    }
                    error_msg = rule.validate("") or "This field is required."
                elif rule_type == "min_length":
                    n = rule_dict["n"]
                    condition = {
                        "op": "bool_expr",
                        "args": {
                            "left": {"op": "transform", "args": {"input": get_val, "method": "length"}},
                            "right": n,
                            "operator": "<",
                        },
                    }
                    error_msg = f"Must be at least {n} characters."
                elif rule_type == "max_length":
                    n = rule_dict["n"]
                    condition = {
                        "op": "bool_expr",
                        "args": {
                            "left": {"op": "transform", "args": {"input": get_val, "method": "length"}},
                            "right": n,
                            "operator": ">",
                        },
                    }
                    error_msg = f"Must be at most {n} characters."
                elif rule_type == "email":
                    condition = {
                        "op": "bool_expr",
                        "args": {
                            "left": {"op": "transform", "args": {"input": get_val, "method": "is_email"}},
                            "right": False,
                            "operator": "==",
                        },
                    }
                    error_msg = "Must be a valid email address."
                elif rule_type == "min_value":
                    n = rule_dict["n"]
                    condition = {
                        "op": "bool_expr",
                        "args": {
                            "left": {"op": "transform", "args": {"input": get_val, "method": "float"}},
                            "right": n,
                            "operator": "<",
                        },
                    }
                    error_msg = f"Must be at least {n}."
                elif rule_type == "max_value":
                    n = rule_dict["n"]
                    condition = {
                        "op": "bool_expr",
                        "args": {
                            "left": {"op": "transform", "args": {"input": get_val, "method": "float"}},
                            "right": n,
                            "operator": ">",
                        },
                    }
                    error_msg = f"Must be at most {n}."
                elif rule_type == "pattern":
                    condition = {
                        "op": "bool_expr",
                        "args": {
                            "left": {
                                "op": "transform",
                                "args": {"input": get_val, "method": "test_pattern", "pattern": rule_dict["regex"]},
                            },
                            "right": False,
                            "operator": "==",
                        },
                    }
                    error_msg = "Does not match required pattern."
                else:
                    continue

                actions.append({
                    "op": "conditional",
                    "args": {
                        "condition": condition,
                        "on_true": {
                            "op": "dom_set_text",
                            "args": {"id": error_id, "text": error_msg},
                        },
                        "on_false": {
                            "op": "dom_set_text",
                            "args": {"id": error_id, "text": ""},
                        },
                    },
                })

        # Build a proper DAP sequence dict (not a string)
        return dScript(data={"op": "sequence", "args": {"actions": actions}})

    def validated_submit(
        self,
        url: str,
        form_data,
        state_property=None,
        on_success=None,
        on_error=None,
        method: str = "POST",
    ) -> 'dScript':
        """
        Validate first, then submit only if all rules pass.

        Runs all validation rules client-side. If any field has an error
        (its ``#{field}-error`` element is non-empty) the submit is skipped.
        Only when every error element is empty does the network request fire.
        """
        # Step 1: clear all error elements, then set them if rules fail
        validate_actions = []

        # First clear all error elements
        for field in self.fields:
            validate_actions.append({
                "op": "dom_set_text",
                "args": {"id": f"{field}-error", "text": ""},
            })

        # Then run each rule — on failure set the error text
        for field, rules in self.fields.items():
            error_id = f"{field}-error"
            # Use the input id matching the field name (e.g. "title" → "#title" or "#title-input")
            # The selector used in did.py is "#new-task-input" but the form field key is "title".
            # We look for an element whose id matches the field name directly, or fall back to
            # the selector stored in form_data if available.
            field_selector = f"#{field}"
            # Try to get the actual selector from form_data if it's a FormData instance
            try:
                from dars.hooks.form_helpers import FormData
                if isinstance(form_data, FormData) and field in form_data.fields:
                    fv = form_data.fields[field]
                    if hasattr(fv, '_to_structure'):
                        struct = fv._to_structure()
                        if isinstance(struct, dict) and struct.get('op') == 'get_dom_value':
                            field_selector = struct['args'].get('selector', field_selector)
                        elif isinstance(struct, dict) and struct.get('op') == 'get_event_property':
                            pass  # keep default
                    elif hasattr(fv, 'selector'):
                        field_selector = fv.selector
            except Exception:
                pass

            get_val = {
                "op": "get_dom_value",
                "args": {"selector": field_selector},
            }

            for rule in rules:
                rule_dict = rule.to_dict()
                if not rule_dict:
                    continue

                rule_type = rule_dict.get("type")

                if rule_type == "required":
                    condition = {
                        "op": "bool_expr",
                        "args": {
                            "left": {"op": "transform", "args": {"input": get_val, "method": "length"}},
                            "right": 0,
                            "operator": "==",
                        },
                    }
                    error_msg = "This field is required."
                elif rule_type == "min_length":
                    n = rule_dict["n"]
                    condition = {
                        "op": "bool_expr",
                        "args": {
                            "left": {"op": "transform", "args": {"input": get_val, "method": "length"}},
                            "right": n,
                            "operator": "<",
                        },
                    }
                    error_msg = f"Must be at least {n} characters."
                elif rule_type == "max_length":
                    n = rule_dict["n"]
                    condition = {
                        "op": "bool_expr",
                        "args": {
                            "left": {"op": "transform", "args": {"input": get_val, "method": "length"}},
                            "right": n,
                            "operator": ">",
                        },
                    }
                    error_msg = f"Must be at most {n} characters."
                elif rule_type == "email":
                    condition = {
                        "op": "bool_expr",
                        "args": {
                            "left": {"op": "transform", "args": {"input": get_val, "method": "is_email"}},
                            "right": False,
                            "operator": "==",
                        },
                    }
                    error_msg = "Must be a valid email address."
                elif rule_type == "min_value":
                    n = rule_dict["n"]
                    condition = {
                        "op": "bool_expr",
                        "args": {
                            "left": {"op": "transform", "args": {"input": get_val, "method": "float"}},
                            "right": n,
                            "operator": "<",
                        },
                    }
                    error_msg = f"Must be at least {n}."
                elif rule_type == "max_value":
                    n = rule_dict["n"]
                    condition = {
                        "op": "bool_expr",
                        "args": {
                            "left": {"op": "transform", "args": {"input": get_val, "method": "float"}},
                            "right": n,
                            "operator": ">",
                        },
                    }
                    error_msg = f"Must be at most {n}."
                elif rule_type == "pattern":
                    condition = {
                        "op": "bool_expr",
                        "args": {
                            "left": {
                                "op": "transform",
                                "args": {"input": get_val, "method": "test_pattern", "pattern": rule_dict["regex"]},
                            },
                            "right": False,
                            "operator": "==",
                        },
                    }
                    error_msg = "Does not match required pattern."
                else:
                    continue

                # Only set error if the error element is currently empty (first failing rule wins)
                validate_actions.append({
                    "op": "conditional",
                    "args": {
                        "condition": {
                            "op": "bool_expr",
                            "args": {
                                "left": {
                                    "op": "bool_expr",
                                    "args": {
                                        "left": condition,
                                        "right": True,
                                        "operator": "==",
                                    },
                                },
                                "right": {
                                    "op": "bool_expr",
                                    "args": {
                                        "left": {
                                            "op": "get_dom_value",
                                            "args": {"selector": f"#{error_id}"},
                                        },
                                        "right": "",
                                        "operator": "==",
                                    },
                                },
                                "operator": "&&",
                            },
                        },
                        "on_true": {
                            "op": "dom_set_text",
                            "args": {"id": error_id, "text": error_msg},
                        },
                    },
                })

        # Step 2: build the submit action
        submit_action = form_data.submit(
            url=url,
            state_property=state_property,
            on_success=on_success,
            on_error=on_error,
            method=method,
        ).data

        # Step 3: check if ALL error elements are empty — only then submit.
        # Build a chain of AND conditions: error1=="" && error2=="" && ...
        error_ids = [f"{field}-error" for field in self.fields]

        def _empty_check(eid):
            return {
                "op": "bool_expr",
                "args": {
                    "left": {
                        "op": "get_dom_value",
                        "args": {"selector": f"#{eid}"},
                    },
                    "right": "",
                    "operator": "==",
                },
            }

        if error_ids:
            all_valid_condition = _empty_check(error_ids[0])
            for eid in error_ids[1:]:
                all_valid_condition = {
                    "op": "bool_expr",
                    "args": {
                        "left": all_valid_condition,
                        "right": _empty_check(eid),
                        "operator": "&&",
                    },
                }
        else:
            # No fields — always submit
            all_valid_condition = {"op": "bool_expr", "args": {"left": True, "right": True, "operator": "=="}}

        conditional_submit = {
            "op": "conditional",
            "args": {
                "condition": all_valid_condition,
                "on_true": submit_action,
            },
        }

        return dScript(data={
            "op": "sequence",
            "args": {
                "actions": validate_actions + [conditional_submit],
            },
        })

    # ------------------------------------------------------------------
    # Rules JSON
    # ------------------------------------------------------------------

    def get_rules_json(self) -> str:
        """
        Return a JSON string of all serialisable rules.

        :class:`CustomRule` entries are omitted (they cannot be transmitted
        to the browser).

        Returns:
            JSON string ``{"field_name": [{"type": "required"}, ...], ...}``
        """
        out: Dict[str, list] = {}
        for field, rules in self.fields.items():
            serialised = [r.to_dict() for r in rules if r.to_dict()]
            if serialised:
                out[field] = serialised
        return json.dumps(out)
