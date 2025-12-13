# Dars Project Configuration

The file (dars.config.json) configures how Dars exports and builds your project. It is created by `dars init <name>` for new projects and can be merged/updated in existing projects with `dars init --update`.

## Example

```json
{
  "entry": "main.py",
  "format": "html",
  "outdir": "dist",
  "publicDir": null,
  "include": [],
  "exclude": ["**/__pycache__", ".git", ".venv", "node_modules"],
  "bundle": false,
  "defaultMinify": true,
  "viteMinify": true,
  "markdownHighlight": true,
  "markdownHighlightTheme": "auto",
  "utility_styles": {},
  "backendEntry": "backend.api:app"
}
```

## Fields

- entry
  Python entry file for your app. Used by `dars build` and by `dars export config`.

- format
  Export format. Supported: `html` and `desktop` (BETA). When set to `desktop`, the build command will produce native desktop artifacts.

- outdir
  Directory where the exported files are written.

- publicDir
  Directory whose contents are copied as-is into the output (e.g. `public/` or `assets/`). If `null`, Dars will try to autodetect common locations.

- include / exclude
  Simple filters (by substring) applied when copying from `publicDir`.

- bundle
  Reserved for future use. Current exporters already produce a bundled output.

- defaultMinify
  Toggle the built-in Python minifier (safe and conservative). Controls HTML minification and provides JS/CSS fallback when advanced tools are unavailable.
  - `true` (default): run the default Python-side minifier.
  - `false`: skip the default minifier. You can still use Vite/esbuild via `viteMinify`.

- viteMinify
  Toggle the advanced JS minifier.
  - `true` (default): prefer the advanced minifier; fall back to the secondary minifier; if neither is available, a conservative built-in fallback is used.
  - `false`: skip the advanced minifier and use the secondary minifier directly; fall back to the conservative built-in if not available.

- utility_styles
  Dictionary defining custom utility classes. Keys are class names, values are lists of utility strings or raw CSS properties.
  Example: `"btn-primary": ["bg-blue-500", "text-white"]`

- markdownHighlight
  Auto-inject a client-side syntax highlighter for fenced code blocks in Markdown.
  - `true` (default): injects Prism.js assets once per page and highlights `pre code` blocks.
  - `false`: no assets injected; you can include your own highlighter or none at all.

- backendEntry
  Python import path for your FastAPI/SSR backend application (e.g. `"backend.api:app"`).
  - Used by tools like `dars dev --backend` to start the backend server.
  - When your app defines routes with `RouteType.SSR`, `dars config validate` will require this field to be present.

## Desktop-specific (BETA)

- targetPlatform
  Desktop build target. Only effective when `format` is `desktop`.
  - Values: `auto` (default), `windows`, `linux`, `macos`.
  - Note: macOS targets must be built on macOS for signing.

> Desktop export is BETA: suitable for testing, not recommended for production yet. Configuration keys and defaults may change.

## Behavior and defaults

- `dars init --update` merges your existing config with Dars defaults and writes the result back, adding any new keys (like `defaultMinify`, `viteMinify`) without removing your current settings.
- During `dars export` and `dars build`, Dars reads this file and configures the minification pipeline accordingly.
- If advanced minifiers are not available, builds still complete with a conservative fallback. On `dars build`, a small notice may appear indicating that a less powerful minifier was used.
- You can force-skip the default Python minifier per run with `--no-minify` (does not affect `viteMinify`).

## Tips

- To add or refresh the config in an existing project:
  ```bash
  dars init --update
  ```
- To review optional tooling that can enhance bundling/minification, run:
  ```bash
  dars doctor
  ```
- If you want to force using only the secondary minifier, set `"viteMinify": false`.
 - To disable the default minifier by config, set `"defaultMinify": false`; to disable it per-run use `--no-minify`.
