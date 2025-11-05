from dars.all import *


# Sección "Getting Started"
getting_started_comp = Container(
    Container(
         
        Text("Getting Started with Dars Framework", 
             style={"font-size": "2.5rem", "font-weight": "bold", "color": "#00d68f", "text-align": "center", "margin-bottom": "30px"}),
        
        Text("Welcome to Dars, a modern Python framework for building web applications with reusable UI components.", 
             style={"font-size": "1.2rem", "color": "#b2ffe5", "text-align": "center", "margin-bottom": "50px", "line-height": "1.6"}),
        
        # Quick Start Section - MODIFICADA
        Container(
            Text("Quick Start", 
                 style={"font-size": "2rem", "font-weight": "bold", "color": "#00d68f", "margin-bottom": "25px", "text-align": "center"}),
            
            Container(
                Container(
                    Container(
                        Text("1. Install Dars", 
                             style={"font-size": "1.4rem", "font-weight": "bold", "color": "#00d68f", "margin-bottom": "10px", "text-align": "center"}),
                        Container(
                            Text("Get started by installing the framework", 
                                 style={"color": "#b2ffe5", "margin-bottom": "15px", "line-height": "1.6", "text-align": "center"}),
                            Container(
                                Link("View Installation Instructions", 
                                     href="https://ztamdev.github.io/Dars-Framework/downloads.html", 
                                     style={"color": "#00d68f", "text-decoration": "none", "font-weight": "bold", "display": "inline-block", "padding": "10px 15px", "border": "2px solid #00d68f", "border-radius": "5px"}),
                                style={"text-align": "center"}
                            ),
                            style={"margin-bottom": "30px"}
                        ),
                        
                        Text("2. Explore Components", 
                             style={"font-size": "1.4rem", "font-weight": "bold", "color": "#00d68f", "margin-bottom": "10px", "text-align": "center"}),
                        Container(
                            Text("Discover all available UI components", 
                                 style={"color": "#b2ffe5", "margin-bottom": "15px", "line-height": "1.6", "text-align": "center"}),
                            Container(
                                Link("Browse Components", 
                                     href="https://ztamdev.github.io/Dars-Framework/documentation.html#dars-components-documentation", 
                                     style={"color": "#00d68f", "text-decoration": "none", "font-weight": "bold", "display": "inline-block", "padding": "10px 15px", "border": "2px solid #00d68f", "border-radius": "5px"}),
                                style={"text-align": "center"}
                            ),
                            style={"margin-bottom": "30px"}
                        ),
                        
                        Text("3. Command-Line Usage", 
                             style={"font-size": "1.4rem", "font-weight": "bold", "color": "#00d68f", "margin-bottom": "10px", "text-align": "center"}),
                        Container(
                            Text("Learn CLI commands and workflows", 
                                 style={"color": "#b2ffe5", "margin-bottom": "15px", "line-height": "1.6", "text-align": "center"}),
                            Container(
                                Link("CLI Documentation", 
                                     href="https://ztamdev.github.io/Dars-Framework/documentation.html#dars-cli-reference", 
                                     style={"color": "#00d68f", "text-decoration": "none", "font-weight": "bold", "display": "inline-block", "padding": "10px 15px", "border": "2px solid #00d68f", "border-radius": "5px"}),
                                style={"text-align": "center"}
                            ),
                            style={"margin-bottom": "30px"}
                        ),
                        
                        style={"background-color": "#2a3b2f", "padding": "40px", "border-radius": "10px", "max-width": "800px", "margin": "0 auto"}
                    ),
                    style={"width": "100%", "display": "flex", "justify-content": "center"}
                ),
                style={"width": "100%", "margin-bottom": "40px"}
            ),
            style={"margin-bottom": "50px", "width": "100%","text-align": "center"}
        ),
        
        # Need Help Section
        Container(
            Text("Need More Help?", 
                 style={"font-size": "1.8rem", "font-weight": "bold", "color": "#00d68f", "margin-bottom": "20px", "text-align": "center"}),
            
            Text("For advanced topics and support, check our comprehensive documentation and community resources.", 
                 style={"color": "#b2ffe5", "margin-bottom": "30px", "text-align": "center", "line-height": "1.6"}),
            
            Container(
                Link("Visit GitHub Repository", 
                     href="https://github.com/ZtaMDev/Dars-Framework", 
                     style={"background-color": "#00d68f", "color": "#212529", "padding": "12px 24px", "border-radius": "5px", "text-decoration": "none", "font-weight": "bold", "display": "inline-block"}),
                style={"text-align": "center"}
            ),
            
            style={"text-align": "center", "padding": "40px", "background-color": "#1e2b23", "border-radius": "10px", "border": "2px solid #00d68f", "max-width": "800px", "margin": "0 auto"}
        ),
        
        style={"max-width": "1200px", "margin": "0 auto", "padding": "0 20px", "width": "100%"}
    ),
    style={"padding": "80px 0", "background": "linear-gradient(to bottom, #304635, #212529)", "width": "100%", "text-align": "center"},
    id="getting-started-section"
)