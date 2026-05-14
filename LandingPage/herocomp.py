from dars.all import *


def create_hero():
    return Container(
        Image(
            src="Dars-logo.png",
            alt="Dars Framework Logo",
            width="240px",
            height="240px",
            id="hero-logo",
            style={
                "opacity": "0",
                "transform": "scale(0.8)",
                "margin-bottom": "20px",
                "transition": "all 0.7s cubic-bezier(0.4, 0, 0.2, 1)"
            },
        ),
        Text(
            text="Dars Framework",
            id="hero-title",
            style={
                "font-size": "64px",
                "font-weight": "800",
                "margin": "0",
                "background": "linear-gradient(90deg, #92ffe5, #38c49f, #7dfdd8, #92ffe5)",
                "background-size": "300% 300%",
                "background-clip": "text",
                "-webkit-background-clip": "text",
                "color": "transparent",
                "opacity": "0",
                "transform": "translateY(20px)",
                "transition": "all 0.8s ease-out",
                "animation": "colorCycle 6s ease-in-out infinite alternate"
            }
        ),
        Text(
            text=(
                "Dynamic Application Rendering System is a modern Full-Stack Python framework for web and desktop apps development. "
                "Dars is designed to make web and desktop apps development simple, fast, and enjoyable. "
                "With an intuitive API and powerful features, you can build modern web and desktop apps in record time using Python."
            ),
            id="hero-description",
            style={
                "font-size": "20px",
                "color": "#a0cfc0",
                "max-width": "800px",
                "text-align": "center",
                "margin-top": "20px",
                "opacity": "0",
                "line-height": "1.6",
                "transform": "translateY(10px)",
                "transition": "all 0.9s ease-out"
            }
        ),
        Container(
            Container(
                Text(
                    id="pip-command-text",
                    text="pip install dars-framework",
                    style={
                        "font-family": "monospace",
                        "font-size": "18px",
                        "color": "#92ffe5",
                        "background": "rgba(20, 30, 27, 0.6)",
                        "padding": "12px 20px",
                        "border-radius": "8px",
                        "border": "1px solid rgba(100,255,200,0.1)",
                        "transition": "all 0.3s ease",
                        "cursor": "pointer",
                        "margin-right": "0px",
                        "flex": "1"
                    }
                ),
                Button(
                    text="Copy",
                    on_click=[
                        copyElementText("pip-command-text"),
                        this().state(text="Copied!", style={
                            "background": "linear-gradient(135deg, #38c49f 0%, #2a6b5b 100%) !important"
                            }
                        ),
                        setTimeout(1000, this().state(
                            text="Copy", 
                            style={
                                "background": "linear-gradient(135deg, #1d4a3f 0%, #2a6b5b 100%) !important"
                                }
                            )
                        )
                    ],
                    style={
                        "background": "rgba(20, 30, 27, 0.9)",
                        "border": "1px solid rgba(100,255,200,0.3)",
                        "color": "#92ffe5",
                        "padding": "12px 5px",
                        "border-radius": "8px",
                        "cursor": "pointer",
                        "font-size": "14px",
                        "font-weight": "600",
                        "transition": "all 0.3s ease",
                        "opacity": "0",
                        "width": "0px",
                        "overflow": "hidden",
                        "white-space": "nowrap",
                        "margin-left": "0px",
                        "flex-shrink": "0"
                    },
                    id="copy-btn"
                ),
                style={
                    "display": "flex",
                    "align-items": "center",
                    "background": "rgba(20, 30, 27, 0.6)",
                    "border": "1px solid rgba(100,255,200,0.1)",
                    "border-radius": "8px",
                    "padding": "0px",
                    "transition": "all 0.3s ease",
                    "overflow": "hidden",
                    "max-width": "fit-content"
                },
                id="pip-command-inner"
            ),
            style={
                "display": "flex",
                "align-items": "center",
                "margin-top": "20px",
                "opacity": "0",
                "align-items":"center",
                "transform": "translateY(10px)",
                "transition": "all 0.9s ease-out"
            },
            id="pip-command"
        ),
        Button(
            text="Get Started",
            id="get-started-btn",
            on_click=goToNew("https://ztamdev.github.io/Dars-Framework/docs.html"),
            style={
                "margin-top": "25px",
                "margin-bottom": "20px",
                "padding": "14px 42px",
                "font-size": "18px",
                "font-weight": "600",
                "border": "none",
                "border-radius": "12px",
                "cursor": "pointer",
                "opacity": "0",
            }
        ),
        id="hero-section",
        style={
            "min-height": "100vh",
            "display": "flex",
            "height": "auto",
            "flex-direction": "column",
            "align-items": "center",
            "justify-content": "center",
            "text-align": "center",
            "background": "linear-gradient(135deg, #0f1e1a 0%, #132d24 100%)",
            "position": "relative",
            "padding-top": "80px",
            "padding": "80px 20px 40px",
        }
    )