# Dars Project Configuration

The `dars.config.json` file is the central nervous system of your Dars project. It defines how your application is compiled, optimized, and prepared for deployment.

---

## Configuration Overview

A standard configuration file looks like this:

```json
{
  "entry": "main.py",
  "format": "html",
  "outdir": "dist",
  "publicDir": "public",
  "include": [],
  "exclude": ["**/__pycache__", ".git", ".venv", "node_modules"],
  "bundle": true,
  "minify": true,
  "markdownHighlight": true,
  "markdownHighlightTheme": "auto",
  "port": 8000,
  "utility_styles": {},
  "backendEntry": "backend.api:app"
}
```

---

## Core Fields

### 1. Build & Path Configuration
- **`entry`** (string): The Python entry point of your application. Defaults to `main.py`.
- **`format`** (string): Target deployment format. 
  - `html`: Standard web application (SPA/MPA/SSR).
  - `desktop`: Native desktop application (Electron-based, BETA).
- **`outdir`** (string): The directory where compiled assets will be saved. Defaults to `dist`. This directory is also the default path used by `dars preview`.
- **`publicDir`** (string): Directory for static assets (images, fonts, etc.) that will be copied directly to the output.

### 2. File Filtering
- **`include`** (list): List of glob patterns or substrings to include from the public directory.
- **`exclude`** (list): List of patterns to ignore during the build process.

### 3. Optimization & Minification
Dars now uses **dars-bundler** — a standalone, high-performance Rust binary — as its sole minification engine. It replaces the previous Python-based rjsmin/rcssmin pipeline and the optional Vite/esbuild dependency.

- **`minify`** (boolean, default `true`): Enables or disables JS and CSS minification via `dars-bundler`. When enabled, the bundler runs **SWC** (Rust) for AST-level JS minification with dead-code elimination, and **LightningCSS** for CSS minification. **No Node.js, npm, or Vite installation is required.**
- **`bundle`** (boolean): Ensures all internal dependencies are bundled into the final distribution.

> **Note:** The old `viteMinify` and `defaultMinify` keys are still accepted for backwards compatibility but are ignored — `minify` is the single control point.

### 4. Features & Integrations
- **`markdownHighlight`** (boolean): Automatically injects Prism.js for syntax highlighting in Markdown components.
- **`backendEntry`** (string): Import path for your FastAPI backend (e.g., `"backend.api:app"`). Required for SSR projects.
- **`port`** (number): The port for the development preview server. Defaults to `8000`. This port is respected by both `dars dev` and `dars preview`.

---

## The dars-bundler

`dars-bundler` is a standalone Rust binary that Dars ships alongside its runtime. It is automatically detected and invoked during `dars build` / `dars export` — **no manual configuration is needed**.

### How it works
1. After Dars generates your HTML/CSS/JS output, `dars-bundler` is called on the output directory.
2. It walks all JS files and runs **SWC minification** (variable renaming, dead-code elimination, constant folding).
3. It walks all CSS files and runs **LightningCSS minification** (vendor-prefix removal, color optimization, unused selector pruning).
4. Files in `lib/` (the Dars runtime: `dars.min.js`, `dap.js`, etc.) are processed with the same pipeline.
5. HTML files are **not touched** by dars-bundler; they are already optimized by BeautifulSoup during export.

### Discovery order
The bundler is resolved in this order:
1. `DARS_BUNDLER_PATH` env variable (user override)
2. Same directory as the Python executable
3. System `PATH`
4. `dars/bundler/` subdirectory shipped with the framework
5. DarsBundler dev repo `target/debug` or `target/release` (development mode)

### Disabling minification
Set `"minify": false` in `dars.config.json` **or** pass `--no-minify` to the CLI:
```bash
dars build --no-minify
dars export --no-minify
```

---

## Custom Utility Styles

One of Dars' most powerful features is the ability to define custom utility classes directly in the configuration. This allows you to create reusable design tokens.

```json
{
  "utility_styles": {
    "btn-primary": [
      "bg-blue-600",
      "text-white",
      "px-4",
      "py-2",
      "rounded-lg",
      "hover:bg-blue-700",
      "transition-all"
    ],
    "card-glass": [
      "bg-white/30",
      "backdrop-blur-md",
      "border",
      "border-white/20",
      "rounded-2xl",
      "shadow-xl"
    ]
  }
}
```

Usage in Python:
```python
Button("Click Me", style="btn-primary")
Container(style="card-glass")
```

---

## Deployment Targets

### Web (HTML)
The standard format for deploying to the web. When `format` is `html`, Dars generates optimized HTML, CSS, and JS files compatible with any static host or FastAPI server.

### Desktop (BETA)
When `format` is `desktop`, Dars produces native desktop artifacts.
- **`targetPlatform`** (string): Specifies the target OS (`auto`, `windows`, `linux`, `macos`).

---

## Best Practices

1. **Keep it minimal**: Only include necessary files in your `publicDir` to speed up build times.
2. **Environment Variables**: Use the `dars env` system to manage different configurations for development and production.
3. **Validate often**: Use `dars config validate` to ensure your configuration matches the requirements of your chosen route types (especially for SSR).
