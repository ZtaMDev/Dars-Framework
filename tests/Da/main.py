from dars.core.app import App
from dars.core.page import Page
from dars.components.basic.text import Text
from dars.components.basic.button import Button
from dars.components.basic.container import Container
from dars.components.advanced.card import Card
from dars.components.advanced.table import Table, TableColumn
from dars.components.advanced.tabs import Tabs, Tab

# Define la primera página
page1 = Page(
    name="home",
    title="Página de Inicio",
    root=Container(
        children=[
            Text("¡Bienvenido a mi aplicación Dars multi-página!"),
            Text("Esta es la página de inicio."),
            Button("Ir a la Página de Componentes", on_click="navigate_to_components"),
            Card(
                title="Información Importante",
                children=[
                    Text("Aquí puedes encontrar información relevante.")
                ]
            )
        ]
    )
)

# Define la segunda página con nuevos componentes
page2 = Page(
    name="components",
    title="Página de Componentes",
    root=Container(
        children=[
            Text("Demostración de Componentes Nuevos"),
            Tabs(
                tabs=[
                    Tab(
                        title="Tabla",
                        id="button-tab",
                        content=Table(
                            columns=[
                                TableColumn(key="Nombre", title="name"),
                                TableColumn(key="Edad", title="age")
                            ],
                            data=[
                                {"name": "Alice", "age": 30},
                                {"name": "Bob", "age": 24}
                            ]
                        )
                    ),
                    Tab(
                        id="button-tab",
                        title="Botón",
                        content=Button("Haz clic aquí", on_click="alert('Botón clickeado!')")
                    )
                ]
            ),
            Button("Volver a Inicio", on_click="navigate_to_home")
        ]
    )
)

# Crea la aplicación y añade las páginas
app = App(
    title="Mi App Multi-Página Dars",
    description="Una aplicación Dars de ejemplo con múltiples páginas y nuevos componentes."
)

app.add_page(page1)
app.add_page(page2)

# Puedes establecer la página principal explícitamente si no es la primera que añades
# app.main_page = "home"

# Para ejecutar esta aplicación, guarda este código como un archivo .py (ej. app.py)
# y luego usa el comando dars export:
# dars export app.py --format html --output ./dist

# Nota: El exportador actual (HTMLCSSJSExporter) solo exportará la página principal
# (index.html). Para un soporte completo de multi-página, se requeriría una
# implementación adicional en el exportador para generar un archivo HTML por cada página.

# Para previsualizar la aplicación (solo la página principal):
# dars preview ./dist