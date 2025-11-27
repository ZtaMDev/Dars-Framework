from dars.all import *

def create_counter_demo():
    """Interactive counter demonstration with State V2"""
    
    # Create counter display
    counter_display = Text("0", id="counter-value", style={
        "font-size": "72px",
        "font-weight": "bold",
        "color": "#60a5fa",
        "text-align": "center",
        "margin": "30px 0",
        "font-family": "monospace"
    })
    
    # Create state
    counter_state = State(counter_display, text=0)
    
    # Buttons
    increment_btn = Button(
        "Increment",
        on_click=counter_state.text.increment(by=1),
        style={
            "background": "linear-gradient(135deg, #3b82f6,  #2563eb)",
            "color": "white",
            "border": "none",
            "padding": "12px 28px",
            "border-radius": "8px",
            "font-size": "16px",
            "font-weight": "600",
            "cursor": "pointer",
            "margin": "5px",
            "transition": "transform 0.2s ease"
        },
        hover_style={
            "transform": "translateY(-2px)",
            "box-shadow": "0 6px 20px rgba(59, 130, 246, 0.4)"
        }
    )
    
    decrement_btn = Button(
        "Decrement",
        on_click=counter_state.text.increment(by=-1),
        style={
            "background": "linear-gradient(135deg, #ef4444, #dc2626)",
            "color": "white",
            "border": "none",
            "padding": "12px 28px",
            "border-radius": "8px",
            "font-size": "16px",
            "font-weight": "600",
            "cursor": "pointer",
            "margin": "5px",
            "transition": "transform 0.2s ease"
        },
        hover_style={
            "transform": "translateY(-2px)",
            "box-shadow": "0 6px 20px rgba(239, 68, 68, 0.4)"
        }
    )
    
    reset_btn = Button(
        "Reset",
        on_click=counter_state.reset(),
        style={
            "background": "linear-gradient(135deg, #64748b, #475569)",
            "color": "white",
            "border": "none",
            "padding": "12px 28px",
            "border-radius": "8px",
            "font-size": "16px",
            "font-weight": "600",
            "cursor": "pointer",
            "margin": "5px",
            "transition": "transform 0.2s ease"
        },
        hover_style={
            "transform": "translateY(-2px)",
            "box-shadow": "0 6px 20px rgba(100, 116, 139, 0.4)"
        }
    )
    
    pulse_btn = Button(
        "Pulse Animation",
        on_click=pulse(id="counter-value", scale=1.2, iterations=2),
        style={
            "background": "linear-gradient(135deg, #8b5cf6, #7c3aed)",
            "color": "white",
            "border": "none",
            "padding": "12px 28px",
            "border-radius": "8px",
            "font-size": "16px",
            "font-weight": "600",
            "cursor": "pointer",
            "margin": "5px",
            "transition": "transform 0.2s ease"
        },
        hover_style={
            "transform": "translateY(-2px)",
            "box-shadow": "0 6px 20px rgba(139, 92, 246, 0.4)"
        }
    )
    
    return Container(
        Text(
            "Interactive Counter",
            style={
                "font-size": "32px",
                "font-weight": "700",
                "color": "#f1f5f9",
                "margin-bottom": "15px",
                "text-align": "center"
            }
        ),
        Text(
            "Pure Pythonic state management - no verbose syntax needed",
            style={
                "font-size": "16px",
                "color": "#94a3b8",
                "margin-bottom": "20px",
                "text-align": "center"
            }
        ),
        counter_display,
        Container(
            increment_btn,
            decrement_btn,
            reset_btn,
            pulse_btn,
            style={
                "display": "flex",
                "flex-wrap": "wrap",
                "justify-content": "center",
                "gap": "10px"
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
                'counter = State(display, text=0)\nincrement_btn.on_click = counter.text.increment(by=1)',
                style={
                    "font-family": "monospace",
                    "font-size": "14px",
                    "color": "#60a5fa",
                    "background": "rgba(30, 41, 59, 0.6)",
                    "padding": "15px",
                    "border-radius": "8px",
                    "border": "1px solid rgba(59, 130, 246, 0.2)",
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
            "max-width": "700px"
        }
    )
