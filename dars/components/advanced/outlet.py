from dars.components.basic.container import Container

class Outlet(Container):
    """
    Outlet component for nested SPA routing.
    Acts as a placeholder where child routes will be rendered.
    """
    def __init__(self, **props):
        super().__init__(**props)
        self.props["data-dars-outlet"] = "true"
        self.class_name = "dars-outlet " + props.get("class_name", "")
