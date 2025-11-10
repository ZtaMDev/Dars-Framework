from dars.all import *

def create_navbar():
    left_block = Container(
        Image(
            alt="Logo",
            src="Dars-logo.png",
            width="38px",
            height="38px",
            style={
                "object-fit": "contain",
                "margin-right": "10px"
            }
        ),
        Text(
            text="Dars Framework",
            style={
                "font-size": "20px",
                "font-weight": "700",
                "color": "#a2ffe2",
                "margin": "0"
            }
        ),
        id="navbar-left",
        style={
            "display": "flex",
            "align-items": "center",
            "justify-content": "flex-start",
            "height": "100%"
        }
    )

    # Botones para la parte derecha del navbar
    right_block = Container(
        Link(
            "Home",
            href="/",
            style={
                "color": "#a0cfc0",
                "text-decoration": "none",
                "margin": "0 15px",
                "font-weight": "500",
                "font-size": "16px",
                "transition": "all 0.3s ease",
                "padding": "8px 16px",
                "border-radius": "6px"
            }
        ),
        Link(
            "Documentation",
            href="/docs.html",
            style={
                "color": "#a0cfc0",
                "text-decoration": "none",
                "margin": "0 15px",
                "font-weight": "500",
                "font-size": "16px",
                "transition": "all 0.3s ease",
                "padding": "8px 16px",
                "border-radius": "6px"
            }
        ),
        Link(
            "Releases",
            href="/releases.html",
            style={
                "color": "#a0cfc0",
                "text-decoration": "none",
                "margin": "0 15px",
                "font-weight": "500",
                "font-size": "16px",
                "transition": "all 0.3s ease",
                "padding": "8px 16px",
                "border-radius": "6px"
            }
        ),
        Link(
            "PlayGround",
            href="https://dars-playground.vercel.app/",
            style={
                "color": "#a0cfc0",
                "text-decoration": "none",
                "margin": "0 15px",
                "font-weight": "500",
                "font-size": "16px",
                "transition": "all 0.3s ease",
                "padding": "8px 16px",
                "border-radius": "6px"
            }
        ),
        Link(
            "GitHub",
            href="https://github.com/ZtaMDev/Dars-Framework",
            style={
                "color": "#a0cfc0",
                "text-decoration": "none",
                "margin": "0 15px",
                "font-weight": "500",
                "font-size": "16px",
                "transition": "all 0.3s ease",
                "padding": "8px 16px",
                "border-radius": "6px"
            }
        ),
        id="navbar-right",
        style={
            "display": "flex",
            "align-items": "center",
            "justify-content": "flex-end",
            "height": "100%"
        }
    )

    return Navbar(
        left_block,
        right_block,
        id="dars-navbar",
        style={
            "display": "flex",
            "align-items": "center",
            "justify-content": "space-between",
            "height": "64px",
            "padding": "0 40px",
            "position": "fixed",
            "top": "0",
            "width": "100%",
            "z-index": "999",
            "backdrop-filter": "blur(12px)",
            "background": "rgba(20, 30, 27, 0.6)",
            "border-bottom": "1px solid rgba(100,255,200,0.1)",
            "box-shadow": "0 2px 10px rgba(0,0,0,0.2)"
        }
    )