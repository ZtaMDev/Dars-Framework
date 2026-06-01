from dars.all import *


@route("/about", route_type=RouteType.PRIVATE)
def about():
    show_loading = setVRef(True, ".show-loading")
    show_content = setVRef(False, ".show-content")
    username_sel = ".user-name"

    # ── Session Check ──────────────────────────────────────────────────
    on_me_success = runSequence(
        updateVRef(".show-loading", False),
        updateVRef(".show-content", True),
        updateVRefFromResponse(username_sel, key="response.user.username"),
    )
    on_me_error = runSequence(
        updateVRef(".show-loading", False),
    )

    fetch_me, *_ = useFetch(
        "/_dars/auth/me", method="GET", on_success=on_me_success, on_error=on_me_error
    )

    # ── Logout ─────────────────────────────────────────────────────────
    on_logout_success = runSequence(
        updateVRef(".show-content", False),
        updateVRef(".show-loading", True),
        updateVRef(username_sel, ""),
        navigate_to("/login"),
    )

    fetch_logout, *_ = useFetch(
        "/_dars/auth/logout", method="POST", on_success=on_logout_success
    )

    page = Page(
        Container(
            Head("About - PRIVATE Route"),
            Show(
                show_loading,
                Container(Text("Checking session..."), style="padding: 20px;"),
            ),
            Show(
                show_content,
                Container(
                    Text(
                        "Welcome to the Private About Page!",
                        style="font-size: 22px; font-weight: bold; margin-bottom: 10px; color: #10b981;",
                    ),
                    Container(
                        Text("Logged in as: ", style="font-weight: 500;"),
                        Text("", class_name=username_sel.replace(".", "")),
                        style="display: flex; gap: 8px; margin-bottom: 15px;",
                    ),
                    Button(
                        "Logout",
                        on_click=fetch_logout,
                        style="padding: 10px; background: #ef4444; color: white; border: none; border-radius: 4px; cursor: pointer;",
                    ),
                    style="display: flex; flex-direction: column; width: 300px; padding: 20px; border: 1px solid #eee; border-radius: 8px; box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);",
                ),
            ),
            style="display: flex; justify-content: center; align-items: center; height: 100vh; font-family: system-ui, sans-serif; background-color: #f0fdf4;",
        )
    )
    page.add_script(fetch_me)
    return page
