# Dars Project Configuration (dars.config.json)

This file configures how Dars exports and builds your project. It is created by `dars init <name>` for new projects and can be merged/updated in existing projects with `dars init --update`.

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
  "viteMinify": true
}
```

## Fields

- entry
  Python entry file for your app. Used by `dars build` and by `dars export config`.

- format
  Export format. Currently only `html` is supported.

- outdir
  Directory where the exported files are written.

- publicDir
  Directory whose contents are copied as-is into the output (e.g. `public/` or `assets/`). If `null`, Dars will try to autodetect common locations.

- include / exclude
  Simple filters (by substring) applied when copying from `publicDir`.

- bundle
  Reserved for future use. Current exporters already produce a bundled output.

- viteMinify
  Toggle the advanced JS minifier.
  - `true` (default): prefer the advanced minifier; fall back to the secondary minifier; if neither is available, a conservative built-in fallback is used.
  - `false`: skip the advanced minifier and use the secondary minifier directly; fall back to the conservative built-in if not available.

## Behavior and defaults

- `dars init --update` merges your existing config with Dars defaults and writes the result back, adding any new keys (like `viteMinify`) without removing your current settings.
- During `dars export` and `dars build`, Dars reads this file and configures the minification pipeline accordingly.
- If advanced minifiers are not available, builds still complete with a conservative fallback. On `dars build`, a small notice may appear indicating that a less powerful minifier was used.

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
