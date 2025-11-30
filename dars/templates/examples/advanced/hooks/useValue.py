from dars.all import *

app = App("useValue & Pythonic Helpers Demo")

# Create state
form_state = State(
    "form",
    firstname="John",
    lastname="Doe",
    age=25,
    bio="Python developer",
    theme="light",
    api_url="https://api.example.com",
    user_id=123
)

@FunctionComponent
def ValueCard(title, **props):
    return f'''
    <div {Props.id} {Props.class_name} {Props.style}>
        <h3 style="margin-top: 0; color: #333;">{title}</h3>
        {Props.children}
    </div>
    '''

@route("/")
def index():
    page = Page(
        Container(
            Text("useValue & Pythonic Helpers", style={"font-size": "28px", "font-weight": "bold", "margin-bottom": "30px"}),
            
            # Section 1: Basic useValue (Initial Values)
            ValueCard(
                title="1. Basic useValue (Initial Values)",
                children=Container(
                    Text("These inputs are initialized from state and are reactive bindings. You can edit them freely.", style={"margin-bottom": "10px", "color": "#666"}),
                    Container(
                        Text("First Name:", style={"font-weight": "bold"}),
                        Input(id="first", value=useDynamic("form.firstname"), placeholder="First Name"),
                        style={"margin-bottom": "10px"}
                    ),
                    Container(
                        Text("Last Name:", style={"font-weight": "bold"}),
                        Input(id="last", value=useDynamic("form.lastname"), placeholder="Last Name"),
                        style={"margin-bottom": "10px"}
                    ),
                    Container(
                        Text("Age:", style={"font-weight": "bold"}),
                        Input(id="age", value=useDynamic("form.age"), type="number"),
                        style={"margin-bottom": "10px"}
                    )
                )
            ),
            
            # Section 2: V() Helper & Concatenation
            ValueCard(
                title="2. V() Helper & Concatenation",
                children=Container(
                    Text("Combine values using Python syntax (V() + string + V()). No RawJS needed!", style={"margin-bottom": "10px", "color": "#666"}),
                    Container(
                        Button(
                            "Combine Names", 
                            on_click=form_state.bio.set(
                                V("#first") + " " + V("#last")
                            ),
                            style={"margin-right": "10px"}
                        ),
                        Button(
                            "Greeting", 
                            on_click=form_state.bio.set(
                                "Hello, " + V("#first") + "!"
                            )
                        ),
                        style={"margin-bottom": "15px"}
                    ),
                    Text("Result (Bio):", style={"font-weight": "bold"}),
                    Text(text=useDynamic("form.bio"), style={"padding": "10px", "background": "#f5f5f5", "border-radius": "4px"})
                )
            ),
            
            # Section 3: Transformations
            ValueCard(
                title="3. Pythonic Transformations",
                children=Container(
                    Text("Apply transformations directly in Python: .upper(), .lower(), .int(), .float()", style={"margin-bottom": "10px", "color": "#666"}),
                    Container(
                        Button(
                            "UPPERCASE First Name", 
                            on_click=form_state.firstname.set(V("#first").upper()),
                            style={"margin-right": "10px"}
                        ),
                        Button(
                            "lowercase Last Name", 
                            on_click=form_state.lastname.set(V("#last").lower()),
                            style={"margin-right": "10px"}
                        ),
                        Button(
                            "Add 10 Years", 
                            on_click=form_state.age.set(V("#age").int() + 10)
                        ),
                        style={"margin-bottom": "10px"}
                    )
                )
            ),
            
            # Section 4: URL Builder
            ValueCard(
                title="4. URL Builder",
                children=Container(
                    Text("Construct dynamic URLs easily with url() helper.", style={"margin-bottom": "10px", "color": "#666"}),
                    Container(
                        Text("API URL:", style={"font-weight": "bold"}),
                        Input(id="api_base", value=useDynamic("form.api_url")),
                        style={"margin-bottom": "10px"}
                    ),
                    Container(
                        Text("User ID:", style={"font-weight": "bold"}),
                        Input(id="uid", value=useDynamic("form.user_id")),
                        style={"margin-bottom": "10px"}
                    ),
                    Button(
                        "Generate Endpoint", 
                        on_click=form_state.bio.set(
                            url("{base}/users/{id}/profile", base=V("#api_base"), id=V("#uid"))
                        )
                    )
                )
            ),
            
            # Section 5: Custom Transformations
            ValueCard(
                title="5. Custom Transformations",
                children=Container(
                    Text("Use transform() for custom JavaScript logic.", style={"margin-bottom": "10px", "color": "#666"}),
                    Button(
                        "Reverse First Name", 
                        on_click=form_state.firstname.set(
                            transform("#first", "value.split('').reverse().join('')")
                        )
                    )
                )
            ),
            
            # Section 6: FunctionComponent Support
            ValueCard(
                title="6. FunctionComponent Support",
                children=Container(
                    Text("useValue works directly in templates to render initial values.", style={"margin-bottom": "10px", "color": "#666"}),
                    Container(
                        Text(f"Initial Name: {useValue('form.firstname')} {useValue('form.lastname')}", style={"font-weight": "bold", "color": "blue"}),
                        Text(f"Initial Bio: {useValue('form.bio')}", style={"font-style": "italic"}),
                        style={"padding": "10px", "background": "#eef", "border-radius": "4px"}
                    )
                )
            ),
            
            style={"max-width": "800px", "margin": "0 auto", "font-family": "Arial, sans-serif", "background": "#f9f9f9", "padding": "20px"}
        )
    )
    
    return page

app.add_page("index", index())

if __name__ == "__main__":
    app.rTimeCompile(port=8002)
