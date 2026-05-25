from dars.all import *

@route("/about", route_type=RouteType.SSR)
def about():
    return Page(
        Container(
            Text("about SSR Page works!")
        )
    )
