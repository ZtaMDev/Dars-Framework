from dars.all import *

app = App(title="Hello World", theme="dark")
# Crear componentes
index = Page(
    Text(
        text="Hello World",
        style={
            'font-size': '48px',
            'color': '#2c3e50',
            'margin-bottom': '20px',
            'font-weight': 'bold',
            'text-align': 'center'
        }
    ),
    Text(
        text="Hello World",
        style={
            'font-size': '20px',
            'color': '#7f8c8d',
            'margin-bottom': '40px',
            'text-align': 'center'
        }
    ),

    Button(
        text="Click Me!",
        # Modern state updates using this()
        on_click=[this().state(text="Clicked!", style={'background-color': '#27ae60'}), dScript("alert('Hello World!')")],
        # Hover effects using this()
        on_mouse_enter=this().state(style={'background-color': '#2980b9'}),
        on_mouse_leave=this().state(style={'background-color': '#3498db'}),
        style={
            'background-color': '#3498db',
            'color': 'white',
            'padding': '15px 30px',
            'border': 'none',
            'border-radius': '8px',
            'font-size': '18px',
            'cursor': 'pointer',
            'transition': 'background-color 0.3s'
        }
    ),
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
index.attr()
app.add_page("index", index, title="Hello World", index=True)

if __name__ == "__main__":
    app.rTimeCompile()