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


6. **Official Templates**  
   Browse ready-to-use examples in the following files:
   - [Hello World](template_hello_world.md)
   - [Simple Form](template_simple_form.md)
   - [Form Components](template_form_components.md)
   - [Flex Layout Responsive](template_flex_layout_responsive.md)
   - [Grid Layout Responsive](template_grid_layout_responsive.md)
   - [Multipage Example](template_multipage_example.md)
   - [Layout Multipage Demo](template_layout_multipage_demo.md)
   - [PWA Custom Icons](template_pwa_custom_icons.md)
   - [All Components Demo](template_all_components_demo.md)
   - [Dashboard](template_dashboard.md)
   - [Modern Web App](template_modern_web_app.md)
   - [Complete App](template_complete_app.md)

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
