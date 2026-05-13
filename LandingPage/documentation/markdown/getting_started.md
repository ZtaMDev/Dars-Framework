# Getting Started with Dars

Welcome to Dars, a modern Python framework for building web applications with reusable UI components.

## VS Code Extension

There is an official **Dars Framework** extension for VS Code to have the dars dev tools.

- **VS Code Marketplace**: https://marketplace.visualstudio.com/items?itemName=ZtaMDev.dars-framework
- **Open VSX**: https://open-vsx.org/extension/ztamdev/dars-framework

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
state = State("app", title_val="Simple Counter", count=0)

# 2. Define Route
@route("/")
def index():
    return Page(
        # 3. Use useValue for app text
        Text(
            text=useValue("app.title_val"),
            style="fs-[33px] text-black font-bold mb-[5x] ",
        ),

        # 4. Display reactive count
        Text(
            text=useDynamic("app.count"),
            style="fs-[48px] mt-5 mb-[12px]"
        ),
        # 5. Interactive Button
        Button(
            text="+1",
            on_click=(
                state.count.increment(1)
            ),
            style="bg-[#3498db] text-white p-[15px] px-[30px] rounded-[8px] border-none cursor-pointer fs-[18px]",
        ),

        # 6. Interactive Button
        Button(
            text="-1",
            on_click=(
                state.count.decrement(1)
            ),
            style="bg-[#3498db] text-white p-[15px] px-[30px] rounded-[8px] border-none cursor-pointer fs-[18px] mt-[5px]",
        ),
        # 7. Interactive Button
        Button(
            text="Reset",
            on_click=(
                state.reset()
            ),
            style="bg-[#3498db] text-white p-[15px] px-[30px] rounded-[8px] border-none cursor-pointer fs-[18px] mt-[5px]",
        ),
        style="flex flex-col items-center justify-center h-[100vh] ffam-[Arial] bg-[#f0f2f5]",

    )

# 8. Add page
app.add_page("index", index(), title="index")

if __name__ == "__main__":
    app.rTimeCompile(add_file_types=".js,.css")

```

- Include any extension your project uses beyond default Python files.

## Need More Help?

- For advanced topics, see the full documentation and examples in the referenced files above.
- If you have questions or need support, check the official repository or community channels.

Start building with Dars...
