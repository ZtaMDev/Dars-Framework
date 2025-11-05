from dars.all import *
from dars.core.component import Component
from dars.exporters.web.html_css_js import HTMLCSSJSExporter as Exporter
class CustomSect(Component):
    def __init__(self, id: str = None, **props):
        super().__init__(**props)
        
        self.id = id
        
        self.set_event(EventTypes.CLICK, dScript("console.log('click')"))
        
    def render(self, exporter: 'Exporter') -> str:
        # Usar el exporter para renderizar hijos consistentemente
        hijos_html = self.render_children(exporter)
        return f'''
        <div class="mi-componente" id="{self.id}">
            <h2>HI</h2>
            <div class="contenido">
                {hijos_html}
            </div>
        </div>
        '''