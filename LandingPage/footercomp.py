from dars.all import *
from dars.env import DarsEnv
def create_footer():
    return Container(
        Container(
            # Primera fila: Logo y descripción
            Container(
                Container(
                    Image(
                        src="Dars-logo.png",
                        alt="Dars Framework",
                        width="50px",
                        height="50px",
                        style={
                            "margin-right": "15px",
                            "filter": "drop-shadow(0 0 10px rgba(162, 255, 226, 0.4))"
                        }
                    ),
                    Container(
                        Text(
                            "Dars Framework",
                            style={
                                "font-size": "24px",
                                "font-weight": "700",
                                "color": "#a2ffe2",
                                "margin-bottom": "5px"
                            }
                        ),
                        style={"text-align": "left"}
                    ),
                    style={
                        "display": "flex",
                        "align-items": "center",
                        "margin-bottom": "30px"
                    }
                ),
                # Segunda fila: Enlaces y información
                Container(
                    Container(
                        Text(
                            "Quick Links",
                            style={
                                "font-size": "18px",
                                "font-weight": "600",
                                "color": "#a2ffe2",
                                "margin-bottom": "15px"
                            }
                        ),
                        Link(
                            "Documentation",
                            href="/docs.html" if DarsEnv.dev else "https://ztamdev.github.io/Dars-Framework/docs.html",
                            style={
                                "color": "#a0cfc0",
                                "text-decoration": "none",
                                "display": "block",
                                "margin-bottom": "8px",
                                "transition": "all 0.3s ease",
                                "font-size": "14px"
                            }
                        ),
                        Link(
                            "GitHub",
                            href="https://github.com/ZtaMDev/Dars-Framework",
                            style={
                                "color": "#a0cfc0",
                                "text-decoration": "none",
                                "display": "block",
                                "margin-bottom": "8px",
                                "transition": "all 0.3s ease",
                                "font-size": "14px"
                            }
                        ),
                        Link(
                            "Examples",
                            href="https://github.com/ZtaMDev/Dars-Framework/tree/CrystalMain/dars/templates/examples",
                            style={
                                "color": "#a0cfc0",
                                "text-decoration": "none",
                                "display": "block",
                                "margin-bottom": "8px",
                                "transition": "all 0.3s ease",
                                "font-size": "14px"
                            }
                        ),
                        style={"flex": "1", "min-width": "150px"}
                    ),
                    # Columna de recursos
                    Container(
                        Text(
                            "Resources",
                            style={
                                "font-size": "18px",
                                "font-weight": "600",
                                "color": "#a2ffe2",
                                "margin-bottom": "15px"
                            }
                        ),

                        Link(
                            "Getting Started",
                            href="/docs.html" if DarsEnv.dev else "https://ztamdev.github.io/Dars-Framework/docs.html",
                            style={
                                "color": "#a0cfc0",
                                "text-decoration": "none",
                                "display": "block",
                                "margin-bottom": "8px",
                                "transition": "all 0.3s ease",
                                "font-size": "14px"
                            }
                        ),

                        Link(
                            "Releases",
                            href="/releases.html" if DarsEnv.dev else "https://github.com/ZtaMDev/Dars-Framework/releases.html",
                            style={
                                "color": "#a0cfc0",
                                "text-decoration": "none",
                                "display": "block",
                                "margin-bottom": "8px",
                                "transition": "all 0.3s ease",
                                "font-size": "14px"
                            }
                        ),
                        style={"flex": "1", "min-width": "150px"}
                    ),
                    # Columna de información
                    Container(

                        Text(
                            "A modern FullStack Python framework for web and desktop applications.",
                            style={
                                "color": "#a0cfc0",
                                "font-size": "14px",
                                "line-height": "1.5",
                                "margin-bottom": "15px"
                            }
                        ),
                        style={
                            "display": "flex",
                            "flex-direction": "column",
                            "align-items": "center",
                            "min-width": "200px"
                        }
                    ),
                    style={
                        "display": "flex",
                        "flex-wrap": "wrap",
                        "gap": "40px",
                        "justify-content": "space-between",
                        "margin-bottom": "30px"
                    }
                ),
                # Tercera fila: Copyright y créditos
                Container(
                    Container(
                        Text(
                            "© 2025 Dars Framework.",
                            style={
                                "color": "#a0cfc0",
                                "font-size": "14px",
                                "opacity": "0.7"
                            }
                        ),
                        style={"flex": "1"}
                    ),
                    Container(
                        Text(
                            "Created with ",
                            style={
                                "color": "#a0cfc0",
                                "font-size": "14px",
                                "opacity": "0.7",
                                "display": "inline"
                            }
                        ),
                        Link(
                            "Dars Framework",
                            href="/" if DarsEnv.dev else "https://github.com/ZtaMDev/Dars-Framework",
                            style={
                                "color": "#a2ffe2",
                                "text-decoration": "none",
                                "font-weight": "600",
                                "display": "inline",
                                "font-size": "14px"
                            }
                        ),
                        Text(
                            " by ",
                            style={
                                "color": "#a0cfc0",
                                "font-size": "14px",
                                "opacity": "0.7",
                                "display": "inline"
                            }
                        ),
                        Link(
                            "ZtaDev",
                            href="https://github.com/ZtaMDev",
                            style={
                                "color": "#a2ffe2",
                                "text-decoration": "none",
                                "font-weight": "600",
                                "display": "inline",
                                "font-size": "14px"
                            }
                        ),
                        style={"flex": "1", "text-align": "right"}
                    ),
                    style={
                        "display": "flex",
                        "flex-wrap": "wrap",
                        "justify-content": "space-between",
                        "align-items": "center",
                        "padding-top": "20px",
                        "border-top": "1px solid rgba(100,255,200,0.1)"
                    }
                ),
                style={
                    "max-width": "1200px",
                    "margin": "0 auto",
                    "padding": "50px 20px"
                }
            ),
            style={
                "background": "rgba(10, 15, 13, 0.8)",
                "backdrop-filter": "blur(12px)",
                "border-top": "1px solid rgba(100,255,200,0.15)"
            }
        ),
        id="footer-section",
        style={
            "background": "linear-gradient(135deg, #0a1512 0%, #0f1e1a 100%)",
            "margin-top": "auto"
        }
    )