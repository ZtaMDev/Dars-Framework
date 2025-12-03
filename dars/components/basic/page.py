# Dars Framework - Core Source File
#
# This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0.
# If a copy of the MPL was not distributed with this file, You can obtain one at
# https://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2025 ZtaDev
from dars.core.component import Component
from typing import Optional, Dict, Any, List

class Page(Component):
    """Root component for pages in Dars multipage apps. Allows passing children as positional arguments and scripts per page."""
    def __init__(self, *children: Component, id: Optional[str] = None, class_name: Optional[str] = None, style: Optional[Dict[str, Any]] = None, **props):
        super().__init__(id=id, class_name=class_name, style=style, **props)
        self.scripts = []
        for child in children:
            self.add_child(child)

    def add_script(self, script):
        self.scripts.append(script)

    def useWatch(self, state_path: str, *js_helpers):
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
        from dars.hooks.use_watch import useWatch
        watcher = useWatch(state_path, *js_helpers)
        self.add_script(watcher)
        return self

    def get_scripts(self):
        return self.scripts

    def render(self, exporter: Any) -> str:
        # El método render será implementado por el exporter
        raise NotImplementedError("El método render debe ser implementado por el exporter")
