from dars.components.advanced.head import Head
from dars.all import *
# pyrefly: ignore [missing-import]
from footercomp import create_footer
# pyrefly: ignore [missing-import]
from documentation.sidebarcomp import create_sidebar
# pyrefly: ignore [missing-import]
from navbarcomp import create_navbar

docs = Page(
    Head(
        title="Documentation - Dars Framework",
        description="Everything you need to build modern apps with Python.",
        keywords=["dars", "framework", "python", "documentation"],
        lang="en"
    ),
    create_navbar(),
    create_sidebar(),
    Container(
        # Hero header for docs
        Container(
            Image(
                src="Dars-logo.png",
                alt="Dars Framework Logo",
                width="56px",
                height="56px",
                style={
                    "filter": "drop-shadow(0 0 16px rgba(146, 255, 229, 0.25))",
                }
            ),
            Container(
                Text(
                    text="Documentation",
                    style={
                        "font-size": "32px",
                        "font-weight": "800",
                        "margin": "0",
                        "background": "linear-gradient(90deg, #92ffe5, #38c49f)",
                        "background-clip": "text",
                        "-webkit-background-clip": "text",
                        "color": "transparent",
                        "letter-spacing": "-0.3px",
                    }
                ),
                Text(
                    text="Everything you need to build modern apps with Python.",
                    style={
                        "font-size": "15px",
                        "color": "rgba(160, 207, 192, 0.7)",
                        "margin": "4px 0 0 0",
                    }
                ),
                style={
                    "display": "flex",
                    "flex-direction": "column",
                }
            ),
            id="docs-hero",
            style={
                "display": "flex",
                "align-items": "center",
                "justify-content": "center",
                "gap": "18px",
                "padding": "28px 32px",
                "border-bottom": "1px solid rgba(146, 255, 229, 0.06)",
            }
        ),
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
            Markdown(file_path="./documentation/markdown/auth.md", class_name="markdown_docs", dark_theme=True, id="md-auth"),
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

docs.add_script(
    dScript(code="""
(function() {
    var layout = document.getElementById('markdown-layout');
    if (!layout) return;

    var style = document.createElement('style');
    style.textContent = `
        /* Enhanced docs tables */
        #markdown-content-container table {
            border-collapse: separate;
            border-spacing: 0;
            border-radius: 8px;
            overflow: hidden;
            border: 1px solid rgba(146, 255, 229, 0.1);
            width: 100%;
            margin: 16px 0;
        }
        #markdown-content-container th {
            background: rgba(16, 185, 129, 0.1) !important;
            border-bottom: 1px solid rgba(146, 255, 229, 0.12) !important;
            padding: 10px 14px !important;
            font-weight: 600;
            text-align: left;
            font-size: 13px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            color: #92ffe5;
        }
        #markdown-content-container td {
            padding: 10px 14px !important;
            border-bottom: 1px solid rgba(255,255,255,0.03) !important;
        }
        #markdown-content-container tr:last-child td {
            border-bottom: none !important;
        }

        /* Blockquote styling */
        #markdown-content-container blockquote {
            border-left: 3px solid #10b981;
            background: rgba(16, 185, 129, 0.06);
            padding: 12px 20px;
            border-radius: 0 8px 8px 0;
            margin: 16px 0;
        }

        /* HR dividers */
        #markdown-content-container hr {
            border: none;
            height: 1px;
            background: linear-gradient(90deg, transparent, rgba(146,255,229,0.12), transparent);
            margin: 32px 0;
        }

        /* Code inline */
        #markdown-content-container code:not(pre code) {
            background: rgba(146, 255, 229, 0.08);
            border: 1px solid rgba(146, 255, 229, 0.1);
            border-radius: 4px;
            padding: 2px 6px;
            font-size: 0.9em;
        }
    `;
    document.head.appendChild(style);
})();
""")
)