from dars.all import *
from dars.hooks.use_watch import useWatch

app = App("Surgical useDynamic Test")

user_state = State("user", name="John Doe", bio="Software Developer", status="Active")

app.useWatch("user.name", log("Name changed (app.useWatch)!"))
app.add_script(useWatch("user.bio", log("Bio changed (app.add_script)!")))

@FunctionComponent
def WatcherComp(**props):
    return f'''
    <div {Props.id} {Props.class_name} {Props.style}>
        <p>Watchers active! Check console for logs.</p>
    </div>
    '''

@route("/")
def index():
    page = Page(
        Container(
            Text("Surgical useDynamic Test", style={"font-size": "24px", "margin-bottom": "20px"}),
            
            # 1. Text Component Binding
            Container(
                Text("Text Component: ", style={"font-weight": "bold"}),
                Text(text=useDynamic("user.name"), style={"color": "blue"}),
                style={"margin-bottom": "10px"}
            ),
            
            # 2. Input Binding (Value)
            Container(
                Text("Input (Value):", style={"font-weight": "bold"}),
                Input(value=useDynamic("user.name"), placeholder="Type name..."),
                style={"margin-bottom": "10px"}
            ),
            
            # 3. Button Binding (Text)
            Container(
                Text("Button (Text): ", style={"font-weight": "bold"}),
                Button(text=useDynamic("user.status")),
                style={"margin-bottom": "10px", "display": "flex", "align-items": "center", "gap": "10px"}
            ),
            
            # 4. Textarea Binding (Value)
            Container(
                Text("Textarea (Value):", style={"font-weight": "bold"}),
                Textarea(value=useDynamic("user.bio"), rows=3),
                style={"margin-bottom": "20px"}
            ),
            
            WatcherComp(),

            Container(
                    Button("Update Name", on_click=user_state.name.set("Updated Name")),
                    Button("Update Bio", on_click=user_state.bio.set("Updated Bio Content")),
                    Button("Update Status", on_click=user_state.status.set("Inactive")),
                    Button("Reset", on_click=user_state.reset()),
                style={"margin-top": "20px", "display": "flex", "gap": "10px"}
            ),
        ),
        style={"padding": "20px", "font-family": "Arial"}
    )
    
    page.useWatch("user.status", log("Status changed (page.useWatch)!"))
    
    return page

app.add_page("index", index())

if __name__ == "__main__":
    app.rTimeCompile()
