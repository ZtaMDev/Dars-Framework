# Release Notes v1.4.6

> **Major Feature Release**: Introduces Single Page Application (SPA) support and a powerful client-side routing system.

## Installation

```bash
pip install --upgrade dars-framework
```

or

```bash
pip install dars-framework==1.4.5
```

## What's New

### Single Page Application (SPA) Support

**New Routing System:**
- **Client-Side Routing**: Build fast, responsive SPAs with Python.
- **Nested Routes & Layouts**: Create complex UI hierarchies using the `parent` parameter and the new `Outlet` component.
- **Persistent Layouts**: Keep headers, sidebars, and navigation bars active while content changes dynamically.

**Robust Error Handling:**
- **Automatic 404 Handling**: Dars now automatically redirects invalid routes to a 404 page.
- **Default & Custom 404**: Includes a built-in clean 404 page, or define your own with `app.set_404_page()`.

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

```bash
pip install --upgrade dars-framework
```

or

```bash
pip install dars-framework==1.4.4
```

## What's Fixed

- **Style Merge Fix (CRITICAL)** - `Mod.set()` now correctly merges style properties
- **Removed `this().goto()`** - Non-functional feature removed; use `state.state()` instead
- **Fixed Syntax Warning** - Corrected invalid escape sequence in `js_lib.py`
- **Improved State 0 Restoration** - Event handlers now re-attach when returning to default state

---

# Release Notes v1.4.3 (DEPRECATED)

> State management enhancements with compile-time validation, component self-navigation, and critical style merge fix. Improves developer experience and fixes property replacement bug.

## Installation

```bash
pip install --upgrade dars-framework
```

or

```bash
pip install dars-framework==1.4.3
```

## What's New

- **`this().goto(idx)`** - Component self-navigation for state transitions
- **`this_for(id)`** - Compile-time validation helper for state navigation
- **Style Merge Fix** - Critical fix: `Mod.set()` now merges style properties instead of replacing them
- **Enhanced Documentation** - Guides for state management patterns

---

# Release Notes v1.4.2

> New utility dScript functions added to `utils_ds` for enhanced client-side interactions.

## Installation

```bash
pip install --upgrade dars-framework
```

or

```bash
pip install dars-framework==1.4.2
```

## What's New

### Utility Functions (`utils_ds`)

- `setTimeout(delay: int, code: dScript)`: Execute a dScript after a delay (ms).
- `setText(id: str, text: str)`: Set the text content of an element.
- `showModal(id: str)`, `hideModal(id: str)`: Modal visibility helpers.
- `goTo(href: str)`, `goToNew(href: str)`, `reload()`, `goBack()`, `goForward()`: Navigation utilities.
- `alert(message: str)`, `confirm(message: str, on_ok: str = "", on_cancel: str = "")`, `log(message: str)`: Alert & console utilities.
- `show(id: str)`, `hide(id: str)`, `toggle(id: str)`, `addClass(id: str, class_name: str)`, `removeClass(id: str, class_name: str)`, `toggleClass(id: str, class_name: str)`: DOM manipulation utilities.
- `scrollTo(x: int = 0, y: int = 0)`, `scrollToTop()`, `scrollToBottom()`, `scrollToElement(id: str)`: Scroll utilities.
- `submitForm(form_id: str)`, `resetForm(form_id: str)`, `getValue(input_id: str, target_id: str)`, `clearInput(input_id: str)`: Form utilities.
- `saveToLocal(key: str, value: str)`, `loadFromLocal(key: str, target_id: str)`, `removeFromLocal(key: str)`, `clearLocalStorage()`: Storage utilities.
- `copyToClipboard(text: str)`, `copyElementText(id: str)`: Clipboard utilities.
- `focus(id: str)`, `blur(id: str)`: Focus utilities.

These functions are documented in `https://ztamdev.github.io/Dars-Framework/docs.html#dars-script-system` and for states in `https://ztamdev.github.io/Dars-Framework/docs.html#state-management-in-dars-dstate-cstate-goto-mods`.

---

# Release Notes v1.4.1

> SEO and Apple device optimizations. Enhanced metadata generation with automatic MIME type detection for favicons and comprehensive iOS/Safari support.

## Installation

```bash
pip install --upgrade dars-framework
```

or

```bash
pip install dars-framework==1.4.1
```

## What's New

### Automatic Favicon MIME Type Detection

**Smart Icon Type Recognition:**
- Favicon links now automatically detect and use the correct MIME type based on file extension
- Supports PNG, ICO, SVG, JPG/JPEG, WebP, and GIF formats
- No manual type specification needed
- Eliminates incorrect `image/x-icon` type for PNG files

**Before (v1.4.0):**
```html
<link rel="icon" href="logo.png" type="image/x-icon">  <!-- Incorrect! -->
```

**After (v1.4.1):**
```html
<link rel="icon" href="logo.png" type="image/png">  <!-- Correct! -->
```

### Enhanced Apple Device Support

**New App Properties:**
- `apple_mobile_web_app_capable` - Enable fullscreen mode when added to home screen
- `apple_mobile_web_app_status_bar_style` - Control status bar appearance:
  - `"default"` - Standard iOS status bar
  - `"black"` - Black status bar
  - `"black-translucent"` - **Transparent status bar** (solves Safari iOS 16+ solid color issue)
- `apple_mobile_web_app_title` - Custom title for home screen icon

**Usage:**
```python
app = App(
    title="My App",
    favicon="logo.png",
    apple_touch_icon="logo.png",
    apple_mobile_web_app_capable=True,
    apple_mobile_web_app_status_bar_style="black-translucent",  # Enables transparency!
    apple_mobile_web_app_title="MyApp"
)
```

### Safari 15+ Theme Color Enhancements

**Adaptive Theme Colors:**
- Theme color now includes media query variants for light/dark mode
- Proper integration with iOS system appearance settings
- **Fixes Safari iOS 16+ transparency issues** where solid colors blocked background visibility

**Generated Meta Tags:**
```html
<meta name="theme-color" content="#0d1513">
<meta name="theme-color" media="(prefers-color-scheme: light)" content="#0d1513">
<meta name="theme-color" media="(prefers-color-scheme: dark)" content="#0d1513">
```

### Improved Apple Touch Icon

**Multiple Size Specifications:**
- Apple touch icon now includes size attribute for better iOS home screen quality
- Generates both standard and 180x180 sized icon links

**Generated Links:**
```html
<link rel="apple-touch-icon" href="logo.png">
<link rel="apple-touch-icon" sizes="180x180" href="logo.png">
```

### Modern Mobile Web App Meta Tag

**Standards Compliance:**
- Added `mobile-web-app-capable` meta tag alongside `apple-mobile-web-app-capable`
- Eliminates deprecation warnings in modern browsers
- Maintains backward compatibility with older iOS versions

**Generated Meta Tags:**
```html
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-capable" content="yes">
```

## Technical Improvements

### Exporter Enhancements (`dars/exporters/web/html_css_js.py`)

- **New `_detect_icon_mime_type()` Helper**: Automatically detects MIME types from file extensions
- **Enhanced `_generate_meta_tags()`**: Adds Apple-specific meta tags and theme-color variants
- **Updated `_generate_links()`**: Applies automatic MIME detection and sizes attribute

### App Class Updates (`dars/core/app.py`)

- Added 3 new initialization parameters for Apple mobile web app support
- Properties auto-initialize with sensible defaults (`apple_mobile_web_app_title` defaults to app title)
- All new properties are **optional** and **backward compatible**

## Migration Notes

### For Existing Projects

**Automatic Upgrade:**
- No configuration changes required
- Favicons automatically get correct MIME types
- Theme colors automatically include light/dark variants
- All new features are opt-in

**Optional iOS Enhancement:**
```python
# Add to your App initialization
app = App(
    # ... existing params ...
    apple_mobile_web_app_capable=True,
    apple_mobile_web_app_status_bar_style="black-translucent",
    apple_mobile_web_app_title="MyApp"
)
```

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

```bash
pip install --upgrade dars-framework
```

or

```bash
pip install dars-framework==1.4.0
```

## Notes:

All advanced and basic templates are now updated using the new features.

# Release Notes v1.3.9

> Desktop File System API, Pythonic Arg helper, keyboard event filtering, and comprehensive template synchronization. Major enhancements to desktop capabilities with improved developer experience.

## Installation

```bash
pip install --upgrade dars-framework
```

or

```bash
pip install dars-framework==1.3.9
```

## What's New

### Desktop File System API - `list_directory`

**Comprehensive Directory Listing:**
- New `list_directory()` function for browsing files and folders
- Optional glob pattern filtering (e.g., `"*.py"` for Python files only)
- Optional `include_size` parameter (default: False) to show/hide file sizes
- Full integration with `get_value()` for dynamic paths from inputs
- Seamless chaining with `dScript.then()` for UI updates
- Returns array of `{name, isDirectory, size?}` objects

**Usage:**
```python
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
        this().state(id="count", text=RawJS("`Found ${value.length} files`"))
    )
)

# Include file sizes
list_directory(".", "*", include_size=True)
```

### Pythonic `Arg` Helper

**Cleaner dScript.ARG Access:**
- New `Arg` singleton for Pythonic access to `dScript.ARG`
- More readable than `RawJS("dScript.ARG")`
- Provides helper methods like `.map()`, `.join()`, `.length`, etc.
- Auto-generates proper JavaScript code
- Exported in `dars.all` for easy access

**Usage:**
```python
from dars.scripts.dscript import Arg

# Old way (still works)
this().state(text=RawJS("dScript.ARG.map(f => f.name).join('\\n')"))

# New Pythonic way
this().state(text=Arg.map("f => f.name").join("\\n"))

# Properties
Arg.length  # -> "dScript.ARG.length"
Arg.value   # -> "dScript.ARG.value"

# Methods
Arg.map("f => f.name")  # -> "dScript.ARG.map(f => f.name)"
Arg.filter("x => x > 0")  # -> "dScript.ARG.filter(x => x > 0)"
```

### Enhanced Keyboard Event Filtering

**Specific Key Event Handlers:**
- New keyboard event constants for specific keys (e.g., `KEY_DOWN_ENTER`, `KEY_DOWN_ESCAPE`)
- Event type parsing with `.` delimiter for key filtering (e.g., `"keydown.Enter"`)
- Proper event delegation with key matching
- Works across all event attachment mechanisms
- Backward compatible with existing keyboard events

**New Event Constants:**
```python
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
```

### Configurable DevTools

**Electron DevTools Control:**
- New `devtools` parameter in `App` class (default: `True`)
- Respects `DARS_DEV` and `DARS_DEVTOOLS` environment variables
- DevTools only open when both conditions met: dev mode + devtools enabled
- Better control over development environment
- Applies to all Electron generation methods

**Usage:**
```python
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
```

### Dynamic Form Element Updates

**Fixed `change` Function:**
- Corrected dynamic text updates for form elements
- Uses `.value` for `Input`, `Textarea`, `Select`
- Uses `.textContent` for other elements (Text, Button, etc.)
- Ensures UI updates properly reflect state changes
- Fixed issue where form input values weren't updating

### Improved Event Delegation

**Keyboard Event Fix:**
- Fixed event delegation for key-filtered keyboard events
- Properly checks both base event name and filtered event name in eventMap
- Ensures `keydown.Enter` and similar events work correctly
- Maintains backward compatibility with non-filtered events

## Bug Fixes

- Fixed `change` function to use `.value` for form elements instead of `.textContent`
- Fixed event delegation to properly handle key-filtered keyboard events like `keydown.Enter`
- Fixed ElectronExporter default templates to include latest IPC handlers
- Fixed CLI template generation to include all current File System API functions

## Improved

- Enhanced developer experience with configurable DevTools
- Cleaner syntax with `Arg` helper for dScript.ARG access
- More powerful keyboard event handling with key-specific filtering

## Migration Guide

### From v1.3.8 to v1.3.9

No breaking changes. You can upgrade safely:

```bash
pip install --upgrade dars-framework
```

**Optional: Use new features**

1. **Use `list_directory` for file browsing:**
```python
from dars.desktop import list_directory, get_value

Button("Browse", 
    on_click=list_directory(get_value("dir")).then(...)
)
```

2. **Use `Arg` helper for cleaner code:**
```python
from dars.scripts.dscript import Arg

# Instead of RawJS("dScript.ARG.map(...)") 
text=Arg.map("x => x.name").join("\\n")
```

3. **Use specific keyboard events:**
```python
Input(
    on_keydown_enter=submit_action,
    on_keydown_escape=cancel_action
)
```

## Documentation

- Updated Desktop exporter documentation with File System API examples
- Added `Arg` helper documentation in scripts section
- Enhanced keyboard events documentation with key-specific examples

# Release Notes v1.3.8

> Dynamic state updates, improved event handling, and enhanced Electron dev experience. Introduces `this()` for event-time component updates, `RawJS` for JavaScript injection, and `dScript.then()` for async chaining.

## Installation

```bash
pip install --upgrade dars-framework
```

or

```bash
pip install dars-framework==1.3.8
```

## What's New

### Dynamic State Updates with `this()`

**Effortless Component Updates:**
- New `this()` helper for direct, event-time component updates without pre-registering states
- Update any component property: `text`, `html`, `style`, `attrs`, `classes`
- Works in both desktop and web exports
- Perfect for async operations and file I/O

**Usage:**
```python
from dars.core.state import this

# Button that updates itself
btn = Button("Click me", on_click=this().state(
    text="Clicked!",
    style={"color": "red"}
))

# Counter with Mod helpers
counter = Text("0", id="count")
inc_btn = Button("+1", on_click=this().state(text=Mod.inc("count")))
```

### Raw JavaScript Injection with `RawJS`

**Dynamic Value Passing:**
- New `RawJS` class for injecting raw JavaScript variables into state updates
- Essential for passing values from async operations
- Use `dScript.ARG` as a placeholder for chained script results

**Usage:**
```python
from dars.scripts.dscript import RawJS, dScript
from dars.desktop import read_text

# File content becomes button text
read_btn = Button("Load",
    on_click=read_text("data.txt").then(
        this().state(text=RawJS(dScript.ARG))
    )
)
```

### Script Chaining with `dScript.then()`

**Sequential Async Operations:**
- New `.then()` method for chaining `dScript` objects
- Pass results between scripts using `dScript.ARG` (resolves to `value`)
- Built-in error handling and logging for debugging
- Enables complex workflows like read → process → update → write

**Usage:**
```python
# Chain file operations
Button("Process",
    on_click=read_text("input.txt")
        .then(dScript(code="return value.toUpperCase()"))
        .then(write_text("output.txt", RawJS("value")))
        .then(this().state(text="Done!"))
)
```

### Event Handler Assignment Fix

**Fixed Critical Bug:**
- Event handlers can now be assigned via attribute assignment: `btn.on_click = handler`
- Previously only constructor assignment worked: `Button(on_click=handler)`
- Added `__setattr__` override to properly register events in all cases
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
- **Dynamic Updates**: New `change({dynamic: true, ...})` path in `dars/js_lib.py`
- **RawJS Support**: State methods now detect and preserve `RawJS` values
- **this() Proxy**: Clean API for self-referential component updates

### Script System Improvements
- **Chaining Infrastructure**: Robust async IIFE wrapping for sequential execution
- **Value Passing**: Standardized `value` variable for inter-script communication
- **Debug Logging**: Verbose console output for troubleshooting chains

### Component System Fixes
- **Event Collection**: `VDomBuilder` now correctly serializes all event handlers
- **Attribute Interception**: `__setattr__` catches `on_*` assignments
- **Backward Compatible**: All existing event patterns continue working

### Dev Mode Stability
- **Debounce**: 300ms consolidation window for file change events
- **State Management**: Proper `restart_triggered` flag handling
- **Process Cleanup**: Reliable Electron termination before restart

## Documentation Updates

**Comprehensive Coverage:**
- New `this()` section in README with quick examples
- Expanded `state_management.md` with complete file operations guide
- Enhanced `exporters.md` with desktop API examples and chaining patterns
- Updated `scripts.md` with `.then()` method documentation

## Migration Notes

### For Existing Projects

**Seamless Upgrade:**
- No breaking changes - all existing code remains compatible
- New features are opt-in and additive
- Event handlers work with both constructor and attribute assignment

## Desktop Exporter Status

**Still in BETA:**
- File operations (`read_text`, `write_text`, `read_file`, `write_file`) are stable
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

> Compile-time and runtime component manipulation. Introduces `app.create()` / `app.delete()` for pre-export tree editing, and `createComp()` / `deleteComp()` for dynamic DOM operations with safe event hydration.

## Installation

```bash
pip install --upgrade dars-framework
```

or

```bash
pip install dars-framework==1.3.6
```

## What's New

### Compile-Time Component Manipulation

- `app.create(target, root=None, on_top_of=None, on_bottom_of=None)`
  - Inserts components before/after a reference child or at the end of the `root`.
  - Accepts `target` as an instance, a callable, or a `str` (id to move an existing component).
  - Multipage support: `root` can be a component id, a component instance, or a page name.
- `app.delete(id)`
  - Removes a component by id from the tree before export (no-op if not found).

### Runtime Component Manipulation

- `createComp(target, root, position='append')`
  - Generates a `dScript` that calls `Dars.runtime.createComponent(root_id, vdom_data, position)`.
  - Serializes the Python component to VDOM and rehydrates events for the subtree.
  - Positions: `append`, `prepend`, `before:<id>`, `after:<id>`.
- `deleteComp(id)`
  - Generates `dScript` that calls `Dars.runtime.deleteComponent(id)`.

### Event Hydration for Dynamic Content

- Event rehydration for the newly created subtree (supports arrays of handlers).
- Every dynamic node with an `id` also gets `class="dars-id-<id>"` for reliable selection when multiple instances exist.

### Barrel Import

- `from dars.all import *` now includes `createComp` and `deleteComp` from `dars.backend`.


# Release Notes v1.3.5

> Enhanced styling and development experience update featuring active styles, improved preview system, and advanced file monitoring. Delivers better visual feedback and faster development workflow.

## Installation

```bash
pip install --upgrade dars-framework
```

or

```bash
pip install dars-framework==1.3.5
```

## What's New

### Active Styles Support

**Complete Component Styling System:**
- New `active_style` attribute for all components, providing visual feedback during user interaction
- Completes the styling triad: `style`, `hover_style`, and `active_style`
- Works seamlessly with existing hover styles introduced in v1.3.4

**Usage:**
```python
Button("Click it",
        id="btn1",
        on_click=[dScript('console.log(`HI`)'), txtstate.state(1)],
        style={"color": "green"},
        hover_style={"color": "red"},      # from v1.3.4
        active_style={"color": "purple"},  # new in v1.3.5
)
```

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

```bash
pip install --upgrade dars-framework
```

or

```bash
pip install dars-framework==1.3.4
```

## What's New

### Hover Styles Support

**Enhanced Component Interactivity:**
- New `hover_style` attribute for all components, allowing dynamic styling on mouse hover
- Styles are automatically generated with higher specificity to ensure proper application

### Multi-Handler Event System

**Flexible Event Management:**
- Components now support arrays of event handlers for the same event type
- Multiple `dScript`, inline JavaScript, or mixed handlers can be assigned to single events
- Handlers execute in sequence with individual error handling
- Full backward compatibility with existing single-handler syntax

### Runtime Versioning

**Enhanced Debugging & Tracking:**
- JavaScript runtime now includes version information accessible via `Dars.version`
- Release URL exposed through `Dars.releaseUrl` for quick reference
- Better debugging and environment identification
- Framework version tracking in deployed applications

**Usage:**
```javascript
// Access version information
console.log(`Using Dars v${Dars.version}`);
console.log(`Release: ${Dars.releaseUrl}`);
```

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

```bash
pip install --upgrade dars-framework
```

or

```bash
pip install dars-framework==1.3.3
```

## What's New

### Section Component

**Semantic HTML Container:**
- New `Section` component that renders as `<section></section>` instead of generic `<div>`
- Maintains all functionality of Container component (children, styles, etc.)
- Improves HTML readability and semantic structure for debugging
- Better accessibility and SEO through proper sectioning elements

**Usage:**
```python
# Creates <section> with all container capabilities
Section(Button("HI"), styles={...})
```

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
```python
# Old way (still works)
Container(children=[...])

# New semantic way
Section(children=[...])
```

## Desktop Exporter Status

**Still in BETA** - No changes from v1.3.2

## Known Issues

- None introduced in this release
- Continuing to monitor Electron desktop exporter stability

---

# Release Notes v1.3.2

> Major minification improvements with combined JS files and optimized event handling. Electron desktop exporter remains in beta.

## Installation

```bash
pip install --upgrade dars-framework
```

or

```bash
pip install dars-framework==1.3.2
```

## Highlights

### Enhanced Minification System

**Combined JavaScript Bundles:**
- When `viteMinify: true` and `bundle: true` are enabled, the exporter now combines all JavaScript files into single optimized bundles
- Single-page apps: All JS combined into `app.js`
- Multi-page apps: Each page gets its own `app_{slug}.js` bundle
- Eliminates reference issues between separate files during minification

**Optimized Event Handling:**
- Events are no longer stored in VDOM tree
- Event handlers are now generated as valid JavaScript directly in runtime
- Improved compatibility with Vite minification and obfuscation
- Better performance and smaller bundle sizes

**Smart File Management:**
- When using combined bundles, individual files (`runtime_dars.js`, `script.js`, `vdom_tree.js`) are not generated
- HTML files are updated to reference only the combined bundle
- Backward compatible - falls back to separate files when `viteMinify: false`

### Vite Minification Perfection

- Vite can now minify the entire application as a single cohesive unit
- Resolves function reference issues that previously broke minification
- Proper obfuscation of all JavaScript code, including event handlers
- Maintains full functionality while significantly reducing bundle size

### Configuration-Driven Behavior

```json
{
  "viteMinify": true,
  "bundle": true,
  "defaultMinify": true
}
```

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
- Basic file system operations (`read_text`, `write_text`)
- Development mode with hot reload
- Production packaging still experimental

## Migration Notes

### For Existing Projects

**No breaking changes** - existing configurations continue to work. To benefit from the new minification:

1. Update your `dars.config.json`:
```json
{
  "viteMinify": true,
  "bundle": true
}
```

2. Run `dars build` or `dars export` as usual

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

```bash
pip install --upgrade dars-framework
```

or

```bash
pip install dars-framework==1.3.1
```

## Highlights

### Native Functions

You can acces native functions via `dars.desktop` module:

```python
from dars.desktop import *
```

With this module you can acces for now 2 main functions:

```python 
write_text("./app/lib/hello.txt", "Hello Text")
```
and

```python
read_text("./app/lib/hello.txt")
```

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

```bash
pip install --upgrade dars-framework
```

or

```bash
pip install dars-framework==1.3.0
```

## Highlights

- **New: Native Desktop Export (BETA)**
  - Build desktop apps directly from Dars projects.
  - Project config supports `format: "desktop"` and `targetPlatform` (`auto|windows|linux|macos`).
  - Backend scaffold via `dars init --type desktop` (or `--update`), generating minimal main process files and preload bridge.
  - IPC bridge includes basic FS read/write for quick experiments.
  - Source emitted to `dist/source-electron/`; packaged artifacts in `dist/`.
  - Note: This capability is BETA and not recommended for production yet.

- **New: Desktop Build Flow in CLI**
  - `dars build` respects `format: "desktop"` in `dars.config.json`.
  - Platform flags are selected automatically or via `targetPlatform`.
  - Robust error output: full stdout/stderr on packaging failure.

- **New: Doctor Integration for Desktop Tooling**
  - `dars doctor --all --yes` checks and installs optional desktop tooling.
  - Pins the desktop runtime to a compatible version automatically when needed.

- **Packaging Reliability Improvements**
  - Project metadata auto-filled from `App` (name/title, description, author, version) with sensible defaults.
  - Version defaulted to `0.1.0` when absent (warning emitted).
  - Package manager forced to a stable toolchain to avoid ENOENT errors during packaging.
  - Runtime version pinned explicitly in both dev deps and build config to ensure predictable builds.

## Quickstart (Desktop BETA)

```bash
# Initialize or update a project with desktop scaffolding
dars init --type desktop
# or
dars init --update

# Verify optional tooling
dars doctor --all --yes

# Build using project config (format: "desktop")
dars build
```

Minimal `dars.config.json` for desktop:

```json
{
  "entry": "main.py",
  "format": "desktop",
  "outdir": "dist",
  "targetPlatform": "auto"
}
```

## Bug Fixes

- Fixed packaging failures caused by missing metadata in project manifests by auto-populating:
  - `description` from `App.description` (fallback to a default)
  - `author` from `App.author` (fallback to a default)
  - `version` from `App.version` (fallback `0.1.0` with warning)
- Stabilized packaging by pinning desktop runtime version in both dev dependencies and build configuration.
- Avoided package-manager ENOENT errors in packaging by forcing a stable manager and resolving runners reliably on Windows.
- Correct platform flags for packaging: `--win`, `--linux`, `--mac`.
- Improved error reporting to include stdout and stderr from the packaging tool.

## Notes

- This feature set is **BETA**. Many options (signing, advanced IPC, updates, and deeper configuration) are still evolving.
- Usable for internal tools and early testing. Not recommended for production deployment yet.
- Expect changes to configuration keys and defaults in future versions.

I spent ~1 month iterating on this capability and consolidated changes into this single BETA release once it reached a usable threshold. Feedback is welcome to help stabilize and expand the desktop feature set.

# Release Notes v1.2.9

> Optional default minification, precise CLI control, faster builds, and clearer minification status.

## Installation

```bash
pip install --upgrade dars-framework
```

or

```bash
pip install dars-framework==1.2.8
```

## Highlights

- **New: Configurable Default Minifier**
  - `defaultMinify` (default: true) controls the built‑in Python minifier.
  - Preserves `pre`, `code`, `textarea`, `script`, `style`.
  - Only removes non‑conditional HTML comments and collapses spaces between tags.
  - Does not collapse text-node spaces (Markdown and `<pre><code>` remain intact).

- **New: CLI Flag `--no-minify`**
  - Available in `dars build` and `dars export`.
  - Disables only the default Python minifier for that run.
  - Independent from `viteMinify`.

- **Minification Modes Work Together**
  - When `defaultMinify` and `viteMinify` are both true:
    - Default minifier applies (safe HTML and fallback for JS/CSS).
    - Vite/esbuild minify JS/CSS where available.
  - Status line now reflects the active mode:
    - “Applying minification (default)”
    - “Applying minification (vite)”
    - “Applying minification (default + vite)”

- **Faster Default Minifier**
  - Default minifier uses fast Python fallback (rjsmin/rcssmin/regex) and never shells out to Vite/esbuild.
  - Results in near‑instant minification step.

## Bug Fixes

- Default minifier no longer ignores config; `defaultMinify` and `--no-minify` are strictly honored.
- Eliminated unintended use of esbuild/Vite inside the default minifier.
- Improved label accuracy to match the actual minification pipeline (default, vite, or both).

## Notes

- Relevant configuration:
  - `defaultMinify`: true/false. Controls the Python-side minification (HTML + JS/CSS fallback).
  - `viteMinify`: true/false. Controls Vite/esbuild for JS/CSS when available.
- Backward compatibility:
  - Defaults maintain previous behavior, now safer for Markdown/code blocks.
  - You can disable default minification per-run with `--no-minify` without affecting `viteMinify`.

Upgrade Recommendation: Recommended for all users; especially helpful for projects with Markdown/code samples and those wanting faster, more controllable minification.

# Older release notes can be found

In the github repository [Here](https://github.com/ZtaMDev/Dars-Framework/releases).
