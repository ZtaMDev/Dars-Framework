# Dars - Script System

## Introduction

The script system of Dars allows adding interactive logic and dynamic behaviors to applications. Scripts are written in JavaScript and seamlessly integrate with UI components.

## Fundamentals

### What are Scripts?

Scripts in Dars are fragments of JavaScript code that:

- Handle user interface events
- Implement client-side business logic
- Provide advanced interactivity
- Run in the context of the exported application

### Types of Scripts

Dars supports three main types of scripts:

1. **InlineScript**: Code defined directly in Python
2. **FileScript**: Code loaded from external files
3. **dScript**: Flexible script that can be defined either inline (as a string) or as a reference to an external file. Only one mode is allowed at a time.

## Base Script Class

All scripts inherit from the base `Script` class:

```python
from abc import ABC, abstractmethod

class Script(ABC):
    def __init__(self):
        pass
        
    @abstractmethod
    def get_code(self) -> str:
        """Retorna el código del script"""
        pass
```

## dScript

### When to use dScript

dScript is a flexible class that allows you to define a script as either:
- Inline JavaScript (via the `code` argument)
- Or as a reference to an external file (via the `file_path` argument)

But **never both at the same time**. This is useful for presets, user-editable actions, and advanced integrations.

### Basic Syntax

```python
from dars.scripts.dscript import dScript

# Inline JS
script_inline = dScript(code="""
function hello() { alert('Hello from dScript!'); }
document.addEventListener('DOMContentLoaded', hello);
""")

# External file
script_file = dScript(file_path="./scripts/my_script.js")
```

### Example: Editable JS preset from Python

```python
from dars.scripts.dscript import dScript

custom_action = dScript(code="""
function customClick() {
    alert('Custom action from preset!');
}
document.addEventListener('DOMContentLoaded', function() {
    var btn = document.getElementById('my-btn');
    if (btn) btn.onclick = customClick;
});
""")

app.add_script(custom_action)
```

## InlineScript

### Basic Syntax

```python
from dars.scripts.script import InlineScript

script = InlineScript("""
function saludar() {
    alert('¡Hola desde Dars!');
}

document.addEventListener('DOMContentLoaded', function() {
    console.log('Aplicación cargada');
});
""")
```

### Practical Examples

#### Button Event Handling

```python
script_botones = InlineScript("""
// Function to handle button clicks
function manejarClickBoton(evento) {
    const boton = evento.target;
    const texto = boton.textContent;
    
    console.log(`Button pressed: ${texto}`);
    
    // Change text temporarily
    const textoOriginal = boton.textContent;
    boton.textContent = '¡Presionado!';
    boton.disabled = true;
    
    setTimeout(() => {
        boton.textContent = textoOriginal;
        boton.disabled = false;
    }, 1000);
}

// Add events to all buttons
document.addEventListener('DOMContentLoaded', function() {
    const botones = document.querySelectorAll('button');
    botones.forEach(boton => {
        boton.addEventListener('click', manejarClickBoton);
    });
});
""")
```

#### Form Validation

```python
script_validacion = InlineScript("""
// Form validation
function validarFormulario() {
    const inputs = document.querySelectorAll('input[required]');
    let esValido = true;
    
    inputs.forEach(input => {
        if (!input.value.trim()) {
            mostrarError(input, 'This field is required');
            esValido = false;
        } else {
            limpiarError(input);
        }
        
        // Specific type validation
        if (input.type === 'email' && input.value) {
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(input.value)) {
                mostrarError(input, 'Email is invalid');
                esValido = false;
            }
        }
    });
    
    return esValido;
}

function mostrarError(input, mensaje) {
    //  Remove previous error
    limpiarError(input);
    
    // Create error element
    const error = document.createElement('div');
    error.className = 'error-mensaje';
    error.textContent = mensaje;
    error.style.color = '#dc3545';
    error.style.fontSize = '12px';
    error.style.marginTop = '5px';
    
    // Add after the input
    input.parentNode.insertBefore(error, input.nextSibling);
    
    // Change input style
    input.style.borderColor = '#dc3545';
}

function limpiarError(input) {
    const error = input.parentNode.querySelector('.error-mensaje');
    if (error) {
        error.remove();
    }
    input.style.borderColor = '';
}

// Configure real-time validation
document.addEventListener('DOMContentLoaded', function() {
    const inputs = document.querySelectorAll('input');
    inputs.forEach(input => {
        input.addEventListener('blur', function() {
            if (this.hasAttribute('required') && !this.value.trim()) {
                mostrarError(this, 'This field is required');
            } else {
                limpiarError(this);
            }
        });
        
        input.addEventListener('input', function() {
            limpiarError(this);
        });
    });
});
""")
```

#### Visual Effects and Animations

```python
script_animaciones = InlineScript("""
// Fade in effect for elements
function fadeIn(elemento, duracion = 500) {
    elemento.style.opacity = '0';
    elemento.style.display = 'block';
    
    const inicio = performance.now();
    
    function animar(tiempo) {
        const progreso = (tiempo - inicio) / duracion;
        
        if (progreso < 1) {
            elemento.style.opacity = progreso;
            requestAnimationFrame(animar);
        } else {
            elemento.style.opacity = '1';
        }
    }
    
    requestAnimationFrame(animar);
}

// Typing effect for text
function efectoTyping(elemento, texto, velocidad = 50) {
    elemento.textContent = '';
    let i = 0;
    
    function escribir() {
        if (i < texto.length) {
            elemento.textContent += texto.charAt(i);
            i++;
            setTimeout(escribir, velocidad);
        }
    }
    
    escribir();
}

// Parallax simple
function iniciarParallax() {
    window.addEventListener('scroll', function() {
        const scrolled = window.pageYOffset;
        const elementos = document.querySelectorAll('.parallax');
        
        elementos.forEach(elemento => {
            const velocidad = elemento.dataset.velocidad || 0.5;
            const yPos = -(scrolled * velocidad);
            elemento.style.transform = `translateY(${yPos}px)`;
        });
    });
}

// Inicializar efectos
document.addEventListener('DOMContentLoaded', function() {
    // Fade in para todos los elementos con clase 'fade-in'
    const elementosFadeIn = document.querySelectorAll('.fade-in');
    elementosFadeIn.forEach((elemento, index) => {
        setTimeout(() => fadeIn(elemento), index * 200);
    });
    
    // Efecto typing para títulos
    const titulos = document.querySelectorAll('.typing-effect');
    titulos.forEach(titulo => {
        const texto = titulo.textContent;
        efectoTyping(titulo, texto);
    });
    
    // Inicializar parallax
    iniciarParallax();
});
""")
```

### Integration with Exporter

The exporter (`html_css_js.py`) automatically detects and exports all scripts of type `dScript`, `InlineScript`, and `FileScript`. You can safely mix and match them in your app, and all will be included in the generated JS.

---

## FileScript

### Basic Syntax

```python
from dars.scripts.script import FileScript

# Load script from file
script = FileScript("./scripts/mi_script.js")
```

### File Organization

```
mi_proyecto/
├── app.py
├── scripts/
│   ├── utils.js
│   ├── validaciones.js
│   └── animaciones.js
└────── api.js

```

#### Example: utils.js

```javascript
// scripts/utils.js

// General utilities
const Utils = {
    // Date formatting
    formatearFecha: function(fecha) {
        return new Intl.DateTimeFormat('es-ES', {
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        }).format(fecha);
    },
    
    // Debounce for event optimization
    debounce: function(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    },
    
    // Email validation
    esEmailValido: function(email) {
        const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return regex.test(email);
    },
    
    // Generate unique ID
    generarId: function() {
        return '_'+ Math.random().toString(36).substr(2, 9);
    },
    
    // Local storage
    guardarEnLocal: function(clave, valor) {
        try {
            localStorage.setItem(clave, JSON.stringify(valor));
            return true;
        } catch (e) {
            console.error('Error al guardar en localStorage:', e);
            return false;
        }
    },
    
    obtenerDeLocal: function(clave) {
        try {
            const item = localStorage.getItem(clave);
            return item ? JSON.parse(item) : null;
        } catch (e) {
            console.error('Error al leer de localStorage:', e);
            return null;
        }
    }
};

// Make available globally
window.Utils = Utils;
```

#### Example: api.js

```javascript
// scripts/api.js

// API client
class ApiClient {
    constructor(baseUrl) {
        this.baseUrl = baseUrl;
        this.headers = {
            'Content-Type': 'application/json'
        };
    }
    
    async request(endpoint, options = {}) {
        const url = `${this.baseUrl}${endpoint}`;
        const config = {
            headers: this.headers,
            ...options
        };
        
        try {
            const response = await fetch(url, config);
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            return await response.json();
        } catch (error) {
            console.error('Error en la petición:', error);
            throw error;
        }
    }
    
    async get(endpoint) {
        return this.request(endpoint, { method: 'GET' });
    }
    
    async post(endpoint, data) {
        return this.request(endpoint, {
            method: 'POST',
            body: JSON.stringify(data)
        });
    }
    
    async put(endpoint, data) {
        return this.request(endpoint, {
            method: 'PUT',
            body: JSON.stringify(data)
        });
    }
    
    async delete(endpoint) {
        return this.request(endpoint, { method: 'DELETE' });
    }
}

// Global instance
window.api = new ApiClient('https://api.ejemplo.com');
```

### Usage in the Application

#### Global and Page-specific Scripts (multipage)

In multipage applications, you can add global scripts to the App and page-specific scripts to each Page:

```python
from dars.scripts.script import InlineScript
from dars.components.basic import Page, Button, Text

home = Page(
    Text("Inicio"),
    Button("Ir a About", id="btn-about")
)
home.add_script(InlineScript("""
document.addEventListener('DOMContentLoaded', function() {
    var btn = document.getElementById('btn-about');
    if (btn) btn.onclick = () => window.location.href = 'about.html';
});
"""))

about = Page(
    Text("Sobre Nosotros"),
    Button("Volver", id="btn-home")
)
about.add_script(InlineScript("""
document.addEventListener('DOMContentLoaded', function() {
    var btn = document.getElementById('btn-home');
    if (btn) btn.onclick = () => window.location.href = 'index.html';
});
"""))

# Global script
app.add_script(InlineScript("console.log('Script global para todas las páginas');"))
```

When exporting, each page will have its own JS file combining global scripts and page-specific scripts.

```python
from dars.scripts.script import FileScript

# Load multiple scripts
app.add_script(FileScript("./scripts/utils.js"))
app.add_script(FileScript("./scripts/api.js"))
app.add_script(FileScript("./scripts/validaciones.js"))
```

## Component Integration

### Connecting Scripts to Components

```python
from dars.core.app import App
from dars.components.basic.button import Button
from dars.components.basic.input import Input
from dars.components.basic.container import Container
from dars.scripts.script import InlineScript

# Create components with specific IDs
formulario = Container(
    id="formulario-contacto",
    children=[
        Input(
            id="campo-nombre",
            placeholder="Nombre",
            required=True
        ),
        Input(
            id="campo-email",
            placeholder="Email",
            input_type="email",
            required=True
        ),
        Button(
            id="boton-enviar",
            text="Enviar"
        )
    ]
)

# Script that interacts with components
script_formulario = InlineScript("""
document.addEventListener(\'DOMContentLoaded\', function() {
    const formulario = document.getElementById(\'formulario-contacto\');
    const campoNombre = document.getElementById(\'campo-nombre\');
    const campoEmail = document.getElementById(\'campo-email\');
    const botonEnviar = document.getElementById(\'boton-enviar\');
    
    // Real-time validation
    campoNombre.addEventListener(\'input\', function() {
        validarNombre(this.value);
    });
    
    campoEmail.addEventListener(\'input\', function() {
        validarEmail(this.value);
    });
    
    // Handle form submission
    botonEnviar.addEventListener(\'click\', function(e) {
        e.preventDefault();
        enviarFormulario();
    });
    
    function validarNombre(nombre) {
        const esValido = nombre.length >= 2;
        campoNombre.style.borderColor = esValido ? \'#28a745\' : \'#dc3545\';
        return esValido;
    }
    
    function validarEmail(email) {
        const regex = /^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$/;
        const esValido = regex.test(email);
        campoEmail.style.borderColor = esValido ? \'#28a745\' : \'#dc3545\';
        return esValido;
    }
    
    function enviarFormulario() {
        const nombre = campoNombre.value;
        const email = campoEmail.value;
        
        if (validarNombre(nombre) && validarEmail(email)) {
            // Simular envío
            botonEnviar.textContent = \'Enviando...\';
            botonEnviar.disabled = true;
            
            setTimeout(() => {
                alert(\'Formulario enviado correctamente\');
                campoNombre.value = \'\';
                campoEmail.value = \'\';
                botonEnviar.textContent = \'Enviar\';
                botonEnviar.disabled = false;
            }, 2000);
        } else {
            alert(\'Por favor, corrige los errores en el formulario\');
        }
    }
});
""")

# Add to the application
app = App(title="Form with Script")
app.set_root(form)
app.add_script(form_script)


