#!/usr/bin/env python3
"""
Template: Aplicación Web Moderna con Propiedades Extendidas
===========================================================

Este template demuestra todas las nuevas propiedades extendidas de la clase App:
- SEO completo (meta tags, keywords, description, robots)
- Open Graph para redes sociales (Facebook, LinkedIn, etc.)
- Twitter Cards para compartir en Twitter
- Progressive Web App (PWA) con manifest y configuración móvil
- Favicon y iconos para diferentes dispositivos
- Colores de tema y configuración visual
- URL canónica y configuración de robots

Además incluye todos los nuevos componentes básicos:
- Checkbox, RadioButton, Select, Slider, DatePicker

Uso:
    dars init mi_app_moderna --template advanced/modern_web_app
    dars export mi_app_moderna.py --format html --output ./mi_app_moderna
    dars preview ./mi_app_moderna
"""

from dars.core.app import App
from dars.components.basic.container import Container
from dars.components.basic.text import Text
from dars.components.basic.button import Button
from dars.components.basic.input import Input
from dars.components.basic.checkbox import Checkbox
from dars.components.basic.radiobutton import RadioButton
from dars.components.basic.select import Select, SelectOption
from dars.components.basic.slider import Slider
from dars.components.basic.datepicker import DatePicker
from dars.components.advanced.card import Card
from dars.scripts.script import InlineScript

# Crear aplicación con todas las propiedades extendidas modernas
app = App(
    # === PROPIEDADES BÁSICAS ===
    title="Mi Aplicación Web Moderna | Dars Framework",
    description="Una aplicación web moderna creada con Dars Framework que demuestra SEO avanzado, Open Graph, Twitter Cards, PWA y todos los componentes básicos disponibles.",
    author="Tu Nombre",
    keywords=["dars", "framework", "python", "web", "moderna", "seo", "pwa", "responsive"],
    language="es",
    
    # === ICONOS Y FAVICON ===
    favicon="/assets/favicon.ico",
    icon="/assets/icon-192x192.png",
    apple_touch_icon="/assets/apple-touch-icon.png",
    manifest="/assets/manifest.json",
    
    # === COLORES DE TEMA (PWA) ===
    theme_color="#1e3a8a",  # Azul profesional
    background_color="#f8fafc",  # Gris claro
    
    # === OPEN GRAPH (REDES SOCIALES) ===
    og_title="Mi Aplicación Web Moderna - Dars Framework",
    og_description="Descubre cómo crear aplicaciones web modernas con Python usando Dars Framework. SEO optimizado, PWA, y componentes interactivos.",
    og_image="https://mi-dominio.com/assets/og-image-1200x630.jpg",
    og_url="https://mi-dominio.com",
    og_type="website",
    og_site_name="Mi Aplicación Moderna",
    
    # === TWITTER CARDS ===
    twitter_card="summary_large_image",
    twitter_site="@mi_usuario",
    twitter_creator="@desarrollador",
    
    # === SEO AVANZADO ===
    robots="index, follow, max-snippet:-1, max-image-preview:large",
    canonical_url="https://mi-dominio.com",
    
    # === PWA CONFIGURACIÓN ===
    pwa_enabled=True,
    pwa_name="Mi App Moderna",
    pwa_short_name="AppModerna",
    pwa_display="standalone",
    pwa_orientation="portrait-primary"
)

# === CONTENEDOR PRINCIPAL ===
main_container = Container(style={
    'max-width': '1200px',
    'margin': '0 auto',
    'padding': '20px',
    'font-family': 'system-ui, -apple-system, sans-serif'
})

# === SECCIÓN HERO ===
hero_section = Container(style={
    'text-align': 'center',
    'padding': '60px 20px',
    'background': 'linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%)',
    'border-radius': '20px',
    'margin-bottom': '40px',
    'box-shadow': '0 10px 40px rgba(0,0,0,0.1)'
})

hero_title = Text(
    text="🌟 Aplicación Web Moderna",
    style={
        'font-size': '48px',
        'font-weight': '800',
        'color': '#1e3a8a',
        'margin-bottom': '20px',
        'display': 'block'
    }
)

hero_subtitle = Text(
    text="Demostrando todas las características modernas del framework Dars",
    style={
        'font-size': '20px',
        'color': '#64748b',
        'margin-bottom': '30px',
        'display': 'block'
    }
)

cta_button = Button(
    text="🚀 Explorar Componentes",
    style={
        'background': 'linear-gradient(45deg, #1e3a8a, #3b82f6)',
        'color': 'white',
        'padding': '15px 30px',
        'font-size': '18px',
        'font-weight': 'bold',
        'border': 'none',
        'border-radius': '25px',
        'cursor': 'pointer',
        'box-shadow': '0 8px 25px rgba(30, 58, 138, 0.4)'
    }
)

# === SECCIÓN DE CARACTERÍSTICAS ===
features_section = Container(style={
    'padding': '60px 20px',
    'background': 'white',
    'border-radius': '20px',
    'margin-bottom': '40px',
    'box-shadow': '0 5px 30px rgba(0,0,0,0.08)'
})

features_title = Text(
    text="✨ Características Modernas",
    style={
        'font-size': '36px',
        'font-weight': '700',
        'color': '#1e3a8a',
        'text-align': 'center',
        'margin-bottom': '40px',
        'display': 'block'
    }
)

features_grid = Container(style={
    'display': 'grid',
    'grid-template-columns': 'repeat(auto-fit, minmax(300px, 1fr))',
    'gap': '30px'
})

# Crear tarjetas de características
features_data = [
    ('🔍', 'SEO Avanzado', 'Meta tags completos, keywords, description, robots.txt y URL canónica.'),
    ('📱', 'Progressive Web App', 'Configuración PWA completa con manifest, iconos y colores de tema.'),
    ('🌐', 'Open Graph & Twitter', 'Integración completa con redes sociales para compartir perfectamente.'),
    ('🎨', 'Componentes Modernos', 'Checkbox, RadioButton, Select, Slider, DatePicker con diseño moderno.')
]

for icon, title, description in features_data:
    feature_card = Card(
        title=f"{icon} {title}",
        style={
            'border': 'none',
            'border-radius': '15px',
            'box-shadow': '0 8px 30px rgba(0,0,0,0.12)',
            'border-left': '5px solid #3b82f6'
        }
    )
    
    feature_description = Text(
        text=description,
        style={
            'color': '#64748b',
            'line-height': '1.6'
        }
    )
    
    feature_card.add_child(feature_description)
    features_grid.add_child(feature_card)

# === SECCIÓN DE FORMULARIO ===
form_section = Container(style={
    'padding': '60px 20px',
    'background': 'linear-gradient(135deg, #f1f5f9 0%, #e2e8f0 100%)',
    'border-radius': '20px',
    'margin-bottom': '40px'
})

form_title = Text(
    text="📝 Formulario Interactivo",
    style={
        'font-size': '36px',
        'font-weight': '700',
        'color': '#1e3a8a',
        'text-align': 'center',
        'margin-bottom': '40px',
        'display': 'block'
    }
)

form_container = Container(style={
    'max-width': '600px',
    'margin': '0 auto',
    'background': 'white',
    'padding': '40px',
    'border-radius': '15px',
    'box-shadow': '0 10px 40px rgba(0,0,0,0.1)'
})

# Campos del formulario
name_input = Input(
    placeholder="Tu nombre completo",
    style={
        'width': '100%',
        'padding': '12px',
        'margin-bottom': '20px',
        'border': '2px solid #e2e8f0',
        'border-radius': '8px'
    }
)

email_input = Input(
    placeholder="tu@email.com",
    input_type="email",
    style={
        'width': '100%',
        'padding': '12px',
        'margin-bottom': '20px',
        'border': '2px solid #e2e8f0',
        'border-radius': '8px'
    }
)

terms_checkbox = Checkbox(
    label="Acepto los términos y condiciones",
    style={'margin': '20px 0'}
)

# RadioButtons
user_type_title = Text(
    text="Tipo de usuario:",
    style={'font-weight': 'bold', 'margin': '20px 0 10px 0', 'display': 'block'}
)

developer_radio = RadioButton(
    label="Desarrollador",
    name="user_type",
    value="developer",
    style={'margin': '5px 0'}
)

designer_radio = RadioButton(
    label="Diseñador",
    name="user_type", 
    value="designer",
    style={'margin': '5px 0'}
)

# Select
country_select = Select(
    placeholder="Selecciona tu país",
    style={
        'width': '100%',
        'padding': '12px',
        'margin': '20px 0',
        'border': '2px solid #e2e8f0',
        'border-radius': '8px'
    }
)

country_select.add_option(SelectOption(value="es", label="España"))
country_select.add_option(SelectOption(value="mx", label="México"))
country_select.add_option(SelectOption(value="ar", label="Argentina"))
country_select.add_option(SelectOption(value="us", label="Estados Unidos"))

# Slider
experience_title = Text(
    text="Años de experiencia:",
    style={'font-weight': 'bold', 'margin': '20px 0 10px 0', 'display': 'block'}
)

experience_slider = Slider(
    min_value=0,
    max_value=20,
    value=5,
    show_value=True,
    label="años",
    style={'margin': '10px 0 20px 0'}
)

# DatePicker
birth_date_title = Text(
    text="Fecha de nacimiento:",
    style={'font-weight': 'bold', 'margin': '20px 0 10px 0', 'display': 'block'}
)

birth_date_picker = DatePicker(
    format="DD/MM/YYYY",
    style={
        'width': '100%',
        'padding': '12px',
        'margin': '10px 0 20px 0',
        'border': '2px solid #e2e8f0',
        'border-radius': '8px'
    }
)

submit_button = Button(
    text="🚀 Enviar Formulario",
    style={
        'background': 'linear-gradient(45deg, #10b981, #059669)',
        'color': 'white',
        'padding': '15px 30px',
        'font-size': '16px',
        'font-weight': 'bold',
        'border': 'none',
        'border-radius': '8px',
        'cursor': 'pointer',
        'width': '100%',
        'margin-top': '20px'
    }
)

# Script interactivo
interactive_script = InlineScript("""
document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 Aplicación Web Moderna cargada');
    
    // Mostrar información de meta tags
    const metaInfo = {
        title: document.title,
        description: document.querySelector('meta[name="description"]')?.content,
        themeColor: document.querySelector('meta[name="theme-color"]')?.content,
        manifest: document.querySelector('link[rel="manifest"]')?.href
    };
    console.log('🔍 Meta Tags:', metaInfo);
    
    // Manejar formulario
    const submitButton = document.querySelector('button[style*="10b981"]');
    if (submitButton) {
        submitButton.addEventListener('click', function(e) {
            e.preventDefault();
            
            const formData = {
                name: document.querySelector('input[placeholder*="nombre"]')?.value,
                email: document.querySelector('input[type="email"]')?.value,
                terms: document.querySelector('input[type="checkbox"]')?.checked,
                userType: document.querySelector('input[type="radio"]:checked')?.value,
                country: document.querySelector('select')?.value,
                experience: document.querySelector('input[type="range"]')?.value,
                birthDate: document.querySelector('input[type="date"]')?.value
            };
            
            if (!formData.name || !formData.email || !formData.terms) {
                alert('⚠️ Por favor completa todos los campos obligatorios');
                return;
            }
            
            alert(`✅ ¡Formulario enviado exitosamente!
            
Datos recibidos:
• Nombre: ${formData.name}
• Email: ${formData.email}
• Tipo: ${formData.userType || 'No especificado'}
• País: ${formData.country || 'No especificado'}
• Experiencia: ${formData.experience || 0} años

¡Gracias por probar la aplicación!`);
        });
    }
    
    // PWA Installation
    window.addEventListener('beforeinstallprompt', (e) => {
        e.preventDefault();
        const installBtn = document.createElement('button');
        installBtn.textContent = '📲 Instalar App';
        installBtn.style.cssText = `
            position: fixed; bottom: 20px; right: 20px;
            background: linear-gradient(45deg, #8b5cf6, #a855f7);
            color: white; border: none; padding: 12px 20px;
            border-radius: 25px; cursor: pointer; font-weight: bold;
            box-shadow: 0 4px 20px rgba(139, 92, 246, 0.4); z-index: 1000;
        `;
        installBtn.addEventListener('click', () => e.prompt());
        document.body.appendChild(installBtn);
    });
});
""")

# === ENSAMBLAR APLICACIÓN ===
hero_section.add_child(hero_title)
hero_section.add_child(hero_subtitle)
hero_section.add_child(cta_button)

features_section.add_child(features_title)
features_section.add_child(features_grid)

form_container.add_child(name_input)
form_container.add_child(email_input)
form_container.add_child(terms_checkbox)
form_container.add_child(user_type_title)
form_container.add_child(developer_radio)
form_container.add_child(designer_radio)
form_container.add_child(country_select)
form_container.add_child(experience_title)
form_container.add_child(experience_slider)
form_container.add_child(birth_date_title)
form_container.add_child(birth_date_picker)
form_container.add_child(submit_button)

form_section.add_child(form_title)
form_section.add_child(form_container)

main_container.add_child(hero_section)
main_container.add_child(features_section)
main_container.add_child(form_section)

# Configurar aplicación
app.set_root(main_container)
app.add_script(interactive_script)

# Usar métodos extendidos
app.add_keywords(["responsive", "interactivo", "moderno"])
app.set_theme_colors("#1e3a8a", "#f8fafc")
app.enable_pwa("Mi App Moderna", "AppModerna")

# Estilos globales
app.add_global_style('body', {
    'margin': '0',
    'padding': '20px',
    'background': 'linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%)',
    'font-family': 'system-ui, -apple-system, sans-serif'
})

app.add_global_style('button:hover', {
    'transform': 'translateY(-2px)',
    'transition': 'all 0.3s ease'
})

if __name__ == "__main__":
    print("🌟 Template: Aplicación Web Moderna")
    print("📱 Incluye: SEO, Open Graph, Twitter Cards, PWA, Favicon")
    print("🎯 Componentes: Checkbox, RadioButton, Select, Slider, DatePicker")
    print("🚀 Para usar: dars init mi_app --template advanced/modern_web_app")
