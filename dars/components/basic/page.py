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
    """
    Root component for individual pages in a Dars application.
    
    Props:
    - ***children** (Component): Positional arguments for child components to be rendered in the page.
    - **id** (str): Unique identifier for the component.
    - **class_name** (str): String containing regular CSS class names.
    - **style** (dict): Optional dictionary for CSS utility classes (prefer `style`).
    - **Events**: Handlers like `on_click`, `on_mouse_enter`, etc.
    
    Example:
    ```python
    Page(
        Navbar(),
        Container(
            Text("Home Page", class_name="text-4xl font-bold"),
            class_name="max-w-7xl mx-auto py-12"
        ),
        Footer(),
        class_name="bg-white"
    )
    ```
    """
    def __init__(self, *children: Component, id: Any = None, class_name: Any = None, style: Optional[Dict[str, Any] | str] = None, **props):
        super().__init__(id=id, class_name=class_name, style=style, **props)
        self.scripts = []
        for child in children:
            self.add_child(child)

    def add_script(self, script):
        """
        Adds a script to this page.
        
        Supports multiple script types:
        
        - **DScript**: Direct Python function compilation to JavaScript
        - **String**: Inline JavaScript code
        - **Dictionary**: Raw script object (fallback)
        - **Utility Chains**: DAP utility functions with promise-based chaining
        
        **Script Types:**
        
        1. **DScript** - Compile Python to JavaScript:
           ```python
           page.add_script(dScript(file_path="script.js"))
           ```
        
        2. **Inline JavaScript**:
           ```python
           page.add_script("console.log('Page loaded');")
           ```
        
        3. **Utility Functions** - Chain DAP commands:
           ```python
           from dars.scripts.utils_ds import setTimeout, addClass, log
           
           # Sequential animations with promise chaining
           page.add_script(
               setTimeout(5, addClass("logo", "show"))
               .then(setTimeout(350, addClass("title", "show")))
               .then(setTimeout(650, addClass("description", "show")))
           )
           ```
        
        4. **useWatch** - React to state changes:
           ```python
           page.add_script(
               useWatch("user.name", log("Name changed!"))
           )
           ```
        
        **Common Utilities:**
        
        - **setTimeout(ms, action)**: Execute action after delay (returns Promise)
        - **addClass(id, class)**: Add CSS class to element
        - **removeClass(id, class)**: Remove CSS class
        - **toggleClass(id, class)**: Toggle CSS class
        - **log(msg)**: Log to console
        - **navigate(url)**: Navigate to URL
        - **createComp(target, root)**: Dynamically create components
        - **updateComp(id, props)**: Update component properties
        - **deleteComp(id)**: Remove component from DOM
        
        **Promise Chaining:**
        
        All timeout/async utilities return Promises, allowing sequential execution:
        
        ```python
        page.add_script(
            setTimeout(100, log("Step 1"))
            .then(setTimeout(200, log("Step 2")))
            .then(setTimeout(300, log("Step 3")))
        )
        ```
        
        Returns self to allow method chaining.
        """
        self.scripts.append(script)

    def useWatch(self, state_path: Any, *js_helpers):
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

    def setup_auth(self, verify_credentials_callback, secret: Any, auth_id: Any = None):
        """
        Configures an isolated auth setup for this specific page.
        """
        from dars.backend.auth_routes import register_auth_config
        if auth_id is None:
            auth_id = f"page_{self.id or id(self)}"
        
        register_auth_config(verify_credentials_callback, secret, auth_id)
        self._auth_id = auth_id
        
        metadata = getattr(self, '__dars_route_metadata__', None)
        if metadata:
            metadata.requires_auth = True
            metadata.auth_id = auth_id
            
        return self

    def get_scripts(self):
        return self.scripts

    def render(self, exporter: Any) -> str:
        # El método render será implementado por el exporter
        raise NotImplementedError("El método render debe ser implementado por el exporter")
