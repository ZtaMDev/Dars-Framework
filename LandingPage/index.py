# Dars Framework - Core Source File
#
# This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0.
# If a copy of the MPL was not distributed with this file, You can obtain one at
# https://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2025 ZtaDev
from dars.all import *
from herocomp import create_hero
from featurescomp import create_features
from navbarcomp import create_navbar
from howitworkscomp import create_howitworks
from footercomp import create_footer
from documentation.documentation import docs
from releases.releases import releases
app = App(
    title="Dars Framework",
    language="en",
    favicon="Dars-logo.png",
    apple_touch_icon="Dars-logo.png",
    author="ZMDev",
    description="Dars framework landing page for the UI multiplatform python framework",
    theme_color="#0d1513",
    background_color="#0d1513",
    apple_mobile_web_app_capable=True,
    apple_mobile_web_app_status_bar_style="black-translucent",
    apple_mobile_web_app_title="Dars Framework",
    keywords=["framework","python","python framework", "dars","dars framework", "ui components", "declarative UI"]
)

index = Page(
    create_navbar(),
    create_hero(),
    create_features(),
    create_howitworks(),
    create_footer(),
)
app.set_theme("dark")
app.add_global_style(file_path="index.css")
app.add_script(dScript(file_path="script.js"))
app.add_page("index", index, title="Dars Framework", index=True)
app.add_page("docs", docs, title="Dars Docs")
app.add_page("releases", releases, title="Dars Versions")
if __name__ == "__main__":
    app.rTimeCompile(add_file_types=".py, .js, .css, .md, .svg, .png")