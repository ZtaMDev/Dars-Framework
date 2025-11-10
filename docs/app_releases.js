window.__DARS_VDOM__={type:"T1",id:"page_152",children:[{type:"T2",id:"container_153",children:[{type:"T3",id:"dars-navbar",children:[{type:"T2",id:"navbar-left",children:[{type:"T4",id:"image_154"},{type:"T5",id:"text_155",text:"Dars Framework"}]},{type:"T2",id:"container_156",children:[{type:"T2",id:"navbar-right",children:[{type:"T6",id:"link_157",text:"Home"},{type:"T6",id:"link_158",text:"Documentation"},{type:"T6",id:"link_159",text:"Releases"},{type:"T6",id:"link_160",text:"PlayGround"},{type:"T6",id:"link_161",text:"GitHub"}]},{type:"T2",id:"hamburger-menu",children:[{type:"T2",id:"hamburger-btn",children:[{type:"T2",id:"container_162",children:[{type:"T2",id:"container_163"},{type:"T2",id:"container_164"},{type:"T2",id:"container_165"}]}]},{type:"T2",id:"mobile-menu",children:[{type:"T6",id:"link_166",text:"Home"},{type:"T6",id:"link_167",text:"Documentation"},{type:"T6",id:"link_168",text:"Releases"},{type:"T6",id:"link_169",text:"PlayGround"},{type:"T6",id:"link_170",text:"GitHub"}]}]}]}]}]},{type:"T2",id:"container_171",children:[{type:"T2",id:"markdown-content-container",children:[{type:"T9",id:"markdown_172",text:`# Release Notes v1.3.1 BETA

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

In the github repository [Here](https://github.com/ZtaMDev/Dars-Framework/releases).`}]},{type:"T2",id:"footer-section",children:[{type:"T2",id:"container_173",children:[{type:"T2",id:"container_174",children:[{type:"T2",id:"container_175",children:[{type:"T4",id:"image_176"},{type:"T2",id:"container_177",children:[{type:"T5",id:"text_178",text:"Dars Framework"}]}]},{type:"T2",id:"container_179",children:[{type:"T2",id:"container_180",children:[{type:"T5",id:"text_181",text:"Quick Links"},{type:"T6",id:"link_182",text:"Documentation"},{type:"T6",id:"link_183",text:"GitHub"},{type:"T6",id:"link_184",text:"Examples"}]},{type:"T2",id:"container_185",children:[{type:"T5",id:"text_186",text:"Resources"},{type:"T6",id:"link_187",text:"Getting Started"},{type:"T6",id:"link_188",text:"Releases"}]},{type:"T2",id:"container_189",children:[{type:"T5",id:"text_190",text:"Info: "},{type:"T5",id:"text_191",text:"A modern Python framework for web and desktop applications"}]}]},{type:"T2",id:"container_192",children:[{type:"T2",id:"container_193",children:[{type:"T5",id:"text_194",text:"\xA9 2024 Dars Framework."}]},{type:"T2",id:"container_195",children:[{type:"T5",id:"text_196",text:"Created with "},{type:"T6",id:"link_197",text:"Dars Framework"},{type:"T5",id:"text_198",text:" by "},{type:"T6",id:"link_199",text:"ZtaDev"}]}]}]}]}]}]},{type:"T10",id:"documentation-sidebar"}]},function(){const d=new Map;let a=null,l=null;function c(){}const b={Text:{create(e){if(!e||e.isIsland)return null;const t=document.createElement("span");if(e.id&&(t.id=e.id),e.class&&(t.className=e.class),e.style)for(const n in e.style)try{t.style.setProperty(n.replace(/_/g,"-"),String(e.style[n]))}catch{}if(Object.prototype.hasOwnProperty.call(e,"text")&&(t.textContent=String(e.text||"")),e.props)for(const n in e.props){const i=e.props[n];try{i===!1||i===null||typeof i>"u"?t.removeAttribute(n):t.setAttribute(n,String(i))}catch{}}return t}},Container:{create(e){if(!e||e.isIsland)return null;const t=document.createElement("div");e.id&&(t.id=e.id);const n="dars-container";if(t.className=e.class?n+" "+e.class:n,e.style)for(const i in e.style)try{t.style.setProperty(i.replace(/_/g,"-"),String(e.style[i]))}catch{}if(e.props)for(const i in e.props){const o=e.props[i];try{o===!1||o===null||typeof o>"u"?t.removeAttribute(i):t.setAttribute(i,String(o))}catch{}}return t}}};function y(e,t){if(!e)return;t(e);const n=e.children||[];for(let i=0;i<n.length;i++)y(n[i],t)}function _(e){try{if(typeof atob=="function")return atob(e);if(typeof Buffer<"u")return Buffer.from(e,"base64").toString("utf8")}catch{}return""}function E(e){try{if(!e)return null;if(e&&e.type==="inline"&&e.code)return new Function("event",e.code);const t=e&&(e.b||e.code_b64)||null;if(t){const n=_(t);if(n)return new Function("event",n)}}catch{}return null}function B(e){y(e,t=>{if(t&&t.id&&t.events&&!d.has(t.id)){const n={};for(const i in t.events){const o=t.events[i],u=E(o);u&&(n[i]=u)}Object.keys(n).length?d.set(t.id,n):d.delete(t.id)}})}function M(e,t){if(!(!e||!t))for(const[n,i]of Object.entries(t))try{i===!1||i===null||typeof i>"u"?e.removeAttribute(n):e.setAttribute(n,String(i))}catch{}}function S(e,t={},n={}){for(const i in t)if(!(i in n))try{e.removeAttribute(i)}catch{}for(const i in n){const o=n[i];try{o===!1||o===null||typeof o>"u"?e.removeAttribute(i):e.setAttribute(i,String(o))}catch{}}}function D(e,t={},n={}){for(const i in t)if(!(i in n))try{e.style.removeProperty(i.replace(/_/g,"-"))}catch{}for(const i in n){const o=n[i];try{e.style.setProperty(i.replace(/_/g,"-"),String(o))}catch{}}}function A(e,t){(t||document).addEventListener(e,function(n){let i=n.target;const o=t||document;for(;i&&i!==o;){const u=i.id;if(u&&d.has(u)){const f=d.get(u)[e];if(i&&i.__darsEv&&i.__darsEv[e])return;if(typeof f=="function"){try{f.call(i,n)}catch(r){console.error("[Dars] handler error",r)}return}}i=i.parentNode}},!0)}function w(e,t){return e&&t?e.type!==t.type:e!==t}function x(e){if(!e)return;const t=e.children||[];for(let n=0;n<t.length;n++)x(t[n]);if(e.id&&d.delete(e.id),e.id){const n=document.getElementById(e.id);if(n&&n.parentNode)try{n.parentNode.removeChild(n)}catch{}}}function k(e,t){if(!t||!t.id)return{ok:!1,reason:"missing-new"};let n=document.getElementById(t.id);if(!n){const r=e&&e.id?document.getElementById(e.id):null;if(r)try{r.id=t.id,n=r}catch{}}if(!n)return{ok:!1,reason:"missing-el"};if(w(e,t))return{ok:!1,reason:"type-changed"};const i=!!t.isIsland;if(!i&&t.class&&(n.className=t.class),i||S(n,e&&e.props||{},t.props||{}),i||D(n,e&&e.style||{},t.style||{}),!i&&Object.prototype.hasOwnProperty.call(t,"text")&&n.textContent!==String(t.text||"")&&(n.textContent=String(t.text||"")),i)return{ok:!0};const o=e&&e.children?e.children:[],u=t.children?t.children:[],p=new Map;for(let r=0;r<o.length;r++){const s=o[r]&&(o[r].id||o[r].key)||null;s&&p.set(String(s),o[r])}const f=new Set;for(let r=0;r<u.length;r++){const s=u[r],v=s&&(s.id||s.key)||null;if(!v)if(r<o.length){const m=k(o[r],s);if(!m.ok)return m;f.add(o[r]);continue}else return{ok:!1,reason:"children-added"};const T=p.get(String(v));if(T){const m=k(T,s);if(!m.ok)return m;f.add(T)}else{if(r<o.length){const h=o[r];if(!w(h,s)){const g=k(h,s);if(!g.ok)return g;f.add(h);continue}}const m=createSubtree(s);if(m){const h=r<o.length?o[r]:null;if(h&&h.id){const g=document.getElementById(h.id);g&&g.parentNode?g.parentNode.insertBefore(m,g):n.appendChild(m)}else n.appendChild(m);continue}return{ok:!1,reason:"children-added"}}}for(let r=0;r<o.length;r++){const s=o[r];f.has(s)||x(s)}return{ok:!0}}function C(e){typeof requestAnimationFrame=="function"?requestAnimationFrame(e):setTimeout(e,16)}function N(e){const t=a;if(!t){a=e;try{window.__DARS_VDOM__=e}catch{}return}C(()=>{const n=k(t,e);if(!n.ok){console.warn("[Dars] Structural change detected (",n.reason,"), reloading...");try{location.reload()}catch{}return}a=e;try{window.__DARS_VDOM__=e}catch{}})}function L(e){a=e;try{window.__DARS_VDOM__=e}catch{}["click","dblclick","mousedown","mouseup","mouseenter","mouseleave","mousemove","keydown","keyup","keypress","change","input","submit","focus","blur"].forEach(n=>A(n,document))}function I(){const e=window.__DARS_VERSION_URL||"version.txt";let t=null,n=!1;function i(u,p,f,r){try{const s=new XMLHttpRequest;r&&(s.responseType=r),s.open("GET",u,!0),s.timeout=5e3,s.onreadystatechange=function(){s.readyState===4&&(s.status>=200&&s.status<300?p(s.response):f())},s.onerror=f,s.ontimeout=f,s.setRequestHeader("Cache-Control","no-store"),s.send()}catch{f()}}function o(){i(e,function(u){let p=(u||"").toString().trim();if(p&&(n=!1),l||(l=p),p&&p!==l){l=p;try{location.reload()}catch{}return}t=setTimeout(o,600)},function(){n||(console.log("[Dars] waiting for version.txt"),n=!0),t=setTimeout(o,600)},"text")}return o(),()=>{t&&clearTimeout(t)}}document.addEventListener("DOMContentLoaded",function(){window.__DARS_VDOM__?L(window.__DARS_VDOM__):console.warn("[Dars] No VDOM snapshot found for hydration"),window.__DARS_VERSION_URL&&window.__DARS_SNAPSHOT_URL&&I()})}(),window.addEventListener("scroll",()=>{const d=document.getElementById("dars-navbar");window.scrollY>20?d.classList.add("scrolled"):d.classList.remove("scrolled");const a=document.getElementById("features-section");if(a&&!a.classList.contains("visible")){const l=a.getBoundingClientRect().top,c=window.innerHeight/1.5;l<c&&(a.classList.add("visible"),document.querySelectorAll('[id^="feature-card-"]').forEach((y,_)=>{setTimeout(()=>{y.style.opacity="1",y.style.transform="translateY(0)"},_*100)}))}}),document.addEventListener("DOMContentLoaded",()=>{const d=document.getElementById("hero-logo"),a=document.getElementById("hero-title"),l=document.getElementById("hero-description"),c=document.getElementById("pip-command"),b=document.getElementById("get-started-btn"),y=document.getElementById("scroll-text");d&&setTimeout(()=>d.classList.add("show"),5),a&&setTimeout(()=>a.classList.add("show"),350),l&&setTimeout(()=>l.classList.add("show"),650),c&&setTimeout(()=>c.classList.add("show"),950),b&&setTimeout(()=>b.classList.add("show"),1250),y&&setTimeout(()=>y.classList.add("show"),1500)});function R(){window.open("https://ztamdev.github.io/Dars-Framework/docs.html","_self")}function P(){navigator.clipboard.writeText("pip install dars framework").then(()=>{const a=document.querySelector("#copy-btn"),l=a.textContent;a.textContent="Copied!",a.style.background="linear-gradient(135deg, #38c49f 0%, #2a6b5b 100%) !important",setTimeout(()=>{a.textContent=l,a.style.background="linear-gradient(135deg, #1d4a3f 0%, #2a6b5b 100%) !important"},2e3)})}document.addEventListener("DOMContentLoaded",function(){const d=document.getElementById("hamburger-btn"),a=document.getElementById("mobile-menu"),l=document.body;d&&a&&(d.addEventListener("click",function(c){c.stopPropagation(),a.style.display==="flex"?(a.style.display="none",d.classList.remove("menu-open"),l.classList.remove("menu-open")):(a.style.display="flex",d.classList.add("menu-open"),l.classList.add("menu-open"))}),a.querySelectorAll("a").forEach(c=>{c.addEventListener("click",function(){a.style.display="none",d.classList.remove("menu-open"),l.classList.remove("menu-open")})}),document.addEventListener("click",function(c){!d.contains(c.target)&&!a.contains(c.target)&&(a.style.display="none",d.classList.remove("menu-open"),l.classList.remove("menu-open"))}),document.addEventListener("keydown",function(c){c.key==="Escape"&&a.style.display==="flex"&&(a.style.display="none",d.classList.remove("menu-open"),l.classList.remove("menu-open"))}))});
