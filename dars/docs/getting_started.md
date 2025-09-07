The documentstion of dars is moving to the documentation official website please visit https://ztamdev.github.io/Dars-Framework/documentation.html because this documents will be deprecated in some time...
# Getting Started with Dars

Welcome to Dars, a modern Python framework for building web applications with reusable UI components.

## Quick Start

1. **Install Dars**  
   See [INSTALL.md](../../INSTALL.md) for installation instructions.

2. **Project Structure**  
   Learn about the framework internal project layout in [STRUCTURE.md](../../STRUCTURE.md).

3. **Explore Components**  
   Discover all available UI components in [components.md](components.md).

4. **Command-Line Usage**  
   Find CLI commands, options, and workflows in [cli.md](cli.md).

5. **App Class**
   Learn how to create an app class in [App Documentation](app.md).

6. **Component Search and Modification**
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

### Project Structure  
   Learn about the recommended project layout in [STRUCTURE.md](../../STRUCTURE.md).

### Explore Components  
   Discover all available UI components in [components.md](components.md).

### Command-Line Usage  
   Find CLI commands, options, and workflows in [cli.md](cli.md).

### Need More Help?
- For advanced topics, see the full documentation and examples in the referenced files above.
- If you have questions or need support, check the official repository or community channels.

Start building with Dars...
