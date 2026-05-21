from dars.all import *

CODE_MD = '''```python
from dars.all import *

app = App("My App")
counter = State("ui", count=0)

@route("/")
def index():
    return Page(
        Text(useDynamic("ui.count"), 
            style="fs-[48px] font-bold"
        ),
        Button("+", 
            on_click=counter.count.increment(1)
        ),
        Button("−", 
            on_click=counter.count.decrement(1)
        ),
    )

app.add_page("index", index(), title="Index")
```'''


def _code_example():
    """Code editor + live result side by side, compact."""

    code_panel = Container(
        # Top bar
        Container(
            Container(
                Container(style={"width":"10px","height":"10px","border-radius":"50%","background":"#ff5f57"}),
                Container(style={"width":"10px","height":"10px","border-radius":"50%","background":"#febc2e"}),
                Container(style={"width":"10px","height":"10px","border-radius":"50%","background":"#28c840"}),
                style={"display":"flex","gap":"6px","align-items":"center"}
            ),
            Text(text="main.py", style={
                "font-size": "11px", "color": "rgba(160,207,192,0.45)",
                "font-family": "monospace", "margin-left": "12px",
            }),
            style={
                "display":"flex","align-items":"center",
                "padding":"10px 14px",
                "background":"rgba(8,14,12,0.9)",
                "border-bottom":"1px solid rgba(146,255,229,0.05)",
                "border-radius":"10px 10px 0 0",
            }
        ),
        # Code via Markdown (Prism syntax highlight)
        Container(
            Markdown(content=CODE_MD, dark_theme=True, class_name="code_block"),
            style={"padding": "0", "overflow-x": "auto"}
        ),
        id="code-panel",
        style={
            "background": "rgba(10,16,14,0.95)",
            "border": "1px solid rgba(146,255,229,0.08)",
            "border-radius": "10px",
            "flex": "1.2",
            "min-width": "0",
            "overflow": "hidden",
        }
    )
    counter = State("counter", count=0)
    result_panel = Container(
        # Top bar
        Container(
            Container(
                Container(style={"width":"7px","height":"7px","border-radius":"50%","background":"#10b981"}),
                Text(text="Preview", style={
                    "font-size":"10px","color":"#10b981","font-weight":"600",
                    "text-transform":"uppercase","letter-spacing":"0.8px",
                }),
                style={"display":"flex","align-items":"center","gap":"6px"}
            ),
            style={
                "padding":"9px 14px",
                "border-bottom":"1px solid rgba(146,255,229,0.05)",
            }
        ),
        # Counter demo
        Container(
            Text(text="Counter", style={
                "font-size":"20px","color":"#10b981","font-weight":"600",
                "text-transform":"uppercase","margin-bottom":"20px",
            }),
            Text(text=useDynamic("counter.count"), id="demo-counter-value", style={
                "font-size": "52px", "font-weight": "800", "line-height": "1",
                "background": "linear-gradient(135deg, #92ffe5, #38c49f)",
                "background-clip": "text", "-webkit-background-clip": "text",
                "color": "transparent", "margin-bottom": "20px",
                "transition": "transform 0.15s ease",
            }),
            Container(
                Button(text="−", id="demo-dec-btn", on_click=counter.count.decrement(1), style={
                    "width":"44px","height":"44px","border-radius":"10px",
                    "border":"1px solid rgba(146,255,229,0.15)",
                    "background":"rgba(26,58,48,0.8)","color":"#92ffe5",
                    "font-size":"22px","font-weight":"700","cursor":"pointer",
                    "transition":"all 0.2s ease",
                },
                hover_style={
                    "border":"1px solid rgba(146,255,229,0.5)",
                    "scale":"1.1",
                    "background-color":"rgba(26,58,48,0.5)",
                },
                active_style={
                    "border":"1px solid rgba(146,255,229,0.5)",
                },
                ),
                Button(text="+", id="demo-inc-btn", on_click=counter.count.increment(1), style={
                        "width":"44px","height":"44px","border-radius":"10px",
                        "border":"none",
                        "background":"linear-gradient(135deg, #10b981, #059669)",
                        "color":"white","font-size":"22px","font-weight":"700",
                        "cursor":"pointer","transition":"all 0.2s ease",
                        "box-shadow":"0 4px 12px rgba(16,185,129,0.3)",
                    },
                    hover_style={
                        "box-shadow":"0 4px 12px rgba(16,185,129,0.3)",
                        "scale":"1.1",
                        "background-color":"#059669",
                    },
                    active_style={
                        "box-shadow":"0 4px 12px rgba(16,185,129,0.3)",
                    }
                ),
                style={"display":"flex","gap":"12px"}
            ),
            style={
                "display":"flex","flex-direction":"column",
                "align-items":"center","justify-content":"center",
                "text-align":"center",
                "flex":"1","padding":"28px 16px",
            }
        ),
        id="result-panel",
        style={
            "background": "rgba(10,16,14,0.95)",
            "border": "1px solid rgba(146,255,229,0.08)",
            "border-radius": "10px",
            "width": "240px", "flex-shrink": "0",
            "display": "flex", "flex-direction": "column",
            "overflow": "hidden",
        }
    )

    return Container(
        code_panel,
        result_panel,
        id="code-showcase",
        style={
            "display": "flex", "align-items": "stretch",
            "gap": "20px", "max-width": "1100px",
            "margin": "0 auto 40px", "padding": "0 20px",
            "width": "100%"
        }
    )


def _feature_card(icon, title, description, card_id, delay):
    return Container(
        Container(
            Image(
                src=icon, alt=title, width="80px", height="80px",
                style={
                    "margin-bottom": "20px",
                    "filter": "drop-shadow(0 0 10px rgba(162, 255, 226, 0.3))",
                    "transition": "all 0.3s ease"
                }
            ),
            Text(text=title, style={
                "font-size": "24px", "font-weight": "700",
                "color": "#a2ffe2", "margin-bottom": "12px"
            }),
            Text(text=description, style={
                "font-size": "16px", "color": "#a0cfc0", "line-height": "1.5"
            }),
            style={"text-align": "center", "padding": "40px 30px"}
        ),
        id=card_id,
        style={
            "background": "rgba(20, 30, 27, 0.6)",
            "border": "1px solid rgba(100,255,200,0.1)",
            "border-radius": "16px",
            "backdrop-filter": "blur(12px)",
            "box-shadow": "0 8px 32px rgba(0,0,0,0.2)",
            "transition": "all 0.3s ease",
        }
    )

def create_example():
    return Container(
            Text(
                text="Write Less, Build More",
                id="example-title",
                style={
                    "font-size": "56px", "font-weight": "900",
                    "text-align": "center", "margin-bottom": "20px",
                    "background": "linear-gradient(90deg, #92ffe5, #38c49f, #7dfdd8, #92ffe5)",
                    "background-size": "300% 300%",
                    "background-clip": "text", "-webkit-background-clip": "text",
                    "color": "transparent",
                    "animation": "colorCycle 6s ease-in-out infinite alternate",
                    "letter-spacing": "-1.5px"
                }
            ),
            Text(
                text="Experience a declarative, state-driven approach. Build high-performance applications with an elegant Pythonic API that handles the heavy lifting for you.",
                id="example-subtitle",
                style={
                    "font-size": "22px", "color": "#a0cfc0",
                    "text-align": "center", "margin-bottom": "60px",
                    "max-width": "800px",
                    "margin-left": "auto", "margin-right": "auto",
                    "line-height": "1.6"
                }
            ),
            _code_example(),
            id="example-section",
            style={
                "padding": "30px 10px",
                "background": "linear-gradient(135deg, #0a1512 0%, #0f1e1a 100%)",
                "min-height": "100vh",
                "display": "flex", "flex-direction": "column",
                "justify-content": "flex-start"
            },
        )
def create_features():
    return Container(
        Text(
            text="Features",
            style={
                "font-size": "48px", "font-weight": "800",
                "text-align": "center", "margin-bottom": "20px",
                "background": "linear-gradient(90deg, #92ffe5, #38c49f, #7dfdd8, #92ffe5)",
                "background-size": "300% 300%",
                "background-clip": "text", "-webkit-background-clip": "text",
                "color": "transparent",
                "animation": "colorCycle 6s ease-in-out infinite alternate"
            }
        ),
        Text(
            text="Everything you need to build amazing applications",
            style={
                "font-size": "20px", "color": "#a0cfc0",
                "text-align": "center", "margin-bottom": "50px",
                "max-width": "600px",
                "margin-left": "auto", "margin-right": "auto"
            }
        ),
        Container(
            _feature_card("rocket.svg", "Fast Development",
                "Build applications quickly with our intuitive API and pre-built components, or creating your own custom components.",
                "feature-card-0", 0.0),
            _feature_card("globe.svg", "Multiplatform",
                "Deploy your apps on the web with the same codebase and minimal configuration.",
                "feature-card-1", 0.1),
            _feature_card("lightning.svg", "High Performance",
                "Optimized rendering and efficient resource management for smooth experiences.",
                "feature-card-2", 0.2),
            style={
                "display": "grid",
                "grid-template-columns": "repeat(auto-fit, minmax(350px, 1fr))",
                "gap": "30px", "max-width": "1200px",
                "margin": "0 auto", "padding": "0 20px"
            }
        ),
        id="features-section",
        style={
            "padding": "50px 40px",
            "background": "linear-gradient(135deg, #0f1e1a 0%, #132d24 100%)",
            "min-height": "100vh",
            "display": "flex", "flex-direction": "column",
            "justify-content": "flex-start"
        }
    )
