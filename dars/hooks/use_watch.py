# Dars Framework - Core Source File
#
# This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0.
# If a copy of the MPL was not distributed with this file, You can obtain one at
# https://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2025 ZtaDev
"""
useWatch Hook

Enables watching state changes and executing callbacks.
"""

class WatchMarker:
    """
    Represents a watcher script.
    Works with app.add_script() and page.add_script().
    """
    
    def __init__(self, state_path: str | list[str], callback_code: str):
        """
        Initialize a watch marker.
        
        Args:
            state_path: Dot-notation path to state property (e.g., "user.name") or list of paths
            callback_code: JavaScript code to execute when state changes
        """
        self.state_path = state_path
        self.callback_code = callback_code
        self.code = self.get_code()
    
    def get_code(self):
        """Return the JavaScript code for this watcher"""
        if isinstance(self.state_path, list):
            # Generate a watch call for each path
            codes = []
            for path in self.state_path:
                codes.append(f"window.Dars.watch('{path}', function() {{ {self.callback_code} }});")
            return "".join(codes)
        else:
            return f"window.Dars.watch('{self.state_path}', function() {{ {self.callback_code} }});"


def useWatch(state_path: str | list[str], *js_helpers):
    """
    Watch a state property (or list of properties) and execute callback(s) when it changes.
    
    Usage with app.add_script():
        app.add_script(useWatch("user.name", log("Name changed!")))
        
    Usage with multiple states:
        app.add_script(useWatch(["user.name", "user.email"], log("Contact info changed!")))
        
    Usage with multiple callbacks:
        app.add_script(useWatch("user.name", log("Name changed!"), alert("Update!")))
    
    The returned WatchMarker has a get_code() method that generates the JavaScript.
    """
    # Convert js_helpers to actual JavaScript code
    callback_parts = []
    
    def process_helper(helper):
        if isinstance(helper, list):
            for item in helper:
                process_helper(item)
        elif hasattr(helper, 'get_code'):
            # It's a dScript or similar object
            callback_parts.append(helper.get_code())
        else:
            # It's a string or something else
            callback_parts.append(str(helper))

    for helper in js_helpers:
        process_helper(helper)
    
    # Join with semicolons to ensure valid JS if multiple statements are concatenated
    # (though dScript usually handles this, extra safety doesn't hurt)
    callback_code = "".join(callback_parts)
    return WatchMarker(state_path, callback_code)
