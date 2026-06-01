from dars.all import *

@route("/login")
def login():
    # ── VRefs ──────────────────────────────────────────────────────────
    show_loading = setVRef(True,  ".login-loading")
    show_form    = setVRef(False, ".login-form")
    error_sel    = ".login-error"

    # ── Session Check ──────────────────────────────────────────────────
    on_me_success = runSequence(
        updateVRef(".login-loading", False),
        redirect_after_login(),
    )
    on_me_error = runSequence(
        updateVRef(".login-loading", False),
        updateVRef(".login-form", True),
    )

    fetch_me, *_ = useFetch(
        "/_dars/auth/me",
        method="GET",
        on_success=on_me_success,
        on_error=on_me_error,
    )

    # ── Login Form ─────────────────────────────────────────────────────
    login_form = collect_form(username=V("#login-user"), password=V("#login-pass"))
    validator = FormValidator({
        "username": [required()],
        "password": [required()],
    })

    on_login_success = runSequence(
        updateVRef(error_sel, ""),
        updateVRef(".login-form", False),
        updateVRef(".login-loading", True),
        redirect_after_login(),
    )
    on_login_error = runSequence(
        updateVRefFromResponse(error_sel, key="response.detail"),
    )

    submit_login = validator.validated_submit(
        url="/_dars/auth/login",
        form_data=login_form,
        on_success=on_login_success,
        on_error=on_login_error,
    )

    page = Page(
        Container(
            Head("Login - Dars"),

            # Loading
            Show(show_loading, Container(
                Spinner(),
                Text("Checking session...", style="margin-left: 8px;"),
                style="display: flex; align-items: center; justify-content: center; padding: 40px;",
            )),

            # Login form
            Show(show_form, Container(
                Text("Login", style="font-size: 24px; font-weight: bold; margin-bottom: 8px; text-align: center;"),
                Text("Use admin / 1234", style="font-size: 14px; color: #6b7280; margin-bottom: 20px; text-align: center;"),
                Input(id="login-user", placeholder="Username",
                      style="padding: 10px; margin-bottom: 10px; border: 1px solid #d1d5db; border-radius: 6px; width: 100%; box-sizing: border-box;"),
                Input(id="login-pass", placeholder="Password", type="password",
                      style="padding: 10px; margin-bottom: 10px; border: 1px solid #d1d5db; border-radius: 6px; width: 100%; box-sizing: border-box;"),
                Text("", class_name="login-error", style="color: #dc2626; font-size: 14px; margin-bottom: 10px;"),
                Button("Login", on_click=submit_login,
                       style="padding: 10px; background: #4f46e5; color: white; border: none; border-radius: 6px; cursor: pointer; width: 100%; font-weight: 500;"),
                style="width: 320px; padding: 24px; border: 1px solid #e5e7eb; border-radius: 12px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); background: white;",
            ), style="display: flex; justify-content: center; align-items: center; min-height: 60vh;"),

            style="display: flex; justify-content: center; align-items: center; min-height: 100vh; font-family: system-ui, sans-serif; background: #f3f4f6;",
        )
    )

    page.add_script(fetch_me)
    return page
