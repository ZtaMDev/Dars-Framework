from dars.core.component import Component
from typing import List, Optional

class Tabs(Component):
    """
    Componente de navegación por pestañas.
    tabs: Lista de títulos de pestañas
    panels: Lista de componentes o strings (contenido de cada pestaña)
    selected: Índice de la pestaña activa (opcional)
    """
    def __init__(self, tabs: List[str], panels: List[Component], selected: Optional[int]=0, minimum_logic: bool = True, **props):
        super().__init__(**props)
        self.tabs = tabs
        self.panels = panels
        self.selected = selected or 0
        self.minimum_logic = minimum_logic
        for panel in panels:
            if hasattr(panel, 'render'):
                self.add_child(panel)

    def render(self) -> str:
        tab_headers = ''.join(
            f'<button class="dars-tab{ " dars-tab-active" if i == self.selected else "" }" data-tab="{i}">{title}</button>'
            for i, title in enumerate(self.tabs)
        )
        panels_html = ''.join(
            f'<div class="dars-tab-panel{ " dars-tab-panel-active" if i == self.selected else "" }">{panel.render() if hasattr(panel, "render") else panel}</div>'
            for i, panel in enumerate(self.panels)
        )
        return f'<div class="dars-tabs"><div class="dars-tabs-header">{tab_headers}</div><div class="dars-tabs-panels">{panels_html}</div></div>'
