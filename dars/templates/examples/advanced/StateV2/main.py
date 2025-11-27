"""
State V2 Example Template
Professional demonstration of the new Pythonic state management system

This template showcases:
- Pure Python state API
- Reactive properties  
- Auto-increment/decrement operations
- Reset functionality
- 15+ animation functions
- Animation chaining with sequence()
"""

from dars.all import *
from hero_component import create_hero
from counter_component import create_counter_demo
from timer_component import create_timer_demo
from animation_component import create_animation_showcase

# Initialize app
app = App(
    title="State V2 Demo",
    language="en",
    favicon=None,
    author="Dars Framework",
    description="Professional State V2 and Animation System Demo",
    theme_color="#0f172a",
    background_color="#0f172a"
)

# Build page with functional components
page = Page(
    create_hero(),
    Container(
        create_counter_demo(),
        create_timer_demo(),
        create_animation_showcase(),
        
        # Features overview
        Container(
            Text(
                "Key Features",
                style={
                    "font-size": "28px",
                    "font-weight": "700",
                    "color": "#f1f5f9",
                    "margin-bottom": "25px",
                    "text-align": "center"
                }
            ),
            Container(
                Container(
                    Text("Pure Pythonic API", style={
                        "font-size": "18px",
                        "font-weight": "600",
                        "color": "#60a5fa",
                        "margin-bottom": "8px"
                    }),
                    Text("state.text.increment() - Clean and intuitive", style={
                        "font-size": "14px",
                        "color": "#94a3b8",
                        "line-height": "1.5"
                    }),
                    style={
                        "background": "rgba(30, 41, 59, 0.5)",
                        "padding": "20px",
                        "border-radius": "12px",
                        "border": "1px solid rgba(59, 130, 246, 0.2)"
                    }
                ),
                Container(
                    Text("Auto Operations", style={
                        "font-size": "18px",
                        "font-weight": "600",
                        "color": "#34d399",
                        "margin-bottom": "8px"
                    }),
                    Text("Continuous reactive operations with interval control", style={
                        "font-size": "14px",
                        "color": "#94a3b8",
                        "line-height": "1.5"
                    }),
                    style={
                        "background": "rgba(30, 41, 59, 0.5)",
                        "padding": "20px",
                        "border-radius": "12px",
                        "border": "1px solid rgba(16, 185, 129, 0.2)"
                    }
                ),
                Container(
                    Text("Animation System", style={
                        "font-size": "18px",
                        "font-weight": "600",
                        "color": "#ec4899",
                        "margin-bottom": "8px"
                    }),
                    Text("15+ animations with chainable dScript API", style={
                        "font-size": "14px",
                        "color": "#94a3b8",
                        "line-height": "1.5"
                    }),
                    style={
                        "background": "rgba(30, 41, 59, 0.5)",
                        "padding": "20px",
                        "border-radius": "12px",
                        "border": "1px solid rgba(236, 72, 153, 0.2)"
                    }
                ),
                style={
                    "display": "grid",
                    "grid-template-columns": "repeat(auto-fit, minmax(280px, 1fr))",
                    "gap": "20px",
                    "max-width": "1000px",
                    "margin": "0 auto"
                }
            ),
            style={
                "padding": "60px 20px",
                "background": "rgba(15, 23, 42, 0.4)"
            }
        ),
        
        style={
            "min-height": "100vh",
            "padding": "0 20px 60px"
        }
    ),
    style={
        "background": "linear-gradient(180deg, #0f172a 0%, #1e293b 50%, #0f172a 100%)",
        "min-height": "100vh",
        "font-family": "system-ui, -apple-system, sans-serif"
    }
)

# Configure app
app.set_theme("dark")
app.add_global_style(file_path="styles.css")
app.add_page("index", page, title="State V2 Demo", index=True)

if __name__ == "__main__":
    app.rTimeCompile()
