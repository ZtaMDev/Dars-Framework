# Dars Framework - Core Source File
#
# This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0.
# If a copy of the MPL was not distributed with this file, You can obtain one at
# https://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2025 ZtaDev
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

    # Botones para la parte derecha del navbar (desktop)
    right_block = Container(
        Link(
            "Home",
            href="https://ztamdev.github.io/Dars-Framework/",
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
            href="https://ztamdev.github.io/Dars-Framework/docs.html",
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
            href="https://ztamdev.github.io/Dars-Framework/releases.html",
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

    # Menú hamburguesa mejorado para móviles
    hamburger_menu = Container(
        # Botón hamburguesa mejorado
        Container(
            Container(
                Container(style={
                    "width": "24px", 
                    "height": "2px", 
                    "background": "#a2ffe2", 
                    "border-radius": "2px",
                    "transition": "all 0.3s ease",
                    "margin": "3px 0"
                }),
                Container(style={
                    "width": "24px", 
                    "height": "2px", 
                    "background": "#a2ffe2", 
                    "border-radius": "2px",
                    "transition": "all 0.3s ease",
                    "margin": "3px 0"
                }),
                Container(style={
                    "width": "18px", 
                    "height": "2px", 
                    "background": "#a2ffe2", 
                    "border-radius": "2px",
                    "transition": "all 0.3s ease",
                    "margin": "3px 0"
                }),
                style={
                    "display": "flex",
                    "flex-direction": "column",
                    "align-items": "center",
                    "justify-content": "center",
                    "width": "44px",
                    "height": "44px",
                    "position": "relative"
                }
            ),
            id="hamburger-btn",
            style={
                "display": "none",
                "background": "rgba(162, 255, 226, 0.1)",
                "border": "1px solid rgba(162, 255, 226, 0.3)",
                "border-radius": "10px",
                "cursor": "pointer",
                "padding": "0",
                "z-index": "1000",
                "transition": "all 0.3s ease",
                "align-items": "center",
                "justify-content": "center",
                "backdrop-filter": "blur(10px)",
                "box-shadow": "0 4px 15px rgba(0,0,0,0.2)"
            }
        ),
        
        # Menú desplegable
        Container(
            Link(
                "Home",
                href="https://ztamdev.github.io/Dars-Framework/",
                style={
                    "color": "#a0cfc0",
                    "text-decoration": "none",
                    "display": "block",
                    "padding": "18px 25px",
                    "font-weight": "500",
                    "font-size": "18px",
                    "transition": "all 0.3s ease",
                    "border-bottom": "1px solid rgba(100,255,200,0.1)"
                }
            ),
            Link(
                "Documentation",
                href="https://ztamdev.github.io/Dars-Framework/docs.html",
                style={
                    "color": "#a0cfc0",
                    "text-decoration": "none",
                    "display": "block",
                    "padding": "18px 25px",
                    "font-weight": "500",
                    "font-size": "18px",
                    "transition": "all 0.3s ease",
                    "border-bottom": "1px solid rgba(100,255,200,0.1)"
                }
            ),
            Link(
                "Releases",
                href="https://ztamdev.github.io/Dars-Framework/releases.html",
                style={
                    "color": "#a0cfc0",
                    "text-decoration": "none",
                    "display": "block",
                    "padding": "18px 25px",
                    "font-weight": "500",
                    "font-size": "18px",
                    "transition": "all 0.3s ease",
                    "border-bottom": "1px solid rgba(100,255,200,0.1)"
                }
            ),
            Link(
                "PlayGround",
                href="https://dars-playground.vercel.app/",
                style={
                    "color": "#a0cfc0",
                    "text-decoration": "none",
                    "display": "block",
                    "padding": "18px 25px",
                    "font-weight": "500",
                    "font-size": "18px",
                    "transition": "all 0.3s ease",
                    "border-bottom": "1px solid rgba(100,255,200,0.1)"
                }
            ),
            Link(
                "GitHub",
                href="https://github.com/ZtaMDev/Dars-Framework",
                style={
                    "color": "#a0cfc0",
                    "text-decoration": "none",
                    "display": "block",
                    "padding": "18px 25px",
                    "font-weight": "500",
                    "font-size": "18px",
                    "transition": "all 0.3s ease"
                }
            ),
            id="mobile-menu",
            style={
                "display": "none",
                "position": "fixed",
                "top": "64px",
                "left": "0",
                "width": "100%",
                "background": "rgba(15, 25, 22, 0.98)",
                "backdrop-filter": "blur(25px)",
                "border-top": "1px solid rgba(100,255,200,0.15)",
                "box-shadow": "0 8px 30px rgba(0,0,0,0.4)",
                "z-index": "999",
                "flex-direction": "column"
            }
        ),
        id="hamburger-menu",
        style={
            "display": "none",
            "align-items": "center",
            "justify-content": "flex-end",
            "height": "100%"
        }
    )

    return Container(
        Navbar(
            left_block,
            Container(
                right_block,
                hamburger_menu,
                style={
                    "display": "flex",
                    "align-items": "center",
                    "justify-content": "flex-end",
                    "height": "100%",
                    "gap": "15px"
                }
            ),
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
        ),
    )