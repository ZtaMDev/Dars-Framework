#!/usr/bin/env python3
"""
Dars - Aplicación de Demostración Completa
Una aplicación que demuestra todas las características principales de Dars
"""

import sys
import os

from dars.core.app import App
from dars.components.basic.text import Text
from dars.components.basic.button import Button
from dars.components.basic.input import Input
from dars.components.basic.container import Container
from dars.scripts.script import InlineScript, FileScript

# Crear la aplicación con configuración avanzada
app = App(
    title="Dars - Demostración Completa",
    theme="light",
    responsive=True
)

# Estilos globales
app.add_global_style("body", {
    'margin': '0',
    'padding': '0',
    'font-family': '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
    'background-color': '#f8f9fa'
})

app.add_global_style(".fade-in", {
    'opacity': '0',
    'transition': 'opacity 0.5s ease-in-out'
})

# Contenedor principal
main_container = Container(
    id="main-app",
    style={
        'min-height': '100vh',
        'display': 'flex',
        'flex-direction': 'column'
    }
)

# Header/Navegación
header = Container(
    id="header",
    style={
        'background': 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        'color': 'white',
        'padding': '20px 0',
        'box-shadow': '0 2px 10px rgba(0,0,0,0.1)'
    }
)

nav_container = Container(
    style={
        'max-width': '1200px',
        'margin': '0 auto',
        'padding': '0 20px',
        'display': 'flex',
        'justify-content': 'space-between',
        'align-items': 'center'
    }
)

logo = Text(
    text="🚀 Dars Demo",
    style={
        'font-size': '28px',
        'font-weight': 'bold'
    }
)

nav_menu = Container(
    style={
        'display': 'flex',
        'gap': '30px'
    }
)

nav_items = ["Inicio", "Componentes", "Formularios", "Dashboard", "Acerca"]
for item in nav_items:
    nav_button = Button(
        id=f"nav-{item.lower()}",
        text=item,
        style={
            'background': 'transparent',
            'color': 'white',
            'border': '2px solid transparent',
            'padding': '8px 16px',
            'border-radius': '20px',
            'cursor': 'pointer',
            'transition': 'all 0.3s ease'
        }
    )
    nav_menu.add_child(nav_button)

# Área de contenido principal
content_area = Container(
    id="content-area",
    style={
        'flex': '1',
        'max-width': '1200px',
        'margin': '0 auto',
        'padding': '40px 20px'
    }
)

# Sección Hero
hero_section = Container(
    id="hero",
    class_name="fade-in",
    style={
        'text-align': 'center',
        'padding': '60px 0',
        'background': 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
        'border-radius': '20px',
        'margin-bottom': '40px',
        'color': 'white'
    }
)

hero_title = Text(
    text="Bienvenido a Dars",
    style={
        'font-size': '48px',
        'font-weight': 'bold',
        'margin-bottom': '20px'
    }
)

hero_subtitle = Text(
    text="Framework de UI multiplataforma en Python",
    style={
        'font-size': '24px',
        'margin-bottom': '30px',
        'opacity': '0.9'
    }
)

hero_description = Text(
    text="Crea interfaces de usuario modernas con Python y expórtalas a HTML, React, React Native, PySide6, C# y Kotlin",
    style={
        'font-size': '18px',
        'margin-bottom': '40px',
        'max-width': '600px',
        'margin-left': 'auto',
        'margin-right': 'auto',
        'line-height': '1.6'
    }
)

hero_cta = Button(
    id="hero-cta",
    text="🚀 Comenzar Ahora",
    style={
        'background-color': 'white',
        'color': '#f5576c',
        'padding': '15px 30px',
        'border': 'none',
        'border-radius': '30px',
        'font-size': '18px',
        'font-weight': 'bold',
        'cursor': 'pointer',
        'box-shadow': '0 4px 15px rgba(0,0,0,0.2)'
    }
)

# Sección de características
features_section = Container(
    id="features",
    class_name="fade-in",
    style={
        'margin-bottom': '40px'
    }
)

features_title = Text(
    text="Características Principales",
    style={
        'font-size': '36px',
        'font-weight': 'bold',
        'text-align': 'center',
        'margin-bottom': '40px',
        'color': '#2c3e50'
    }
)

features_grid = Container(
    style={
        'display': 'grid',
        'grid-template-columns': 'repeat(auto-fit, minmax(300px, 1fr))',
        'gap': '30px'
    }
)

# Función para crear tarjetas de características
def crear_feature_card(icono, titulo, descripcion):
    card = Container(
        style={
            'background': 'white',
            'padding': '30px',
            'border-radius': '15px',
            'box-shadow': '0 5px 20px rgba(0,0,0,0.1)',
            'text-align': 'center',
            'transition': 'transform 0.3s ease'
        }
    )
    
    card_icon = Text(
        text=icono,
        style={
            'font-size': '48px',
            'margin-bottom': '20px'
        }
    )
    
    card_title = Text(
        text=titulo,
        style={
            'font-size': '24px',
            'font-weight': 'bold',
            'margin-bottom': '15px',
            'color': '#2c3e50'
        }
    )
    
    card_description = Text(
        text=descripcion,
        style={
            'font-size': '16px',
            'line-height': '1.6',
            'color': '#6c757d'
        }
    )
    
    card.add_child(card_icon)
    card.add_child(card_title)
    card.add_child(card_description)
    
    return card

# Crear tarjetas de características
features_data = [
    ("🐍", "Python Puro", "Escribe interfaces de usuario usando únicamente Python, sin necesidad de aprender otros lenguajes."),
    ("🌐", "Multiplataforma", "Exporta a HTML, React, React Native, PySide6, C# y Kotlin desde un solo código fuente."),
    ("⚡", "Fácil de Usar", "Sintaxis simple e intuitiva que permite crear aplicaciones complejas con pocas líneas de código."),
    ("🎨", "Personalizable", "Sistema de estilos flexible que soporta CSS moderno y temas personalizados."),
    ("🔧", "Extensible", "Arquitectura modular que permite agregar nuevos componentes y exportadores fácilmente."),
    ("📱", "Responsive", "Interfaces que se adaptan automáticamente a diferentes tamaños de pantalla y dispositivos.")
]

for icono, titulo, descripcion in features_data:
    features_grid.add_child(crear_feature_card(icono, titulo, descripcion))

# Sección de demostración interactiva
demo_section = Container(
    id="demo",
    class_name="fade-in",
    style={
        'background': 'white',
        'padding': '40px',
        'border-radius': '15px',
        'box-shadow': '0 5px 20px rgba(0,0,0,0.1)',
        'margin-bottom': '40px'
    }
)

demo_title = Text(
    text="Demostración Interactiva",
    style={
        'font-size': '32px',
        'font-weight': 'bold',
        'text-align': 'center',
        'margin-bottom': '30px',
        'color': '#2c3e50'
    }
)

# Formulario de demostración
demo_form = Container(
    style={
        'max-width': '500px',
        'margin': '0 auto'
    }
)

form_title = Text(
    text="Prueba los Componentes",
    style={
        'font-size': '20px',
        'margin-bottom': '20px',
        'color': '#495057'
    }
)

# Campos del formulario
name_input = Input(
    id="demo-name",
    placeholder="Tu nombre",
    style={
        'width': '100%',
        'padding': '12px',
        'border': '2px solid #e9ecef',
        'border-radius': '8px',
        'font-size': '16px',
        'margin-bottom': '15px'
    }
)

email_input = Input(
    id="demo-email",
    placeholder="tu@email.com",
    input_type="email",
    style={
        'width': '100%',
        'padding': '12px',
        'border': '2px solid #e9ecef',
        'border-radius': '8px',
        'font-size': '16px',
        'margin-bottom': '15px'
    }
)

message_input = Input(
    id="demo-message",
    placeholder="Tu mensaje...",
    style={
        'width': '100%',
        'padding': '12px',
        'border': '2px solid #e9ecef',
        'border-radius': '8px',
        'font-size': '16px',
        'margin-bottom': '20px',
        'min-height': '100px'
    }
)

demo_button = Button(
    id="demo-submit",
    text="Enviar Demostración",
    style={
        'width': '100%',
        'background': 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        'color': 'white',
        'padding': '15px',
        'border': 'none',
        'border-radius': '8px',
        'font-size': '16px',
        'font-weight': 'bold',
        'cursor': 'pointer'
    }
)

# Resultado de la demostración
demo_result = Container(
    id="demo-result",
    style={
        'margin-top': '20px',
        'padding': '20px',
        'background-color': '#f8f9fa',
        'border-radius': '8px',
        'display': 'none'
    }
)

result_text = Text(
    id="result-text",
    text="",
    style={
        'font-size': '16px',
        'color': '#495057'
    }
)

# Footer
footer = Container(
    style={
        'background-color': '#2c3e50',
        'color': 'white',
        'text-align': 'center',
        'padding': '40px 20px',
        'margin-top': 'auto'
    }
)

footer_text = Text(
    text="© 2024 PyWebUI Framework - Creado con ❤️ en Python",
    style={
        'font-size': '16px'
    }
)

# Script principal de la aplicación
main_script = InlineScript(r"""
// Estado global de la aplicación
const AppState = {
    currentSection: 'inicio',
    animationDelay: 100,
    isLoaded: false
};

// Utilidades
const Utils = {
    // Animación de fade in
    fadeIn: function(element, delay = 0) {
        setTimeout(() => {
            element.style.opacity = '1';
        }, delay);
    },
    
    // Scroll suave
    smoothScroll: function(target) {
        document.querySelector(target).scrollIntoView({
            behavior: 'smooth'
        });
    },
    
    // Validar email
    isValidEmail: function(email) {
        const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return regex.test(email);
    }
};

// Gestión de navegación
const Navigation = {
    init: function() {
        const navButtons = document.querySelectorAll('[id^="nav-"]');
        navButtons.forEach(button => {
            button.addEventListener('click', this.handleNavClick.bind(this));
            
            // Efectos hover
            button.addEventListener('mouseenter', function() {
                this.style.borderColor = 'white';
                this.style.backgroundColor = 'rgba(255,255,255,0.1)';
            });
            
            button.addEventListener('mouseleave', function() {
                this.style.borderColor = 'transparent';
                this.style.backgroundColor = 'transparent';
            });
        });
    },
    
    handleNavClick: function(event) {
        const section = event.target.textContent.toLowerCase();
        this.navigateToSection(section);
    },
    
    navigateToSection: function(section) {
        AppState.currentSection = section;
        
        // Aquí podrías implementar navegación real entre secciones
        console.log(`Navegando a: ${section}`);
        
        // Ejemplo de scroll a sección
        if (section === 'componentes') {
            Utils.smoothScroll('#demo');
        }
    }
};

// Gestión de animaciones
const Animations = {
    init: function() {
        this.setupIntersectionObserver();
        this.animateHero();
        this.setupCardHovers();
    },
    
    setupIntersectionObserver: function() {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    Utils.fadeIn(entry.target, 200);
                }
            });
        }, { threshold: 0.1 });
        
        document.querySelectorAll('.fade-in').forEach(el => {
            observer.observe(el);
        });
    },
    
    animateHero: function() {
        const hero = document.getElementById('hero');
        if (hero) {
            Utils.fadeIn(hero, 300);
        }
    },
    
    setupCardHovers: function() {
        const cards = document.querySelectorAll('#features > div > div');
        cards.forEach(card => {
            card.addEventListener('mouseenter', function() {
                this.style.transform = 'translateY(-10px)';
                this.style.boxShadow = '0 10px 30px rgba(0,0,0,0.15)';
            });
            
            card.addEventListener('mouseleave', function() {
                this.style.transform = 'translateY(0)';
                this.style.boxShadow = '0 5px 20px rgba(0,0,0,0.1)';
            });
        });
    }
};

// Gestión del formulario de demostración
const DemoForm = {
    init: function() {
        const submitButton = document.getElementById('demo-submit');
        if (submitButton) {
            submitButton.addEventListener('click', this.handleSubmit.bind(this));
        }
        
        // Validación en tiempo real
        const inputs = ['demo-name', 'demo-email', 'demo-message'];
        inputs.forEach(id => {
            const input = document.getElementById(id);
            if (input) {
                input.addEventListener('input', this.validateField.bind(this));
                input.addEventListener('blur', this.validateField.bind(this));
            }
        });
    },
    
    validateField: function(event) {
        const field = event.target;
        const value = field.value.trim();
        
        // Limpiar estilos previos
        field.style.borderColor = '#e9ecef';
        
        if (field.id === 'demo-email' && value) {
            if (Utils.isValidEmail(value)) {
                field.style.borderColor = '#28a745';
            } else {
                field.style.borderColor = '#dc3545';
            }
        } else if (value) {
            field.style.borderColor = '#28a745';
        }
    },
    
    handleSubmit: function(event) {
        event.preventDefault();
        
        const name = document.getElementById('demo-name').value.trim();
        const email = document.getElementById('demo-email').value.trim();
        const message = document.getElementById('demo-message').value.trim();
        
        // Validación
        if (!name || !email || !message) {
            this.showResult('Por favor, completa todos los campos.', 'error');
            return;
        }
        
        if (!Utils.isValidEmail(email)) {
            this.showResult('Por favor, ingresa un email válido.', 'error');
            return;
        }
        
        // Simular envío
        this.simulateSubmission(name, email, message);
    },
    
    simulateSubmission: function(name, email, message) {
        const button = document.getElementById('demo-submit');
        const originalText = button.textContent;
        
        button.textContent = 'Enviando...';
        button.disabled = true;
        button.style.opacity = '0.7';
        
        setTimeout(() => {
            this.showResult(`¡Gracias ${name}! Tu mensaje ha sido enviado correctamente. Te contactaremos en ${email}.`, 'success');
            
            // Limpiar formulario
            document.getElementById('demo-name').value = '';
            document.getElementById('demo-email').value = '';
            document.getElementById('demo-message').value = '';
            
            // Restaurar botón
            button.textContent = originalText;
            button.disabled = false;
            button.style.opacity = '1';
        }, 2000);
    },
    
    showResult: function(message, type) {
        const resultContainer = document.getElementById('demo-result');
        const resultText = document.getElementById('result-text');
        
        if (resultContainer && resultText) {
            resultText.textContent = message;
            resultContainer.style.display = 'block';
            resultContainer.style.backgroundColor = type === 'success' ? '#d4edda' : '#f8d7da';
            resultContainer.style.color = type === 'success' ? '#155724' : '#721c24';
            resultContainer.style.borderLeft = `4px solid ${type === 'success' ? '#28a745' : '#dc3545'}`;
            
            // Auto-ocultar después de 5 segundos
            setTimeout(() => {
                resultContainer.style.display = 'none';
            }, 5000);
        }
    }
};

// Efectos especiales
const SpecialEffects = {
    init: function() {
        this.setupHeroCTA();
        this.setupParallax();
    },
    
    setupHeroCTA: function() {
        const ctaButton = document.getElementById('hero-cta');
        if (ctaButton) {
            ctaButton.addEventListener('click', function() {
                Utils.smoothScroll('#demo');
            });
            
            ctaButton.addEventListener('mouseenter', function() {
                this.style.transform = 'translateY(-2px)';
                this.style.boxShadow = '0 6px 20px rgba(0,0,0,0.3)';
            });
            
            ctaButton.addEventListener('mouseleave', function() {
                this.style.transform = 'translateY(0)';
                this.style.boxShadow = '0 4px 15px rgba(0,0,0,0.2)';
            });
        }
    },
    
    setupParallax: function() {
        window.addEventListener('scroll', function() {
            const scrolled = window.pageYOffset;
            const hero = document.getElementById('hero');
            
            if (hero) {
                const speed = scrolled * 0.5;
                hero.style.transform = `translateY(${speed}px)`;
            }
        });
    }
};

// Inicialización principal
document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 Dars Demo App iniciada');
    
    // Inicializar módulos
    Navigation.init();
    Animations.init();
    DemoForm.init();
    SpecialEffects.init();
    
    // Marcar como cargada
    AppState.isLoaded = true;
    
    // Mensaje de bienvenida
    setTimeout(() => {
        console.log('✨ Todas las funcionalidades cargadas correctamente');
    }, 1000);
});

// Manejo de errores globales
window.addEventListener('error', function(e) {
    console.error('Error en la aplicación:', e.error);
});
""")

# Ensamblar la aplicación
nav_container.add_child(logo)
nav_container.add_child(nav_menu)
header.add_child(nav_container)

hero_section.add_child(hero_title)
hero_section.add_child(hero_subtitle)
hero_section.add_child(hero_description)
hero_section.add_child(hero_cta)

features_section.add_child(features_title)
features_section.add_child(features_grid)

demo_form.add_child(form_title)
demo_form.add_child(name_input)
demo_form.add_child(email_input)
demo_form.add_child(message_input)
demo_form.add_child(demo_button)

demo_result.add_child(result_text)
demo_form.add_child(demo_result)

demo_section.add_child(demo_title)
demo_section.add_child(demo_form)

content_area.add_child(hero_section)
content_area.add_child(features_section)
content_area.add_child(demo_section)

footer.add_child(footer_text)

main_container.add_child(header)
main_container.add_child(content_area)
main_container.add_child(footer)

app.set_root(main_container)
app.add_script(main_script)

# Para exportar esta aplicación, ejecuta:
# dars export examples/demo/complete_app.py --format html --output ./complete_app_output

if __name__ == "__main__":
    app.rTimeCompile()  # Preview/compilación rápida

