from dars.exporters.base import Exporter
from dars.core.app import App
from dars.core.component import Component
from dars.components.basic.text import Text
from dars.components.basic.button import Button
from dars.components.basic.input import Input
from dars.components.basic.container import Container
from dars.components.basic.image import Image
from dars.components.basic.link import Link
from dars.components.basic.textarea import Textarea
from dars.components.basic.checkbox import Checkbox
from dars.components.basic.radiobutton import RadioButton
from dars.components.basic.select import Select
from dars.components.basic.slider import Slider
from dars.components.basic.datepicker import DatePicker
from dars.components.advanced.card import Card
from dars.components.advanced.modal import Modal
from dars.components.advanced.navbar import Navbar
from typing import Dict, Any
import os
from bs4 import BeautifulSoup

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
        """Genera el contenido HTML con todas las propiedades de la aplicación"""
        body_content = ""
        if app.root:
            body_content = self.render_component(app.root)
        
        # Generar meta tags
        meta_tags_html = self._generate_meta_tags(app)
        
        # Generar links (favicon, manifest, etc.)
        links_html = self._generate_links(app)
        
        # Generar Open Graph tags
        og_tags_html = self._generate_open_graph_tags(app)
        
        # Generar Twitter Card tags
        twitter_tags_html = self._generate_twitter_tags(app)
        
        html_template = f"""<!DOCTYPE html>
<html lang="{app.language}">
<head>
    <meta charset="{app.config.get('charset', 'UTF-8')}">
    {meta_tags_html}
    <title>{app.title}</title>
    {links_html}
    {og_tags_html}
    {twitter_tags_html}
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    {body_content}
    <script src="script.js"></script>
</body>
</html>"""
        soup = BeautifulSoup(html_template, "html.parser")
        return soup.prettify()
    
    def _generate_meta_tags(self, app: App) -> str:
        """Genera todos los meta tags de la aplicación"""
        meta_tags = app.get_meta_tags()
        meta_html = []
        
        for name, content in meta_tags.items():
            if content:
                meta_html.append(f'    <meta name="{name}" content="{content}">')
        
        # Añadir canonical URL si está configurado
        if app.canonical_url:
            meta_html.append(f'    <link rel="canonical" href="{app.canonical_url}">')
        
        return '\n'.join(meta_html)
    
    def _generate_links(self, app: App) -> str:
        """Genera todos los links (favicon, manifest, iconos)"""
        links = []
        
        # Favicon
        if app.favicon:
            links.append(f'    <link rel="icon" type="image/x-icon" href="{app.favicon}">')
        
        # Icono principal
        if app.icon:
            links.append(f'    <link rel="icon" type="image/png" href="{app.icon}">')
        
        # Apple Touch Icon
        if app.apple_touch_icon:
            links.append(f'    <link rel="apple-touch-icon" href="{app.apple_touch_icon}">')
        
        # PWA Manifest
        if app.manifest:
            links.append(f'    <link rel="manifest" href="{app.manifest}">')
        
        return '\n'.join(links)
    
    def _generate_open_graph_tags(self, app: App) -> str:
        """Genera todos los tags Open Graph para redes sociales"""
        og_tags = app.get_open_graph_tags()
        og_html = []
        
        for property_name, content in og_tags.items():
            if content:
                og_html.append(f'    <meta property="{property_name}" content="{content}">')
        
        return '\n'.join(og_html)
    
    def _generate_twitter_tags(self, app: App) -> str:
        """Genera todos los tags de Twitter Card"""
        twitter_tags = app.get_twitter_tags()
        twitter_html = []
        
        for name, content in twitter_tags.items():
            if content:
                twitter_html.append(f'    <meta name="{name}" content="{content}">')
        
        return '\n'.join(twitter_html)
        
    def generate_css(self, app: App) -> str:
        """Genera el contenido CSS"""
        css_content = """/* Estilos base de Dars */
* {
    box-sizing: border-box;
}

body {
    margin: 0;
    padding: 0;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
}

/* Estilos de componentes Dars */
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

.dars-image {
    max-width: 100%;
    height: auto;
}

.dars-link {
    color: #007bff;
    text-decoration: none;
}

.dars-link:hover {
    text-decoration: underline;
}

.dars-textarea {
    width: 100%;
    padding: 8px 12px;
    border: 1px solid #ccc;
    border-radius: 4px;
    font-size: 14px;
}

.dars-textarea:focus {
    outline: none;
    border-color: #007bff;
    box-shadow: 0 0 0 2px rgba(0, 123, 255, 0.25);
}

.dars-card {
    background-color: white;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    padding: 20px;
    margin-bottom: 20px;
}

.dars-card h2 {
    margin-top: 0;
    margin-bottom: 15px;
    font-size: 24px;
    color: #333;
}

.dars-modal {
    display: none; /* Hidden by default */
    position: fixed; /* Stay in place */
    z-index: 1; /* Sit on top */
    left: 0;
    top: 0;
    width: 100%; /* Full width */
    height: 100%; /* Full height */
    overflow: auto; /* Enable scroll if needed */
    background-color: rgba(0,0,0,0.4); /* Black w/ opacity */
    justify-content: center;
    align-items: center;
}

.dars-modal-content {
    background-color: #fefefe;
    margin: auto;
    padding: 20px;
    border: 1px solid #888;
    width: 80%;
    max-width: 500px;
    border-radius: 8px;
    box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2), 0 6px 20px 0 rgba(0,0,0,0.19);
}

.dars-navbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1rem;
    background-color: #f8f9fa;
    border-bottom: 1px solid #dee2e6;
}

.dars-navbar-brand {
    font-weight: bold;
    font-size: 1.25rem;
    color: #333;
}

.dars-navbar-nav {
    display: flex;
    gap: 1rem;
}

.dars-navbar-nav a {
    color: #007bff;
    text-decoration: none;
    padding: 0.5rem 1rem;
}

.dars-navbar-nav a:hover {
    background-color: #e9ecef;
    border-radius: 4px;
}

/* Estilos para nuevos componentes básicos */

/* Checkbox */
.dars-checkbox-wrapper {
    display: flex;
    align-items: center;
    gap: 8px;
    margin: 4px 0;
}

.dars-checkbox {
    width: 16px;
    height: 16px;
    cursor: pointer;
}

.dars-checkbox:disabled {
    opacity: 0.6;
    cursor: not-allowed;
}

.dars-checkbox-wrapper label {
    cursor: pointer;
    user-select: none;
}

/* RadioButton */
.dars-radio-wrapper {
    display: flex;
    align-items: center;
    gap: 8px;
    margin: 4px 0;
}

.dars-radio {
    width: 16px;
    height: 16px;
    cursor: pointer;
}

.dars-radio:disabled {
    opacity: 0.6;
    cursor: not-allowed;
}

.dars-radio-wrapper label {
    cursor: pointer;
    user-select: none;
}

/* Select */
.dars-select {
    display: inline-block;
    padding: 8px 12px;
    border: 1px solid #ccc;
    border-radius: 4px;
    font-size: 14px;
    background-color: white;
    cursor: pointer;
    min-width: 120px;
}

.dars-select:focus {
    outline: none;
    border-color: #007bff;
    box-shadow: 0 0 0 2px rgba(0, 123, 255, 0.25);
}

.dars-select:disabled {
    opacity: 0.6;
    cursor: not-allowed;
    background-color: #f8f9fa;
}

.dars-select option:disabled {
    color: #6c757d;
}

/* Slider */
.dars-slider-wrapper {
    display: flex;
    align-items: center;
    gap: 12px;
    margin: 8px 0;
}

.dars-slider-wrapper.dars-slider-vertical {
    flex-direction: column;
    align-items: stretch;
}

.dars-slider {
    flex: 1;
    cursor: pointer;
}

.dars-slider-horizontal .dars-slider {
    width: 100%;
    height: 6px;
}

.dars-slider-vertical .dars-slider {
    width: 6px;
    height: 100px;
    writing-mode: bt-lr; /* IE */
    -webkit-appearance: slider-vertical; /* WebKit */
}

.dars-slider:disabled {
    opacity: 0.6;
    cursor: not-allowed;
}

.dars-slider-value {
    font-weight: bold;
    min-width: 40px;
    text-align: center;
    padding: 4px 8px;
    background-color: #f8f9fa;
    border-radius: 4px;
    font-size: 12px;
}

.dars-slider-wrapper label {
    font-weight: 500;
    margin-bottom: 4px;
}

/* DatePicker */
.dars-datepicker {
    display: inline-block;
    padding: 8px 12px;
    border: 1px solid #ccc;
    border-radius: 4px;
    font-size: 14px;
    background-color: white;
    cursor: pointer;
}

.dars-datepicker:focus {
    outline: none;
    border-color: #007bff;
    box-shadow: 0 0 0 2px rgba(0, 123, 255, 0.25);
}

.dars-datepicker:disabled {
    opacity: 0.6;
    cursor: not-allowed;
    background-color: #f8f9fa;
}

.dars-datepicker:readonly {
    background-color: #f8f9fa;
    cursor: default;
}

.dars-datepicker-inline {
    display: inline-block;
    border: 1px solid #ccc;
    border-radius: 4px;
    padding: 12px;
    background-color: white;
}

.dars-datepicker-inline .dars-datepicker {
    border: none;
    padding: 0;
}

"""
        
        # Agregar estilos globales de la aplicación definidos por el usuario
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
        elif isinstance(component, Image):
            return self.render_image(component)
        elif isinstance(component, Link):
            return self.render_link(component)
        elif isinstance(component, Textarea):
            return self.render_textarea(component)
        elif isinstance(component, Checkbox):
            return self.render_checkbox(component)
        elif isinstance(component, RadioButton):
            return self.render_radiobutton(component)
        elif isinstance(component, Select):
            return self.render_select(component)
        elif isinstance(component, Slider):
            return self.render_slider(component)
        elif isinstance(component, DatePicker):
            return self.render_datepicker(component)
        elif isinstance(component, Card):
            return self.render_card(component)
        elif isinstance(component, Modal):
            return self.render_modal(component)
        elif isinstance(component, Navbar):
            return self.render_navbar(component)
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
        
    def render_image(self, image: Image) -> str:
        """Renderiza un componente Image"""
        component_id = self.generate_unique_id(image)
        class_attr = f'class="dars-image {image.class_name or ""}"'
        style_attr = f'style="{self.render_styles(image.style)}"' if image.style else ""
        width_attr = f'width="{image.width}"' if image.width else ""
        height_attr = f'height="{image.height}"' if image.height else ""

        return f'<img id="{component_id}" src="{image.src}" alt="{image.alt}" {width_attr} {height_attr} {class_attr} {style_attr} />'

    def render_link(self, link: Link) -> str:
        """Renderiza un componente Link"""
        component_id = self.generate_unique_id(link)
        class_attr = f'class="dars-link {link.class_name or ""}"'
        style_attr = f'style="{self.render_styles(link.style)}"' if link.style else ""
        target_attr = f'target="{link.target}"'

        return f'<a id="{component_id}" href="{link.href}" {target_attr} {class_attr} {style_attr}>{link.text}</a>'

    def render_textarea(self, textarea: Textarea) -> str:
        """Renderiza un componente Textarea"""
        component_id = self.generate_unique_id(textarea)
        class_attr = f'class="dars-textarea {textarea.class_name or ""}"'
        style_attr = f'style="{self.render_styles(textarea.style)}"' if textarea.style else ""
        rows_attr = f'rows="{textarea.rows}"'
        cols_attr = f'cols="{textarea.cols}"'
        placeholder_attr = f'placeholder="{textarea.placeholder}"' if textarea.placeholder else ""
        disabled_attr = "disabled" if textarea.disabled else ""
        readonly_attr = "readonly" if textarea.readonly else ""
        required_attr = "required" if textarea.required else ""
        maxlength_attr = f'maxlength="{textarea.max_length}"' if textarea.max_length else ""

        attrs = [class_attr, style_attr, rows_attr, cols_attr, placeholder_attr,
                 disabled_attr, readonly_attr, required_attr, maxlength_attr]
        attrs_str = " ".join(attr for attr in attrs if attr)

        return f'<textarea id="{component_id}" {attrs_str}>{textarea.value}</textarea>'

    def render_card(self, card: Card) -> str:
        """Renderiza un componente Card"""
        component_id = self.generate_unique_id(card)
        class_attr = f'class="dars-card {card.class_name or ""}"'
        style_attr = f'style="{self.render_styles(card.style)}"' if card.style else ""
        title_html = f'<h2>{card.title}</h2>' if card.title else ""
        children_html = ""
        for child in card.children:
            children_html += self.render_component(child)

        return f'<div id="{component_id}" {class_attr} {style_attr}>{title_html}{children_html}</div>'

    def render_modal(self, modal: Modal) -> str:
        """Renderiza un componente Modal"""
        component_id = self.generate_unique_id(modal)
        class_attr = f'class="dars-modal {modal.class_name or ""}"'
        style_attr = f'style="{self.render_styles(modal.style)}"' if modal.style else ""
        title_html = f'<h2>{modal.title}</h2>' if modal.title else ""
        children_html = ""
        for child in modal.children:
            children_html += self.render_component(child)

        display_style = "display: flex;" if modal.is_open else "display: none;"
        modal_overlay_style = f'style="{display_style} position: fixed; top: 0; left: 0; width: 100%; height: 100%; background-color: rgba(0,0,0,0.5); justify-content: center; align-items: center; z-index: 1000; {style_attr}"'

        return f'<div id="{component_id}" {class_attr} {modal_overlay_style}>\n    <div class="dars-modal-content" style="background: white; padding: 20px; border-radius: 8px; max-width: 500px; width: 90%;">\n        {title_html}\n        {children_html}\n    </div>\n</div>'

    def render_navbar(self, navbar: Navbar) -> str:
        """Renderiza un componente Navbar"""
        component_id = self.generate_unique_id(navbar)
        class_attr = f'class="dars-navbar {navbar.class_name or ""}"'
        style_attr = f'style="{self.render_styles(navbar.style)}"' if navbar.style else ""
        brand_html = f'<div class="dars-navbar-brand">{navbar.brand}</div>' if navbar.brand else ""
        children_html = ""
        for child in navbar.children:
            children_html += self.render_component(child)

        return f'<nav id="{component_id}" {class_attr} {style_attr}>{brand_html}<div class="dars-navbar-nav">{children_html}</div></nav>'

    def render_checkbox(self, checkbox: Checkbox) -> str:
        """Renderiza un componente Checkbox"""
        component_id = self.generate_unique_id(checkbox)
        class_attr = f'class="dars-checkbox {checkbox.class_name or ""}"'
        style_attr = f'style="{self.render_styles(checkbox.style)}"' if checkbox.style else ""
        checked_attr = "checked" if checkbox.checked else ""
        disabled_attr = "disabled" if checkbox.disabled else ""
        required_attr = "required" if checkbox.required else ""
        name_attr = f'name="{checkbox.name}"' if checkbox.name else ""
        value_attr = f'value="{checkbox.value}"' if checkbox.value else ""
        
        attrs = [class_attr, style_attr, checked_attr, disabled_attr, required_attr, name_attr, value_attr]
        attrs_str = " ".join(attr for attr in attrs if attr)
        
        label_html = f'<label for="{component_id}">{checkbox.label}</label>' if checkbox.label else ""
        
        return f'<div class="dars-checkbox-wrapper"><input type="checkbox" id="{component_id}" {attrs_str}>{label_html}</div>'

    def render_radiobutton(self, radio: RadioButton) -> str:
        """Renderiza un componente RadioButton"""
        component_id = self.generate_unique_id(radio)
        class_attr = f'class="dars-radio {radio.class_name or ""}"'
        style_attr = f'style="{self.render_styles(radio.style)}"' if radio.style else ""
        checked_attr = "checked" if radio.checked else ""
        disabled_attr = "disabled" if radio.disabled else ""
        required_attr = "required" if radio.required else ""
        name_attr = f'name="{radio.name}"'
        value_attr = f'value="{radio.value}"'
        
        attrs = [class_attr, style_attr, checked_attr, disabled_attr, required_attr, name_attr, value_attr]
        attrs_str = " ".join(attr for attr in attrs if attr)
        
        label_html = f'<label for="{component_id}">{radio.label}</label>' if radio.label else ""
        
        return f'<div class="dars-radio-wrapper"><input type="radio" id="{component_id}" {attrs_str}>{label_html}</div>'

    def render_select(self, select: Select) -> str:
        """Renderiza un componente Select"""
        component_id = self.generate_unique_id(select)
        class_attr = f'class="dars-select {select.class_name or ""}"'
        style_attr = f'style="{self.render_styles(select.style)}"' if select.style else ""
        disabled_attr = "disabled" if select.disabled else ""
        required_attr = "required" if select.required else ""
        multiple_attr = "multiple" if select.multiple else ""
        size_attr = f'size="{select.size}"' if select.size else ""
        
        attrs = [class_attr, style_attr, disabled_attr, required_attr, multiple_attr, size_attr]
        attrs_str = " ".join(attr for attr in attrs if attr)
        
        # Generar opciones
        options_html = ""
        if select.placeholder and not select.multiple:
            selected = "selected" if not select.value else ""
            options_html += f'<option value="" disabled {selected}>{select.placeholder}</option>'
        
        for option in select.options:
            selected = "selected" if option.value == select.value else ""
            disabled = "disabled" if option.disabled else ""
            options_html += f'<option value="{option.value}" {selected} {disabled}>{option.label}</option>'
        
        return f'<select id="{component_id}" {attrs_str}>{options_html}</select>'

    def render_slider(self, slider: Slider) -> str:
        """Renderiza un componente Slider"""
        component_id = self.generate_unique_id(slider)
        class_attr = f'class="dars-slider {slider.class_name or ""}"'
        style_attr = f'style="{self.render_styles(slider.style)}"' if slider.style else ""
        disabled_attr = "disabled" if slider.disabled else ""
        min_attr = f'min="{slider.min_value}"'
        max_attr = f'max="{slider.max_value}"'
        value_attr = f'value="{slider.value}"'
        step_attr = f'step="{slider.step}"'
        
        attrs = [class_attr, style_attr, disabled_attr, min_attr, max_attr, value_attr, step_attr]
        attrs_str = " ".join(attr for attr in attrs if attr)
        
        label_html = f'<label for="{component_id}">{slider.label}</label>' if slider.label else ""
        value_display = f'<span class="dars-slider-value">{slider.value}</span>' if slider.show_value else ""
        
        wrapper_class = "dars-slider-vertical" if slider.orientation == "vertical" else "dars-slider-horizontal"
        
        return f'<div class="dars-slider-wrapper {wrapper_class}">{label_html}<input type="range" id="{component_id}" {attrs_str}>{value_display}</div>'

    def render_datepicker(self, datepicker: DatePicker) -> str:
        """Renderiza un componente DatePicker"""
        component_id = self.generate_unique_id(datepicker)
        class_attr = f'class="dars-datepicker {datepicker.class_name or ""}"'
        style_attr = f'style="{self.render_styles(datepicker.style)}"' if datepicker.style else ""
        disabled_attr = "disabled" if datepicker.disabled else ""
        required_attr = "required" if datepicker.required else ""
        readonly_attr = "readonly" if datepicker.readonly else ""
        value_attr = f'value="{datepicker.value}"' if datepicker.value else ""
        placeholder_attr = f'placeholder="{datepicker.placeholder}"' if datepicker.placeholder else ""
        min_attr = f'min="{datepicker.min_date}"' if datepicker.min_date else ""
        max_attr = f'max="{datepicker.max_date}"' if datepicker.max_date else ""
        
        # Determinar el tipo de input según si incluye tiempo
        input_type = "datetime-local" if datepicker.show_time else "date"
        
        attrs = [class_attr, style_attr, disabled_attr, required_attr, readonly_attr, 
                value_attr, placeholder_attr, min_attr, max_attr]
        attrs_str = " ".join(attr for attr in attrs if attr)
        
        # Si es inline, usar un div contenedor adicional
        if datepicker.inline:
            return f'<div class="dars-datepicker-inline"><input type="{input_type}" id="{component_id}" {attrs_str}></div>'
        else:
            return f'<input type="{input_type}" id="{component_id}" {attrs_str}>'

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


