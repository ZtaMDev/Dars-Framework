#!/usr/bin/env python3
"""
Dars - Ejemplo Básico: Formulario Simple
Demuestra el uso de inputs, validación básica y manejo de eventos
"""

import sys
import os

from dars.core.app import App
from dars.components.basic.text import Text
from dars.components.basic.button import Button
from dars.components.basic.input import Input
from dars.components.basic.container import Container
from dars.scripts.script import InlineScript

# Crear la aplicación
app = App(title="Formulario Simple - Dars")

# Contenedor principal
main_container = Container(
    style={
        'display': 'flex',
        'justify-content': 'center',
        'align-items': 'center',
        'min-height': '100vh',
        'background-color': '#ecf0f1',
        'font-family': 'Arial, sans-serif'
    }
)

# Tarjeta del formulario
form_card = Container(
    style={
        'background-color': 'white',
        'padding': '40px',
        'border-radius': '12px',
        'box-shadow': '0 4px 20px rgba(0,0,0,0.1)',
        'max-width': '400px',
        'width': '100%'
    }
)

# Título del formulario
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
label_nombre = Text(
    text="Nombre:",
    style={
        'font-size': '16px',
        'color': '#34495e',
        'margin-bottom': '8px',
        'font-weight': '500'
    }
)

input_nombre = Input(
    id="campo-nombre",
    placeholder="Ingresa tu nombre completo",
    required=True,
    style={
        'width': '100%',
        'padding': '12px',
        'border': '2px solid #bdc3c7',
        'border-radius': '6px',
        'font-size': '16px',
        'margin-bottom': '20px'
    }
)

# Campo email
label_email = Text(
    text="Email:",
    style={
        'font-size': '16px',
        'color': '#34495e',
        'margin-bottom': '8px',
        'font-weight': '500'
    }
)

input_email = Input(
    id="campo-email",
    placeholder="tu@email.com",
    input_type="email",
    required=True,
    style={
        'width': '100%',
        'padding': '12px',
        'border': '2px solid #bdc3c7',
        'border-radius': '6px',
        'font-size': '16px',
        'margin-bottom': '20px'
    }
)

# Campo mensaje
label_mensaje = Text(
    text="Mensaje:",
    style={
        'font-size': '16px',
        'color': '#34495e',
        'margin-bottom': '8px',
        'font-weight': '500'
    }
)

input_mensaje = Input(
    id="campo-mensaje",
    placeholder="Escribe tu mensaje aquí...",
    style={
        'width': '100%',
        'padding': '12px',
        'border': '2px solid #bdc3c7',
        'border-radius': '6px',
        'font-size': '16px',
        'margin-bottom': '30px',
        'min-height': '100px'
    }
)

# Botones
button_container = Container(
    style={
        'display': 'flex',
        'gap': '15px',
        'justify-content': 'center'
    }
)

boton_enviar = Button(
    id="boton-enviar",
    text="Enviar",
    style={
        'background-color': '#27ae60',
        'color': 'white',
        'padding': '12px 24px',
        'border': 'none',
        'border-radius': '6px',
        'font-size': '16px',
        'cursor': 'pointer',
        'font-weight': '500'
    }
)

boton_limpiar = Button(
    id="boton-limpiar",
    text="Limpiar",
    style={
        'background-color': '#95a5a6',
        'color': 'white',
        'padding': '12px 24px',
        'border': 'none',
        'border-radius': '6px',
        'font-size': '16px',
        'cursor': 'pointer',
        'font-weight': '500'
    }
)

# Script para funcionalidad
script = InlineScript("""
// Variables globales
let formularioValido = false;

// Funciones de validación
function validarNombre(nombre) {
    return nombre.trim().length >= 2;
}

function validarEmail(email) {
    const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return regex.test(email);
}

function validarMensaje(mensaje) {
    return mensaje.trim().length >= 10;
}

// Mostrar/ocultar mensajes de error
function mostrarError(campo, mensaje) {
    limpiarError(campo);
    
    const error = document.createElement('div');
    error.className = 'error-mensaje';
    error.textContent = mensaje;
    error.style.color = '#e74c3c';
    error.style.fontSize = '14px';
    error.style.marginTop = '5px';
    
    campo.parentNode.insertBefore(error, campo.nextSibling);
    campo.style.borderColor = '#e74c3c';
}

function limpiarError(campo) {
    const error = campo.parentNode.querySelector('.error-mensaje');
    if (error) {
        error.remove();
    }
    campo.style.borderColor = '#bdc3c7';
}

function mostrarExito(campo) {
    limpiarError(campo);
    campo.style.borderColor = '#27ae60';
}

// Validar formulario completo
function validarFormulario() {
    const nombre = document.getElementById('campo-nombre').value;
    const email = document.getElementById('campo-email').value;
    const mensaje = document.getElementById('campo-mensaje').value;
    
    let esValido = true;
    
    // Validar nombre
    if (!validarNombre(nombre)) {
        mostrarError(document.getElementById('campo-nombre'), 'El nombre debe tener al menos 2 caracteres');
        esValido = false;
    } else {
        mostrarExito(document.getElementById('campo-nombre'));
    }
    
    // Validar email
    if (!validarEmail(email)) {
        mostrarError(document.getElementById('campo-email'), 'Ingresa un email válido');
        esValido = false;
    } else {
        mostrarExito(document.getElementById('campo-email'));
    }
    
    // Validar mensaje
    if (!validarMensaje(mensaje)) {
        mostrarError(document.getElementById('campo-mensaje'), 'El mensaje debe tener al menos 10 caracteres');
        esValido = false;
    } else {
        mostrarExito(document.getElementById('campo-mensaje'));
    }
    
    return esValido;
}

// Enviar formulario
function enviarFormulario() {
    if (validarFormulario()) {
        const botonEnviar = document.getElementById('boton-enviar');
        const textoOriginal = botonEnviar.textContent;
        
        // Simular envío
        botonEnviar.textContent = 'Enviando...';
        botonEnviar.disabled = true;
        botonEnviar.style.backgroundColor = '#95a5a6';
        
        setTimeout(() => {
            alert('¡Formulario enviado correctamente!\\n\\nGracias por contactarnos.');
            limpiarFormulario();
            
            botonEnviar.textContent = textoOriginal;
            botonEnviar.disabled = false;
            botonEnviar.style.backgroundColor = '#27ae60';
        }, 2000);
    }
}

// Limpiar formulario
function limpiarFormulario() {
    document.getElementById('campo-nombre').value = '';
    document.getElementById('campo-email').value = '';
    document.getElementById('campo-mensaje').value = '';
    
    // Limpiar errores
    const campos = ['campo-nombre', 'campo-email', 'campo-mensaje'];
    campos.forEach(id => {
        const campo = document.getElementById(id);
        limpiarError(campo);
    });
}

// Configurar eventos
document.addEventListener('DOMContentLoaded', function() {
    // Eventos de botones
    document.getElementById('boton-enviar').addEventListener('click', enviarFormulario);
    document.getElementById('boton-limpiar').addEventListener('click', limpiarFormulario);
    
    // Validación en tiempo real
    document.getElementById('campo-nombre').addEventListener('blur', function() {
        if (this.value.trim()) {
            if (validarNombre(this.value)) {
                mostrarExito(this);
            } else {
                mostrarError(this, 'El nombre debe tener al menos 2 caracteres');
            }
        }
    });
    
    document.getElementById('campo-email').addEventListener('blur', function() {
        if (this.value.trim()) {
            if (validarEmail(this.value)) {
                mostrarExito(this);
            } else {
                mostrarError(this, 'Ingresa un email válido');
            }
        }
    });
    
    document.getElementById('campo-mensaje').addEventListener('blur', function() {
        if (this.value.trim()) {
            if (validarMensaje(this.value)) {
                mostrarExito(this);
            } else {
                mostrarError(this, 'El mensaje debe tener al menos 10 caracteres');
            }
        }
    });
    
    // Limpiar errores al escribir
    const campos = ['campo-nombre', 'campo-email', 'campo-mensaje'];
    campos.forEach(id => {
        document.getElementById(id).addEventListener('input', function() {
            if (this.style.borderColor === 'rgb(231, 76, 60)') { // Color de error
                limpiarError(this);
            }
        });
    });
    
    // Efectos hover en botones
    const botones = [document.getElementById('boton-enviar'), document.getElementById('boton-limpiar')];
    
    document.getElementById('boton-enviar').addEventListener('mouseenter', function() {
        if (!this.disabled) this.style.backgroundColor = '#229954';
    });
    
    document.getElementById('boton-enviar').addEventListener('mouseleave', function() {
        if (!this.disabled) this.style.backgroundColor = '#27ae60';
    });
    
    document.getElementById('boton-limpiar').addEventListener('mouseenter', function() {
        this.style.backgroundColor = '#7f8c8d';
    });
    
    document.getElementById('boton-limpiar').addEventListener('mouseleave', function() {
        this.style.backgroundColor = '#95a5a6';
    });
});
""")

# Ensamblar la aplicación
button_container.add_child(boton_enviar)
button_container.add_child(boton_limpiar)

form_card.add_child(titulo)
form_card.add_child(label_nombre)
form_card.add_child(input_nombre)
form_card.add_child(label_email)
form_card.add_child(input_email)
form_card.add_child(label_mensaje)
form_card.add_child(input_mensaje)
form_card.add_child(button_container)

main_container.add_child(form_card)

app.set_root(main_container)
app.add_script(script)

# Para exportar esta aplicación, ejecuta:
# ./dars_exporter export examples/basic/simple_form.py --format html --output ./simple_form_output

if __name__ == '__main__':
    app.rTimeCompile()