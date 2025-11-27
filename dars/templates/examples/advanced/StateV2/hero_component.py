from dars.all import *

def create_hero():
    """Hero section introducing State V2"""
    return Container(
        Text(
            text="State V2 Dars Framework",
            style={
                "font-size": "56px",
                "font-weight": "800",
                "margin": "0 0 20px 0",
                "background": "linear-gradient(90deg, #4f46e5, #7c3aed, #a855f7)",
                "background-clip": "text",
                "-webkit-background-clip": "text",
                "color": "transparent",
                "text-align": "center"
            }
        ),
        Text(
            text="Modern Pythonic State Management and Animations",
            style={
                "font-size": "20px",
                "color": "#94a3b8",
                "max-width": "700px",
                "text-align": "center",
                "margin-bottom": "30px",
                "line-height": "1.6"
            }
        ),
        Text(
            text="Experience the power of reactive state management with a pure Python API. No more verbose dState syntax - just clean, intuitive code.",
            style={
                "font-size": "16px",
                "color": "#64748b",
                "max-width": "600px",
                "text-align": "center",
                "margin-bottom": "40px",
                "line-height": "1.5"
            }
        ),
        id="hero-section",
        style={
            "min-height": "60vh",
            "display": "flex",
            "flex-direction": "column",
            "align-items": "center",
            "justify-content": "center",
            "padding": "80px 20px 60px",
            "background": "linear-gradient(135deg, #0f172a 0%, #1e293b 100%)"
        }
    )
