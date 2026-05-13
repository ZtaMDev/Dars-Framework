# Dars Framework - Core Source File
#
# This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0.
# If a copy of the MPL was not distributed with this file, You can obtain one at
# https://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2025 ZtaDev
"""Utility functions for creating common dScript patterns using secure DAP actions."""
from dars.scripts.dscript import dScript, RawJS
from dars.actionProtocol import Action
from typing import Union, List


# ============= Modal Utilities =============

def showModal(id: str) -> RawJS:
    """
    Returns a RawJS action that shows a Dars Modal component.
    
    This function triggers the `modal_show` command in the DAP registry, 
    making the specified modal element visible.
    
    Args:
        id (str): The DOM ID of the Modal component to show.
        
    Returns:
        RawJS: The compiled action object ready to be used in an event handler.
        
    Example:
        ```python
        # Button that opens a settings modal
        Button("Settings", on_click=showModal("settings_modal"))
        ```
    """
    return RawJS(code=Action.modal_show(id))


def hideModal(id: str) -> RawJS:
    """
    Returns a RawJS action that hides a Dars Modal component.
    
    This function triggers the `modal_hide` command in the DAP registry, 
    hiding the specified modal element.
    
    Args:
        id (str): The DOM ID of the Modal component to hide.
        
    Returns:
        RawJS: The compiled action object ready to be used in an event handler.
        
    Example:
        ```python
        # Button inside the modal to close it
        Button("Close", on_click=hideModal("settings_modal"))
        ```
    """
    return RawJS(code=Action.modal_hide(id))


# ============= Navigation Utilities =============

def goTo(href: str) -> RawJS:
    """
    Navigate to a URL in the current tab.
    
    This command updates `window.location.href` to the specified URL.
    
    Args:
        href (str): The target URL or path to navigate to.
        
    Returns:
        RawJS: The compiled navigation action.
        
    Example:
        ```python
        Button("Go to Dashboard", on_click=goTo("/dashboard"))
        ```
    """
    return RawJS(code=Action.navigate(href))


def goToNew(href: str) -> RawJS:
    """
    Open a URL in a new browser tab.
    
    This command uses `window.open(href, '_blank')` to open the URL.
    
    Args:
        href (str): The target URL to open.
        
    Returns:
        RawJS: The compiled navigation action.
        
    Example:
        ```python
        Button("Open Docs", on_click=goToNew("https://docs.dars.dev"))
        ```
    """
    return RawJS(code=Action.navigate_new(href))


def reload() -> RawJS:
    """
    Reload the current page.
    
    Returns:
        RawJS: The compiled reload action.
        
    Example:
        ```python
        Button("Refresh Page", on_click=reload())
        ```
    """
    return RawJS(code=Action.reload())


def goBack() -> RawJS:
    """
    Navigate back in the browser history.
    
    Returns:
        RawJS: The compiled history_back action.
        
    Example:
        ```python
        Button("Back", on_click=goBack())
        ```
    """
    return RawJS(code=Action.history_back())


def goForward() -> RawJS:
    """
    Navigate forward in the browser history.
    
    Returns:
        RawJS: The compiled history_forward action.
        
    Example:
        ```python
        Button("Forward", on_click=goForward())
        ```
    """
    return RawJS(code=Action.history_forward())


# ============= Alert & Console Utilities =============

def alert(message: Union[str, 'ValueRef']) -> RawJS:
    """
    Show a browser alert dialog.
    
    Args:
        message (str | ValueRef): The message to display in the alert. Can be a literal string 
                                  or a dynamic `ValueRef` (e.g., `V(".input-field")`).
        
    Returns:
        RawJS: The compiled alert action.
        
    Example:
        ```python
        # Static message
        Button("Say Hello", on_click=alert("Hello, World!"))
        
        # Dynamic message using ValueRef
        Button("Show Input", on_click=alert(V("#name_input")))
        ```
    """
    from dars.hooks.value_helpers import ValueRef
    if isinstance(message, ValueRef):
        return RawJS(code=Action.alert(message=RawJS(message._get_code())))
    else:
        return RawJS(code=Action.alert(message=message))


def confirm(message: str, on_ok: Union[str, dScript, RawJS] = None, on_cancel: Union[str, dScript, RawJS] = None) -> RawJS:
    """
    Show a browser confirm dialog with optional callbacks for OK and Cancel.
    
    Args:
        message (str): The question or statement to show to the user.
        on_ok (Union[str, dScript, RawJS], optional): Action to execute if the user clicks OK.
        on_cancel (Union[str, dScript, RawJS], optional): Action to execute if the user clicks Cancel.
        
    Returns:
        RawJS: The compiled confirm dialog logic.
        
    Example:
        ```python
        Button(
            "Delete Item", 
            on_click=confirm(
                "Are you sure you want to delete this?", 
                on_ok=updateVRef("#status", "Deleted!"),
                on_cancel=alert("Action canceled")
            )
        )
        ```
    """
    import json
    def _to_code(act):
        if act is None: return ""
        if isinstance(act, RawJS): return act.code
        if hasattr(act, "get_code"): return act.get_code()
        return str(act)

    return RawJS(code=f"""
    if (confirm({json.dumps(message)})) {{
        {_to_code(on_ok)}
    }} else {{
        {_to_code(on_cancel)}
    }}
    """)


def log(message: Union[str, 'ValueRef']) -> RawJS:
    """
    Log a message to the browser console.
    
    Args:
        message (str | ValueRef): The message to log. Can be a static string or a dynamic `ValueRef`.
        
    Returns:
        RawJS: The compiled console.log action.
        
    Example:
        ```python
        Button("Debug", on_click=log("Button was clicked!"))
        Button("Log Input", on_click=log(V("#username")))
        ```
    """
    from dars.hooks.value_helpers import ValueRef
    if isinstance(message, ValueRef):
        return RawJS(code=Action.log(message=RawJS(message._get_code())))
    else:
        return RawJS(code=Action.log(message=message))


def getDateTime(format: str = "iso") -> 'ValueRef':
    """Get current date/time as a ValueRef for use in forms and state."""
    from dars.hooks.value_helpers import ValueRef
    
    class DateTimeRef(ValueRef):
        def __init__(self, format_type: str):
            self.selector = None
            self.format_type = format_type
            self._transform = None
        
        def _get_code(self) -> str:
            if self.format_type == "iso": return "(new Date().toISOString())"
            elif self.format_type == "locale": return "(new Date().toLocaleString())"
            elif self.format_type == "date": return "(new Date().toLocaleDateString())"
            elif self.format_type == "time": return "(new Date().toLocaleTimeString())"
            elif self.format_type == "timestamp": return "(Date.now())"
            return "(new Date().toISOString())"
    
    return DateTimeRef(format)


# ============= DOM Manipulation Utilities =============

def show(id: str) -> RawJS:
    """
    Show a DOM element by setting its CSS display property.
    
    Args:
        id (str): The ID of the element to show.
        
    Returns:
        RawJS: The compiled `dom_show` action.
        
    Example:
        ```python
        Button("Show Details", on_click=show("details_panel"))
        ```
    """
    return RawJS(code=Action.dom_show(id))


def hide(id: str) -> RawJS:
    """
    Hide a DOM element by setting its CSS display property to 'none'.
    
    Args:
        id (str): The ID of the element to hide.
        
    Returns:
        RawJS: The compiled `dom_hide` action.
        
    Example:
        ```python
        Button("Hide Details", on_click=hide("details_panel"))
        ```
    """
    return RawJS(code=Action.dom_hide(id))


def toggle(id: str) -> RawJS:
    """
    Toggle a DOM element's visibility.
    
    If the element is currently hidden (display: none), it will be shown.
    If it is visible, it will be hidden.
    
    Args:
        id (str): The ID of the element to toggle.
        
    Returns:
        RawJS: The compiled `dom_toggle` action.
        
    Example:
        ```python
        Button("Toggle Menu", on_click=toggle("mobile_menu"))
        ```
    """
    return RawJS(code=Action.dom_toggle(id))


def setText(id: str, text: Union[str, 'ValueRef']) -> RawJS:
    """
    Set the text content of a DOM element.
    
    Args:
        id (str): The ID of the target element.
        text (str | ValueRef): The text to set. Can be a static string or a dynamic `ValueRef`.
        
    Returns:
        RawJS: The compiled `dom_set_text` action.
        
    Example:
        ```python
        # Static text
        Button("Set Title", on_click=setText("header", "New Title"))
        
        # Dynamic text from input
        Button("Update", on_click=setText("display", V("#input_field")))
        ```
    """
    from dars.hooks.value_helpers import ValueRef
    if isinstance(text, ValueRef):
        return RawJS(code=Action.dom_set_text(id=id, text=RawJS(text._get_code())))
    else:
        return RawJS(code=Action.dom_set_text(id=id, text=text))


def addClass(id: str, class_name: str) -> RawJS:
    """
    Add a CSS class to a DOM element.
    
    Args:
        id (str): The ID of the element.
        class_name (str): The CSS class to add.
        
    Returns:
        RawJS: The compiled `class_add` action.
        
    Example:
        ```python
        Button("Highlight", on_click=addClass("text_block", "highlighted"))
        ```
    """
    return RawJS(code=Action.class_add(id, class_name))


def removeClass(id: str, class_name: str) -> RawJS:
    """
    Remove a CSS class from a DOM element.
    
    Args:
        id (str): The ID of the element.
        class_name (str): The CSS class to remove.
        
    Returns:
        RawJS: The compiled `class_remove` action.
        
    Example:
        ```python
        Button("Remove Highlight", on_click=removeClass("text_block", "highlighted"))
        ```
    """
    return RawJS(code=Action.class_remove(id, class_name))


def toggleClass(id: str, class_name: str) -> RawJS:
    """
    Toggle a CSS class on a DOM element.
    
    If the element has the class, it will be removed. If it doesn't, it will be added.
    
    Args:
        id (str): The ID of the element.
        class_name (str): The CSS class to toggle.
        
    Returns:
        RawJS: The compiled `class_toggle` action.
        
    Example:
        ```python
        Button("Toggle Dark Mode", on_click=toggleClass("app_body", "dark-theme"))
        ```
    """
    return RawJS(code=Action.class_toggle(id, class_name))


# ============= Scroll Utilities =============

def scrollTo(x: int = 0, y: int = 0) -> RawJS:
    """
    Scroll the window to a specific pixel coordinate.
    
    Args:
        x (int): Horizontal pixel position (default: 0).
        y (int): Vertical pixel position (default: 0).
        
    Returns:
        RawJS: The compiled `scroll_to` action.
        
    Example:
        ```python
        Button("Scroll to top", on_click=scrollTo(0, 0))
        ```
    """
    return RawJS(code=Action.scroll_to(x, y))


def scrollToTop() -> RawJS:
    """
    Scroll smoothly to the top of the page.
    
    Returns:
        RawJS: The compiled `scroll_top` action.
        
    Example:
        ```python
        Button("Back to Top", on_click=scrollToTop())
        ```
    """
    return RawJS(code=Action.scroll_top())


def scrollToBottom() -> RawJS:
    """
    Scroll smoothly to the bottom of the page.
    
    Returns:
        RawJS: The compiled `scroll_bottom` action.
        
    Example:
        ```python
        Button("Go to Footer", on_click=scrollToBottom())
        ```
    """
    return RawJS(code=Action.scroll_bottom())


def scrollToElement(id: str) -> RawJS:
    """
    Scroll smoothly until the specified element is in view.
    
    Args:
        id (str): The ID of the target element.
        
    Returns:
        RawJS: The compiled `scroll_to_element` action.
        
    Example:
        ```python
        Button("Go to Pricing", on_click=scrollToElement("pricing_section"))
        ```
    """
    return RawJS(code=Action.scroll_to_element(id))


# ============= Form Utilities =============

def submitForm(form_id: str) -> RawJS:
    """
    Programmatically submit a form.
    
    Args:
        form_id (str): The ID of the `<form>` element.
        
    Returns:
        RawJS: The compiled `form_submit` action.
        
    Example:
        ```python
        Button("Save", on_click=submitForm("profile_form"))
        ```
    """
    return RawJS(code=Action.form_submit(form_id))


def resetForm(form_id: str) -> RawJS:
    """
    Programmatically reset a form to its initial values.
    
    Args:
        form_id (str): The ID of the `<form>` element.
        
    Returns:
        RawJS: The compiled `form_reset` action.
        
    Example:
        ```python
        Button("Clear Form", on_click=resetForm("contact_form"))
        ```
    """
    return RawJS(code=Action.form_reset(form_id))


def getValue(input_id: str, target_id: str) -> RawJS:
    """Get value from input and set to target."""
    return RawJS(code=Action.dom_set_text(id=target_id, text=RawJS(f"document.getElementById('{input_id}').value")))


def clearInput(input_id: str) -> RawJS:
    """
    Clear the value of an input field and trigger the 'input' event.
    
    Args:
        input_id (str): The ID of the input or textarea.
        
    Returns:
        RawJS: The compiled `input_clear` action.
        
    Example:
        ```python
        Button("Clear Search", on_click=clearInput("search_box"))
        ```
    """
    return RawJS(code=Action.input_clear(input_id))


# ============= Storage Utilities =============

def saveToLocal(key: str, value: str) -> RawJS:
    """
    Save a key-value pair to the browser's localStorage.
    
    Args:
        key (str): The key under which to store the value.
        value (str): The string value to store.
        
    Returns:
        RawJS: The compiled `storage_set` action.
        
    Example:
        ```python
        Button("Accept Cookies", on_click=saveToLocal("cookies_accepted", "true"))
        ```
    """
    return RawJS(code=Action.storage_set(key, value))


def loadFromLocal(key: str, target_id: str) -> RawJS:
    """Load from localStorage and set to target."""
    return RawJS(code=Action.dom_set_text(id=target_id, text=RawJS(f"localStorage.getItem('{key}') || ''")))


def removeFromLocal(key: str) -> RawJS:
    """
    Remove an item from the browser's localStorage.
    
    Args:
        key (str): The key to remove.
        
    Returns:
        RawJS: The compiled `storage_remove` action.
        
    Example:
        ```python
        Button("Sign Out", on_click=removeFromLocal("auth_token"))
        ```
    """
    return RawJS(code=Action.storage_remove(key))


def clearLocalStorage() -> RawJS:
    """
    Clear all items from the browser's localStorage.
    
    Returns:
        RawJS: The compiled `storage_clear` action.
        
    Example:
        ```python
        Button("Clear Data", on_click=clearLocalStorage())
        ```
    """
    return RawJS(code=Action.storage_clear())


# ============= Clipboard Utilities =============

def copyToClipboard(text: Union[str, 'ValueRef']) -> RawJS:
    """
    Copy a given string or dynamic value to the system clipboard.
    
    Args:
        text (str | ValueRef): The text to copy, or a ValueRef pointing to it.
        
    Returns:
        RawJS: The compiled `clipboard_write` action.
        
    Example:
        ```python
        Button("Copy Link", on_click=copyToClipboard("https://dars.dev"))
        Button("Copy Result", on_click=copyToClipboard(V("#result_box")))
        ```
    """
    from dars.hooks.value_helpers import ValueRef
    if isinstance(text, ValueRef):
        return RawJS(code=Action.clipboard_write(text=RawJS(text._get_code())))
    else:
        return RawJS(code=Action.clipboard_write(text=text))


def copyElementText(id: str) -> RawJS:
    """
    Copy the text content of a specified DOM element to the clipboard.
    
    Args:
        id (str): The ID of the element whose text content to copy.
        
    Returns:
        RawJS: The compiled `clipboard_copy_element` action.
        
    Example:
        ```python
        Button("Copy Code", on_click=copyElementText("code_snippet_1"))
        ```
    """
    return RawJS(code=Action.clipboard_copy_element(id))


# ============= Focus Utilities =============

def focus(id: str) -> RawJS:
    """
    Set browser focus on a specific DOM element (e.g., an input field).
    
    Args:
        id (str): The ID of the element to focus.
        
    Returns:
        RawJS: The compiled `dom_focus` action.
        
    Example:
        ```python
        Button("Search", on_click=focus("search_input"))
        ```
    """
    return RawJS(code=Action.dom_focus(id))


def blur(id: str) -> RawJS:
    """
    Remove focus from a specific DOM element.
    
    Args:
        id (str): The ID of the element to blur.
        
    Returns:
        RawJS: The compiled `dom_blur` action.
        
    Example:
        ```python
        Button("Done", on_click=blur("active_input"))
        ```
    """
    return RawJS(code=Action.dom_blur(id))


# ============= Keyboard Event Utilities =============

def switch(cases: dict, default=None) -> RawJS:
    """Create a switch-case statement for keyboard events."""
    import json
    def _to_code(act):
        if act is None: return ""
        if isinstance(act, list):
            return "\n".join(_to_code(a) for a in act)
        if isinstance(act, RawJS): return act.code
        if hasattr(act, "get_code"): return act.get_code()
        return str(act)

    lines = ["var _ev = typeof event !== 'undefined' ? event : null;"]
    lines.append("if (_ev && _ev.key) {")
    lines.append("  switch(true) {")
    for k, v in cases.items():
        lines.append(f"    case (_ev.key === {json.dumps(str(k))} || _ev.code === {json.dumps(str(k))}):")
        lines.append(f"      {_to_code(v)}")
        lines.append(f"      break;")
    if default is not None:
        lines.append("    default:")
        lines.append(f"      {_to_code(default)}")
    lines.append("  }")
    lines.append("}")
    return RawJS(code="\n".join(lines))


# ============= Timer Utilities =============

def setTimeout(delay: int, code: Union['dScript', 'RawJS', str]) -> 'RawJS':
    """Set a timeout to execute a script after a delay. Returns a Promise for chainability."""
    from dars.scripts.dscript import RawJS
    if hasattr(code, 'code'):
        code_str = code.code
    elif hasattr(code, 'get_code'):
        code_str = code.get_code()
    else:
        code_str = str(code)
    
    code_val = f"(new Promise((_res_timeout, _rej_timeout) => setTimeout(async () => {{ try {{ {code_str}; _res_timeout(); }} catch(e) {{ _rej_timeout(e); }} }}, {delay})))"
    return RawJS(code=code_val)


def getInputValue(input_id: str, parent_id: str = None) -> RawJS:
    """Get the value from an input element."""
    if parent_id:
        code = f"document.getElementById('{parent_id}').querySelector('#{input_id}').value"
    else:
        code = f"document.getElementById('{input_id}').value"
    
    return RawJS(code=code)