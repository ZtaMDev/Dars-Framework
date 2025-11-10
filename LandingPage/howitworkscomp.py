from dars.all import *

def create_howitworks():
    return Container(
        Text(
            "How It Works",
            style={
                "font-size": "48px",
                "font-weight": "800",
                "text-align": "center",
                "margin-bottom": "20px",
                "background": "linear-gradient(90deg, #92ffe5, #38c49f, #7dfdd8, #92ffe5)",
                "background-size": "300% 300%",
                "background-clip": "text",
                "-webkit-background-clip": "text",
                "color": "transparent",
                "animation": "colorCycle 6s ease-in-out infinite alternate"
            }
        ),
        Text(
            "Get started with Dars in three simple steps",
            style={
                "font-size": "20px",
                "color": "#a0cfc0",
                "text-align": "center",
                "margin-bottom": "40px",  # Reducido de 60px a 40px
                "max-width": "600px",
                "margin-left": "auto",
                "margin-right": "auto"
            }
        ),
        Container(
            # Paso 1: Install
            Container(
                Container(
                    Image(
                        src="download.svg",
                        alt="Install",
                        width="80px",
                        height="80px",
                        style={
                            "margin-bottom": "20px",
                            "filter": "drop-shadow(0 0 10px rgba(162, 255, 226, 0.4))",
                            "transition": "all 0.3s ease"
                        }
                    ),
                    Text(
                        "Install",
                        style={
                            "font-size": "24px",
                            "font-weight": "700",
                            "color": "#a2ffe2",
                            "margin-bottom": "12px"
                        }
                    ),
                    Text(
                        "Install Dars with a simple ",
                        style={
                            "font-size": "16px",
                            "color": "#a0cfc0",
                            "line-height": "1.5",
                            "display": "inline"
                        }
                    ),
                    Text(
                        "pip install dars-framework",
                        style={
                            "font-size": "16px",
                            "color": "#92ffe5",
                            "font-weight": "600",
                            "font-family": "monospace",
                            "background": "rgba(162, 255, 226, 0.1)",
                            "padding": "4px 8px",
                            "border-radius": "4px",
                            "display": "inline",
                            "line-height": "1.5"
                        }
                    ),
                    Text(
                        " and start building immediately.",
                        style={
                            "font-size": "16px",
                            "color": "#a0cfc0",
                            "line-height": "1.5",
                            "display": "inline"
                        }
                    ),
                    style={
                        "text-align": "center",
                        "padding": "40px 30px"
                    }
                ),
                id="howitworks-step-1",
                style={
                    "background": "rgba(20, 30, 27, 0.6)",
                    "border": "1px solid rgba(100,255,200,0.1)",
                    "border-radius": "16px",
                    "backdrop-filter": "blur(12px)",
                    "box-shadow": "0 8px 32px rgba(0,0,0,0.2)",
                    "transition": "all 0.6s ease",
                    "position": "relative",
                    "overflow": "hidden"
                }
            ),
            # Paso 2: Develop
            Container(
                Container(
                    Image(
                        src="code.svg",
                        alt="Develop",
                        width="80px",
                        height="80px",
                        style={
                            "margin-bottom": "20px",
                            "filter": "drop-shadow(0 0 10px rgba(162, 255, 226, 0.4))",
                            "transition": "all 0.3s ease"
                        }
                    ),
                    Text(
                        "Develop",
                        style={
                            "font-size": "24px",
                            "font-weight": "700",
                            "color": "#a2ffe2",
                            "margin-bottom": "12px"
                        }
                    ),
                    Text(
                        "Use the intuitive API to create routes, components, and pages with minimal code.",
                        style={
                            "font-size": "16px",
                            "color": "#a0cfc0",
                            "line-height": "1.5"
                        }
                    ),
                    style={
                        "text-align": "center",
                        "padding": "40px 30px"
                    }
                ),
                id="howitworks-step-2",
                style={
                    "background": "rgba(20, 30, 27, 0.6)",
                    "border": "1px solid rgba(100,255,200,0.1)",
                    "border-radius": "16px",
                    "backdrop-filter": "blur(12px)",
                    "box-shadow": "0 8px 32px rgba(0,0,0,0.2)",
                    "transition": "all 0.6s ease",
                    "position": "relative",
                    "overflow": "hidden"
                }
            ),
            # Paso 3: Deploy
            Container(
                Container(
                    Image(
                        src="deploy.svg",
                        alt="Deploy",
                        width="80px",
                        height="80px",
                        style={
                            "margin-bottom": "20px",
                            "filter": "drop-shadow(0 0 10px rgba(162, 255, 226, 0.4))",
                            "transition": "all 0.3s ease"
                        }
                    ),
                    Text(
                        "Deploy",
                        style={
                            "font-size": "24px",
                            "font-weight": "700",
                            "color": "#a2ffe2",
                            "margin-bottom": "12px"
                        }
                    ),
                    Text(
                        "Deploy your application in the test built-in server or your preferred hosting provider. Or export it to desktop as a native app.",
                        style={
                            "font-size": "16px",
                            "color": "#a0cfc0",
                            "line-height": "1.5"
                        }
                    ),
                    style={
                        "text-align": "center",
                        "padding": "40px 30px"
                    }
                ),
                id="howitworks-step-3",
                style={
                    "background": "rgba(20, 30, 27, 0.6)",
                    "border": "1px solid rgba(100,255,200,0.1)",
                    "border-radius": "16px",
                    "backdrop-filter": "blur(12px)",
                    "box-shadow": "0 8px 32px rgba(0,0,0,0.2)",
                    "transition": "all 0.6s ease",
                    "position": "relative",
                    "overflow": "hidden"
                }
            ),
            style={
                "display": "grid",
                "grid-template-columns": "repeat(auto-fit, minmax(350px, 1fr))",
                "gap": "30px",
                "max-width": "1200px",
                "margin": "0 auto",
                "padding": "0 20px"
            }
        ),
        id="howitworks-section",
        style={
            "padding": "50px 40px",  # Cambiado de 0px 40px a 80px 40px
            "background": "linear-gradient(135deg, #0f1e1a 0%, #132d24 100%)",
            "min-height": "auto",    # Cambiado de 100vh a auto
            "display": "flex",
            "flex-direction": "column",
            "justify-content": "flex-start"  # Cambiado de center a flex-start
        }
    )