from dars.all import *
# pyrefly: ignore [missing-import]
from pages.about import about
# pyrefly: ignore [missing-import]
from pages.tasklist import tasklist, verify_user
# pyrefly: ignore [missing-import]
from pages.auth import auth

app = App(title="Static App", theme="dark")
# Setup dars auth(route protection for now only one for app in text updates will be a lot better)
# In the next commits i will include an ID parameter to have more than 1 per app, and also route.setup_auth() to not use app.setup_auth() globaly
app.setup_auth(verify_credentials_callback=verify_user, secret="super_secret_test_key_123")

# 1. Define Page
index = Page(
    Container(
        Text(
            text="Welcome to Dars Static",
            style="fs-[42px] font-bold mb-[10px]",
        ),
        Text(
            text="This is a standard multipage static-style project.",
            style="fs-[18px] text-gray-500",
        ),
        style="flex flex-col items-center justify-center h-[100vh] ffam-[Arial] bg-[#f0f2f5]",
    )
)

# 2. Add Page
app.add_page("index", index, title="Home")
app.add_page('about', about())
app.add_page('tasklist', tasklist())
app.add_page('auth', auth())

# 3. Run app
if __name__ == "__main__":
    app.rTimeCompile()