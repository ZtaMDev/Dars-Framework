# Release Notes v1.9.3

> **Configurable Dev Port, Local DOMPurify & Runtime Resource Optimization**

## Installation

```bash
pip install --upgrade dars-framework
```

## What's New

### Configurable Development Port

You can now customize the port used by the `dars dev` preview server directly in your project configuration or via CLI:

- **`dars.config.json`**: Added a new `"port"` field (default: `8000`).
- **CLI Override**: Use `--port` or `-P` to override the configuration at runtime.
  ```bash
  dars dev --port 4000
  ```
- **Automatic Propagation**: The CLI now correctly propagates the port setting to the underlying application process.

### Localized Runtime Dependencies (CDN-Free)

To improve load times and reliability, especially in offline or restricted environments, we have moved core runtime dependencies from CDNs to local assets:

- **Local DOMPurify**: The framework now includes and uses a local version of `dompurify.js`.
- **Resource Management**: Core runtime resources are now managed within a dedicated `resources/` directory in the web exporter and copied to the `/lib` directory of the final export.

### Python-Native Resource Minification

The minification pipeline has been extended to ensure all runtime assets are as lean as possible:

- **`rjsmin` Integration**: All JavaScript resources, including `dompurify.js` and the Dars runtime, are now minified using the Python-native `rjsmin` during the export process.
- **Improved Build Speed**: By avoiding external tools like Vite for core library minification, we maintain a fast and stable build process.

### Runtime Architecture Improvements

- **Resource Decoupling**: The legacy `js_lib.py` has been retired in favor of a file-based resource system. This allows for better code splitting and easier maintenance of the Dars runtime components.
- **Port Detection Hardening**: Improved the `rTimeCompile` logic to reliably detect the project root and configuration, ensuring that custom settings are respected even when starting the app from different working directories.

---

# Release Notes v1.9.2

> **Documentation Corrections & Complete App Class Docstring**

## Installation

```bash
pip install --upgrade dars-framework
```

## What's New

### Standardized Component Docstrings

Fixed documentation inconsistencies across all component modules:

- **`class_name` Documentation**: Corrected to reflect that it contains **regular CSS class names** (not utility classes) for standard HTML class attributes.
- **`style` Documentation**: Updated to clarify that it contains **CSS utility classes** (Tailwind-like syntax) for convenience styling.

### Complete App Class Docstring

Added a comprehensive docstring to the `App` class with:

- Detailed description of SPA, MPA, and Desktop modes.
- Complete property documentation for all constructor parameters.
- SEO and PWA configuration details.
- Usage examples for each mode.

---

# Release Notes v1.9.1

> **Premium Utility Styles, DAP Reactivity Fixes & Documentation Overhaul**

## Installation

```bash
pip install --upgrade dars-framework
```

## What's New

### Utility Style System

We've significantly expanded the utility-first styling system to bring it closer to a better developer experience, adding many features:

- **Advanced Gradients**: Full support for multi-stop gradients using `bg-gradient-to-{dir}`, `from-{color}`, `via-{color}`, and `to-{color}`. Internally uses a modern CSS variable architecture (`--tw-gradient-stops`).
- **Ring System**: New utilities for outer rings and focus indicators: `ring`, `ring-{n}`, `ring-{color}`, `ring-opacity-{n}`, and `ring-offset-{n}`.
- **Smart Property Switching**: The `text-` prefix is now intelligent. It automatically switches between `font-size` and `color` based on the provided value (e.g., `text-xl` vs `text-indigo-500`).
- **Divide Utilities**: Added `divide-x` and `divide-y` to easily add borders between child elements.
- **New UI Utilities**: Added `accent-{color}`, `caret-{color}`, `line-clamp-{n}`, and expanded support for specific border sides (e.g., `border-t-2`, `border-x-4`).
- **Shadow Colors**: Support for colored shadows via `shadow-{color}`.

### DAP & Reactivity Hardening

- **Fixed `updateVRef` Reactivity**: Resolved a critical issue where components using `ValueRef` (via `setVRef`) were not consistently re-rendering when updated through Dars Action Protocol (DAP) scripts.

### Documentation

- **Complete Documentation**: All guides in the landing page have been restructured for better flow and clarity.
- **Standardized Docstrings**: Every core component and utility function now features a complete Python docstring, including:
  - Detailed property descriptions.
  - Standard global props list.

---

# Release Notes v1.9.0

> **Secure Action Protocol (DAP) & Zero-Eval Runtime Hardening**

## Installation

```bash
pip install --upgrade dars-framework
```

## What's New

### Definitive Removal of `new Function()`

Building on the milestone of v1.8.9, v1.9.0 achieves a 100% "Zero-Eval" runtime for all dynamic event execution.

- **Context-Aware Script Injection**: Dynamic scripts (event handlers, lifecycle hooks) are now executed via a secure script injection mechanism that natively propagates `event` and `element` (the `this` context) without using `eval()` or `new Function()`.

### Dars Action Protocol (DAP) v2: Command Registry

Introduced a centralized **Command Registry** in the browser runtime (`dars.min.js`). This moves the framework from "sending code strings" to "sending structured commands".

- **Pre-defined Operations**: All common UI tasks (navigation, state changes, modal control, DOM updates) are now registered as secure, pre-defined operations.
- **Protocol-Driven Execution**: The `dispatch(action, context)` function ensures that actions are processed as structured data objects `{op, args}`, eliminating the risk of arbitrary code execution.
- **Advanced Control Flow**: Support for sequences, delays, and conditional logic within the protocol itself.

### Expanded DAP Command Library

The browser runtime now includes a comprehensive library of registered commands, covering almost all utility functions in `utils_ds.py`:

- **Interactive Dialogs**: `alert`, `confirm` (with DAP-driven `on_ok`/`on_cancel` callbacks), and `log`.
- **Navigation & History**: `navigate`, `reload`, `history_back`, `history_forward`.
- **DOM & Visibility**: `dom_show`, `dom_hide`, `dom_toggle`, `dom_focus`, `dom_blur`, `dom_reflow`.
- **Content & Styles**: `dom_set_text`, `dom_set_html` (sanitized via DOMPurify), `dom_set_style`, `dom_set_attr`, `class_add`, `class_remove`, `class_toggle`.
- **Storage & State**: `storage_set`, `storage_remove`, `storage_clear`, and `storage_get` (with direct state-update mapping).
- **Network**: Native `fetch` support with success and error handlers.
- **VRefs**: `vref_update` and `vref_get`.

### Reliable Markdown Highlighting & Assets

Fixed several long-standing issues with Prism.js integration and global asset management:

- **SSR Highlight Consistency**: Ensured that syntax highlighting works reliably in SSR, static exports, and SPA transitions using a robust retry-based initialization and a centralized asset registry.

---

# Release Notes v1.8.11

> **Native String Concatenation & Math Fixes**

## Installation

```bash
pip install --upgrade dars-framework
```

## What's New

### Restored Native String Concatenation

Fixed a major regression in `MathExpression` where using the `+` operator aggressively coerced all operands into `parseFloat()`. This behavior broke string concatenation, resulting in `0` or `NaN` when attempting to combine strings and `ValueRef` values.

- The compiler now generates native JavaScript addition `(left + right)`.
- JavaScript handles type inference automatically: combining strings will safely concatenate them, and combining numeric values will add them.
- If strict numeric addition is required from a DOM input (which usually returns strings), developers must explicitly use `.float()` or `.int()` on the `ValueRef` (e.g. `V(".num1").float() + V(".num2").float()`).

---

# Release Notes v1.8.10

> **State V2 Reactivity Hardening & FunctionComponent Fixes**

## Installation

```bash
pip install --upgrade dars-framework
```

## What's New

### State V2 Reactivity Decoupling

The Dars runtime state manager has been decoupled from strict physical DOM bindings, enabling robust reactivity for headless and virtual components:

- **State Registry Priority**: The `change()` handler now persists new state values to the internal `__reactiveRegistry` before attempting to locate a DOM element. This ensures that virtual states update reliably even when no matching element ID exists.
- **Arithmetic State Operations**: Fixed a critical bug where `increment` and `decrement` methods would always evaluate from `0` when bound to headless states. The `startLoop()` runtime function now checks the state registry if a target element is not found, allowing seamless mathematical operations in the background.

### FunctionComponent Reactivity Fixes

Resolved multiple issues affecting `useDynamic` and reactive bindings inside `@FunctionComponent` trees:

- **Binding Export Fix**: FunctionComponent templates are now correctly pre-rendered during multi-page (`app.add_page`) generation. This ensures that all `useDynamic` bindings nested inside FunctionComponents are successfully collected and exported into the reactive Javascript bundle.
- **Runtime Generation Fix**: Repaired a syntax error in the internal reactive JavaScript generator (`_generate_reactive_bindings_js`) that caused silent failures (missing closing braces) when exporting a project containing exclusively FunctionComponent bindings without any standard built-in bindings.

---

# Release Notes v1.8.9

> **Ultimate Security & Reactivity Hardening: Removal of Eval/New Function & Native JS Compilation**

> [!IMPORTANT]
> **SECURITY ADVISORY**: v1.8.9 achieves a major milestone by removing `eval()` and `new Function()` from the core client-side runtime (`dars.min.js`). However, the web framework (as seen in certain SSR/Fullstack exports) is not yet 100% free of `new Function()` and `_executeExternalScript` for specific dynamic execution flows. This will be fully addressed in the upcoming **Dars Flight Protocol (DFP)** release.

## Installation

```bash
pip install --upgrade dars-framework
```

## What's New

### Zero Eval Runtime & Secure Script Execution

We have completely overhauled how Dars executes dynamic code in the browser.

- **Removal of Legacy Eval**: Major instances of `eval()` and `new Function()` have been eliminated from the runtime (`dars.min.js`).
- **Async IIFE Injection**: Dynamic scripts (event handlers, lifecycle hooks) are now executed via a secure, async IIFE-based script injection mechanism. This provides better scope isolation and prevents global scope pollution.
- **Native `await` Support**: You can now use `await` directly within any event handler or transformation script.

### Native JavaScript Compilation Pipeline

The `dScript` compiler is now a core framework utility, moving complex resolution logic from the browser to the build/export phase.

- **Optimized JS Emission**: Python expressions using `V()`, `MathExpression`, and `BooleanExpression` are now compiled into clean, native JavaScript code strings.
- **Consistent Serialization**: Centralized the `compile_val` logic to ensure that complex structures (lists, dicts) containing reactive objects are correctly translated into executable JS literals, resolving previous "RawJS is not serializable" warnings.

### Hardened Reactivity & Math Logic

Fixed several long-standing issues with the reactivity pipeline:

- **Smart Arithmetic vs Concatenation**: Resolved the `NaN` errors in calculators. The compiler now correctly handles the `+` operator, favoring native JS concatenation for strings and addition for numbers.
- **Template Literal Safety**: Refactored the `url()` and `transform()` helpers to use a structured concatenation model, eliminating `SyntaxError: Unexpected identifier` issues caused by nested backticks in template literals.

### Async-Aware VDOM & Lazy Hydration

The initial rendering engine (`_elFromVNode`) is now asynchronous-aware:

- **Lazy Property Resolution**: VDOM properties (text, class, style, attributes) can now be initialized with Promises. The runtime will automatically hydrate these properties as they resolve, enabling powerful async patterns during the initial render.
- **Fixed Code Injection Bugs**: Resolved the issue where raw JS code strings were occasionally rendered as text in the browser instead of being executed.

### Bug Fixes

- **Recursive Compiler**: `compile_val` now recursively handles nested collections, ensuring all parts of a complex prop are correctly compiled.
- **Fixed VRef Rendering**: Improved the `ValueRef` string representation to integrate seamlessly with the new native compiler.

---

# Release Notes v1.8.8

> **Critical Security Update: Dars Server Protocol (DSP) & SSR Hydration Fix**

> [!CAUTION]
> **SECURITY WARNING**: Versions <= v1.8.7 are considered deprecated and NOT recommended for production use. v1.8.8 addresses critical security surfaces by temporarily removing experimental Server Components. Upgrading is mandatory.

## Installation

```bash
pip install --upgrade dars-framework
```

## What's New

### Dars Server Protocol (DSP)

Introduced a new unified protocol for transmitting VDOM snapshots, component states, and reactive bindings from the server to the client. This ensures that SSR-rendered pages are hydrated with full parity to client-side renders.

### SSR Hydration & Interactivity Fixes

Resolved critical issues where reactive bindings (`useDynamic`) and `VRef` bindings were not correctly executed after initial server rendering.

- **Unified Reactivity Registry**: Client-side bindings are now registered through a centralized mechanism, preventing ID mismatches.
- **Improved SPA Routing**: The client-side router now natively supports DSP payloads, allowing seamless interactivity when navigating between SSR-rendered routes.

### [IMPORTANT] Server Components Removal

As part of security hardening, the experimental "Dars Server Components" feature (using `use_server=True`) has been removed from this version.

- Projects using this feature should transition to the standard **SSR Route** architecture, which now provides superior performance and security through the DSP.
- This removal reduces the attack surface while we work on a more robust, sandboxed implementation for future releases.

---

# Release Notes v1.8.7

> **Dars Server Components & FastAPI Integration**

## Installation

```bash
pip install --upgrade dars-framework
```

## What's New

### Dars Server Components

v1.8.7 introduces **first-class Server Components**, allowing individual components to be fully rendered on the server while maintaining client-side interactivity.

- **Simple Usage**: Just add `use_server=True` to any component inheriting from the base `Component` class.
- **Full Support**: All standard Dars components (Text, Button, Container, etc.) support server-side rendering out of the box.
- **Seamless Hydration**: Components are rendered on the backend (FastAPI) and hydrated on the client, preserving events and state.

```python
Button("Server Rendered Button", use_server=True, on_click=...)
```

### FastAPI Integration Plugin

The new version of `create_dars_app` plugin provides tight integration with FastAPI, making it easier than ever to build full-stack SSR applications.

- **Backend-Driven**: The Dars frontend is served and managed by your FastAPI backend.
- **API Co-location**: Define your API routes and your UI components in the same project structure.

### SSR Project Template

Scaffold a complete SSR project and then add Server Components support in seconds:

```bash
dars init my-app --type ssr
```

This template sets up:

- A FastAPI backend using `create_dars_app`.
- A Dars frontend configured for SSR.
- Best practices for project structure and deployment.

---

# Release Notes v1.8.6

> **Environment Management & File Upload Component**

## Installation

```bash
pip install --upgrade dars-framework
```

## What's New

### DarsEnv: Environment Awareness

New `DarsEnv` class provides a standard way to check the current environment mode:

- `DarsEnv.dev`: returns `True` during development (`dars dev`), and `False` during production builds (`dars build` / `dars export`).

This allows you to write conditional logic in your components:

```python
from dars.env import DarsEnv

Link(target="/docs" if DarsEnv.dev else "https://example.domain.com/env", text="Docs")
```

### FileUpload Component

A new `FileUpload` component is now available in `dars.components.advanced`:

- Wraps `<input type="file">` with a custom, styleable interface.
- Supports `accept`, `multiple`, and hidden input handling.
- Fully reactive `on_change` events.

```python
from dars.components.advanced import FileUpload

FileUpload(
    label="Upload Document",
    accept=".pdf",
    on_change=log("File uploaded")
)
```

---

# Release Notes v1.8.5

> **Outlet improvements + SSR lazy-load placeholders + SPA router hardening**

## Installation

```bash
pip install --upgrade dars-framework
```

## What's New

### Multiple Outlets via `outlet_id`

Nested routing now supports targeting a specific outlet in a parent layout:

- `Outlet(outlet_id="main" | "sidebar" | ...)`
- `app.add_page(..., outlet_id="...")`
- The SPA config includes `outletId` per route so the client router can mount the child route into the correct outlet.

### Optional `Outlet(placeholder=...)`

`Outlet` can render an optional placeholder while the child route region is empty (e.g. SSR lazy-load or SPA navigation).
If `placeholder` is not provided, the outlet remains empty.

### SSR lazy-load loading/error placeholders (SPA navigation)

New API:

- `app.set_loading_state(loadingComp, onErrorComp)`

Exporters and the SSR backend render these as static HTML placeholders and expose them to the SPA router.
This keeps state/events safe and avoids breaking hydration.

### Trailing slash normalization

The SPA router now treats paths with trailing slashes as equivalent:

- `/dashboard` and `/dashboard/` match the same route

This prevents incorrect 404 redirects when a user navigates to a valid route with a trailing slash.

---

# Release Notes v1.8.4

> **Python-native minification + major Utility Styles upgrade**

## Installation

```bash
pip install --upgrade dars-framework
```

## What's New

### Python-native minification by default (no Node/Bun required)

v1.8.4 upgrades the default minification pipeline to use real, battle-tested Python minifiers:

- **JavaScript**: `rjsmin`
- **CSS**: `rcssmin`

This makes builds and exports work reliably in pure-Python environments.

### Optional `viteMinify` mode preserved

If you enable `viteMinify: true` in `dars.config.json`, Dars can still use Vite/esbuild **optionally** when available.
When tools are not installed, Dars falls back to the Python minifiers automatically.

### Runtime bundle safety: `dars.min.js`

The embedded runtime bundle (`dars.min.js`) is now treated as a special case:

- It is **never** passed through Vite/esbuild (to prevent corruption / ESM `export` output).
- It is minified using **Python-only `rjsmin`**, regardless of `viteMinify`.

### Utility Styles: Arbitrary Properties (`prop-[value]`)

The utility system now supports Tailwind-like **arbitrary properties**:

```python
style="background-image-[linear-gradient(90deg,_rgba(0,0,0,.35),_#00ffcc)]"
style="padding-[calc(1rem_+_2vw)]"
style="color-[var(--brand-color)]"
style="--brand-color-[#00ffcc]"
```

Also includes background gradient support via `bg-[linear-gradient(...)]` (maps to `background-image`).

### Utility Styles: composable `filter` / `backdrop-filter` / `transform`

Multiple filter/transform utilities now **compose** instead of overwriting:

```python
style="filter-[blur(6px)] filter-[brightness(120%)]"
```

### Bug fixes for utility parsing

- Fixed `text-[#hex]` / `text-[rgba(...)]` being interpreted as `font-size` instead of `color`.
- Fixed prefix collisions like `border-top-[...]` incorrectly becoming `border-color: top-[...]`.

### LandingPage: navbar styles migrated to utility strings

The LandingPage navbar now uses `style="..."` utility strings instead of large inline style dicts,
improving consistency and providing a real-world example of the upgraded styling system.

---

# Release Notes v1.8.3

> **Critical Build Fix**

## Installation

```bash
pip install --upgrade dars-framework
```

## What's New

### Fixed production build crash: `Unexpected token 'export'`

In some environments, the JS minification pipeline (Vite/esbuild) could emit ESM output ending with `export default ...` inside `app.js`. Since exported pages load `app.js` as a classic script, browsers would fail to parse it with:

`Uncaught SyntaxError: Unexpected token 'export'`

v1.8.3 fixes this by forcing the minifier output format to **IIFE** for browser scripts, preventing ESM `export` statements from being generated during build.

---

# Release Notes v1.8.2

> **Bug Fixes & Utility System Improvements**

## Installation

```bash
pip install --upgrade dars-framework
```

## What's New

### Fixed setTimeout Promise Handling

The `setTimeout` utility function in `utils_ds.py` has been updated to properly return a Promise, enabling correct chaining with `.then()` operations. This fixes JavaScript syntax errors that occurred when using sequential animations or delayed operations.

### Enhanced Animation System

Improved the animation chaining system to handle missing DOM elements gracefully, preventing runtime errors when referenced elements don't exist in the component tree.

### Responsive Design Enhancements

Updated CSS media queries for better handling of text overflow on small screens, ensuring content remains readable across all device sizes without cutting off important information.

---

# Release Notes v1.8.1

> **Style System Optimization & SSR-Aware Registry**

## Installation

```bash
pip install --upgrade dars-framework
```

## What's New

### New Style Optimization Pipeline (Phase 1)

v1.8.1 introduces the first phase of a new **style optimization system** focused on reducing inline CSS while keeping full compatibility with Dars reactivity and dynamic operations.

- Static styles defined via `style={...}` or Tailwind-like strings in `style="..."` are now:
  - Parsed into CSS dicts by the exporter.
  - Fingerprinted and converted into generated classes: `.dars-s-<hash>`.
  - Emitted once into a central style registry instead of repeating large inline `style` blocks.
- The exporter automatically attaches the generated class to the component and clears the redundant inline style, resulting in:
  - Smaller HTML output.
  - Less DOM churn on updates.
  - Better cacheability for repeated style patterns.

The original `class_name` remains fully respected and is appended **after** the generated `dars-s-*` class, so user classes (and external CSS frameworks) retain override power.

### Central Style Registry in the HTML Head

The optimized styles are accumulated into a central registry and injected in the `<head>` as:

```html
<link rel="stylesheet" href="runtime_css.css" />
<style id="dars-style-registry">
  /* .dars-s-* rules here */
</style>
<link rel="stylesheet" href="styles.css" />
```

Order is carefully chosen so that:

- `runtime_css.css` provides the base UI tokens and default component styling.
- `#dars-style-registry` contains all extracted `.dars-s-*` rules (including those coming from `hover_style`/`active_style` phases on future releases).
- `styles.css` (hover/active styles + `app.add_global_style()` + user CSS files) comes last, ensuring user styles can override the framework-generated ones.

### Full Export Coverage: Single/Multi Page, SPA & SSR

The new style pipeline now runs consistently across all export modes:

- **Single page & multipage**:
  - `HTMLCSSJSExporter.export` collects static styles from the component tree before rendering.
  - The generated HTML includes the `#dars-style-registry` block in the head.

- **SPA export (`_export_spa`)**:
  - Each SPA route runs the same static-style collection before serializing its `html`.
  - The per-route config in `__DARS_SPA_CONFIG__` now includes a `styles` field containing the CSS for that route.
  - At runtime, the SPA router calls `_injectStyles(routeName, styles)` so that SSR/SPA navigations share the same optimized classes.

- **SSR backend (`dars.backend.ssr`)**:
  - `SSRRenderer.render_route` uses a **deep copy** of each route's root tree to avoid mutating the original components when collecting styles.
  - Static styles are extracted to `.dars-s-*` classes, and the resulting CSS is injected into the SSR HTML head using `#dars-style-registry`.
  - The SSR JSON API (`/api/ssr/<route>`) now returns a `styles` field alongside `html`, `vdom`, `events`, etc., so the SPA router can inject the same registry CSS on client-side navigations.

### Runtime & Router Adjustments

The embedded JS runtime (`dars/js_lib.py` → `DARS_MIN_JS`) has been updated to be style-optimization aware without breaking existing behavior:

- `Dars.change({ id, dynamic: true, style: {...} })` and state rules that manipulate `attrs.style` continue to write directly to `el.style[...]`.
  - They do **not** depend on an initial inline `style` attribute, so elements whose base styles were moved to `.dars-s-*` remain fully reactive.
- Class updates via `attrs.class` preserve internal `dars-*` classes (including `.dars-s-*`) and only replace user classes, ensuring the optimization never gets wiped by state changes.
- The SPA router:
  - Loads SSR route data from `/api/ssr/...` and now respects the `styles` payload from the backend.
  - Uses `_injectStyles(routeName, styles)` on every SSR navigation so that optimized classes stay active even after client-side route changes.

These changes are designed to be **backwards compatible** for projects that used only `style`/`class_name` and dynamic state. The main effect you will notice in v1.8.1 is smaller, cleaner HTML with fewer repeated inline styles, especially for static or Tailwind-like styling.

---

# Release Notes v1.8.0

> **Advanced Multimedia Components & Electron Security Baseline**

## Installation

```bash
pip install --upgrade dars-framework
```

## What's New

### New Advanced Multimedia Components: Video & Audio

v1.8.0 introduces two new first-class components in the basic library:

- `Video`: wrapper around `<video>`
- `Audio`: wrapper around `<audio>`

Both are **fully reactive** and integrate with the existing hooks system:

- `State` + `useDynamic` for:
  - `src`
  - `autoplay`
  - `muted`
  - `loop`
  - `controls`
  - `plays_inline` (Video)
- `useValue` for non-reactive initial values.
- `VRef` (setVRef/useVRef) can target `src` and other props when needed.

Example:

```python
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
```

#### Reactive Boolean Attributes

The web exporter has been extended so that `useDynamic` bindings on boolean attributes behave correctly:

- When a `State` value changes, the runtime:
  - Adds or removes the HTML attributes: `autoplay`, `muted`, `loop`, `controls`, `playsinline`.
  - Synchronizes the corresponding JS properties on the media element (`el.autoplay`, `el.muted`, etc.).
- Dynamic markers (from `useDynamic`) no longer count as _truthy_ defaults:
  - `controls=True`, `plays_inline=True` remain active by default.
  - `autoplay`, `loop`, `muted` are off by default unless explicitly set by state or by a literal `True`.

This ensures that Video/Audio behave predictably both on initial render and during reactive updates.

### Automatic media/ Directory Copy

The HTML/CSS/JS exporter now supports a **convention-based media folder**:

- If your project root contains a `media/` directory, Dars will:
  - Recursively copy `media/` into the export `output_path`.
  - Preserve subdirectory structure.
- Any `src="/media/..."` used in `Image`, `Video` or `Audio` will point to real files in the exported build.

This makes it straightforward to ship videos, audio tracks and posters alongside your static export.

### Electron 39.2.6 Security Baseline

To keep desktop builds secure and reproducible, v1.8.0 introduces an **Electron security baseline**:

- All desktop templates and Electron scaffolds now pin Electron to `39.2.6`:
  - `dars/templates/desktop/template/backend/package.json`
  - CLI `init` desktop scaffolds and `init --update` flows.
- `dars doctor` gains version-awareness:
  - New constant `MIN_SAFE_ELECTRON = "39.2.6"`.
  - When you run `dars doctor --all --yes`, Dars will install/update Electron globally via Bun as `electron@39.2.6` and `electron-builder@latest`.
- `dars dev` for desktop projects now warns if your installed Electron is below the baseline and suggests:

  ```bash
  dars doctor --all --yes
  ```

This keeps both templates and global tooling aligned with a reviewed Electron version.

### Desktop Dev Flow Fixes (Electron + rTimeCompile)

Several quality-of-life fixes improve desktop (Electron) development:

- `App.rTimeCompile` desktop branch:
  - Stops the "Starting preview..." spinner after Electron launches.
  - Exits the method immediately when desktop mode finishes, preventing the web preview server from starting on top of Electron dev.
- `dars core/js_bridge`:
  - `electron_dev_spawn` now sets `ELECTRON_DISABLE_SECURITY_WARNINGS=true` for dev runs.
  - This suppresses the noisy _Electron Security Warning (Insecure Content-Security-Policy)_ in dev tools without touching the CSP used by the Dars runtime.

Result: smoother desktop dev cycle with clear logs and no accidental web preview server when working on Electron apps.

### Documentation Updates

- `LandingPage/documentation/markdown/components.md` now documents:
  - `Video` and `Audio` components.
  - Reactive integration with `State`, `useDynamic`, `V()` and VRefs.
  - Recommended `media/` folder convention for assets.

---
