from dars.all import *

app = App("Custom Function Component Example")

@FunctionComponent
def UserCard(name, email, **props):
    return f"""
    <div {Props.id} {Props.class_name} {Props.style}>
        <h3>Name: {useDynamic("userCard.name")}</h3>
        <p>Email: {useDynamic("userCard.email")}</p>
    </div>
    """

@FunctionComponent
def ProfileEditMenu(name, email, **props):
    return f"""
    <div {Props.id} {Props.class_name} {Props.style}>
        <p>Name:</p><input id="username" type="text" value={name}>
        <p>Email:</p><input id="useremail" type="email" value={email}>
    </div>
    """

userCardState = State("userCard", name="John Doe", email="john@example.com")
def EditProfile():
    return Container(
        ProfileEditMenu(name="John Doe", email="john@example.com", id="editProfile", style={"padding": "20px"}),
        Button("Close", on_click=hideModal("editProfile")), 
        Button("Save", on_click=[hideModal("editProfile"), userCardState.name.set(getInputValue("username", "editProfile")), userCardState.email.set(getInputValue("useremail", "editProfile"))]),
    )
        

editProfile = Modal(children=[EditProfile()], 
    title="Edit Profile", 
    open=False, 
    id="editProfile",
    style={"text-align": "center"}
)

@route("/")
def index():
    return Page(
        Section(
            UserCard(name="John Doe", email="john@example.com", id="userCard", style={"padding": "20px"}),
            style={"background-color": "#f0f0f0", "padding": "20px", "border-radius": "10px", "box-shadow": "0 4px 8px rgba(0, 0, 0, 0.1)"}
        ),
        Button(
            "Click Me", 
            on_click=showModal("editProfile"),
            style={"margin-top": "20px", "margin-bottom": "20px", "border-radius": "10px", "box-shadow": "0 4px 8px rgba(0, 0, 0, 0.1)"}
        ),
        editProfile,
        style={"display": "flex", "flex-direction": "column", "align-items": "center", "justify-content": "center", "height": "100vh", "background-color": "grey"},
    )

app.add_page("index", index(), title="Custom Function Component")
if __name__ == "__main__":
    app.rTimeCompile()