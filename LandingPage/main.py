from dars.all import *
from getting_started import getting_started_comp
from scripts import *
from component_based import *
from custom_section import *
from dars.components.basic.markdown import Markdown
from dars.core.component import Component
app = App(
    title="Dars Landing-Page", 
    language="en", 
    favicon="Dars-logo.png", 
    apple_touch_icon="Dars-logo.png", 
    author="ZtaMDev", 
    description="Dars framework landing page for the UI multiplatform python framework", 
    theme_color="#121212", 
    background_color="#121212")
app.add_global_style(selector="body", styles={
    "background-color": "#212529",
    "min-height": "100vh",
    "margin": "0",
    "font-family": "Arial, sans-serif",
    "background": "linear-gradient(to bottom, #212529, #304635)"
})

mobile_detection_scriptorg = """ function isMobileDevice2() { return (typeof window.orientation !== "undefined") || (navigator.userAgent.indexOf('IEMobile') !== -1) || (navigator.userAgent.indexOf('Android') !== -1) || (navigator.userAgent.indexOf('iPhone') !== -1) || (navigator.userAgent.indexOf('iPad') !== -1) || (navigator.userAgent.indexOf('iPod') !== -1) || (window.innerWidth <= 850); } 
function initMobileDetection2() { if (isMobileDevice2()) { setTimeout(function() { var modal = document.getElementById('mobile-warning-modal'); if (modal) { modal.style.display = 'flex'; } }, 1000); } window.addEventListener('resize', function() { var modal = document.getElementById('mobile-warning-modal'); if (window.innerWidth <= 850) { if (modal) modal.style.display = 'flex'; } else { if (modal) modal.style.display = 'none'; } }); } if (document.readyState === 'loading') { document.addEventListener('DOMContentLoaded', initMobileDetection); } else { initMobileDetection2(); } """
def section_divider():
    return Container(
        style={
            "height": "2px",
            "width": "80%",
            "margin": "50px auto",
            "background": "linear-gradient(to right, transparent, #00d68f60, transparent)",
            "border-radius": "2px"
        }
    )
#script detector:
mobile_detection_script = """
function isMobileDevice() {
    return (typeof window.orientation !== "undefined") || 
           (navigator.userAgent.indexOf('IEMobile') !== -1) ||
           (navigator.userAgent.indexOf('Android') !== -1) ||
           (navigator.userAgent.indexOf('iPhone') !== -1) ||
           (navigator.userAgent.indexOf('iPad') !== -1) ||
           (navigator.userAgent.indexOf('iPod') !== -1) ||
           (window.innerWidth <= 850);
}

function handlePlaygroundLink() {
    // KEEP: Always keep the Playground link visible on all devices
    var playgroundLink = document.getElementById('linkPlayground');
    if (!playgroundLink) return;
    playgroundLink.style.display = ""; // ensure visible
}

function initMobileDetection() {
    // Ejecutar al cargar
    handlePlaygroundLink();

    // Re-verificar al redimensionar (no ocultaremos el playground)
    window.addEventListener('resize', handlePlaygroundLink);
}

// Esperar a que el DOM esté cargado
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initMobileDetection);
} else {
    initMobileDetection();
}

"""
# Crea el modal de advertencia para móviles(UNUSED)
mobile_warning_modal = Container(
    Container(
        Container(
            Text("Limited experience on mobile devices",  
                 style={"font-size": "1.5rem", "font-weight": "bold", "color": "#00d68f", "margin-bottom": "20px", "text-align": "center"}),
            Text("The mobile version of Dars Framework page isn't already optimized for mobile devices.", 
                 style={"margin-bottom": "15px", "color": "#b2ffe5", "text-align": "center"}),
            Text("For better experience, please visit this page from a computer.", 
                 style={"margin-bottom": "20px", "color": "#b2ffe5", "text-align": "center"}),
            Container(
                Button(
                    text="Continue", 
                    on_click=dScript(code="document.getElementById('mobile-warning-modal').style.display = 'none';"),
                    style={"background-color": "#00d68f", "color": "#212529", "padding": "10px 20px", "border-radius": "5px", "border": "none", "cursor": "pointer", "font-weight": "bold", "margin": "0 auto", "display": "block"}
                ),
                style={"text-align": "center"}
            ),
            style={"padding": "30px", "text-align": "center"}
        ),
        style={"background-color": "#304635", "border-radius": "10px", "padding": "20px", "border": "2px solid #00d68f", "max-width": "90%", "width": "400px"}
    ),
    id="mobile-warning-modal",
    style={
        "position": "fixed",
        "top": "0",
        "left": "0",
        "width": "100%",
        "height": "100%",
        "background-color": "rgba(0, 0, 0, 0.85)",
        "display": "none",
        "z-index": "10000",
        "justify-content": "center",
        "align-items": "center"
    }
)
#styles:
LINK_STYLE = {"color": "#b2ffe5", "text-decoration": "none", "border-radius": "5px", "padding": "8px 5px"}
NAVBAR_A_STYLE = {"transition" : "all 0.5s ease", "justify-content" : "center"}
NAVBAR_A_HOVER = {"background-color": "#00d68f50", "transition": "all 0.5s ease"}
IMAGE_NAVBAR_STYLE = {
    "height": "30px",
    "display": "flex",
    "align-items": "center",
}

#global styles:
app.add_global_style(selector=".dars-navbar-nav a:hover", styles=NAVBAR_A_HOVER)
app.add_global_style(selector=".dars-navbar-nav a", styles=NAVBAR_A_STYLE)
app.add_global_style(selector="#navbar-container > div", styles={"width": "100%"})
app.add_global_style(selector=".dars-navbar", styles={"display": "flex", "width": "100%", "box-sizing": "border-box"})
app.add_global_style(".dars-navbar-nav", {"flex-wrap": "wrap"})

app.add_global_style(
    selector="#start-container", 
    styles={
        "display": "flex",
        "justify-content": "space-between",
        "align-items": "center",
        "width": "100%",
        "padding": "10px 20px",
        "background-color": "#304635",
        "border-bottom": "2px solid #00d68f",
        "box-sizing": "border-box"
    }
)

# Estilos para el modal de advertencia móvil
app.add_global_style(
    selector="#mobile-warning-modal",
    styles={
        "position": "fixed",
        "top": "0",
        "left": "0",
        "width": "100%",
        "height": "100%",
        "background-color": "rgba(0, 0, 0, 0.85)",
        "display": "none",
        "z-index": "10000",
        "justify-content": "center",
        "align-items": "center"
    }
)

app.add_global_style(
    selector="#mobile-warning-modal .dars-modal-content",
    styles={
        "background-color": "#304635",
        "border-radius": "10px",
        "padding": "30px",
        "max-width": "90%",
        "width": "400px",
        "border": "2px solid #00d68f",
        "text-align": "center"
    }
)

app.add_global_style(
    selector="#mobile-warning-modal .dars-modal-title",
    styles={
        "color": "#00d68f",
        "font-size": "1.5rem",
        "margin-bottom": "20px"
    }
)

app.add_global_style(
    selector="#navbar-left", 
    styles={
        "display": "flex", 
        "align-items": "center", 
        "gap": "8px",
    }
)

app.add_global_style(
    selector="#navbar-right", 
    styles={
        "display": "flex", 
        "align-items": "center", 
        "gap": "15px",
    }
)
# Estilos para la sección hero
app.add_global_style(
    selector="#hero-section",
    styles={
        "display": "flex",
        "align-items": "center",
        "justify-content": "space-between",
        "max-width": "1200px",
        "margin": "0 auto",
        "padding": "60px 20px",
        "gap": "40px"
    }
)
app.add_global_style(
    selector="#hero-image",
    styles={
        "flex": "1",
        "display": "flex",
        "justify-content": "center",
        "position": "relative"
    }
)
app.add_global_style(
    selector="#hero-text",
    styles={
        "flex": "1",
        "padding-right": "40px"
    }
)

app.add_global_style(
    selector="#hero-image",
    styles={
        "flex": "1",
        "display": "flex",
        "justify-content": "center"
    }
)

app.add_global_style(
    selector="#how-it-works",
    styles={
        "background-color": "#1e2b23",
        "padding": "80px 20px",
        "border-top": "2px solid #00d68f",
        "border-bottom": "2px solid #00d68f"
    }
)

app.add_global_style(
    selector="footer a",
    styles={
        "color": "#00d68f",
        "text-decoration": "none",
        "font-weight": "bold",
        "transition": "color 0.3s ease"
    }
)
app.add_global_style(
    selector="#hero-image",
    styles={
        "flex": "1",
        "display": "flex",
        "justify-content": "center",
        "position": "relative"
    }
)
app.add_global_style(
    selector="footer a:hover",
    styles={
        "color": "#b2ffe5",
        "text-decoration": "underline"
    }
)
app.add_global_style(selector="body", styles={
     "background-color": "#212529",
     "margin": "0",
     "padding": "0",
     "font-family": "Arial, sans-serif"
})

app.add_global_style(
    selector="#how-it-works a",
    styles={
        "color": "#00d68f",
        "text-decoration": "underline",
        "font-weight": "bold",
        "transition": "color 0.3s ease"
    }
)

app.add_global_style(
    selector="#how-it-works a:hover",
    styles={
        "color": "#b2ffe5",
        "text-decoration": "underline"
    }
)
app.add_global_style(selector="h1, h2, h3, h4, h5, h6", styles={
    "color": "#00d68f"
})

app.add_global_style(selector="p", styles={
    "color": "#b2ffe5",
    "line-height": "1.6"
})

# Agrega esto con los otros estilos globales
app.add_global_style(
    selector="#how-it-works h2, #how-it-works h1, #how-it-works .dars-text", 
    styles={
        "text-align": "center",
        "width": "100%",
        "display": "block"
    }
)

# Fondo principal del contenedor de documentación
app.add_global_style(
    selector="#markdown_docs",
    styles={
        "background-color": "#1e2b23",
        "color": "#b2ffe5",
        "padding": "40px",
        "border-radius": "10px",
        "max-width": "900px",
        "margin": "40px auto",
        "box-shadow": "0 5px 15px rgba(0,0,0,0.3)",
        "line-height": "1.6"
    }
)

# Títulos
app.add_global_style(
    selector="#markdown_docs h1, #markdown_docs h2, #markdown_docs h3, #markdown_docs h4, #markdown_docs h5, #markdown_docs h6",
    styles={
        "color": "#00d68f",
        "margin-top": "1.5em",
        "margin-bottom": "0.5em",
        "font-weight": "600"
    }
)

# Texto y listas
app.add_global_style(
    selector="#markdown_docs p, #markdown_docs li",
    styles={
        "color": "#b2ffe5",
        "margin-bottom": "1em"
    }
)

# Links
app.add_global_style(
    selector="#markdown_docs a",
    styles={
        "color": "#00d68f",
        "text-decoration": "underline",
        "font-weight": "bold",
        "transition": "color 0.3s ease"
    }
)
app.add_global_style(
    selector="#markdown_docs a:hover",
    styles={
        "color": "#b2ffe5"
    }
)

# Código inline
app.add_global_style(
    selector="#markdown_docs code",
    styles={
        "background-color": "#2a3b2f",
        "color": "#b2ffe5",
        "padding": "4px 6px",
        "border-radius": "4px",
        "font-family": "monospace",
        "font-size": "0.9em"
    }
)

# Bloques de código
app.add_global_style(
    selector="#markdown_docs pre",
    styles={
        "background-color": "#2a3b2f",
        "color": "#b2ffe5",
        "padding": "15px",
        "border-radius": "6px",
        "overflow": "auto",
        "margin-bottom": "1.5em",
        "border": "1px solid #00d68f30"
    }
)

# Citas
app.add_global_style(
    selector="#markdown_docs blockquote",
    styles={
        "border-left": "4px solid #00d68f",
        "background-color": "#304635",
        "padding": "10px 15px",
        "border-radius": "6px",
        "color": "#b2ffe5",
        "font-style": "italic",
        "margin": "20px 0"
    }
)

# Tablas
app.add_global_style(
    selector="#markdown_docs table",
    styles={
        "border-collapse": "collapse",
        "width": "100%",
        "margin-bottom": "1.5em"
    }
)
app.add_global_style(
    selector="#markdown_docs th, #markdown_docs td",
    styles={
        "border": "1px solid #00d68f40",
        "padding": "8px",
        "text-align": "left",
        "color": "#b2ffe5"
    }
)
app.add_global_style(
    selector="#markdown_docs th",
    styles={
        "background-color": "#304635",
        "color": "#00d68f",
        "font-weight": "600"
    }
)

# Separadores
app.add_global_style(
    selector="#markdown_docs hr",
    styles={
        "border": "none",
        "height": "1px",
        "background-color": "#00d68f50",
        "margin": "2em 0"
    }
)

# Navbar base
app.add_global_style(
    selector="#dars-navbar",
    styles={
        "display": "flex",
        "justify-content": "space-between",
        "align-items": "center",
        "width": "100%",
        "padding": "15px 30px",
        "position": "sticky",
        "top": "0",
        "z-index": "1000",
        "background": "linear-gradient(135deg, rgba(33,37,41,0.9), rgba(48,70,53,0.85))",
        "backdrop-filter": "blur(10px)",
        "border-bottom": "1px solid rgba(0, 214, 143, 0.3)",
        "box-shadow": "0 2px 10px rgba(0,0,0,0.4)",
    }
)

# Links de navegación (desktop)
app.add_global_style(
    selector="#navbar-right",
    styles={
        "display": "flex",
        "align-items": "center",
        "gap": "20px"
    }
)

app.add_global_style(
    selector=".dars-navbar-nav .nav-link",
    styles={
        "color": "#b2ffe5",
        "font-size": "1rem",
        "font-weight": "500",
        "margin": "0 10px",
        "text-decoration": "none",
        "position": "relative",
        "transition": "color 0.3s ease",
    }
)

# Hover animado
app.add_global_style(
    selector=".dars-navbar-nav .nav-link::after",
    styles={
        "content": "''",
        "position": "absolute",
        "width": "0%",
        "height": "2px",
        "left": "0",
        "bottom": "-4px",
        "background-color": "#00d68f",
        "transition": "width 0.3s ease",
    }
)
app.add_global_style(
    selector=".dars-navbar-nav .nav-link:hover",
    styles={"color": "#00d68f"}
)
app.add_global_style(
    selector=".dars-navbar-nav .nav-link:hover::after",
    styles={"width": "100%"}
)


# Desktop: ocultar hamburguesa
app.add_global_style(
    selector="@media (min-width: 769px)",
    styles={
        "#navbar-hamburger": {
            "display": "none"
        }
    }
)

# Mobile: mostrar hamburguesa y mostrar menú como panel lateral
app.add_global_style(
    selector="@media (max-width: 768px)",
    styles={
        "#navbar-hamburger": {
            "display": "block"
        },
        "#navbar-right": {
            "position": "fixed",
            "top": "0",
            "right": "-100%",
            "height": "100%",
            "width": "70%",
            "max-width": "320px",
            "background": "#1e2b23",
            "flex-direction": "column",
            "padding": "60px 20px",
            "gap": "18px",
            "box-shadow": "-2px 0 12px rgba(0,0,0,0.5)",
            "transition": "right 0.28s ease",
            "z-index": "2000"
        },
        "#navbar-right.open": {
            "right": "0px"
        },
        ".dars-navbar-nav .nav-link": {
            "font-size": "1.05rem",
            "padding": "12px 0",
            "width": "100%",
            "border-bottom": "1px solid rgba(0,214,143,0.06)",
            "display": "block"
        },
        "#dars-navbar": {
            "padding": "10px 14px"
        }
    }
)

def create_navbar():
    left_block = Container(
        Image(
            alt="Logo",
            src="Dars-logo.png",
            width="40px",
            height="40px",
            style={"object-fit": "contain", "margin-right": "10px"}
        ),
        Text(
            text="Dars Framework",
            style={"font-size": "20px", "font-weight": "700", "color": "#b2ffe5", "margin": "0"}
        ),
        id="navbar-left"
    )

    right_block = Container(
        Link("Home", href="https://ztamdev.github.io/Dars-Framework/", class_name="nav-link"),
        Link("About", href="https://ztamdev.github.io/Dars-Framework/about.html", class_name="nav-link"),
        Link("Download", href="https://ztamdev.github.io/Dars-Framework/downloads.html", class_name="nav-link"),
        Link("Playground", href="https://dars-playground.vercel.app/", class_name="nav-link", id="linkPlayground"),
        Link("Documentation", href="https://ztamdev.github.io/Dars-Framework/documentation.html", class_name="nav-link"),
        id="navbar-right",
        class_name="dars-navbar-nav"
    )

    # Botón hamburguesa (aparece en móvil)
    hamburger = Container(
        Text("☰", style={
            "font-size": "28px",
            "color": "#b2ffe5",
            "cursor": "pointer",
            "padding": "5px 10px"
        }),
        id="navbar-hamburger",
        style={"display": "none"}
    )

    return Navbar(
        left_block,
        right_block,
        hamburger,
        id="dars-navbar"
    )

navbar_script = dScript(code="""
document.addEventListener('DOMContentLoaded', function initNav() {
    const navRight = document.getElementById('navbar-right');
    const burger = document.getElementById('navbar-hamburger');

    // Safety guards in case elements are not present yet
    if (!burger || !navRight) return;

    // Ensure overlay exists (hidden) so we can reuse it
    let overlay = document.getElementById('nav-overlay');
    if (!overlay) {
        overlay = document.createElement('div');
        overlay.id = 'nav-overlay';
        overlay.style.position = 'fixed';
        overlay.style.top = '0';
        overlay.style.left = '0';
        overlay.style.width = '100%';
        overlay.style.height = '100%';
        overlay.style.background = 'rgba(0,0,0,0.35)';
        overlay.style.zIndex = '1999';
        overlay.style.display = 'none';
        document.body.appendChild(overlay);
    }

    function openMenu() {
        navRight.classList.add('open');
        overlay.style.display = 'block';
    }
    function closeMenu() {
        navRight.classList.remove('open');
        overlay.style.display = 'none';
    }

    burger.addEventListener('click', function (e) {
        e.stopPropagation();
        if (navRight.classList.contains('open')) closeMenu(); else openMenu();
    });

    // Close when clicking overlay
    overlay.addEventListener('click', function () {
        closeMenu();
    });

    // Close menu when any nav link is clicked (mobile behavior)
    const links = navRight.querySelectorAll('.nav-link');
    links.forEach(link => link.addEventListener('click', closeMenu));

    // Also close when tapping outside via document listener
    document.addEventListener('click', function (ev) {
        const target = ev.target;
        if (!navRight.contains(target) && target !== burger) {
            if (navRight.classList.contains('open')) closeMenu();
        }
    });
});
""")
app.add_script(navbar_script)
app.add_global_style(
    selector="""
#page-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: #212529;  /* mismo color de fondo de la página */
    z-index: 9999;
    display: flex;
    justify-content: center;
    align-items: center;
    opacity: 1;
    transition: opacity 1.5s ease;
}

#overlay-logo {
    width: 150px;
    height: 150px;
    animation: floatLogo 2s ease-in-out infinite alternate;
}

@keyframes floatLogo {
    0% { transform: translateY(0px) scale(1); opacity: 1; }
    50% { transform: translateY(-15px) scale(1.05); opacity: 0.9; }
    100% { transform: translateY(0px) scale(1); opacity: 1; }
}
"""
, styles={"":""})
overlay_script = dScript(code="""
window.addEventListener('load', () => {
    const overlay = document.getElementById('page-overlay');
    if (overlay) {
        overlay.style.opacity = '0';
        setTimeout(() => overlay.remove(), 1600);  // se elimina después de la transición
    }
});
""")
app.add_script(overlay_script)
app.add_global_style(file_path="exmp.css")
overlay = Container(
    Image(
        src="Dars-logo.png", 
        alt="Dars Framework Logo",
        id="overlay-logo"
    ),
    id="page-overlay"
)

#pages:
index = Page(
    FlexLayout(
        children=[create_navbar()],
        wrap="no_wrap",
        justify="flex-start",
        align="center",
        id="navbar-container",
        style={"width": "100%"}
    ),
    # Hero Section con imagen a la izquierda y texto a la derecha
    Container(
        Container(
            Container(
                # Imagen a la izquierda con fondo de código
                Container(
                    Container(
                        Image(
                            alt="Dars Framework Logo", 
                            src="Dars-logo.png", 
                            width="300px", 
                            height="300px",
                            style={"max-width": "100%", "height": "auto", "border-radius": "10px", "box-shadow": "0 5px 15px rgba(0,0,0,0.3)", "position": "relative", "z-index": "2"}
                        ),
                        style={"position": "relative", "z-index": "2"},
                        id="code-background-container"
                    ),
                    style={"position": "relative", "padding": "20px"},
                    id="hero-image"
                ),
                # Texto a la derecha
                Container(
                    Text("Dars Framework", style={"font-size": "2.8rem", "font-weight": "bold", "color": "#00d68f", "margin-bottom": "20px"}),
                    Text("Dynamic Application Rendering System is an modern Python framework for web development", style={"font-size": "1.3rem", "color": "#b2ffe5", "margin-bottom": "30px", "line-height": "1.5"}),
                    Text("Dars is designed to make web development simple, fast, and enjoyable. With an intuitive API and powerful features, you can build modern web applications in record time using Python.", style={"font-size": "1.1rem", "color": "#b2ffe5", "margin-bottom": "40px", "line-height": "1.6"}),
                    Container(
                        Button(
                            text="Get Started", 
                            on_click=dScript(code="""
                                document.getElementById('getting-started-section').scrollIntoView({
                                    behavior: 'smooth'
                                });
                            """),
                            style={"background-color": "#00d68f", "color": "#212529", "padding": "12px 24px", "border-radius": "5px", "text-decoration": "none", "font-weight": "bold", "margin": "0 10px", "border": "none", "cursor": "pointer"}
                        ),

                        Button(
                            text="View Documentation", 
                            on_click=dScript(code="window.open('https://ztamdev.github.io/Dars-Framework/documentation.html', '_blank');"),
                            style={"background-color": "transparent", "color": "#00d68f", "padding": "12px 24px", "border-radius": "5px", "text-decoration": "none", "border": "2px solid #00d68f", "font-weight": "bold", "margin": "0 10px", "cursor": "pointer"}
                        ),
                        style={"display": "flex", "flex-wrap": "wrap", "gap": "15px"}
                    ),
                    id="hero-text"
                ),
                id="hero-section"
            ),
            style={"max-width": "1200px", "margin": "0 auto"}
        ),
        style={"padding": "40px 0", "background": "linear-gradient(to bottom, #212529, #304635)"}
    ),
    
    # Sección "Cómo funciona"
    Container(
        Container(
            Text("How Dars Framework Works", style={"font-size": "2.5rem", "font-weight": "bold", "color": "#00d68f", "text-align": "center", "margin-bottom": "50px"}),
            section_divider(),
            Container(
                Container(
                    Text("1. Install", style={"font-size": "1.8rem", "font-weight": "bold", "color": "#00d68f", "margin-bottom": "15px"}),
                    Container(
                        Text("Install Dars with a simple ", style={"color": "#b2ffe5", "display": "inline", "line-height": "1.6"}),
                        Link("pip command", href="https://ztamdev.github.io/Dars-Framework/downloads.html", style={"color": "#00d68f", "text-decoration": "underline", "display": "inline", "font-weight": "bold"}),
                        Text(" and start building immediately.", style={"color": "#b2ffe5", "display": "inline", "line-height": "1.6"}),
                        style={"line-height": "1.6"}
                    ),
                    style={"background-color": "#2a3b2f", "padding": "30px", "border-radius": "8px", "flex": "1", "min-width": "250px", "text-align": "center", "box-shadow": "0 4px 6px rgba(0, 0, 0, 0.2)"}
                ),
                Container(
                    Text("2. Develop", style={"font-size": "1.8rem", "font-weight": "bold", "color": "#00d68f", "margin-bottom": "15px"}),
                    Text("Use the intuitive API to create routes, components, and pages with minimal code.", style={"color": "#b2ffe5", "line-height": "1.6"}),
                    style={"background-color": "#2a3b2f", "padding": "30px", "border-radius": "8px", "flex": "1", "min-width": "250px", "text-align": "center", "box-shadow": "0 4px 6px rgba(0, 0, 0, 0.2)"}
                ),
                Container(
                    Text("3. Deploy", style={"font-size": "1.8rem", "font-weight": "bold", "color": "#00d68f", "margin-bottom": "15px"}),
                    Text("Deploy your application in the test built-in server or your preferred hosting provider.", style={"color": "#b2ffe5", "line-height": "1.6"}),
                    style={"background-color": "#2a3b2f", "padding": "30px", "border-radius": "8px", "flex": "1", "min-width": "250px", "text-align": "center", "box-shadow": "0 4px 6px rgba(0, 0, 0, 0.2)"}
                ),
                style={"display": "flex", "flex-wrap": "wrap", "gap": "20px", "justify-content": "center", "max-width": "1000px", "margin": "0 auto"}
            ),
            style={"max-width": "1200px", "margin": "0 auto", "padding": "0 20px"}
        ),
        id="how-it-works",
        style={"background-color": "#1e2b23", "padding": "80px 20px", "border-top": "2px solid #00d68f", "border-bottom": "2px solid #00d68f"}
    ),
    compb,
    getting_started_comp,
    # Footer
    Container(
        Container(
            Text("Created with ", style={"color": "#b2ffe5", "display": "inline", "margin-right": "5px"}),
            Link("Dars Framework", href="https://github.com/ZtaMDev/Dars-Framework", style={"color": "#00d68f", "text-decoration": "none", "font-weight": "bold", "display": "inline"}),
            Text(" • Documentation: ", style={"color": "#b2ffe5", "display": "inline", "margin": "0 5px"}),
            Link("Getting Started", href="https://ztamdev.github.io/Dars-Framework/documentation.html", style={"color": "#00d68f", "text-decoration": "none", "font-weight": "bold", "display": "inline"}),
            Text(" • Developer: ", style={"color": "#b2ffe5", "display": "inline", "margin": "0 5px"}),
            Link("ZtaDev", href="https://github.com/ZtaMDev", style={"color": "#00d68f", "text-decoration": "none", "font-weight": "bold", "display": "inline"}),
            style={"text-align": "center", "padding": "30px 20px", "border-top": "1px solid #304635"}
        ),
        style={"background-color": "#1e2b23", "margin-top": "auto"}
    ),
    id="index-page",
    style={"background-color": "#212529", "min-height": "100vh", "margin": "0", "font-family": "Arial, sans-serif"}
)

about = Page(
    FlexLayout(
        children=[create_navbar()],
        wrap="no_wrap",
        justify="flex-start",
        align="center",
        id="navbar-container",
        style={"width": "100%"}
    ),
    Container(
        Container(
            # Hero Section con imagen de fondo
            Container(
                Container(
                    Text("About Dars Framework", 
                        style={"font-size": "3.5rem", "font-weight": "bold", "color": "#00d68f", "text-align": "center", "margin-bottom": "20px", "text-shadow": "0 2px 4px rgba(0,0,0,0.5)"}),
                    Text("The Modern Python Framework for Web Development", 
                        style={"font-size": "1.5rem", "color": "#b2ffe5", "text-align": "center", "margin-bottom": "40px", "line-height": "1.5"}),
                    style={"padding": "80px 20px", "text-align": "center"}
                ),
                style={
                    "background": "linear-gradient(rgba(33, 37, 41, 0.9), rgba(48, 70, 53, 0.9)), url('Dars-logo.png') center/cover",
                    "border-radius": "15px",
                    "margin-bottom": "60px",
                    "box-shadow": "0 10px 30px rgba(0, 0, 0, 0.3)"
                }
            ),
            section_divider(),
            # What is Dars Section
            Container(
                Container(
                    Text("What is Dars Framework?", 
                        style={"font-size": "2.5rem", "font-weight": "bold", "color": "#00d68f", "margin-bottom": "30px", "text-align": "center", "position": "relative"}),
                    
                    Container(
                        Container(
                            Text("Dars (Dynamic Application Rendering System) is an innovative Python framework designed to simplify web development while maintaining power and flexibility.", 
                                style={"font-size": "1.2rem", "color": "#b2ffe5", "line-height": "1.8", "margin-bottom": "25px"}),
                            
                            Container(
                                Container(
                                    Text("Component-Based", 
                                        style={"font-size": "1.3rem", "font-weight": "bold", "color": "#00d68f", "margin-bottom": "10px"}),
                                    Text("Build with reusable components that make development faster and more maintainable", 
                                        style={"color": "#b2ffe5", "line-height": "1.6", "font-size": "0.95rem"}),
                                    style={"padding": "20px", "flex": "1", "min-width": "250px"}
                                ),
                                Container(
                                    Text("Python-Powered", 
                                        style={"font-size": "1.3rem", "font-weight": "bold", "color": "#00d68f", "margin-bottom": "10px"}),
                                    Text("Leverage Python's simplicity and ecosystem without learning new complex syntax", 
                                        style={"color": "#b2ffe5", "line-height": "1.6", "font-size": "0.95rem"}),
                                    style={"padding": "20px", "flex": "1", "min-width": "250px"}
                                ),
                                style={"display": "flex", "flex-wrap": "wrap", "gap": "20px", "margin-bottom": "30px"}
                            ),
                            
                            Text("The framework enables developers to create modern, responsive web applications using an intuitive API and powerful features. With Dars, you can focus on building features rather than dealing with complex configuration.", 
                                style={"font-size": "1.1rem", "color": "#b2ffe5", "line-height": "1.8", "margin-bottom": "30px"}),
                            
                            style={"max-width": "1000px", "margin": "0 auto"}
                        ),
                        style={"padding": "40px", "background-color": "#2a3b2f", "border-radius": "12px", "border-left": "5px solid #00d68f"}
                    ),
                    
                    style={"max-width": "1200px", "margin": "0 auto", "padding": "0 20px"}
                ),
                style={"margin-bottom": "70px"}
            ),
            section_divider(),
            
            # Technology Stack Section
            Container(
                Container(
                    Text("Technology Stack", 
                        style={"font-size": "2.5rem", "font-weight": "bold", "color": "#00d68f", "margin-bottom": "40px", "text-align": "center"}),
                    
                    Container(
                        Container(
                            Container(
                                Text("Core Technologies", 
                                    style={"font-size": "1.4rem", "font-weight": "bold", "color": "#00d68f", "margin-bottom": "25px", "text-align": "center", "border-bottom": "2px solid #00d68f", "padding-bottom": "10px"}),
                                
                                Container(
                                    Container(
                                        Text("Python 3.8+", 
                                            style={"color": "#b2ffe5", "padding": "12px 20px", "background-color": "#304635", "border-radius": "25px", "margin": "8px", "display": "inline-block", "font-weight": "500"}),
                                        Text("HTML5", 
                                            style={"color": "#b2ffe5", "padding": "12px 20px", "background-color": "#304635", "border-radius": "25px", "margin": "8px", "display": "inline-block", "font-weight": "500"}),
                                        Text("CSS3", 
                                            style={"color": "#b2ffe5", "padding": "12px 20px", "background-color": "#304635", "border-radius": "25px", "margin": "8px", "display": "inline-block", "font-weight": "500"}),
                                        Text("JavaScript ES6+", 
                                            style={"color": "#b2ffe5", "padding": "12px 20px", "background-color": "#304635", "border-radius": "25px", "margin": "8px", "display": "inline-block", "font-weight": "500"}),
                                        style={"text-align": "center", "margin-bottom": "20px"}
                                    ),
                                    
                                    Container(
                                        Text("Modern Web Standards", 
                                            style={"color": "#b2ffe5", "padding": "12px 20px", "background-color": "#304635", "border-radius": "25px", "margin": "8px", "display": "inline-block", "font-weight": "500"}),
                                        Text("Component Architecture", 
                                            style={"color": "#b2ffe5", "padding": "12px 20px", "background-color": "#304635", "border-radius": "25px", "margin": "8px", "display": "inline-block", "font-weight": "500"}),
                                        Text("Responsive Design", 
                                            style={"color": "#b2ffe5", "padding": "12px 20px", "background-color": "#304635", "border-radius": "25px", "margin": "8px", "display": "inline-block", "font-weight": "500"}),
                                        style={"text-align": "center"}
                                    ),
                                    
                                    style={"margin-bottom": "30px"}
                                ),
                                
                                style={"flex": "1", "min-width": "300px", "padding": "25px"}
                            ),
                            style={"background-color": "#2a3b2f", "border-radius": "12px", "box-shadow": "0 5px 15px rgba(0,0,0,0.2)"}
                        ),
                        
                        Container(
                            Container(
                                Text("Development Tools", 
                                    style={"font-size": "1.4rem", "font-weight": "bold", "color": "#00d68f", "margin-bottom": "25px", "text-align": "center", "border-bottom": "2px solid #00d68f", "padding-bottom": "10px"}),
                                
                                Container(
                                    Text("• Built-in Development Server", 
                                        style={"color": "#b2ffe5", "margin-bottom": "12px", "font-size": "1.1rem"}),
                                    Text("• Hot Reload Capability", 
                                        style={"color": "#b2ffe5", "margin-bottom": "12px", "font-size": "1.1rem"}),
                                    Text("• CLI Tools for Project Management", 
                                        style={"color": "#b2ffe5", "margin-bottom": "12px", "font-size": "1.1rem"}),
                                    Text("• Export to Multiple Formats", 
                                        style={"color": "#b2ffe5", "margin-bottom": "12px", "font-size": "1.1rem"}),
                                    Text("• Template System", 
                                        style={"color": "#b2ffe5", "margin-bottom": "12px", "font-size": "1.1rem"}),
                                    Text("• PWA Support", 
                                        style={"color": "#b2ffe5", "font-size": "1.1rem"}),
                                    
                                    style={"padding": "0 20px"}
                                ),
                                
                                style={"flex": "1", "min-width": "300px", "padding": "25px"}
                            ),
                            style={"background-color": "#2a3b2f", "border-radius": "12px", "box-shadow": "0 5px 15px rgba(0,0,0,0.2)"}
                        ),
                        
                        style={"display": "flex", "flex-wrap": "wrap", "gap": "30px", "justify-content": "center"}
                    ),
                    
                    style={"max-width": "1000px", "margin": "0 auto"}
                ),
                style={"margin-bottom": "70px", "padding": "0 20px"}
            ),
            section_divider(),
            # Mission Section
            Container(
                Container(
                    Text("Our Vision", 
                        style={"font-size": "2.5rem", "font-weight": "bold", "color": "#00d68f", "margin-bottom": "40px", "text-align": "center"}),
                    
                    Container(
                        Container(
                            Text("Bridging the Gap", 
                                style={"font-size": "1.8rem", "font-weight": "bold", "color": "#00d68f", "margin-bottom": "25px", "text-align": "center"}),
                            
                            Text("Dars Framework was created to bridge the gap between Python's backend capabilities and modern frontend development needs. We believe that Python developers should be able to create full-stack applications without switching between multiple languages and frameworks.", 
                                style={"font-size": "1.1rem", "color": "#b2ffe5", "line-height": "1.8", "margin-bottom": "30px", "text-align": "center"}),
                            
                            Container(
                                Text("""
                                    Our mission is to empower developers with tools that are:
                                    • Intuitive and easy to learn
                                    • Powerful and flexible
                                    • Performant and scalable
                                    • Community-driven and open source
                                """, 
                                style={"color": "#b2ffe5", "line-height": "1.8", "font-size": "1.1rem", "white-space": "pre-line"}),
                                style={"background-color": "#304635", "padding": "25px", "border-radius": "10px", "border-left": "4px solid #00d68f", "max-width": "600px", "margin": "0 auto"}
                            ),
                            
                            style={"text-align": "center", "padding": "40px"}
                        ),
                        style={"background": "linear-gradient(to right, #2a3b2f, #1e2b23)", "border-radius": "15px", "border": "2px solid #00d68f", "box-shadow": "0 10px 30px rgba(0, 0, 0, 0.3)"}
                    ),
                    
                    style={"max-width": "900px", "margin": "0 auto"}
                ),
                style={"margin-bottom": "70px", "padding": "0 20px"}
            ),
            section_divider(),
            # Call to Action Section
            Container(
                Container(
                    Text("Ready to Get Started?", 
                        style={"font-size": "2.2rem", "font-weight": "bold", "color": "#00d68f", "margin-bottom": "25px", "text-align": "center"}),
                    
                    Text("Join the growing community of developers building amazing web applications with Dars Framework", 
                        style={"font-size": "1.2rem", "color": "#b2ffe5", "margin-bottom": "40px", "text-align": "center", "line-height": "1.6"}),
                    
                    Container(
                        Button(
                            text="View Documentation", 
                            on_click=dScript(code="window.open('https://ztamdev.github.io/Dars-Framework/documentation.html#getting-started-with-dars', '_blank');"),
                            style={"background-color": "#00d68f", "color": "#212529", "padding": "15px 30px", "border-radius": "8px", "font-weight": "bold", "border": "none", "cursor": "pointer", "font-size": "1.1rem", "margin": "0 15px"}
                        ),
                        Button(
                            text="Explore GitHub", 
                            on_click=dScript(code="window.open('https://github.com/ZtaMDev/Dars-Framework', '_blank');"),
                            style={"background-color": "transparent", "color": "#00d68f", "padding": "15px 30px", "border-radius": "8px", "font-weight": "bold", "border": "2px solid #00d68f", "cursor": "pointer", "font-size": "1.1rem", "margin": "0 15px"}
                        ),
                        style={"display": "flex", "flex-wrap": "wrap", "justify-content": "center", "gap": "20px"}
                    ),
                    
                    style={"text-align": "center", "padding": "50px", "background": "linear-gradient(to right, #304635, #2a3b2f)", "border-radius": "15px", "box-shadow": "0 10px 30px rgba(0, 0, 0, 0.3)"}
                ),
                style={"max-width": "800px", "margin": "0 auto", "padding": "0 20px", "margin-bottom": "50px"}
            ),
            
            style={"max-width": "1200px", "margin": "0 auto", "padding": "40px 20px"}
        ),
        style={
    "background": """
        linear-gradient(135deg, #212529 0%, #1e2b23 40%, #304635 70%, #00d68f20 100%),
        repeating-radial-gradient(circle at 0 0, #00d68f05, #00d68f05 2px, transparent 2px, transparent 20px)
    """,
    "min-height": "100vh",
    "background-attachment": "fixed",
    }
    ),
    # Footer
    Container(
        Container(
            Text("Created with ", style={"color": "#b2ffe5", "display": "inline", "margin-right": "5px"}),
            Link("Dars Framework", href="https://github.com/ZtaMDev/Dars-Framework", style={"color": "#00d68f", "text-decoration": "none", "font-weight": "bold", "display": "inline"}),
            Text(" • Documentation: ", style={"color": "#b2ffe5", "display": "inline", "margin": "0 5px"}),
            Link("Getting Started", href="https://github.com/ZtaMDev/Dars-Framework/blob/CrystalMain/dars/docs/getting_started.md", style={"color": "#00d68f", "text-decoration": "none", "font-weight": "bold", "display": "inline"}),
            Text(" • Developer: ", style={"color": "#b2ffe5", "display": "inline", "margin": "0 5px"}),
            Link("ZtaDev", href="https://github.com/ZtaMDev", style={"color": "#00d68f", "text-decoration": "none", "font-weight": "bold", "display": "inline"}),
            style={"text-align": "center", "padding": "30px 20px", "border-top": "1px solid #304635"}
        ),
        style={"background-color": "#1e2b23", "margin-top": "auto"}
    ),
    id="about-page",
    style={"background-color": "#212529", "min-height": "100vh", "margin": "0", "font-family": "Arial, sans-serif"}
)


    
downloads = Page(
    FlexLayout(
        children=[create_navbar()],
        wrap="no_wrap",
        justify="flex-start",
        align="center",
        id="navbar-container",
        style={"width": "100%"}
    ),
    Container(
        Container(
            # Hero Section
            Container(
                Container(
                    Text("Download & Installation", 
                        style={"font-size": "3.2rem", "font-weight": "bold", "color": "#00d68f", "text-align": "center", "margin-bottom": "20px", "text-shadow": "0 2px 4px rgba(0,0,0,0.5)"}),
                    Text("Get started with Dars Framework in just a few steps", 
                        style={"font-size": "1.4rem", "color": "#b2ffe5", "text-align": "center", "line-height": "1.5"}),
                    style={
                        "padding": "70px 20px", 
                        "text-align": "center",
                        "display": "flex",
                        "flex-direction": "column",
                        "justify-content": "center",
                        "min-height": "400px"
                    }
                ),
                style={
                    "background": "linear-gradient(rgba(33, 37, 41, 0.9), rgba(48, 70, 53, 0.9)), url('Dars-logo.png') center/cover",
                    "border-radius": "15px",
                    "margin-bottom": "60px",
                    "box-shadow": "0 10px 30px rgba(0, 0, 0, 0.3)",
                    "display": "flex",
                    "flex-direction": "column",
                    "justify-content": "space-between"
                }
            ),
            
            # Installation Section
            Container(
                Text("Installation", 
                    style={"font-size": "2.5rem", "font-weight": "bold", "color": "#00d68f", "margin-bottom": "40px", "text-align": "center"}),
                
                Container(
                    Text("Install Dars Framework with a single command:", 
                        style={"font-size": "1.3rem", "color": "#b2ffe5", "margin-bottom": "30px", "text-align": "center"}),
                    
                    # Comando instalación con botón copiar
                    Container(
                        Container(
                            Container(
                                Text("pip install dars-framework", 
                                    style={"font-family": "monospace", "font-size": "1.2rem", "color": "#00d68f", "padding": "18px", "background-color": "#1e2b23", "border-radius": "8px", "flex": "1", "border": "1px solid #00d68f"}),
                                Button(
                                    text="Copy", 
                                    on_click=dScript(code="""
                                        navigator.clipboard.writeText('pip install dars-framework')
                                        .then(() => alert('Command copied to clipboard!'))
                                        .catch(err => console.error('Failed to copy: ', err));
                                    """),
                                    style={"background-color": "#00d68f", "color": "#212529", "padding": "18px 25px", "border-radius": "8px", "border": "none", "cursor": "pointer", "font-weight": "bold", "margin-left": "15px", "font-size": "1.1rem"}
                                ),
                                style={"display": "flex", "align-items": "center", "justify-content": "center", "max-width": "550px", "margin": "0 auto", "flex-wrap": "wrap", "gap": "15px"}
                            ),
                            style={"margin-bottom": "25px"}
                        ),
                        
                        # Enlace a Releases
                        Container(
                            Text("Looking for specific versions or release notes?", 
                                style={"color": "#b2ffe5", "margin-bottom": "15px", "text-align": "center", "font-style": "italic", "font-size": "1.1rem"}),
                            Link("View all releases on GitHub →", 
                                href="https://github.com/ZtaMDev/Dars-Framework/releases", 
                                style={"color": "#00d68f", "text-decoration": "none", "font-weight": "bold", "display": "inline-block", "padding": "12px 20px", "border": "2px solid #00d68f", "border-radius": "6px", "font-size": "1.1rem"}),
                            style={"text-align": "center", "margin-bottom": "30px"}
                        ),
                        
                        Text("Once installed, you're ready to start building your first Dars application!", 
                            style={"color": "#b2ffe5", "text-align": "center", "line-height": "1.6", "font-size": "1.1rem"}),
                        
                        style={"background-color": "#2a3b2f", "padding": "50px 40px", "border-radius": "12px", "margin-bottom": "60px", "text-align": "center", "border": "2px solid #304635"}
                    )
                )
            ),
            section_divider(),
            # CLI Commands Section
            Container(
                Text("Essential CLI Commands", 
                    style={"font-size": "2.5rem", "font-weight": "bold", "color": "#00d68f", "margin-bottom": "50px", "text-align": "center"}),
                
                Container(
                    Container(
                        # Command 1
                        Container(
                            Container(
                                Text("dars init my_project", 
                                    style={"font-family": "monospace", "font-size": "1.1rem", "color": "#00d68f", "padding": "15px", "background-color": "#1e2b23", "border-radius": "6px", "margin-bottom": "15px", "border": "1px solid #00d68f"}),
                                Text("Create a new Dars project", 
                                    style={"color": "#b2ffe5", "font-size": "1rem", "text-align": "center"}),
                                style={"text-align": "center", "padding": "10px"}
                            ),
                            style={"background": "linear-gradient(145deg, #2a3b2f, #304635)", "padding": "25px", "border-radius": "10px", "flex": "1", "min-width": "280px", "box-shadow": "0 5px 15px rgba(0,0,0,0.2)"}
                        ),
                        
                        # Command 2
                        Container(
                            Container(
                                Text("dars export main.py --format html", 
                                    style={"font-family": "monospace", "font-size": "1.1rem", "color": "#00d68f", "padding": "15px", "background-color": "#1e2b23", "border-radius": "6px", "margin-bottom": "15px", "border": "1px solid #00d68f"}),
                                Text("Export app to HTML/CSS/JS", 
                                    style={"color": "#b2ffe5", "font-size": "1rem", "text-align": "center"}),
                                style={"text-align": "center", "padding": "10px"}
                            ),
                            style={"background": "linear-gradient(145deg, #2a3b2f, #304635)", "padding": "25px", "border-radius": "10px", "flex": "1", "min-width": "280px", "box-shadow": "0 5px 15px rgba(0,0,0,0.2)"}
                        ),
                        
                        # Command 3
                        Container(
                            Container(
                                Text("dars preview ./output", 
                                    style={"font-family": "monospace", "font-size": "1.1rem", "color": "#00d68f", "padding": "15px", "background-color": "#1e2b23", "border-radius": "6px", "margin-bottom": "15px", "border": "1px solid #00d68f"}),
                                Text("Preview exported app locally", 
                                    style={"color": "#b2ffe5", "font-size": "1rem", "text-align": "center"}),
                                style={"text-align": "center", "padding": "10px"}
                            ),
                            style={"background": "linear-gradient(145deg, #2a3b2f, #304635)", "padding": "25px", "border-radius": "10px", "flex": "1", "min-width": "280px", "box-shadow": "0 5px 15px rgba(0,0,0,0.2)"}
                        ),
                        
                        # Command 4
                        Container(
                            Container(
                                Text("dars info main.py", 
                                    style={"font-family": "monospace", "font-size": "1.1rem", "color": "#00d68f", "padding": "15px", "background-color": "#1e2b23", "border-radius": "6px", "margin-bottom": "15px", "border": "1px solid #00d68f"}),
                                Text("Show info about your app", 
                                    style={"color": "#b2ffe5", "font-size": "1rem", "text-align": "center"}),
                                style={"text-align": "center", "padding": "10px"}
                            ),
                            style={"background": "linear-gradient(145deg, #2a3b2f, #304635)", "padding": "25px", "border-radius": "10px", "flex": "1", "min-width": "280px", "box-shadow": "0 5px 15px rgba(0,0,0,0.2)"}
                        ),
                        
                        style={"display": "flex", "flex-wrap": "wrap", "gap": "25px", "justify-content": "center", "margin-bottom": "50px"}
                    ),
                    
                    section_divider(),
                    
                    # Templates Section
                    Container(
                        Text("Using Templates", 
                            style={"font-size": "1.8rem", "font-weight": "bold", "color": "#00d68f", "margin-bottom": "25px", "text-align": "center"}),
                        
                        Container(
                            Container(
                                Text("dars init my_project -t basic/hello_world", 
                                    style={"font-family": "monospace", "font-size": "1rem", "color": "#00d68f", "padding": "15px", "background-color": "#1e2b23", "border-radius": "6px", "margin-bottom": "15px", "border": "1px solid #00d68f"}),
                                Text("Start with a template for faster development", 
                                    style={"color": "#b2ffe5", "font-size": "1rem", "text-align": "center"}),
                                style={"text-align": "center", "padding": "20px"}
                            ),
                            style={"background-color": "#2a3b2f", "padding": "30px", "border-radius": "10px", "max-width": "500px", "margin": "0 auto", "border": "2px solid #304635"}
                        ),
                        
                        style={"margin-bottom": "50px"}
                    ),
                    
                    # Help Command
                    Container(
                        Container(
                            Text("Need help? Use:", 
                                style={"color": "#b2ffe5", "margin-bottom": "20px", "text-align": "center", "font-size": "1.2rem"}),
                            Container(
                                Text("dars --help", 
                                    style={"font-family": "monospace", "font-size": "1.1rem", "color": "#00d68f", "padding": "15px", "background-color": "#1e2b23", "border-radius": "6px", "border": "1px solid #00d68f"}),
                                style={"text-align": "center"}
                            ),
                            style={"text-align": "center", "padding": "25px"}
                        ),
                        style={"background-color": "#1e2b23", "padding": "35px", "border-radius": "12px", "border": "2px solid #00d68f", "max-width": "400px", "margin": "0 auto"}
                    ),
                    
                    style={"max-width": "1000px", "margin": "0 auto"}
                ),
                style={"margin-bottom": "60px"}
            ),
            
            section_divider(),
            # Documentation Section
            Container(
                Container(
                    Text("Complete Documentation", 
                        style={"font-size": "2.2rem", "font-weight": "bold", "color": "#00d68f", "margin-bottom": "30px", "text-align": "center"}),
                    
                    Text("Explore all available commands, options, and advanced usage in our comprehensive documentation", 
                        style={"color": "#b2ffe5", "margin-bottom": "40px", "text-align": "center", "line-height": "1.6", "font-size": "1.1rem"}),
                    
                    Container(
                        Link("View Full CLI Documentation →", 
                            href="https://ztamdev.github.io/Dars-Framework/documentation.html#dars-cli-reference", 
                            style={"background-color": "#00d68f", "color": "#212529", "padding": "18px 35px", "border-radius": "8px", "text-decoration": "none", "font-weight": "bold", "display": "inline-block", "font-size": "1.1rem", "border": "2px solid #00d68f"}),
                        style={"text-align": "center", "margin-bottom": "20px"}
                    ),
                    
                    Container(
                        Link("Browse All Documentation →", 
                            href="https://ztamdev.github.io/Dars-Framework/documentation.html", 
                            style={"color": "#00d68f", "text-decoration": "none", "font-weight": "bold", "display": "inline-block", "padding": "15px 25px", "border": "2px solid #00d68f", "border-radius": "6px", "font-size": "1rem"}),
                        style={"text-align": "center"}
                    ),
                    
                    style={"padding": "50px", "background": "linear-gradient(to right, #2a3b2f, #1e2b23)", "border-radius": "12px", "text-align": "center", "border": "2px solid #304635", "box-shadow": "0 10px 30px rgba(0, 0, 0, 0.3)"}
                ),
                style={"margin-bottom": "50px", "max-width": "800px", "margin": "0 auto"}
            ),
            section_divider(),
            # Getting Started CTA
            Container(
                Container(
                    Text("Ready to Start Building?", 
                        style={"font-size": "2rem", "font-weight": "bold", "color": "#00d68f", "margin-bottom": "25px", "text-align": "center"}),
                    
                    Container(
                        Button(
                            text="Get Started Guide", 
                            on_click=dScript(code="window.location.href = 'https://ztamdev.github.io/Dars-Framework/documentation.html#getting-started-with-dars';"),
                            style={"background-color": "#00d68f", "color": "#212529", "padding": "16px 32px", "border-radius": "8px", "text-decoration": "none", "font-weight": "bold", "border": "none", "cursor": "pointer", "font-size": "1.1rem", "margin": "0 10px"}
                        ),
                        Button(
                            text="View Examples", 
                            on_click=dScript(code="window.open('https://github.com/ZtaMDev/Dars-Framework/tree/CrystalMain/dars/templates/examples', '_blank');"),
                            style={"background-color": "transparent", "color": "#00d68f", "padding": "16px 32px", "border-radius": "8px", "text-decoration": "none", "font-weight": "bold", "border": "2px solid #00d68f", "cursor": "pointer", "font-size": "1.1rem", "margin": "0 10px"}
                        ),
                        style={"display": "flex", "flex-wrap": "wrap", "justify-content": "center", "gap": "20px"}
                    ),
                    
                    style={"text-align": "center", "padding": "50px", "background-color": "#304635", "border-radius": "12px", "border": "2px solid #00d68f"}
                ),
                style={"max-width": "700px", "margin": "0 auto", "padding": "0 20px"}
            ),
            
            style={"max-width": "1200px", "margin": "0 auto", "padding": "40px 20px"}
        ),
        style={
            "background": """
                linear-gradient(135deg, #212529 0%, #1e2b23 40%, #304635 70%, #00d68f20 100%),
                repeating-radial-gradient(circle at 0 0, #00d68f05, #00d68f05 2px, transparent 2px, transparent 20px)
            """,
            "min-height": "100vh",
            "background-attachment": "fixed",
        }
    ),
    # Footer
    Container(
        Container(
            Text("Created with ", style={"color": "#b2ffe5", "display": "inline", "margin-right": "5px"}),
            Link("Dars Framework", href="https://github.com/ZtaMDev/Dars-Framework", style={"color": "#00d68f", "text-decoration": "none", "font-weight": "bold", "display": "inline"}),
            Text(" • Documentation: ", style={"color": "#b2ffe5", "display": "inline", "margin": "0 5px"}),
            Link("Getting Started", href="https://ztamdev.github.io/Dars-Framework/documentation.html", style={"color": "#00d68f", "text-decoration": "none", "font-weight": "bold", "display": "inline"}),
            Text(" • Developer: ", style={"color": "#b2ffe5", "display": "inline", "margin": "0 5px"}),
            Link("ZtaDev", href="https://github.com/ZtaMDev", style={"color": "#00d68f", "text-decoration": "none", "font-weight": "bold", "display": "inline"}),
            style={"text-align": "center", "padding": "30px 20px", "border-top": "1px solid #304635"}
        ),
        style={"background-color": "#1e2b23", "margin-top": "auto"}
    ),
    id="downloads-page",
    style={
    "background": """
        linear-gradient(135deg, #212529 0%, #1e2b23 40%, #304635 70%, #00d68f20 100%),
        repeating-radial-gradient(circle at 0 0, #00d68f05, #00d68f05 2px, transparent 2px, transparent 20px)
    """,
    "min-height": "100vh",
    "background-attachment": "fixed",  # Para que el patrón se quede fijo al hacer scroll
    }
)


# Estilos para los links del menú flotante
FLOATING_LINK_STYLE = {
    "display": "block",
    "color": "#00d68f",
    "text-decoration": "none",
    "margin-bottom": "10px",
    "font-weight": "bold"
}

# Botón flotante en la esquina inferior derecha
sidebar = Container(
    # Botón flotante
    Button(
        text="☰ Contents",
        on_click=dScript(code="""
            const sidebar = document.getElementById('sidebar-links');
            if (sidebar.style.display === 'none' || sidebar.style.display === '') {
                sidebar.style.display = 'block';
            } else {
                sidebar.style.display = 'none';
            }
        """),
        style={
            "background-color": "#00d68f",
            "color": "#212529",
            "border": "none",
            "padding": "12px 16px",
            "border-radius": "5px",
            "cursor": "pointer",
            "font-weight": "bold",
            "position": "fixed",
            "bottom": "20px",
            "right": "20px",
            "z-index": "1000"
        }
    ),
    # Contenedor de links oculto
    Container(
        Link("Home", href="#dars-framework-documentation", style=FLOATING_LINK_STYLE),
        Link("Getting started", href="#getting-started-with-dars", style=FLOATING_LINK_STYLE),
        Link("App", href="#app-class-and-pwa-features-in-dars-framework", style=FLOATING_LINK_STYLE),
        Link("State Management", href="#state-management-in-dars-dstate-cstate-goto-mods", style=FLOATING_LINK_STYLE),
        Link("Installing", href="#installation-guide-dars-framework", style=FLOATING_LINK_STYLE),
        Link("Components", href="#dars-components-documentation", style=FLOATING_LINK_STYLE),
        Link("Custom Components", href="#custom-components-in-dars-framework", style=FLOATING_LINK_STYLE),
        Link("Events", href="#events-in-dars", style=FLOATING_LINK_STYLE),
        Link("Exporter", href="#dars-exporter-documentation", style=FLOATING_LINK_STYLE),
        Link("Scripts", href="#dars-script-system", style=FLOATING_LINK_STYLE),
        Link("Dars CLI", href="#dars-cli-reference", style=FLOATING_LINK_STYLE),
        id="sidebar-links",
        style={
            "display": "none",
            "position": "fixed",
            "bottom": "70px",  # aparece encima del botón
            "right": "20px",
            "background-color": "#1e2b23",
            "padding": "15px",
            "border-radius": "8px",
            "border": "2px solid #00d68f",
            "z-index": "999",
            "box-shadow": "0 4px 12px rgba(0,0,0,0.3)"
        }
    ),
    id="sidebar-floating"
)

app.add_global_style(
    selector="""
.lazy-hidden {
    opacity: 0;
    display: none;
    transform: translateY(20px);
    transition: opacity 0.6s ease, transform 0.6s ease;
}
.lazy-visible {
    opacity: 1;
    transform: translateY(0);
}
""",
    styles={"": ""}
)

app.add_script(dScript(code="""
document.addEventListener('DOMContentLoaded', () => {
    // Selecciona todos los bloques Markdown sin tocar su id
    const markdownBlocks = document.querySelectorAll('.markdown-docs');

    markdownBlocks.forEach(block => {
        block.classList.add('lazy-hidden'); // Oculto al inicio
    });

    const observerOptions = {
        root: null,
        rootMargin: '300px',
        threshold: 0.1
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if(entry.isIntersecting){
                entry.target.classList.add('lazy-visible');
                entry.target.classList.remove('lazy-hidden');
            } else {
                entry.target.classList.remove('lazy-visible');
                entry.target.classList.add('lazy-hidden');
            }
        });
    }, observerOptions);

    markdownBlocks.forEach(block => observer.observe(block));
});
"""))


documentation = Page(
    FlexLayout(
        children=[create_navbar()],
        wrap="no_wrap",
        justify="flex-start",
        align="center",
        id="navbar-container",
        style={"width": "100%"}
    ),
    Markdown(
        file_path="index.md",
        style={"class": "markdown-docs"},
        id="markdown_docs"
    ),
    Markdown(
        file_path="INSTALL.md",
        style={"class": "markdown-docs"},
        id="markdown_docs"
    ),
    Markdown(
        file_path="getting_started.md",
        style={"class": "markdown-docs"},
        id="markdown_docs"
    ),
    Markdown(
        file_path="config.md", 
        style={"class": "markdown-docs"}, 
        id="markdown_docs"
    ),
    Markdown(
        file_path="app.md",
        style={"class": "markdown-docs"},
        id="markdown_docs"
    ),
    Markdown(
        file_path="state_management.md",
        style={"class": "markdown-docs"},
        id="markdown_docs"
    ),
    Markdown(
        file_path="components.md",
        style={"class": "markdown-docs"},
        id="markdown_docs"
    ),
    
    Markdown(
        file_path="custom_components.md",
        style={"class": "markdown-docs"},
        id="markdown_docs"
    ),
    Markdown(
        file_path="events.md",
        style={"class": "markdown-docs"},
        id="markdown_docs"
    ),
    Markdown(
        file_path="exporters.md",
        style={"class": "markdown-docs"},
        id="markdown_docs"
    ),
    Markdown(
        file_path="scripts.md",
        style={"class": "markdown-docs"},
        id="markdown_docs"
    ),
    Markdown(
        file_path="cli.md",
        style={"class": "markdown-docs"},
        id="markdown_docs"
    ),
    sidebar,
    # Footer
    Container(
        Container(
            Text("Created with ", style={"color": "#b2ffe5", "display": "inline", "margin-right": "5px"}),
            Link("Dars Framework", href="https://github.com/ZtaMDev/Dars-Framework", style={"color": "#00d68f", "text-decoration": "none", "font-weight": "bold", "display": "inline"}),
            Text(" • Documentation: ", style={"color": "#b2ffe5", "display": "inline", "margin": "0 5px"}),
            Link("Getting Started", href="https://github.com/ZtaMDev/Dars-Framework/blob/CrystalMain/dars/docs/getting_started.md", style={"color": "#00d68f", "text-decoration": "none", "font-weight": "bold", "display": "inline"}),
            Text(" • Developer: ", style={"color": "#b2ffe5", "display": "inline", "margin": "0 5px"}),
            Link("ZtaDev", href="https://github.com/ZtaMDev", style={"color": "#00d68f", "text-decoration": "none", "font-weight": "bold", "display": "inline"}),
            style={"text-align": "center", "padding": "30px 20px", "border-top": "1px solid #304635"}
        ),
        style={"background-color": "#1e2b23", "margin-top": "auto"}
    ),
    style={
    "background": """
        linear-gradient(135deg, #212529 0%, #1e2b23 40%, #304635 70%, #00d68f20 100%),
        repeating-radial-gradient(circle at 0 0, #00d68f05, #00d68f05 2px, transparent 2px, transparent 20px)
    """,
    "min-height": "100vh",
    "background-attachment": "fixed",  # Para que el patrón se quede fijo al hacer scroll
    }

    
)


# Botones - animación suave
app.add_global_style(
    selector="button, .btn",
    styles={
        "transition": "all 0.3s ease",
    }
)

app.add_global_style(
    selector="button:hover, .btn:hover",
    styles={
        "transform": "translateY(-3px) scale(1.05)",
        "box-shadow": "0 6px 14px rgba(0,0,0,0.25)",
    }
)

app.add_global_style(
    selector="button:active, .btn:active",
    styles={
        "transform": "translateY(0) scale(0.97)",
        "box-shadow": "0 3px 8px rgba(0,0,0,0.2)",
    }
)

# Inputs y campos de texto - animación de foco
app.add_global_style(
    selector="input, textarea, select",
    styles={
        "transition": "all 0.3s ease",
    }
)

app.add_global_style(
    selector="input:focus, textarea:focus, select:focus",
    styles={
        "transform": "scale(1.01)",
        "box-shadow": "0 0 8px rgba(0,0,0,0.2)",
    }
)

# Links generales - animación hover
app.add_global_style(
    selector="a",
    styles={
        "transition": "all 0.3s ease",
    }
)

app.add_global_style(
    selector="a:hover",
    styles={
        "transform": "translateY(-1px)",
        "text-shadow": "0 2px 6px rgba(0,0,0,0.3)",
    }
)

app.set_theme("dark")
app.add_page(name="index", root=index, title="Dars Framework", index=True)
app.add_page(name="about", root=about, title="About")
app.add_page(name="downloads", root=downloads, title="Downloads")
app.add_page(name="documentation", root=documentation, title="Dars-Documentation")

#Script
app.add_script(dScript(code=mobile_detection_script))

app.add_script(dScript(code="console.log('Dars framework version: 1.2.2 running...')"))
if __name__ == "__main__":
    app.rTimeCompile(add_file_types=".js, .md, .css")