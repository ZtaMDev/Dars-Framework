# Getting Started with Dars

Welcome to Dars, a modern Python framework for building web applications with reusable UI components.

## Quick Start

1. **Install Dars**  
   See INSTALL section for installation instructions.

2. **Explore Components**  
   Discover all available UI components in [components.md](#dars-components-documentation).

3. **Command-Line Usage**  
   Find CLI commands, options, and workflows in [cli.md](#dars-cli-reference).

4. **App Class**
   Learn how to create an app class in [App Documentation](#app-class-and-pwa-features-in-dars-framework).

5. **Component Search and Modification**
   All components in Dars now support a powerful search and modification system:

```python

from dars.all import *

app = App(title="Hello World", theme="dark")

# 1. Define State
state = State("app", title="Hello Dars!", count=0)

# 2. Define Route
@route("/")
def index(): 
    return Page(
        Text( # 3. Use useDynamic for reactive updates
            text=useDynamic("app.title"),
            style={
                'font-size': '48px',
                'color': '#2c3e50',
                'font-weight': 'bold',
                'margin-bottom': '20px'
            }
        ),
        
        # 4. Interactive Button
        Button(
            text="Update Title & Count",
            on_click=(
                state.title.set("You clicked the button!")
                .then(state.count.increment(1))
            ),
            style={
                'background-color': '#3498db',
                'color': 'white',
                'padding': '15px 30px',
                'border-radius': '8px',
                'border': 'none',
                'cursor': 'pointer',
                'font-size': '18px'
            }
        ),

        # 5. Display reactive count
        Text(
            text=useDynamic("app.count"),
            style={'font-size': '24px', 'margin-top': '20px'}
        ),

        # 6. useValue for initial value (won't update)
        Text(
            text=useValue("app.title"),
            style={'color': '#95a5a6', 'margin-top': '40px', 'font-style': 'italic'}
        ),

        style={
            'display': 'flex', 'flex-direction': 'column', 
            'align-items': 'center', 'justify-content': 'center', 
            'height': '100vh', 'font-family': 'Arial, sans-serif',
            'background-color': '#f0f2f5'
        }
    ) 

# 7. Add page
app.add_page("index", index(), title="index")

# 8. Run app with preview
if __name__ == "__main__":
    app.rTimeCompile()

```

7.  **Adding Custom File Types**

```python

app.rTimeCompile().add_file_types = ".js,.css"

```

* Include any extension your project uses beyond default Python files.

## Need More Help?

- For advanced topics, see the full documentation and examples in the referenced files above.
- If you have questions or need support, check the official repository or community channels.

Start building with Dars...
