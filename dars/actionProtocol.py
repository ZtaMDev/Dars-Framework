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
    NAVIGATE = "navigate"
    NAVIGATE_NEW = "navigate_new"
    RELOAD = "reload"
    HISTORY_BACK = "history_back"
    HISTORY_FORWARD = "history_forward"
    
    # === State Management ===
    CHANGE = "change"
    
    # === Modal ===
    MODAL_SHOW = "modal_show"
    MODAL_HIDE = "modal_hide"
    
    # === DOM Visibility ===
    DOM_SHOW = "dom_show"
    DOM_HIDE = "dom_hide"
    DOM_TOGGLE = "dom_toggle"
    
    # === DOM Content ===
    DOM_SET_TEXT = "dom_set_text"
    DOM_SET_HTML = "dom_set_html"
    DOM_SET_STYLE = "dom_set_style"
    DOM_SET_VALUE = "dom_set_value"
    DOM_SET_ATTR = "dom_set_attr"
    DOM_REFLOW = "dom_reflow"
    DOM_ANIMATE = "dom_animate"
    
    # === Focus ===
    DOM_FOCUS = "dom_focus"
    DOM_BLUR = "dom_blur"
    
    # === CSS Classes ===
    CLASS_ADD = "class_add"
    CLASS_REMOVE = "class_remove"
    CLASS_TOGGLE = "class_toggle"
    
    # === Scroll ===
    SCROLL_TO = "scroll_to"
    SCROLL_TOP = "scroll_top"
    SCROLL_BOTTOM = "scroll_bottom"
    SCROLL_TO_ELEMENT = "scroll_to_element"
    
    # === Forms ===
    FORM_SUBMIT = "form_submit"
    FORM_RESET = "form_reset"
    INPUT_CLEAR = "input_clear"
    INPUT_SET = "input_set"
    
    # === Storage ===
    STORAGE_SET = "storage_set"
    STORAGE_GET = "storage_get"
    STORAGE_REMOVE = "storage_remove"
    STORAGE_CLEAR = "storage_clear"
    
    # === Clipboard ===
    CLIPBOARD_WRITE = "clipboard_write"
    CLIPBOARD_COPY_ELEMENT = "clipboard_copy_element"
    
    # === Alerts & Console ===
    ALERT = "alert"
    CONFIRM = "confirm"
    LOG = "log"
    
    # === Animation ===
    ANIMATE = "animate"
    
    # === Control Flow ===
    SEQUENCE = "sequence"
    DELAY = "delay"
    CONDITIONAL = "conditional"
    
    # === VRef ===
    VREF_UPDATE = "vref_update"
    VREF_GET = "vref_get"
    
    # === Dynamic Components ===
    COMP_CREATE = "comp_create"
    COMP_DELETE = "comp_delete"
    COMP_UPDATE = "comp_update"
    
    # === HTTP (Backend) ===
    FETCH = "fetch"
    CALL_SERVER = "call_server"
    


class ActionBuilder:
    """Helper class to build structured JS actions from Python."""
    
    @staticmethod
    def navigate(path: str) -> str:
        return f"window.location.href = '{path}';"
    
    @staticmethod
    def navigate_new(path: str) -> str:
        return f"window.open('{path}', '_blank');"
    
    @staticmethod
    def reload() -> str:
        return "window.location.reload();"
    
    @staticmethod
    def history_back() -> str:
        return "window.history.back();"
    
    @staticmethod
    def history_forward() -> str:
        return "window.history.forward();"
    
    @staticmethod
    def change(target_id: str, **kwargs) -> str:
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
    
    @staticmethod
    def modal_show(modal_id: str) -> str:
        return f"if (window.DarsModal) window.DarsModal.show('{modal_id}');"
    
    @staticmethod
    def modal_hide(modal_id: str) -> str:
        return f"if (window.DarsModal) window.DarsModal.hide('{modal_id}');"
    
    @staticmethod
    def dom_show(element_id: str) -> str:
        return f"var el = document.getElementById('{element_id}'); if(el) el.style.display = 'block';"
    
    @staticmethod
    def dom_hide(element_id: str) -> str:
        return f"var el = document.getElementById('{element_id}'); if(el) el.style.display = 'none';"
    
    @staticmethod
    def dom_toggle(element_id: str) -> str:
        return f"var el = document.getElementById('{element_id}'); if(el) el.style.display = el.style.display === 'none' ? 'block' : 'none';"
    
    @staticmethod
    def dom_set_style(id: str, style: dict) -> str:
        import json
        js_styles = "".join([f"el.style[{json.dumps(k)}] = {json.dumps(v)};" for k, v in style.items()])
        return f"var el = document.getElementById('{id}'); if(el) {{ {js_styles} }}"

    @staticmethod
    def dom_set_text(id: str, text: str) -> str:
        import json
        return f"var el = document.getElementById('{id}'); if(el) el.textContent = {json.dumps(text)};"
    
    @staticmethod
    def dom_set_value(element_id: str, value: Any) -> str:
        import json
        return f"var el = document.getElementById('{element_id}'); if(el) el.value = {json.dumps(value)};"

    @staticmethod
    def dom_animate(id: str, keyframes: list, options: dict) -> str:
        import json
        kf = json.dumps(keyframes)
        opt = json.dumps(options)
        return f"var el = document.getElementById('{id}'); if(el) el.animate({kf}, {opt});"

    @staticmethod
    def dom_reflow(id: str) -> str:
        return f"var el = document.getElementById('{id}'); if(el) void el.offsetWidth;"
    
    @staticmethod
    def dom_focus(element_id: str) -> str:
        return f"var el = document.getElementById('{element_id}'); if(el) el.focus();"
    
    @staticmethod
    def dom_blur(element_id: str) -> str:
        return f"var el = document.getElementById('{element_id}'); if(el) el.blur();"
    
    @staticmethod
    def class_add(element_id: str, class_name: str) -> str:
        import json
        return f"var el = document.getElementById('{element_id}'); if(el) el.classList.add({json.dumps(class_name)});"
    
    @staticmethod
    def class_remove(element_id: str, class_name: str) -> str:
        import json
        return f"var el = document.getElementById('{element_id}'); if(el) el.classList.remove({json.dumps(class_name)});"
    
    @staticmethod
    def class_toggle(element_id: str, class_name: str) -> str:
        import json
        return f"var el = document.getElementById('{element_id}'); if(el) el.classList.toggle({json.dumps(class_name)});"
    
    @staticmethod
    def scroll_to(x: int = 0, y: int = 0) -> str:
        return f"window.scrollTo({x}, {y});"
    
    @staticmethod
    def scroll_top() -> str:
        return "window.scrollTo({ top: 0, behavior: 'smooth' });"
    
    @staticmethod
    def scroll_bottom() -> str:
        return "window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' });"
    
    @staticmethod
    def scroll_to_element(element_id: str) -> str:
        return f"var el = document.getElementById('{element_id}'); if(el) el.scrollIntoView({{ behavior: 'smooth' }});"
    
    @staticmethod
    def form_submit(form_id: str) -> str:
        return f"var form = document.getElementById('{form_id}'); if(form) form.submit();"
    
    @staticmethod
    def form_reset(form_id: str) -> str:
        return f"var form = document.getElementById('{form_id}'); if(form) form.reset();"
    
    @staticmethod
    def input_clear(input_id: str) -> str:
        return f"var el = document.getElementById('{input_id}'); if(el) {{ el.value = ''; el.dispatchEvent(new Event('input', {{ bubbles: true }})); }}"
    
    @staticmethod
    def storage_set(key: str, value: str) -> str:
        import json
        return f"localStorage.setItem({json.dumps(key)}, {json.dumps(value)});"
    
    @staticmethod
    def storage_remove(key: str) -> str:
        import json
        return f"localStorage.removeItem({json.dumps(key)});"
    
    @staticmethod
    def storage_clear() -> str:
        return "localStorage.clear();"
    
    @staticmethod
    def clipboard_write(text: str) -> str:
        import json
        return f"navigator.clipboard.writeText({json.dumps(text)});"
    
    @staticmethod
    def clipboard_copy_element(element_id: str) -> str:
        return f"var el = document.getElementById('{element_id}'); if(el) navigator.clipboard.writeText(el.textContent || '');"
    
    @staticmethod
    def alert(message: str) -> str:
        import json
        return f"alert({json.dumps(message)});"
    
    @staticmethod
    def log(message: str) -> str:
        import json
        return f"console.log({json.dumps(message)});"
    
    @staticmethod
    def redirect_after_login(fallback: str = "/") -> str:
        """
        Navigate to the URL specified in ?redirect= query param.
        Reads window.location.search, decodes the 'redirect' param,
        and uses window.navigateTo() (SPA) or falls back to window.location.href.
        """
        safe_fallback = fallback.replace("'", "\\'")
        return (
            "(function(){"
            "var p=new URLSearchParams(window.location.search);"
            "var t=p.get('redirect');"
            "t=t?decodeURIComponent(t):'" + safe_fallback + "';"
            "if(window.navigateTo)window.navigateTo(t);"
            "else window.location.href=t;"
            "})();"
        )

    @staticmethod
    def animate(element_id: str, animation_type: str, duration: int = 300, **kwargs) -> str:
        import json
        args = json.dumps({"id": element_id, "type": animation_type, "duration": duration, **kwargs})
        return f"if (window.Dars && window.Dars.animate) window.Dars.animate({args});"
    
    @staticmethod
    def sequence(*actions) -> str:
        def extract_code(act):
            if isinstance(act, str): return act
            if isinstance(act, dict): return act.get("code") or ""
            if hasattr(act, "get_code"): return act.get_code()
            return ""
        valid_actions = [extract_code(a) for a in actions if a is not None]
        return "\n".join(valid_actions)
    
    @staticmethod
    def delay(ms: int, action: Optional[Any] = None) -> str:
        if action:
            act_code = action
            if isinstance(action, dict): act_code = action.get("code", "")
            elif hasattr(action, "get_code"): act_code = action.get_code()
            return f"setTimeout(() => {{\n{act_code}\n}}, {ms});"
        return ""
    
    @staticmethod
    def vref_update(selector: str, value: Any) -> str:
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
    
    @staticmethod
    def comp_create(root_id: str, comp_data: Dict[str, Any], position: str = "append") -> str:
        """Create component dynamically using compiled HTML + metadata."""
        import json
        v = json.dumps(comp_data)
        return f"if (window.Dars && window.Dars.runtime && typeof window.Dars.runtime.createComponent === 'function') window.Dars.runtime.createComponent('{root_id}', {v}, '{position}');"
    
    @staticmethod
    def comp_delete(component_id: str) -> str:
        """Delete a component using runtime."""
        return f"if (window.Dars && window.Dars.runtime && typeof window.Dars.runtime.deleteComponent === 'function') window.Dars.runtime.deleteComponent('{component_id}');"


# Convenience alias
Action = ActionBuilder
