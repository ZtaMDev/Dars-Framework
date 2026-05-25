from dars.core.auth import requires_auth
from dars.hooks import useDynamic
from dars.all import *
# Setup Dars Auth
def verify_user(username, password):
    if username == "admin" and password == "1234":
        return {"id": "1", "username": "admin", "role": "admin"}
    return None
@route("/auth", route_type=RouteType.SSR)
def auth():
    # ── VRefs ──────────────────────────────────────────────────────────
    # Visibility states
    show_loading = setVRef(True, ".show-loading")
    show_login = setVRef(False, ".show-login")
    show_dashboard = setVRef(False, ".show-dashboard")
    
    # Data states
    error_sel = ".login-error"
    username_sel = ".user-name"
    role_sel = ".user-role"
    

    # ── Session Check ──────────────────────────────────────────────────
    on_me_success = runSequence(
        updateVRef(".show-loading", False),
        updateVRef(".show-dashboard", True),
        updateVRefFromResponse(username_sel, key="response.user.username"),
        updateVRefFromResponse(role_sel, key="response.user.role"),
    )
    on_me_error = runSequence(
        updateVRef(".show-loading", False),
        updateVRef(".show-login", True),
    )
    
    fetch_me, *_ = useFetch(
        "/_dars/auth/me", 
        method="GET", 
        on_success=on_me_success, 
        on_error=on_me_error
    )

    # ── Login Form ─────────────────────────────────────────────────────
    login_form = collect_form(username=V("#username_input"), password=V("#password_input"))
    validator = FormValidator({
        "username": [required()],
        "password": [required()]
    })
    
    on_login_success = runSequence(
        updateVRef(error_sel, ""),
        updateVRef(".show-login", False),
        updateVRef(".show-dashboard", True),
        updateVRefFromResponse(username_sel, key="response.user.username"),
        updateVRefFromResponse(role_sel, key="response.user.role"),
    )
    
    on_login_error = runSequence(
        updateVRefFromResponse(error_sel, key="response.detail")
    )

    submit_login = validator.validated_submit(
        url="/_dars/auth/login",
        form_data=login_form,
        on_success=on_login_success,
        on_error=on_login_error
    )

    # ── Logout ─────────────────────────────────────────────────────────
    on_logout_success = runSequence(
        updateVRef(".show-dashboard", False),
        updateVRef(".show-login", True),
        updateVRef(username_sel, ""),
        updateVRef(role_sel, "")
    )
    
    fetch_logout, *_ = useFetch(
        "/_dars/auth/logout", 
        method="POST", 
        on_success=on_logout_success
    )

    # ── Page ───────────────────────────────────────────────────────────
    page = Page(
        Container(
            Head("Auth Test"),
            
            # Loading State
            Show(
                show_loading,
                Container(Text("Checking session..."), style="padding: 20px;")
            ),
            
            # Not Logged In (Login Form)
            Show(
                show_login,
                Container(
                    Text("Login to Dars", style="font-size: 24px; font-weight: bold; margin-bottom: 20px;"),
                    Input(id="username_input", placeholder="Username (admin)", style="padding: 10px; margin-bottom: 10px; border: 1px solid #ccc;"),
                    Input(id="password_input", placeholder="Password (1234)", type="password", style="padding: 10px; margin-bottom: 10px; border: 1px solid #ccc;"),
                    Text("", class_name=error_sel.replace(".", ""), style="color: red; margin-bottom: 10px; font-size: 14px;"),
                    Button("Login", on_click=submit_login, style="padding: 10px; background: #4f46e5; color: white; border: none; border-radius: 4px; cursor: pointer;"),
                    style="display: flex; flex-direction: column; width: 300px; padding: 20px; border: 1px solid #eee; border-radius: 8px; box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);"
                )
            ),
            
            # Logged In (Dashboard)
            Show(
                show_dashboard,
                Container(
                    Text("Welcome back!", style="font-size: 20px; font-weight: bold; margin-bottom: 10px;"),
                    Container(
                        Text("Username: ", style="font-weight: 500;"),
                        Text("", class_name=username_sel.replace(".", "")),
                        style="display: flex; gap: 8px; margin-bottom: 5px;"
                    ),
                    Container(
                        Text("Role: ", style="font-weight: 500;"),
                        Text("", class_name=role_sel.replace(".", "")),
                        style="display: flex; gap: 8px; margin-bottom: 15px;"
                    ),
                    Button("Logout", on_click=fetch_logout, style="padding: 10px; background: #ef4444; color: white; border: none; border-radius: 4px; cursor: pointer;"),
                    style="display: flex; flex-direction: column; width: 300px; padding: 20px; border: 1px solid #eee; border-radius: 8px; box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);"
                )
            ),
            
            style="display: flex; justify-content: center; align-items: center; height: 100vh; font-family: system-ui, sans-serif; background-color: #f9fafb;"
        )
    )

    # Trigger session check on page load
    page.add_script(fetch_me)

    return page
