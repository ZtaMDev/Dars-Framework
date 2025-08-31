from dars.core.app import *
from dars.components.basic.container import Container
from dars.components.basic.markdown import Markdown

app = App(title="Component Customasitation")
# From string
markdown_component = Markdown(
    file_path="README.md",
    id="my-markdown",
    class_name="custom-markdown",
    dark_theme=True,
    style={"padding": "20px", "backgroundColor": "#f8f9fa"}
)
Mic = Container(
    markdown_component
)

app.set_root(Mic)

if __name__ == "__main__":
    app.rTimeCompile(add_file_types=".md")