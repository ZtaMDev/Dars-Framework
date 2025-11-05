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

   app = App(title="Search Demo")

   # Create a page with nested components
   page = Page(
       Container(
           Text(text="Welcome!", id="welcome-text"),
           Container(
               Button(text="Click me", class_name="action-btn"),
               Button(text="Cancel", class_name="action-btn"),
               id="buttons-container"
           ),
           id="main-container"
       )
   )

   # Find and modify components
   page.find(id="welcome-text")\
       .attr(text="Welcome to Dars!", style={"color": "blue"})

   # Chain searches to find nested components
   page.find(id="buttons-container")\
       .find(class_name="action-btn")\
       .attr(style={"padding": "10px"})

   app.add_page(name="main", root=page)

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
