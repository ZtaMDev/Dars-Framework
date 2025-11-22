from dars.all import *
from dars.core.state import this
from dars.scripts.dscript import dScript

# Crear la aplicación
app = App(title="Mi App con Navbar Funcional")

# Función para crear el navbar (reutilizable en todas las páginas)
def crear_navbar():
    nav_style = {
        "color": "white", 
        "text-decoration": "none", 
        "margin-right": "20px", 
        "padding": "10px 15px", 
        "border-radius": "5px",
        "transition": "all 0.3s ease"
    }
    nav_hover = {
        "background-color": "rgba(255,255,255,0.2)",
        "transform": "translateY(-2px)"
    }
    
    home_link = Link(text="Inicio", href="/", style=nav_style, hover_style=nav_hover)
    about_link = Link(text="Acerca de", href="/about.html", style=nav_style, hover_style=nav_hover)
    contact_link = Link(text="Contacto", href="/contact.html", style=nav_style, hover_style=nav_hover)
    
    return Navbar(
        home_link, 
        about_link, 
        contact_link,
        brand="DarsApp",
        style={
            "background": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
            "padding": "15px 30px",
            "box-shadow": "0 4px 6px rgba(0,0,0,0.1)"
        }
    )

# PÁGINA DE INICIO
home_content = Container(
    Text(
        text="Bienvenido a DarsApp",
        style={
            "font-size": "3rem",
            "color": "#2c3e50",
            "text-align": "center",
            "margin": "50px 0 30px 0",
            "font-weight": "bold"
        }
    ),
    Text(
        text="Una aplicación de demostración construida con el framework Dars",
        style={
            "font-size": "1.3rem",
            "color": "#7f8c8d",
            "text-align": "center",
            "margin": "0 0 50px 0",
            "line-height": "1.6"
        }
    ),
    # --- COMPONENTES AVANZADOS DEMO ---
    Card([
        Text(text="Este es un Card avanzado con hijos", style={"margin-bottom": "10px"}),
        Link(text="Ir a Contacto", href="/contact.html", style={"color": "#667eea", "text-decoration": "none"}, hover_style={"text-decoration": "underline"})
    ], title="Demo Card", style={"margin": "30px auto", "max-width": "400px"}),

    # --- Modal con botón para cerrar ---
    Modal([
        Text(text="Este es el contenido de un Modal avanzado", style={"text-align": "center"}),
        Button(
            text="Cerrar Modal", 
            id="btn-cerrar-modal", 
            style={"margin": "20px auto 0 auto", "display": "block", "background": "#e74c3c", "color": "white", "border": "none", "padding": "10px 20px", "border-radius": "5px", "cursor": "pointer"},
            hover_style={"background": "#c0392b"},
            on_click=hideModal(id="modal-demo")
        )
    ], title="Demo Modal", is_open=False, id="modal-demo", style={"margin": "30px auto"}),
    
    Button(
        text="Mostrar Modal",
        id="btn-abrir-modal",
        style={"margin": "20px 0", "padding": "10px 20px", "background": "#667eea", "color": "white", "border": "none", "border-radius": "5px", "cursor": "pointer"},
        hover_style={"background": "#5a6fd6", "transform": "translateY(-2px)"},
        on_click=showModal(id="modal-demo")
    ),

    Tabs(
        minimum_logic=True,
        tabs=["Tab 1", "Tab 2", "Tab 3"],
        panels=[
            Text(text="Contenido de la pestaña 1"),
            Card([Text(text="Contenido dentro de un Card en Tab 2")]),
            Container(Text(text="Panel 3 con Container"))
        ],
        selected=0,
        style={"margin": "30px auto", "max-width": "600px"}
    ),

    Accordion(
        minimum_logic=True,
        sections=[
            ("Sección 1", Text(text="Contenido de la sección 1")),
            ("Sección 2", Card([Text(text="Contenido de la sección 2 en Card")]))
        ],
        open_indices=[0],
        style={"margin": "30px auto", "max-width": "600px"}
    ),

    Table(
        columns=[
            {"title": "Nombre", "field": "nombre"},
            {"title": "Edad", "field": "edad"}
        ],
        data=[
            {"nombre": "Ana", "edad": 28},
            {"nombre": "Luis", "edad": 34}
        ],
        style={"margin": "30px auto", "max-width": "400px"}
    ),
    
    style={
        "display": "flex",
        "flex-direction": "column",
        "align-items": "center"
    }
)

home_page = Page(
    crear_navbar(),
    home_content,
    style={
        "font-family": "Arial, sans-serif",
        "background": "linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%)",
        "min-height": "100vh"
    }
)

# PÁGINA ACERCA DE
about_content = Container(
    Text(
        text="Acerca de DarsApp",
        style={
            "font-size": "2.5rem",
            "color": "#2c3e50",
            "text-align": "center",
            "margin": "50px 0 30px 0",
            "font-weight": "bold"
        }
    ),
    Text(
        text="Nuestra Historia",
        style={
            "font-size": "1.8rem",
            "color": "#34495e",
            "text-align": "center",
            "margin-bottom": "20px",
            "font-weight": "bold"
        }
    ),
    Text(
        text="DarsApp es una aplicación de demostración que muestra las capacidades del framework Dars para crear interfaces web modernas y funcionales. Nuestro objetivo es proporcionar una experiencia de usuario excepcional a través de un diseño limpio y una navegación intuitiva.",
        style={
            "font-size": "1.1rem",
            "line-height": "1.8",
            "color": "#7f8c8d",
            "text-align": "center",
            "background": "white",
            "padding": "40px",
            "border-radius": "15px",
            "box-shadow": "0 5px 15px rgba(0,0,0,0.1)",
            "max-width": "800px",
            "margin": "0 auto"
        }
    ),
    style={
        "max-width": "1200px",
        "margin": "0 auto",
        "padding": "20px"
    }
)

about_page = Page(
    crear_navbar(),
    about_content,
    style={
        "font-family": "Arial, sans-serif",
        "background": "linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%)",
        "min-height": "100vh"
    }
)

# PÁGINA CONTACTO
contact_content = Container(
    Text(
        text="Contáctanos",
        style={
            "font-size": "2.5rem",
            "color": "#2c3e50",
            "text-align": "center",
            "margin": "50px 0 30px 0",
            "font-weight": "bold"
        }
    ),
    Text(
        text="Información de Contacto",
        style={
            "font-size": "1.8rem",
            "color": "#34495e",
            "margin-bottom": "30px",
            "font-weight": "bold",
            "text-align": "center"
        }
    ),
    Text(
        text="Contact INFO",
        style={
            "font-size": "1.1rem",
            "line-height": "2",
            "color": "#7f8c8d",
            "text-align": "center",
            "white-space": "pre-line",
            "background": "white",
            "padding": "40px",
            "border-radius": "15px",
            "box-shadow": "0 5px 15px rgba(0,0,0,0.1)",
            "max-width": "600px",
            "margin": "0 auto"
        }
    ),
    Text(
        text="Horario de Atención:\nLunes a Viernes: 9:00 AM - 6:00 PM\nSábados: 10:00 AM - 2:00 PM",
        style={
            "font-size": "1rem",
            "line-height": "1.6",
            "color": "#95a5a6",
            "text-align": "center",
            "margin-top": "30px",
            "white-space": "pre-line"
        }
    ),
    style={
        "max-width": "1200px",
        "margin": "0 auto",
        "padding": "20px"
    }
)

contact_page = Page(
    crear_navbar(),
    contact_content,
    style={
        "font-family": "Arial, sans-serif",
        "background": "linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%)",
        "min-height": "100vh"
    }
)

# Agregar estilos globales
app.add_global_style(selector="body", styles={
    "margin": "0",
    "padding": "0",
    "font-family": "Arial, sans-serif"
})

# Agregar todas las páginas a la aplicación
app.add_page(name="index", root=home_page, index=True)
app.add_page(name="about", root=about_page)
app.add_page(name="contact", root=contact_page)

if __name__ == "__main__":
    app.rTimeCompile()  # Preview en vivo
