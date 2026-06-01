from documentation.documentation import docs
from featurescomp import create_example, create_features
from footercomp import create_footer
from herocomp import create_hero
from howitworkscomp import create_howitworks
from navbarcomp import create_navbar
from releases.releases import releases
from roadmap.roadmap import roadmap

from dars.all import *

app = App(
    title="Dars Framework",
    language="en",
    favicon="Dars-logo.png",
    apple_touch_icon="Dars-logo.png",
    author="ZMDev",
    description="Dars framework landing page for the UI Fullstack multiplatform python framework",
    theme_color="#0d1513",
    theme="dark",
    background_color="#0d1513",
    apple_mobile_web_app_capable=True,
    apple_mobile_web_app_status_bar_style="black-translucent",
    apple_mobile_web_app_title="Dars Framework",
    keywords=[
        "framework",
        "python",
        "python framework",
        "dars",
        "dars framework",
        "ui components",
        "declarative UI",
    ],
)
index = Page(
    create_navbar(),
    create_hero(),
    create_example(),
    create_features(),
    create_howitworks(),
    create_footer(),
    style="bg-[#0d1513]",
)
app.add_global_style(file_path="index.css")
app.add_script(dScript(file_path="script.js"))

# Hero entrance animations (sequential on load)
index.add_script(
    setTimeout(5, addClass("hero-logo", "show"))
    .then(setTimeout(350, addClass("hero-title", "show")))
    .then(setTimeout(650, addClass("hero-description", "show")))
    .then(setTimeout(950, addClass("pip-command", "show")))
    .then(setTimeout(1250, addClass("get-started-btn", "show")))
)

index.add_script(
    animateOnView(
        "example-title",
        [
            {"opacity": "0", "transform": "translateY(40px)"},
            {"opacity": "1", "transform": "translateY(0)"},
        ],
        duration=800,
        easing="cubic-bezier(0.16, 1, 0.3, 1)",
    )
)

index.add_script(
    animateOnView(
        "example-subtitle",
        [
            {"opacity": "0", "transform": "translateY(30px)"},
            {"opacity": "1", "transform": "translateY(0)"},
        ],
        duration=800,
        easing="cubic-bezier(0.16, 1, 0.3, 1)",
        threshold=0.2,
    )
)

index.add_script(
    animateOnView(
        "code-showcase",
        [
            {"opacity": "0", "transform": "translateY(50px) scale(0.97)"},
            {"opacity": "1", "transform": "translateY(0) scale(1)"},
        ],
        duration=1000,
        easing="cubic-bezier(0.16, 1, 0.3, 1)",
        threshold=0.1,
    )
)

index.add_script(
    staggerOnView(
        ["feature-card-0", "feature-card-1", "feature-card-2"],
        [
            {"opacity": "0", "transform": "translateY(50px) rotateX(10deg)"},
            {"opacity": "1", "transform": "translateY(0) rotateX(0deg)"},
        ],
        duration=800,
        stagger_delay=150,
        easing="cubic-bezier(0.16, 1, 0.3, 1)",
        threshold=0.15,
    )
)

index.add_script(
    staggerOnView(
        ["howitworks-step-1", "howitworks-step-2", "howitworks-step-3"],
        [
            {"opacity": "0", "transform": "translateY(40px) scale(0.95)"},
            {"opacity": "1", "transform": "translateY(0) scale(1)"},
        ],
        duration=700,
        stagger_delay=180,
        easing="cubic-bezier(0.16, 1, 0.3, 1)",
        threshold=0.1,
    )
)

# Pages
app.add_page("index", index, title="Dars Framework", index=True)
app.add_page("docs", docs, title="Dars Docs")
app.add_page("releases", releases, title="Dars Versions")
app.add_page("roadmap", roadmap, title="Dars Roadmap")

if __name__ == "__main__":
    app.rTimeCompile(add_file_types=".py, .js, .css, .md, .svg, .png")
