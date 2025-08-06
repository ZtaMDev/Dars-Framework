from dars.core.component import Component

class Spinner(Component):
    """
    Indicador de carga circular (spinner).
    """
    def __init__(self, **props):
        super().__init__(**props)

    def render(self) -> str:
        return '<div class="dars-spinner"></div>'
