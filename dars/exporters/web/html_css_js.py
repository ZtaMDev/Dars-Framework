from dars.exporters.base import Exporter
from dars.core.app import App
from dars.core.component import Component
from dars.components.basic.text import Text
from dars.components.basic.button import Button
from dars.components.basic.input import Input
from dars.components.basic.container import Container
from typing import Dict, Any
import os

class HTMLCSSJSExporter(Exporter):
    """Exportador para HTML, CSS y JavaScript"""
    
    def get_platform(self) -> str:
        return "html"
        
    def export(self, app: App, output_path: str) -> bool:
        """Exporta la aplicación a HTML/CSS/JS"""
        try:
            self.create_output_directory(output_path)
            
            # Generar HTML
            html_content = self.generate_html(app)
            self.write_file(os.path.join(output_path, "index.html"), html_content)
            
            # Generar CSS
            css_content = self.generate_css(app)
            self.write_file(os.path.join(output_path, "styles.css"), css_content)
            
            # Generar JavaScript
            js_content = self.generate_javascript(app)
            self.write_file(os.path.join(output_path, "script.js"), js_content)
            
            return True
        except Exception as e:
            print(f"Error al exportar: {e}")
            return False
            
    def generate_html(self, app: App) -> str:
        """Genera el contenido HTML"""
        body_content = ""
        if app.root:
            body_content = self.render_component(app.root)
            
        html_template = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{app.title}</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    {body_content}
    <script src="script.js"></script>
</body>
</html>"""
        return html_template
        
    def generate_css(self, app: App) -> str:
        """Genera el contenido CSS"""
        css_content = """/* Estilos base */
* {
    box-sizing: border-box;
}

body {
    margin: 0;
    padding: 0;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
}

/* Estilos de componentes */
.dars-container {
    display: block;
}

.dars-text {
    display: inline-block;
}

.dars-button {
    display: inline-block;
    padding: 8px 16px;
    border: 1px solid #ccc;
    background-color: #f8f9fa;
    color: #333;
    cursor: pointer;
    border-radius: 4px;
    font-size: 14px;
}

.dars-button:hover {
    background-color: #e9ecef;
}

.dars-button:disabled {
    opacity: 0.6;
    cursor: not-allowed;
}

.dars-input {
    display: inline-block;
    padding: 8px 12px;
    border: 1px solid #ccc;
    border-radius: 4px;
    font-size: 14px;
}

.dars-input:focus {
    outline: none;
    border-color: #007bff;
    box-shadow: 0 0 0 2px rgba(0, 123, 255, 0.25);
}

"""
        
        # Agregar estilos globales de la aplicación
        for selector, styles in app.global_styles.items():
            css_content += f"{selector} {{\n"
            css_content += f"    {self.render_styles(styles)}\n"
            css_content += "}\n\n"
            
        return css_content
        
    def generate_javascript(self, app: App) -> str:
        """Genera el contenido JavaScript"""
        js_content = """// Dars Runtime
document.addEventListener('DOMContentLoaded', function() {
    console.log('Dars App loaded');
    
    // Inicializar eventos de componentes
    initializeEvents();
});

function initializeEvents() {
    // Los eventos específicos se agregarán aquí
}

"""
        
        # Agregar scripts de la aplicación
        for script in app.scripts:
            js_content += f"// Script: {script.__class__.__name__}\n"
            js_content += script.get_code()
            js_content += "\n\n"
            
        return js_content
        
    def render_component(self, component: Component) -> str:
        """Renderiza un componente a HTML"""
        if isinstance(component, Text):
            return self.render_text(component)
        elif isinstance(component, Button):
            return self.render_button(component)
        elif isinstance(component, Input):
            return self.render_input(component)
        elif isinstance(component, Container):
            return self.render_container(component)
        else:
            # Componente genérico
            return self.render_generic_component(component)
            
    def render_text(self, text: Text) -> str:
        """Renderiza un componente Text"""
        component_id = self.generate_unique_id(text)
        class_attr = f'class="dars-text {text.class_name or ""}"'
        style_attr = f'style="{self.render_styles(text.style)}"' if text.style else ""
        
        return f'<span id="{component_id}" {class_attr} {style_attr}>{text.text}</span>'
        
    def render_button(self, button: Button) -> str:
        """Renderiza un componente Button"""
        component_id = self.generate_unique_id(button)
        class_attr = f'class="dars-button {button.class_name or ""}"'
        style_attr = f'style="{self.render_styles(button.style)}"' if button.style else ""
        disabled_attr = "disabled" if button.disabled else ""
        type_attr = f'type="{button.button_type}"'
        
        return f'<button id="{component_id}" {class_attr} {style_attr} {type_attr} {disabled_attr}>{button.text}</button>'
        
    def render_input(self, input_comp: Input) -> str:
        """Renderiza un componente Input"""
        component_id = self.generate_unique_id(input_comp)
        class_attr = f'class="dars-input {input_comp.class_name or ""}"'
        style_attr = f'style="{self.render_styles(input_comp.style)}"' if input_comp.style else ""
        type_attr = f'type="{input_comp.input_type}"'
        value_attr = f'value="{input_comp.value}"' if input_comp.value else ""
        placeholder_attr = f'placeholder="{input_comp.placeholder}"' if input_comp.placeholder else ""
        disabled_attr = "disabled" if input_comp.disabled else ""
        readonly_attr = "readonly" if input_comp.readonly else ""
        required_attr = "required" if input_comp.required else ""
        
        attrs = [class_attr, style_attr, type_attr, value_attr, placeholder_attr, 
                disabled_attr, readonly_attr, required_attr]
        attrs_str = " ".join(attr for attr in attrs if attr)
        
        return f'<input id="{component_id}" {attrs_str} />'
        
    def render_container(self, container: Container) -> str:
        """Renderiza un componente Container"""
        component_id = self.generate_unique_id(container)
        class_attr = f'class="dars-container {container.class_name or ""}"'
        style_attr = f'style="{self.render_styles(container.style)}"' if container.style else ""
        
        # Renderizar hijos
        children_html = ""
        for child in container.children:
            children_html += self.render_component(child)
            
        return f'<div id="{component_id}" {class_attr} {style_attr}>{children_html}</div>'
        
    def render_generic_component(self, component: Component) -> str:
        """Renderiza un componente genérico"""
        component_id = self.generate_unique_id(component)
        class_attr = f'class="{component.class_name or ""}"'
        style_attr = f'style="{self.render_styles(component.style)}"' if component.style else ""
        
        # Renderizar hijos
        children_html = ""
        for child in component.children:
            children_html += self.render_component(child)
            
        return f'<div id="{component_id}" {class_attr} {style_attr}>{children_html}</div>'

