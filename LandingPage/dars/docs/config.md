# dars.config.json

This file controls how Dars exports and builds your project.
It is created or updated by `dars init` and `dars init --update`.

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
  Python entry file used by `dars build` and optionally by `dars export config`.

- format
  Export format (currently `html`).

- outdir
  Destination directory for exported files.

- publicDir
  Directory copied as-is into the output (useful for assets). If `null`, Dars will try to autodetect common locations like `public/` or `assets/`.

- include / exclude
  Basic filters (by substring) applied when copying from `publicDir`.

- bundle
  Reserved for future use. Current exporters already perform the necessary bundling.

- viteMinify
  Toggle the advanced JS minifier. When `true` (default), the build prefers an advanced minifier. When `false`, it uses the secondary minifier. If none are available, Dars falls back to a conservative built-in minification.

## Tips

- You can update or add this config to an existing project at any time with:
  ```bash
  dars init --update
  ```
- To see optional tooling that can enhance bundling/minification, run:
  ```bash
  dars doctor
  ```
