# Dars Framework - Core Source File
#
# This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0.
# If a copy of the MPL was not distributed with this file, You can obtain one at
# https://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2025 ZtaDev
from typing import Optional
from .script import Script

class dScript(Script):
    """
    Script that can be defined as inline (JS code in string) or as a reference to an external file.
    Only one of the two must be present.
    """
    def __init__(self, code: Optional[str] = None, file_path: Optional[str] = None, target_language: str = "javascript", module: bool = False):
        super().__init__(target_language, module=module)
        if (code is None and file_path is None) or (code is not None and file_path is not None):
            raise ValueError("You have to specify only one: 'code' (inline) or 'file_path' (external), but not both.")
        self.code = code
        self.file_path = file_path

    def get_code(self) -> str:
        if self.code is not None:
            return self.code
        elif self.file_path is not None:
            try:
                with open(self.file_path, 'r') as f:
                    return f.read()
            except FileNotFoundError:
                raise FileNotFoundError(f"The script file was not found: {self.file_path}")
        else:
            raise ValueError("No code or file path defined for this dScript.")

    def then(self, script: 'dScript') -> 'dScript':
        """
        Chain another script to execute after this one resolves.
        Wraps the current script in an async IIFE if needed and appends .then().
        """
        current_code = self.get_code().strip()
        next_code = script.get_code().strip()
        
        # If next_code is an async IIFE (starts with (async), unwrap it to be a function body
        # or just pass it as a callback.
        # Simplest approach: assume current_code returns a Promise.
        # We wrap current_code in `Promise.resolve(...)` to be safe?
        # No, read_text returns a dScript that is an async IIFE returning a value.
        
        # We need to construct a new JS that chains them.
        # (async () => { await (current_code); await (next_code); })() ?
        # But we want to pass the result of current to next?
        # The user asked for: read_text(...).then(this.state(...))
        # read_text returns a value. this.state(...) usually ignores arguments or expects specific ones.
        # But maybe we want to inject the result into the state change?
        
        # If the user does: read_text(..., then=this.state(text=dScript.ARG))
        # But here we are doing .then() on the dScript object.
        
        # Let's implement a generic chaining.
        # We can't easily parse JS to know if it returns a promise.
        # But our `read_text` implementation returns an async IIFE.
        
        combined_code = f"""
(async () => {{
    try {{
        const result = await {current_code};
        // Make result available as 'value' or argument to next script
        const value = result; 
        await (async (value) => {{ 
            {next_code} 
        }})(result);
        return result;
    }} catch (e) {{
        console.error("Chained script error:", e);
        throw e;
    }}
}})()
""".strip()
        return dScript(code=combined_code)

    # Helper for placeholder argument
    ARG = "value"

class RawJS:
    """
    Wrapper to indicate that a string should be treated as raw JavaScript code
    instead of a string literal when serialized.
    """
    def __init__(self, code: str):
        self.code = code
    
    def __str__(self):
        return self.code
    
    def __repr__(self):
        return self.code

# Pythonic helper for dScript.ARG access
class _ArgHelper:
    """Pythonic wrapper for dScript.ARG to avoid raw JS strings.
    
    Usage:
        Arg.text -> RawJS("dScript.ARG.text")
        Arg.value -> RawJS("dScript.ARG.value")
        Arg -> RawJS("dScript.ARG")
    """
    def __getattr__(self, name: str):
        return RawJS(f"dScript.ARG.{name}")
    
    def __str__(self):
        return "dScript.ARG"
    
    def __repr__(self):
        return "Arg (dScript.ARG accessor)"

# Singleton instance
Arg = _ArgHelper()

# Special constant for referencing dScript.ARG in .then() chains
ARG = "dScript.ARG"
