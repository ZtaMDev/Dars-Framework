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
    Returns a RawJS that shows a Dars Modal component.
    """
    return RawJS(code=Action.modal_show(id))


def hideModal(id: str) -> RawJS:
    """
    Returns a RawJS that hides a Dars Modal component.
    """
    return RawJS(code=Action.modal_hide(id))


# ============= Navigation Utilities =============

def goTo(href: str) -> RawJS:
    """Navigate to a URL in the current tab."""
    return RawJS(code=Action.navigate(href))


def goToNew(href: str) -> RawJS:
    """Open a URL in a new tab."""
    return RawJS(code=Action.navigate_new(href))


def reload() -> RawJS:
    """Reload the current page."""
    return RawJS(code=Action.reload())


def goBack() -> RawJS:
    """Navigate back in browser history."""
    return RawJS(code=Action.history_back())


def goForward() -> RawJS:
    """Navigate forward in browser history."""
    return RawJS(code=Action.history_forward())


# ============= Alert & Console Utilities =============

def alert(message: Union[str, 'ValueRef']) -> RawJS:
    """Show a browser alert dialog."""
    from dars.hooks.value_helpers import ValueRef
    if isinstance(message, ValueRef):
        return RawJS(code=Action.alert(message=RawJS(message._get_code())))
    else:
        return RawJS(code=Action.alert(message=message))


def confirm(message: str, on_ok: Union[str, dScript, RawJS] = None, on_cancel: Union[str, dScript, RawJS] = None) -> RawJS:
    """Show a browser confirm dialog with optional callbacks."""
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
    """Log a message to the browser console."""
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
    """Show an element."""
    return RawJS(code=Action.dom_show(id))


def hide(id: str) -> RawJS:
    """Hide an element."""
    return RawJS(code=Action.dom_hide(id))


def toggle(id: str) -> RawJS:
    """Toggle an element's visibility."""
    return RawJS(code=Action.dom_toggle(id))


def setText(id: str, text: Union[str, 'ValueRef']) -> RawJS:
    """Set the text content of an element."""
    from dars.hooks.value_helpers import ValueRef
    if isinstance(text, ValueRef):
        return RawJS(code=Action.dom_set_text(id=id, text=RawJS(text._get_code())))
    else:
        return RawJS(code=Action.dom_set_text(id=id, text=text))


def addClass(id: str, class_name: str) -> RawJS:
    """Add a CSS class to an element."""
    return RawJS(code=Action.class_add(id, class_name))


def removeClass(id: str, class_name: str) -> RawJS:
    """Remove a CSS class from an element."""
    return RawJS(code=Action.class_remove(id, class_name))


def toggleClass(id: str, class_name: str) -> RawJS:
    """Toggle a CSS class on an element."""
    return RawJS(code=Action.class_toggle(id, class_name))


# ============= Scroll Utilities =============

def scrollTo(x: int = 0, y: int = 0) -> RawJS:
    """Scroll window to position."""
    return RawJS(code=Action.scroll_to(x, y))


def scrollToTop() -> RawJS:
    """Scroll to top smoothly."""
    return RawJS(code=Action.scroll_top())


def scrollToBottom() -> RawJS:
    """Scroll to bottom smoothly."""
    return RawJS(code=Action.scroll_bottom())


def scrollToElement(id: str) -> RawJS:
    """Scroll to element smoothly."""
    return RawJS(code=Action.scroll_to_element(id))


# ============= Form Utilities =============

def submitForm(form_id: str) -> RawJS:
    """Submit a form."""
    return RawJS(code=Action.form_submit(form_id))


def resetForm(form_id: str) -> RawJS:
    """Reset a form."""
    return RawJS(code=Action.form_reset(form_id))


def getValue(input_id: str, target_id: str) -> RawJS:
    """Get value from input and set to target."""
    return RawJS(code=Action.dom_set_text(id=target_id, text=RawJS(f"document.getElementById('{input_id}').value")))


def clearInput(input_id: str) -> RawJS:
    """Clear an input field."""
    return RawJS(code=Action.input_clear(input_id))


# ============= Storage Utilities =============

def saveToLocal(key: str, value: str) -> RawJS:
    """Save to localStorage."""
    return RawJS(code=Action.storage_set(key, value))


def loadFromLocal(key: str, target_id: str) -> RawJS:
    """Load from localStorage and set to target."""
    return RawJS(code=Action.dom_set_text(id=target_id, text=RawJS(f"localStorage.getItem('{key}') || ''")))


def removeFromLocal(key: str) -> RawJS:
    """Remove from localStorage."""
    return RawJS(code=Action.storage_remove(key))


def clearLocalStorage() -> RawJS:
    """Clear all localStorage."""
    return RawJS(code=Action.storage_clear())


# ============= Clipboard Utilities =============

def copyToClipboard(text: Union[str, 'ValueRef']) -> RawJS:
    """Copy text to clipboard."""
    from dars.hooks.value_helpers import ValueRef
    if isinstance(text, ValueRef):
        return RawJS(code=Action.clipboard_write(text=RawJS(text._get_code())))
    else:
        return RawJS(code=Action.clipboard_write(text=text))


def copyElementText(id: str) -> RawJS:
    """Copy element text to clipboard."""
    return RawJS(code=Action.clipboard_copy_element(id))


# ============= Focus Utilities =============

def focus(id: str) -> RawJS:
    """Set focus on an element."""
    return RawJS(code=Action.dom_focus(id))


def blur(id: str) -> RawJS:
    """Remove focus from an element."""
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