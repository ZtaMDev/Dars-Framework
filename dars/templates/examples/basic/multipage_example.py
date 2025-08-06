# Ejemplo de uso del sistema multipágina de Dars
from dars.core.app import App
from dars.components.basic.page import Page
from dars.components.basic.text import Text
from dars.components.basic.button import Button
from dars.scripts.script import InlineScript

# Instancia de la app
app = App(title="Demo Multipágina Dars", description="Ejemplo de múltiples páginas con Dars")

# Página principal
home = Page(
    Text("Bienvenido a la página principal de Dars!"),
    Button("Ir a Sobre Nosotros", id="btn-about", class_name="dars-btn-link", style={"margin": "16px"})
)
# Script solo para la home
home.add_script(InlineScript("""
document.addEventListener('DOMContentLoaded', function() {
    var btn = document.getElementById('btn-about');
    if (btn) {
        btn.addEventListener('click', function() {
            window.location.href = 'about.html';
        });
    }
});
"""))

about = Page(
    Text("Sobre Nosotros: Dars es un framework Python para la web."),
    Button("Volver al inicio", id="btn-home", class_name="dars-btn-link", style={"margin": "16px"})
)
about.add_script(InlineScript("""
document.addEventListener('DOMContentLoaded', function() {
    var btn = document.getElementById('btn-home');
    if (btn) {
        btn.addEventListener('click', function() {
            window.location.href = 'index.html';
        });
    }
});
"""))

contact = Page(
    Text("Contacto: Escríbenos a contacto@dars.dev"),
    Button("Volver al inicio", id="btn-home2", class_name="dars-btn-link", style={"margin": "16px"})
)
contact.add_script(InlineScript("""
document.addEventListener('DOMContentLoaded', function() {
    var btn = document.getElementById('btn-home2');
    if (btn) {
        btn.addEventListener('click', function() {
            window.location.href = 'index.html';
        });
    }
});
"""))


# Registro multipágina
# ¡IMPORTANTE! Nunca pases una lista como root, siempre un solo componente (Container, etc)
# El exporter ahora también protege automáticamente y envuelve listas en un Container.
app.add_page("home", home, title="Inicio", index=True)
app.add_page("about", about, title="Sobre Nosotros")
app.add_page("contact", contact, title="Contacto")

# También sigue funcionando el modo clásico (single-page):
#app.set_root(home)

if __name__ == "__main__":
    app.rTimeCompile()
