#!/usr/bin/env python3
"""
Dars - Ejemplo Básico: Hello World
Un ejemplo simple que muestra los conceptos fundamentales de Dars
"""

import sys
import os

from dars.core.app import App
from dars.components.basic.text import Text
from dars.components.basic.button import Button
from dars.components.basic.container import Container
from dars.scripts.script import InlineScript

# Crear la aplicación
app = App(title="Hello World - Dars")

# Crear componentes
container = Container(
    style={
        'display': 'flex',
        'flex-direction': 'column',
        'align-items': 'center',
        'justify-content': 'center',
        'min-height': '100vh',
        'background-color': '#f0f2f5',
        'font-family': 'Arial, sans-serif'
    }
)

titulo = Text(
    text="¡Hola Mundo!",
    style={
        'font-size': '48px',
        'color': '#2c3e50',
        'margin-bottom': '20px',
        'font-weight': 'bold',
        'text-align': 'center'
    }
)

subtitulo = Text(
    text="Tu primera aplicación con Dars",
    style={
        'font-size': '20px',
        'color': '#7f8c8d',
        'margin-bottom': '40px',
        'text-align': 'center'
    }
)

boton = Button(
    text="¡Hacer clic aquí!",
    style={
        'background-color': '#3498db',
        'color': 'white',
        'padding': '15px 30px',
        'border': 'none',
        'border-radius': '8px',
        'font-size': '18px',
        'cursor': 'pointer',
        'transition': 'background-color 0.3s'
    }
)

# Script para interactividad
script = InlineScript("""
function manejarClick() {
    alert('¡Felicidades! Has creado tu primera aplicación Dars');
    console.log('Botón presionado en Hello World');
}

document.addEventListener('DOMContentLoaded', function() {
    const boton = document.querySelector('button');
    if (boton) {
        boton.addEventListener('click', manejarClick);
        
        // Efecto hover
        boton.addEventListener('mouseenter', function() {
            this.style.backgroundColor = '#2980b9';
        });
        
        boton.addEventListener('mouseleave', function() {
            this.style.backgroundColor = '#3498db';
        });
    }
});
""")

# Ensamblar la aplicación
container.add_child(titulo)
container.add_child(subtitulo)
container.add_child(boton)

app.set_root(container)
app.add_script(script)

if __name__ == '__main__':
    app.rTimeCompile()

