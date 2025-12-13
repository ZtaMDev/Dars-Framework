from dars.all import *

def create_animation_showcase():
    """Animation system demonstration"""
    
    # Animation target box
    anim_box = Container(
        Text(
            "Watch Me Animate!",
            style={
                "font-size": "24px",
                "font-weight": "600",
                "color": "white",
                "text-align": "center"
            }
        ),
        id="anim-target",
        style={
            "background": "linear-gradient(135deg, #ec4899, #8b5cf6)",
            "padding": "40px",
            "border-radius": "16px",
            "margin": "30px auto",
            "max-width": "300px",
            "box-shadow": "0 8px 24px rgba(139, 92, 246, 0.3)"
        }
    )
    
    # Animation buttons
    fade_btn = Button(
        "Fade In",
        on_click=fadeIn(id="anim-target", duration=600),
        style={
            "background": "rgba(59, 130, 246, 0.15)",
            "color": "#60a5fa",
            "border": "1px solid rgba(59, 130, 246, 0.3)",
            "padding": "10px 20px",
            "border-radius": "8px",
            "font-size": "14px",
            "font-weight": "600",
            "cursor": "pointer",
            "margin": "5px",
            "transition": "all 0.2s ease"
        },
        hover_style={
            "background": "rgba(59, 130, 246, 0.25)",
            "border-color": "rgba(59, 130, 246, 0.5)"
        }
    )
    
    slide_btn = Button(
        "Slide In",
        on_click=slideIn(id="anim-target", direction="left", duration=500),
        style={
            "background": "rgba(16, 185, 129, 0.15)",
            "color": "#34d399",
            "border": "1px solid rgba(16, 185, 129, 0.3)",
            "padding": "10px 20px",
            "border-radius": "8px",
            "font-size": "14px",
            "font-weight": "600",
            "cursor": "pointer",
            "margin": "5px",
            "transition": "all 0.2s ease"
        },
        hover_style={
            "background": "rgba(16, 185, 129, 0.25)",
            "border-color": "rgba(16, 185, 129, 0.5)"
        }
    )
    
    shake_btn = Button(
        "Shake",
        on_click=shake(id="anim-target", intensity=10),
        style={
            "background": "rgba(245, 158, 11, 0.15)",
            "color": "#fbbf24",
            "border": "1px solid rgba(245, 158, 11, 0.3)",
            "padding": "10px 20px",
            "border-radius": "8px",
            "font-size": "14px",
            "font-weight": "600",
            "cursor": "pointer",
            "margin": "5px",
            "transition": "all 0.2s ease"
        },
        hover_style={
            "background": "rgba(245, 158, 11, 0.25)",
            "border-color": "rgba(245, 158, 11, 0.5)"
        }
    )
    
    pulse_btn = Button(
        "Pulse",
        on_click=pulse(id="anim-target", scale=1.15, iterations=3),
        style={
            "background": "rgba(139, 92, 246, 0.15)",
            "color": "#a78bfa",
            "border": "1px solid rgba(139, 92, 246, 0.3)",
            "padding": "10px 20px",
            "border-radius": "8px",
            "font-size": "14px",
            "font-weight": "600",
            "cursor": "pointer",
            "margin": "5px",
            "transition": "all 0.2s ease"
        },
        hover_style={
            "background": "rgba(139, 92, 246, 0.25)",
            "border-color": "rgba(139, 92, 246, 0.5)"
        }
    )
    
    bounce_btn = Button(
        "Bounce",
        on_click=bounce(id="anim-target", distance=20),
        style={
            "background": "rgba(236, 72, 153, 0.15)",
            "color": "#f472b6",
            "border": "1px solid rgba(236, 72, 153, 0.3)",
            "padding": "10px 20px",
            "border-radius": "8px",
            "font-size": "14px",
            "font-weight": "600",
            "cursor": "pointer",
            "margin": "5px",
            "transition": "all 0.2s ease"
        },
        hover_style={
            "background": "rgba(236, 72, 153, 0.25)",
            "border-color": "rgba(236, 72, 153, 0.5)"
        }
    )
    
    sequence_btn = Button(
        "Sequence",
        on_click=sequence(
            fadeIn(id="anim-target", duration=400),
            pulse(id="anim-target", scale=1.1, iterations=2),
            shake(id="anim-target", intensity=5, duration=400)
        ),
        style={
            "background": "rgba(239, 68, 68, 0.15)",
            "color": "#f87171",
            "border": "1px solid rgba(239, 68, 68, 0.3)",
            "padding": "10px 20px",
            "border-radius": "8px",
            "font-size": "14px",
            "font-weight": "600",
            "cursor": "pointer",
            "margin": "5px",
            "transition": "all 0.2s ease"
        },
        hover_style={
            "background": "rgba(239, 68, 68, 0.25)",
            "border-color": "rgba(239, 68, 68, 0.5)"
        }
    )
    
    return Container(
        Text(
            "Animation System",
            style={
                "font-size": "32px",
                "font-weight": "700",
                "color": "#f1f5f9",
                "margin-bottom": "15px",
                "text-align": "center"
            }
        ),
        Text(
            "15+ built-in animations with chainable dScript API",
            style={
                "font-size": "16px",
                "color": "#94a3b8",
                "margin-bottom": "20px",
                "text-align": "center"
            }
        ),
        anim_box,
        Container(
            fade_btn,
            slide_btn,
            shake_btn,
            pulse_btn,
            bounce_btn,
            sequence_btn,
            style={
                "display": "flex",
                "flex-wrap": "wrap",
                "justify-content": "center",
                "gap": "10px",
                "max-width": "600px",
                "margin": "0 auto"
            }
        ),
        # Code example
        Container(
            Text(
                "Code Example:",
                style={
                    "font-size": "14px",
                    "font-weight": "600",
                    "color": "#94a3b8",
                    "margin": "30px 0 10px 0"
                }
            ),
            Text(
                'button.on_click = sequence(\n    fadeIn(id="box"),\n    pulse(id="box", scale=1.1),\n    shake(id="box")\n)',
                style={
                    "font-family": "monospace",
                    "font-size": "14px",
                    "color": "#ec4899",
                    "background": "rgba(30, 41, 59, 0.6)",
                    "padding": "15px",
                    "border-radius": "8px",
                    "border": "1px solid rgba(236, 72, 153, 0.2)",
                    "white-space": "pre"
                }
            ),
            style={
                "max-width": "500px",
                "margin": "0 auto"
            }
        ),
        style={
            "background": "rgba(15, 23, 42, 0.6)",
            "backdrop-filter": "blur(10px)",
            "padding": "40px",
            "border-radius": "16px",
            "border": "1px solid rgba(255, 255, 255, 0.1)",
            "box-shadow": "0 8px 32px rgba(0, 0, 0, 0.3)",
            "margin": "30px auto",
            "max-width": "750px"
        }
    )
