from dars.components.basic.container import Container

class Outlet(Container):
    """
    Outlet component for nested SPA routing.
    Acts as a placeholder where child routes will be rendered.
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
