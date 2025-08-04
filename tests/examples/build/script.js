// Dars Runtime
document.addEventListener('DOMContentLoaded', function() {
    console.log('Dars App loaded');
    
    // Inicializar eventos de componentes
    initializeEvents();
});

function initializeEvents() {
    // Los eventos específicos se agregarán aquí
}

// Script: InlineScript

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


