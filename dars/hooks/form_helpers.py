# Dars Framework - Core Source File
#
# This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0.
# If a copy of the MPL was not distributed with this file, You can obtain one at
# https://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2025 ZtaDev
"""
Form data collection utilities using V() expressions.

Provides Pythonic helpers for collecting and submitting form data
without writing raw JavaScript.
"""

from typing import Dict, Any
from dars.scripts.dscript import dScript


class FormData:
    """
    Pythonic form data collector using V() expressions.

    Collects form field values declaratively and generates DAP payloads
    to create a JSON object from the form data.

    Example:
        form_data = FormData({
            "name": V("#name-input"),
            "email": V("#email-input"),
            "age": V("#age-input").int(),
        })

        Button("Submit", on_click=form_data.alert())
        Button("Submit", on_click=form_data.to_state(form.submitted_data))
        Button("Submit", on_click=form_data.submit_and_alert(form.submitted_data))
    """

    def __init__(self, fields: Dict[str, Any]):
        """
        Initialize form data collector.

        Args:
            fields: Dictionary mapping field names to V() expressions or values.
        """
        self.fields = fields

    def _to_structure(self) -> dict:
        """Generate DAP structure for the form data object."""

        def process_value(value_expr):
            if hasattr(value_expr, '_to_structure'):
                return value_expr._to_structure()
            elif isinstance(value_expr, dict):
                return {k: process_value(v) for k, v in value_expr.items()}
            elif isinstance(value_expr, list):
                return [process_value(v) for v in value_expr]
            return value_expr

        processed_fields = {k: process_value(v) for k, v in self.fields.items()}
        return {"op": "collect_values", "args": processed_fields}

    def alert(self, title: str = "Form Data") -> dScript:
        """
        Show form data in an alert dialog.

        Args:
            title: Title prefix shown before the form data.

        Returns:
            dScript encoding a DAP ``alert`` action.
        """
        data_struct = self._to_structure()
        msg = {"op": "transform", "args": {"input": data_struct, "method": "json_stringify"}}
        full_msg = {"op": "string_concat", "args": {"parts": [title + ":\n\n", msg]}}
        from dars.actionProtocol import Action
        return dScript(data=Action.alert(message=full_msg))

    def log(self, message: str = "Form Data") -> dScript:
        """
        Log form data to the browser console.

        Args:
            message: Label shown before the data object.

        Returns:
            dScript encoding a DAP ``log`` action.
        """
        data_struct = self._to_structure()
        from dars.actionProtocol import Action
        return dScript(data=Action.log(message=data_struct))

    def to_state(self, state_property) -> dScript:
        """
        Save form data to a state property.

        Args:
            state_property: State property to write to (e.g. ``form.submitted_data``).

        Returns:
            dScript encoding a DAP ``change`` action.
        """
        data_struct = self._to_structure()
        json_data = {"op": "transform", "args": {"input": data_struct, "method": "json_stringify"}}
        change_args = {
            "id": state_property._state.component.id,
            "dynamic": True,
            state_property._name: json_data,
        }
        from dars.actionProtocol import Action
        return dScript(data=Action.change(change_args))

    def submit(
        self,
        url: str,
        state_property=None,
        on_success=None,
        on_error=None,
        method: str = "POST",
    ) -> dScript:
        """
        Submit form data to a URL via POST.

        Args:
            url: Endpoint to POST the JSON payload to.
            state_property: Optional state property to store the response in.
            on_success: Optional dScript executed on a successful response.
            on_error: Optional dScript executed on a failed response.

        Returns:
            dScript encoding a DAP ``network_request`` action.
        """
        data_struct = self._to_structure()

        def _to_action(act):
            if hasattr(act, 'get_action'):
                return act.get_action()
            if hasattr(act, 'code'):
                return {"op": "inline", "args": {"code": act.code}}
            if isinstance(act, str):
                return {"op": "inline", "args": {"code": act}}
            return act

        success_actions = []
        if state_property:
            response_val = {"op": "get_context_value", "args": {"key": "response_data"}}
            json_data = {"op": "transform", "args": {"input": response_val, "method": "json_stringify"}}
            change_args = {
                "id": state_property._state.component.id,
                "dynamic": True,
                state_property._name: json_data,
            }
            success_actions.append({"op": "change", "args": change_args})
        if on_success:
            success_actions.append(_to_action(on_success))

        error_actions = []
        if on_error:
            error_actions.append(_to_action(on_error))
        else:
            error_actions.append({"op": "alert", "args": {"message": "Error submitting form"}})

        return dScript(data={
            "op": "network_request",
            "args": {
                "url": url,
                "method": method,
                "headers": {"Content-Type": "application/json"},
                "body": {
                    "op": "transform",
                    "args": {"input": data_struct, "method": "json_stringify"},
                },
                "on_success": {"op": "sequence", "args": {"actions": success_actions}},
                "on_error": {"op": "sequence", "args": {"actions": error_actions}},
            },
        })

    def submit_and_alert(
        self,
        state_property=None,
        title: str = "Form Submitted",
    ) -> dScript:
        """
        Show an alert with the form data and optionally save it to state.

        Args:
            state_property: Optional state property to write to.
            title: Title prefix shown in the alert.

        Returns:
            dScript encoding a DAP ``sequence`` action.
        """
        data_struct = self._to_structure()
        msg = {"op": "transform", "args": {"input": data_struct, "method": "json_stringify"}}
        full_msg = {"op": "string_concat", "args": {"parts": [title + ":\n\n", msg]}}

        actions = [
            {"op": "alert", "args": {"message": full_msg}},
            {"op": "log", "args": {"message": data_struct}},
        ]

        if state_property:
            json_data = {"op": "transform", "args": {"input": data_struct, "method": "json_stringify"}}
            change_args = {
                "id": state_property._state.component.id,
                "dynamic": True,
                state_property._name: json_data,
            }
            actions.append({"op": "change", "args": change_args})

        return dScript(data={"op": "sequence", "args": {"actions": actions}})


def collect_form(*fields, **kwargs) -> FormData:
    """
    Convenience constructor for :class:`FormData`.

    Accepts either keyword arguments or positional ``(name, expr)`` tuples.

    Example::

        form = collect_form(
            name=V("#name-input"),
            email=V("#email-input"),
            age=V("#age-input").int(),
        )
    """
    if kwargs:
        return FormData(kwargs)
    if len(fields) == 1 and isinstance(fields[0], dict):
        return FormData(fields[0])
    return FormData({name: expr for name, expr in fields})
