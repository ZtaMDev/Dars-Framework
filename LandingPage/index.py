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
    keywords=["framework","python","python framework", "dars","dars framework", "ui components", "declarative UI"]
)

index = Page(
    create_navbar(),
    create_hero(),
    create_features(),
    create_howitworks(),
    create_footer()
)
app.add_global_style(file_path="index.css")
app.add_script(dScript(file_path="script.js"))
app.add_page("index", index, title="Dars Framework", index=True)
app.add_page("docs", docs, title="Dars Docs")
app.add_page("releases", releases, title="Dars Versions")
 
if __name__ == "__main__":
    app.rTimeCompile(add_file_types=".py, .js, .css, .md, .svg")