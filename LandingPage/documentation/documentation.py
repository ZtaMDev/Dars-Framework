from dars.all import *
from footercomp import create_footer
from documentation.sidebarcomp import create_sidebar
from navbarcomp import create_navbar

docs = Page(
    create_navbar(),
    create_sidebar(),
    Container(
        Container(
            Markdown(
                file_path="./documentation/markdown/index.md", 
                class_name="markdown_docs", 
                dark_theme=True
            ),
            Markdown(file_path="./documentation/markdown/install.md", class_name="markdown_docs", dark_theme=True),
            Markdown(
                file_path="./documentation/markdown/getting_started.md",
                class_name="markdown_docs",
                dark_theme=True
            ),
            Markdown(file_path="./documentation/markdown/config.md", class_name="markdown_docs", dark_theme=True),
            Markdown(
                file_path="./documentation/markdown/app.md",
                class_name="markdown_docs",
                dark_theme=True
            ),
            Markdown(file_path="./documentation/markdown/routing.md", class_name="markdown_docs", dark_theme=True),
            Markdown(file_path="./documentation/markdown/backend_api.md", class_name="markdown_docs", dark_theme=True),
            Markdown(file_path="./documentation/markdown/state_management.md", class_name="markdown_docs", dark_theme=True),
            Markdown(file_path="./documentation/markdown/components.md", class_name="markdown_docs", dark_theme=True),
            Markdown(file_path="./documentation/markdown/animations.md", class_name="markdown_docs", dark_theme=True),
            Markdown(file_path="./documentation/markdown/custom_components.md", class_name="markdown_docs", dark_theme=True),
            Markdown(file_path="./documentation/markdown/events.md", class_name="markdown_docs", dark_theme=True),
            Markdown(file_path="./documentation/markdown/exporters.md", class_name="markdown_docs", dark_theme=True),
            Markdown(file_path="./documentation/markdown/scripts.md", class_name="markdown_docs", dark_theme=True),
            Markdown(file_path="./documentation/markdown/cli.md", class_name="markdown_docs", dark_theme=True),
            id="markdown-content-container",
            style={
                "max-width": "800px",
                "margin": "0 auto",
                "padding": "40px 20px"
            }
        ),
        create_footer(),
        style={
            "margin-left": "280px",
            "min-height": "100vh",
            "background": "linear-gradient(135deg, #0f1e1a 0%, #132d24 100%)",
            "transition": "margin-left 0.3s ease"
        }
    ),
    style={
        "background": "linear-gradient(135deg, #0f1e1a 0%, #132d24 100%)"
    }
)