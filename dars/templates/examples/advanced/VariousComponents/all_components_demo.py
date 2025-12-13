#!/usr/bin/env python3
"""
Plantilla: Todos los Componentes Dars - Básicos y Avanzados
Demuestra el uso completo e integrado de todos los componentes básicos y avanzados:
Text, Button, Input, Container, Image, Link, Textarea, Checkbox, RadioButton, Select, Slider, DatePicker,
Table, Tabs, Accordion, ProgressBar, Spinner, Tooltip

Uso:
dars init mi_proyecto -t advanced/all_components_demo
"""

from dars.core.app import App
from dars.components.basic.container import Container
from dars.components.basic.text import Text
from dars.components.basic.button import Button
from dars.components.basic.input import Input
from dars.components.basic.image import Image
from dars.components.basic.link import Link
from dars.components.basic.textarea import Textarea
from dars.components.basic.checkbox import Checkbox
from dars.components.basic.radiobutton import RadioButton
from dars.components.basic.select import Select, SelectOption
from dars.components.basic.slider import Slider
from dars.components.basic.datepicker import DatePicker
from dars.components.advanced.table import Table
from dars.components.advanced.tabs import Tabs
from dars.components.advanced.accordion import Accordion
from dars.components.basic.progressbar import ProgressBar
from dars.components.basic.spinner import Spinner
from dars.components.basic.tooltip import Tooltip

# App principal
app = App(title="Dars - Todos los Componentes Básicos y Avanzados")
# Estilos comunes
input_style = {
    'padding': '10px',
    'border': '1px solid #ddd',
    'border-radius': '6px',
    'width': '100%',
    'margin-bottom': '10px'
}

main = Container(
    Text("Demostración de TODOS los componentes de Dars", style={"font-size": "2rem", "font-weight": "bold", "margin-bottom": "24px", "color": "#2c3e50"}),
    
    # Básicos
    Text("Componentes Básicos", style={"font-size": "1.5rem", "margin": "24px 0 12px 0", "color": "#007bff", "border-bottom": "2px solid #007bff", "padding-bottom": "5px"}),
    
    Container(
        Text("Texto de ejemplo", style={"margin-bottom": "8px", "font-weight": "500"}),
        Button(
            "Botón primario", 
            style={'background': '#007bff', 'color': 'white', 'padding': '10px 20px', 'border': 'none', 'border-radius': '6px', 'cursor': 'pointer', 'transition': 'background 0.2s'},
            hover_style={'background': '#0056b3'}
        ),
        style={'margin-bottom': '20px'}
    ),
    
    Container(
        Input(placeholder="Campo de texto", style=input_style),
        Textarea(value="Texto multilinea de ejemplo", rows=3, style=input_style),
        style={'margin-bottom': '20px'}
    ),
    
    Container(
        Image(src="https://via.placeholder.com/120x60.png?text=Logo", alt="Logo Demo", style={"margin": "10px 0", "border-radius": "4px"}),
        Link(
            "Ir a Dars Framework", 
            href="https://github.com/ZtaMDev/Dars-Framework", 
            target="_blank",
            style={'color': '#007bff', 'text-decoration': 'none', 'font-weight': 'bold'},
            hover_style={'text-decoration': 'underline'}
        ),
        style={'display': 'flex', 'align-items': 'center', 'gap': '20px', 'margin-bottom': '20px'}
    ),
    
    Container(
        Checkbox(label="Acepto términos y condiciones", checked=True, style={'margin-bottom': '10px'}),
        RadioButton(label="Opción A", name="grupo1", checked=True, style={'margin-right': '15px'}),
        RadioButton(label="Opción B", name="grupo1"),
        style={'margin-bottom': '20px'}
    ),
    
    Container(
        Select(
            options=[SelectOption("uno", "Uno"), SelectOption("dos", "Dos")], 
            value="uno", 
            placeholder="Selecciona una opción",
            style=input_style
        ),
        Slider(min_value=0, max_value=100, value=50, label="Volumen", show_value=True, style={'margin': '20px 0'}),
        DatePicker(value="2025-08-06", style=input_style),
        style={'margin-bottom': '20px', 'background': '#f8f9fa', 'padding': '20px', 'border-radius': '8px'}
    ),
    
    # Avanzados
    Text("Componentes Avanzados", style={"font-size": "1.5rem", "margin": "32px 0 12px 0", "color": "#4a90e2", "border-bottom": "2px solid #4a90e2", "padding-bottom": "5px"}),
    
    Table(
        columns=[{"title": "Nombre", "field": "nombre"}, {"title": "Edad", "field": "edad"}],
        data=[{"nombre": "Ana", "edad": 28}, {"nombre": "Luis", "edad": 34}],
        page_size=10,
        style={'width': '100%', 'margin-bottom': '20px', 'border-collapse': 'collapse'}
    ),
    
    Tabs(
        tabs=["Tab 1", "Tab 2"],
        panels=[
            Container(Text("Contenido de la pestaña 1"), style={'padding': '20px', 'background': '#f1f1f1'}),
            Container(Text("Contenido de la pestaña 2"), style={'padding': '20px', 'background': '#e1e1e1'})
        ],
        selected=0,
        style={'margin-bottom': '20px'}
    ),
    
    Accordion(
        sections=[
            ("Sección 1", Text("Contenido de la sección 1")),
            ("Sección 2", Text("Contenido de la sección 2"))
        ],
        open_indices=[0],
        style={'margin-bottom': '20px'}
    ),
    
    Container(
        Text("Progreso y Carga", style={"font-weight": "bold", "margin-bottom": "10px"}),
        ProgressBar(value=70, max_value=100, style={'margin-bottom': '15px'}),
        Spinner(style={'margin-bottom': '15px'}),
        Tooltip(
            child=Button(
                "Pasa el mouse", 
                style={'background': '#6c757d', 'color': 'white', 'padding': '8px 16px', 'border': 'none', 'border-radius': '4px', 'cursor': 'help'}
            ), 
            text="Tooltip de ejemplo", 
            position="top"
        ),
        style={'padding': '20px', 'border': '1px solid #eee', 'border-radius': '8px'}
    ),
    style={
    'max-width': '900px',
    'margin': '40px auto',
    'padding': '32px',
    'background': 'white',
    'border-radius': '12px',
    'box-shadow': '0 2px 12px rgba(0,0,0,0.08)',
    'font-family': 'Arial, sans-serif'
})


app.root = main

if __name__ == "__main__":
    app.rTimeCompile()
