from dars.all import *
from navbarcomp import create_navbar
from footercomp import create_footer
from releases.sidebarcomp import create_sidebar_releases

releases = Page(
    create_navbar(),
    Container(
        # Hero header for releases
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
                    text="Release Notes",
                    style={
                        "font-size": "32px",
                        "font-weight": "800",
                        "margin": "0",
                        "background": "linear-gradient(90deg, #7dfdd8, #38c49f, #92ffe5)",
                        "background-clip": "text",
                        "-webkit-background-clip": "text",
                        "color": "transparent",
                        "letter-spacing": "-0.3px",
                    }
                ),
                Text(
                    text="Changelog and version history for Dars Framework.",
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
            id="releases-hero",
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
            Markdown(
                file_path="./releases/versions.md",
                class_name="markdown_docs",
                dark_theme=True
            ),
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
    create_sidebar_releases(),
    style={
        "background": "linear-gradient(135deg, #0f1e1a 0%, #132d24 100%)"
    }
)

releases.add_script(
    dScript(code="""
(function() {
    var container = document.getElementById('markdown-content-container');
    if (!container) return;

    var style = document.createElement('style');
    style.textContent = `
        /* Version badges for h1 headings */
        #markdown-content-container h1 {
            position: relative;
            padding-bottom: 12px;
            margin-top: 48px;
        }
        #markdown-content-container h1::after {
            content: "";
            position: absolute;
            bottom: 0; left: 0;
            width: 60px; height: 3px;
            background: linear-gradient(90deg, #10b981, #059669);
            border-radius: 3px;
        }

        /* Blockquote as version summary */
        #markdown-content-container blockquote {
            border-left: 3px solid #059669;
            background: rgba(16, 185, 129, 0.06);
            padding: 12px 20px;
            border-radius: 0 8px 8px 0;
            margin: 12px 0 20px 0;
            font-style: italic;
        }
        #markdown-content-container blockquote p {
            margin: 0;
            color: #a0cfc0;
        }

        /* Code blocks */
        #markdown-content-container pre {
            border: 1px solid rgba(146, 255, 229, 0.08);
            border-radius: 8px;
        }

        /* Inline code */
        #markdown-content-container code:not(pre code) {
            background: rgba(146, 255, 229, 0.08);
            border: 1px solid rgba(146, 255, 229, 0.1);
            border-radius: 4px;
            padding: 2px 6px;
            font-size: 0.9em;
        }

        /* HR dividers between versions */
        #markdown-content-container hr {
            border: none;
            height: 1px;
            background: linear-gradient(90deg, transparent, rgba(146,255,229,0.15), transparent);
            margin: 40px 0;
        }

        /* H2 section headers */
        #markdown-content-container h2 {
            font-size: 20px;
            color: #92ffe5;
            margin-top: 28px;
        }

        /* H3 feature headers */
        #markdown-content-container h3 {
            position: relative;
            padding-left: 16px;
            margin-top: 24px;
        }
        #markdown-content-container h3::before {
            content: "";
            position: absolute;
            left: 0; top: 4px; bottom: 4px;
            width: 3px;
            background: linear-gradient(180deg, #10b981, #059669);
            border-radius: 3px;
        }
    `;
    document.head.appendChild(style);
})();
""")
)