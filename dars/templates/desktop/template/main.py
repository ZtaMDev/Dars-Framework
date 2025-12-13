from dars.all import *

app = App(
    title="Dars + Electron",
    description="Build native desktop apps with Python",
    desktop=True,
    icon="icons/icon.png"
)

# Main page with Dars + Electron showcase
index = Page(
    Container(
        # Logo section: Dars + Electron
        FlexLayout(
            children=[
                # Dars logo
                Image(
                    src="icon.png",
                    alt="Dars Framework",
                    width="200px",
                    height="200px",
                    style={
                        'filter': 'drop-shadow(0 4px 12px rgba(162, 255, 226, 0.3))'
                    }
                ),
                # Plus sign
                Text(
                    text="+",
                    style={
                        'font-size': '80px',
                        'font-weight': '300',
                        'color': 'rgba(162, 255, 226, 0.9)',
                        'margin': '0 50px',
                        'line-height': '200px',
                        'text-shadow': '0 0 20px rgba(162, 255, 226, 0.5)'
                    }
                ),
                # Electron logo
                Image(
                    src="electron-icon.png",
                    alt="Electron",
                    width="300px",
                    height="300px",
                    style={
                        'filter': 'drop-shadow(0 4px 12px rgba(162, 255, 226, 0.3))'
                    }
                )
            ],
            direction="row",
            justify="center",
            align="center",
            style={
                'margin-bottom': '40px'
            }
        ),
        
        # Description
        Text(
            text="Dars + Electron for native apps",
            style={
                'font-size': '32px',
                'font-weight': '700',
                'color': '#a2ffe2',
                'text-align': 'center',
                'margin-bottom': '20px',
                'letter-spacing': '0.5px',
                'text-shadow': '0 0 20px rgba(162, 255, 226, 0.4)'
            }
        ),
        
        Text(
            text="Create native desktop apps with Python + Electron backend",
            style={
                'font-size': '18px',
                'color': '#a0cfc0',
                'text-align': 'center',
                'max-width': '500px',
                'margin': '0 auto',
                'line-height': '1.6',
                'text-shadow': '0 0 10px rgba(162, 255, 226, 0.2)'
            }
        ),
        
        style={
            'display': 'flex',
            'flex-direction': 'column',
            'align-items': 'center',
            'justify-content': 'center',
            'min-height': '100vh',
            'padding': '40px 20px',
            'background': 'linear-gradient(135deg, #0f1e1a 0%, #132d24 50%, #0a1512 100%)',
            'font-family': '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif'
        }
    ),
    style={
        'margin': '0',
        'padding': '0'
    }
)

app.add_page("index", index, title="Dars + Electron", index=True)

if __name__ == "__main__":
    app.rTimeCompile()