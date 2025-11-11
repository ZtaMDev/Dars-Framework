from dars.all import *

app = App(title="Dars-HealthCheck", theme="dark")
# Crear componentes
container = Container(
    Text(
        text="Dars Health Check",
        style={
            'font-size': '48px',
            'color': '#2c3e50',
            'margin-bottom': '20px',
            'font-weight': 'bold',
            'text-align': 'center'
        }
    ),
    Text(
        text="Dars Health Check",
        style={
            'font-size': '20px',
            'color': '#7f8c8d',
            'margin-bottom': '40px',
            'text-align': 'center'
        }
    ),

    Button(
        text="Check",
        on_click= dScript("""alert('Health Check')"""),
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

app.set_root(container)

if __name__ == "__main__":
    app.rTimeCompile()