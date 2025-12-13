from dars.all import *
from footercomp import create_footer
from documentation.sidebarcomp import create_sidebar
from navbarcomp import create_navbar

docs = Page(
    create_navbar(),
    create_sidebar(),
    Container(
        Container(
            Markdown(file_path="./documentation/markdown/index.md", class_name="markdown_docs", dark_theme=True, id="md-index"),
            Markdown(file_path="./documentation/markdown/install.md", class_name="markdown_docs", dark_theme=True, id="md-install"),
            Markdown(file_path="./documentation/markdown/getting_started.md", class_name="markdown_docs", dark_theme=True, id="md-getting_started"),
            Markdown(file_path="./documentation/markdown/cli.md", class_name="markdown_docs", dark_theme=True, id="md-cli"),
            Markdown(file_path="./documentation/markdown/config.md", class_name="markdown_docs", dark_theme=True, id="md-config"),
            Markdown(file_path="./documentation/markdown/env.md", class_name="markdown_docs", dark_theme=True, id="md-env"),
            Markdown(file_path="./documentation/markdown/app.md", class_name="markdown_docs", dark_theme=True, id="md-app"),
            Markdown(file_path="./documentation/markdown/components.md", class_name="markdown_docs", dark_theme=True, id="md-components"),
            Markdown(file_path="./documentation/markdown/styling.md", class_name="markdown_docs", dark_theme=True, id="md-styling"),
            Markdown(file_path="./documentation/markdown/custom_components.md", class_name="markdown_docs", dark_theme=True, id="md-custom_components"),
            Markdown(file_path="./documentation/markdown/animations.md", class_name="markdown_docs", dark_theme=True, id="md-animations"),
            Markdown(file_path="./documentation/markdown/routing.md", class_name="markdown_docs", dark_theme=True, id="md-routing"),
            Markdown(file_path="./documentation/markdown/ssr.md", class_name="markdown_docs", dark_theme=True, id="md-ssr"),
            Markdown(file_path="./documentation/markdown/state_management.md", class_name="markdown_docs", dark_theme=True, id="md-state_management"),
            Markdown(file_path="./documentation/markdown/hooks.md", class_name="markdown_docs", dark_theme=True, id="md-hooks"),
            Markdown(file_path="./documentation/markdown/operations.md", class_name="markdown_docs", dark_theme=True, id="md-operations"),
            Markdown(file_path="./documentation/markdown/backend_api.md", class_name="markdown_docs", dark_theme=True, id="md-backend_api"),
            Markdown(file_path="./documentation/markdown/events.md", class_name="markdown_docs", dark_theme=True, id="md-events"),
            Markdown(file_path="./documentation/markdown/KeyEvents.md", class_name="markdown_docs", dark_theme=True, id="md-KeyEvents"),
            Markdown(file_path="./documentation/markdown/exporters.md", class_name="markdown_docs", dark_theme=True, id="md-exporters"),
            Markdown(file_path="./documentation/markdown/scripts.md", class_name="markdown_docs", dark_theme=True, id="md-scripts"),

            id="markdown-content-container",
            style={
                "max-width": "800px",
                "margin": "0 auto",
                "padding": "40px 20px"
            }
        ),
        create_footer(),
        id="markdown-layout",
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