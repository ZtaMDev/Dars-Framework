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

from typing import Dict, Any, Union
from dars.scripts.dscript import dScript
import json


class FormData:
    """
    Pythonic form data collector using V() expressions.
    
    Collects form field values declaratively and generates JavaScript
    to create a JSON object from the form data.
    
    Example:
        form_data = FormData({
            "name": V("#name-input"),
            "email": V("#email-input"),
            "age": V("#age-input").int(),
            "is_premium": V("#premium-checkbox"),
            "discount": (V("#premium-checkbox") == True).then("10%", "0%")
        })
        
        # Show in alert
        Button("Submit", on_click=form_data.alert())
        
        # Save to state
        Button("Submit", on_click=form_data.to_state(form.submitted_data))
        
        # Both alert and save
        Button("Submit", on_click=form_data.submit_and_alert(form.submitted_data))
    """
    
    def __init__(self, fields: Dict[str, Any]):
        """
        Initialize form data collector.
        
        Args:
            fields: Dictionary mapping field names to V() expressions or values
                   Example: {"name": V("#name"), "age": V("#age").int()}
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
            else:
                return value_expr
        
        processed_fields = {k: process_value(v) for k, v in self.fields.items()}
        
        # We need an op that constructs an object from these fields, 
        # but since 'args' in DAP are already an object, 
        # we can just return a structure like { "op": "collect_values", "args": processed_fields }
        # The dispatcher's _resolve will resolve the values in args.
        return {"op": "collect_values", "args": processed_fields}
    
    def alert(self, title: str = "Form Data") -> dScript:
        """
        Generate dScript that shows form data in an alert dialog.
        
        Args:
            title: Title for the alert dialog
            
        Returns:
            dScript object that can be used in on_click handlers
            
        Example:
            Button("Submit", on_click=form_data.alert("Submitted!"))
        """
    def alert(self, title: str = "Form Data") -> dScript:
        """Show form data in alert (secure DAP)."""
        data_struct = self._to_structure()
        # We need to stringify it for alert
        msg = {"op": "transform", "args": {"input": data_struct, "method": "json_stringify"}}
        # But wait, alert takes a string. We can prepend title. 
        # We might need 'string_concat' op.
        full_msg = {"op": "string_concat", "args": {"parts": [title + ":\n\n", msg]}}
        
        # dScript supports data directly
        from dars.actionProtocol import Action
        return dScript(data=Action.alert(message=full_msg))

    def log(self, message: str = "Form Data") -> dScript:
        """Log form data to console (secure DAP)."""
        # console.log can take objects directly, so no need for stringify
        # But Action.log takes a message. DAP dispatcher console.log(args.message).
        # If args.message is an object, it logs the object.
        data_struct = self._to_structure()
        # To log "Message: Object", we might want separate args or formatted log. 
        # Current Action.log only has message. 
        # I'll create a list/array for log? DAP log support usually implies single message. 
        # If I return an array [msg, data_struct], console.log might print it as array.
        # Let's stringify for now or assume DAP log handles it.
        # Given js_lib console.log(args.message), if message is resolved to an object, it logs the object.
        # But we want "Message: Object". 
        # I'll stick to logging the object for now, or just tuple?
        # Let's log the object directly.
        from dars.actionProtocol import Action
        return dScript(data=Action.log(message=data_struct))
    
    def to_state(self, state_property) -> dScript:
        """
        Generate dScript that saves form data to a state property.
        
        Args:
            state_property: State property to save to (e.g., form.submitted_data)
            
        Returns:
            dScript object that can be used in on_click handlers
            
        Example:
            Button("Submit", on_click=form_data.to_state(form.submitted_data))
        """
    def to_state(self, state_property) -> dScript:
        """Save form data to state (secure DAP)."""
        data_struct = self._to_structure()
        # State.change takes stringified values for 'dynamic' changes usually, but 
        # if the change handler supports objects, we can pass object.
        # js_lib.py change op: window.Dars.change(args).
        # args usually is { id: ..., values: ... }.
        # The previous code stringified it: {state_property._name}: formDataJSON
        # So we should stringify it.
        json_data = {"op": "transform", "args": {"input": data_struct, "method": "json_stringify"}}
        
        from dars.actionProtocol import Action
        # We need to construct the change action manually or use Action.change
        # Action.state_set_value? 
        # state_property is a ValueRef or similar.
        # state_property._state.component.id 
        # state_property._name
        
        change_args = {
            "id": state_property._state.component.id,
            "dynamic": True,
            state_property._name: json_data
        }
        
        return dScript(data=Action.change(change_args))
    
    def submit_and_alert(self, state_property=None, title: str = "Form Submitted") -> dScript:
        """
        Generate dScript that shows alert AND optionally saves to state.
        
        Args:
            state_property: Optional state property to save to
            title: Title for the alert dialog
            
        Returns:
            dScript object that can be used in on_click handlers
            
        Example:
            # Alert only
            Button("Submit", on_click=form_data.submit_and_alert())
            
            # Alert and save to state
            Button("Submit", on_click=form_data.submit_and_alert(form.submitted_data))
        """
    def submit(self, url: str, state_property=None, on_success=None, on_error=None) -> dScript:
        """Submit form data to ID (secure DAP)."""
        data_struct = self._to_structure()
        
        # Helper to convert callback to structure
        def _to_action(act):
            if hasattr(act, 'get_action'): return act.get_action()
            if hasattr(act, 'code'): return {"op": "inline", "args": {"code": act.code}}
            if isinstance(act, str): return {"op": "inline", "args": {"code": act}}
            return act

        # We use a new op 'network_request' (or 'fetch')
        # We need to update ActionProtocol and js_lib.py
        # For now, I'll generate the structure directly assuming support.
        
        fetch_args = {
            "url": url,
            "method": "POST",
            "headers": {"Content-Type": "application/json"},
            "body": {"op": "transform", "args": {"input": data_struct, "method": "json_stringify"}}
        }
        
        success_actions = []
        if state_property:
             # Save response to state
             # Response data is available in 'last_response'? Or passed as arg?
             # This is tricky with DAP. 'fetch' usually returns response.
             # We might need 'fetch' to set a variable in context or pass result to 'on_success'.
             # Or 'network_request' op takes 'on_success' action and passes data as context variable.
             # Let's assume on_success actions have access to 'data' in context or we specifically set state with 'response_data'.
             # I'll usage a special value "get_context_value", arg "response_data".
             # This requires 'get_context_value' op.
             response_val = {"op": "get_context_value", "args": {"key": "response_data"}}
             json_data = {"op": "transform", "args": {"input": response_val, "method": "json_stringify"}}
             
             change_args = {
                "id": state_property._state.component.id,
                "dynamic": True,
                state_property._name: json_data
             }
             success_actions.append({"op": "change", "args": change_args})

        if on_success:
            success_actions.append(_to_action(on_success))
            
        error_actions = []
        if on_error:
            error_actions.append(_to_action(on_error))
        else:
            # Default error alert
            error_actions.append({"op": "alert", "args": {"message": "Error submitting form"}})

        return dScript(data={
            "op": "network_request",
            "args": {
                "url": url,
                "method": "POST",
                "headers": {"Content-Type": "application/json"},
                "body": {"op": "transform", "args": {"input": data_struct, "method": "json_stringify"}},
                "on_success": {"op": "sequence", "args": {"actions": success_actions}},
                "on_error": {"op": "sequence", "args": {"actions": error_actions}}
            }
        })

    def submit_and_alert(self, state_property=None, title: str = "Form Submitted") -> dScript:
        """Submit and alert (secure DAP)."""
        data_struct = self._to_structure()
        msg = {"op": "transform", "args": {"input": data_struct, "method": "json_stringify"}}
        full_msg = {"op": "string_concat", "args": {"parts": [title + ":\n\n", msg]}}
        
        actions = []
        actions.append({"op": "alert", "args": {"message": full_msg}})
        actions.append({"op": "log", "args": {"message": data_struct}})
        
        if state_property:
             json_data = {"op": "transform", "args": {"input": data_struct, "method": "json_stringify"}}
             change_args = {
                "id": state_property._state.component.id,
                "dynamic": True,
                state_property._name: json_data
             }
             actions.append({"op": "change", "args": change_args})
             
        from dars.actionProtocol import Action
        return dScript(data=Action.sequence(actions))


def collect_form(*fields, **kwargs) -> FormData:
    """
    Helper function to create a FormData collector.
    
    Args:
        *fields: Tuples of (name, V_expression)
        **kwargs: Alternative dict-style syntax
        
    Returns:
        FormData instance
        
    Example:
        # Using tuples
        form = collect_form(
            ("name", V("#name-input")),
            ("email", V("#email-input")),
            ("age", V("#age-input").int())
        )
        
        # Using kwargs (cleaner!)
        form = collect_form(
            name=V("#name-input"),
            email=V("#email-input"),
            age=V("#age-input").int(),
            is_premium=V("#premium-checkbox"),
            discount=(V("#premium-checkbox") == True).then("10%", "0%")
        )
    """
    if kwargs:
        # Using kwargs syntax
        return FormData(kwargs)
    elif len(fields) == 1 and isinstance(fields[0], dict):
        # Using dict
        return FormData(fields[0])
    else:
        # Using tuples
        field_dict = {name: expr for name, expr in fields}
        return FormData(field_dict)
