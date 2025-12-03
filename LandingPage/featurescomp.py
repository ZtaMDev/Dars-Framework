# Dars Framework - Core Source File
#
# This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0.
# If a copy of the MPL was not distributed with this file, You can obtain one at
# https://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2025 ZtaDev
from dars.all import *

def create_features():
    # Crear cada feature card explícitamente con su propio ID e imágenes SVG
    feature_card_0 = Container(
        Container(
            Image(
                src="rocket.svg",
                alt="Fast Development",
                width="80px",
                height="80px",
                style={
                    "margin-bottom": "20px",
                    "filter": "drop-shadow(0 0 10px rgba(162, 255, 226, 0.3))",
                    "transition": "all 0.3s ease"
                }
            ),
            Text(
                text="Fast Development",
                style={
                    "font-size": "24px",
                    "font-weight": "700",
                    "color": "#a2ffe2",
                    "margin-bottom": "12px"
                }
            ),
            Text(
                text="Build applications quickly with our intuitive API and pre-built components, or creating your own custom components.",
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
        id="feature-card-0",
        style={
            "background": "rgba(20, 30, 27, 0.6)",
            "border": "1px solid rgba(100,255,200,0.1)",
            "border-radius": "16px",
            "backdrop-filter": "blur(12px)",
            "box-shadow": "0 8px 32px rgba(0,0,0,0.2)",
            "opacity": "0",
            "transform": "translateY(40px) rotateX(10deg)",
            "transition": "all 0.6s ease 0.0s"
        }
    )

    feature_card_1 = Container(
        Container(
            Image(
                src="globe.svg",
                alt="Multiplatform",
                width="80px",
                height="80px",
                style={
                    "margin-bottom": "20px",
                    "filter": "drop-shadow(0 0 10px rgba(162, 255, 226, 0.3))",
                    "transition": "all 0.3s ease"
                }
            ),
            Text(
                text="Multiplatform",
                style={
                    "font-size": "24px",
                    "font-weight": "700",
                    "color": "#a2ffe2",
                    "margin-bottom": "12px"
                }
            ),
            Text(
                text="Deploy your apps on web and desktop with the same codebase changing only a single configuration.",
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
        id="feature-card-1",
        style={
            "background": "rgba(20, 30, 27, 0.6)",
            "border": "1px solid rgba(100,255,200,0.1)",
            "border-radius": "16px",
            "backdrop-filter": "blur(12px)",
            "box-shadow": "0 8px 32px rgba(0,0,0,0.2)",
            "opacity": "0",
            "transform": "translateY(40px) rotateX(10deg)",
            "transition": "all 0.6s ease 0.1s"
        }
    )

    feature_card_2 = Container(
        Container(
            Image(
                src="lightning.svg",
                alt="High Performance",
                width="80px",
                height="80px",
                style={
                    "margin-bottom": "20px",
                    "filter": "drop-shadow(0 0 10px rgba(162, 255, 226, 0.3))",
                    "transition": "all 0.3s ease"
                }
            ),
            Text(
                text="High Performance",
                style={
                    "font-size": "24px",
                    "font-weight": "700",
                    "color": "#a2ffe2",
                    "margin-bottom": "12px"
                }
            ),
            Text(
                text="Optimized rendering and efficient resource management for smooth experiences.",
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
        id="feature-card-2",
        style={
            "background": "rgba(20, 30, 27, 0.6)",
            "border": "1px solid rgba(100,255,200,0.1)",
            "border-radius": "16px",
            "backdrop-filter": "blur(12px)",
            "box-shadow": "0 8px 32px rgba(0,0,0,0.2)",
            "opacity": "0",
            "transform": "translateY(40px) rotateX(10deg)",
            "transition": "all 0.6s ease 0.2s"
        }
    )

    feature_card_3 = Container(
        Container(
            Image(
                src="tools.svg",
                alt="Easy to Use",
                width="80px",
                height="80px",
                style={
                    "margin-bottom": "20px",
                    "filter": "drop-shadow(0 0 10px rgba(162, 255, 226, 0.3))",
                    "transition": "all 0.3s ease"
                }
            ),
            Text(
                text="Easy to Use",
                style={
                    "font-size": "24px",
                    "font-weight": "700",
                    "color": "#a2ffe2",
                    "margin-bottom": "12px"
                }
            ),
            Text(
                text="Declarative syntax and comprehensive documentation to get you started fast with an built in state managment for your UI components.",
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
        id="feature-card-3",
        style={
            "background": "rgba(20, 30, 27, 0.6)",
            "border": "1px solid rgba(100,255,200,0.1)",
            "border-radius": "16px",
            "backdrop-filter": "blur(12px)",
            "box-shadow": "0 8px 32px rgba(0,0,0,0.2)",
            "opacity": "0",
            "transform": "translateY(40px) rotateX(10deg)",
            "transition": "all 0.6s ease 0.3s"
        }
    )

    feature_card_4 = Container(
        Container(
            Image(
                src="palette.svg",
                alt="Modern UI",
                width="80px",
                height="80px",
                style={
                    "margin-bottom": "20px",
                    "filter": "drop-shadow(0 0 10px rgba(162, 255, 226, 0.3))",
                    "transition": "all 0.3s ease"
                }
            ),
            Text(
                text="Modern UI",
                style={
                    "font-size": "24px",
                    "font-weight": "700",
                    "color": "#a2ffe2",
                    "margin-bottom": "12px"
                }
            ),
            Text(
                text="Beautiful, responsive components that follow modern design principles with standard CSS styles.",
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
        id="feature-card-4",
        style={
            "background": "rgba(20, 30, 27, 0.6)",
            "border": "1px solid rgba(100,255,200,0.1)",
            "border-radius": "16px",
            "backdrop-filter": "blur(12px)",
            "box-shadow": "0 8px 32px rgba(0,0,0,0.2)",
            "opacity": "0",
            "transform": "translateY(40px) rotateX(10deg)",
            "transition": "all 0.6s ease 0.4s"
        }
    )

    feature_card_5 = Container(
        Container(
            Image(
                src="puzzle.svg",
                alt="Extensible",
                width="80px",
                height="80px",
                style={
                    "margin-bottom": "20px",
                    "filter": "drop-shadow(0 0 10px rgba(162, 255, 226, 0.3))",
                    "transition": "all 0.3s ease"
                }
            ),
            Text(
                text="Extensible",
                style={
                    "font-size": "24px",
                    "font-weight": "700",
                    "color": "#a2ffe2",
                    "margin-bottom": "12px"
                }
            ),
            Text(
                text="Flexible and easy to use for various types of applications.",
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
        id="feature-card-5",
        style={
            "background": "rgba(20, 30, 27, 0.6)",
            "border": "1px solid rgba(100,255,200,0.1)",
            "border-radius": "16px",
            "backdrop-filter": "blur(12px)",
            "box-shadow": "0 8px 32px rgba(0,0,0,0.2)",
            "opacity": "0",
            "transform": "translateY(40px) rotateX(10deg)",
            "transition": "all 0.6s ease 0.5s"
        }
    )

    return Container(
        Text(
            text="Features",
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
            text="Everything you need to build amazing applications",
            style={
                "font-size": "20px",
                "color": "#a0cfc0",
                "text-align": "center",
                "margin-bottom": "60px",
                "max-width": "600px",
                "margin-left": "auto",
                "margin-right": "auto"
            }
        ),
        Container(
            feature_card_0,
            feature_card_1,
            feature_card_2,
            feature_card_3,
            feature_card_4,
            feature_card_5,
            style={
                "display": "grid",
                "grid-template-columns": "repeat(auto-fit, minmax(350px, 1fr))",
                "gap": "30px",
                "max-width": "1200px",
                "margin": "0 auto",
                "padding": "0 20px"
            }
        ),
        id="features-section",
        style={
            "padding": "50px 40px",
            "background": "linear-gradient(135deg, #0a1512 0%, #0f1e1a 100%)",
            "min-height": "100vh",
            "display": "flex",
            "flex-direction": "column",
            "justify-content": "flex-start"
        }
    )
