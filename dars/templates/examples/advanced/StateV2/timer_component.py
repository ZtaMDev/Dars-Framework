from dars.all import *

def create_timer_demo():
    """Auto-incrementing timer demonstration"""
    
    # Timer display
    timer_display = Text("0", id="timer-value", style={
        "font-size": "64px",
        "font-weight": "bold",
        "color": "#34d399",
        "text-align": "center",
        "margin": "30px 0",
        "font-family": "monospace"
    })
    
    # Create state with auto operations
    timer_state = State(timer_display, text=0)
    
    # Control buttons
    start_btn = Button(
        "Start Timer",
        on_click=timer_state.text.auto_increment(by=1, interval=1000),
        style={
            "background": "linear-gradient(135deg, #10b981, #059669)",
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
            "box-shadow": "0 6px 20px rgba(16, 185, 129, 0.4)"
        }
    )
    
    stop_btn = Button(
        "Stop Timer",
        on_click=timer_state.text.stop_auto(),
        style={
            "background": "linear-gradient(135deg, #f59e0b, #d97706)",
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
            "box-shadow": "0 6px 20px rgba(245, 158, 11, 0.4)"
        }
    )
    
    reset_btn = Button(
        "Reset",
        on_click=timer_state.reset(),
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
    
    return Container(
        Text(
            "Auto-Incrementing Timer",
            style={
                "font-size": "32px",
                "font-weight": "700",
                "color": "#f1f5f9",
                "margin-bottom": "15px",
                "text-align": "center"
            }
        ),
        Text(
            "Continuous reactive operations made simple",
            style={
                "font-size": "16px",
                "color": "#94a3b8",
                "margin-bottom": "20px",
                "text-align": "center"
            }
        ),
        timer_display,
        Container(
            start_btn,
            stop_btn,
            reset_btn,
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
                'timer = State(display, text=0)\nstart_btn.on_click = timer.text.auto_increment(by=1, interval=1000)\nstop_btn.on_click = timer.text.stop_auto()',
                style={
                    "font-family": "monospace",
                    "font-size": "14px",
                    "color": "#34d399",
                    "background": "rgba(30, 41, 59, 0.6)",
                    "padding": "15px",
                    "border-radius": "8px",
                    "border": "1px solid rgba(52, 211, 153, 0.2)",
                    "white-space": "pre"
                }
            ),
            style={
                "max-width": "550px",
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
