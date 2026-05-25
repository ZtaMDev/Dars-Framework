from dars.all import *

def verify_user_about(username, password):
    if username == "guest" and password == "guest":
        return {"id": "guest_1", "username": "guest", "role": "guest"}
    return None
# This is apage that requires authentication from the user so it uses the decorator and the backend will call
# the callback to retrive data from python to the client using JSON
@route("/about", route_type=RouteType.SSR)
@requires_auth(verify_credentials_callback=verify_user_about, secret="about_secret_456")
def about():
    # Visibility states
    show_loading = setVRef(True, ".show-loading")
    show_login = setVRef(False, ".show-login")
    show_content = setVRef(False, ".show-content")
    
    error_sel = ".login-error"
    username_sel = ".user-name"
    
    # ── Session Check ──────────────────────────────────────────────────
    on_me_success = runSequence(
        updateVRef(".show-loading", False),
        updateVRef(".show-content", True),
        updateVRefFromResponse(username_sel, key="response.user.username"),
    )
    on_me_error = runSequence(
        updateVRef(".show-loading", False),
        updateVRef(".show-login", True),
    )
    
    fetch_me, *_ = useFetch(
        "/_dars/auth/auth_about/me", 
        method="GET", 
        on_success=on_me_success, 
        on_error=on_me_error
    )
    
    # ── Login Form ─────────────────────────────────────────────────────
    login_form = collect_form(username=V("#about_user"), password=V("#about_pass"))
    validator = FormValidator({
        "username": [required()],
        "password": [required()]
    })
    
    on_login_success = runSequence(
        updateVRef(error_sel, ""),
        updateVRef(".show-login", False),
        updateVRef(".show-content", True),
        updateVRefFromResponse(username_sel, key="response.user.username"),
    )
    
    on_login_error = runSequence(
        updateVRefFromResponse(error_sel, key="response.detail")
    )

    submit_login = validator.validated_submit(
        url="/_dars/auth/auth_about/login",
        form_data=login_form,
        on_success=on_login_success,
        on_error=on_login_error
    )
    
    # ── Logout ─────────────────────────────────────────────────────────
    on_logout_success = runSequence(
        updateVRef(".show-content", False),
        updateVRef(".show-login", True),
        updateVRef(username_sel, "")
    )
    
    fetch_logout, *_ = useFetch(
        "/_dars/auth/auth_about/logout", 
        method="POST", 
        on_success=on_logout_success
    )
    
    page = Page(
        Container(
            Head("About - Dynamic Auth"),
            
            # Loading State
            Show(
                show_loading,
                Container(Text("Checking session..."), style="padding: 20px;")
            ),
            
            # Login Form
            Show(
                show_login,
                Container(
                    Text("Guest Login (guest/guest)", style="font-size: 20px; font-weight: bold; margin-bottom: 20px;"),
                    Input(id="about_user", placeholder="Username", style="padding: 10px; margin-bottom: 10px; border: 1px solid #ccc;"),
                    Input(id="about_pass", placeholder="Password", type="password", style="padding: 10px; margin-bottom: 10px; border: 1px solid #ccc;"),
                    Text("", class_name=error_sel.replace(".", ""), style="color: red; margin-bottom: 10px; font-size: 14px;"),
                    Button("Login as Guest", on_click=submit_login, style="padding: 10px; background: #10b981; color: white; border: none; border-radius: 4px; cursor: pointer;"),
                    style="display: flex; flex-direction: column; width: 300px; padding: 20px; border: 1px solid #eee; border-radius: 8px; box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);"
                )
            ),
            
            # Content (Guarded)
            Show(
                show_content,
                Container(
                    Text("Welcome to the Guarded About Page!", style="font-size: 22px; font-weight: bold; margin-bottom: 10px; color: #10b981;"),
                    Container(
                        Text("Logged in as: ", style="font-weight: 500;"),
                        Text("", class_name=username_sel.replace(".", "")),
                        style="display: flex; gap: 8px; margin-bottom: 15px;"
                    ),
                    Button("Logout", on_click=fetch_logout, style="padding: 10px; background: #ef4444; color: white; border: none; border-radius: 4px; cursor: pointer;"),
                    style="display: flex; flex-direction: column; width: 300px; padding: 20px; border: 1px solid #eee; border-radius: 8px; box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);"
                )
            ),
            style="display: flex; justify-content: center; align-items: center; height: 100vh; font-family: system-ui, sans-serif; background-color: #f0fdf4;"
        )
    )
    page.add_script(fetch_me)
    return page
