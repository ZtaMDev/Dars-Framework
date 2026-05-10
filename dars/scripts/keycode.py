# Dars Framework - Core Source File
#
# This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0.
# If a copy of the MPL was not distributed with this file, You can obtain one at
# https://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2025 ZtaDev
"""
KeyCode constants for keyboard event handling.

Provides easy access to key codes for keyboard events.
Use with on_key_down, on_key_up, and on_key_press event handlers.

Example:
    from dars.all import *
    
    # Simple key handler
    Input(on_key_down=onKey(KeyCode.ENTER, log("Enter pressed")))
    
    # Multiple keys with switch()
    Input(on_key_down=switch({
        KeyCode.ENTER: log("Enter pressed"),
        KeyCode.ESCAPE: alert("Escape pressed"),
        KeyCode.TAB: focus("next-input")
    }))
    
    # Global keyboard shortcuts
    addGlobalKeys(app, {
        KeyCode.ENTER: submit_form(),
        KeyCode.ESCAPE: close_modal(),
        (KeyCode.S, 'ctrl'): save_document()
    })
"""

class KeyCodeMeta(type):
    """Metaclass to provide attribute access to key codes"""
    
    def __getattr__(cls, name):
        """Allow accessing keys as attributes (e.g., KeyCode.ENTER)"""
        # Check if it's in our mapping
        if name in cls._KEY_MAP:
            return cls._KEY_MAP[name]
        
        # For single letters, return the lowercase letter
        if len(name) == 1 and name.isalpha():
            return name.lower()
        
        raise AttributeError(f"KeyCode has no attribute '{name}'")


class KeyCode(metaclass=KeyCodeMeta):
    """
    KeyCode constants for keyboard event handling.
    
    Access keys as attributes:
        KeyCode.ENTER
        KeyCode.ESCAPE
        KeyCode.A
        KeyCode.SPACE
    
    Or use the key() method for dynamic access:
        KeyCode.key('Enter')
        KeyCode.key('a')
    """
    
    # Special keys mapping
    _KEY_MAP = {
        # Navigation
        'ENTER': 'Enter',
        'TAB': 'Tab',
        'ESCAPE': 'Escape',
        'ESC': 'Escape',
        'BACKSPACE': 'Backspace',
        'DELETE': 'Delete',
        'INSERT': 'Insert',
        'HOME': 'Home',
        'END': 'End',
        'PAGEUP': 'PageUp',
        'PAGEDOWN': 'PageDown',
        'PAGE_UP': 'PageUp',
        'PAGE_DOWN': 'PageDown',
        
        # Arrow keys
        'ARROWUP': 'ArrowUp',
        'ARROWDOWN': 'ArrowDown',
        'ARROWLEFT': 'ArrowLeft',
        'ARROWRIGHT': 'ArrowRight',
        'UP': 'ArrowUp',
        'DOWN': 'ArrowDown',
        'LEFT': 'ArrowLeft',
        'RIGHT': 'ArrowRight',
        
        # Modifiers
        'SHIFT': 'Shift',
        'CONTROL': 'Control',
        'CTRL': 'Control',
        'ALT': 'Alt',
        'META': 'Meta',
        'COMMAND': 'Meta',
        'CMD': 'Meta',
        
        # Function keys
        'F1': 'F1', 'F2': 'F2', 'F3': 'F3', 'F4': 'F4',
        'F5': 'F5', 'F6': 'F6', 'F7': 'F7', 'F8': 'F8',
        'F9': 'F9', 'F10': 'F10', 'F11': 'F11', 'F12': 'F12',
        
        # Special characters
        'SPACE': ' ',
        'SPACEBAR': ' ',
        'PLUS': '+',
        'MINUS': '-',
        'EQUALS': '=',
        'SLASH': '/',
        'BACKSLASH': '\\',
        'COMMA': ',',
        'PERIOD': '.',
        'SEMICOLON': ';',
        'QUOTE': "'",
        'DOUBLEQUOTE': '"',
        'BACKTICK': '`',
        'LEFTBRACKET': '[',
        'RIGHTBRACKET': ']',
        'LEFTPAREN': '(',
        'RIGHTPAREN': ')',
        'LEFTBRACE': '{',
        'RIGHTBRACE': '}',
        
        # Numbers
        'ZERO': '0', 'ONE': '1', 'TWO': '2', 'THREE': '3', 'FOUR': '4',
        'FIVE': '5', 'SIX': '6', 'SEVEN': '7', 'EIGHT': '8', 'NINE': '9',
        
        # Letters (lowercase)
        'A': 'a', 'B': 'b', 'C': 'c', 'D': 'd', 'E': 'e', 'F': 'f',
        'G': 'g', 'H': 'h', 'I': 'i', 'J': 'j', 'K': 'k', 'L': 'l',
        'M': 'm', 'N': 'n', 'O': 'o', 'P': 'p', 'Q': 'q', 'R': 'r',
        'S': 's', 'T': 't', 'U': 'u', 'V': 'v', 'W': 'w', 'X': 'x',
        'Y': 'y', 'Z': 'z',
    }
    
    @classmethod
    def key(cls, key_name: str) -> str:
        """
        Get key code by name (case-insensitive).
        
        Args:
            key_name: Name of the key (e.g., 'Enter', 'a', 'Escape')
        
        Returns:
            Key code string
        
        Example:
            KeyCode.key('enter')  # Returns 'Enter'
            KeyCode.key('A')      # Returns 'a'
        """
        upper_name = key_name.upper()
        if upper_name in cls._KEY_MAP:
            return cls._KEY_MAP[upper_name]
        
        # For single characters, return as-is
        if len(key_name) == 1:
            return key_name.lower()
        
        # Return the original if not found
        return key_name


def onKey(key_code: str, action, ctrl: bool = False, shift: bool = False, alt: bool = False, meta: bool = False):
    """
    Create a keyboard event handler for a specific key (secure DAP).
    """
    def _to_action(act):
        if hasattr(act, 'get_action'): return act.get_action() or {"op": "inline", "args": {"code": act.get_code()}}
        if isinstance(act, str): return {"op": "inline", "args": {"code": act}}
        return act

    return dScript(data={
        "op": "key_event",
        "args": {
            "key": key_code,
            "ctrl": ctrl,
            "shift": shift,
            "alt": alt,
            "meta": meta,
            "action": _to_action(action),
            "preventDefault": True
        }
    })


def addGlobalKeys(app: 'App', key_handlers: dict):
    """
    Add global keyboard shortcuts to the app.
    
    This is the RECOMMENDED way to add app-level keyboard shortcuts.
    All actions must return dScript.
    
    Args:
        app: The Dars App instance
        key_handlers: Dictionary mapping KeyCode to dScript actions (or lists)
            Format: {KeyCode.ENTER: action, ...}
            Or with modifiers: {(KeyCode.S, 'ctrl'): action, ...}
            Or with lists: {KeyCode.ENTER: [action1, action2], ...}
    
    Example:
        addGlobalKeys(app, {
            KeyCode.ENTER: submit_form(),
            KeyCode.ESCAPE: close_modal(),
            (KeyCode.S, 'ctrl'): save_document(),
            (KeyCode.Z, 'ctrl'): undo(),
            (KeyCode.Z, 'ctrl', 'shift'): redo(),
            # With multiple actions
            (KeyCode.ENTER, 'ctrl'): [
                formState.message.set("Submitted!"),
                alert("Done!")
            ]
        })
    """
    from dars.scripts.dscript import dScript
    
    def extract_code(action):
        """Helper to extract JavaScript code from action"""
        if hasattr(action, 'code'):
            return action.code
        elif hasattr(action, 'get_code'):
            return action.get_code()
        else:
            return str(action)
    
    handlers_code = []
    
    for key_spec, action in key_handlers.items():
        # Parse key specification
        if isinstance(key_spec, tuple):
            key_code = key_spec[0]
            modifiers = key_spec[1:] if len(key_spec) > 1 else []
        else:
            key_code = key_spec
            modifiers = []
        
        # Get action code - handle lists
        if isinstance(action, list):
            action_codes = [extract_code(act) for act in action]
            action_code = ' '.join(action_codes)
        else:
            action_code = extract_code(action)
        
        # Build condition
        conditions = [f"event.key === '{key_code}'"]
        
        for mod in modifiers:
            if mod.lower() in ['ctrl', 'control']:
                conditions.append("event.ctrlKey")
            elif mod.lower() == 'shift':
                conditions.append("event.shiftKey")
            elif mod.lower() == 'alt':
                conditions.append("event.altKey")
            elif mod.lower() in ['meta', 'cmd', 'command']:
                conditions.append("event.metaKey")
        
        condition = " && ".join(conditions)
        handlers_code.append(f"if ({condition}) {{ event.preventDefault(); {action_code} }}")
    
    # Create global event listener
    global_handler = dScript(f'''
        document.addEventListener('keydown', function(event) {{
            {' '.join(handlers_code)}
        }});
    ''')
    
    app.add_script(global_handler)
