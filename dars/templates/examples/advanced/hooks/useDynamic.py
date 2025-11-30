from dars.all import *

app = App("useDynamic Comprehensive Test")

# Create state with all test properties
ui_state = State(
    "ui",
    # Text properties
    title="Dynamic Title",
    subtitle="Dynamic Subtitle",
    
    # Input properties
    username="",
    email="",
    message="",
    search_hint="Type to search...",
    
    # Button properties
    button_label="Click Me",
    is_disabled=False,
    
    # Image properties
    image_url="https://placehold.co/600x400",
    image_alt="Placeholder Image",
    
    # Link properties
    link_url="https://example.com",
    link_text="Visit Example",
    
    # Checkbox properties
    is_checked=False,
    checkbox_disabled=False,
    
    # Select properties
    selected_option="option1"
)

@FunctionComponent
def DynamicCard(**props):
    """Example of useDynamic in FunctionComponent"""
    return f'''
    <div {Props.id} {Props.class_name} {Props.style}>
        <h3>{useDynamic("ui.title")}</h3>
        <p>{useDynamic("ui.subtitle")}</p>
    </div>
    '''

@route("/")
def index():
    page = Page(
        Container(
            Text("useDynamic Comprehensive Test", style={"font-size": "28px", "margin-bottom": "30px", "font-weight": "bold"}),
            
            # Section 1: Text Component
            Section(
                Text("1. Text Component", style={"font-size": "20px", "font-weight": "bold", "margin-bottom": "10px"}),
                Container(
                    Text("Title: ", style={"font-weight": "bold"}),
                    Text(text=useDynamic("ui.title"), style={"color": "blue"}),
                    style={"margin-bottom": "10px"}
                ),
                Container(
                    Text("Subtitle: ", style={"font-weight": "bold"}),
                    Text(text=useDynamic("ui.subtitle"), style={"color": "green"}),
                    style={"margin-bottom": "10px"}
                ),
                style={"margin-bottom": "30px", "padding": "15px", "border": "1px solid #ddd", "border-radius": "5px"}
            ),
            
            # Section 2: Input Component
            Section(
                Text("2. Input Component", style={"font-size": "20px", "font-weight": "bold", "margin-bottom": "10px"}),
                Container(
                    Text("Username (value binding):", style={"font-weight": "bold", "margin-bottom": "5px"}),
                    Input(value=useDynamic("ui.username"), placeholder="Enter username"),
                    style={"margin-bottom": "10px"}
                ),
                Container(
                    Text("Email (value binding):", style={"font-weight": "bold", "margin-bottom": "5px"}),
                    Input(value=useDynamic("ui.email"), placeholder="Enter email"),
                    style={"margin-bottom": "10px"}
                ),
                Container(
                    Text("Search (placeholder binding):", style={"font-weight": "bold", "margin-bottom": "5px"}),
                    Input(placeholder=useDynamic("ui.search_hint")),
                    style={"margin-bottom": "10px"}
                ),
                style={"margin-bottom": "30px", "padding": "15px", "border": "1px solid #ddd", "border-radius": "5px"}
            ),
            
            # Section 3: Button Component
            Section(
                Text("3. Button Component", style={"font-size": "20px", "font-weight": "bold", "margin-bottom": "10px"}),
                Container(
                    Text("Button (text binding):", style={"font-weight": "bold", "margin-bottom": "5px"}),
                    Button(text=useDynamic("ui.button_label")),
                    style={"margin-bottom": "10px"}
                ),
                Container(
                    Text("Button (disabled binding):", style={"font-weight": "bold", "margin-bottom": "5px"}),
                    Button(text="Test Button", disabled=useDynamic("ui.is_disabled")),
                    style={"margin-bottom": "10px"}
                ),
                style={"margin-bottom": "30px", "padding": "15px", "border": "1px solid #ddd", "border-radius": "5px"}
            ),
            
            # Section 4: Textarea Component
            Section(
                Text("4. Textarea Component", style={"font-size": "20px", "font-weight": "bold", "margin-bottom": "10px"}),
                Container(
                    Text("Message (value binding):", style={"font-weight": "bold", "margin-bottom": "5px"}),
                    Textarea(value=useDynamic("ui.message"), rows=4, placeholder="Enter message"),
                    style={"margin-bottom": "10px"}
                ),
                style={"margin-bottom": "30px", "padding": "15px", "border": "1px solid #ddd", "border-radius": "5px"}
            ),
            
            # Section 5: Image Component
            Section(
                Text("5. Image Component", style={"font-size": "20px", "font-weight": "bold", "margin-bottom": "10px"}),
                Container(
                    Text("Image (src & alt binding):", style={"font-weight": "bold", "margin-bottom": "5px"}),
                    Image(src=useDynamic("ui.image_url"), alt=useDynamic("ui.image_alt"), style={"max-width": "200px"}),
                    style={"margin-bottom": "10px"}
                ),
                style={"margin-bottom": "30px", "padding": "15px", "border": "1px solid #ddd", "border-radius": "5px"}
            ),
            
            # Section 6: Link Component
            Section(
                Text("6. Link Component", style={"font-size": "20px", "font-weight": "bold", "margin-bottom": "10px"}),
                Container(
                    Text("Link (href & text binding):", style={"font-weight": "bold", "margin-bottom": "5px"}),
                    Link(href=useDynamic("ui.link_url"), text=useDynamic("ui.link_text")),
                    style={"margin-bottom": "10px"}
                ),
                style={"margin-bottom": "30px", "padding": "15px", "border": "1px solid #ddd", "border-radius": "5px"}
            ),
            
            # Section 7: Checkbox Component
            Section(
                Text("7. Checkbox Component", style={"font-size": "20px", "font-weight": "bold", "margin-bottom": "10px"}),
                Container(
                    Text("Checkbox (checked binding):", style={"font-weight": "bold", "margin-bottom": "5px"}),
                    Checkbox(checked=useDynamic("ui.is_checked"), label="I agree"),
                    style={"margin-bottom": "10px"}
                ),
                Container(
                    Text("Checkbox (disabled binding):", style={"font-weight": "bold", "margin-bottom": "5px"}),
                    Checkbox(disabled=useDynamic("ui.checkbox_disabled"), label="Disabled checkbox"),
                    style={"margin-bottom": "10px"}
                ),
                style={"margin-bottom": "30px", "padding": "15px", "border": "1px solid #ddd", "border-radius": "5px"}
            ),
            
            # Section 8: FunctionComponent with useDynamic
            Section(
                Text("8. FunctionComponent with useDynamic", style={"font-size": "20px", "font-weight": "bold", "margin-bottom": "10px"}),
                DynamicCard(style={"padding": "10px", "background": "#f0f0f0", "border-radius": "5px"}),
                style={"margin-bottom": "30px", "padding": "15px", "border": "1px solid #ddd", "border-radius": "5px"}
            ),
            
            # Control Panel
            Section(
                Text("Control Panel", style={"font-size": "20px", "font-weight": "bold", "margin-bottom": "10px"}),
                
                # Text controls
                Container(
                    Text("Text Controls:", style={"font-weight": "bold", "margin-bottom": "5px"}),
                    Container(
                        Button("Change Title", on_click=ui_state.title.set("New Title!")),
                        Button("Change Subtitle", on_click=ui_state.subtitle.set("Updated Subtitle")),
                        style={"display": "flex", "gap": "10px", "margin-bottom": "10px"}
                    ),
                ),
                
                # Input controls
                Container(
                    Text("Input Controls:", style={"font-weight": "bold", "margin-bottom": "5px"}),
                    Container(
                        Button("Set Username", on_click=ui_state.username.set("john_doe")),
                        Button("Set Email", on_click=ui_state.email.set("john@example.com")),
                        Button("Change Hint", on_click=ui_state.search_hint.set("Search here...")),
                        style={"display": "flex", "gap": "10px", "margin-bottom": "10px"}
                    ),
                ),
                
                # Button controls
                Container(
                    Text("Button Controls:", style={"font-weight": "bold", "margin-bottom": "5px"}),
                    Container(
                        Button("Change Label", on_click=ui_state.button_label.set("New Label")),
                        Button("Toggle Disabled", on_click=ui_state.is_disabled.set(RawJS("!window.Dars.getState('ui').is_disabled"))),
                        style={"display": "flex", "gap": "10px", "margin-bottom": "10px"}
                    ),
                ),
                
                # Textarea controls
                Container(
                    Text("Textarea Controls:", style={"font-weight": "bold", "margin-bottom": "5px"}),
                    Container(
                        Button("Set Message", on_click=ui_state.message.set("Hello from Dars!")),
                        style={"display": "flex", "gap": "10px", "margin-bottom": "10px"}
                    ),
                ),
                
                # Image controls
                Container(
                    Text("Image Controls:", style={"font-weight": "bold", "margin-bottom": "5px"}),
                    Container(
                        Button("Change Image", on_click=ui_state.image_url.set("https://placehold.co/128x128")),
                        Button("Change Alt", on_click=ui_state.image_alt.set("New Alt Text")),
                        style={"display": "flex", "gap": "10px", "margin-bottom": "10px"}
                    ),
                ),
                
                # Link controls
                Container(
                    Text("Link Controls:", style={"font-weight": "bold", "margin-bottom": "5px"}),
                    Container(
                        Button("Change URL", on_click=ui_state.link_url.set("https://google.com")),
                        Button("Change Text", on_click=ui_state.link_text.set("Visit Google")),
                        style={"display": "flex", "gap": "10px", "margin-bottom": "10px"}
                    ),
                ),
                
                # Checkbox controls
                Container(
                    Text("Checkbox Controls:", style={"font-weight": "bold", "margin-bottom": "5px"}),
                    Container(
                        Button("Toggle Checked", on_click=ui_state.is_checked.set(RawJS("!window.Dars.getState('ui').is_checked"))),
                        Button("Toggle Disabled", on_click=ui_state.checkbox_disabled.set(RawJS("!window.Dars.getState('ui').checkbox_disabled"))),
                        style={"display": "flex", "gap": "10px", "margin-bottom": "10px"}
                    ),
                ),
                
                # Reset
                Container(
                    Button("Reset All", on_click=ui_state.reset(), style={"background": "#ff4444", "color": "white"}),
                    style={"margin-top": "20px"}
                ),
                
                style={"padding": "15px", "border": "2px solid #333", "border-radius": "5px", "background": "#f9f9f9"}
            ),
            
            style={"padding": "20px", "font-family": "Arial, sans-serif", "max-width": "800px", "margin": "0 auto"}
        )
    )
    
    return page

app.add_page("index", index())

if __name__ == "__main__":
    app.rTimeCompile(port=8001)
