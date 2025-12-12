# Dars Framework - Core Source File
#
# This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0.
# If a copy of the MPL was not distributed with this file, You can obtain one at
# https://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2025 ZtaDev
"""Utility functions for creating common dScript patterns"""
from dars.scripts.dscript import dScript
from typing import Union


# ============= Modal Utilities =============

def showModal(id: str) -> dScript:
    """
    Returns a dScript that shows a Dars Modal component.
    
    Args:
        id: The ID of the modal component to show
             
    Example:
        Button("Open Modal", on_click=showModal(id="my-modal"))
    """
    code = f"const m = document.getElementById('{id}'); m.removeAttribute('hidden'); m.classList.remove('dars-modal-hidden'); m.style.display = 'flex';"
    return dScript(code)


def hideModal(id: str) -> dScript:
    """
    Returns a dScript that hides a Dars Modal component.
    
    Args:
        id: The ID of the modal component to hide
        
    Example:
        Button("Close Modal", on_click=hideModal(id="my-modal"))
    """
    code = f"const m = document.getElementById('{id}'); m.setAttribute('hidden', ''); m.classList.add('dars-modal-hidden'); m.style.display = 'none';"
    return dScript(code)


# ============= Navigation Utilities =============

def goTo(href: str) -> dScript:
    """
    Navigate to a URL in the current tab.
    
    Args:
        href: The URL to navigate to
        
    Example:
        Button("Go Home", on_click=goTo(href="/"))
    """
    code = f"window.location.href = '{href}';"
    return dScript(code)


def goToNew(href: str) -> dScript:
    """
    Open a URL in a new tab.
    
    Args:
        href: The URL to open in a new tab
        
    Example:
        Button("Open in New Tab", on_click=goToNew(href="https://example.com"))
    """
    code = f"window.open('{href}', '_blank');"
    return dScript(code)


def reload() -> dScript:
    """
    Reload the current page.
    
    Example:
        Button("Refresh", on_click=reload())
    """
    return dScript("window.location.reload();")


def goBack() -> dScript:
    """
    Navigate back in browser history.
    
    Example:
        Button("Back", on_click=goBack())
    """
    return dScript("window.history.back();")


def goForward() -> dScript:
    """
    Navigate forward in browser history.
    
    Example:
        Button("Forward", on_click=goForward())
    """
    return dScript("window.history.forward();")


# ============= Alert & Console Utilities =============

def alert(message: Union[str, 'ValueRef']) -> dScript:
    """
    Show a browser alert dialog.
    
    Args:
        message: The message to display (string or ValueRef from V())
        
    Example:
        Button("Alert", on_click=alert(message="Hello World!"))
        Button("Alert from State", on_click=alert(V("user.name")))
        Button("Alert from Input", on_click=alert(V("#myInput")))
    """
    from dars.hooks.value_helpers import ValueRef
    
    if isinstance(message, ValueRef):
        return dScript(f"(async () => {{ alert(await {message._get_code()}); }})();")
    else:
        escaped_message = message.replace("'", "\\'")
        return dScript(f"alert('{escaped_message}');")


def confirm(message: str, on_ok: str = "", on_cancel: str = "") -> dScript:
    """
    Show a browser confirm dialog with optional callbacks.
    
    Args:
        message: The message to display
        on_ok: JavaScript code to execute if user clicks OK
        on_cancel: JavaScript code to execute if user clicks Cancel
        
    Example:
        Button("Delete", on_click=confirm(
            message="Are you sure?",
            on_ok="console.log('Deleted')",
            on_cancel="console.log('Cancelled')"
        ))
    """
    escaped_message = message.replace("'", "\\'")
    if on_ok or on_cancel:
        code = f"if (confirm('{escaped_message}')) {{ {on_ok} }} else {{ {on_cancel} }}"
    else:
        code = f"confirm('{escaped_message}');"
    return dScript(code)


def log(message: Union[str, 'ValueRef']) -> dScript:
    """
    Log a message to the browser console.
    
    Args:
        message: The message to log (string or ValueRef from V())
        
    Example:
        Button("Log", on_click=log(message="Button clicked"))
        Button("Log State", on_click=log(V("cart.total")))
    """
    from dars.hooks.value_helpers import ValueRef
    
    if isinstance(message, ValueRef):
        return dScript(f"(async () => {{ console.log(await {message._get_code()}); }})();")
    else:
        escaped_message = message.replace("'", "\\'")
        return dScript(f"console.log('{escaped_message}');")

def getDateTime(format: str = "iso") -> 'ValueRef':
    """
    Get current date/time as a ValueRef for use in forms and state.
    
    This returns a special ValueRef that resolves to the current date/time
    on the client side when the form is submitted or state is updated.
    
    Args:
        format: Format of the datetime string
               - "iso" (default): ISO 8601 format (e.g., "2025-12-04T21:53:49.123Z")
               - "locale": Localized format (e.g., "12/4/2025, 9:53:49 PM")
               - "date": Date only (e.g., "12/4/2025")
               - "time": Time only (e.g., "9:53:49 PM")
               - "timestamp": Unix timestamp in milliseconds
        
    Returns:
        ValueRef that resolves to current datetime
        
    Example:
        # In form collection
        form_data = collect_form(
            name=V("#name"),
            submitted_at=getDateTime()  # ISO format
        )
        
        # Different formats
        collect_form(
            created_at=getDateTime("iso"),
            display_date=getDateTime("locale"),
            date_only=getDateTime("date"),
            time_only=getDateTime("time"),
            timestamp=getDateTime("timestamp")
        )
        
        # In state updates
        Button("Save", on_click=state.last_updated.set(getDateTime()))
    """
    from dars.hooks.value_helpers import ValueRef
    
    # Create a special ValueRef that generates datetime code
    class DateTimeRef(ValueRef):
        def __init__(self, format_type: str):
            # Don't call super().__init__ since we don't have a selector
            self.selector = None
            self.format_type = format_type
            self._transform = None
        
        def _get_code(self) -> str:
            """Generate JavaScript code to get current datetime."""
            if self.format_type == "iso":
                return "(new Date().toISOString())"
            elif self.format_type == "locale":
                return "(new Date().toLocaleString())"
            elif self.format_type == "date":
                return "(new Date().toLocaleDateString())"
            elif self.format_type == "time":
                return "(new Date().toLocaleTimeString())"
            elif self.format_type == "timestamp":
                return "(Date.now())"
            else:
                # Default to ISO
                return "(new Date().toISOString())"
    
    return DateTimeRef(format)

# ============= DOM Manipulation Utilities =============

def show(id: str) -> dScript:
    """
    Show an element by setting display to block.
    
    Args:
        id: The ID of the element to show
        
    Example:
        Button("Show", on_click=show(id="my-element"))
    """
    return dScript(f"document.getElementById('{id}').style.display = 'block';")


def hide(id: str) -> dScript:
    """
    Hide an element by setting display to none.
    
    Args:
        id: The ID of the element to hide
        
    Example:
        Button("Hide", on_click=hide(id="my-element"))
    """
    return dScript(f"document.getElementById('{id}').style.display = 'none';")


def toggle(id: str) -> dScript:
    """
    Toggle an element's visibility.
    
    Args:
        id: The ID of the element to toggle
        
    Example:
        Button("Toggle", on_click=toggle(id="my-element"))
    """
    code = f"const el = document.getElementById('{id}'); el.style.display = el.style.display === 'none' ? 'block' : 'none';"
    return dScript(code)


def setText(id: str, text: Union[str, 'ValueRef']) -> dScript:
    """
    Set the text content of an element.
    
    Args:
        id: The ID of the element
        text: The new text content (string or ValueRef from V())
        
    Example:
        Button("Update", on_click=setText(id="status", text="Done!"))
        Button("Copy State", on_click=setText(id="display", text=V("user.name")))
    """
    from dars.hooks.value_helpers import ValueRef
    
    if isinstance(text, ValueRef):
        return dScript(f"(async () => {{ document.getElementById('{id}').textContent = await {text._get_code()}; }})();")
    else:
        escaped_text = text.replace("'", "\\'")
        return dScript(f"document.getElementById('{id}').textContent = '{escaped_text}';")


def addClass(id: str, class_name: str) -> dScript:
    """
    Add a CSS class to an element.
    
    Args:
        id: The ID of the element
        class_name: The class name to add
        
    Example:
        Button("Highlight", on_click=addClass(id="text", class_name="highlight"))
    """
    return dScript(f"document.getElementById('{id}').classList.add('{class_name}');")


def removeClass(id: str, class_name: str) -> dScript:
    """
    Remove a CSS class from an element.
    
    Args:
        id: The ID of the element
        class_name: The class name to remove
        
    Example:
        Button("Remove", on_click=removeClass(id="text", class_name="highlight"))
    """
    return dScript(f"document.getElementById('{id}').classList.remove('{class_name}');")


def toggleClass(id: str, class_name: str) -> dScript:
    """
    Toggle a CSS class on an element.
    
    Args:
        id: The ID of the element
        class_name: The class name to toggle
        
    Example:
        Button("Toggle", on_click=toggleClass(id="text", class_name="active"))
    """
    return dScript(f"document.getElementById('{id}').classList.toggle('{class_name}');")


# ============= Scroll Utilities =============

def scrollTo(x: int = 0, y: int = 0) -> dScript:
    """
    Scroll the window to a specific position.
    
    Args:
        x: Horizontal scroll position in pixels
        y: Vertical scroll position in pixels
        
    Example:
        Button("Top", on_click=scrollTo(x=0, y=0))
    """
    return dScript(f"window.scrollTo({x}, {y});")


def scrollToTop() -> dScript:
    """
    Scroll to the top of the page smoothly.
    
    Example:
        Button("To Top", on_click=scrollToTop())
    """
    return dScript("window.scrollTo({ top: 0, behavior: 'smooth' });")


def scrollToBottom() -> dScript:
    """
    Scroll to the bottom of the page smoothly.
    
    Example:
        Button("To Bottom", on_click=scrollToBottom())
    """
    return dScript("window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' });")


def scrollToElement(id: str) -> dScript:
    """
    Scroll to a specific element smoothly.
    
    Args:
        id: The ID of the element to scroll to
        
    Example:
        Button("Go to Section", on_click=scrollToElement(id="section-2"))
    """
    return dScript(f"document.getElementById('{id}').scrollIntoView({{ behavior: 'smooth' }});")


# ============= Form Utilities =============

def submitForm(form_id: str) -> dScript:
    """
    Submit a form programmatically.
    
    Args:
        form_id: The ID of the form to submit
        
    Example:
        Button("Submit", on_click=submitForm(form_id="my-form"))
    """
    return dScript(f"document.getElementById('{form_id}').submit();")


def resetForm(form_id: str) -> dScript:
    """
    Reset a form to its initial values.
    
    Args:
        form_id: The ID of the form to reset
        
    Example:
        Button("Reset", on_click=resetForm(form_id="my-form"))
    """
    return dScript(f"document.getElementById('{form_id}').reset();")


def getValue(input_id: str, target_id: str) -> dScript:
    """
    Get the value from an input and set it to another element.
    
    Args:
        input_id: The ID of the input element
        target_id: The ID of the element to update
        
    Example:
        Button("Copy", on_click=getValue(input_id="input1", target_id="output"))
    """
    code = f"document.getElementById('{target_id}').textContent = document.getElementById('{input_id}').value;"
    return dScript(code)


def clearInput(input_id: str) -> dScript:
    """
    Clear an input field.
    
    Args:
        input_id: The ID of the input to clear
        
    Example:
        Button("Clear", on_click=clearInput(input_id="search"))
    """
    return dScript(f"document.getElementById('{input_id}').value = '';")


# ============= Storage Utilities =============

def saveToLocal(key: str, value: str) -> dScript:
    """
    Save a value to localStorage.
    
    Args:
        key: The storage key
        value: The value to store
        
    Example:
        Button("Save", on_click=saveToLocal(key="username", value="john"))
    """
    escaped_value = value.replace("'", "\\'")
    return dScript(f"localStorage.setItem('{key}', '{escaped_value}');")


def loadFromLocal(key: str, target_id: str) -> dScript:
    """
    Load a value from localStorage and display it.
    
    Args:
        key: The storage key
        target_id: The ID of the element to update with the value
        
    Example:
        Button("Load", on_click=loadFromLocal(key="username", target_id="display"))
    """
    code = f"const val = localStorage.getItem('{key}'); if (val) document.getElementById('{target_id}').textContent = val;"
    return dScript(code)


def removeFromLocal(key: str) -> dScript:
    """
    Remove a value from localStorage.
    
    Args:
        key: The storage key to remove
        
    Example:
        Button("Clear Storage", on_click=removeFromLocal(key="username"))
    """
    return dScript(f"localStorage.removeItem('{key}');")


def clearLocalStorage() -> dScript:
    """
    Clear all localStorage data.
    
    Example:
        Button("Clear All", on_click=clearLocalStorage())
    """
    return dScript("localStorage.clear();")


# ============= Clipboard Utilities =============

def copyToClipboard(text: Union[str, 'ValueRef']) -> dScript:
    """
    Copy text to clipboard.
    
    Args:
        text: The text to copy (string or ValueRef from V())
        
    Example:
        Button("Copy", on_click=copyToClipboard(text="Hello World"))
        Button("Copy State", on_click=copyToClipboard(V("user.email")))
        Button("Copy Input", on_click=copyToClipboard(V("#myInput")))
    """
    from dars.hooks.value_helpers import ValueRef
    
    if isinstance(text, ValueRef):
        return dScript(f"(async () => {{ const val = await {text._get_code()}; navigator.clipboard.writeText(String(val)).catch(err => console.error('Copy failed:', err)); }})();")
    else:
        escaped_text = text.replace("'", "\\'")
        return dScript(f"navigator.clipboard.writeText('{escaped_text}').catch(err => console.error('Copy failed:', err));")


def copyElementText(id: str) -> dScript:
    """
    Copy the text content of an element to clipboard.
    
    Args:
        id: The ID of the element whose text to copy
        
    Example:
        Button("Copy Code", on_click=copyElementText(id="code-block"))
    """
    code = f"const text = document.getElementById('{id}').textContent; navigator.clipboard.writeText(text).catch(err => console.error('Copy failed:', err));"
    return dScript(code)


# ============= Focus Utilities =============

def focus(id: str) -> dScript:
    """
    Set focus on an element.
    
    Args:
        id: The ID of the element to focus
        
    Example:
        Button("Focus Input", on_click=focus(id="search-input"))
    """
    return dScript(f"document.getElementById('{id}').focus();")


def blur(id: str) -> dScript:
    """
    Remove focus from an element.
    
    Args:
        id: The ID of the element to blur
        
    Example:
        Button("Blur", on_click=blur(id="input"))
    """
    return dScript(f"document.getElementById('{id}').blur();")


# ============= Keyboard Event Utilities =============

def switch(cases: dict, default=None) -> dScript:
    """
    Create a switch-case statement for keyboard events.
    
    Works with KeyCode constants for clean keyboard handling.
    Supports both single actions and lists of actions.
    
    Args:
        cases: Dictionary mapping key codes to dScript actions (or lists of dScript)
        default: Optional default dScript action if no case matches
        
    Example:
        from dars.scripts.keycode import KeyCode
        
        # Single actions
        Input(on_key_down=switch({
            KeyCode.ENTER: log("Enter pressed"),
            KeyCode.ESCAPE: alert("Escape pressed"),
            KeyCode.TAB: focus("next-input")
        }))
        
        # Multiple actions per key
        Input(on_key_down=switch({
            KeyCode.ENTER: [
                formState.message.set("Submitted!"),
                alert("Done!")
            ],
            KeyCode.ESCAPE: [
                clearInput("username"),
                clearInput("password")
            ]
        }))
    """
    def extract_code(action):
        """Helper to extract JavaScript code from action"""
        if hasattr(action, 'code'):
            return action.code
        elif hasattr(action, 'get_code'):
            return action.get_code()
        else:
            return str(action)
    
    conditions = []
    
    for key_code, action in cases.items():
        # Handle lists of actions
        if isinstance(action, list):
            action_codes = [extract_code(act) for act in action]
            action_code = ' '.join(action_codes)
        else:
            # Single action
            action_code = extract_code(action)
        
        conditions.append(f"if (event.key === '{key_code}') {{ {action_code} }}")
    
    # Add default case if provided
    if default:
        if isinstance(default, list):
            default_codes = [extract_code(act) for act in default]
            default_code = ' '.join(default_codes)
        else:
            default_code = extract_code(default)
        conditions.append(f"else {{ {default_code} }}")
    
    return dScript(' else '.join(conditions))


# ============= Timer Utilities =============

def setTimeout(delay: int, code: dScript) -> dScript:
    """
    Set a timeout to execute a script after a delay.
    
    Args:
        code: The script to execute
        delay: The delay in milliseconds
        
    Example:
        Button("Delayed Action", on_click=setTimeout(code=alert('Delayed!'), delay=2000))
    """
    return dScript(f"new Promise(resolve => {{ const _self=this; const _ev=typeof event!=='undefined'?event:null; setTimeout(() => {{ (function(event){{ {code.code} }}).call(_self, _ev); resolve(); }}, {delay}); }})")


def getInputValue(input_id: str, parent_id: str = None) -> dScript:
    """
    Get the value from an input element (for use with State.set()).
    
    This returns a JavaScript expression that evaluates to the input's value,
    which can be used with State.set() or other dynamic operations.
    
    Args:
        input_id: The ID of the input element
        parent_id: Optional parent container ID to search within
        
    Example:
        # Use with State.set()
        state.name.set(getInputValue("username"))
        
        # With parent container
        state.email.set(getInputValue("email", parent_id="modal"))
    """
    if parent_id:
        code = f"document.getElementById('{parent_id}').querySelector('#{input_id}').value"
    else:
        code = f"document.getElementById('{input_id}').value"
    return dScript(code)