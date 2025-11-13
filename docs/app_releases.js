window.__DARS_VDOM__={type:"T1",id:"page_151",children:[{type:"T2",id:"container_152",children:[{type:"T3",id:"dars-navbar",children:[{type:"T2",id:"navbar-left",children:[{type:"T4",id:"image_153"},{type:"T5",id:"text_154",text:"Dars Framework"}]},{type:"T2",id:"container_155",children:[{type:"T2",id:"navbar-right",children:[{type:"T6",id:"link_156",text:"Home"},{type:"T6",id:"link_157",text:"Documentation"},{type:"T6",id:"link_158",text:"Releases"},{type:"T6",id:"link_159",text:"PlayGround"},{type:"T6",id:"link_160",text:"GitHub"}]},{type:"T2",id:"hamburger-menu",children:[{type:"T2",id:"hamburger-btn",children:[{type:"T2",id:"container_161",children:[{type:"T2",id:"container_162"},{type:"T2",id:"container_163"},{type:"T2",id:"container_164"}]}]},{type:"T2",id:"mobile-menu",children:[{type:"T6",id:"link_165",text:"Home"},{type:"T6",id:"link_166",text:"Documentation"},{type:"T6",id:"link_167",text:"Releases"},{type:"T6",id:"link_168",text:"PlayGround"},{type:"T6",id:"link_169",text:"GitHub"}]}]}]}]}]},{type:"T2",id:"container_170",children:[{type:"T2",id:"markdown-content-container",children:[{type:"T9",id:"markdown_171",text:`# Release Notes v1.3.4

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

In the github repository [Here](https://github.com/ZtaMDev/Dars-Framework/releases).`}]},{type:"T2",id:"footer-section",children:[{type:"T2",id:"container_172",children:[{type:"T2",id:"container_173",children:[{type:"T2",id:"container_174",children:[{type:"T4",id:"image_175"},{type:"T2",id:"container_176",children:[{type:"T5",id:"text_177",text:"Dars Framework"}]}]},{type:"T2",id:"container_178",children:[{type:"T2",id:"container_179",children:[{type:"T5",id:"text_180",text:"Quick Links"},{type:"T6",id:"link_181",text:"Documentation"},{type:"T6",id:"link_182",text:"GitHub"},{type:"T6",id:"link_183",text:"Examples"}]},{type:"T2",id:"container_184",children:[{type:"T5",id:"text_185",text:"Resources"},{type:"T6",id:"link_186",text:"Getting Started"},{type:"T6",id:"link_187",text:"Releases"}]},{type:"T2",id:"container_188",children:[{type:"T5",id:"text_189",text:"Info: "},{type:"T5",id:"text_190",text:"A modern Python framework for web and desktop applications"}]}]},{type:"T2",id:"container_191",children:[{type:"T2",id:"container_192",children:[{type:"T5",id:"text_193",text:"\xA9 2024 Dars Framework."}]},{type:"T2",id:"container_194",children:[{type:"T5",id:"text_195",text:"Created with "},{type:"T6",id:"link_196",text:"Dars Framework"},{type:"T5",id:"text_197",text:" by "},{type:"T6",id:"link_198",text:"ZtaDev"}]}]}]}]}]}]},{type:"T10",id:"documentation-sidebar"}]},function(){const d=new Map;let r=null,l=null;function c(){}function b(){}function g(e,n){if(!e)return;n(e);const t=e.children||[];for(let i=0;i<t.length;i++)g(t[i],n)}function k(e){try{if(typeof atob=="function")return atob(e);if(typeof Buffer<"u")return Buffer.from(e,"base64").toString("utf8")}catch{}return""}function S(e){try{if(!e)return null;if(e&&e.type==="inline"&&e.code)return new Function("event",e.code);const n=e&&(e.b||e.code_b64)||null;if(n){const t=k(n);if(t)return new Function("event",t)}}catch{}return null}function A(e){g(e,n=>{if(n&&n.id&&n.events&&!d.has(n.id)){const t={};for(const i in n.events){const o=n.events[i],u=S(o);u&&(t[i]=u)}Object.keys(t).length?d.set(n.id,t):d.delete(n.id)}})}function L(e,n){if(!(!e||!n))for(const[t,i]of Object.entries(n))try{i===!1||i===null||typeof i>"u"?e.removeAttribute(t):e.setAttribute(t,String(i))}catch{}}function E(e,n={},t={}){for(const i in n)if(!(i in t))try{e.removeAttribute(i)}catch{}for(const i in t){const o=t[i];try{o===!1||o===null||typeof o>"u"?e.removeAttribute(i):e.setAttribute(i,String(o))}catch{}}}function M(e,n={},t={}){for(const i in n)if(!(i in t))try{e.style.removeProperty(i.replace(/_/g,"-"))}catch{}for(const i in t){const o=t[i];try{e.style.setProperty(i.replace(/_/g,"-"),String(o))}catch{}}}function D(e,n){(n||document).addEventListener(e,function(t){let i=t.target;const o=n||document;for(;i&&i!==o;){const u=i.id;if(u&&d.has(u)){const p=d.get(u)[e];if(i&&i.__darsEv&&i.__darsEv[e])return;if(typeof p=="function"){try{p.call(i,t)}catch(a){console.error("[Dars] handler error",a)}return}}i=i.parentNode}},!0)}function x(e,n){return e&&n?e.type!==n.type:e!==n}function _(e){if(!e)return;const n=e.children||[];for(let t=0;t<n.length;t++)_(n[t]);if(e.id&&d.delete(e.id),e.id){const t=document.getElementById(e.id);if(t&&t.parentNode)try{t.parentNode.removeChild(t)}catch{}}}function v(e,n){if(!n||!n.id)return{ok:!1,reason:"missing-new"};let t=document.getElementById(n.id);if(!t){const a=e&&e.id?document.getElementById(e.id):null;if(a)try{a.id=n.id,t=a}catch{}}if(!t)return{ok:!1,reason:"missing-el"};if(x(e,n))return{ok:!1,reason:"type-changed"};const i=!!n.isIsland;if(!i&&n.class&&(t.className=n.class),i||E(t,e&&e.props||{},n.props||{}),i||M(t,e&&e.style||{},n.style||{}),!i&&Object.prototype.hasOwnProperty.call(n,"text")&&t.textContent!==String(n.text||"")&&(t.textContent=String(n.text||"")),i)return{ok:!0};const o=e&&e.children?e.children:[],u=n.children?n.children:[],f=new Map;for(let a=0;a<o.length;a++){const s=o[a]&&(o[a].id||o[a].key)||null;s&&f.set(String(s),o[a])}const p=new Set;for(let a=0;a<u.length;a++){const s=u[a],T=s&&(s.id||s.key)||null;if(!T)if(a<o.length){const m=v(o[a],s);if(!m.ok)return m;p.add(o[a]);continue}else return{ok:!1,reason:"children-added"};const w=f.get(String(T));if(w){const m=v(w,s);if(!m.ok)return m;p.add(w)}else{if(a<o.length){const h=o[a];if(!x(h,s)){const y=v(h,s);if(!y.ok)return y;p.add(h);continue}}const m=createSubtree(s);if(m){const h=a<o.length?o[a]:null;if(h&&h.id){const y=document.getElementById(h.id);y&&y.parentNode?y.parentNode.insertBefore(m,y):t.appendChild(m)}else t.appendChild(m);continue}return{ok:!1,reason:"children-added"}}}for(let a=0;a<o.length;a++){const s=o[a];p.has(s)||_(s)}return{ok:!0}}function C(e){typeof requestAnimationFrame=="function"?requestAnimationFrame(e):setTimeout(e,16)}function N(e){const n=r;if(!n){r=e;try{window.__DARS_VDOM__=e}catch{}return}C(()=>{const t=v(n,e);if(!t.ok){console.warn("[Dars] Structural change detected (",t.reason,"), reloading...");try{location.reload()}catch{}return}r=e;try{window.__DARS_VDOM__=e}catch{}})}function B(e){r=e;try{window.__DARS_VDOM__=e}catch{}["click","dblclick","mousedown","mouseup","mouseenter","mouseleave","mousemove","keydown","keyup","keypress","change","input","submit","focus","blur"].forEach(t=>D(t,document))}function I(){const e=window.__DARS_VERSION_URL||"version.txt";let n=null,t=!1;function i(u,f,p,a){try{const s=new XMLHttpRequest;a&&(s.responseType=a),s.open("GET",u,!0),s.timeout=5e3,s.onreadystatechange=function(){s.readyState===4&&(s.status>=200&&s.status<300?f(s.response):p())},s.onerror=p,s.ontimeout=p,s.setRequestHeader("Cache-Control","no-store"),s.send()}catch{p()}}function o(){i(e,function(u){let f=(u||"").toString().trim();if(f&&(t=!1),l||(l=f),f&&f!==l){l=f;try{location.reload()}catch{}return}n=setTimeout(o,600)},function(){t||(console.log("[Dars] waiting for version.txt"),t=!0),n=setTimeout(o,600)},"text")}return o(),()=>{n&&clearTimeout(n)}}document.addEventListener("DOMContentLoaded",function(){window.__DARS_VDOM__?B(window.__DARS_VDOM__):console.warn("[Dars] No VDOM snapshot found for hydration"),window.__DARS_VERSION_URL&&window.__DARS_SNAPSHOT_URL&&I()})}(),window.addEventListener("scroll",()=>{const d=document.getElementById("dars-navbar");window.scrollY>20?d.classList.add("scrolled"):d.classList.remove("scrolled");const r=document.getElementById("features-section");if(r&&!r.classList.contains("visible")){const l=r.getBoundingClientRect().top,c=window.innerHeight/1.5;l<c&&(r.classList.add("visible"),document.querySelectorAll('[id^="feature-card-"]').forEach((g,k)=>{setTimeout(()=>{g.style.opacity="1",g.style.transform="translateY(0)"},k*100)}))}}),document.addEventListener("DOMContentLoaded",()=>{const d=document.getElementById("hero-logo"),r=document.getElementById("hero-title"),l=document.getElementById("hero-description"),c=document.getElementById("pip-command"),b=document.getElementById("get-started-btn"),g=document.getElementById("scroll-text");d&&setTimeout(()=>d.classList.add("show"),5),r&&setTimeout(()=>r.classList.add("show"),350),l&&setTimeout(()=>l.classList.add("show"),650),c&&setTimeout(()=>c.classList.add("show"),950),b&&setTimeout(()=>b.classList.add("show"),1250),g&&setTimeout(()=>g.classList.add("show"),1500)});function R(){window.open("https://ztamdev.github.io/Dars-Framework/docs.html","_self")}function P(){navigator.clipboard.writeText("pip install dars framework").then(()=>{const r=document.querySelector("#copy-btn"),l=r.textContent;r.textContent="Copied!",r.style.background="linear-gradient(135deg, #38c49f 0%, #2a6b5b 100%) !important",setTimeout(()=>{r.textContent=l,r.style.background="linear-gradient(135deg, #1d4a3f 0%, #2a6b5b 100%) !important"},2e3)})}document.addEventListener("DOMContentLoaded",function(){const d=document.getElementById("hamburger-btn"),r=document.getElementById("mobile-menu"),l=document.body;d&&r&&(d.addEventListener("click",function(c){c.stopPropagation(),r.style.display==="flex"?(r.style.display="none",d.classList.remove("menu-open"),l.classList.remove("menu-open")):(r.style.display="flex",d.classList.add("menu-open"),l.classList.add("menu-open"))}),r.querySelectorAll("a").forEach(c=>{c.addEventListener("click",function(){r.style.display="none",d.classList.remove("menu-open"),l.classList.remove("menu-open")})}),document.addEventListener("click",function(c){!d.contains(c.target)&&!r.contains(c.target)&&(r.style.display="none",d.classList.remove("menu-open"),l.classList.remove("menu-open"))}),document.addEventListener("keydown",function(c){c.key==="Escape"&&r.style.display==="flex"&&(r.style.display="none",d.classList.remove("menu-open"),l.classList.remove("menu-open"))}))});
