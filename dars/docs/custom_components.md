This is an example of how to create a custom component in Dars. The `Button` class inherits from `Component` and defines its own initialization and rendering logic. You can use `self.set_event` to attach event handlers to components.

> Note: when you instance a CustomComponent you need to do it like this CustomComponent(id="") <-- with parentesis

```python
from dars.all import *
from dars.core.component import Component
from dars.exporters.web.html_css_js import *

class CustomComponent(Component):
    def __init__(self, title: str, id: str = None, **props):
        super().__init__(**props)
        
        self.title = title
        self.id = id
        self.set_event(EventTypes.CLICK, dScript("console.log('click')"))
    def render(self, exporter: 'Exporter') -> str:
        # Use the exporter to consistently render children
        children_html = self.render_children(exporter)
        return f'''
        <div class="my-component" id="{self.id}">
            <h2>{self.title}</h2>
            <div class="content">
                {children_html}
            </div>
        </div>
        '''
```


