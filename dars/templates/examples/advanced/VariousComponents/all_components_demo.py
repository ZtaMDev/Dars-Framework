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

main = Container(style={
    'max-width': '900px',
    'margin': '40px auto',
    'padding': '32px',
    'background': 'white',
    'border-radius': '12px',
    'box-shadow': '0 2px 12px rgba(0,0,0,0.08)'
})

main.children += [
    Text("Demostración de TODOS los componentes de Dars", style={"font-size": "2rem", "font-weight": "bold", "margin-bottom": "24px"}),
    # Básicos
    Text("Componentes Básicos", style={"font-size": "1.3rem", "margin": "24px 0 12px 0", "color": "#007bff"}),
    Text("Texto de ejemplo", style={"margin-bottom": "8px"}),
    Button("Botón primario"),
    Input(placeholder="Campo de texto"),
    Image(src="https://via.placeholder.com/120x60.png?text=Logo", alt="Logo Demo", style={"margin": "10px 0"}),
    Link("Ir a Dars Framework", href="https://github.com/ZtaMDev/Dars-Framework", target="_blank"),
    Textarea(value="Texto multilinea de ejemplo", rows=3),
    Checkbox(label="Acepto términos y condiciones", checked=True),
    RadioButton(label="Opción A", name="grupo1", checked=True),
    RadioButton(label="Opción B", name="grupo1"),
    Select(options=[SelectOption("uno", "Uno"), SelectOption("dos", "Dos")], value="uno", placeholder="Selecciona una opción"),
    Slider(min_value=0, max_value=100, value=50, label="Volumen", show_value=True),
    DatePicker(value="2025-08-06"),
    # Avanzados
    Text("Componentes Avanzados", style={"font-size": "1.3rem", "margin": "32px 0 12px 0", "color": "#4a90e2"}),
    Table(
        columns=[{"title": "Nombre", "field": "nombre"}, {"title": "Edad", "field": "edad"}],
        data=[{"nombre": "Ana", "edad": 28}, {"nombre": "Luis", "edad": 34}],
        page_size=10
    ),
    Tabs(
        tabs=["Tab 1", "Tab 2"],
        panels=[Text("Contenido de la pestaña 1"), Text("Contenido de la pestaña 2")],
        selected=0
    ),
    Accordion(
        sections=[
            ("Sección 1", Text("Contenido de la sección 1")),
            ("Sección 2", Text("Contenido de la sección 2"))
        ],
        open_indices=[0]
    ),
    ProgressBar(value=70, max_value=100),
    Spinner(),
    Tooltip(child=Button("Pasa el mouse"), text="¡Tooltip de ejemplo!", position="top")
]

app.root = main

if __name__ == "__main__":
    app.rTimeCompile()
