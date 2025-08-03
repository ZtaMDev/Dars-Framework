# Dars - Sistema de Scripts

## Introducción

El sistema de scripts de Dars permite agregar lógica interactiva y comportamientos dinámicos a las aplicaciones. Los scripts se escriben en JavaScript o TypeScript y se integran seamlessly con los componentes de la interfaz de usuario.

## Conceptos Fundamentales

### ¿Qué son los Scripts?

Los scripts en Dars son fragmentos de código JavaScript o TypeScript que:

- Manejan eventos de la interfaz de usuario
- Implementan lógica de negocio del lado del cliente
- Proporcionan interactividad avanzada
- Se ejecutan en el contexto de la aplicación exportada

### Tipos de Scripts

Dars soporta dos tipos principales de scripts:

1. **InlineScript**: Código definido directamente en Python
2. **FileScript**: Código cargado desde archivos externos

## Clase Base Script

Todos los scripts heredan de la clase base `Script`:

```python
from abc import ABC, abstractmethod

class Script(ABC):
    def __init__(self, target_language: str = "javascript"):
        self.target_language = target_language  # "javascript" o "typescript"
        
    @abstractmethod
    def get_code(self) -> str:
        """Retorna el código del script en el lenguaje objetivo"""
        pass
```

## InlineScript

### Sintaxis Básica

```python
from pywebui.scripts.script import InlineScript

script = InlineScript("""
function saludar() {
    alert('¡Hola desde Dars!');
}

document.addEventListener('DOMContentLoaded', function() {
    console.log('Aplicación cargada');
});
""", target_language="javascript")
```

### Ejemplos Prácticos

#### Manejo de Eventos de Botones

```python
script_botones = InlineScript("""
// Función para manejar clicks de botones
function manejarClickBoton(evento) {
    const boton = evento.target;
    const texto = boton.textContent;
    
    console.log(`Botón presionado: ${texto}`);
    
    // Cambiar el texto temporalmente
    const textoOriginal = boton.textContent;
    boton.textContent = '¡Presionado!';
    boton.disabled = true;
    
    setTimeout(() => {
        boton.textContent = textoOriginal;
        boton.disabled = false;
    }, 1000);
}

// Agregar eventos a todos los botones
document.addEventListener('DOMContentLoaded', function() {
    const botones = document.querySelectorAll('button');
    botones.forEach(boton => {
        boton.addEventListener('click', manejarClickBoton);
    });
});
""")
```

#### Validación de Formularios

```python
script_validacion = InlineScript("""
// Validación de formularios
function validarFormulario() {
    const inputs = document.querySelectorAll('input[required]');
    let esValido = true;
    
    inputs.forEach(input => {
        if (!input.value.trim()) {
            mostrarError(input, 'Este campo es obligatorio');
            esValido = false;
        } else {
            limpiarError(input);
        }
        
        // Validación específica por tipo
        if (input.type === 'email' && input.value) {
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(input.value)) {
                mostrarError(input, 'Email inválido');
                esValido = false;
            }
        }
    });
    
    return esValido;
}

function mostrarError(input, mensaje) {
    // Remover error anterior
    limpiarError(input);
    
    // Crear elemento de error
    const error = document.createElement('div');
    error.className = 'error-mensaje';
    error.textContent = mensaje;
    error.style.color = '#dc3545';
    error.style.fontSize = '12px';
    error.style.marginTop = '5px';
    
    // Agregar después del input
    input.parentNode.insertBefore(error, input.nextSibling);
    
    // Cambiar estilo del input
    input.style.borderColor = '#dc3545';
}

function limpiarError(input) {
    const error = input.parentNode.querySelector('.error-mensaje');
    if (error) {
        error.remove();
    }
    input.style.borderColor = '';
}

// Configurar validación en tiempo real
document.addEventListener('DOMContentLoaded', function() {
    const inputs = document.querySelectorAll('input');
    inputs.forEach(input => {
        input.addEventListener('blur', function() {
            if (this.hasAttribute('required') && !this.value.trim()) {
                mostrarError(this, 'Este campo es obligatorio');
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

#### Efectos Visuales y Animaciones

```python
script_animaciones = InlineScript("""
// Efectos de fade in para elementos
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

// Efecto de typing para texto
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

## FileScript

### Sintaxis Básica

```python
from pywebui.scripts.script import FileScript

# Cargar script desde archivo
script = FileScript("./scripts/mi_script.js", target_language="javascript")
```

### Organización de Archivos

```
mi_proyecto/
├── app.py
├── scripts/
│   ├── utils.js
│   ├── validaciones.js
│   ├── animaciones.js
│   └── api.js
└── estilos/
    └── main.css
```

#### Ejemplo: utils.js

```javascript
// scripts/utils.js

// Utilidades generales
const Utils = {
    // Formatear fecha
    formatearFecha: function(fecha) {
        return new Intl.DateTimeFormat('es-ES', {
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        }).format(fecha);
    },
    
    // Debounce para optimizar eventos
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
    
    // Validar email
    esEmailValido: function(email) {
        const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return regex.test(email);
    },
    
    // Generar ID único
    generarId: function() {
        return '_' + Math.random().toString(36).substr(2, 9);
    },
    
    // Almacenamiento local
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

// Hacer disponible globalmente
window.Utils = Utils;
```

#### Ejemplo: api.js

```javascript
// scripts/api.js

// Cliente API
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

// Instancia global
window.api = new ApiClient('https://api.ejemplo.com');
```

### Uso en la Aplicación

```python
from pywebui.scripts.script import FileScript

# Cargar múltiples scripts
app.add_script(FileScript("./scripts/utils.js"))
app.add_script(FileScript("./scripts/api.js"))
app.add_script(FileScript("./scripts/validaciones.js"))
```

## Scripts en TypeScript

### Configuración

```python
script_typescript = InlineScript("""
// Definir interfaces
interface Usuario {
    id: number;
    nombre: string;
    email: string;
    activo: boolean;
}

interface ConfiguracionApp {
    tema: 'claro' | 'oscuro';
    idioma: string;
    notificaciones: boolean;
}

// Clase principal de la aplicación
class AplicacionPrincipal {
    private usuarios: Usuario[] = [];
    private config: ConfiguracionApp;
    
    constructor(config: ConfiguracionApp) {
        this.config = config;
        this.inicializar();
    }
    
    private inicializar(): void {
        this.cargarUsuarios();
        this.configurarEventos();
        this.aplicarTema();
    }
    
    private async cargarUsuarios(): Promise<void> {
        try {
            const response = await fetch('/api/usuarios');
            this.usuarios = await response.json();
            this.renderizarUsuarios();
        } catch (error) {
            console.error('Error al cargar usuarios:', error);
        }
    }
    
    private configurarEventos(): void {
        document.addEventListener('DOMContentLoaded', () => {
            this.configurarFormularios();
            this.configurarBotones();
        });
    }
    
    private configurarFormularios(): void {
        const formularios = document.querySelectorAll('form');
        formularios.forEach(form => {
            form.addEventListener('submit', this.manejarEnvioFormulario.bind(this));
        });
    }
    
    private manejarEnvioFormulario(evento: Event): void {
        evento.preventDefault();
        const form = evento.target as HTMLFormElement;
        const datos = new FormData(form);
        
        // Procesar datos del formulario
        this.procesarFormulario(datos);
    }
    
    private procesarFormulario(datos: FormData): void {
        // Lógica de procesamiento
        console.log('Procesando formulario:', datos);
    }
    
    private aplicarTema(): void {
        document.body.className = `tema-${this.config.tema}`;
    }
    
    private renderizarUsuarios(): void {
        const contenedor = document.getElementById('lista-usuarios');
        if (!contenedor) return;
        
        contenedor.innerHTML = this.usuarios
            .map(usuario => this.crearElementoUsuario(usuario))
            .join('');
    }
    
    private crearElementoUsuario(usuario: Usuario): string {
        return `
            <div class="usuario ${usuario.activo ? 'activo' : 'inactivo'}">
                <h3>${usuario.nombre}</h3>
                <p>${usuario.email}</p>
                <button onclick="app.toggleUsuario(${usuario.id})">
                    ${usuario.activo ? 'Desactivar' : 'Activar'}
                </button>
            </div>
        `;
    }
    
    public toggleUsuario(id: number): void {
        const usuario = this.usuarios.find(u => u.id === id);
        if (usuario) {
            usuario.activo = !usuario.activo;
            this.renderizarUsuarios();
        }
    }
}

// Inicializar aplicación
const configuracion: ConfiguracionApp = {
    tema: 'claro',
    idioma: 'es',
    notificaciones: true
};

const app = new AplicacionPrincipal(configuracion);

// Hacer disponible globalmente
(window as any).app = app;
""", target_language="typescript")
```

## Integración con Componentes

### Conectar Scripts con Componentes

```python
from pywebui.core.app import App
from pywebui.components.basic.button import Button
from pywebui.components.basic.input import Input
from pywebui.components.basic.container import Container
from pywebui.scripts.script import InlineScript

# Crear componentes con IDs específicos
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

# Script que interactúa con los componentes
script_formulario = InlineScript("""
document.addEventListener('DOMContentLoaded', function() {
    const formulario = document.getElementById('formulario-contacto');
    const campoNombre = document.getElementById('campo-nombre');
    const campoEmail = document.getElementById('campo-email');
    const botonEnviar = document.getElementById('boton-enviar');
    
    // Validación en tiempo real
    campoNombre.addEventListener('input', function() {
        validarNombre(this.value);
    });
    
    campoEmail.addEventListener('input', function() {
        validarEmail(this.value);
    });
    
    // Manejo del envío
    botonEnviar.addEventListener('click', function(e) {
        e.preventDefault();
        enviarFormulario();
    });
    
    function validarNombre(nombre) {
        const esValido = nombre.length >= 2;
        campoNombre.style.borderColor = esValido ? '#28a745' : '#dc3545';
        return esValido;
    }
    
    function validarEmail(email) {
        const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        const esValido = regex.test(email);
        campoEmail.style.borderColor = esValido ? '#28a745' : '#dc3545';
        return esValido;
    }
    
    function enviarFormulario() {
        const nombre = campoNombre.value;
        const email = campoEmail.value;
        
        if (validarNombre(nombre) && validarEmail(email)) {
            // Simular envío
            botonEnviar.textContent = 'Enviando...';
            botonEnviar.disabled = true;
            
            setTimeout(() => {
                alert('Formulario enviado correctamente');
                campoNombre.value = '';
                campoEmail.value = '';
                botonEnviar.textContent = 'Enviar';
                botonEnviar.disabled = false;
            }, 2000);
        } else {
            alert('Por favor, corrige los errores en el formulario');
        }
    }
});
""")

# Agregar a la aplicación
app = App(title="Formulario con Scripts")
app.set_root(formulario)
app.add_script(script_formulario)
```

## Mejores Prácticas

### Organización del Código

```python
# Separar scripts por funcionalidad
script_utils = FileScript("./scripts/utils.js")
script_validaciones = FileScript("./scripts/validaciones.js")
script_api = FileScript("./scripts/api.js")
script_main = FileScript("./scripts/main.js")

# Agregar en orden de dependencias
app.add_script(script_utils)      # Primero las utilidades
app.add_script(script_api)        # Luego el cliente API
app.add_script(script_validaciones)  # Después las validaciones
app.add_script(script_main)       # Finalmente el script principal
```

### Manejo de Errores

```python
script_error_handling = InlineScript("""
// Manejo global de errores
window.addEventListener('error', function(e) {
    console.error('Error global:', e.error);
    // Enviar error a servicio de logging
    if (window.api) {
        window.api.post('/api/errores', {
            mensaje: e.error.message,
            archivo: e.filename,
            linea: e.lineno,
            url: window.location.href,
            timestamp: new Date().toISOString()
        }).catch(err => console.error('Error al reportar error:', err));
    }
});

// Promesas no manejadas
window.addEventListener('unhandledrejection', function(e) {
    console.error('Promesa rechazada no manejada:', e.reason);
    e.preventDefault(); // Prevenir que aparezca en la consola
});

// Función helper para try-catch
function ejecutarSeguro(fn, contexto = 'Operación') {
    try {
        return fn();
    } catch (error) {
        console.error(`Error en ${contexto}:`, error);
        return null;
    }
}

// Función helper para async/await
async function ejecutarSeguroAsync(fn, contexto = 'Operación asíncrona') {
    try {
        return await fn();
    } catch (error) {
        console.error(`Error en ${contexto}:`, error);
        return null;
    }
}
""")
```

### Performance y Optimización

```python
script_performance = InlineScript("""
// Lazy loading de imágenes
function configurarLazyLoading() {
    const imagenes = document.querySelectorAll('img[data-src]');
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.removeAttribute('data-src');
                observer.unobserve(img);
            }
        });
    });
    
    imagenes.forEach(img => observer.observe(img));
}

// Throttle para eventos de scroll
function throttle(func, limit) {
    let inThrottle;
    return function() {
        const args = arguments;
        const context = this;
        if (!inThrottle) {
            func.apply(context, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    }
}

// Optimizar eventos de scroll
const scrollOptimizado = throttle(function() {
    // Lógica de scroll
}, 100);

window.addEventListener('scroll', scrollOptimizado);

// Precargar recursos críticos
function precargarRecursos() {
    const recursos = [
        '/api/datos-criticos',
        '/imagenes/hero.jpg',
        '/scripts/modulo-importante.js'
    ];
    
    recursos.forEach(recurso => {
        const link = document.createElement('link');
        link.rel = 'preload';
        link.href = recurso;
        link.as = recurso.endsWith('.js') ? 'script' : 
                  recurso.endsWith('.css') ? 'style' : 'fetch';
        document.head.appendChild(link);
    });
}

// Inicializar optimizaciones
document.addEventListener('DOMContentLoaded', function() {
    configurarLazyLoading();
    precargarRecursos();
});
""")
```

El sistema de scripts de Dars proporciona una forma poderosa y flexible de agregar interactividad a las aplicaciones, manteniendo la separación entre la lógica de presentación (componentes) y la lógica de comportamiento (scripts).

