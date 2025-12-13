"""
Dars - Ejemplo Básico: Formulario Simple
Demuestra el uso de inputs, validación básica y manejo de eventos con sintaxis moderna
"""

from dars.all import *

# Crear la aplicación
app = App(title="Formulario Simple - Dars")


# Título
titulo = Text(
    text="Formulario de Contacto",
    style={
        'font-size': '28px',
        'color': '#2c3e50',
        'margin-bottom': '30px',
        'text-align': 'center',
        'font-weight': 'bold'
    }
)

# Campo nombre
label_nombre = Text("Nombre:", style={'font-size': '16px', 'color': '#34495e', 'margin-bottom': '8px', 'font-weight': '500'})
input_nombre = Input(
    id="campo-nombre",
    placeholder="Ingresa tu nombre completo",
    required=True,
    on_blur=dScript("if(this.value.trim()) { window.validarNombre(this.value) ? window.mostrarExito(this) : window.mostrarError(this, 'El nombre debe tener al menos 2 caracteres'); }"),
    on_input=dScript("if(this.style.borderColor === 'rgb(231, 76, 60)') window.limpiarError(this)"),
    style={'width': '100%', 'padding': '12px', 'border': '2px solid #bdc3c7', 'border-radius': '6px', 'font-size': '16px', 'margin-bottom': '20px'}
)

# Campo email
label_email = Text("Email:", style={'font-size': '16px', 'color': '#34495e', 'margin-bottom': '8px', 'font-weight': '500'})
input_email = Input(
    id="campo-email",
    placeholder="tu@email.com",
    input_type="email",
    required=True,
    on_blur=dScript("if(this.value.trim()) { window.validarEmail(this.value) ? window.mostrarExito(this) : window.mostrarError(this, 'Ingresa un email válido'); }"),
    on_input=dScript("if(this.style.borderColor === 'rgb(231, 76, 60)') window.limpiarError(this)"),
    style={'width': '100%', 'padding': '12px', 'border': '2px solid #bdc3c7', 'border-radius': '6px', 'font-size': '16px', 'margin-bottom': '20px'}
)

# Campo mensaje
label_mensaje = Text("Mensaje:", style={'font-size': '16px', 'color': '#34495e', 'margin-bottom': '8px', 'font-weight': '500'})
input_mensaje = Input(
    id="campo-mensaje",
    placeholder="Escribe tu mensaje aquí...",
    on_blur=dScript("if(this.value.trim()) { window.validarMensaje(this.value) ? window.mostrarExito(this) : window.mostrarError(this, 'El mensaje debe tener al menos 10 caracteres'); }"),
    on_input=dScript("if(this.style.borderColor === 'rgb(231, 76, 60)') window.limpiarError(this)"),
    style={'width': '100%', 'padding': '12px', 'border': '2px solid #bdc3c7', 'border-radius': '6px', 'font-size': '16px', 'margin-bottom': '30px', 'min-height': '100px'}
)

boton_enviar = Button(
    id="boton-enviar",
    text="Enviar",
    # Modern hover effects
    on_mouse_enter=this().state(style={'background-color': '#229954'}),
    on_mouse_leave=this().state(style={'background-color': '#27ae60'}),
    on_click=dScript("""
        const nombre = document.getElementById('campo-nombre');
        const email = document.getElementById('campo-email');
        const mensaje = document.getElementById('campo-mensaje');
        
        let valido = true;
        if (!window.validarNombre(nombre.value)) { window.mostrarError(nombre, 'Nombre inválido'); valido = false; }
        if (!window.validarEmail(email.value)) { window.mostrarError(email, 'Email inválido'); valido = false; }
        if (!window.validarMensaje(mensaje.value)) { window.mostrarError(mensaje, 'Mensaje muy corto'); valido = false; }
        
        if (valido) {
            const btn = this;
            const originalText = btn.textContent;
            btn.textContent = 'Enviando...';
            btn.style.backgroundColor = '#95a5a6';
            setTimeout(() => {
                alert('¡Enviado!');
                console.log("Nombre: " + nombre.value);
                console.log("Email: " + email.value);
                console.log("Mensaje: " + mensaje.value);
                btn.textContent = originalText;
                btn.style.backgroundColor = '#27ae60';
                nombre.value = ''; email.value = ''; mensaje.value = '';
                [nombre, email, mensaje].forEach(window.limpiarError);
            }, 1500);
        }
    """),
    style={'background-color': '#27ae60', 'color': 'white', 'padding': '12px 24px', 'border': 'none', 'border-radius': '6px', 'font-size': '16px', 'cursor': 'pointer', 'font-weight': '500', 'transition': 'background-color 0.2s'}
)

boton_limpiar = Button(
    id="boton-limpiar",
    text="Limpiar",
    on_mouse_enter=this().state(style={'background-color': '#7f8c8d'}),
    on_mouse_leave=this().state(style={'background-color': '#95a5a6'}),
    on_click=dScript("""
        document.getElementById('campo-nombre').value = '';
        document.getElementById('campo-email').value = '';
        document.getElementById('campo-mensaje').value = '';
        ['campo-nombre', 'campo-email', 'campo-mensaje'].forEach(id => window.limpiarError(document.getElementById(id)));
    """),
    style={'background-color': '#95a5a6', 'color': 'white', 'padding': '12px 24px', 'border': 'none', 'border-radius': '6px', 'font-size': '16px', 'cursor': 'pointer', 'font-weight': '500', 'transition': 'background-color 0.2s'}
)

# Botones
button_container = Container(
    boton_enviar,
    boton_limpiar,
    style={'display': 'flex', 'gap': '15px', 'justify-content': 'center'}
)

# Tarjeta del formulario
form_card = Container(
    titulo,
    label_nombre,
    input_nombre,
    label_email,
    input_email,
    label_mensaje,
    input_mensaje,
    button_container,
    style={
        'background-color': 'white',
        'padding': '40px',
        'border-radius': '12px',
        'box-shadow': '0 4px 20px rgba(0,0,0,0.1)',
        'max-width': '400px',
        'width': '100%'
    }
)



# Contenedor principal
main_container = Container(
    form_card,
    style={
        'display': 'flex',
        'justify-content': 'center',
        'align-items': 'center',
        'min-height': '100vh',
        'background-color': '#ecf0f1',
        'font-family': 'Arial, sans-serif'
    }
)

# Script de validación reutilizable
validation_logic = dScript(r"""
    window.validarNombre = function(nombre) {
        return nombre.trim().length >= 2;
    };
    
    window.validarEmail = function(email) {
        const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return regex.test(email);
    };
    
    window.validarMensaje = function(mensaje) {
        return mensaje.trim().length >= 10;
    };

    window.mostrarError = function(campo, mensaje) {
        window.limpiarError(campo);
        const error = document.createElement('div');
        error.className = 'error-mensaje';
        error.textContent = mensaje;
        error.style.color = '#e74c3c';
        error.style.fontSize = '14px';
        error.style.marginTop = '5px';
        campo.parentNode.insertBefore(error, campo.nextSibling);
        campo.style.borderColor = '#e74c3c';
    };

    window.limpiarError = function(campo) {
        const error = campo.parentNode.querySelector('.error-mensaje');
        if (error) error.remove();
        campo.style.borderColor = '#bdc3c7';
    };

    window.mostrarExito = function(campo) {
        window.limpiarError(campo);
        campo.style.borderColor = '#27ae60';
    };
""")

app.add_script(validation_logic)
app.set_root(main_container)

if __name__ == '__main__':
    app.rTimeCompile()