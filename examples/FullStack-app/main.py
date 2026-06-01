# pyrefly: ignore [missing-import]
from pages.about import about
from pages.login import login
from pages.products import products

# pyrefly: ignore [missing-import]
from pages.tasklist import tasklist

from dars.all import *

# !IMPORTANT: For this project you need the v1.9.16 of dars

app = App(title="Static App", theme="dark")


# Setup centralized auth (admin/1234)
# Setup Dars Auth
def verify_user(username, password):
    if username == "admin" and password == "1234":
        return {"id": "1", "username": "admin", "role": "admin"}
    return None


app.setup_auth(
    verify_credentials_callback=verify_user,
    secret="super_secret_test_key_123",
    login_page="/login",
)

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
app.add_page("index", index, title="Home", route="/")
app.add_page("about", about())
app.add_page("tasklist", tasklist())
app.add_page("products", products())
app.add_page("login", login())

# 3. Run app
if __name__ == "__main__":
    app.rTimeCompile()
