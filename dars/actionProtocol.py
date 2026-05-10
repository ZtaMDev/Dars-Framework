# Dars Framework - Core Source File
#
# This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0.
# If a copy of the MPL was not distributed with this file, You can obtain one at
# https://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2025 ZtaDev

"""
Dars Action Protocol (DAP) - Secure Action Definitions

This module defines all supported DAP operations that the browser runtime can execute.
At compile-time (Python/export), dScript actions are converted to structured DAP payloads.
At runtime (browser), ONLY these predefined operations are executed - never eval().

Security Model:
- Developer writes: Button("Click", on_click=goTo("/home"))
- Exporter outputs: { "op": "navigate", "args": { "path": "/home" } }
- Browser executes: _dispatch({ op: "navigate", args: {...} }) - NO EVAL
"""

from typing import Any, Dict, Optional, Union


class DAPOp:
    """All supported DAP (Dars Action Protocol) operations.
    
    These string constants define the operation types that the browser
    runtime's _dispatch() function can handle securely.
    """
    
    # === Navigation ===
    NAVIGATE = "navigate"           # Navigate to path in current tab
    NAVIGATE_NEW = "navigate_new"   # Open path in new tab
    RELOAD = "reload"               # Reload current page
    HISTORY_BACK = "history_back"   # Go back in history
    HISTORY_FORWARD = "history_forward"  # Go forward in history
    
    # === State Management ===
    CHANGE = "change"               # Change component state (id, text, style, attrs, etc.)
    
    # === Modal ===
    MODAL_SHOW = "modal_show"       # Show a Dars Modal
    MODAL_HIDE = "modal_hide"       # Hide a Dars Modal
    
    # === DOM Visibility ===
    DOM_SHOW = "dom_show"           # Set display: block
    DOM_HIDE = "dom_hide"           # Set display: none
    DOM_TOGGLE = "dom_toggle"       # Toggle visibility
    
    # === DOM Content ===
    DOM_SET_TEXT = "dom_set_text"   # Set textContent
    DOM_SET_HTML = "dom_set_html"   # Set innerHTML (sanitized)
    DOM_SET_STYLE = "dom_set_style" # Set CSS style properties
    DOM_SET_VALUE = "dom_set_value" # Set input value
    DOM_SET_ATTR = "dom_set_attr"   # Set attribute
    DOM_REFLOW = "dom_reflow"       # Force layout reflow
    DOM_ANIMATE = "dom_animate"     # Run Web Animations API animation
    
    # === Focus ===
    DOM_FOCUS = "dom_focus"         # Focus element
    DOM_BLUR = "dom_blur"           # Blur element
    
    # === CSS Classes ===
    CLASS_ADD = "class_add"         # Add CSS class
    CLASS_REMOVE = "class_remove"   # Remove CSS class
    CLASS_TOGGLE = "class_toggle"   # Toggle CSS class
    
    # === Scroll ===
    SCROLL_TO = "scroll_to"         # Scroll to x, y
    SCROLL_TOP = "scroll_top"       # Scroll to top
    SCROLL_BOTTOM = "scroll_bottom" # Scroll to bottom
    SCROLL_TO_ELEMENT = "scroll_to_element"  # Scroll element into view
    
    # === Forms ===
    FORM_SUBMIT = "form_submit"     # Submit form
    FORM_RESET = "form_reset"       # Reset form
    INPUT_CLEAR = "input_clear"     # Clear input value
    INPUT_SET = "input_set"         # Set input value
    
    # === Storage ===
    STORAGE_SET = "storage_set"     # localStorage.setItem
    STORAGE_GET = "storage_get"     # localStorage.getItem (to target)
    STORAGE_REMOVE = "storage_remove"  # localStorage.removeItem
    STORAGE_CLEAR = "storage_clear" # localStorage.clear
    
    # === Clipboard ===
    CLIPBOARD_WRITE = "clipboard_write"  # Write text to clipboard
    CLIPBOARD_COPY_ELEMENT = "clipboard_copy_element"  # Copy element text
    
    # === Alerts & Console ===
    ALERT = "alert"                 # Show alert dialog
    CONFIRM = "confirm"             # Show confirm dialog with callbacks
    LOG = "log"                     # Console.log
    
    # === Animation ===
    ANIMATE = "animate"             # Run animation (fadeIn, fadeOut, etc.)
    
    # === Control Flow ===
    SEQUENCE = "sequence"           # Execute actions in sequence
    DELAY = "delay"                 # Wait ms, then execute action
    CONDITIONAL = "conditional"     # Execute action based on condition
    
    # === VRef ===
    VREF_UPDATE = "vref_update"     # Update VRef value
    VREF_GET = "vref_get"           # Get VRef value
    
    # === Dynamic Components ===
    COMP_CREATE = "comp_create"     # Create component dynamically
    COMP_DELETE = "comp_delete"     # Delete component
    COMP_UPDATE = "comp_update"     # Update component
    
    # === HTTP (Backend) ===
    FETCH = "fetch"                 # Controlled fetch request
    
    # === Desktop (Electron) ===
    DESKTOP_FS_READ = "desktop_fs_read"   # Read file
    DESKTOP_FS_WRITE = "desktop_fs_write" # Write file


class ActionBuilder:
    """Helper class to build structured JS actions from Python.
    
    Usage:
        from dars.actionProtocol import ActionBuilder as Action
        
        Button("Go", on_click=Action.navigate("/home"))
        Button("Show", on_click=Action.dom_show("my-element"))
    """
    
    # === Navigation ===
    @staticmethod
    def navigate(path: str) -> str:
        """Navigate to a path in the current tab."""
        return f"window.location.href = '{path}';"
    
    @staticmethod
    def navigate_new(path: str) -> str:
        """Open a path in a new tab."""
        return f"window.open('{path}', '_blank');"
    
    @staticmethod
    def reload() -> str:
        """Reload the current page."""
        return "window.location.reload();"
    
    @staticmethod
    def history_back() -> str:
        """Go back in browser history."""
        return "window.history.back();"
    
    @staticmethod
    def history_forward() -> str:
        """Go forward in browser history."""
        return "window.history.forward();"
    
    # === State ===
    @staticmethod
    def change(target_id: str, **kwargs) -> str:
        """Change component state."""
        import json
        lines = [f"var __el_{target_id} = document.getElementById('{target_id}');", f"if (__el_{target_id}) {{"]
        if "text" in kwargs:
            lines.append(f"  __el_{target_id}.textContent = {json.dumps(kwargs['text'])};")
        if "value" in kwargs:
            lines.append(f"  __el_{target_id}.value = {json.dumps(kwargs['value'])};")
        if "style" in kwargs and isinstance(kwargs["style"], dict):
            for k, v in kwargs["style"].items():
                lines.append(f"  __el_{target_id}.style[{json.dumps(k)}] = {json.dumps(v)};")
        lines.append("}")
        return "\n".join(lines)
    
    # === Modal ===
    @staticmethod
    def modal_show(modal_id: str) -> str:
        """Show a Dars Modal."""
        return f"if (window.DarsModal) window.DarsModal.show('{modal_id}');"
    
    @staticmethod
    def modal_hide(modal_id: str) -> str:
        """Hide a Dars Modal."""
        return f"if (window.DarsModal) window.DarsModal.hide('{modal_id}');"
    
    # === DOM Visibility ===
    @staticmethod
    def dom_show(element_id: str) -> str:
        """Show an element (display: block)."""
        return f"var el = document.getElementById('{element_id}'); if(el) el.style.display = 'block';"
    
    @staticmethod
    def dom_hide(element_id: str) -> str:
        """Hide an element (display: none)."""
        return f"var el = document.getElementById('{element_id}'); if(el) el.style.display = 'none';"
    
    @staticmethod
    def dom_toggle(element_id: str) -> str:
        """Toggle element visibility."""
        return f"var el = document.getElementById('{element_id}'); if(el) el.style.display = el.style.display === 'none' ? 'block' : 'none';"
    
    # === DOM Content ===
    @staticmethod
    def dom_set_style(id: str, style: dict) -> str:
        """Set CSS style properties for an element."""
        import json
        js_styles = "".join([f"el.style[{json.dumps(k)}] = {json.dumps(v)};" for k, v in style.items()])
        return f"var el = document.getElementById('{id}'); if(el) {{ {js_styles} }}"

    @staticmethod
    def dom_set_text(id: str, text: str) -> str:
        """Set element textContent."""
        import json
        return f"var el = document.getElementById('{id}'); if(el) el.textContent = {json.dumps(text)};"
    
    @staticmethod
    def dom_set_value(element_id: str, value: Any) -> str:
        """Set input element value."""
        import json
        return f"var el = document.getElementById('{element_id}'); if(el) el.value = {json.dumps(value)};"

    @staticmethod
    def dom_animate(id: str, keyframes: list, options: dict) -> str:
        """Run a Web Animations API animation on an element."""
        import json
        kf = json.dumps(keyframes)
        opt = json.dumps(options)
        return f"var el = document.getElementById('{id}'); if(el) el.animate({kf}, {opt});"

    @staticmethod
    def dom_reflow(id: str) -> str:
        """Force layout reflow (useful for starting animations)."""
        return f"var el = document.getElementById('{id}'); if(el) void el.offsetWidth;"
    
    # === Focus ===
    @staticmethod
    def dom_focus(element_id: str) -> str:
        """Focus an element."""
        return f"var el = document.getElementById('{element_id}'); if(el) el.focus();"
    
    @staticmethod
    def dom_blur(element_id: str) -> str:
        """Blur an element."""
        return f"var el = document.getElementById('{element_id}'); if(el) el.blur();"
    
    # === CSS Classes ===
    @staticmethod
    def class_add(element_id: str, class_name: str) -> str:
        """Add a CSS class to an element."""
        import json
        return f"var el = document.getElementById('{element_id}'); if(el) el.classList.add({json.dumps(class_name)});"
    
    @staticmethod
    def class_remove(element_id: str, class_name: str) -> str:
        """Remove a CSS class from an element."""
        import json
        return f"var el = document.getElementById('{element_id}'); if(el) el.classList.remove({json.dumps(class_name)});"
    
    @staticmethod
    def class_toggle(element_id: str, class_name: str) -> str:
        """Toggle a CSS class on an element."""
        import json
        return f"var el = document.getElementById('{element_id}'); if(el) el.classList.toggle({json.dumps(class_name)});"
    
    # === Scroll ===
    @staticmethod
    def scroll_to(x: int = 0, y: int = 0) -> str:
        """Scroll window to position."""
        return f"window.scrollTo({x}, {y});"
    
    @staticmethod
    def scroll_top() -> str:
        """Scroll to top of page."""
        return "window.scrollTo({ top: 0, behavior: 'smooth' });"
    
    @staticmethod
    def scroll_bottom() -> str:
        """Scroll to bottom of page."""
        return "window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' });"
    
    @staticmethod
    def scroll_to_element(element_id: str) -> str:
        """Scroll element into view."""
        return f"var el = document.getElementById('{element_id}'); if(el) el.scrollIntoView({{ behavior: 'smooth' }});"
    
    # === Forms ===
    @staticmethod
    def form_submit(form_id: str) -> str:
        """Submit a form."""
        return f"var form = document.getElementById('{form_id}'); if(form) form.submit();"
    
    @staticmethod
    def form_reset(form_id: str) -> str:
        """Reset a form."""
        return f"var form = document.getElementById('{form_id}'); if(form) form.reset();"
    
    @staticmethod
    def input_clear(input_id: str) -> str:
        """Clear an input field."""
        return f"var el = document.getElementById('{input_id}'); if(el) {{ el.value = ''; el.dispatchEvent(new Event('input', {{ bubbles: true }})); }}"
    
    # === Storage ===
    @staticmethod
    def storage_set(key: str, value: str) -> str:
        """Save to localStorage."""
        import json
        return f"localStorage.setItem({json.dumps(key)}, {json.dumps(value)});"
    
    @staticmethod
    def storage_remove(key: str) -> str:
        """Remove from localStorage."""
        import json
        return f"localStorage.removeItem({json.dumps(key)});"
    
    @staticmethod
    def storage_clear() -> str:
        """Clear all localStorage."""
        return "localStorage.clear();"
    
    # === Clipboard ===
    @staticmethod
    def clipboard_write(text: str) -> str:
        """Write text to clipboard."""
        import json
        return f"navigator.clipboard.writeText({json.dumps(text)});"
    
    @staticmethod
    def clipboard_copy_element(element_id: str) -> str:
        """Copy element text to clipboard."""
        return f"var el = document.getElementById('{element_id}'); if(el) navigator.clipboard.writeText(el.textContent || '');"
    
    # === Alerts ===
    @staticmethod
    def alert(message: str) -> str:
        """Show an alert dialog."""
        import json
        return f"alert({json.dumps(message)});"
    
    @staticmethod
    def log(message: str) -> str:
        """Log to console."""
        import json
        return f"console.log({json.dumps(message)});"
    
    # === Animation ===
    @staticmethod
    def animate(element_id: str, animation_type: str, duration: int = 300, **kwargs) -> str:
        """Run an animation."""
        import json
        args = json.dumps({"id": element_id, "type": animation_type, "duration": duration, **kwargs})
        return f"if (window.Dars && window.Dars.animate) window.Dars.animate({args});"
    
    # === Control Flow ===
    @staticmethod
    def sequence(*actions) -> str:
        """Execute multiple actions in sequence."""
        def extract_code(act):
            if isinstance(act, str): return act
            if isinstance(act, dict): return act.get("code") or ""
            if hasattr(act, "get_code"): return act.get_code()
            return ""
        
        valid_actions = [extract_code(a) for a in actions if a is not None]
        return "\n".join(valid_actions)
    
    @staticmethod
    def delay(ms: int, action: Optional[Any] = None) -> str:
        """Wait, then optionally execute action."""
        if action:
            act_code = action
            if isinstance(action, dict): act_code = action.get("code", "")
            elif hasattr(action, "get_code"): act_code = action.get_code()
            return f"setTimeout(() => {{\n{act_code}\n}}, {ms});"
        return ""
    
    # === VRef ===
    @staticmethod
    def vref_update(selector: str, value: Any) -> str:
        """Update a VRef value."""
        import json
        v = json.dumps(value)
        return (f"document.querySelectorAll('{selector}').forEach(el => {{\n"
                f"  if(el.tagName === 'INPUT' || el.tagName === 'TEXTAREA') {{\n"
                f"    if(el.type === 'checkbox' || el.type === 'radio') el.checked = Boolean({v});\n"
                f"    else el.value = {v};\n"
                f"  }} else if(el.tagName === 'SELECT') {{\n"
                f"    el.value = {v};\n"
                f"  }} else {{\n"
                f"    el.textContent = {v};\n"
                f"  }}\n"
                f"}});")
    
    # === Dynamic Components ===
    @staticmethod
    def comp_create(root_id: str, vdom: Dict[str, Any], position: str = "append") -> str:
        """Create a component dynamically."""
        import json
        v = json.dumps(vdom)
        return f"if (window.Dars && window.Dars.createComponent) window.Dars.createComponent('{root_id}', {v}, '{position}');"
    
    @staticmethod
    def comp_delete(component_id: str) -> str:
        """Delete a component."""
        return f"var el = document.getElementById('{component_id}'); if (el && el.parentNode) el.parentNode.removeChild(el);"


# Convenience alias
Action = ActionBuilder
