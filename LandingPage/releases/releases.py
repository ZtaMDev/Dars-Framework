# Dars Framework - Core Source File
#
# This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0.
# If a copy of the MPL was not distributed with this file, You can obtain one at
# https://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2025 ZtaDev
from dars.all import *
from navbarcomp import create_navbar
from footercomp import create_footer
from releases.sidebarcomp import create_sidebar_releases
releases = Page(
    create_navbar(),
    Container(
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