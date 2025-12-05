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
    
    def _generate_collection_code(self) -> str:
        """Generate JavaScript code to collect all form fields into an object."""
        
        def process_value(value_expr, indent_level=1):
            """Recursively process a value, handling V() expressions and nested dicts."""
            indent = "    " * indent_level
            
            # Check if it's a V() expression
            if hasattr(value_expr, '_get_code'):
                # It's a ValueRef or expression with _get_code method
                js_code = value_expr._get_code()
                return f'await {js_code}'
            elif hasattr(value_expr, 'to_dscript'):
                # It's an expression with to_dscript method (BooleanExpression, etc.)
                dscript_obj = value_expr.to_dscript()
                js_code = dscript_obj.code if hasattr(dscript_obj, 'code') else str(dscript_obj)
                return f'await {js_code}'
            elif isinstance(value_expr, dict):
                # It's a nested dictionary - process recursively
                nested_assignments = []
                for nested_key, nested_value in value_expr.items():
                    nested_code = process_value(nested_value, indent_level + 1)
                    nested_assignments.append(f'{indent}    "{nested_key}": {nested_code}')
                return "{\n" + ",\n".join(nested_assignments) + f"\n{indent}}}"
            elif isinstance(value_expr, list):
                # It's a list - process each item
                list_items = []
                for item in value_expr:
                    item_code = process_value(item, indent_level + 1)
                    list_items.append(f'{indent}    {item_code}')
                return "[\n" + ",\n".join(list_items) + f"\n{indent}]"
            else:
                # It's a literal value
                return json.dumps(value_expr)
        
        field_assignments = []
        for field_name, value_expr in self.fields.items():
            value_code = process_value(value_expr, indent_level=2)
            field_assignments.append(f'        "{field_name}": {value_code}')
        
        return "{\n" + ",\n".join(field_assignments) + "\n    }"
    
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
        collection_code = self._generate_collection_code()
        
        js_code = f"""
(async () => {{
    try {{
        const formData = {collection_code};
        alert('{title}:\\n\\n' + JSON.stringify(formData, null, 2));
        console.log('Form data:', formData);
    }} catch (e) {{
        console.error('Form collection error:', e);
        alert('Error collecting form data: ' + e.message);
    }}
}})();
        """.strip()
        
        return dScript(js_code)
    
    def log(self, message: str = "Form Data") -> dScript:
        """
        Generate dScript that logs form data to console.
        
        Args:
            message: Message to log with the data
            
        Returns:
            dScript object that can be used in on_click handlers
            
        Example:
            Button("Log Form", on_click=form_data.log())
        """
        collection_code = self._generate_collection_code()
        
        js_code = f"""
(async () => {{
    try {{
        const formData = {collection_code};
        console.log('{message}:', formData);
    }} catch (e) {{
        console.error('Form collection error:', e);
    }}
}})();
        """.strip()
        
        return dScript(js_code)
    
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
        collection_code = self._generate_collection_code()
        
        js_code = f"""
(async () => {{
    try {{
        const formData = {collection_code};
        const formDataJSON = JSON.stringify(formData, null, 2);
        
        // Update state with the collected data
        let ch = window.__DARS_CHANGE_FN;
        if (!ch) {{
            if (window.Dars && typeof window.Dars.change === 'function') {{
                ch = window.Dars.change.bind(window.Dars);
            }} else {{
                const m = await import('/lib/dars.min.js');
                ch = (m.change || (m.default && m.default.change));
            }}
            if (typeof ch === 'function') window.__DARS_CHANGE_FN = ch;
        }}
        
        if (typeof ch === 'function') {{
            ch({{
                id: '{state_property._state.component.id}',
                dynamic: true,
                {state_property._name}: formDataJSON
            }});
        }}
    }} catch (e) {{
        console.error('Form to state error:', e);
    }}
}})();
        """.strip()
        
        return dScript(js_code)
    
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
        collection_code = self._generate_collection_code()
        
        state_update_code = ""
        if state_property:
            state_update_code = f"""
        
        // Update state with the collected data
        let ch = window.__DARS_CHANGE_FN;
        if (!ch) {{
            if (window.Dars && typeof window.Dars.change === 'function') {{
                ch = window.Dars.change.bind(window.Dars);
            }} else {{
                const m = await import('/lib/dars.min.js');
                ch = (m.change || (m.default && m.default.change));
            }}
            if (typeof ch === 'function') window.__DARS_CHANGE_FN = ch;
        }}
        
        if (typeof ch === 'function') {{
            ch({{
                id: '{state_property._state.component.id}',
                dynamic: true,
                {state_property._name}: formDataJSON
            }});
        }}
            """
        
        js_code = f"""
(async () => {{
    try {{
        const formData = {collection_code};
        const formDataJSON = JSON.stringify(formData, null, 2);
        
        // Show alert
        alert('{title}:\\n\\n' + formDataJSON);
        console.log('Form submitted:', formData);{state_update_code}
    }} catch (e) {{
        console.error('Form submission error:', e);
        alert('Error submitting form: ' + e.message);
    }}
}})();
        """.strip()
        
        return dScript(js_code)
    
    def submit(self, url: str, state_property=None, on_success=None, on_error=None) -> dScript:
        """
        Submit form data to a backend endpoint via POST request using dars.backend.
        
        Args:
            url: Backend endpoint URL (e.g., "http://localhost:3000/submit")
            state_property: Optional state property to save response to
            on_success: Optional dScript to execute on successful submission
            on_error: Optional dScript to execute on error
            
        Returns:
            dScript object that can be used in on_click handlers
            
        Example:
            # Simple submit
            Button("Submit", on_click=form_data.submit("http://localhost:3000/submit"))
            
            # Submit and save response to state
            Button("Submit", on_click=form_data.submit(
                url="http://localhost:3000/submit",
                state_property=form.response
            ))
            
            # Submit with success callback
            Button("Submit", on_click=form_data.submit(
                url="http://localhost:3000/submit",
                on_success=alert("Form submitted successfully!")
            ))
        """
        collection_code = self._generate_collection_code()
        
        # Generate success callback code
        success_code = ""
        if on_success:
            if hasattr(on_success, 'code'):
                success_code = on_success.code
            else:
                success_code = str(on_success)
        
        # Generate error callback code
        error_code = ""
        if on_error:
            if hasattr(on_error, 'code'):
                error_code = on_error.code
            else:
                error_code = str(on_error)
        else:
            error_code = "alert('Error submitting form: ' + error.message);"
        
        # Generate state update code if state_property provided
        state_update_code = ""
        if state_property:
            state_update_code = f"""
        // Update state with response
        let ch = window.__DARS_CHANGE_FN;
        if (!ch) {{
            if (window.Dars && typeof window.Dars.change === 'function') {{
                ch = window.Dars.change.bind(window.Dars);
            }} else {{
                const m = await import('/lib/dars.min.js');
                ch = (m.change || (m.default && m.default.change));
            }}
            if (typeof ch === 'function') window.__DARS_CHANGE_FN = ch;
        }}
        
        if (typeof ch === 'function') {{
            ch({{
                id: '{state_property._state.component.id}',
                dynamic: true,
                {state_property._name}: JSON.stringify(data, null, 2)
            }});
        }}
            """
        
        # Use dars.backend style with operation ID and callback
        js_code = f"""
(async () => {{
    try {{
        const formData = {collection_code};
        
        console.log('Submitting form to {url}:', formData);
        
        // Use fetch directly but in dars.backend style
        const response = await fetch('{url}', {{
            method: 'POST',
            headers: {{
                'Content-Type': 'application/json'
            }},
            body: JSON.stringify(formData)
        }});
        
        if (!response.ok) {{
            throw new Error(`HTTP ${{response.status}}: ${{response.statusText}}`);
        }}
        
        const data = await response.json();
        console.log('Form submission response:', data);
        {state_update_code}
        // Execute success callback
        {success_code}
        
    }} catch (error) {{
        console.error('Form submission error:', error);
        
        // Execute error callback
        {error_code}
    }}
}})();
        """.strip()
        
        return dScript(js_code)


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
