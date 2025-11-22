# Ejemplo de uso del sistema multipágina de Dars
from dars.all import *

# Instancia de la app
app = App(title="Demo Multipágina Dars", description="Ejemplo de múltiples páginas con Dars")

# Página principal
home = Page(
    Text("Bienvenido a la página principal de Dars!"),
    Button(
        "Ir a Sobre Nosotros", 
        id="btn-about", 
        class_name="dars-btn-link", 
        style={"margin": "16px"},
        on_click=dScript("window.location.href = 'about.html'"),
        on_mouse_enter=this().state(style={'text-decoration': 'underline'}),
        on_mouse_leave=this().state(style={'text-decoration': 'none'})
    )
)

about = Page(
    Text("Sobre Nosotros: Dars es un framework Python para la web."),
    Button(
        "Volver al inicio", 
        id="btn-home", 
        class_name="dars-btn-link", 
        style={"margin": "16px"},
        on_click=dScript("window.location.href = 'index.html'"),
        on_mouse_enter=this().state(style={'text-decoration': 'underline'}),
        on_mouse_leave=this().state(style={'text-decoration': 'none'})
    )
)

contact = Page(
    Text("Contacto: Escríbenos a contacto@dars.dev"),
    Button(
        "Volver al inicio", 
        id="btn-home2", 
        class_name="dars-btn-link", 
        style={"margin": "16px"},
        on_click=dScript("window.location.href = 'index.html'"),
        on_mouse_enter=this().state(style={'text-decoration': 'underline'}),
        on_mouse_leave=this().state(style={'text-decoration': 'none'})
    )
)

# Registro multipágina
app.add_page("home", home, title="Inicio", index=True)
app.add_page("about", about, title="Sobre Nosotros")
app.add_page("contact", contact, title="Contacto")

if __name__ == '__main__':
    app.rTimeCompile()
