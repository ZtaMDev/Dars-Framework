from dars.components.basic.container import Container

class Outlet(Container):
    """
    Routing placeholder component for Single Page Applications (SPA).
    Acts as the target where child routes will be dynamically rendered based on the URL.
    
    Props:
    - **outlet_id** (str): Unique identifier for the outlet (defaults to `"main"`).
    - **placeholder** (Component): Component to display while the route content is being loaded.
    - ***children** (Component): Initial content for the outlet if no route is matched.
    - **id** (str): Unique identifier for the component.
    - **class_name** (str): String containing CSS utility classes (e.g., `"flex-1 p-6 bg-slate-50 min-h-screen overflow-y-auto"`).
    - **style** (dict): Optional dictionary for direct inline styles (prefer `class_name`).
    - **Events**: Handlers for navigation and lifecycle events.
    
    Example:
    ```python
    Outlet(
        outlet_id="main-view",
        placeholder=Spinner(class_name="m-auto"),
        class_name="w-full h-full"
    )
    ```
    """
    def __init__(self, outlet_id: str = "main", placeholder=None, *children, **props):
        if placeholder is None and ('loading' in props):
            placeholder = props.pop('loading')

        if (not children) and (placeholder is not None):
            if isinstance(placeholder, list):
                children = tuple(placeholder)
            else:
                children = (placeholder,)

        super().__init__(*children, **props)
        self.props["data-dars-outlet"] = "true"
        try:
            self.props["data-dars-outlet-id"] = str(outlet_id or "main")
        except Exception:
            self.props["data-dars-outlet-id"] = "main"
        base_cls = (getattr(self, "class_name", "") or "").strip()
        self.class_name = ("dars-outlet " + base_cls).strip()
