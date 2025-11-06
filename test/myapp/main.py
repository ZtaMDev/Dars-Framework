from dars.all import *
from dars.core.state import dState

app = App(title="Hello World", theme="dark")
cont = Text("0", id="Cont")
# Suppose index is your component instance with a stable id
counter = dState("counter", component=cont, states=[0,1,2])

# Built-in attr-style update
app.add_script(counter.state(1, render=cont.attr(text="f")))
# Crear componentes
index = Page(
    cont,
    Button("Increment", id="Increment", on_click=counter.state(2, cComp=True, render="<span>2</span>")),
    style={
        'display': 'flex',
        'flex-direction': 'column',
        'align-items': 'center',
        'justify-content': 'center',
        'min-height': '100vh',
        'background-color': '#f0f2f5',
        'font-family': 'Arial, sans-serif'
    }
)

app.add_page("index", index, title="Hello World", index=True)

if __name__ == "__main__":
    app.rTimeCompile()