"""
useWatch Hook

Enables watching state changes and executing callbacks.
"""

class WatchMarker:
    """
    Represents a watcher script.
    Works with app.add_script() and page.add_script().
    """
    
    def __init__(self, state_path: str, callback_code: str):
        """
        Initialize a watch marker.
        
        Args:
            state_path: Dot-notation path to state property (e.g., "user.name")
            callback_code: JavaScript code to execute when state changes
        """
        self.state_path = state_path
        self.callback_code = callback_code
        self.code = self.get_code()
    
    def get_code(self):
        """Return the JavaScript code for this watcher"""
        return f"window.Dars.watch('{self.state_path}', function() {{ {self.callback_code} }});"


def useWatch(state_path: str, *js_helpers):
    """
    Watch a state property and execute callback when it changes.
    
    Usage with app.add_script():
        app.add_script(useWatch("user.name", log("Name changed!")))
    
    Usage with page.add_script():
        page.add_script(useWatch("user.name", log("Name changed!")))
        
    Usage with app.useWatch() (convenience):
        app.useWatch("user.name", log("Name changed!"))
        
    Usage with page.useWatch() (convenience):
        page.useWatch("user.name", log("Name changed!"))
    
    The returned WatchMarker has a get_code() method that generates the JavaScript.
    """
    # Convert js_helpers to actual JavaScript code
    callback_parts = []
    for helper in js_helpers:
        if hasattr(helper, 'get_code'):
            # It's a dScript or similar object
            callback_parts.append(helper.get_code())
        else:
            # It's a string or something else
            callback_parts.append(str(helper))
    
    callback_code = "".join(callback_parts)
    return WatchMarker(state_path, callback_code)
