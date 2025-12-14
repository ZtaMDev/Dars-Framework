(()=>{window.__DARS_VDOM__={type:"T1",id:"page_135",key:"0",children:[{type:"T2",id:"container_136",key:"0/0",children:[{type:"T3",id:"dars-navbar",key:"0/0/0",children:[{type:"T2",id:"navbar-left",key:"0/0/0/0",children:[{type:"T4",id:"link_10",key:"0/0/0/0/0"},{type:"T5",id:"text_137",key:"0/0/0/0/1",text:"Dars Framework"}]},{type:"T2",id:"container_138",key:"0/0/0/1",children:[{type:"T2",id:"navbar-right",key:"0/0/0/1/0",children:[{type:"T6",id:"link_6",key:"0/0/0/1/0/0",text:"Home"},{type:"T6",id:"link_9",key:"0/0/0/1/0/1",text:"Documentation"},{type:"T6",id:"link_8",key:"0/0/0/1/0/2",text:"Releases"},{type:"T6",id:"link_16",key:"0/0/0/1/0/3",text:"PlayGround"},{type:"T6",id:"link_139",key:"0/0/0/1/0/4",text:"GitHub"}]},{type:"T2",id:"hamburger-menu",key:"0/0/0/1/1",children:[{type:"T2",id:"hamburger-btn",key:"0/0/0/1/1/0",children:[{type:"T2",id:"container_140",key:"0/0/0/1/1/0/0",children:[{type:"T2",id:"container_23",key:"0/0/0/1/1/0/0/0"},{type:"T2",id:"container_141",key:"0/0/0/1/1/0/0/1"},{type:"T2",id:"text_26",key:"0/0/0/1/1/0/0/2"}]}]},{type:"T2",id:"mobile-menu",key:"0/0/0/1/1/1",children:[{type:"T6",id:"link_7",key:"0/0/0/1/1/1/0",text:"Home"},{type:"T6",id:"image_3",key:"0/0/0/1/1/1/1",text:"Documentation"},{type:"T6",id:"image_24",key:"0/0/0/1/1/1/2",text:"Releases"},{type:"T6",id:"link_18",key:"0/0/0/1/1/1/3",text:"PlayGround"},{type:"T6",id:"link_73",key:"0/0/0/1/1/1/4",text:"GitHub"}]}]}]}]}]},{type:"T2",id:"markdown-layout",key:"0/1",children:[{type:"T2",id:"markdown-content-container",key:"0/1/0",children:[{type:"T9",id:"markdown_142",key:"0/1/0/0",text:`# Release Notes v1.8.7

> **Dars Server Components & FastAPI Integration**

## Installation

\`\`\`bash
pip install --upgrade dars-framework
\`\`\`

## What's New

### Dars Server Components

v1.8.7 introduces **first-class Server Components**, allowing individual components to be fully rendered on the server while maintaining client-side interactivity.

- **Simple Usage**: Just add \`use_server=True\` to any component inheriting from the base \`Component\` class.
- **Full Support**: All standard Dars components (Text, Button, Container, etc.) support server-side rendering out of the box.
- **Seamless Hydration**: Components are rendered on the backend (FastAPI) and hydrated on the client, preserving events and state.

\`\`\`python
Button("Server Rendered Button", use_server=True, on_click=...)
\`\`\`

### FastAPI Integration Plugin

The new version of \`create_dars_app\` plugin provides tight integration with FastAPI, making it easier than ever to build full-stack SSR applications.

- **Backend-Driven**: The Dars frontend is served and managed by your FastAPI backend.
- **API Co-location**: Define your API routes and your UI components in the same project structure.

### SSR Project Template

Scaffold a complete SSR project and then add Server Components support in seconds:

\`\`\`bash
dars init my-app --type ssr
\`\`\`

This template sets up:
- A FastAPI backend using \`create_dars_app\`.
- A Dars frontend configured for SSR.
- Best practices for project structure and deployment.

---

# Release Notes v1.8.6

> **Environment Management & File Upload Component**

## Installation

\`\`\`bash
pip install --upgrade dars-framework
\`\`\`

## What's New

### DarsEnv: Environment Awareness

New \`DarsEnv\` class provides a standard way to check the current environment mode:

- \`DarsEnv.dev\`: returns \`True\` during development (\`dars dev\`), and \`False\` during production builds (\`dars build\` / \`dars export\`).

This allows you to write conditional logic in your components:

\`\`\`python
from dars.env import DarsEnv

Link(target="/docs" if DarsEnv.dev else "https://example.domain.com/env", text="Docs")
\`\`\`

### FileUpload Component

A new \`FileUpload\` component is now available in \`dars.components.advanced\`:

- Wraps \`<input type="file">\` with a custom, styleable interface.
- Supports \`accept\`, \`multiple\`, and hidden input handling.
- Fully reactive \`on_change\` events.

\`\`\`python
from dars.components.advanced import FileUpload

FileUpload(
    label="Upload Document",
    accept=".pdf",
    on_change=log("File uploaded")
)
\`\`\`

---

# Release Notes v1.8.5

> **Outlet improvements + SSR lazy-load placeholders + SPA router hardening**

## Installation

\`\`\`bash
pip install --upgrade dars-framework
\`\`\`

## What's New

### Multiple Outlets via \`outlet_id\`

Nested routing now supports targeting a specific outlet in a parent layout:

- \`Outlet(outlet_id="main" | "sidebar" | ...)\`
- \`app.add_page(..., outlet_id="...")\`
- The SPA config includes \`outletId\` per route so the client router can mount the child route into the correct outlet.

### Optional \`Outlet(placeholder=...)\`

\`Outlet\` can render an optional placeholder while the child route region is empty (e.g. SSR lazy-load or SPA navigation).
If \`placeholder\` is not provided, the outlet remains empty.

### SSR lazy-load loading/error placeholders (SPA navigation)

New API:

- \`app.set_loading_state(loadingComp, onErrorComp)\`

Exporters and the SSR backend render these as static HTML placeholders and expose them to the SPA router.
This keeps state/events safe and avoids breaking hydration.

### Trailing slash normalization

The SPA router now treats paths with trailing slashes as equivalent:

- \`/dashboard\` and \`/dashboard/\` match the same route

This prevents incorrect 404 redirects when a user navigates to a valid route with a trailing slash.

---

# Release Notes v1.8.4

> **Python-native minification + major Utility Styles upgrade**

## Installation

\`\`\`bash
pip install --upgrade dars-framework
\`\`\`

## What's New

### Python-native minification by default (no Node/Bun required)

v1.8.4 upgrades the default minification pipeline to use real, battle-tested Python minifiers:

- **JavaScript**: \`rjsmin\`
- **CSS**: \`rcssmin\`

This makes builds and exports work reliably in pure-Python environments.

### Optional \`viteMinify\` mode preserved

If you enable \`viteMinify: true\` in \`dars.config.json\`, Dars can still use Vite/esbuild **optionally** when available.
When tools are not installed, Dars falls back to the Python minifiers automatically.

### Runtime bundle safety: \`dars.min.js\`

The embedded runtime bundle (\`dars.min.js\`) is now treated as a special case:

- It is **never** passed through Vite/esbuild (to prevent corruption / ESM \`export\` output).
- It is minified using **Python-only \`rjsmin\`**, regardless of \`viteMinify\`.

### Utility Styles: Arbitrary Properties (\`prop-[value]\`)

The utility system now supports Tailwind-like **arbitrary properties**:

\`\`\`python
style="background-image-[linear-gradient(90deg,_rgba(0,0,0,.35),_#00ffcc)]"
style="padding-[calc(1rem_+_2vw)]"
style="color-[var(--brand-color)]"
style="--brand-color-[#00ffcc]"
\`\`\`

Also includes background gradient support via \`bg-[linear-gradient(...)]\` (maps to \`background-image\`).

### Utility Styles: composable \`filter\` / \`backdrop-filter\` / \`transform\`

Multiple filter/transform utilities now **compose** instead of overwriting:

\`\`\`python
style="filter-[blur(6px)] filter-[brightness(120%)]"
\`\`\`

### Bug fixes for utility parsing

- Fixed \`text-[#hex]\` / \`text-[rgba(...)]\` being interpreted as \`font-size\` instead of \`color\`.
- Fixed prefix collisions like \`border-top-[...]\` incorrectly becoming \`border-color: top-[...]\`.

### LandingPage: navbar styles migrated to utility strings

The LandingPage navbar now uses \`style="..."\` utility strings instead of large inline style dicts,
improving consistency and providing a real-world example of the upgraded styling system.

---

# Release Notes v1.8.3

> **Critical Build Fix**

## Installation

\`\`\`bash
pip install --upgrade dars-framework
\`\`\`

## What's New

### Fixed production build crash: \`Unexpected token 'export'\`

In some environments, the JS minification pipeline (Vite/esbuild) could emit ESM output ending with \`export default ...\` inside \`app.js\`. Since exported pages load \`app.js\` as a classic script, browsers would fail to parse it with:

\`Uncaught SyntaxError: Unexpected token 'export'\`

v1.8.3 fixes this by forcing the minifier output format to **IIFE** for browser scripts, preventing ESM \`export\` statements from being generated during build.

---

# Release Notes v1.8.2

> **Bug Fixes & Utility System Improvements**

## Installation

\`\`\`bash
pip install --upgrade dars-framework
\`\`\`

## What's New

### Fixed setTimeout Promise Handling

The \`setTimeout\` utility function in \`utils_ds.py\` has been updated to properly return a Promise, enabling correct chaining with \`.then()\` operations. This fixes JavaScript syntax errors that occurred when using sequential animations or delayed operations.

### Enhanced Animation System

Improved the animation chaining system to handle missing DOM elements gracefully, preventing runtime errors when referenced elements don't exist in the component tree.

### Responsive Design Enhancements

Updated CSS media queries for better handling of text overflow on small screens, ensuring content remains readable across all device sizes without cutting off important information.

---

# Release Notes v1.8.1

> **Style System Optimization & SSR-Aware Registry**

## Installation

\`\`\`bash
pip install --upgrade dars-framework
\`\`\`

## What's New

### New Style Optimization Pipeline (Phase 1)

v1.8.1 introduces the first phase of a new **style optimization system** focused on reducing inline CSS while keeping full compatibility with Dars reactivity and dynamic operations.

- Static styles defined via \`style={...}\` or Tailwind-like strings in \`style="..."\` are now:
  - Parsed into CSS dicts by the exporter.
  - Fingerprinted and converted into generated classes: \`.dars-s-<hash>\`.
  - Emitted once into a central style registry instead of repeating large inline \`style\` blocks.
- The exporter automatically attaches the generated class to the component and clears the redundant inline style, resulting in:
  - Smaller HTML output.
  - Less DOM churn on updates.
  - Better cacheability for repeated style patterns.

The original \`class_name\` remains fully respected and is appended **after** the generated \`dars-s-*\` class, so user classes (and external CSS frameworks) retain override power.

### Central Style Registry in the HTML Head

The optimized styles are accumulated into a central registry and injected in the \`<head>\` as:

\`\`\`html
<link rel="stylesheet" href="runtime_css.css">
<style id="dars-style-registry">
  /* .dars-s-* rules here */
</style>
<link rel="stylesheet" href="styles.css">
\`\`\`

Order is carefully chosen so that:

- \`runtime_css.css\` provides the base UI tokens and default component styling.
- \`#dars-style-registry\` contains all extracted \`.dars-s-*\` rules (including those coming from \`hover_style\`/\`active_style\` phases on future releases).
- \`styles.css\` (hover/active styles + \`app.add_global_style()\` + user CSS files) comes last, ensuring user styles can override the framework-generated ones.

### Full Export Coverage: Single/Multi Page, SPA & SSR

The new style pipeline now runs consistently across all export modes:

- **Single page & multipage**:
  - \`HTMLCSSJSExporter.export\` collects static styles from the component tree before rendering.
  - The generated HTML includes the \`#dars-style-registry\` block in the head.

- **SPA export (\`_export_spa\`)**:
  - Each SPA route runs the same static-style collection before serializing its \`html\`.
  - The per-route config in \`__DARS_SPA_CONFIG__\` now includes a \`styles\` field containing the CSS for that route.
  - At runtime, the SPA router calls \`_injectStyles(routeName, styles)\` so that SSR/SPA navigations share the same optimized classes.

- **SSR backend (\`dars.backend.ssr\`)**:
  - \`SSRRenderer.render_route\` uses a **deep copy** of each route's root tree to avoid mutating the original components when collecting styles.
  - Static styles are extracted to \`.dars-s-*\` classes, and the resulting CSS is injected into the SSR HTML head using \`#dars-style-registry\`.
  - The SSR JSON API (\`/api/ssr/<route>\`) now returns a \`styles\` field alongside \`html\`, \`vdom\`, \`events\`, etc., so the SPA router can inject the same registry CSS on client-side navigations.

### Runtime & Router Adjustments

The embedded JS runtime (\`dars/js_lib.py\` \u2192 \`DARS_MIN_JS\`) has been updated to be style-optimization aware without breaking existing behavior:

- \`Dars.change({ id, dynamic: true, style: {...} })\` and state rules that manipulate \`attrs.style\` continue to write directly to \`el.style[...]\`.
  - They do **not** depend on an initial inline \`style\` attribute, so elements whose base styles were moved to \`.dars-s-*\` remain fully reactive.
- Class updates via \`attrs.class\` preserve internal \`dars-*\` classes (including \`.dars-s-*\`) and only replace user classes, ensuring the optimization never gets wiped by state changes.
- The SPA router:
  - Loads SSR route data from \`/api/ssr/...\` and now respects the \`styles\` payload from the backend.
  - Uses \`_injectStyles(routeName, styles)\` on every SSR navigation so that optimized classes stay active even after client-side route changes.

These changes are designed to be **backwards compatible** for projects that used only \`style\`/\`class_name\` and dynamic state. The main effect you will notice in v1.8.1 is smaller, cleaner HTML with fewer repeated inline styles, especially for static or Tailwind-like styling.

---

# Release Notes v1.8.0

> **Advanced Multimedia Components & Electron Security Baseline**

## Installation

\`\`\`bash
pip install --upgrade dars-framework
\`\`\`

## What's New

### New Advanced Multimedia Components: Video & Audio

v1.8.0 introduces two new first-class components in the basic library:

- \`Video\`: wrapper around \`<video>\`
- \`Audio\`: wrapper around \`<audio>\`

Both are **fully reactive** and integrate with the existing hooks system:

- \`State\` + \`useDynamic\` for:
  - \`src\`
  - \`autoplay\`
  - \`muted\`
  - \`loop\`
  - \`controls\`
  - \`plays_inline\` (Video)
- \`useValue\` for non-reactive initial values.
- \`VRef\` (setVRef/useVRef) can target \`src\` and other props when needed.

Example:

\`\`\`python
from dars.all import *
from dars.hooks.value_helpers import V

media_state = State(
    "media",
    current_video="/media/intro.mp4",
    current_audio="/media/theme1.mp3",
    autoplay_video=False,
    muted_video=True,
    loop_audio=True,
)

@route("/", index=True)
def index():
    return Page(
        Container(
            Video(
                src=useDynamic("media.current_video"),
                poster="/media/poster.jpg",
                width="720",
                controls=True,
                autoplay=useDynamic("media.autoplay_video"),
                muted=useDynamic("media.muted_video"),
                preload="metadata",
            ),
            Button(
                "Toggle Mute",
                on_click=media_state.muted_video.set(
                    (V("media.muted_video").bool() == True).then(False, True)
                ),
            ),
            Button(
                "Toggle Autoplay",
                on_click=media_state.autoplay_video.set(
                    (V("media.autoplay_video").bool() == True).then(False, True)
                ),
            ),
            Text("Audio actual:"),
            Text(useDynamic("media.current_audio")),
            Audio(
                src=useDynamic("media.current_audio"),
                controls=True,
                loop=useDynamic("media.loop_audio"),
                preload="auto",
            ),
        )
    )
\`\`\`

#### Reactive Boolean Attributes

The web exporter has been extended so that \`useDynamic\` bindings on boolean attributes behave correctly:

- When a \`State\` value changes, the runtime:
  - Adds or removes the HTML attributes: \`autoplay\`, \`muted\`, \`loop\`, \`controls\`, \`playsinline\`.
  - Synchronizes the corresponding JS properties on the media element (\`el.autoplay\`, \`el.muted\`, etc.).
- Dynamic markers (from \`useDynamic\`) no longer count as *truthy* defaults:
  - \`controls=True\`, \`plays_inline=True\` remain active by default.
  - \`autoplay\`, \`loop\`, \`muted\` are off by default unless explicitly set by state or by a literal \`True\`.

This ensures that Video/Audio behave predictably both on initial render and during reactive updates.

### Automatic media/ Directory Copy

The HTML/CSS/JS exporter now supports a **convention-based media folder**:

- If your project root contains a \`media/\` directory, Dars will:
  - Recursively copy \`media/\` into the export \`output_path\`.
  - Preserve subdirectory structure.
- Any \`src="/media/..."\` used in \`Image\`, \`Video\` or \`Audio\` will point to real files in the exported build.

This makes it straightforward to ship videos, audio tracks and posters alongside your static export.

### Electron 39.2.6 Security Baseline

To keep desktop builds secure and reproducible, v1.8.0 introduces an **Electron security baseline**:

- All desktop templates and Electron scaffolds now pin Electron to \`39.2.6\`:
  - \`dars/templates/desktop/template/backend/package.json\`
  - CLI \`init\` desktop scaffolds and \`init --update\` flows.
- \`dars doctor\` gains version-awareness:
  - New constant \`MIN_SAFE_ELECTRON = "39.2.6"\`.
  - When you run \`dars doctor --all --yes\`, Dars will install/update Electron globally via Bun as \`electron@39.2.6\` and \`electron-builder@latest\`.
- \`dars dev\` for desktop projects now warns if your installed Electron is below the baseline and suggests:

  \`\`\`bash
  dars doctor --all --yes
  \`\`\`

This keeps both templates and global tooling aligned with a reviewed Electron version.

### Desktop Dev Flow Fixes (Electron + rTimeCompile)

Several quality-of-life fixes improve desktop (Electron) development:

- \`App.rTimeCompile\` desktop branch:
  - Stops the "Starting preview..." spinner after Electron launches.
  - Exits the method immediately when desktop mode finishes, preventing the web preview server from starting on top of Electron dev.
- \`dars core/js_bridge\`:
  - \`electron_dev_spawn\` now sets \`ELECTRON_DISABLE_SECURITY_WARNINGS=true\` for dev runs.
  - This suppresses the noisy *Electron Security Warning (Insecure Content-Security-Policy)* in dev tools without touching the CSP used by the Dars runtime.

Result: smoother desktop dev cycle with clear logs and no accidental web preview server when working on Electron apps.

### Documentation Updates

- \`LandingPage/documentation/markdown/components.md\` now documents:
  - \`Video\` and \`Audio\` components.
  - Reactive integration with \`State\`, \`useDynamic\`, \`V()\` and VRefs.
  - Recommended \`media/\` folder convention for assets.

---

# Release Notes v1.7.9

> **Global JS Error Handling & safer eval() in the runtime**

## Installation

\`\`\`bash
pip install --upgrade dars-framework
\`\`\`

## What's New

### Centralized safeEval for runtime-generated JS

This release introduces a **centralized eval helper** in the core Dars runtime (\`dars.min.js\`), designed to make hydration/runtime debugging safer and more observable without changing existing behavior in production:

- New internal helper in the JS runtime:

  \`\`\`js
  function _safeEval(code, ctx) {
    if (code == null) return;
    try {
      return (0, eval)(code);
    } catch (err) {
      console.error('[Dars] Eval error:', err);
      // Optional dev hook \u2013 only called if you define it
      try {
        const D = (globalThis && globalThis.Dars) || (typeof window !== 'undefined' ? window.Dars : null);
        if (D && typeof D.onError === 'function') {
          D.onError(err, Object.assign({ code: String(code) }, ctx || {}));
        }
      } catch (_) {}
    }
  }
  \`\`\`

- The runtime keeps using \`eval\` internally where necessary, but now all critical call sites go through \`_safeEval\` instead of raw \`(0,eval)(...)\`.

### Global JS error hook: window.Dars.onError

To help you surface client-side errors during development (especially hydration and dynamic updates), the runtime now exposes a **single global hook**:

- If present, \`window.Dars.onError(err, context)\` is invoked by \`_safeEval\` whenever a runtime-generated script fails.
- \`context\` is a small dictionary that always includes:
  - \`code\`: the JS string that was evaluated.
  - Additional fields depending on where the error happened (see below).
- The hook is **fully optional**:
  - If \`window.Dars\` or \`window.Dars.onError\` are not defined, the runtime simply logs to \`console.error\` and continues as before.
  - This means existing projects and production builds keep working without any changes.

### Errors from events and lifecycle hooks now share the same pipeline

Two of the most important dynamic execution points are now wired to \`_safeEval\` and the global hook:

1. **Event handlers attached from the VDOM**

   - Previously, many handlers used raw \`(0,eval)(c)\` inside \`try/catch\` blocks.
   - Now, event execution goes through \`_safeEval(c, { type, event, phase: 'event_handler' })\`.
   - If you define \`window.Dars.onError\`, you receive:
     - The original \`Error\` instance.
     - The event object (\`event\`).
     - The handler type (\`type\`) and phase (\`'event_handler'\`).

2. **Component lifecycle hooks (onMount, onUpdate, onUnmount)**

   - Lifecycle JS stored in the VDOM used to be executed with inline \`try/catch\`.
   - Now, \`_runLifecycle(id, hook)\` delegates to \`_safeEval(code, { hook, id })\` when a lifecycle snippet is present.
   - This lets you centralize errors from hydration and dynamic updates, while preserving the same control flow in the runtime.

Result: you get a **single, consistent error-reporting channel** for all dynamic runtime code, without changing how the framework behaves when no hook is provided.

### Files Modified

- \`dars/js_lib.py\`
  - Added the \`_safeEval(code, ctx)\` helper to the embedded \`DARS_MIN_JS\` runtime.
  - Refactored event handlers and lifecycle execution to use \`_safeEval\` and forward enriched context to an optional \`window.Dars.onError\` hook.

---

# Release Notes v1.7.8

> **Full-Stack SSR DX: backendEntry Defaults, Validation & CLI Backend Runner**

## Installation

\`\`\`bash
pip install --upgrade dars-framework
\`\`\`

## What's New

### Automatic backendEntry for SSR Projects

When you scaffold a new SSR project with:

\`\`\`bash
dars init my-app --type ssr
\`\`\`

Dars now creates a \`dars.config.json\` that includes a default backend entry:

\`\`\`json
"backendEntry": "backend.api:app"
\`\`\`

This matches the generated \`backend/api.py\` file and makes it trivial to start the FastAPI SSR backend.

### Smarter Config Validation for SSR

The \`dars config validate\` command has been extended to understand when your project is using SSR:

- Introspects the \`entry\` module and inspects:
  - SPA routes (\`app._spa_routes\`) for \`RouteType.SSR\`.
  - Multipage routes (\`app._pages\`) whose root metadata has \`route_type = RouteType.SSR\`.
- If dynamic detection fails, a fallback **static scan** looks for \`RouteType.SSR\` in the entry source file.
- When any SSR route is detected and \`backendEntry\` is missing in \`dars.config.json\`, validation now reports:

> This app is not going to work because you don't have configured the backendEntry in dars.config.json with your backend entry file.

This prevents half-configured SSR apps where routes are marked as \`RouteType.SSR\` but no backend has been wired.

### New CLI Command: \`dars dev --backend\`

To simplify the SSR development workflow, a new flag was added to the \`dars dev\` command:

\`\`\`bash
# Frontend dev (preview + hot reload)
dars dev

# Backend-only dev (SSR/API)
dars dev --backend
\`\`\`

Behavior:

- \`dars dev\` (no flags):
  - Resolves \`entry\` from \`dars.config.json\` (default \`main.py\`).
  - Runs the file directly (\`python main.py\`), which is expected to call \`app.rTimeCompile()\`.
  - Starts the Dars preview server on \`http://localhost:8000\` with hot reload.

- \`dars dev --backend\`:
  - Reads \`backendEntry\` from \`dars.config.json\` (e.g. \`"backend.api:app"\`).
  - Starts the FastAPI SSR backend via uvicorn:

    \`\`\`bash
    python -m uvicorn backend.api:app --reload --host 127.0.0.1 --port 3000
    \`\`\`

  - If \`backendEntry\` is missing, uses the same validation message as \`dars config validate\` to explain that SSR will not work.

Result: you can now run a full-stack SSR dev setup with two explicit terminals:

\`\`\`bash
# Terminal 1 - Frontend
dars dev

# Terminal 2 - Backend
dars dev --backend
\`\`\`

This keeps logs cleanly separated while still leveraging the built-in hot reload from \`app.rTimeCompile()\` and uvicorn's reload system.

---

# Release Notes v1.7.7

> **Component Lifecycle Hooks, Dynamic VRefs & Safer Runtime Updates**

## Installation

\`\`\`bash
pip install --upgrade dars-framework
\`\`\`

## What's New

### Component Lifecycle Hooks (onMount, onUpdate, onUnmount)

This release introduces **component-level lifecycle hooks**, available both for regular components and \`@FunctionComponent\`:

- New props on components (and FunctionComponents):
  - \`onMount\`
  - \`onUpdate\`
  - \`onUnmount\`
- Hooks accept \`dScript\` & functions or inline JS strings.
- The VDOM now includes a \`lifecycle\` block per node with:
  - Hook type (\`inline\`/\`dscript\`).
  - JS code ready to be executed in the runtime.

### Dynamic createComp/deleteComp with Lifecycle and Events

The dynamic backend helpers are now fully compatible with lifecycle, events and VRefs:

- \`createComp(target, root, position="append")\`:
  - Uses \`VDomBuilder\` to serialize the full component into VDOM.
  - Injects the \`_events\` map produced by the exporter for that subtree.
  - In the runtime, \`runtime.createComponent(rootId, vdom, pos)\`:
    - Builds actual DOM from the VDOM.
    - Rehydrates events for the whole subtree (\`_attachEventsForVNode\`).
    - Registers lifecycle in \`__lifecycle\` and fires \`onMount\` for all nodes with hooks.
    - Calls \`DarsHydrate(el)\` so the rest of bindings (V(), VRefs, useDynamic, etc.) attach to the dynamic subtree as well.

- \`deleteComp(id)\`:
  - Calls \`runtime.deleteComponent(id)\`.
  - The runtime runs \`onUnmount\` for that id before removing the node and its VDOM entry.

Result: components created and destroyed with \`createComp\`/\`deleteComp\` have the **same lifecycle behavior** and event rehydration as components rendered in the initial VDOM.

### onUpdate wired into dynamic changes and VRefs

The \`onUpdate\` hook now fires in two key scenarios:

1. **Dynamic state changes** (runtime \`change()\`):
   - When \`Dars.change({ id, dynamic: true, ... })\` is called (e.g. via \`updateComp()\`), the runtime:
     - Applies changes to \`text\`, \`html\`, \`style\`, \`attrs\`, \`classes\`, etc.
     - Notifies watchers (\`watch()\` / internals).
     - Calls \`_runLifecycle(id, 'onUpdate')\` whether the element exists or the change is purely logical.

2. **VRef changes** via \`updateVRef()\`:
   - New runtime helper: \`Dars.updateVRef(selector)\`.
   - The JS generated by \`updateVRef(...)\` now, after updating the DOM and \`window.__DARS_VREF_VALUES__\`, does:

     \`\`\`js
     if (window.Dars && window.Dars.updateVRef) {
         window.Dars.updateVRef(selector);
     }
     \`\`\`

   - \`Dars.updateVRef(selector)\`:
     - Finds all elements matching the selector.
     - For each, walks up the DOM tree until it finds the first ancestor with lifecycle registered.
     - Runs \`onUpdate\` for that id (once per id), allowing parent components to react to shared VRef changes.

### Improved dynamic VRefs (setVRef + updateVRef)

Several adjustments ensure \`setVRef()\` works equally well in the initial render and in components created dynamically via \`createComp\`:

- \`setVRef(value, selector)\` now creates a \`VRefValue\` whose metadata is preserved in the VDOM:
  - \`Text(text=setVRef(0, ".dyn_count"))\` serializes as:
    - \`text: "0"\` (initial value).
    - \`class: "dyn_count"\` auto-added when the selector is of type \`.class\`.
  - The runtime registers \`window.__DARS_VREF_VALUES__['.dyn_count'] = 0\` during hydration.
- This works the same when that \`Text\` is part of a component created with \`createComp\`: the VDOM includes both the initial value and the class, and \`updateVRef(".dyn_count", ...)\` can find and update all instances correctly.

### New equal() helper for expressions with V()

To make it easier to compose numeric and literal expressions with \`V()\`, this release adds the \`equal()\` helper in \`dars.hooks.value_helpers\`:

\`\`\`python
from dars.hooks.value_helpers import V, equal

# Sumar 1 a un VRef
Button(
    "Increment",
    on_click=updateVRef(".dyn_count", V(".dyn_count").int() + 1),
)

# Resetear a 0 usando equal()
Button(
    "Reset",
    on_click=updateVRef(".dyn_count", equal(0)),
)

# Combinar con otra expresi\xF3n basada en V()
expr = V(".a").int() + equal(V(".b").int())
updateVRef(".result", expr)
\`\`\`

- \`equal(value)\` normalizes any value (literal, \`V()\`, \`MathExpression\`, etc.) into a \`MathExpression\`, so it integrates into the operation tree with the same async semantics and \`NaN\` validation as the rest of the expression system.

> Note: to reset a VRef it's better to use \`equal(0)\` directly as the target value instead of adding it to the current value.

### Fixes in updateComp() and JS generation

JS generation for \`updateComp()\` (dynamic backend) has been hardened so it works correctly with complex expressions containing \`//\` comments and async IIFEs such as those generated by \`updateVRef(...)\`:

- The internal code in \`updateComp()\` now:
  - No longer collapses whitespace/newlines in the JS payload, avoiding cases where \`//\` comments consume the rest of the line.
  - Safely strips the trailing \`;\` from \`dScript.code\` before inlining it into the \`change({ ... })\` payload.
- This allows \`updateComp()\` to be combined with complex scripts (including those generated by \`V()\` / \`updateVRef\`) without causing \`SyntaxError\` in \`app.js\`.

### Documentation updates

The hooks and components documentation has been updated to reflect these changes:

- \`LandingPage/documentation/markdown/hooks.md\`:
  - Extended **Pythonic Value Helpers** section with the new \`equal()\` helper and examples together with \`V()\` and \`updateVRef\`.
- \`LandingPage/documentation/markdown/components.md\`:
  - The **Runtime Component Manipulation (createComp / deleteComp)** and new **Component Lifecycle Hooks** sections explain that dynamically created subtrees:
    - Rehydrate events.
    - Register and execute lifecycle hooks (\`onMount\`/\`onUpdate\`/\`onUnmount\`).
    - Are compatible with VRefs and the current VDOM system.

---

# Release Notes v1.7.6

> **Security Hardening for Prism.js Integration**

## Installation

\`\`\`bash
pip install --upgrade dars-framework
\`\`\`

## What's New

### Safer CDN Loading for Syntax Highlighting

This release focuses on tightening the security of the **Prism.js** integration used for code highlighting in exported documentation and apps.

Previously, the Prism script was injected without any additional security attributes:

\`\`\`html
<script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/prism.min.js"><\/script>
\`\`\`

Starting from **v1.7.6**, Dars now injects the script tag with **Subresource Integrity (SRI)**, \`crossorigin\`, and \`referrerpolicy\` attributes:

\`\`\`html
<script
  src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/prism.min.js"
  integrity="sha512-7Z9J3l1+EYfeaPKcGXu3MS/7T+w19WtKQY/n+xzmw4hZhJ9tyYmcUS+4QqAlzhicE5LAfMQSF3iFTK9bQdTxXg=="
  crossorigin="anonymous"
  referrerpolicy="no-referrer">
<\/script>
\`\`\`

#### Benefits

- **Subresource Integrity (SRI)** ensures that the script loaded from the CDN has not been tampered with.
- \`crossorigin="anonymous"\` is required for SRI on cross-origin resources and avoids leaking credentials.
- \`referrerpolicy="no-referrer"\` prevents the browser from sending the full URL of your site to the CDN as the HTTP referrer.

This change makes the default code-highlighting setup more secure by default, while remaining fully backwards compatible for existing projects.

---

# Release Notes v1.7.5

> **CLI Doctor, Error Handling & JS Minification Improvements**

## Installation

\`\`\`bash
pip install --upgrade dars-framework
\`\`\`

## What's New

### Faster, More Helpful \`dars doctor\`

The \`dars doctor\` command has been refined to give you **actionable diagnostics** with less noise:

- Single-pass detection for:
  - Node.js LTS
  - Bun
  - Optional tools: \`esbuild\`, \`vite\`, \`electron\`, \`electron-builder\`
  - Python dependencies from \`pyproject.toml\`
- Clear report table with required vs detected versions and status.
- Non-interactive modes:
  - \`dars doctor --check\` exits with code \`0\` when core requirements (Python deps) are satisfied, \`1\` otherwise.
  - \`dars doctor --all --yes\` attempts to install all missing tools using Bun and pip without extra prompts.
- When Bun is missing, doctor can invoke the official installers:
  - Windows (PowerShell): \`powershell -NoProfile -ExecutionPolicy Bypass -c "irm bun.sh/install.ps1 | iex"\`
  - macOS/Linux: \`curl -fsSL https://bun.sh/install | bash\`
- Optional web/desktop tools can be installed globally with Bun:
  - \`bun add -g vite\`
  - \`bun add -g esbuild\`
  - \`bun add -g electron\`
  - \`bun add -g electron-builder\`

These improvements make \`dars doctor\` a practical environment bootstrapper, not just a checker.

### Short, Human-Friendly CLI Errors

The CLI now avoids dumping huge tracebacks for common scenarios:

- Global wrapper around the \`main()\` entrypoint shows concise messages:
  - On \`KeyboardInterrupt\` (Ctrl+C): \`Process interrupted by user\`.
  - On generic errors: \`Process failed: <message>\`.
  - Full tracebacks are still available when running with \`DARS_DEBUG=1\`.
- \`dars build\` specifically catches \`KeyboardInterrupt\` around the heavy export step and reports:
  - \`Process interrupted by user during build\` instead of a long stack trace.

This improves the day-to-day UX, especially when cancelling long builds or dev sessions.

### JS Bundling: Always \`app.js\` in Build Mode

The web exporter has been updated so that **JS combination depends only on the bundle flag**, not on Vite:

- When \`bundle=True\` (build/production):
  - Single-page apps export a unified \`app.js\` bundle containing:
    - VDOM snapshot
    - Dars runtime glue
    - Page/user scripts
  - Multi-page apps export per-page bundles: \`app_{slug}.js\`.
- When \`bundle=False\` (development):
  - The exporter keeps separate files (\`runtime_dars*.js\`, \`script*.js\`, \`vdom_tree*.js\`) for easier debugging.

This guarantees consistent bundling in production regardless of whether Vite is used for minification.

### Safer & Smarter JS Minification (Default vs Vite)

JS minification has been hardened to avoid runtime breakage and to clearly separate **default** minify from **Vite-based** minify:

- \`minify_js\` now follows this strategy:
  - If \`viteMinify\` is enabled (\`DARS_VITE_MINIFY=1\`) and Vite is available, use Vite for JS minification.
  - If Vite is enabled but not available, and \`esbuild\` is installed, fall back to \`esbuild\` as the minifier backend.
  - If \`viteMinify\` is disabled, skip Vite/esbuild and use the conservative **regex-based Python minifier** (comments + whitespace) for JS.
- The core runtime bundle \`dars.min.js\` is now **explicitly skipped** by the default minifier to avoid corrupting already-minified code.
  - This prevents \`SyntaxError: Invalid or unexpected token\` errors that could occur when re-minifying the runtime.
- The CLI progress label reflects the actual mode:
  - \`Applying minification (default)\` when only the Python-side minifier is used.
  - \`Applying minification (default + vite)\` when both the default and Vite/esbuild pipelines are active.

These changes make minification more predictable, safer for the Dars runtime, and better aligned with the \`viteMinify\` flag in \`dars.config.json\`.

---

# Release Notes v1.7.4

> **Real SSR Hydration, SPA Config & Streaming**

## Installation

\`\`\`bash
pip install --upgrade dars-framework
\`\`\`

## What's New

### Real SSR Hydration & SPA Integration

Dars Framework 1.7.4 refines the SSR system to deliver a **true SSR experience**:

- The server now renders **the entire page** (HTML + \`<head>\` + \`<body>\`) using \`SSRRenderer\`.
- The content is delivered wrapped in \`__dars_spa_root__\`, allowing the Dars SPA router to hydrate the existing DOM without re-rendering from scratch.
- A minimal SPA route configuration is exposed as \`window.__DARS_SPA_CONFIG__\`, so the client runtime knows all paths, route types, and SSR endpoints from the very first load.

### Serialized Initial State (V1 + V2)

To enable full hydration without a static export pipeline, the SSR backend now serializes the initial state:

- **V1 (STATE_BOOTSTRAP)** \u2192 \`window.__DARS_STATE__\`
- **V2 (STATE_V2_REGISTRY)** \u2192 \`window.__DARS_STATE_V2__\` (via \`State.to_dict()\`)

The \`dars.min.js\` runtime automatically registers the V1 snapshot and exposes the V2 snapshot as \`Dars.stateV2Snapshot\` for tools and advanced debugging.

### Enriched JSON SSR Endpoints

The SSR JSON endpoints (\`/api/ssr/{route_name}\`) now return richer information for the SPA router and external tooling:

- \`html\` \u2013 Body HTML for incremental hydration.
- \`vdom\` \u2013 Per-route VDOM snapshot.
- \`events\` \u2013 Event map for attaching handlers on the client.
- \`states\` \u2013 V1 state snapshot.
- \`statesV2\` \u2013 V2 state snapshot.
- \`spaConfig\` \u2013 Minimal SPA routes configuration.
- \`headMetadata\` \u2013 Metadata extracted from the \`Head\` component.

### HTML Streaming (Experimental)

\`create_ssr_app\` now accepts a new optional \`streaming\` parameter:

\`\`\`python
from dars.backend.ssr import create_ssr_app

fastapi_app = create_ssr_app(dars_app, streaming=True)
\`\`\`

When \`streaming=True\`, HTML responses for SSR routes are sent in two parts:

1. \`<!DOCTYPE html>\`, \`<html>\`, full \`<head>\` and the opening \`<body>\` tag.
2. The rest of the document (\`__dars_spa_root__\` + hydration scripts).

This allows browsers and crawlers to receive metadata and the \`<head>\` **as early as possible**, improving FCP and SEO while the body content finishes rendering.

---

# Release Notes v1.7.3

> **Complete Head Component & SEO Metadata Support**

## Installation

\`\`\`bash
pip install --upgrade dars-framework
\`\`\`

## What's New

### Complete Head Component Support

The \`Head\` component now works seamlessly across all export modes: **SPA**, **SSR**, and **Multipage**. You can manage your page title, description, and social media metadata (Open Graph, Twitter Cards) directly from your Python components.

\`\`\`python
Head(
    title="My App",
    description="The best app ever",
    og_image="/share.png"
)
\`\`\`

### Dynamic SPA Metadata

In Single Page Applications (SPA), the document metadata now **updates automatically** when navigating between routes. The router intelligentally applies:
- \`<title>\`
- Meta tags (\`description\`, \`keywords\`, etc.)
- Open Graph tags (\`og:title\`, \`og:image\`, etc.)
- Twitter Card tags
- Canonical links and favicons

This ensures your SPA is SEO-friendly and displays correct previews when shared on social media, even for client-side routes.

---

# Release Notes v1.7.2

> **Performance & Developer Experience Enhancements**

## Installation

\`\`\`bash
pip install --upgrade dars-framework
\`\`\`

## What's New

### Instant Server Shutdown

The \`dars dev\` command now exits instantly when pressing Ctrl+C. All cleanup operations (watchers, server, file deletion) happen in background threads, providing immediate feedback without blocking.

**Exit Flow:**
\`\`\`
Ctrl+C pressed
\u2193
"Preview stopped" (instant)
\u2193
"Cleaning up preview files..." (spinner, max 2s)
\u2193
"Preview files deleted" (done)
\`\`\`

---

### Optimized Hot Reload Performance

Hot module replacement is now significantly faster through intelligent caching and change detection.

**Optimizations Applied:**

#### 1. Smart dars.min.js Caching

The framework library is no longer rewritten on every hot reload if the content hasn't changed.

\`\`\`python
# Check if file exists and content matches
if os.path.exists(dest_js):
    with open(dest_js, 'r') as f:
        if f.read() == DARS_MIN_JS:
            # Skip write - already up to date
            return
\`\`\`

#### 2. Intelligent Public Directory Sync

Static assets in \`public/\` or \`assets/\` directories are only copied when changes are detected.

**Change Detection:**
- **New files**: Detected via modification time
- **Modified files**: Detected via modification time comparison
- **Deleted files**: Detected via file count mismatch

**Marker File (\`.public_sync\`):**
\`\`\`
1733544800.123    # last sync timestamp
42                # file count
\`\`\`

**Development Mode (bundle=False):**
- Uses \`.public_sync\` marker for optimization
- Only copies when changes detected
- Skips unnecessary I/O operations

**Production Mode (bundle=True):**
- Always copies all files
- No marker file created
- Clean production builds

---

### Background Watcher Initialization

File watchers now initialize in a background thread, allowing the preview server to start immediately.

**Before (v1.7.1):**
- Server waited for all watchers to initialize
- 1-3 second startup delay on large projects
- Blocked on file system operations

**After (v1.7.2):**
- Server starts instantly(when dev_export finished)
- Watchers initialize in background
- Non-blocking startup sequence

---

### Desktop Mode Optimizations

All performance improvements from Web mode have been applied to Desktop mode (Electron) for consistent behavior.

**Improvements:**
- Instant shutdown on Ctrl+C
- Background cleanup (Electron, watchers, files)
- Visual feedback during exit
- Same optimization patterns as Web mode

---

## Performance Improvements

### Startup Speed
- **90% faster** on large projects
- Watchers initialize in background
- Server ready immediately

### Hot Reload Speed
- **50-70% faster** reload times
- Smart caching for static assets
- Only updates changed files

### Shutdown Speed
- **95% faster** exit with Ctrl+C
- All cleanup in background
- Instant user feedback

---

## Technical Details

### Background Cleanup Architecture

All blocking operations moved to daemon threads:

\`\`\`python
def _background_cleanup():
    # Stop watchers
    for w in watchers:
        w.stop()
    
    # Stop directory watchers
    for dw in directory_watchers:
        dw.stop()
    
    # Server shutdown
    if server:
        server.httpd.shutdown()
        server.httpd.server_close()

# Non-blocking execution
cleanup_thread = threading.Thread(target=_background_cleanup, daemon=True)
cleanup_thread.start()
\`\`\`

### Smart Public Directory Sync

Change detection algorithm:

\`\`\`python
# Read marker
with open('.public_sync', 'r') as f:
    last_sync, last_count = f.read().split('\\n')

# Check for changes
current_count = 0
for root, dirs, files in os.walk(public_abs):
    for file in files:
        current_count += 1
        if os.path.getmtime(file) > last_sync:
            return True  # Modified or new file

# Check for deletions
if current_count != last_count:
    return True  # Files added or removed

return False  # No changes
\`\`\`

---

## Files Modified

### Core Changes
- \`dars/core/app.py\` - Background cleanup, watcher initialization
- \`dars/exporters/web/html_css_js.py\` - Smart caching, change detection

### Impact
- **Web Mode**: Faster startup, reload, and shutdown
- **Desktop Mode**: Same optimizations applied

---

All existing projects will automatically benefit from:
- Faster \`dars dev\` startup
- Faster hot reload
- Instant Ctrl+C exit
- Optimized asset copying

**Note:** Development mode will create a \`.public_sync\` file in the preview directory. This file is used for optimization and can be safely ignored. It is not created in production builds.

---

# Release Notes v1.7.1


> **CLI Performance & Developer Experience Improvements**

## Installation

\`\`\`bash
pip install --upgrade dars-framework
\`\`\`

## What's New

### Instant Server Startup

The \`dars dev\` command now starts **instantly** thanks to background directory cleanup. No more waiting for file deletion(probably)!

**Before (v1.7.0):**
- Startup blocked by \`dars_preview\` directory deletion
- 2-5 second delay on large projects
- No visual feedback during initialization

**After (v1.7.1):**
- **Instant startup** - cleanup happens in background
- Visual spinner: "Starting preview..."
- Non-blocking architecture

**How it works:**
1. Old \`dars_preview\` renamed to \`dars_preview_trash_{timestamp}\`
2. Deletion happens in daemon thread
3. Server starts immediately
4. Spinner shows progress

---

### Fast Exit on Ctrl+C

Pressing Ctrl+C now exits **immediately** with visual feedback.

**Before (v1.7.0):**
- Blocked on preview file deletion
- 3-10 second wait on large projects
- No feedback during cleanup

**After (v1.7.1):**
- **Instant response** to Ctrl+C
- Background cleanup with spinner
- Maximum 2-second timeout
- Visual feedback: "Cleaning up preview files..."

**Exit Flow:**
\`\`\`
Ctrl+C pressed
\u2193
"Exiting server..." (immediate)
\u2193
"Cleaning up preview files..." (spinner, max 2s)
\u2193
"\u2714 Preview files deleted." (done!)
\`\`\`

---

### HMR Bug Fixes

#### Fixed: Syntax Highlighting Lost on Hot Reload

**Problem:** After the first load, code blocks had Prism.js highlighting. But after making a change and triggering hot reload, the highlighting disappeared.

**Root Cause:** The \`HTMLCSSJSExporter\` instance is reused across hot reloads. State flags like \`_hljs_injected_pages\` persisted, causing the exporter to skip script injection on subsequent exports.

**Solution:** Reset state flags at the start of every \`export()\` call:

\`\`\`python
# dars/exporters/web/html_css_js.py
def export(self, app, output_path, bundle=False):
    # Reset state for HMR
    if hasattr(self, "_hljs_injected_pages"):
        self._hljs_injected_pages.clear()
    
    # Reset lazy script flags
    lazy_keys = [k for k in self.__dict__.keys() 
                 if k.startswith("_lazy_script_injected_")]
    for k in lazy_keys:
        delattr(self, k)
\`\`\`

**Result:** Syntax highlighting now works reliably across all hot reloads!

---

#### Fixed: Empty Code Blocks

**Problem:** Code blocks appeared as black boxes with no content.

**Root Cause:** A regex pattern in \`render_markdown\` was capturing the closing \`>\` of the \`<code>\` tag, removing all content after it.

**Solution:** Fixed regex to preserve code content:

\`\`\`python
# Before (broken)
re.sub(r'<pre([^>]*)>\\s*<code(?![^>]*class=)([^>]*)>', ...)

# After (fixed)
re.sub(r'<pre([^>]*)>\\s*<code(?![^>]*class=)', ...)
\`\`\`

---

### Developer Experience Improvements

**Visual Feedback:**
- "Starting preview..." spinner during initialization
- "Cleaning up preview files..." spinner on exit
- Success messages with color coding
- Instant response to all commands

---

## Technical Details

### Background Cleanup Architecture

\`\`\`python
# Rename old directory
trash_name = f"dars_preview_trash_{int(time.time()*1000)}"
os.rename(preview_dir, trash_path)

# Delete in background thread
def _bg_cleanup(path):
    shutil.rmtree(path, ignore_errors=True)

threading.Thread(target=_bg_cleanup, args=(trash_path,), daemon=True).start()
\`\`\`

---

### State Reset Pattern

The HMR fix introduces a pattern for managing exporter state across hot reloads:

\`\`\`python
# Reset per-page injection tracking
if hasattr(self, "_hljs_injected_pages"):
    self._hljs_injected_pages.clear()

# Reset dynamic flags
lazy_keys = [k for k in self.__dict__.keys() 
             if k.startswith("_lazy_script_injected_")]
for k in lazy_keys:
    delattr(self, k)
\`\`\`

This ensures scripts are re-injected on every export, maintaining consistency across development cycles.

---

## Files Modified

### Core Changes
- \`dars/core/app.py\` - Background cleanup, startup/exit spinners
- \`dars/exporters/web/html_css_js.py\` - HMR state reset, regex fix

### Impact
- **Web Mode**: Faster startup and exit
- **Desktop Mode**: Same optimizations applied

---

# Release Notes v1.7.0


> **Complete VRef System & Multi-Element Updates**

## Installation

\`\`\`bash
pip install --upgrade dars-framework
\`\`\`

## What's New

### New Hook: setVRef()

Introducing \`setVRef()\`, a powerful new hook that allows you to create independent value references tied to specific DOM selectors. Unlike \`useValue\` which sets initial values for single components, \`setVRef\` creates a lightweight, portable reference that can be shared across your application.

**Key Capabilities:**
*   **Independent Values:** Define values that live in the DOM, identified by a CSS selector.
*   **Shared References:** Use a class selector (e.g., \`.shared-value\`) to share a single value across multiple components.
*   **Function Component Support:** seamless integration with \`@FunctionComponent\` templates.

### Multi-Element Updates (Synchronized State)

The \`updateVRef()\` hook has been upgraded to support widespread updates. When you use a **class selector** (e.g., \`.my-value\`) with \`setVRef\` and \`updateVRef\`, **all** matching elements in the DOM will update simultaneously.

This allows you to share a single "value reference" across multiple independent components (like a main display and a sidebar preview) and keep them in sync with a single line of code.

### Extended Component Support

Extended \`useValue\` and \`useDynamic\` support to cover the entire component library. You can now use reactive bindings in:
- \`Card\`
- \`Modal\`
- \`Navbar\`
- \`DatePicker\`
- \`ProgressBar\`
- \`Tooltip\`
- \`Spinner\`

## Example: Shared Counter

\`\`\`python
from dars.all import *

# 1. Define a shared reference using a class selector
count_ref = setVRef(0, ".shared-count")

# 2. Use it in multiple places
Container(
    # First component
    Text(count_ref, class_name="shared-count"),
    
    # Second component (Function Component)
    CountDisplay(count_ref, class_name="shared-count")
)

# 3. Update BOTH with one click!
Button("Increment All", on_click=updateVRef(".shared-count", V(".shared-count").int() + 1))
\`\`\`

---

# Release Notes v1.6.9

> **Dars SSR System & Backend Integration**

## Installation

\`\`\`bash
pip install --upgrade dars-framework
\`\`\`

## What's New

### Dars Server-Side Rendering (SSR)

v1.6.9 marks the official release of the **Dars SSR System**, bringing true full-stack capabilities to the framework. You can now render pages on the server.

---

### Dars Backend

The new \`dars.backend\` module integrates seamlessly with **FastAPI**, allowing you to serve your Dars application alongside your API routes.

#### Key Functions
- **\`create_ssr_app(dars_app)\`**: Converts your Dars App into a standard ASGI application (FastAPI) capable of server-side rendering.
- **\`RouteType.SSR\`**: A new route type that tells Dars to render the page component on the server before sending it to the client.

#### Example: API + SSR Project

\`\`\`python
# backend/api.py
from fastapi import FastAPI
from dars.backend.ssr import create_ssr_app
from main import app as dars_app

# Create full-stack app
app = create_ssr_app(dars_app)

# Add custom API endpoints
@app.get("/api/custom")
def custom_endpoint():
    return {"message": "Hello from API"}
\`\`\`

---

### SSR Routing

Enable Server-Side Rendering for specific pages with a single parameter:

\`\`\`python
@route("/dashboard", route_type=RouteType.SSR)
def dashboard():
    return Page(
        # This is rendered on the server!
        Heading("Welcome Back", level=1),
        Text(f"Server Time: {datetime.now()}")
    )
\`\`\`

---

### Full-Stack CLI Workflow

The CLI has been updated to support the new full-stack architecture.

#### New Init Command
Create a complete SSR-ready project structure:
\`\`\`bash
dars init my-app --type ssr
\`\`\`
This generates:
- \`backend/\` directory with \`api.py\` and \`apiConfig.py\`
- \`main.py\` configured for SSR
- Dual-port setup for development

#### Development Environment
- **Frontend (Port 8000)**: Hot-reloading dev server.
- **Backend (Port 3000)**: SSR and API server.

The system allows you to configure the SSR backend URL dynamically:

\`\`\`python
# Automatically points to localhost:3000 in dev, and relative in prod
ssr_url = DarsEnv.get_urls()['backend']
app = App(ssr_url=ssr_url)
\`\`\`

---

# Release Notes v1.6.8

> **Component-Level State Updates with updateVRef()**

## Installation

\`\`\`bash
pip install --upgrade dars-framework
\`\`\`

## What's New

### updateVRef() - Pythonic Component-Level State

Dars Framework v1.6.8 introduces \`updateVRef()\`, a powerful new function for updating DOM values and component state without requiring State objects. This completes the component-level state management cycle alongside \`V()\`.

**The Complete Cycle:**
1. **Read**: \`V("#input")\` - Extract values (v1.5.8)
2. **Validate**: \`V("#input").length() >= 3\` - Boolean validation (v1.6.7)
3. **Update**: \`updateVRef("#input", "new value")\` - Update values (v1.6.8) **NEW!**

#### Before (v1.6.7) - Raw JavaScript

\`\`\`python
Button(
    "Increment",
    on_click=dScript("""
        const el = document.querySelector('#count');
        const current = parseInt(el.textContent);
        el.textContent = current + 1;
    """)
)
\`\`\`

#### After (v1.6.8) - Declarative Python

\`\`\`python
Button(
    "Increment",
    on_click=updateVRef("#count", V("#count").int() + 1)
)
\`\`\`

**Benefits:**
- **95% less code**
- **Type-safe** with V() expressions
- **Pythonic** - no inline JavaScript
- **Composable** - works with all V() features
- **Batch updates** - update multiple elements at once

---

### Key Features

#### 1. Simple Value Updates

Update any DOM element value with a single function call:

\`\`\`python
# Update text content
Button("Set Name", on_click=updateVRef("#name", "John Doe"))

# Update input value
Button("Clear", on_click=updateVRef("#email", ""))

# Update checkbox
Button("Check", on_click=updateVRef("#agree", True))

# Update number
Button("Set Price", on_click=updateVRef("#price", 99.99))
\`\`\`

#### 2. V() Expression Integration

Use V() expressions to create dynamic updates:

\`\`\`python
# Copy values
Button("Copy", on_click=updateVRef("#target", V("#source")))

# With transformations
Button("Uppercase", on_click=updateVRef("#output", V("#input").upper()))

# With calculations
Button("Calculate", on_click=updateVRef("#total",
    V("#price").float() * V("#qty").int()
))
\`\`\`

#### 3. Boolean Expression Support

Combine with boolean operators for conditional updates:

\`\`\`python
# Conditional text
Button("Check Age", on_click=updateVRef("#status",
    (V("#age").int() >= 18).then("Adult", "Minor")
))

# Validation messages
Button("Validate", on_click=updateVRef("#message",
    (V("#email").includes("@")).then("\u2713 Valid", "\u2717 Invalid")
))
\`\`\`

#### 4. Batch Updates

Update multiple elements with a single call:

\`\`\`python
# Clear form
Button("Clear All", on_click=updateVRef({
    "#name": "",
    "#email": "",
    "#age": ""
}))

# Fill sample data
Button("Fill Sample", on_click=updateVRef({
    "#name": "John Doe",
    "#email": "john@example.com",
    "#age": 25
}))
\`\`\`

---

### Complete Examples

#### Example 1: Counter (No State Object!)

\`\`\`python
from dars.all import *

@route("/counter")
def counter():
    return Page(
        Container(
            # Display count
            Text("0", id="count", style="text-[48px] font-bold"),
            
            # Update buttons
            Button("+", on_click=updateVRef("#count", V("#count").int() + 1)),
            Button("-", on_click=updateVRef("#count", V("#count").int() - 1)),
            Button("Reset", on_click=updateVRef("#count", 0))
        )
    )
\`\`\`

#### Example 2: Form Auto-Fill

\`\`\`python
@route("/form")
def form():
    return Page(
        Container(
            Input(id="first-name", placeholder="First Name"),
            Input(id="last-name", placeholder="Last Name"),
            Input(id="full-name", placeholder="Full Name", readonly=True),
            
            # Auto-generate full name
            Button(
                "Generate Full Name",
                on_click=updateVRef("#full-name",
                    V("#first-name") + " " + V("#last-name")
                )
            ),
            
            # Clear all
            Button(
                "Clear All",
                on_click=updateVRef({
                    "#first-name": "",
                    "#last-name": "",
                    "#full-name": ""
                })
            )
        )
    )
\`\`\`

#### Example 3: Shopping Cart Calculations

\`\`\`python
@route("/cart")
def cart():
    return Page(
        Container(
            Input(id="price", input_type="number", value="19.99"),
            Input(id="quantity", input_type="number", value="1"),
            Text("0", id="total"),
            
            # Calculate total
            Button(
                "Calculate Total",
                on_click=updateVRef("#total",
                    V("#price").float() * V("#quantity").int()
                )
            ),
            
            # Apply discount
            Button(
                "Apply 10% Discount",
                on_click=updateVRef("#total",
                    V("#total").float() * 0.9
                )
            )
        )
    )
\`\`\`

#### Example 4: Smart Validation

\`\`\`python
@route("/signup")
def signup():
    return Page(
        Container(
            Input(id="username", placeholder="Username"),
            Text("", id="username-status"),
            
            # Validate and normalize
            Button(
                "Validate Username",
                on_click=updateVRef("#username-status",
                    (V("#username").length() >= 3).then(
                        "\u2713 Valid username",
                        "\u2717 Too short (need 3+ characters)"
                    )
                )
            ),
            
            # Auto-fix: lowercase
            Button(
                "Normalize",
                on_click=updateVRef("#username",
                    V("#username").lower().trim()
                )
            )
        )
    )
\`\`\`

---

### API Reference

#### Signature

\`\`\`python
def updateVRef(
    selector: Union[str, Dict[str, Any]], 
    value: Any = None
) -> dScript
\`\`\`

**Parameters:**
- \`selector\`: CSS selector string or dict of {selector: value} pairs
- \`value\`: Value to set (string, number, bool, ValueRef, or expression)

**Returns:**
- \`dScript\` object for use in event handlers

**Supported Value Types:**
- Literals: \`"text"\`, \`42\`, \`True\`
- V() expressions: \`V("#source")\`
- Transformations: \`V("#input").upper()\`
- Math expressions: \`V("#a").int() + V("#b").int()\`
- Boolean expressions: \`(V("#age").int() >= 18).then("Adult", "Minor")\`

**Supported Elements:**
- \`Input\` / \`Textarea\`: Updates \`.value\` property
- \`Checkbox\` / \`Radio\`: Updates \`.checked\` property
- \`Select\`: Updates \`.value\` property
- Other elements: Updates \`.textContent\`

---

### Integration with Existing Features

#### With collect_form()

\`\`\`python
# Collect, validate, and update
form_data = collect_form(
    name=V("#name"),
    email=V("#email")
)

# Normalize before submit
Button(
    "Normalize & Submit",
    on_click=sequence(
        updateVRef({
            "#name": V("#name").trim(),
            "#email": V("#email").lower().trim()
        }),
        form_data.submit("http://localhost:3000/submit")
    )
)
\`\`\`

#### With Boolean Operators

\`\`\`python
# Smart updates based on validation
Button(
    "Update Status",
    on_click=updateVRef("#status",
        (V("#email").includes("@")).and_(
            V("#password").length() >= 8
        ).then("\u2713 Ready", "\u2717 Incomplete")
    )
)
\`\`\`

#### With State (Hybrid Approach)

\`\`\`python
# Local updates for UI
Button("Preview", on_click=updateVRef("#preview",
    "Name: " + V("#name") + ", Age: " + V("#age")
))

# Save to global state when ready
user = State("user", name="", age=0)
Button("Save", on_click=sequence(
    user.name.set(V("#name")),
    user.age.set(V("#age").int())
))
\`\`\`

---

## When to Use What

### Use \`updateVRef()\` when:
- Updating UI elements temporarily
- Form auto-fill and normalization
- Local calculations and previews
- Component-level state
- You don't need reactivity across components

### Use \`State.set()\` when:
- Data needs to persist
- Multiple components need the value
- You need automatic reactivity
- Application-level state

### Use both (Hybrid):
- Local updates for immediate feedback
- State updates for persistence
- Best of both worlds!

---

## Bug Fixes

- Fixed edge case in \`FormData\` where nested boolean expressions weren't properly serialized

---

## What's Next

Future enhancements planned for 1.7.0:
- \`useVRef()\` - Reactive V() expressions with dependencies
- \`setVRef()\` - Set values accessible via V() selectors
- Full exporter integration for reactive bindings
- Enhanced component-level reactivity

---

## Documentation

- **Hooks Guide**: Updated with updateVRef() examples and use cases
- **Operations Guide**: Enhanced with updateVRef() integration examples
- **Best Practices**: Added guidelines for component-level vs global state

---

# Release Notes v1.6.7

> **Boolean Operators, Form Collection & Backend Integration**

## Installation

\`\`\`bash
pip install --upgrade dars-framework
\`\`\`

## What's New

### Boolean & Comparison Operators for V()

Dars Framework v1.6.7 introduces a revolutionary declarative system for boolean logic and validation. Write complex conditionals in pure Python using comparison operators - **no inline JavaScript required!**

**Key Features:**
- **Comparison Operators** - Use Python operators (\`==\`, \`!=\`, \`>\`, \`<\`, \`>=\`, \`<=\`)
- **String Methods** - \`.includes()\`, \`.startswith()\`, \`.endswith()\`, \`.length()\`, \`.bool()\`
- **Logical Operators** - \`.and_()\` and \`.or_()\` for combining conditions
- **Conditional Expressions** - \`.then()\` for ternary operations
- **Type Safety** - Numeric comparisons require \`.int()\` or \`.float()\`

#### Before (v1.6.6) - Raw JavaScript

\`\`\`python
Button(
    "Validate",
    on_click=dScript("""
        const email = document.querySelector('#email').value;
        const age = parseInt(document.querySelector('#age').value);
        
        let valid = false;
        if (email.includes('@') && email.includes('.') && age >= 18 && age <= 120) {
            valid = true;
        }
        
        const message = valid ? '\u2713 Valid' : '\u2717 Invalid';
        
        window.Dars.change({
            id: 'form',
            dynamic: true,
            validation: message
        });
    """)
)
\`\`\`

#### After (v1.6.7) - Declarative Python

\`\`\`python
Button(
    "Validate",
    on_click=form.validation.set(
        (V("#email").includes("@")).and_(
            V("#email").includes(".")
        ).and_(
            V("#age").int() >= 18
        ).and_(
            V("#age").int() <= 120
        ).then("\u2713 Valid", "\u2717 Invalid")
    )
)
\`\`\`

**Benefits:**
- **90% less code**
- **Type-safe** with explicit transformations
- **Readable** - Python syntax
- **No inline JavaScript** - pure Python
- **Chainable** - combine multiple conditions

---

### Comparison Operators

\`\`\`python
# Numeric comparisons (require .int() or .float())
V("#age").int() >= 18
V("#price").float() < 100.0
V("#quantity").int() == 5

# String equality
V("#password") == V("#confirm-password")
V("#email") != ""

# All operators: ==, !=, >, <, >=, <=
\`\`\`

### String Methods

\`\`\`python
# Check if string contains substring
V("#email").includes("@")

# Check string start/end
V("#filename").startswith("report_")
V("#filename").endswith(".pdf")

# Get string length (returns ValueRef with .int())
V("#password").length() >= 8

# Convert to boolean
V("#checkbox").bool()
\`\`\`

### Logical Operators

\`\`\`python
# AND operator
(V("#age").int() >= 18).and_(V("#age").int() <= 65)

# OR operator
(V("#email").includes("@")).or_(V("#phone").length() >= 10)

# Complex combinations
(V("#name").length() >= 3).and_(
    (V("#email").includes("@")).and_(
        V("#email").includes(".")
    )
)
\`\`\`

### Conditional Expressions

\`\`\`python
# Simple conditional
(V("#age").int() >= 18).then("Adult", "Minor")

# With state updates
state.message.set(
    (V("#score").int() >= 60).then("Pass", "Fail")
)

# Complex validation
state.validation.set(
    (V("#password").length() >= 8).and_(
        V("#password") == V("#confirm")
    ).then("\u2713 Valid", "\u2717 Invalid")
)
\`\`\`

---

### Pythonic Form Collection System

**New in v1.6.7**: Collect and submit form data without writing a single line of JavaScript!

The new \`FormData\` class and \`collect_form()\` helper provide a completely declarative way to handle forms using \`V()\` expressions.

#### Basic Usage

\`\`\`python
from dars.all import *

# Collect form data with kwargs syntax
form_data = collect_form(
    name=V("#name-input"),
    email=V("#email-input"),
    age=V("#age-input").int(),
    is_premium=V("#premium-checkbox")
)

# Show in alert
Button("Submit", on_click=form_data.alert())

# Log to console
Button("Log", on_click=form_data.log())

# Save to state
Button("Save", on_click=form_data.to_state(state.data))
\`\`\`

#### Advanced Features

**Nested Dictionaries & Lists:**

\`\`\`python
form_data = collect_form(
    name=V("#name"),
    email=V("#email"),
    
    # Nested validation results
    validation={
        "email_valid": V("#email").includes("@"),
        "age_ok": (V("#age").int() >= 18).and_(
                   V("#age").int() <= 120)
    },
    
    # Conditional values
    discount=(V("#premium").bool()).then("10%", "0%"),
    
    # Timestamp
    submitted_at=getDateTime()
)
\`\`\`

#### FormData Methods

**\`.alert(title)\`** - Show form data in alert dialog

**\`.log(message)\`** - Log form data to console

**\`.to_state(property)\`** - Save form data to state

**\`.submit(url, state_property, on_success, on_error)\`** - Submit to backend via POST

**\`.submit_and_alert(state_property, title)\`** - Submit with alert

---

### Backend Integration

Submit forms to backend APIs with a single method call:

\`\`\`python
from dars.all import *

app = App("Form with Backend")
form = State("form", response="")

# Collect form data
form_data = collect_form(
    name=V("#name"),
    email=V("#email"),
    age=V("#age").int(),
    submitted_at=getDateTime()
)

@route("/")
def index():
    return Page(
        Container(
            Input(id="name", placeholder="Name"),
            Input(id="email", placeholder="Email"),
            Input(id="age", input_type="number", placeholder="Age"),
            
            # Submit to backend - NO RAW JAVASCRIPT!
            Button(
                "Submit to Backend",
                on_click=form_data.submit(
                    url="http://localhost:3000/submit",
                    state_property=form.response,
                    on_success=alert("Form submitted successfully!")
                )
            ),
            
            # Display backend response
            Container(
                Text("Backend Response:", style="font-bold"),
                Text(text=useDynamic("form.response"))
            )
        )
    )

app.add_page("index", index())
\`\`\`

**Features:**
- **Automatic JSON serialization**
- **State integration** - save response to state
- **Success/error callbacks**
- **CORS support**
- **Nested data structures**

---

### getDateTime() - Timestamp Helper

Generate client-side timestamps in multiple formats:

\`\`\`python
# Default ISO format
getDateTime()  # "2025-12-04T22:04:09.123Z"

# Different formats
getDateTime("iso")        # "2025-12-04T22:04:09.123Z"
getDateTime("locale")     # "12/4/2025, 10:04:09 PM"
getDateTime("date")       # "12/4/2025"
getDateTime("time")       # "10:04:09 PM"
getDateTime("timestamp")  # 1733362449123
\`\`\`

**Usage in Forms:**

\`\`\`python
form_data = collect_form(
    name=V("#name"),
    email=V("#email"),
    submitted_at=getDateTime()  # Automatic timestamp
)
\`\`\`

**Usage with State:**

\`\`\`python
Button("Save", on_click=state.last_updated.set(getDateTime()))
\`\`\`

---

## Complete Example

Here's a complete form validation and submission example using all new features:

\`\`\`python
from dars.all import *

app = App("Complete Form Demo")

form = State("form", 
    email_valid="",
    age_valid="",
    password_valid="",
    backend_response=""
)

# Collect form data
form_data = collect_form(
    name=V("#name"),
    email=V("#email"),
    age=V("#age").int(),
    password=V("#password"),
    confirm_password=V("#confirm"),
    
    # Nested validation
    validation={
        "email_valid": V("#email").includes("@"),
        "age_ok": (V("#age").int() >= 18).and_(
                   V("#age").int() <= 120),
        "password_strong": V("#password").length() >= 8,
        "passwords_match": V("#password") == V("#confirm")
    },
    
    # Timestamp
    submitted_at=getDateTime()
)

@route("/")
def index():
    return Page(
        Container(
            # Email validation
            Input(id="email", placeholder="Email"),
            Button(
                "Validate Email",
                on_click=form.email_valid.set(
                    (V("#email").includes("@")).and_(
                        V("#email").includes(".")
                    ).then("\u2713 Valid", "\u2717 Invalid")
                )
            ),
            Text(text=useDynamic("form.email_valid")),
            
            # Age validation
            Input(id="age", input_type="number", placeholder="Age"),
            Button(
                "Validate Age",
                on_click=form.age_valid.set(
                    (V("#age").int() >= 18).and_(
                        V("#age").int() <= 120
                    ).then("\u2713 Valid", "\u2717 Must be 18-120")
                )
            ),
            Text(text=useDynamic("form.age_valid")),
            
            # Password match
            Input(id="password", input_type="password", placeholder="Password"),
            Input(id="confirm", input_type="password", placeholder="Confirm"),
            Button(
                "Check Match",
                on_click=form.password_valid.set(
                    (V("#password") == V("#confirm")).and_(
                        V("#password").length() >= 8
                    ).then("\u2713 Match", "\u2717 No match")
                )
            ),
            Text(text=useDynamic("form.password_valid")),
            
            # Submit to backend
            Button(
                "Submit to Backend",
                on_click=form_data.submit(
                    url="http://localhost:3000/submit",
                    state_property=form.backend_response,
                    on_success=alert("Success!")
                )
            ),
            
            # Display response
            Text(text=useDynamic("form.backend_response"))
        )
    )

app.add_page("index", index())

if __name__ == "__main__":
    app.rTimeCompile()
\`\`\`

---

## Bug Fixes

### Fixed Transformation Chaining

Fixed a critical bug where \`.int()\` and \`.float()\` transformations were overwriting previous transformations instead of chaining them.

**Issue:**
\`\`\`python
# This was failing
V("#name").length() >= 4  # .length() was being overwritten
\`\`\`

**Fixed:**
\`\`\`python
# Now works correctly
V("#name").length() >= 4  # .length() chains with .int()
\`\`\`

### State.set() Expression Compatibility

Added \`to_dscript()\` method to \`BooleanExpression\`, \`ConditionalExpression\`, and \`LogicalExpression\` classes to make them compatible with \`State.set()\` calls.

---

## What's Next

Future enhancements planned for 1.7.0:
- \`useVRef()\` hook for reactive value references
- \`setVRef()\` hook for setting values
- \`updateVRef()\` helper for value updates
- Enhanced exporter integration
- More string methods (\`.replace()\`, \`.split()\`, \`.join()\`)
- Array operations

---

## Documentation

- **Hooks Guide**: Updated with boolean operators, form collection, and getDateTime
- **Operations Guide**: Enhanced with comparison and logical operators
- **Backend Integration**: New guide for form submission and API integration

---

# Release Notes v1.6.6

> **Custom Utility Styles & State Hot Reload Fix**

## Installation

\`\`\`bash
pip install --upgrade dars-framework
\`\`\`

## What's New

### Custom Utility Styles

You can now define your own utility classes in \`dars.config.json\` under the \`utility_styles\` key. This powerful feature allows you to:

- **Compose Utilities**: Combine multiple existing Dars utilities into a single class (e.g., \`btn-primary\`).
- **Use Raw CSS**: Mix standard CSS properties (e.g., \`border: 1px solid red\`) directly within your utility definitions.
- **Recursive Composition**: Build complex utilities by referencing other custom utilities.

**Example \`dars.config.json\`:**
\`\`\`json
{
  "utility_styles": {
    "btn-primary": ["bg-blue-600", "text-white", "p-3", "rounded-lg"],
    "card-fancy": ["bg-white", "shadow-lg", "border: 1px solid #e5e7eb"]
  }
}
\`\`\`

### Critical Fixes

- **State Hot Reload**: Fixed a critical issue where \`State\` objects were duplicated during hot reloads, leading to stale data and unpredictable behavior. The state registry is now properly cleared on every reload.
- **Border Utility Fallback**: Improved the parsing logic for \`border-\` utilities to correctly distinguish between Tailwind-like classes and raw CSS \`border:\` properties.

### Documentation

- **New Custom Utilities Guide**: Added comprehensive documentation for the new custom styling system in \`styling\`.
- **Configuration Reference**: Updated \`config\` with details on \`utility_styles\` and other configuration options.

---

# Release Notes v1.6.5

> **Massive Styling Expansion & SPA Fixes**

## Installation

\`\`\`bash
pip install --upgrade dars-framework
\`\`\`

## What's New

### Massive Styling System Expansion

Dars v1.6.5 brings a colossal update to the utility styling system, making it nearly feature-complete with modern utility-first CSS frameworks like Tailwind.

**New Features:**
- **Complete Color Palette**: Added full ranges (50-950) for \`cyan\`, \`teal\`, \`lime\`, \`amber\`, \`emerald\`, \`fuchsia\`, \`rose\`, \`zinc\`, \`neutral\`, and \`stone\`.
- **Direct Font Size**: New \`fs-[value]\` utility for setting exact font sizes (e.g., \`fs-[14px]\`).
- **Font Family**: New \`ffam-[value]\` utility for setting font families (e.g., \`ffam-sans\`, \`ffam-[Open_Sans]\`).
- **Transforms & Filters**: Full support for \`scale\`, \`rotate\`, \`translate\`, \`skew\`, \`blur\`, \`brightness\`, \`contrast\`, etc.
- **Backdrop Filters**: Added \`backdrop-blur\`, \`backdrop-brightness\`, etc.
- **Expanded Layout**: Added \`table\`, \`contents\`, \`flow-root\`, \`object-fit\`, \`z-index\`, and more.

### Critical Fixes for SPA Styling

Resolved a critical issue where \`hover_style\` and \`active_style\` were not being generated for Single Page Applications (SPA) using the \`@route\` decorator.

- **SPA Routes Support**: The CSS generator now correctly processes all SPA routes to generate state-based styles.
- **Multi-line CSS Fix**: Fixed an issue where multi-line CSS strings in utilities were not correctly parsed into valid CSS rules.

### Documentation Updates

- **New Styling Guide**: Complete reference for the new utility system in \`styling.md\`.
- **Operations Guide**: Detailed documentation for the Pythonic math expression system in \`operations.md\`.
- **Contributing Guide**: Added \`CONTRIBUTING.md\` for community guidelines.

---

# Release Notes v1.6.4

> **Pythonic Mathematical Expressions - Declarative Calculations**

## Installation

\`\`\`bash
pip install --upgrade dars-framework
\`\`\`

## What's New

### Pythonic Expression System with V()

Dars Framework v1.6.4 introduces a revolutionary declarative system for mathematical expressions. Write complex calculations in pure Python using operator overloading - **no inline JavaScript required!**

**Key Features:**
- **Operator Overloading** - Use Python operators (\`+\`, \`-\`, \`*\`, \`/\`, \`%\`, \`**\`)
- **Automatic Precedence** - Parentheses handled automatically
- **Dynamic Operators** - Operators from Select/Input elements
- **NaN Validation** - Safe handling of empty/invalid inputs
- **Type Safety** - Numeric operations require \`.float()\` or \`.int()\`

#### Before (v1.6.3) - Verbose JavaScript

\`\`\`python
Button(
    "Calculate",
    on_click=dScript(f"""
        const n1 = parseFloat(document.querySelector('.num1').value);
        const n2 = parseFloat(document.querySelector('.num2').value);
        const op = document.querySelector('.operation').value;
        
        let result = 0;
        switch(op) {{
            case '+': result = n1 + n2; break;
            case '-': result = n1 - n2; break;
            case '*': result = n1 * n2; break;
            case '/': result = n1 / n2; break;
        }}
        
        window.Dars.change({{
            id: 'calc',
            dynamic: true,
            result: result
        }});
    """)
)
\`\`\`

#### After (v1.6.4) - Declarative Python

\`\`\`python
Button(
    "Calculate",
    on_click=calc.result.set(
        V(".num1").float() + V(".operation").operator() + V(".num2").float()
    )
)
\`\`\`

**Benefits:**
- **less code**
- **Type-safe** with explicit transformations
- **NaN validation** with console warnings
- **Pythonic syntax** - feels natural
- **No inline JavaScript** - pure Python

---

### Mathematical Operations

#### Simple Arithmetic

\`\`\`python
# Addition
calc.total.set(V(".price").float() + V(".tax").float())

# Subtraction
calc.change.set(V(".paid").float() - V(".total").float())

# Multiplication
calc.total.set(V(".price").float() * V(".quantity").int())

# Division
calc.average.set(V(".sum").float() / V(".count").int())
\`\`\`

#### Complex Expressions with Automatic Precedence

\`\`\`python
# a + b * c  \u2192  a + (b * c)  \u2705 Automatic
calc.result.set(
    V(".a").float() + V(".b").float() * V(".c").float()
)

# (a + b) * c  \u2192  (a + b) * c  \u2705 Preserved
calc.result.set(
    (V(".a").float() + V(".b").float()) * V(".c").float()
)

# With literals
calc.total.set(
    (V(".price").float() * V(".qty").int()) * 1.15  # Add 15% tax
)
\`\`\`

**Precedence Table:**

| Operator | Precedence | Associativity |
|----------|------------|---------------|
| \`**\`     | 3 (highest)| Right         |
| \`*\`, \`/\`, \`%\` | 2     | Left          |
| \`+\`, \`-\` | 1 (lowest) | Left          |

---

### Dynamic Operators

Use operators from Select or Input elements with the new \`.operator()\` method:

\`\`\`python
from dars.all import *

calc = State("calc", operation="+", result=0)

@route("/")
def index():
    return Page(
        # Operation selector
        Select(
            value=useValue("calc.operation", selector=".operation"),
            class_name="operation",
            options=[
                SelectOption("+", "\u2795 Add"),
                SelectOption("-", "\u2796 Subtract"),
                SelectOption("*", "\u2716\uFE0F Multiply"),
                SelectOption("/", "\u2797 Divide")
            ]
        ),
        
        # Number inputs
        Input(class_name="num1", input_type="number"),
        Input(class_name="num2", input_type="number"),
        
        # Declarative calculation!
        Button(
            "Calculate",
            on_click=calc.result.set(
                V(".num1").float() + V(".operation").operator() + V(".num2").float()
            )
        ),
        
        # Result display
        Text(text=useDynamic("calc.result"))
    )
\`\`\`

**How it works:**
1. \`V(".operation").operator()\` extracts the operator value
2. Validates against whitelist: \`+\`, \`-\`, \`*\`, \`/\`, \`%\`, \`**\`
3. Uses switch statement for safe evaluation
4. Falls back to \`+\` if invalid (with console warning)

---

### NaN Validation

All mathematical expressions include automatic NaN validation:

\`\`\`python
# Empty inputs automatically return 0
Button(
    "Calculate",
    on_click=calc.result.set(
        V(".num1").float() + V(".num2").float()
    )
)
# Empty inputs \u2192 Returns 0
# Console: "[Dars] Invalid input: one or more values are NaN. Returning 0."
\`\`\`

**Validation Points:**
1. **Input Validation** - Checks operands before calculation
2. **Result Validation** - Checks result after calculation
3. **Console Logging** - Warns when NaN is detected

---

### Enhanced Select Component

- **useValue Support** - Set initial value from state with selector
- **Proper Value Handling** - Correctly selects option based on initial value
- **Selector Integration** - Works seamlessly with \`V()\` for value extraction

\`\`\`python
Select(
    value=useValue("calc.operation", selector=".operation"),
    class_name="operation",
    options=[...]
)
\`\`\`

---

## What's Next

Future enhancements planned for 1.7.0:
- Comparison operators (\`>\`, \`<\`, \`==\`, \`!=\`)
- Logical operators (\`and\`, \`or\`, \`not\`)
- Ternary operator support
- Array/list operations
- Math functions (\`.abs()\`, \`.round()\`, \`.sqrt()\`, etc.)

---

# Release Notes v1.6.3


> **Tailwind-like Utility Class System**

## Installation

\`\`\`bash
pip install --upgrade dars-framework
\`\`\`

## What's New

### Tailwind-like Utility Class System

Dars Framework now includes a powerful, Python-native utility class system inspired by Tailwind CSS. You can style your components using concise utility strings directly in your Python code, without any external build tools or Node.js dependencies.

**Key Features:**
- **Zero Configuration**: Works out of the box.
- **Python-Native**: Parsed at runtime/export time into standard CSS.
- **No Node.js**: No need for npm, PostCSS, or Tailwind CLI.
- **Type-Safe**: Integrated directly into \`Component\` props.

**Example:**

\`\`\`python
from dars.all import *

def MyComponent():
    return Container(
        Text("Hello, Dars!"),
        style="bg-blue-500 p-4 rounded-lg shadow-md hover:bg-blue-600 transition-all",
        hover_style="scale-105",
        active_style="scale-95"
    )
\`\`\`

### Supported Utilities

The system supports a wide range of utilities including:
- **Layout**: \`flex\`, \`grid\`, \`block\`, \`hidden\`, \`flex-row\`, \`justify-center\`, \`items-center\`, \`gap-4\`
- **Spacing**: \`p-4\`, \`m-4\`, \`px-2\`, \`py-2\` (using rem units)
- **Sizing**: \`w-full\`, \`h-screen\`, \`w-1/2\`, \`max-w-md\`
- **Typography**: \`text-xl\`, \`font-bold\`, \`text-center\`, \`text-blue-500\`
- **Backgrounds**: \`bg-red-500\`, \`bg-gray-100\`
- **Borders**: \`border\`, \`border-2\`, \`rounded-lg\`, \`rounded-full\`
- **Effects**: \`shadow-md\`, \`opacity-50\`, \`cursor-pointer\`

### Arbitrary Values

For values not in the standard scale, use square brackets:
\`\`\`python
style="w-[350px] bg-[#1a2b3c] z-[100] top-[50px]"
\`\`\`

### State Integration

Utility strings work seamlessly with Dars State management for dynamic styling:

\`\`\`python
state = State("theme", style="bg-gray-100 p-4")

Container(
    "Content",
    style=useDynamic("theme.style"),  # Binds directly to the utility string
)
\`\`\`

---

# Release Notes v1.6.2

> **useValue Enhancements & Critical Hot Reload Fixes**

## Installation

\`\`\`bash
pip install --upgrade dars-framework
\`\`\`

## What's New

### Enhanced \`useValue\` Hook - Simplified Usage

The \`useValue\` hook has been improved to support direct usage in built-in components without requiring a selector. This makes it easier to set initial (non-reactive) values from state.

**Simplified Syntax:**
\`\`\`python
# Before (required selector)
Text(text=useValue("user.name", ".my-text"))

# Now (selector optional)
Text(text=useValue("user.name"))
\`\`\`

This is perfect for initializing components with state values that don't need to update reactively or be extracted back later.

### Critical Bug Fixes

#### \`useDynamic\` Numeric Value Display
Fixed an issue where \`useDynamic\` would display internal marker strings (e.g., \`__DARS_DYNAMIC_...\`) instead of the actual value when the state property was a number (especially \`0\`). Numeric values are now correctly resolved and displayed in both initial render and reactive updates.

#### State Hot Reloading Fix
Resolved a critical issue where state changes were not reflected after a hot reload. The state registry now correctly deduplicates state objects, ensuring that the most recent version of the state is always used. This fixes cases where changing a default value in code (e.g., \`count=0\` to \`count=2\`) wouldn't update the UI.

---

# Release Notes v1.6.1

> **Side Effects System Enhancement - useWatch Arrays & Multiple Callbacks**

## Installation

\`\`\`bash
pip install --upgrade dars-framework
\`\`\`

## What's New

### Enhanced useWatch Hook - Array Syntax & Multiple Callbacks

The \`useWatch\` hook now supports watching multiple state properties simultaneously and executing multiple callbacks, enabling powerful reactive patterns and side effects.

**Watch Multiple State Properties:**
\`\`\`python
# Watch multiple properties - callback executes when ANY of them change
app.useWatch(
    ["product.name", "product.price"],
    productState.info.set("Product: " + V("product.name") + " - $" + V("product.price"))
)
\`\`\`

**Multiple Callbacks:**
\`\`\`python
# Execute multiple callbacks when state changes
app.useWatch(
    "cart.total",
    log("Total changed!"),
    alert("Cart updated")
)

# Combine array syntax with multiple callbacks
app.useWatch(
    ["product.name", "product.price"],
    productState.info.set("Product: " + V("product.name") + " - $" + V("product.price")),
    log("Product info updated")
)
\`\`\`

**Key Features:**
- **Array Syntax**: Watch multiple state paths with a single watcher
- **Multiple Callbacks**: Execute multiple side effects in sequence
- **Reactive Composition**: Automatically sync derived state when source properties change
- **Clean API**: Simple comma-separated syntax for callbacks

### Bug Fixes

#### Fixed Custom State Property Handling

Resolved an issue where custom state properties (properties other than \`text\`, \`html\`, \`style\`, \`attrs\`) were not correctly triggering watchers when updated via \`change()\`.

**What was fixed:**
- Custom properties like \`info\`, \`count\`, \`status\` now correctly update in \`st.values\`
- Watchers for custom properties now trigger reliably
- State registry properly maintains current values for all properties

**Example that now works correctly:**
\`\`\`python
productState = State("product", name="Milk", price=100, info="")

# This now correctly updates product.info when name or price changes
app.useWatch(
    ["product.name", "product.price"],
    productState.info.set("Product: " + V("product.name") + " - $" + V("product.price"))
)
\`\`\`

#### Improved V() Helper State Access

The \`V()\` helper now correctly retrieves current state values from the state registry instead of reading stale values from the DOM.

**Previous Behavior:**
- \`V("product.name")\` would read the displayed text from the DOM
- This could lead to recursive string concatenation issues
- Values might not reflect the actual state

**Fixed Behavior:**
- \`V("product.name")\` now reads directly from \`window.Dars.getState('product').values['name']\`
- Always returns the current, raw state value
- Falls back to DOM reading for legacy support

---

# Release Notes v1.6.0


> **Critical Bug Fixes & State Management Improvements**

## Installation

\`\`\`bash
pip install --upgrade dars-framework
\`\`\`

## What's Fixed

### 1. Hook Initialization Fixes

Fixed critical bugs where \`useDynamic\` and \`useValue\` hooks were not properly displaying default values from \`State\` objects when used in \`FunctionComponent\`s.

**Issues Resolved:**
- \`useDynamic\` now correctly retrieves default values from the state registry even when props are not explicitly passed to the component
- \`useValue\` now works correctly without requiring a selector parameter
- Both hooks properly display initial state values on first render

**Example:**
\`\`\`python
# This now works correctly!
state = State("ui", count=0, disabled=False)

@FunctionComponent
def Counter(**props):
    return f'''
        <div>
            <p>Count: {useDynamic("ui.count")}</p>
            <button disabled="{useDynamic("ui.disabled")}">Click</button>
        </div>
    '''
\`\`\`

### 2. State Reset Functionality Enhancement

Completely rewrote the \`reset()\` function to correctly handle **all** component properties, including boolean attributes like \`checked\`, \`disabled\`, \`readonly\`, and \`required\`.

**Previous Behavior:**
- Boolean attributes were incorrectly set to \`"false"\` string instead of being removed
- Properties like \`disabled="false"\` would still disable elements (incorrect HTML behavior)

**Fixed Behavior:**
- Boolean attributes are now properly removed when \`False\`
- Both HTML attributes AND DOM properties are synchronized correctly
- Works for: \`checked\`, \`disabled\`, \`readonly\`, \`required\`, \`selected\`, \`autofocus\`, \`autoplay\`, \`controls\`, \`loop\`, \`muted\`

**Example:**
\`\`\`python
state = State("ui", is_disabled=False, is_checked=True)

Button(disabled=useDynamic("ui.is_disabled"))
Checkbox(checked=useDynamic("ui.is_checked"))

# Reset now works perfectly
Button("Reset All", on_click=state.reset())
\`\`\`

### 3. JavaScript Variable Name Sanitization

Fixed \`SyntaxError\` in generated JavaScript caused by HTML IDs containing hyphens being used as variable names.

**Issue:**
\`\`\`javascript
// Generated invalid JS
const el_control-panel = ...  // SyntaxError!
\`\`\`

**Fixed:**
\`\`\`javascript
// Now generates valid JS
const el_control_panel = ...  // \u2713 Valid
\`\`\`

### 4. Boolean Attribute Handling Improvements

Enhanced the reactive binding system to properly handle boolean attributes with the \`is_\` prefix.

**Supported Patterns:**
\`\`\`python
# All of these now work correctly
state = State("ui", is_disabled=False, disabled=False)

# Automatic mapping: is_disabled -> disabled attribute
Button(disabled=useDynamic("ui.is_disabled"))

# State changes properly update the DOM
state.is_disabled.set(True)   # Adds disabled attribute
state.is_disabled.set(False)  # Removes disabled attribute completely
\`\`\`

## Important Notes

### State ID Best Practices

> **[!IMPORTANT] When using \`State\` objects with hooks like \`useDynamic\` and \`useValue\`, the state ID should **NOT** match any component ID in your DOM. The state ID is a unique identifier for the state object itself, not a component.**

**X Incorrect:**
\`\`\`python
# DON'T do this - state ID matches button ID
state = State("my-button", count=0)
Button(id="my-button", text=useDynamic("my-button.count"))
\`\`\`

**\u2713 Correct:**
\`\`\`python
# DO this - state has unique ID
state = State("counter-state", count=0)
Button(id="my-button", text=useDynamic("counter-state.count"))
\`\`\`

The reactive system uses watchers to update components when state changes, so the state ID doesn't need to (and shouldn't) match any specific component ID.

## Technical Details

### Changes to \`js_lib.py\`

1. **\`change()\` function**: Added intelligent boolean attribute detection with \`is_\` prefix support
2. **\`_applyMods()\` function**: Enhanced to handle boolean attributes in state modifications
3. **\`_restoreDefault()\` function**: Improved to correctly restore boolean attributes to their initial state

### Changes to \`html_css_js.py\`

1. **\`_generate_reactive_bindings_js()\`**: Added boolean attribute handling in watcher code generation
2. **Variable name sanitization**: Replaces hyphens with underscores in generated JS variable names
3. **\`_process_function_component()\`**: Added fallback to \`STATE_V2_REGISTRY\` for missing prop values

### Changes to \`use_value.py\`

1. **\`ValueMarker.__init__()\`**: Now always registers markers, even without a selector

---

# Release Notes v1.5.9

> **Unified Keyboard Events & KeyCode System**

## Installation

\`\`\`bash
pip install --upgrade dars-framework
\`\`\`

## What's New

### 1. Unified Keyboard Events (\`on_key_press\`)

Simplified keyboard event handling by consolidating \`on_key_down\` and \`on_key_up\` into a single, robust **\`on_key_press\`** event. This ensures consistent behavior across all components and browsers.

**Deprecated:**
- \`on_key_down\`
- \`on_key_up\`

**New Standard:**
\`\`\`python
Input(on_key_press=log("Key pressed!"))
\`\`\`

### 2. The \`KeyCode\` System

No more magic strings or numbers! The new \`KeyCode\` class provides constants for all keyboard keys, making your code readable and maintainable.

\`\`\`python
from dars.all import KeyCode

# Use constants
KeyCode.ENTER
KeyCode.ESCAPE
KeyCode.TAB
KeyCode.SPACE
KeyCode.A
KeyCode.F1
\`\`\`

### 3. Powerful Helpers: \`onKey\`, \`switch\`, \`addGlobalKeys\`

Introduced three powerful helpers to make keyboard handling elegant and Pythonic.

#### \`onKey()\` - Single Key Handler
Handle specific keys with optional modifiers easily:

\`\`\`python
# Simple
Input(on_key_press=onKey(KeyCode.ENTER, submit_form()))

# With Modifiers
Container(on_key_press=onKey(KeyCode.S, save(), ctrl=True))
\`\`\`

#### \`switch()\` - Multiple Key Handler
Handle multiple keys in a single component without messy if-statements:

\`\`\`python
Input(on_key_press=switch({
    KeyCode.ENTER: submit_form(),
    KeyCode.ESCAPE: clear_form(),
    KeyCode.TAB: focus_next()
}))
\`\`\`

#### \`addGlobalKeys()\` - App-wide Shortcuts
Register global keyboard shortcuts that work anywhere in your app:

\`\`\`python
addGlobalKeys(app, {
    (KeyCode.S, 'ctrl'): save_document(),
    (KeyCode.Z, 'ctrl'): undo(),
    (KeyCode.Z, 'ctrl', 'shift'): redo()
})
\`\`\`

### 4. Documentation

A comprehensive guide to the new system is available in \`KeyEvents.md\`, covering everything from basic usage to advanced global shortcuts and best practices.

## Migration Guide

**From \`on_key_down\` / \`on_key_up\`:**
Simply rename your event handlers to \`on_key_press\`. The underlying behavior uses \`keydown\` for maximum reliability.

\`\`\`python
# Before
Input(on_key_down=dScript("..."))

# After
Input(on_key_press=dScript("..."))
\`\`\`

---

# Release Notes v1.5.8

> **Enhanced V() Helper & useValue Selector Support**

## Installation

\`\`\`bash
pip install --upgrade dars-framework
\`\`\`

## What's New

### 1. V() Helper - State Path Support

The \`V()\` helper now supports extracting values from **reactive state** in addition to DOM elements!

#### State Path Extraction

\`\`\`python
# Extract from reactive state created by useDynamic()
V("cart.total")      # Gets current value of cart.total
V("user.name")       # Gets current value of user.name
V("product.price")   # Gets current value of product.price
\`\`\`

**How it works:**
- \`V("cart.total")\` finds the reactive element created by \`useDynamic("cart.total")\`
- Reads its current \`textContent\` value
- Perfect for combining reactive state with calculations

#### Complete Integration Example

\`\`\`python
from dars.all import *

productState = State("product", price=19.99, quantity=1, total=19.99)

@FunctionComponent
def ProductCard(**props):
    return f'''
    <div {Props.id}>
        <p>Price: \${useDynamic("product.price")}</p>
        <input type="number" value="{useValue("product.quantity", ".qty-input")}" />
        <p>Total: \${useDynamic("product.total")}</p>
    </div>
    '''

# Calculate total: DOM input \xD7 State value
Button("Calculate", on_click=productState.total.set(
    V(".qty-input").int() * V("product.price").float()
))
\`\`\`

### 2. V() Helper - Arithmetic Operator Validation

**Breaking Change (Validation)**: Arithmetic operators now **require** numeric transformations to prevent bugs.

#### The Problem

Previously, you could accidentally multiply strings:
\`\`\`python
# Before: This would concatenate strings, not multiply!
V("#price") * V("#qty")  # "19.99" * "5" = NaN or unexpected behavior
\`\`\`

#### The Solution

Arithmetic operators (\`*\`, \`/\`, \`-\`, \`%\`, \`**\`) now require \`.int()\` or \`.float()\`:

\`\`\`python
# CORRECT - With transformations
V("#price").float() * V("#qty").int()  # 19.99 * 5 = 99.95

# ERROR - Without transformations
V("#price") * V("#qty")
# TypeError: Multiplication requires numeric transformation.
#            Use V('#price').int() or V('#price').float() before multiplying.
\`\`\`

**String concatenation (\`+\`) still works without transformations:**
\`\`\`python
# Always allowed
V("#first") + " " + V("#last")  # String concatenation
"Total: $" + V("cart.total")    # String concatenation
\`\`\`

**Supported Operators:**
- \`+\` - Addition/Concatenation (always allowed)
- \`*\` - Multiplication (requires \`.int()\` or \`.float()\`)
- \`/\` - Division (requires \`.int()\` or \`.float()\`)
- \`-\` - Subtraction (requires \`.int()\` or \`.float()\`)
- \`%\` - Modulo (requires \`.int()\` or \`.float()\`)
- \`**\` - Power (requires \`.int()\` or \`.float()\`)

### 3. useValue() - Selector Support in FunctionComponents

\`useValue()\` now supports automatic selector application in FunctionComponents!

#### Automatic Selector Application

\`\`\`python
@FunctionComponent
def UserForm(**props):
    return f'''
    <div {Props.id}>
        <input value="{useValue("user.name", ".name-input")}" />
        <input value="{useValue("user.email", "#email-field")}" />
    </div>
    '''

# Extract values using the selectors
Button("Save", on_click=userState.name.set(V(".name-input")))
\`\`\`

**How it works:**
1. \`useValue("user.name", ".name-input")\` sets initial value AND applies class \`name-input\`
2. \`V(".name-input")\` extracts the current value (even if modified by user)
3. Perfect for forms with initial values and value extraction

**Supported selectors:**
- **Class selectors** (\`.foo\`) \u2192 Added to element's \`class\` attribute
- **ID selectors** (\`#bar\`) \u2192 Set as element's \`id\` attribute

---

## Migration Guide

### V() Arithmetic Operations

If you were using arithmetic operators without transformations, add \`.int()\` or \`.float()\`:

**Before:**
\`\`\`python
state.total.set(V("#price") * V("#qty"))
\`\`\`

**After:**
\`\`\`python
state.total.set(V("#price").float() * V("#qty").int())
\`\`\`

**String concatenation is unchanged:**
\`\`\`python
# Still works the same
state.fullname.set(V("#first") + " " + V("#last"))
\`\`\`

---

## Complete Example

\`\`\`python
from dars.all import *

app = App("Shopping Cart")

# Reactive state
cartState = State("cart", total=0.0)
productState = State("product", name="Widget", price=19.99, quantity=1)

@FunctionComponent
def ProductCard(**props):
    return f'''
    <div {Props.id} {Props.class_name} {Props.style}>
        <!-- Reactive display -->
        <h3>{useDynamic("product.name")}</h3>
        <p>Price: \${useDynamic("product.price")}</p>
        
        <!-- Editable quantity with selector -->
        <input type="number" 
               value="{useValue("product.quantity", ".qty-input")}"
               min="1" />
        
        <!-- Reactive total -->
        <p>Total: \${useDynamic("cart.total")}</p>
    </div>
    '''

@route("/")
def index():
    return Page(
        ProductCard(id="product-card", name="Milk", price=100, quantity=2, total=0),
        
        # Calculate: DOM input \xD7 State value
        Button("Calculate Total", on_click=cartState.total.set(
            V(".qty-input").int() * V("product.price").float()
        )),
        
        # String concatenation (no transformation needed)
        Button("Show Info", on_click=productState.name.set(
            "Product: " + V("product.name") + " - $" + V("product.price")
            )
        )
    )

app.add_page("index", index(), title="Product", index=True)

# Watch for changes
app.useWatch("cart.total", log("Cart total changed!"))

if __name__ == "__main__":
    app.rTimeCompile()
\`\`\`

---

## Bug Fixes

### useValue Selector Application
- **Issue**: Selectors in \`useValue()\` were not being applied to FunctionComponent elements
- **Fix**: Implemented BeautifulSoup-based HTML parsing to detect and apply selectors
- **Impact**: \`useValue()\` now works identically in FunctionComponents and built-in components

### V() State Path Detection
- **Issue**: No way to extract values from reactive state without DOM elements
- **Fix**: Added intelligent state path detection (e.g., \`"cart.total"\` vs \`".cart-total"\`)
- **Impact**: Seamless integration between \`useDynamic()\`, \`useValue()\`, and \`V()\`

---

## Breaking Changes

### Arithmetic Operator Validation

**Change**: Arithmetic operators (\`*\`, \`/\`, \`-\`, \`%\`, \`**\`) now require \`.int()\` or \`.float()\` transformations.

**Reason**: Prevents accidental string operations that cause bugs.

**Migration**: Add \`.int()\` or \`.float()\` before arithmetic operations:
\`\`\`python
V("#price").float() * V("#qty").int()
\`\`\`

**Note**: String concatenation (\`+\`) is unchanged and still works without transformations.

---

## Documentation Updates

- **hooks.md**: Comprehensive V() documentation with state path examples
- **custom_components.md**: Updated examples showing V() with state paths
- **New examples**: Complete integration patterns for \`useValue()\`, \`useDynamic()\`, and \`V()\`

---

## What's Next

The enhanced V() helper and complete hooks integration pave the way for more advanced reactive patterns and seamless state management in future releases.

---

# Release Notes v1.5.7

> **useValue hook & Value Access Helpers**

## Installation

\`\`\`bash
pip install --upgrade dars-framework
\`\`\`

## What's New

### 1. \`useValue\` Hook

The new \`useValue\` hook allows you to access the **initial value** of a state property without creating a reactive binding. This is perfect for form inputs where you want to set a default value but allow the user to edit it freely.

\`\`\`python
# Initial value from state, but editable by user
Input(value=useValue("user.name"))

# In FunctionComponent templates (resolves to initial value string)
@FunctionComponent
def Profile(**props):
    return f"<div>{useValue('user.name')}</div>"
\`\`\`

### 2. Pythonic Helpers (\`V\`, \`url\`, \`transform\`)

Introducing a set of helpers to make working with DOM values completely Pythonic, eliminating the need for \`RawJS\`.

#### V() - Value Reference
Select DOM elements and perform operations directly in Python:

\`\`\`python
# Concatenation
Button("Combine", on_click=state.fullname.set(
    V("#first") + " " + V("#last")
))

# Transformations
Button("Upper", on_click=state.name.set(V("#name").upper()))
Button("Add", on_click=state.count.set(V("#num1").int() + 10))
\`\`\`

#### url() - URL Builder
Construct dynamic URLs easily with proper interpolation:

\`\`\`python
Button("Fetch", on_click=fetch(
    url("https://api.example.com/users/{id}", id=V("#userId"))
))
\`\`\`

### Stability
- **Fix**: Resolved an issue where reactive bindings could generate duplicate JavaScript variables, causing "Identifier has already been declared" errors during hot reloads or complex state updates.

# Release Notes v1.5.6

> **Enhanced \`useDynamic\` Support & StateV2 Fixes**

## Installation

\`\`\`bash
pip install --upgrade dars-framework
\`\`\`

## What's New

### 1. Expanded \`useDynamic\` Support for Built-in Components

\`useDynamic\` now works with **all properties** of built-in components, including:

#### Image & Link Components
\`\`\`python
# Dynamic image source and alt text
Image(
    src=useDynamic("product.imageUrl"),
    alt=useDynamic("product.name")
)

# Dynamic link href and text
Link(
    href=useDynamic("navigation.url"),
    text=useDynamic("navigation.label")
)
\`\`\`

#### Boolean Attributes
All boolean attributes now support dynamic binding:
\`\`\`python
# Dynamic disabled state
Button(
    text="Submit",
    disabled=useDynamic("form.isSubmitting")
)

# Dynamic checked state
Checkbox(
    checked=useDynamic("settings.notifications"),
    label="Enable Notifications"
)

# Dynamic readonly and required
Input(
    value=useDynamic("user.email"),
    readonly=useDynamic("form.isLocked"),
    required=useDynamic("form.emailRequired")
)
\`\`\`

**Supported Boolean Properties:**
- \`disabled\` - Button, Input, Textarea, Checkbox, RadioButton, Select, Slider
- \`checked\` - Checkbox, RadioButton
- \`readonly\` - Input, Textarea
- \`required\` - Input, Textarea, Checkbox, RadioButton, Select

### 2. StateV2 \`increment()\` & \`decrement()\` Fixes

Fixed critical issues with \`StateV2\` reactive operations:

#### Fixed Validation Error
Previously, \`increment()\` and \`decrement()\` only worked on properties named \`text\`. Now they work on **any numeric property**:

\`\`\`python
# Before: This would error
state = State("counter", count=0)
Button("Increment", on_click=state.count.increment(by=1))  # \u274C ValueError

# After: Works perfectly!
state = State("counter", count=0)
Button("Increment", on_click=state.count.increment(by=1))  # \u2705 Works!
\`\`\`

#### Fixed Persistence Issue
Increment/decrement operations now correctly persist across multiple clicks:

\`\`\`python
state = State("counter", count=0)

# Before: Would increment 0\u21921, then stay at 1 forever
# After: Correctly increments 0\u21921\u21922\u21923\u2192...
Button("Increment", on_click=state.count.increment(by=1))
Button("Decrement", on_click=state.count.decrement(by=1))
\`\`\`

**Technical Details:**
- Implemented client-side state value tracking in \`window.Dars.getState()\`
- State registry now maintains current values for all properties
- \`increment()\`/\`decrement()\` use \`window.Dars.change()\` for proper state updates
- Watchers and UI updates now trigger correctly on every operation

### 3. Documentation Updates

#### Enhanced Hooks Documentation
- Added comprehensive "Supported Properties" table showing which properties work with \`useDynamic\` for each component type
- Documented boolean attribute support

#### New Component Documentation
Added documentation for visualization components in \`components.md\`:

**Chart Component:**
\`\`\`python
import plotly.graph_objects as go

fig = go.Figure(data=[go.Bar(x=['A', 'B', 'C'], y=[1, 3, 2])])
Chart(figure=fig, width="100%", height="400px")
\`\`\`

**DataTable Component:**
\`\`\`python
import pandas as pd

df = pd.DataFrame({
    'Name': ['Alice', 'Bob'],
    'Age': [25, 30]
})
DataTable(data=df, theme="striped", page_size=10)
\`\`\`

## Bug Fixes

### StateV2 Increment/Decrement
- **Issue**: \`increment()\` raised \`ValueError\` for non-\`text\` properties
- **Fix**: Validation now checks if value is numeric (\`int\` or \`float\`) instead of checking property name
- **Impact**: All numeric state properties can now use \`increment()\` and \`decrement()\`

### StateV2 State Persistence
- **Issue**: Increment operations stuck at first value (0\u21921, then stayed at 1)
- **Fix**: Implemented proper client-side state tracking and payload structuring
- **Impact**: Reactive operations now work correctly across multiple invocations

## Breaking Changes

None.

---


## What's Next

The enhanced \`useDynamic\` system and robust StateV2 operations pave the way for more advanced reactive patterns and state management features in future releases.

---

# Release Notes v1.5.5


> **Hooks System Enhanced**: \`useDynamic\` for built-in components and new \`useWatch\` hook.

## Installation

\`\`\`bash
pip install --upgrade dars-framework
\`\`\`

## What's New

### 1. \`useDynamic\` for Built-in Components

You can now use \`useDynamic\` directly in properties of built-in components!

\`\`\`python
# Bind directly to component props
Text(text=useDynamic("user.name"))
Input(value=useDynamic("user.name"))
Button(text=useDynamic("user.status"))
\`\`\`

This works for \`Text\`, \`Button\`, \`Input\`, \`Textarea\`, and more.

### 2. New \`useWatch\` Hook
Monitor state changes and execute side effects with \`useWatch\`.

\`\`\`python
# Global watcher
app.useWatch("cart.total", log("Cart updated!"))

# Page-specific watcher
@route("/cart")
def cart_page():
    page = Page()
    page.useWatch("cart.total", log("Total changed!"))
    return page
\`\`\`

New methods \`app.useWatch()\` and \`page.useWatch()\` make integration seamless.

### 3. Fixes

- Fixed execution order in exporter to ensure reactive bindings are generated correctly.
- Improved state initialization for dynamic props.

---

# Release Notes v1.5.4 (Relaunch from 1.5.3)

> **Hooks System & Reactive Bindings** relaunch with correct license.

## Installation

\`\`\`bash
pip install --upgrade dars-framework
\`\`\`

## What's New

### Hooks System - \`useDynamic()\`

Dars Framework introduces its **first hook** - \`useDynamic()\` - enabling reactive state bindings in FunctionComponents!

#### Reactive State Bindings

Create components that automatically update when state changes:

\`\`\`python
from dars.all import *

# Create state
userState = State("user", name="John Doe", email="john@example.com")

# Use useDynamic in FunctionComponent
@FunctionComponent
def UserCard(**props):
    return f'''
    <div {Props.id} {Props.class_name} {Props.style}>
        <h3>{useDynamic("user.name")}</h3>
        <p>{useDynamic("user.email")}</p>
    </div>
    '''

# Render
card = UserCard(id="userCard")

# Update - DOM automatically reacts!
app.add_script(userState.name.set("Jane Doe"))  # UI updates instantly
\`\`\`

#### How It Works

1. **Initial Render**: \`useDynamic()\` inserts reactive spans with initial prop values
2. **State Changes**: When you call \`.set()\`, the hook intercepts the change
3. **Auto Updates**: All matching reactive spans update automatically

#### Key Features

- **Zero boilerplate** - Just use \`useDynamic("state.property")  in templates
- **Automatic updates** - No manual DOM manipulation needed
- **Multiple bindings** - Multiple components can bind to the same state
- **State V2 integration** - Works seamlessly with dynamic state system

---

### \`getInputValue()\` Utility

New utility function specifically designed for State V2 integration:

\`\`\`python
state = State("product", title="", price=0)

Button("Save", on_click=[
    state.title.set(getInputValue("titleInput")),
    state.price.set(getInputValue("priceInput"))
])
\`\`\`

**Features:**
- Returns input value as JavaScript expression
- Works with \`State.set()\` and other dynamic operations
- Optional \`parent_id\` parameter for scoped searches
- Complements existing \`getValue()\` for assignments

**Difference from \`getValue()\`:**
- \`getValue(input_id, target_id)\` - Performs assignment (sets textContent)
- \`getInputValue(input_id)\` - Returns value expression (for State.set())

---

### CSS Improvements

#### Modern Default Styles

- Updated all component CSS to use CSS variables for easy theming
- Removed opinionated sizing - better CSS flow and overridability
- Added \`accent-color\` support for form controls
- Improved transitions and hover effects
- Better disabled states across all components

#### CSS Variables

Components now respect theme colors:

\`\`\`css
--dars-primary: #007bff;
--dars-spacing-md: 12px;
/* ... and more */
\`\`\`

#### Better Customization

\`\`\`python
# Inline styles work better now
Button("Click", style={"width": "200px", "padding": "16px"})

# Global styles via app.add_global_styles()
app.add_global_styles("""
    .dars-button {
        border-radius: 8px;
    }
""")
\`\`\`

---

### Bug Fixes

#### Fixed Markdown Syntax Highlighting in Multipage Apps

- **Issue**: Prism.js scripts were only injected on first page with Markdown
- **Fix**: Per-page script injection tracking ensures all pages get highlighting(Markdown Component)
- **Impact**: Multipage apps now correctly highlight code on all routes

\`\`\`python
# Now works correctly across all pages
@route("/docs")
def docs():
    return Page(Markdown(content=code_example))

@route("/tutorial")
def tutorial():
    return Page(Markdown(content=tutorial_code))  # Also highlighted now!
\`\`\`

---

## Breaking Changes

None! This release is 100% backwards compatible.

---

## Complete Example

**User Profile with Reactive Updates:**

\`\`\`python
from dars.all import *

app = App("Reactive Profile")

# State for user data
userState = State("user", 
    name="John Doe",
    email="john@example.com"
)

# Reactive display component
@FunctionComponent
def ProfileDisplay(**props):
    return f'''
    <div {Props.id} {Props.class_name} {Props.style}>
        <h2>{useDynamic("user.name")}</h2>
        <p>Email: {useDynamic("user.email")}</p>
    </div>
    '''

# Edit form
def ProfileEditor():
    return Container(
        Input(id="nameInput", value="John Doe"),
        Input(id="emailInput", value="john@example.com"),
        Button("Save", on_click=[
            userState.name.set(getInputValue("nameInput")),
            userState.email.set(getInputValue("emailInput"))
        ])
    )

# Page
@route("/")
def index():
    return Page(
        ProfileDisplay(id="profile"),
        ProfileEditor()
    )

app.add_page("index", index())

if __name__ == "__main__":
    app.rTimeCompile()
\`\`\`

**Result**: Edit the inputs and click Save - the profile display updates instantly!

---

## Migration Guide

No migration needed! Add \`useDynamic()\` to new or existing FunctionComponents:

**Before (static):**
\`\`\`python
@FunctionComponent
def UserCard(name, email, **props):
    return f'<div {Props.id}><h3>{name}</h3><p>{email}</p></div>'
\`\`\`

**After (reactive):**
\`\`\`python
@FunctionComponent
def UserCard(**props):
    return f'''
    <div {Props.id}>
        <h3>{useDynamic("user.name")}</h3>
        <p>{useDynamic("user.email")}</p>
    </div>
    '''
\`\`\`

---

## Documentation

New documentation added:

- **Hooks System** - Complete guide to \`useDynamic()\` and future hooks
- **\`getInputValue()\`** - Usage guide in Scripts documentation
- **Updated Examples** - Reactive patterns and best practices

Visit the [Dars Documentation](https://ztamdev.github.io/Dars-Framework/docs.html) for more details.

---

## What's Next

The hooks system opens the door for more reactive features...


# Release Notes v1.5.3

> **Hooks System & Reactive Bindings**

## Installation

\`\`\`bash
pip install --upgrade dars-framework
\`\`\`

## What's New

### Hooks System - \`useDynamic()\`

Dars Framework introduces its **first hook** - \`useDynamic()\` - enabling reactive state bindings in FunctionComponents!

#### Reactive State Bindings

Create components that automatically update when state changes:

\`\`\`python
from dars.all import *

# Create state
userState = State("user", name="John Doe", email="john@example.com")

# Use useDynamic in FunctionComponent
@FunctionComponent
def UserCard(**props):
    return f'''
    <div {Props.id} {Props.class_name} {Props.style}>
        <h3>{useDynamic("user.name")}</h3>
        <p>{useDynamic("user.email")}</p>
    </div>
    '''

# Render
card = UserCard(id="userCard")

# Update - DOM automatically reacts!
app.add_script(userState.name.set("Jane Doe"))  # UI updates instantly
\`\`\`

#### How It Works

1. **Initial Render**: \`useDynamic()\` inserts reactive spans with initial prop values
2. **State Changes**: When you call \`.set()\`, the hook intercepts the change
3. **Auto Updates**: All matching reactive spans update automatically

#### Key Features

- **Zero boilerplate** - Just use \`useDynamic("state.property")  in templates
- **Automatic updates** - No manual DOM manipulation needed
- **Multiple bindings** - Multiple components can bind to the same state
- **State V2 integration** - Works seamlessly with dynamic state system

---

### \`getInputValue()\` Utility

New utility function specifically designed for State V2 integration:

\`\`\`python
state = State("product", title="", price=0)

Button("Save", on_click=[
    state.title.set(getInputValue("titleInput")),
    state.price.set(getInputValue("priceInput"))
])
\`\`\`

**Features:**
- Returns input value as JavaScript expression
- Works with \`State.set()\` and other dynamic operations
- Optional \`parent_id\` parameter for scoped searches
- Complements existing \`getValue()\` for assignments

**Difference from \`getValue()\`:**
- \`getValue(input_id, target_id)\` - Performs assignment (sets textContent)
- \`getInputValue(input_id)\` - Returns value expression (for State.set())

---

### CSS Improvements

#### Modern Default Styles

- Updated all component CSS to use CSS variables for easy theming
- Removed opinionated sizing - better CSS flow and overridability
- Added \`accent-color\` support for form controls
- Improved transitions and hover effects
- Better disabled states across all components

#### CSS Variables

Components now respect theme colors:

\`\`\`css
--dars-primary: #007bff;
--dars-spacing-md: 12px;
/* ... and more */
\`\`\`

#### Better Customization

\`\`\`python
# Inline styles work better now
Button("Click", style={"width": "200px", "padding": "16px"})

# Global styles via app.add_global_styles()
app.add_global_styles("""
    .dars-button {
        border-radius: 8px;
    }
""")
\`\`\`

---

### Bug Fixes

#### Fixed Markdown Syntax Highlighting in Multipage Apps

- **Issue**: Prism.js scripts were only injected on first page with Markdown
- **Fix**: Per-page script injection tracking ensures all pages get highlighting(Markdown Component)
- **Impact**: Multipage apps now correctly highlight code on all routes

\`\`\`python
# Now works correctly across all pages
@route("/docs")
def docs():
    return Page(Markdown(content=code_example))

@route("/tutorial")
def tutorial():
    return Page(Markdown(content=tutorial_code))  # Also highlighted now!
\`\`\`

---

## Breaking Changes

None! This release is 100% backwards compatible.

---

## Complete Example

**User Profile with Reactive Updates:**

\`\`\`python
from dars.all import *

app = App("Reactive Profile")

# State for user data
userState = State("user", 
    name="John Doe",
    email="john@example.com"
)

# Reactive display component
@FunctionComponent
def ProfileDisplay(**props):
    return f'''
    <div {Props.id} {Props.class_name} {Props.style}>
        <h2>{useDynamic("user.name")}</h2>
        <p>Email: {useDynamic("user.email")}</p>
    </div>
    '''

# Edit form
def ProfileEditor():
    return Container(
        Input(id="nameInput", value="John Doe"),
        Input(id="emailInput", value="john@example.com"),
        Button("Save", on_click=[
            userState.name.set(getInputValue("nameInput")),
            userState.email.set(getInputValue("emailInput"))
        ])
    )

# Page
@route("/")
def index():
    return Page(
        ProfileDisplay(id="profile"),
        ProfileEditor()
    )

app.add_page("index", index())

if __name__ == "__main__":
    app.rTimeCompile()
\`\`\`

**Result**: Edit the inputs and click Save - the profile display updates instantly!

---

## Migration Guide

No migration needed! Add \`useDynamic()\` to new or existing FunctionComponents:

**Before (static):**
\`\`\`python
@FunctionComponent
def UserCard(name, email, **props):
    return f'<div {Props.id}><h3>{name}</h3><p>{email}</p></div>'
\`\`\`

**After (reactive):**
\`\`\`python
@FunctionComponent
def UserCard(**props):
    return f'''
    <div {Props.id}>
        <h3>{useDynamic("user.name")}</h3>
        <p>{useDynamic("user.email")}</p>
    </div>
    '''
\`\`\`

---

## Documentation

New documentation added:

- **Hooks System** - Complete guide to \`useDynamic()\` and future hooks
- **\`getInputValue()\`** - Usage guide in Scripts documentation
- **Updated Examples** - Reactive patterns and best practices

Visit the [Dars Documentation](https://ztamdev.github.io/Dars-Framework/docs.html) for more details.

---

## What's Next

The hooks system opens the door for more reactive features...

# Release Notes v1.5.2

> **Function Components**

## Installation

\`\`\`bash
pip install --upgrade dars-framework
\`\`\`

## What's New

### Function Components System

Dars Framework now features **Function Components** as the primary and recommended way to create custom UI components. This new system provides a clean, Pythonic approach to component creation without the complexity of class inheritance.

#### What are Function Components?

Function Components allow you to create reusable UI elements using simple Python functions with f-string templates. The framework automatically handles IDs, styling, events, and other properties.

**Key Benefits:**
- **Simple & Pythonic**: Just write a function that returns an HTML string
- **No Boilerplate**: No need to inherit from Component class or implement render methods
- **Automatic Property Injection**: Framework handles \`id\`, \`class_name\`, \`style\`, and \`children\` automatically
- **Linter-Friendly**: Two patterns available to avoid linter warnings
- **State Compatible**: Works seamlessly with State V2 for reactive UIs

#### Basic Usage

\`\`\`python
from dars.all import FunctionComponent, Props

@FunctionComponent
def UserCard(name, email, **props):
    return f"""
    <div {Props.id} {Props.class_name} {Props.style}>
        <h3>{name}</h3>
        <p>{email}</p>
        <div class="card-body">
            {Props.children}
        </div>
    </div>
    """

# Usage
card = UserCard("John Doe", "john@example.com", id="user-1", style={"padding": "20px"})
\`\`\`

#### Two Supported Patterns

**Option 1: Using Props Helper (Recommended)**
\`\`\`python
@FunctionComponent
def MyComponent(**props):
    return f"""
    <div {Props.id} {Props.class_name} {Props.style}>
        {Props.children}
    </div>
    """
\`\`\`

**Option 2: Explicit Arguments**
\`\`\`python
@FunctionComponent
def MyComponent(id, class_name, style, children, **props):
    return f"""
    <div {id} {class_name} {style}>
        {children}
    </div>
    """
\`\`\`

Both patterns are fully supported and avoid linter warnings about undefined variables.

#### Props Helper Class

The new \`Props\` class provides static constants for framework properties:

\`\`\`python
Props.id          # "{id}"
Props.class_name  # "{class_name}"
Props.style       # "{style}"
Props.children    # "{children}"
\`\`\`

These resolve to the correct placeholders that the framework replaces during rendering.

#### State V2 Integration Clarification

**Important Concept:** State V2 updates DOM properties, not arbitrary component arguments.

**Correct Usage:**
\`\`\`python
@FunctionComponent
def Counter(**props):
    return f"""
    <div {Props.id}>
        Current count: {Props.children}
    </div>
    """

counter = Counter(id="my-counter", children="0")
state = State(counter, text="Current count: 0")

# Updates textContent of the div
Button("Increment", on_click=state.text.set("Current count: 5"))
\`\`\`

**Why:** Dars exports to static HTML/JS. The JavaScript runtime can only manipulate DOM properties (\`textContent\`, \`style\`, \`innerHTML\`), not re-execute Python functions with new arguments.

# Release Notes v1.5.1

> **Backend HTTP Utilities & Pythonic API Communication**

## Installation

\`\`\`bash
pip install --upgrade dars-framework
\`\`\`

## What's New

### Backend HTTP Utilities System

Dars now includes a comprehensive **Pythonic system** for HTTP requests and API communication without writing any JavaScript. The new \`dars.backend\` module enables you to fetch data, bind it to components, and create reactive UIs entirely in Python.

**Key Features:**
- HTTP functions (get, post, put, delete, patch, fetch)
- \`useData()\` with dot notation for nested data access
- Seamless StateV2 integration
- \`.then()\` chaining for sequential operations
- Component management (createComp, updateComp, deleteComp)
- JSON utilities (stringify, parse, get_value)
- **State() string ID support** - Create states for dynamic components

### HTTP Functions

\`\`\`python
from dars.all import *
from dars.backend import get, post, useData

# GET request with data binding
fetch_btn = Button(
    "Fetch User",
    on_click=get(
        id="userData",
        url="https://api.example.com/users/1",
        callback=name_state.text.set(useData('userData').name)
    )
)

# POST request
submit_btn = Button(
    "Submit",
    on_click=post(
        id="result",
        url="https://api.example.com/submit",
        body={"name": "John", "email": "john@example.com"},
        callback=status_state.text.set("\u2705 Submitted!")
    )
)
\`\`\`

### useData() with Dot Notation

Access fetched data using Pythonic dot notation:

\`\`\`python
# Access nested properties
useData('userData').name           # \u2192 window.userData?.name
useData('user').address.city       # \u2192 window.user?.address?.city
useData('posts').items[0].title    # \u2192 window.posts?.items?.[0]?.title
\`\`\`

### Chaining with .then()

Chain multiple state updates sequentially:

\`\`\`python
callback=(
    status_state.text.set("Loading...")
    .then(name_state.text.set(useData('userData').name))
    .then(email_state.text.set(useData('userData').email))
    .then(status_state.text.set("\u2705 Loaded!"))
)
\`\`\`

### Component Management

Create, update, and delete components dynamically at runtime:

\`\`\`python
from dars.backend import createComp, updateComp, deleteComp

# Create new component
create_btn.on_click = createComp(
    target=Text("Hello!", id="new-item"),
    root="container-id",
    position="append"
)

# Update component
update_btn.on_click = updateComp(
    "my-component-id",
    text="Updated!",
    style={"color": "red"}
)

# Delete component
delete_btn.on_click = deleteComp("component-id")
\`\`\`

### JSON Utilities

Helper functions for working with JSON data:

\`\`\`python
from dars.backend import stringify, parse, get_value

# Stringify with pretty printing
display_state.text.set(stringify(useData('userData'), pretty=True))

# Parse JSON string
data = parse('{"name": "John"}')

# Safe nested access
city = get_value(useData('userData'), 'address.city', default='Unknown')
\`\`\`

### State() String ID Support

\`State()\` now accepts both component objects and string IDs, enabling state management for dynamically created components:

\`\`\`python
from dars.all import *
from dars.backend import createComp

# Traditional: State with component object
existing_text = Text("0", id="counter")
existing_state = State(existing_text, text=0)

# New: State with string ID (for components created later)
dynamic_state = State("dynamic-counter", text=0)

# Create the component later
create_btn.on_click = createComp(
    target=Text("0", id="dynamic-counter"),
    root="container-id"
)

# State works even though component was created after state!
increment_btn.on_click = dynamic_state.text.increment(by=1)
\`\`\`

**Use Cases:**
- Components created with \`createComp()\`
- Dynamically generated UIs
- Conditional component rendering
- Server-side rendered components

## Technical Implementation

### DataAccessor Class

New \`DataAccessor\` class with:
- \`__getattr__\` for dot notation support
- \`.code\` property for RawJS generation
- \`.bind()\` method for StateV2 integration
- \`.get()\` method for safe property access

### StateV2 Enhancements

Updated \`StateV2._generate_change_call()\` to handle \`DataAccessor\` objects:
- Automatically detects \`DataAccessor\` instances
- Extracts \`.code\` property for JavaScript generation
- Seamless integration with existing state management

## Documentation

### New Documentation

**\`backend_api.md\`** - Comprehensive guide (500+ lines) covering:
- Quick Start examples
- HTTP Functions reference
- Data Binding with useData()
- JSON Utilities
- Component Management
- 3 Advanced Examples
- Best Practices
- Complete API Reference

**Documentation URL:** https://ztamdev.github.io/Dars-Framework/docs.html#backend-http-utilities

## Breaking Changes

**None** - This is a fully backward-compatible release. All existing code continues to work.

## Bug Fixes

- **Fixed**: \`StateV2\` now correctly handles \`DataAccessor\` objects in \`to_js_value()\`
- **Fixed**: \`RawJS\` objects are properly serialized in state updates
- **Fixed**: \`dScript.then()\` chaining works correctly with backend operations

## Performance & Compatibility

- **Zero Overhead**: Backend utilities only activate when imported
- **Backward Compatible**: All existing code works without changes
- **Bundle Size**: Minimal impact (+~10KB for backend module)
- **Desktop Support**: Full Electron compatibility maintained

## Migration Guide

No migration needed - this is an additive release. To start using the new features:

\`\`\`python
# Add to your imports
from dars.backend import get, post, useData

# Start using Pythonic HTTP
button.on_click = get(
    id="data",
    url="https://api.example.com/data",
    callback=state.text.set(useData('data').message)
)
\`\`\`

---

**This release makes Dars fully self-contained for building reactive, API-driven UIs without writing any JavaScript!**

---

# Release Notes v1.5.0

> **Animation System Stability & Runtime Improvements**

## Installation

\`\`\`bash
pip install --upgrade dars-framework
\`\`\`

## What's New

### Animation System Stability

Significant improvements to the animation system's reliability and ease of use:

- **Fixed Infinite Pulse**: \`pulse(iterations="infinite")\` now works correctly (fixed \`TypeError\`).
- **Chaining Support**: State updates like \`increment()\` can now be chained with animations using \`.then()\` or \`sequence()\`.
- **Documentation**: Added comprehensive [Animation Guide](https://ztamdev.github.io/Dars-Framework/docs.html#dars-animation-system) to the documentation.

### Dynamic Event Updates

The client-side runtime has been upgraded to fully support dynamic event handler updates:

\`\`\`python
# This now works perfectly in real-time
button.on_click = state.update(
    text="Clicked!",
    on_click=alert("New handler attached!")
)
\`\`\`

## Bug Fixes

- **Fixed**: \`pulse\` animation now correctly handles \`iterations="infinite"\` (mapped to \`Infinity\`).
- **Fixed**: \`SyntaxError\` when chaining state updates (wrapped in async IIFE).

---

# Release Notes v1.4.9

> **Event Handler Support & Dual State System Documentation**

## Installation

\`\`\`bash
pip install --upgrade dars-framework
\`\`\`

## What's New

### State V2: Event Handler Support

State V2 now supports updating event handlers:

\`\`\`python
from dars.all import *

# Update events in State V2
state.update(
    text="Click me",
    on_click=alert("Success!"),
    on_mouseover=dScript("showTooltip()")
)

# Works with dScript objects
button_state.update(on_click=dScript("console.log('clicked')"))
\`\`\`

**Implementation:**
- Automatic detection of \`on_*\` properties
- Extracts \`.code\` from dScript objects  
- Handles arrays of event handlers
- Gracefully skips non-serializable values

### Dual State System Documentation

Documentation now presents **two coexisting state management systems**:

**State V2 (Dynamic)**
- Auto-increment/decrement built-in
- Best for: counters, timers, simple updates

**dState/cState (Indexed)**
- Full state machine support
- Immutable state 0
- Cross-state calls with \`Mod.call()\`
- Best for: workflows, complex UI transitions

Comprehensive comparison table and use case guidance added to state management documentation.

## Bug Fixes

- **Fixed**: State V2 can now handle dScript event handlers without errors
- **Fixed**: \`_generate_change_call()\` properly handles non-JSON-serializable values

## Documentation

- Complete restructure of \`state_management.md\` to include both systems
- Added comparison table for State V2 vs dState/cState
- Restored all original dState/cState documentation
- Added use case recommendations for choosing the right system

---

# Release Notes v1.4.8


> **Critical Fix**: State V2 now properly supports all component properties including \`class_name\`, \`style\`, \`attrs\`, and more.

## Installation

\`\`\`bash
pip install --upgrade dars-framework
\`\`\`

or

\`\`\`bash
pip install dars-framework==1.4.8
\`\`\`

## What's Fixed

### State V2 Complete Property Support

**Previously (v1.4.7):** State V2 only updated \`text\` content, incorrectly setting textContent for all properties.

\`\`\`python
# This didn't work correctly in v1.4.7
counter.class_name.set("active")
\`\`\`

**Now (v1.4.8):** State V2 properly handles **all component properties** using the \`change()\` client function.

\`\`\`python
# All properties now work correctly!
state.text.set("New text")
state.class_name.set("active")
state.style.set({"color": "red"})
state.attrs.set({"title": "Tooltip"})
state.html.set("<strong>Bold</strong>") 
\`\`\`

### Unified Property Handling

All State V2 methods now use the same \`change()\` function as \`this()\` and \`dState\`, ensuring consistent behavior across the framework:

- \`ReactiveProperty.set()\` - Works with any property type
- \`State.update()\` - Updates multiple properties correctly
- \`State.reset()\` - Resets all property types to defaults

### Validation Improvements

**Increment/Decrement Validation:**
Now properly validates that \`increment()\` and \`decrement()\` are only used on numeric properties:

\`\`\`python
# Correct usage
counter.text.increment(by=1)

# Now throws helpful error
counter.class_name.increment(by=1)
\`\`\`

## Bug Fixes

### Fixed: Property Type Handling

- **Fixed**: \`class_name.set()\` now correctly updates element's \`className\`
- **Fixed**: \`style.set()\` now correctly updates inline styles
- **Fixed**: \`attrs.set()\` now correctly updates HTML attributes
- **Fixed**: \`html.set()\` now correctly updates \`innerHTML\`
- **Fixed**: \`update()\` now correctly handles multiple properties simultaneously
- **Fixed**: \`reset()\` now correctly restores all property types

### Technical Details

**Root Cause:** 
State V2 methods were directly manipulating \`el.textContent\` instead of using the framework's \`change()\` function, which properly routes updates based on property type.

**Solution:**
Created \`_generate_change_call()\` helper that generates proper \`change()\` payloads:
- \`text\` \u2192 \`{text: value}\`
- \`html\` \u2192 \`{html: value}\`
- \`style\` \u2192 \`{style: object}\`
- \`class_name\` \u2192 \`{attrs: {class: value}}\` or \`{classes: object}\`
- \`attrs\` \u2192 \`{attrs: object}\`

All reactive methods now use this helper for consistent, correct property updates.

## Complete Property Examples

### Setting Different Property Types

\`\`\`python
from dars.all import *

display = Container(Text("Example"), id="demo")

# Create state with multiple properties
state = State(display, 
    text="Hello",
    class_name="",
    style={"background": "#333"}
)

# Update text
text_btn.on_click = state.text.set("Updated!")

# Update CSS class
class_btn.on_click = state.class_name.set("active highlight")

# Update styles
style_btn.on_click = state.style.set({
    "background": "linear-gradient(135deg, #667eea, #764ba2)",
    "color": "white",
    "padding": "20px"
})

# Update HTML attributes
attr_btn.on_click = state.attrs.set({
    "data-status": "complete",
    "title": "Completed task"
})
\`\`\`

### Advanced Class Manipulation

\`\`\`python
# Add/remove specific classes
state.classes.set({
    "add": ["active", "highlight"],
    "remove": ["disabled", "hidden"]
})

# Toggle classes
state.classes.set({
    "toggle": ["expanded"]
})
\`\`\`

### Update Multiple Properties

\`\`\`python
# Update several properties at once
success_btn.on_click = state.update(
    text="Success!",
    class_name="success",
    style={"color": "green", "fontSize": "18px"},
    attrs={"data-result": "ok"}
)
\`\`\`

## Migration from v1.4.7

**No breaking changes** - all existing code continues to work. However, if you tried using non-\`text\` properties in v1.4.7 and they didn't work, they will now work correctly in v1.4.8.

**If you worked around the limitation:**
\`\`\`python
# Old workaround (v1.4.7)
from dars.core.state import this
button.on_click = this().state(class_name="active")  # Had to use this()

# Now works directly with State V2 (v1.4.8)
button.on_click = state.class_name.set("active")  # \u2705 Works!
\`\`\`

## Dependency Cleanup

- **Removed**: \`rjsmin\` dependency (Apache license, replaced with regex fallback)
- **Removed**: \`fastapi\` dependency (not used in framework)

JS/CSS minification now uses:
1. Vite (if available)
2. esbuild (if available)
3. Regex fallback (always available, no external dependencies)

## Performance & Compatibility

- **Zero overhead**: Property handling uses existing \`change()\` infrastructure
- **Backward compatible**: All v1.4.7 code works in v1.4.8
- **Consistent behavior**: State V2, \`this()\`, and dState now all use same property system
- **Desktop support**: Full Electron compatibility maintained

---

**Upgrade highly recommended** for all projects using State V2, especially if you need to update component properties beyond just \`text\`.

---

# Release Notes v1.4.7


> Introducing State V2 and comprehensive animation system. This is the biggest update to Dars state management, bringing a pure Pythonic API and 15+ built-in animations.

## Installation

\`\`\`bash
pip install --upgrade dars-framework
\`\`\`

or

\`\`\`bash
pip install dars-framework==1.4.7
\`\`\`

## What's New

### State V2 - Pure Pythonic State Management

**New \`State\` Class:**
- Pure Python API - no more verbose dState syntax
- Direct property access with reactive operations
- Built-in auto-increment/auto-decrement operations
- Clean reset functionality
- Seamless animation integration

**Before (dState - deprecated):**
\`\`\`python
from dars.core.state import dState, Mod

display = Text("0", id="counter")
st = dState("counter", component=display, states=[0, 1, 2])
st.cState(1, mods=[Mod.inc(display, prop='text', by=1)])
button.on_click = st.state(1)
\`\`\`

**After (State V2 - recommended):**
\`\`\`python
from dars.all import State

display = Text("0", id="counter")
counter = State(display, text=0)
button.on_click = counter.text.increment(by=1)
\`\`\`

**Key Features:**
- **Reactive Properties**: Direct access with \`state.property.operation()\`
- **Auto Operations**: Continuous operations with \`auto_increment()\`, \`auto_decrement()\`
- **Reset**: Simple \`state.reset()\` to restore initial values
- **Intuitive**: Pythonic API that feels natural

**Usage:**
\`\`\`python
from dars.all import *

# Create component and state
timer_display = Text("0", id="timer", style={"font-size": "36px"})
timer = State(timer_display, text=0)

# Auto-incrementing timer
start_btn.on_click = timer.text.auto_increment(by=1, interval=1000)
stop_btn.on_click = timer.text.stop_auto()
reset_btn.on_click = timer.reset()
\`\`\`

### Comprehensive Animation System

**15+ Built-in Animations:**
- \`fadeIn\` / \`fadeOut\` - Opacity transitions
- \`slideIn\` / \`slideOut\` - Position-based slides (8 directions)
- \`scaleIn\` / \`scaleOut\` - Size transformations
- \`shake\` - Shake effect for alerts
- \`bounce\` - Bounce effect
- \`pulse\` - Heartbeat/pulse effect
- \`rotate\` - Rotation animations
- \`flip\` - Flip on X/Y axis
- \`colorChange\` - Color transitions
- \`morphSize\` - Size morphing
- \`sequence\` - Chain multiple animations

**Animation Chaining:**
\`\`\`python
from dars.all import *

button.on_click = sequence(
    fadeIn(id="box", duration=400),
    pulse(id="box", scale=1.2, iterations=2),
    shake(id="box", intensity=5)
)
\`\`\`

**Integration with State V2:**
\`\`\`python
button.on_click = sequence(
    counter.text.increment(by=1),
    pulse(id="counter", scale=1.2),
    fadeOut(id="counter", duration=200),
    counter.text.set(value=0),
    fadeIn(id="counter", duration=200)
)
\`\`\`

**All Animations:**
- Return \`dScript\` objects for chaining
- Customizable duration, easing, and parameters
- Proper async completion handling
- Work seamlessly with event handlers

### Professional State V2 Template

**New Example Template:**
- Located in \`dars/templates/examples/advanced/StateV2/\`
- Professional, production-ready demonstration
- Function component pattern (LandingPage style)
- Comprehensive showcases:
  - Interactive counter with increment/decrement
  - Auto-incrementing timer
  - Animation showcase with 15+ animations
  - State management best practices
- Responsive design with modern styling
- Complete documentation and code examples

**Template Structure:**
\`\`\`
dars/templates/examples/advanced/StateV2/
\u251C\u2500\u2500 index.py                 # Main application
\u251C\u2500\u2500 hero_component.py        # Hero section
\u251C\u2500\u2500 counter_component.py     # Counter demo
\u251C\u2500\u2500 timer_component.py       # Timer demo
\u251C\u2500\u2500 animation_component.py   # Animation showcase
\u251C\u2500\u2500 styles.css              # Global styles
\u2514\u2500\u2500 README.md               # Documentation
\`\`\`

## Breaking Changes

**dState/cState Deprecation:**
- \`dState\` and \`cState\` are now deprecated
- All functionality replaced by State V2
- Legacy code still works for backward compatibility
- Migration path provided in updated documentation
- New projects should use State V2 exclusively

## Documentation Updates

**Updated Files:**
- \`state_management.md\` - Completely rewritten for State V2
- \`scripts.md\` - Added comprehensive animation system documentation
- All dState/cState references removed from active docs
- Migration guides included for existing projects

## Bug Fixes

**Animation System:**
- Fixed animation chaining with proper Promise handling
- Fixed initial state rendering with \`transition='none'\` pattern
- Fixed \`sequence()\` function trailing semicolon issue
- All animations now properly await completion
- Animations use \`setTimeout(20ms)\` for reliable state application

**State Operations:**
- \`auto_increment\` and \`auto_decrement\` now return proper \`dScript\` objects
- Client-side loop management with \`startLoop\` and \`stopLoop\`
- Proper cleanup of active loops

## Technical Improvements

### Animation Implementation

- All animations wrapped in async IIFEs
- Proper transition timing with \`setTimeout\`
- Force reflow with \`void el.offsetWidth\`
- Set \`transition='none'\` before initial styles
- \`animation.finished\` for Web Animations API
- Proper Promise chaining in \`sequence()\`

## Migration Guide

### From dState to State V2

**1. Import Changes:**
\`\`\`python
# Old
from dars.core.state import dState, Mod

# New
from dars.all import State
\`\`\`

**2. State Creation:**
\`\`\`python
# Old
counter_state = dState("counter", component=display, states=[0, 1, 2])
counter_state.cState(1, mods=[Mod.inc(display, prop='text', by=1)])

# New
counter = State(display, text=0)
\`\`\`

**3. Event Handlers:**
\`\`\`python
#Old
button.on_click = counter_state.state(1)

# New
button.on_click = counter.text.increment(by=1)
\`\`\`

**4.Auto Operations (New Feature):**
\`\`\`python
# Only available in State V2
start_btn.on_click = timer.text.auto_increment(by=1, interval=1000)
stop_btn.on_click = timer.text.stop_auto()
\`\`\`

### Adding Animations

\`\`\`python
from dars.all import fadeIn, pulse, sequence

# Simple animation
button.on_click = fadeIn(id="element", duration=500)

# Chained animations
button.on_click = sequence(
    fadeIn(id="box"),
    pulse(id="box", scale=1.1)
)
\`\`\`

## Performance & Compatibility

- **Zero Overhead**: State V2 only activates when used
- **Backward Compatible**: dState still works for existing code
- **Bundle Size**: Minimal impact (+~15KB for animations)
- **Desktop Support**: Full Electron compatibility

## Examples

### Complete Counter App

\`\`\`python
from dars.all import *

app = App("Counter Demo")

# Create display with state
counter_display = Text("0", id="counter", style={
    "font-size": "48px", 
    "color": "#2563eb"
})
counter = State(counter_display, text=0)

# Buttons with operations
inc_btn = Button("+1", on_click=counter.text.increment(by=1))
dec_btn = Button("-1", on_click=counter.text.decrement(by=1))
reset_btn = Button("Reset", on_click=counter.reset())
pulse_btn = Button("Pulse", on_click=pulse(id="counter", scale=1.2))

page = Page(Container(counter_display, inc_btn, dec_btn, reset_btn, pulse_btn))
app.add_page("index", page, index=True)
app.rTimeCompile()
\`\`\`

### Auto-Incrementing Timer

\`\`\`python
from dars.all import *

app = App("Timer Demo")

timer_display = Text("0", id="timer")
timer = State(timer_display, text=0)

start_btn = Button("Start", on_click=timer.text.auto_increment(by=1, interval=1000))
stop_btn = Button("Stop", on_click=timer.text.stop_auto())
reset_btn = Button("Reset", on_click=timer.reset())

page = Page(Container(timer_display, start_btn, stop_btn, reset_btn))
app.add_page("index", page, index=True)
app.rTimeCompile()
\`\`\`

## Desktop Exporter Status

**Still in BETA** - State V2 and animations fully supported in both web and desktop exports.

---

**This is a landmark release** - State V2 represents the future of Dars state management. Upgrade highly recommended for all projects.

---

# Release Notes v1.4.6


> **Major Feature Release**: Introduces Single Page Application (SPA) support and a powerful client-side routing system.

## Installation

\`\`\`bash
pip install --upgrade dars-framework
\`\`\`

or

\`\`\`bash
pip install dars-framework==1.4.5
\`\`\`

## What's New

### Single Page Application (SPA) Support

**New Routing System:**
- **Client-Side Routing**: Build fast, responsive SPAs with Python.
- **Nested Routes & Layouts**: Create complex UI hierarchies using the \`parent\` parameter and the new \`Outlet\` component.
- **Persistent Layouts**: Keep headers, sidebars, and navigation bars active while content changes dynamically.

**Robust Error Handling:**
- **Automatic 404 Handling**: Dars now automatically redirects invalid routes to a 404 page.
- **Default & Custom 404**: Includes a built-in clean 404 page, or define your own with \`app.set_404_page()\`.

### Developer Experience

**Hot Reload Stability:**
- **Intelligent Polling**: New hot reload system for SPAs that detects changes without spamming logs.
- **Auto-Stop**: Prevents browser lag by stopping polling after 10 consecutive connection failures.

### Fixes & Improvements

- **SPA Export**: Fixed issues where SPA child routes were conflicting with multipage exports.
- **Preview Server**: Improved handling of SPA routes and query parameters.
- **Assets**: Enforced absolute paths for SPA assets to ensure correct loading from any depth.

---


# Release Notes v1.4.4

> Critical bug fix release. Removes non-functional features, fixes style merge, and improves state restoration.

## Installation

\`\`\`bash
pip install --upgrade dars-framework
\`\`\`

or

\`\`\`bash
pip install dars-framework==1.4.4
\`\`\`

## What's Fixed

- **Style Merge Fix (CRITICAL)** - \`Mod.set()\` now correctly merges style properties
- **Removed \`this().goto()\`** - Non-functional feature removed; use \`state.state()\` instead
- **Fixed Syntax Warning** - Corrected invalid escape sequence in \`js_lib.py\`
- **Improved State 0 Restoration** - Event handlers now re-attach when returning to default state

---

# Release Notes v1.4.3 (DEPRECATED)

> State management enhancements with compile-time validation, component self-navigation, and critical style merge fix. Improves developer experience and fixes property replacement bug.

## Installation

\`\`\`bash
pip install --upgrade dars-framework
\`\`\`

or

\`\`\`bash
pip install dars-framework==1.4.3
\`\`\`

## What's New

- **\`this().goto(idx)\`** - Component self-navigation for state transitions
- **\`this_for(id)\`** - Compile-time validation helper for state navigation
- **Style Merge Fix** - Critical fix: \`Mod.set()\` now merges style properties instead of replacing them
- **Enhanced Documentation** - Guides for state management patterns

---

# Release Notes v1.4.2

> New utility dScript functions added to \`utils_ds\` for enhanced client-side interactions.

## Installation

\`\`\`bash
pip install --upgrade dars-framework
\`\`\`

or

\`\`\`bash
pip install dars-framework==1.4.2
\`\`\`

## What's New

### Utility Functions (\`utils_ds\`)

- \`setTimeout(delay: int, code: dScript)\`: Execute a dScript after a delay (ms).
- \`setText(id: str, text: str)\`: Set the text content of an element.
- \`showModal(id: str)\`, \`hideModal(id: str)\`: Modal visibility helpers.
- \`goTo(href: str)\`, \`goToNew(href: str)\`, \`reload()\`, \`goBack()\`, \`goForward()\`: Navigation utilities.
- \`alert(message: str)\`, \`confirm(message: str, on_ok: str = "", on_cancel: str = "")\`, \`log(message: str)\`: Alert & console utilities.
- \`show(id: str)\`, \`hide(id: str)\`, \`toggle(id: str)\`, \`addClass(id: str, class_name: str)\`, \`removeClass(id: str, class_name: str)\`, \`toggleClass(id: str, class_name: str)\`: DOM manipulation utilities.
- \`scrollTo(x: int = 0, y: int = 0)\`, \`scrollToTop()\`, \`scrollToBottom()\`, \`scrollToElement(id: str)\`: Scroll utilities.
- \`submitForm(form_id: str)\`, \`resetForm(form_id: str)\`, \`getValue(input_id: str, target_id: str)\`, \`clearInput(input_id: str)\`: Form utilities.
- \`saveToLocal(key: str, value: str)\`, \`loadFromLocal(key: str, target_id: str)\`, \`removeFromLocal(key: str)\`, \`clearLocalStorage()\`: Storage utilities.
- \`copyToClipboard(text: str)\`, \`copyElementText(id: str)\`: Clipboard utilities.
- \`focus(id: str)\`, \`blur(id: str)\`: Focus utilities.

These functions are documented in \`https://ztamdev.github.io/Dars-Framework/docs.html#dars-script-system\` and for states in \`https://ztamdev.github.io/Dars-Framework/docs.html#state-management-in-dars-dstate-cstate-goto-mods\`.

---

# Release Notes v1.4.1

> SEO and Apple device optimizations. Enhanced metadata generation with automatic MIME type detection for favicons and comprehensive iOS/Safari support.

## Installation

\`\`\`bash
pip install --upgrade dars-framework
\`\`\`

or

\`\`\`bash
pip install dars-framework==1.4.1
\`\`\`

## What's New

### Automatic Favicon MIME Type Detection

**Smart Icon Type Recognition:**
- Favicon links now automatically detect and use the correct MIME type based on file extension
- Supports PNG, ICO, SVG, JPG/JPEG, WebP, and GIF formats
- No manual type specification needed
- Eliminates incorrect \`image/x-icon\` type for PNG files

**Before (v1.4.0):**
\`\`\`html
<link rel="icon" href="logo.png" type="image/x-icon">  <!-- Incorrect! -->
\`\`\`

**After (v1.4.1):**
\`\`\`html
<link rel="icon" href="logo.png" type="image/png">  <!-- Correct! -->
\`\`\`

### Enhanced Apple Device Support

**New App Properties:**
- \`apple_mobile_web_app_capable\` - Enable fullscreen mode when added to home screen
- \`apple_mobile_web_app_status_bar_style\` - Control status bar appearance:
  - \`"default"\` - Standard iOS status bar
  - \`"black"\` - Black status bar
  - \`"black-translucent"\` - **Transparent status bar** (solves Safari iOS 16+ solid color issue)
- \`apple_mobile_web_app_title\` - Custom title for home screen icon

**Usage:**
\`\`\`python
app = App(
    title="My App",
    favicon="logo.png",
    apple_touch_icon="logo.png",
    apple_mobile_web_app_capable=True,
    apple_mobile_web_app_status_bar_style="black-translucent",  # Enables transparency!
    apple_mobile_web_app_title="MyApp"
)
\`\`\`

### Safari 15+ Theme Color Enhancements

**Adaptive Theme Colors:**
- Theme color now includes media query variants for light/dark mode
- Proper integration with iOS system appearance settings
- **Fixes Safari iOS 16+ transparency issues** where solid colors blocked background visibility

**Generated Meta Tags:**
\`\`\`html
<meta name="theme-color" content="#0d1513">
<meta name="theme-color" media="(prefers-color-scheme: light)" content="#0d1513">
<meta name="theme-color" media="(prefers-color-scheme: dark)" content="#0d1513">
\`\`\`

### Improved Apple Touch Icon

**Multiple Size Specifications:**
- Apple touch icon now includes size attribute for better iOS home screen quality
- Generates both standard and 180x180 sized icon links

**Generated Links:**
\`\`\`html
<link rel="apple-touch-icon" href="logo.png">
<link rel="apple-touch-icon" sizes="180x180" href="logo.png">
\`\`\`

### Modern Mobile Web App Meta Tag

**Standards Compliance:**
- Added \`mobile-web-app-capable\` meta tag alongside \`apple-mobile-web-app-capable\`
- Eliminates deprecation warnings in modern browsers
- Maintains backward compatibility with older iOS versions

**Generated Meta Tags:**
\`\`\`html
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-capable" content="yes">
\`\`\`

## Technical Improvements

### Exporter Enhancements (\`dars/exporters/web/html_css_js.py\`)

- **New \`_detect_icon_mime_type()\` Helper**: Automatically detects MIME types from file extensions
- **Enhanced \`_generate_meta_tags()\`**: Adds Apple-specific meta tags and theme-color variants
- **Updated \`_generate_links()\`**: Applies automatic MIME detection and sizes attribute

### App Class Updates (\`dars/core/app.py\`)

- Added 3 new initialization parameters for Apple mobile web app support
- Properties auto-initialize with sensible defaults (\`apple_mobile_web_app_title\` defaults to app title)
- All new properties are **optional** and **backward compatible**

## Migration Notes

### For Existing Projects

**Automatic Upgrade:**
- No configuration changes required
- Favicons automatically get correct MIME types
- Theme colors automatically include light/dark variants
- All new features are opt-in

**Optional iOS Enhancement:**
\`\`\`python
# Add to your App initialization
app = App(
    # ... existing params ...
    apple_mobile_web_app_capable=True,
    apple_mobile_web_app_status_bar_style="black-translucent",
    apple_mobile_web_app_title="MyApp"
)
\`\`\`

## SEO & Performance Impact

- **Improved SEO**: Correct MIME types and proper meta tags
- **Better Mobile Indexing**: Enhanced metadata for mobile search results
- **iOS User Retention**: Superior home screen experience encourages app-like usage

## Desktop Exporter Status

**Still in BETA** - No changes from v1.4.0

---

**Upgrade Highly Recommended** for all projects, especially those targeting iOS/Safari users or requiring proper favicon MIME types.

# Release Notes v1.4.0

> Simple Template update.

## Installation

\`\`\`bash
pip install --upgrade dars-framework
\`\`\`

or

\`\`\`bash
pip install dars-framework==1.4.0
\`\`\`

## Notes:

All advanced and basic templates are now updated using the new features.

# Release Notes v1.3.9

> Desktop File System API, Pythonic Arg helper, keyboard event filtering, and comprehensive template synchronization. Major enhancements to desktop capabilities with improved developer experience.

## Installation

\`\`\`bash
pip install --upgrade dars-framework
\`\`\`

or

\`\`\`bash
pip install dars-framework==1.3.9
\`\`\`

## What's New

### Desktop File System API - \`list_directory\`

**Comprehensive Directory Listing:**
- New \`list_directory()\` function for browsing files and folders
- Optional glob pattern filtering (e.g., \`"*.py"\` for Python files only)
- Optional \`include_size\` parameter (default: False) to show/hide file sizes
- Full integration with \`get_value()\` for dynamic paths from inputs
- Seamless chaining with \`dScript.then()\` for UI updates
- Returns array of \`{name, isDirectory, size?}\` objects

**Usage:**
\`\`\`python
from dars.desktop import list_directory, get_value
from dars.core.state import this

# Simple directory listing
Button("List", 
    on_click=list_directory(get_value("path")).then(
        this().state(id="output", html=RawJS("value.map(f => f.name).join('<br>')"))
    )
)

# Filter by pattern
Button("Python Files",
    on_click=list_directory(".", "*.py").then(
        this().state(id="count", text=RawJS("\`Found \${value.length} files\`"))
    )
)

# Include file sizes
list_directory(".", "*", include_size=True)
\`\`\`

### Pythonic \`Arg\` Helper

**Cleaner dScript.ARG Access:**
- New \`Arg\` singleton for Pythonic access to \`dScript.ARG\`
- More readable than \`RawJS("dScript.ARG")\`
- Provides helper methods like \`.map()\`, \`.join()\`, \`.length\`, etc.
- Auto-generates proper JavaScript code
- Exported in \`dars.all\` for easy access

**Usage:**
\`\`\`python
from dars.scripts.dscript import Arg

# Old way (still works)
this().state(text=RawJS("dScript.ARG.map(f => f.name).join('\\\\n')"))

# New Pythonic way
this().state(text=Arg.map("f => f.name").join("\\\\n"))

# Properties
Arg.length  # -> "dScript.ARG.length"
Arg.value   # -> "dScript.ARG.value"

# Methods
Arg.map("f => f.name")  # -> "dScript.ARG.map(f => f.name)"
Arg.filter("x => x > 0")  # -> "dScript.ARG.filter(x => x > 0)"
\`\`\`

### Enhanced Keyboard Event Filtering

**Specific Key Event Handlers:**
- New keyboard event constants for specific keys (e.g., \`KEY_DOWN_ENTER\`, \`KEY_DOWN_ESCAPE\`)
- Event type parsing with \`.\` delimiter for key filtering (e.g., \`"keydown.Enter"\`)
- Proper event delegation with key matching
- Works across all event attachment mechanisms
- Backward compatible with existing keyboard events

**New Event Constants:**
\`\`\`python
from dars.core.events import EventTypes

# Specific Enter key events
on_keydown_enter    # Triggered only when Enter is pressed
on_keyup_enter      # Triggered only when Enter is released

# Specific Escape key events  
on_keydown_escape   # Triggered only when Escape is pressed
on_keyup_escape     # Triggered only when Escape is released

# Usage
Input(
    id="search",
    on_keydown_enter=search_action,  # Only fires on Enter
    on_keydown_escape=clear_action   # Only fires on Escape
)
\`\`\`

### Configurable DevTools

**Electron DevTools Control:**
- New \`devtools\` parameter in \`App\` class (default: \`True\`)
- Respects \`DARS_DEV\` and \`DARS_DEVTOOLS\` environment variables
- DevTools only open when both conditions met: dev mode + devtools enabled
- Better control over development environment
- Applies to all Electron generation methods

**Usage:**
\`\`\`python
# Disable DevTools even in dev mode
app = App(
    title="My App",
    desktop=True,
    devtools=False  # Won't open DevTools
)

# Default behavior (DevTools enabled)
app = App(
    title="My App",
    desktop=True
)
\`\`\`

### Dynamic Form Element Updates

**Fixed \`change\` Function:**
- Corrected dynamic text updates for form elements
- Uses \`.value\` for \`Input\`, \`Textarea\`, \`Select\`
- Uses \`.textContent\` for other elements (Text, Button, etc.)
- Ensures UI updates properly reflect state changes
- Fixed issue where form input values weren't updating

### Improved Event Delegation

**Keyboard Event Fix:**
- Fixed event delegation for key-filtered keyboard events
- Properly checks both base event name and filtered event name in eventMap
- Ensures \`keydown.Enter\` and similar events work correctly
- Maintains backward compatibility with non-filtered events

## Bug Fixes

- Fixed \`change\` function to use \`.value\` for form elements instead of \`.textContent\`
- Fixed event delegation to properly handle key-filtered keyboard events like \`keydown.Enter\`
- Fixed ElectronExporter default templates to include latest IPC handlers
- Fixed CLI template generation to include all current File System API functions

## Improved

- Enhanced developer experience with configurable DevTools
- Cleaner syntax with \`Arg\` helper for dScript.ARG access
- More powerful keyboard event handling with key-specific filtering

## Migration Guide

### From v1.3.8 to v1.3.9

No breaking changes. You can upgrade safely:

\`\`\`bash
pip install --upgrade dars-framework
\`\`\`

**Optional: Use new features**

1. **Use \`list_directory\` for file browsing:**
\`\`\`python
from dars.desktop import list_directory, get_value

Button("Browse", 
    on_click=list_directory(get_value("dir")).then(...)
)
\`\`\`

2. **Use \`Arg\` helper for cleaner code:**
\`\`\`python
from dars.scripts.dscript import Arg

# Instead of RawJS("dScript.ARG.map(...)") 
text=Arg.map("x => x.name").join("\\\\n")
\`\`\`

3. **Use specific keyboard events:**
\`\`\`python
Input(
    on_keydown_enter=submit_action,
    on_keydown_escape=cancel_action
)
\`\`\`

## Documentation

- Updated Desktop exporter documentation with File System API examples
- Added \`Arg\` helper documentation in scripts section
- Enhanced keyboard events documentation with key-specific examples

# Release Notes v1.3.8

> Dynamic state updates, improved event handling, and enhanced Electron dev experience. Introduces \`this()\` for event-time component updates, \`RawJS\` for JavaScript injection, and \`dScript.then()\` for async chaining.

## Installation

\`\`\`bash
pip install --upgrade dars-framework
\`\`\`

or

\`\`\`bash
pip install dars-framework==1.3.8
\`\`\`

## What's New

### Dynamic State Updates with \`this()\`

**Effortless Component Updates:**
- New \`this()\` helper for direct, event-time component updates without pre-registering states
- Update any component property: \`text\`, \`html\`, \`style\`, \`attrs\`, \`classes\`
- Works in both desktop and web exports
- Perfect for async operations and file I/O

**Usage:**
\`\`\`python
from dars.core.state import this

# Button that updates itself
btn = Button("Click me", on_click=this().state(
    text="Clicked!",
    style={"color": "red"}
))

# Counter with Mod helpers
counter = Text("0", id="count")
inc_btn = Button("+1", on_click=this().state(text=Mod.inc("count")))
\`\`\`

### Raw JavaScript Injection with \`RawJS\`

**Dynamic Value Passing:**
- New \`RawJS\` class for injecting raw JavaScript variables into state updates
- Essential for passing values from async operations
- Use \`dScript.ARG\` as a placeholder for chained script results

**Usage:**
\`\`\`python
from dars.scripts.dscript import RawJS, dScript
from dars.desktop import read_text

# File content becomes button text
read_btn = Button("Load",
    on_click=read_text("data.txt").then(
        this().state(text=RawJS(dScript.ARG))
    )
)
\`\`\`

### Script Chaining with \`dScript.then()\`

**Sequential Async Operations:**
- New \`.then()\` method for chaining \`dScript\` objects
- Pass results between scripts using \`dScript.ARG\` (resolves to \`value\`)
- Built-in error handling and logging for debugging
- Enables complex workflows like read \u2192 process \u2192 update \u2192 write

**Usage:**
\`\`\`python
# Chain file operations
Button("Process",
    on_click=read_text("input.txt")
        .then(dScript(code="return value.toUpperCase()"))
        .then(write_text("output.txt", RawJS("value")))
        .then(this().state(text="Done!"))
)
\`\`\`

### Event Handler Assignment Fix

**Fixed Critical Bug:**
- Event handlers can now be assigned via attribute assignment: \`btn.on_click = handler\`
- Previously only constructor assignment worked: \`Button(on_click=handler)\`
- Added \`__setattr__\` override to properly register events in all cases
- Maintains backward compatibility with existing code

### Enhanced Electron Dev Mode

**Improved Development Experience:**
- Filtered harmless Chrome DevTools warnings (Autofill.enable, etc.)
- Fixed double Electron window bug on file save/reload
- Added debounce logic to prevent concurrent restarts
- Cleaner console output with better error formatting
- Chrome DevTools auto-open in dev mode for easier debugging

**Better Logging:**
- Error-only stderr filtering (no more noise)
- Color-coded messages for different log levels
- Stack traces properly displayed for JavaScript errors

## Technical Improvements

### State System Enhancements
- **Dynamic Updates**: New \`change({dynamic: true, ...})\` path in \`dars/js_lib.py\`
- **RawJS Support**: State methods now detect and preserve \`RawJS\` values
- **this() Proxy**: Clean API for self-referential component updates

### Script System Improvements
- **Chaining Infrastructure**: Robust async IIFE wrapping for sequential execution
- **Value Passing**: Standardized \`value\` variable for inter-script communication
- **Debug Logging**: Verbose console output for troubleshooting chains

### Component System Fixes
- **Event Collection**: \`VDomBuilder\` now correctly serializes all event handlers
- **Attribute Interception**: \`__setattr__\` catches \`on_*\` assignments
- **Backward Compatible**: All existing event patterns continue working

### Dev Mode Stability
- **Debounce**: 300ms consolidation window for file change events
- **State Management**: Proper \`restart_triggered\` flag handling
- **Process Cleanup**: Reliable Electron termination before restart

## Documentation Updates

**Comprehensive Coverage:**
- New \`this()\` section in README with quick examples
- Expanded \`state_management.md\` with complete file operations guide
- Enhanced \`exporters.md\` with desktop API examples and chaining patterns
- Updated \`scripts.md\` with \`.then()\` method documentation

## Migration Notes

### For Existing Projects

**Seamless Upgrade:**
- No breaking changes - all existing code remains compatible
- New features are opt-in and additive
- Event handlers work with both constructor and attribute assignment

## Desktop Exporter Status

**Still in BETA:**
- File operations (\`read_text\`, \`write_text\`, \`read_file\`, \`write_file\`) are stable
- Dev mode with hot reload is fully functional
- Production packaging continues in experimental status
- Native API surface expanding with each release

## Performance & Compatibility

- **Zero Overhead**: Dynamic updates only activate when used
- **Bundle Size**: Minimal impact from new features
- **Browser Support**: Maintains full cross-browser compatibility
- **Desktop Integration**: Enhanced with improved error handling

---

**Upgrade Highly Recommended** for all desktop projects and applications requiring dynamic, event-driven UI updates.


# Release Notes v1.3.6

> Compile-time and runtime component manipulation. Introduces \`app.create()\` / \`app.delete()\` for pre-export tree editing, and \`createComp()\` / \`deleteComp()\` for dynamic DOM operations with safe event hydration.

## Installation

\`\`\`bash
pip install --upgrade dars-framework
\`\`\`

or

\`\`\`bash
pip install dars-framework==1.3.6
\`\`\`

## What's New

### Compile-Time Component Manipulation

- \`app.create(target, root=None, on_top_of=None, on_bottom_of=None)\`
  - Inserts components before/after a reference child or at the end of the \`root\`.
  - Accepts \`target\` as an instance, a callable, or a \`str\` (id to move an existing component).
  - Multipage support: \`root\` can be a component id, a component instance, or a page name.
- \`app.delete(id)\`
  - Removes a component by id from the tree before export (no-op if not found).

### Runtime Component Manipulation

- \`createComp(target, root, position='append')\`
  - Generates a \`dScript\` that calls \`Dars.runtime.createComponent(root_id, vdom_data, position)\`.
  - Serializes the Python component to VDOM and rehydrates events for the subtree.
  - Positions: \`append\`, \`prepend\`, \`before:<id>\`, \`after:<id>\`.
- \`deleteComp(id)\`
  - Generates \`dScript\` that calls \`Dars.runtime.deleteComponent(id)\`.

### Event Hydration for Dynamic Content

- Event rehydration for the newly created subtree (supports arrays of handlers).
- Every dynamic node with an \`id\` also gets \`class="dars-id-<id>"\` for reliable selection when multiple instances exist.

### Barrel Import

- \`from dars.all import *\` now includes \`createComp\` and \`deleteComp\` from \`dars.backend\`.


# Release Notes v1.3.5

> Enhanced styling and development experience update featuring active styles, improved preview system, and advanced file monitoring. Delivers better visual feedback and faster development workflow.

## Installation

\`\`\`bash
pip install --upgrade dars-framework
\`\`\`

or

\`\`\`bash
pip install dars-framework==1.3.5
\`\`\`

## What's New

### Active Styles Support

**Complete Component Styling System:**
- New \`active_style\` attribute for all components, providing visual feedback during user interaction
- Completes the styling triad: \`style\`, \`hover_style\`, and \`active_style\`
- Works seamlessly with existing hover styles introduced in v1.3.4

**Usage:**
\`\`\`python
Button("Click it",
        id="btn1",
        on_click=[dScript('console.log(\`HI\`)'), txtstate.state(1)],
        style={"color": "green"},
        hover_style={"color": "red"},      # from v1.3.4
        active_style={"color": "purple"},  # new in v1.3.5
)
\`\`\`

### Enhanced Preview System

**Optimized Development Server:**
- Completely redesigned preview system with faster load times
- Improved hot reload support for instant code changes
- Better error handling and cleanup processes
- Enhanced Ctrl+C handling for smooth server shutdown

### Advanced File Watcher

**Comprehensive Project Monitoring:**
- New file watching system monitors file creation, deletion, and modification
- Automatic detection of new files in the project directory
- Supports multiple file extensions (.py, .js, .css, etc.)
- Real-time updates without manual intervention

## Fixed Issues

### Responsiveness Improvements
- **Landing Page**: Fixed responsiveness issues on smaller screens
- **Mobile Compatibility**: Enhanced display and interaction on mobile devices

## Technical Improvements

### Development Experience
- **Faster Hot Reload**: Reduced reload intervals and improved change detection
- **Better Error Recovery**: Enhanced error handling during file changes
- **Clean Shutdown**: Improved server termination and resource cleanup

## Migration Notes

### For Existing Projects

**Seamless Upgrade:**
- No breaking changes - all existing code remains compatible
- Active styles can be added incrementally to enhance user interaction

## Desktop Exporter Status

**Still in BETA**

# Release Notes v1.3.4

> Enhanced interactivity update featuring hover styles, multi-handler events, and runtime versioning. Improves component styling and event handling flexibility.

## Installation

\`\`\`bash
pip install --upgrade dars-framework
\`\`\`

or

\`\`\`bash
pip install dars-framework==1.3.4
\`\`\`

## What's New

### Hover Styles Support

**Enhanced Component Interactivity:**
- New \`hover_style\` attribute for all components, allowing dynamic styling on mouse hover
- Styles are automatically generated with higher specificity to ensure proper application

### Multi-Handler Event System

**Flexible Event Management:**
- Components now support arrays of event handlers for the same event type
- Multiple \`dScript\`, inline JavaScript, or mixed handlers can be assigned to single events
- Handlers execute in sequence with individual error handling
- Full backward compatibility with existing single-handler syntax

### Runtime Versioning

**Enhanced Debugging & Tracking:**
- JavaScript runtime now includes version information accessible via \`Dars.version\`
- Release URL exposed through \`Dars.releaseUrl\` for quick reference
- Better debugging and environment identification
- Framework version tracking in deployed applications

**Usage:**
\`\`\`javascript
// Access version information
console.log(\`Using Dars v\${Dars.version}\`);
console.log(\`Release: \${Dars.releaseUrl}\`);
\`\`\`

## Technical Improvements

### Web Exporter Enhancements
- **Improved Style Application**: Fixed CSS generation to ensure all component styles render correctly
- **Robust Event Serialization**: Enhanced handler extraction and code generation for reliable event execution
- **Better Error Handling**: Individual error catching for multi-handler events prevents cascade failures

### Component System
- **Backward Compatibility**: All existing single-handler events continue working unchanged
- **Enhanced Flexibility**: Mix and match handler types (dScript, strings, arrays) with consistent behavior
- **Cleaner Code Generation**: Improved JavaScript output with proper handler separation and error boundaries

## Migration Notes

### For Existing Projects

**Automatic Upgrade:**
- No breaking changes - existing code works identically
- Hover styles can be incrementally added to enhance existing components
- Multi-handler events are optional - single handlers remain fully supported

## Desktop Exporter Status

**Still in BETA** - No changes from v1.3.3

## Performance & Compatibility

- **Zero Overhead**: New features only activate when used
- **Bundle Size**: Minimal impact on final application size
- **Browser Support**: Maintains full cross-browser compatibility
- **Framework Integration**: Seamless with existing Dars ecosystem

---

**Upgrade Recommended** for all projects requiring enhanced interactivity and better development tooling.

# Release Notes v1.3.3

> Minor update featuring new semantic Section component and enhanced state serialization. Continues JavaScript migration improvements from v1.3.2.

## Installation

\`\`\`bash
pip install --upgrade dars-framework
\`\`\`

or

\`\`\`bash
pip install dars-framework==1.3.3
\`\`\`

## What's New

### Section Component

**Semantic HTML Container:**
- New \`Section\` component that renders as \`<section></section>\` instead of generic \`<div>\`
- Maintains all functionality of Container component (children, styles, etc.)
- Improves HTML readability and semantic structure for debugging
- Better accessibility and SEO through proper sectioning elements

**Usage:**
\`\`\`python
# Creates <section> with all container capabilities
Section(Button("HI"), styles={...})
\`\`\`

### Enhanced State & Event Serialization

**Complete JavaScript Migration:**
- States are now fully serialized in JavaScript and no longer exposed in HTML
- Final migration of both state and event systems to pure JavaScript
- Eliminates need for state/event data in VDOM structure
- Improved security and cleaner HTML output

**Benefits:**
- More secure: State data hidden from direct HTML inspection
- Cleaner markup: Reduced data attributes in rendered HTML
- Better performance: Streamlined state management
- Enhanced minification: Better compatibility with Vite optimization

### Documentation Updates

- Updated documentation to reflect new Section component usage
- Enhanced examples and best practices for semantic HTML
- Migration guides for state serialization changes

## Technical Improvements

- **Backward Compatible**: No breaking changes to existing components
- **Progressive Enhancement**: Existing containers continue working as before
- **Performance**: Maintains all optimizations from v1.3.2

## Migration Notes

### For Existing Projects

**Automatic Upgrade:**
- No configuration changes required
- Existing container components remain unchanged
- State management automatically uses new serialization

**Optional Section Component Adoption:**
\`\`\`python
# Old way (still works)
Container(children=[...])

# New semantic way
Section(children=[...])
\`\`\`

## Desktop Exporter Status

**Still in BETA** - No changes from v1.3.2

## Known Issues

- None introduced in this release
- Continuing to monitor Electron desktop exporter stability

---

# Release Notes v1.3.2

> Major minification improvements with combined JS files and optimized event handling. Electron desktop exporter remains in beta.

## Installation

\`\`\`bash
pip install --upgrade dars-framework
\`\`\`

or

\`\`\`bash
pip install dars-framework==1.3.2
\`\`\`

## Highlights

### Enhanced Minification System

**Combined JavaScript Bundles:**
- When \`viteMinify: true\` and \`bundle: true\` are enabled, the exporter now combines all JavaScript files into single optimized bundles
- Single-page apps: All JS combined into \`app.js\`
- Multi-page apps: Each page gets its own \`app_{slug}.js\` bundle
- Eliminates reference issues between separate files during minification

**Optimized Event Handling:**
- Events are no longer stored in VDOM tree
- Event handlers are now generated as valid JavaScript directly in runtime
- Improved compatibility with Vite minification and obfuscation
- Better performance and smaller bundle sizes

**Smart File Management:**
- When using combined bundles, individual files (\`runtime_dars.js\`, \`script.js\`, \`vdom_tree.js\`) are not generated
- HTML files are updated to reference only the combined bundle
- Backward compatible - falls back to separate files when \`viteMinify: false\`

### Vite Minification Perfection

- Vite can now minify the entire application as a single cohesive unit
- Resolves function reference issues that previously broke minification
- Proper obfuscation of all JavaScript code, including event handlers
- Maintains full functionality while significantly reducing bundle size

### Configuration-Driven Behavior

\`\`\`json
{
  "viteMinify": true,
  "bundle": true,
  "defaultMinify": true
}
\`\`\`

- **viteMinify**: Enables advanced Vite-based minification with combined bundles
- **bundle**: Required for production-optimized builds
- **defaultMinify**: Fallback minification when Vite is unavailable

## Bug Fixes

- **Fixed**: Vite minification breaking function references between separate JS files
- **Fixed**: Event handlers not being properly minified and obfuscated
- **Improved**: Multi-page application build performance

## Desktop Exporter Status

**Desktop Exporter remains in BETA**

While the web exporter is now stable and production-ready, the Electron desktop exporter continues in beta due to:

- Ongoing refinement of native API integrations
- Cross-platform packaging and signing requirements
- Advanced IPC and system integration features still in development

**Current Desktop Capabilities:**
- Basic file system operations (\`read_text\`, \`write_text\`)
- Development mode with hot reload
- Production packaging still experimental

## Migration Notes

### For Existing Projects

**No breaking changes** - existing configurations continue to work. To benefit from the new minification:

1. Update your \`dars.config.json\`:
\`\`\`json
{
  "viteMinify": true,
  "bundle": true
}
\`\`\`

2. Run \`dars build\` or \`dars export\` as usual

### Performance Improvements

- **Bundle Size**: Up to 40% reduction in minified JavaScript
- **Load Time**: Faster initial page loads with combined bundles
- **Runtime Performance**: Better optimized event handling
- **Build Time**: More efficient minification process

## Known Issues

- Electron desktop apps may require additional configuration for native module support
- Some edge cases in complex component trees being investigated

## Next Steps

We're working on:
- **v1.4.0**: Production-ready Electron desktop exporter
- **v1.5.0**: Advanced native desktop APIs and system integrations
- **Future**: Plugin system and extended component library

---

# Release Notes v1.3.1 BETA

> Native desktop functions and DX improved with dev mode and file system integration.

## Installation

\`\`\`bash
pip install --upgrade dars-framework
\`\`\`

or

\`\`\`bash
pip install dars-framework==1.3.1
\`\`\`

## Highlights

### Native Functions

You can acces native functions via \`dars.desktop\` module:

\`\`\`python
from dars.desktop import *
\`\`\`

With this module you can acces for now 2 main functions:

\`\`\`python 
write_text("./app/lib/hello.txt", "Hello Text")
\`\`\`
and

\`\`\`python
read_text("./app/lib/hello.txt")
\`\`\`

This two functions allows you to read and write text files in your desktop application filesystem, both returns an dScript() with the code to be executed in the desktop app, and also the 2 functions can be used in events of any component.

Also you can use dScripts to run custom javascript code in the desktop app. and for now 'dars dev' is supported but python main.py with rTimeCompile() is not supported because it have issues with relative paths.

## Bug Fixes

- Fixed dev failures with hot reload using desktop format.

## Notes(Warning)

- This feature set is **BETA**. Many options (signing, advanced IPC, updates, and deeper configuration) are still evolving.
- Usable for internal tools and early testing. Not recommended for production deployment yet.
- Expect changes to configuration keys and defaults in future versions.


# Release Notes v1.3.0 BETA

> Native desktop export (BETA), improved CLI and doctor integration, and metadata fixes for packaging. This is a BETA release: usable for testing, not recommended for production.

## Installation

\`\`\`bash
pip install --upgrade dars-framework
\`\`\`

or

\`\`\`bash
pip install dars-framework==1.3.0
\`\`\`

## Highlights

- **New: Native Desktop Export (BETA)**
  - Build desktop apps directly from Dars projects.
  - Project config supports \`format: "desktop"\` and \`targetPlatform\` (\`auto|windows|linux|macos\`).
  - Backend scaffold via \`dars init --type desktop\` (or \`--update\`), generating minimal main process files and preload bridge.
  - IPC bridge includes basic FS read/write for quick experiments.
  - Source emitted to \`dist/source-electron/\`; packaged artifacts in \`dist/\`.
  - Note: This capability is BETA and not recommended for production yet.

- **New: Desktop Build Flow in CLI**
  - \`dars build\` respects \`format: "desktop"\` in \`dars.config.json\`.
  - Platform flags are selected automatically or via \`targetPlatform\`.
  - Robust error output: full stdout/stderr on packaging failure.

- **New: Doctor Integration for Desktop Tooling**
  - \`dars doctor --all --yes\` checks and installs optional desktop tooling.
  - Pins the desktop runtime to a compatible version automatically when needed.

- **Packaging Reliability Improvements**
  - Project metadata auto-filled from \`App\` (name/title, description, author, version) with sensible defaults.
  - Version defaulted to \`0.1.0\` when absent (warning emitted).
  - Package manager forced to a stable toolchain to avoid ENOENT errors during packaging.
  - Runtime version pinned explicitly in both dev deps and build config to ensure predictable builds.

## Quickstart (Desktop BETA)

\`\`\`bash
# Initialize or update a project with desktop scaffolding
dars init --type desktop
# or
dars init --update

# Verify optional tooling
dars doctor --all --yes

# Build using project config (format: "desktop")
dars build
\`\`\`

Minimal \`dars.config.json\` for desktop:

\`\`\`json
{
  "entry": "main.py",
  "format": "desktop",
  "outdir": "dist",
  "targetPlatform": "auto"
}
\`\`\`

## Bug Fixes

- Fixed packaging failures caused by missing metadata in project manifests by auto-populating:
  - \`description\` from \`App.description\` (fallback to a default)
  - \`author\` from \`App.author\` (fallback to a default)
  - \`version\` from \`App.version\` (fallback \`0.1.0\` with warning)
- Stabilized packaging by pinning desktop runtime version in both dev dependencies and build configuration.
- Avoided package-manager ENOENT errors in packaging by forcing a stable manager and resolving runners reliably on Windows.
- Correct platform flags for packaging: \`--win\`, \`--linux\`, \`--mac\`.
- Improved error reporting to include stdout and stderr from the packaging tool.

## Notes

- This feature set is **BETA**. Many options (signing, advanced IPC, updates, and deeper configuration) are still evolving.
- Usable for internal tools and early testing. Not recommended for production deployment yet.
- Expect changes to configuration keys and defaults in future versions.

I spent ~1 month iterating on this capability and consolidated changes into this single BETA release once it reached a usable threshold. Feedback is welcome to help stabilize and expand the desktop feature set.

# Release Notes v1.2.9

> Optional default minification, precise CLI control, faster builds, and clearer minification status.

## Installation

\`\`\`bash
pip install --upgrade dars-framework
\`\`\`

or

\`\`\`bash
pip install dars-framework==1.2.8
\`\`\`

## Highlights

- **New: Configurable Default Minifier**
  - \`defaultMinify\` (default: true) controls the built\u2011in Python minifier.
  - Preserves \`pre\`, \`code\`, \`textarea\`, \`script\`, \`style\`.
  - Only removes non\u2011conditional HTML comments and collapses spaces between tags.
  - Does not collapse text-node spaces (Markdown and \`<pre><code>\` remain intact).

- **New: CLI Flag \`--no-minify\`**
  - Available in \`dars build\` and \`dars export\`.
  - Disables only the default Python minifier for that run.
  - Independent from \`viteMinify\`.

- **Minification Modes Work Together**
  - When \`defaultMinify\` and \`viteMinify\` are both true:
    - Default minifier applies (safe HTML and fallback for JS/CSS).
    - Vite/esbuild minify JS/CSS where available.
  - Status line now reflects the active mode:
    - \u201CApplying minification (default)\u201D
    - \u201CApplying minification (vite)\u201D
    - \u201CApplying minification (default + vite)\u201D

- **Faster Default Minifier**
  - Default minifier uses fast Python fallback (rjsmin/rcssmin/regex) and never shells out to Vite/esbuild.
  - Results in near\u2011instant minification step.

## Bug Fixes

- Default minifier no longer ignores config; \`defaultMinify\` and \`--no-minify\` are strictly honored.
- Eliminated unintended use of esbuild/Vite inside the default minifier.
- Improved label accuracy to match the actual minification pipeline (default, vite, or both).

## Notes

- Relevant configuration:
  - \`defaultMinify\`: true/false. Controls the Python-side minification (HTML + JS/CSS fallback).
  - \`viteMinify\`: true/false. Controls Vite/esbuild for JS/CSS when available.
- Backward compatibility:
  - Defaults maintain previous behavior, now safer for Markdown/code blocks.
  - You can disable default minification per-run with \`--no-minify\` without affecting \`viteMinify\`.

Upgrade Recommendation: Recommended for all users; especially helpful for projects with Markdown/code samples and those wanting faster, more controllable minification.

# Older release notes can be found

In the github repository [Here](https://github.com/ZtaMDev/Dars-Framework/releases).
`}]},{type:"T2",id:"footer-section",key:"0/1/1",children:[{type:"T2",id:"text_21",key:"0/1/1/0",children:[{type:"T2",id:"container_143",key:"0/1/1/0/0",children:[{type:"T2",id:"container_27",key:"0/1/1/0/0/0",children:[{type:"T4",id:"link_74",key:"0/1/1/0/0/0/0"},{type:"T2",id:"container_22",key:"0/1/1/0/0/0/1",children:[{type:"T5",id:"text_25",key:"0/1/1/0/0/0/1/0",text:"Dars Framework"}]}]},{type:"T2",id:"container_144",key:"0/1/1/0/0/1",children:[{type:"T2",id:"container_145",key:"0/1/1/0/0/1/0",children:[{type:"T5",id:"text_146",key:"0/1/1/0/0/1/0/0",text:"Quick Links"},{type:"T6",id:"link_75",key:"0/1/1/0/0/1/0/1",text:"Documentation"},{type:"T6",id:"link_79",key:"0/1/1/0/0/1/0/2",text:"GitHub"},{type:"T6",id:"link_78",key:"0/1/1/0/0/1/0/3",text:"Examples"}]},{type:"T2",id:"container_147",key:"0/1/1/0/0/1/1",children:[{type:"T5",id:"text_148",key:"0/1/1/0/0/1/1/0",text:"Resources"},{type:"T6",id:"image_32",key:"0/1/1/0/0/1/1/1",text:"Getting Started"},{type:"T6",id:"link_89",key:"0/1/1/0/0/1/1/2",text:"Releases"}]},{type:"T2",id:"container_149",key:"0/1/1/0/0/1/2",children:[{type:"T5",id:"text_150",key:"0/1/1/0/0/1/2/0",text:"A modern FullStack Python framework for web and desktop applications."}]}]},{type:"T2",id:"container_151",key:"0/1/1/0/0/2",children:[{type:"T2",id:"container_152",key:"0/1/1/0/0/2/0",children:[{type:"T5",id:"text_153",key:"0/1/1/0/0/2/0/0",text:"\xA9 2025 Dars Framework."}]},{type:"T2",id:"container_154",key:"0/1/1/0/0/2/1",children:[{type:"T5",id:"text_155",key:"0/1/1/0/0/2/1/0",text:"Created with "},{type:"T6",id:"image_51",key:"0/1/1/0/0/2/1/1",text:"Dars Framework"},{type:"T5",id:"text_156",key:"0/1/1/0/0/2/1/2",text:" by "},{type:"T6",id:"image_57",key:"0/1/1/0/0/2/1/3",text:"ZtaDev"}]}]}]}]}]}]},{type:"T10",id:"documentation-sidebar",key:"0/2"}]};(function(){const d=new Map;let l=null,p=null;function u(){}function S(){}function v(n,t){if(!n)return;t(n);const e=n.children||[];for(let a=0;a<e.length;a++)v(e[a],t)}function k(n,t){if(!(!n||!t))for(const[e,a]of Object.entries(t))try{a===!1||a===null||typeof a>"u"?n.removeAttribute(e):n.setAttribute(e,String(a))}catch{}}function T(n,t={},e={}){for(const a in t)if(!(a in e))try{n.removeAttribute(a)}catch{}for(const a in e){const o=e[a];try{o===!1||o===null||typeof o>"u"?n.removeAttribute(a):n.setAttribute(a,String(o))}catch{}}}function A(n,t={},e={}){for(const a in t)if(!(a in e))try{n.style.removeProperty(a.replace(/_/g,"-"))}catch{}for(const a in e){const o=e[a];try{n.style.setProperty(a.replace(/_/g,"-"),String(o))}catch{}}}function V(n,t){(t||document).addEventListener(n,function(e){let a=e.target;const o=t||document;for(;a&&a!==o;){const m=a.id;if(m&&d.has(m)){const y=d.get(m);if(a&&a.__darsEv&&a.__darsEv[n])return;let c=y[n];if(!c&&(n==="keydown"||n==="keyup"||n==="keypress")){const i=e.key||e.code;if(i){const r=n+"."+i;c=y[r]}}if(typeof c=="function"){try{c.call(a,e)}catch(i){console.error("[Dars] handler error",i)}return}}a=a.parentNode}},!0)}function _(n,t){return n&&t?n.type!==t.type:n!==t}function x(n){if(!n)return;const t=n.children||[];for(let e=0;e<t.length;e++)x(t[e]);if(n.id&&d.delete(n.id),n.id){const e=document.getElementById(n.id);if(e&&e.parentNode)try{e.parentNode.removeChild(e)}catch{}}}function b(n,t){if(!t||!t.id)return{ok:!1,reason:"missing-new"};let e=document.getElementById(t.id);if(!e){const i=n&&n.id?document.getElementById(n.id):null;if(i)try{i.id=t.id,e=i}catch{}}if(!e)return{ok:!1,reason:"missing-el"};if(_(n,t))return{ok:!1,reason:"type-changed"};const a=!!t.isIsland;if(!a&&t.class&&(e.className=t.class),a||T(e,n&&n.props||{},t.props||{}),a||A(e,n&&n.style||{},t.style||{}),!a&&Object.prototype.hasOwnProperty.call(t,"text")&&e.textContent!==String(t.text||"")&&(e.textContent=String(t.text||"")),a)return{ok:!0};const o=n&&n.children?n.children:[],m=t.children?t.children:[],y=new Map;for(let i=0;i<o.length;i++){const r=o[i]&&(o[i].id||o[i].key)||null;r&&y.set(String(r),o[i])}const c=new Set;for(let i=0;i<m.length;i++){const r=m[i],h=r&&(r.id||r.key)||null;if(!h)if(i<o.length){const s=b(o[i],r);if(!s.ok)return s;c.add(o[i]);continue}else return{ok:!1,reason:"children-added"};const w=y.get(String(h));if(w){const s=b(w,r);if(!s.ok)return s;c.add(w)}else{if(i<o.length){const f=o[i];if(!_(f,r)){const g=b(f,r);if(!g.ok)return g;c.add(f);continue}}const s=createSubtree(r);if(s){const f=i<o.length?o[i]:null;if(f&&f.id){const g=document.getElementById(f.id);g&&g.parentNode?g.parentNode.insertBefore(s,g):e.appendChild(s)}else e.appendChild(s);continue}return{ok:!1,reason:"children-added"}}}for(let i=0;i<o.length;i++){const r=o[i];c.has(r)||x(r)}return{ok:!0}}function R(n){typeof requestAnimationFrame=="function"?requestAnimationFrame(n):setTimeout(n,16)}function E(n){const t=l;if(!t){l=n;try{window.__DARS_VDOM__=n}catch{}return}R(()=>{const e=b(t,n);if(!e.ok){console.warn("[Dars] Structural change detected (",e.reason,"), reloading...");try{location.reload()}catch{}return}l=n;try{window.__DARS_VDOM__=n}catch{}})}function C(n){l=n;try{window.__DARS_VDOM__=n}catch{}["click","dblclick","mousedown","mouseup","mouseenter","mouseleave","mousemove","keydown","keyup","keypress","change","input","submit","focus","blur"].forEach(e=>V(e,document))}function I(){try{if(window.__DARS_HOTRELOAD_DISABLED__)return()=>{}}catch{}const n=window.__DARS_VERSION_URL||"version.txt";let t=null,e=!1,a=0;const o=10;let m=!1;function y(i,r,h,w){try{const s=new XMLHttpRequest;w&&(s.responseType=w),s.open("GET",i,!0),s.timeout=5e3,s.onreadystatechange=function(){s.readyState===4&&(s.status>=200&&s.status<300?r(s.response):h())},s.onerror=h,s.ontimeout=h,s.setRequestHeader("Cache-Control","no-store"),s.send()}catch{h()}}function c(){m||y(n,function(i){let r=(i||"").toString().trim();if(!r||r==="0"){if(a+=1,a>=o){console.warn("[Dars] version file not found after",o,"attempts. Hot reload disabled for this session."),m=!0;try{window.__DARS_HOTRELOAD_DISABLED__=!0,window.__DARS_STOP_HOTRELOAD=null}catch{}if(t)try{clearTimeout(t)}catch{}return}e||(console.warn("[Dars] waiting for version file..."),e=!0),t=setTimeout(c,600);return}if(a=0,e=!1,p||(p=r),r&&r!==p){p=r;try{location.reload()}catch{}return}t=setTimeout(c,600)},function(){if(a+=1,a>=o){console.warn("[Dars] version file not reachable after",o,"attempts. Hot reload disabled for this session."),m=!0;try{window.__DARS_HOTRELOAD_DISABLED__=!0,window.__DARS_STOP_HOTRELOAD=null}catch{}if(t)try{clearTimeout(t)}catch{}return}e||(console.warn("[Dars] waiting for version file..."),e=!0),t=setTimeout(c,600)},"text")}return c(),()=>{try{m=!0,t&&clearTimeout(t),window.__DARS_STOP_HOTRELOAD=null}catch{}}}function D(){if(window.__DARS_VDOM__?C(window.__DARS_VDOM__):window.__ROUTE_VDOM__?C(window.__ROUTE_VDOM__):console.warn("[Dars] No VDOM snapshot found for hydration"),window.__DARS_VERSION_URL&&window.__DARS_SNAPSHOT_URL){try{typeof window.__DARS_STOP_HOTRELOAD=="function"&&window.__DARS_STOP_HOTRELOAD()}catch{}try{window.__DARS_STOP_HOTRELOAD=I()}catch{}}}document.readyState==="complete"||document.readyState==="interactive"?D():document.addEventListener("DOMContentLoaded",D)})();window.addEventListener("scroll",()=>{const d=document.getElementById("dars-navbar");window.scrollY>20?d.classList.add("scrolled"):d.classList.remove("scrolled");const l=document.getElementById("features-section");if(l&&!l.classList.contains("visible")){const p=l.getBoundingClientRect().top,u=window.innerHeight/1.5;p<u&&(l.classList.add("visible"),document.querySelectorAll('[id^="feature-card-"]').forEach((v,k)=>{setTimeout(()=>{v.style.opacity="1",v.style.transform="translateY(0)"},k*100)}))}});document.addEventListener("DOMContentLoaded",function(){const d=document.getElementById("hamburger-btn"),l=document.getElementById("mobile-menu"),p=document.body;d&&l&&(d.addEventListener("click",function(u){u.stopPropagation(),l.style.display==="flex"?(l.style.display="none",d.classList.remove("menu-open"),p.classList.remove("menu-open")):(l.style.display="flex",d.classList.add("menu-open"),p.classList.add("menu-open"))}),l.querySelectorAll("a").forEach(u=>{u.addEventListener("click",function(){l.style.display="none",d.classList.remove("menu-open"),p.classList.remove("menu-open")})}),document.addEventListener("click",function(u){!d.contains(u.target)&&!l.contains(u.target)&&(l.style.display="none",d.classList.remove("menu-open"),p.classList.remove("menu-open"))}),document.addEventListener("keydown",function(u){u.key==="Escape"&&l.style.display==="flex"&&(l.style.display="none",d.classList.remove("menu-open"),p.classList.remove("menu-open"))}))});})();
