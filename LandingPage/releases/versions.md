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