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
    theme="dark",
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
    style="bg-[#0d1513]"
)

app.set_theme("dark")
app.add_global_style(file_path="index.css")
app.add_script(dScript(file_path="script.js"))

# Start Animations
index.add_script(
    setTimeout(5, addClass("hero-logo", "show"))
    .then(setTimeout(350, addClass("hero-title", "show")))
    .then(setTimeout(650, addClass("hero-description", "show")))
    .then(setTimeout(950, addClass("pip-command", "show")))
    .then(setTimeout(1250, addClass("get-started-btn", "show")))
)

#Pages
app.add_page("index", index, title="Dars Framework", index=True)
app.add_page("docs", docs, title="Dars Docs")
app.add_page("releases", releases, title="Dars Versions")

if __name__ == "__main__":
    app.rTimeCompile(add_file_types=".py, .js, .css, .md, .svg, .png")