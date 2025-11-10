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