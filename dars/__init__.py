# Dars Framework - Core Source File
#
# This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0.
# If a copy of the MPL was not distributed with this file, You can obtain one at
# https://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2025 ZtaDev
"""# Dars Framework
D.A.R.S is a Full-Stack multiplatform Python UI framework for building modern, interactive web and desktop apps entirely in Python. Seamlessly integrated with FastAPI, it lets you build complete applications with Server-Side Rendering (SSR), reactive SPA routing, static site generation, and a production-ready backend API — all from a single Python codebase, with zero JavaScript required.

Official [Website](https://ztamdev.github.io/Dars-Framework/) |
Documentation [Docs](https://ztamdev.github.io/Dars-Framework/docs.html) |
Official [Roadmap](https://ztamdev.github.io/Dars-Framework/roadmap.html) |
Extension for VSCode [here](https://marketplace.visualstudio.com/items?itemName=ZtaMDev.dars-framework) and OpenVSX version [here](https://open-vsx.org/extension/ztamdev/dars-framework)

---

## How It Works

- Build your UI using Python classes and components (`Text`, `Button`, `Container`, `Page`, `Each`, `Show`, `If`, etc.).
- Preview instantly with hot-reload using `app.rTimeCompile()`.
- Export your app to static/dynamic/SSR web files with a single CLI command.
- Export to native desktop apps (BETA) using project config `format: "desktop"` and `dars build`.
- Use multipage layouts, scripts, hooks, and more — see docs for advanced features.
- **One app, four deployment targets simultaneously:** Dars supports Static Site Generation (SSG), Single-Page Application (SPA) routing, Server-Side Rendering (SSR) with FastAPI, and a full Backend API — all from the same Python codebase. Mix and match freely: export some pages as static HTML for SEO, serve others via SSR for dynamic content, and expose REST API endpoints alongside your UI.
- **Full backend toolkit included:** `useFetch` for declarative data fetching, `FormValidator` for client-side validation, `Each` for runtime list rendering from API responses, `JsonStore` for file-backed persistence, `UploadPipeline` for secure file uploads, `SecurityHeadersMiddleware` for HTTP security, and `DarsEnv` for `.env` file support.
- For more information visit the [Documentation](https://ztamdev.github.io/Dars-Framework/docs.html)

---

## Quick Example: Your First App

```python
from dars.all import *

app = App(title="Hello World", theme="dark")

# 1. Define State
state = State("app", title_val="Simple Counter", count=0)

# 2. Define Route
@route("/")
def index():
    return Page(
        Text(
            text=useValue("app.title_val"),
            style="fs-[33px] text-black font-bold mb-[5px]",
        ),
        Text(
            text=useDynamic("app.count"),
            style="fs-[48px] mt-5 mb-[12px]"
        ),
        Button(
            text="+1",
            on_click=state.count.increment(1),
            style="bg-[#3498db] text-white p-[15px] px-[30px] rounded-[8px] cursor-pointer fs-[18px]",
        ),
        Button(
            text="-1",
            on_click=state.count.decrement(1),
            style="bg-[#3498db] text-white p-[15px] px-[30px] rounded-[8px] cursor-pointer fs-[18px] mt-[5px]",
        ),
        Button(
            text="Reset",
            on_click=state.reset(),
            style="bg-[#3498db] text-white p-[15px] px-[30px] rounded-[8px] cursor-pointer fs-[18px] mt-[5px]",
        ),
        style="flex flex-col items-center justify-center h-[100vh] ffam-[Arial] bg-[#f0f2f5]",
    )

app.add_page("index", index(), title="index")

if __name__ == "__main__":
    app.rTimeCompile()
```

---
"""