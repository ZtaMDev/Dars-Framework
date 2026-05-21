# Dars Framework - Development Roadmap

This document outlines the development roadmap for Dars Framework. The goal is to guide the framework's growth towards a robust and viable alternative for Python-based user interface development.

## Project Metrics

- **Current Version**: v1.9.12
- **Target**: v2.0.0 — Complete Production-Grade Fullstack Python Framework

---

## Completed (v1.0 → v1.9.12)

All of the following have been implemented and shipped:

- **Framework Core**: Base `Component` class, `App` class, Virtual DOM, reactive rendering.
- **Component System**: `Text`, `Button`, `Input`, `Container`, `Page`, `Checkbox`, `RadioButton`, `Select`, `Slider`, `DatePicker`, `Image`, `Link`, `Textarea`, `ProgressBar`, `Tooltip`, `Spinner`, `Markdown`, `Section`, `Video`, `Audio`, `Card`, `Modal`, `Navbar`, `Table`, `Tabs`, `Accordion`, `FileUpload`, `Head`, `Outlet`, `Chart`, `DataTable`.
- **Layout Components**: `Flex`, `Grid`, `Anchor`.
- **Custom Component System**: `FunctionComponent`, `Props`, extensible `Component` base.
- **Script System**: `dScript`, DAP (Dars Action Protocol), `RawJS`, zero-eval runtime, secure script injection.
- **State Management**: `State` V2 (reactive properties, increment/decrement, auto loops, transitions), legacy `dState`/`Mod` backward compat.
- **Hooks**: `useDynamic`, `useValue`, `useWatch`, `setVRef`, `updateVRef`, `V()`, `url()`, `transform()`.
- **Routing**: SPA router, multipage, nested routes, outlets, lazy loading, route types (`public`, `private`, `protected`, `SSR`), route obfuscation.
- **SSR**: Server-side rendering via FastAPI, DSP hydration, client-side rehydration.
- **Exporter**: HTML/CSS/JS with minification via **dars-bundler** (Rust/SWC/LightningCSS), style optimization pipeline, scoped CSS, static-site router elimination.
- **Web Deployment**: Web app routing, SSR, static export, and web-ready build pipelines.
- **CLI**: `dars init`, `dars dev`, `dars build`, `dars export`, `dars preview`, `dars doctor`, `dars test`, hot reload.
- **Utility Styles**: Tailwind-like utility system with arbitrary properties, gradients, rings, filters, transforms.
- **Animations**: `fadeIn`, `fadeOut`, `slideIn`, `slideOut`, `scaleIn`, `scaleOut`, `shake`, `bounce`, `pulse`, `rotate`, `flip`, `popIn`, `popOut`, `sequence`.
- **Security**: XSS prevention (DOMPurify), zero-eval runtime, DAP command registry.
- **Backend**: FastAPI plugin, SSR renderer, route loader, `apiConfig.py`, dev server orchestration.
- **HTTP Utilities**: `fetch`, `get`, `post`, `put`, `delete`, `patch`, `useData`, `DataAccessor`.
- **Form Helpers**: `FormData`, `collect_form`.
- **Browser APIs**: localStorage (get/set/remove/clear), clipboard (write/copy), scroll, focus/blur, DOM manipulation.
- **Documentation**: Full docs, VS Code extension, examples, tutorials.
- **Testing**: Integrated test framework, CLI test runner.
- **Hybrid SSR/SPA Stabilization**: Resolved hydration race conditions, cross-route hydration bugs, and stabilized the shared runtime for SSR/SPA hybrid apps.
- **Anti-Flash System**: Implemented `dars-ready` visibility mechanism with safety fallbacks to prevent FOUC and blank screens during hydration.
- **CLI v2**: Improved `dars preview` with automatic configuration detection, optional paths, and customizable ports. Standardized `dars dev` port propagation.
- **Minification Pipeline**: Optimized minification for SPA shells and SSR routes using a unified `app.js` strategy.
- **dars-bundler**: Standalone Rust minification binary (SWC + LightningCSS + Rayon) replacing rjsmin/rcssmin/Vite. Cross-platform builds (Windows/Linux/macOS) via GitHub Actions. Zero Node.js dependency.
- **Unified `minify` config key**: Replaced `viteMinify` + `defaultMinify` with a single `minify: true/false` key in `dars.config.json`. Backward-compatible with old keys.
- **Static-site router elimination**: Exporter auto-detects static (non-SPA) projects and omits `router.js` + patches `dars.min.js` to remove dead router imports at build time.

---

## 🚧 v2.0.0 Roadmap — Production-Grade Fullstack Framework

Everything below is what's needed to make Dars a real, production-usable fullstack framework.

---

### 1. Authentication & Session Management

- [ ] `DarsAuth` class with JWT generation (`jwt.encode`) and verification
- [ ] Configurable secret, algorithm (`HS256`/`RS256`), and token expiration
- [ ] Refresh token rotation flow
- [ ] Password hashing utilities (bcrypt/argon2 integration)
- [ ] Client-side auth helpers in runtime JS: `authFetch()`, `getToken()`, `setToken()`, `clearToken()`
- [ ] `isAuthenticated()` check for conditional UI rendering
- [ ] `auth.login()` / `auth.logout()` DAP actions
- [ ] Auth endpoint templates: `/api/auth/login`, `/logout`, `/refresh`, `/me`
- [ ] `@requires_auth` decorator for SSR/API routes
- [ ] `@requires_role("admin")` RBAC decorator
- [ ] Route guard decorators with custom permission checks
- [ ] Automatic 401 redirect on token expiry
- [ ] OAuth2 provider integration (Google, GitHub)

### 2. Middleware System

- [ ] `DarsMiddleware` base class with `before_request()` / `after_response()` hooks
- [ ] Global middleware registration: `app.use(middleware)`
- [ ] Route-specific middleware: `@middleware(AuthMiddleware)`
- [ ] Middleware chain execution order
- [ ] `AuthMiddleware` — verify JWT on protected routes
- [ ] `CORSMiddleware` — configurable cross-origin resource sharing
- [ ] `RateLimitMiddleware` — per-IP / per-user rate limiting
- [ ] `LoggingMiddleware` — request/response logging
- [x] `SecurityHeadersMiddleware` — CSP, HSTS, X-Frame-Options, X-Content-Type-Options, Referrer-Policy

### 3. Data Layer & Persistence

- [x] `JsonStore` — JSON file-based key-value store for prototyping
- [ ] `SQLiteStore` — lightweight SQLite wrapper
- [ ] Key-value API: `store.get()`, `store.set()`, `store.delete()`, `store.list()`
- [ ] SQLAlchemy/SQLModel ORM integration
- [ ] `DarsModel` base class with CRUD operations
- [ ] Database connection management (pooling, lifecycle)
- [ ] Auto-generated CRUD API endpoints from models
- [ ] Alembic integration for schema migrations
- [ ] `dars db migrate` / `dars db upgrade` CLI commands
- [ ] Pydantic model integration for request/response validation
- [ ] JSON schema generation from models

### 4. HTTP Client Improvements

- [x] Request interceptors — auto-inject auth headers in all requests
- [x] Response interceptors — handle 401 → redirect to login
- [ ] Global error handler for network failures
- [x] `useFetch()` hook — declarative data fetching bound to State
- [x] Automatic `isLoading` / `error` / `data` state management
- [ ] Response cache with TTL
- [ ] Auto-refetch on window focus / interval
- [ ] Implement actual retry logic (currently signature-only in `fetch()`)
- [ ] File upload via `fetch()` with `FormData` support
- [ ] Streaming / Server-Sent Events (SSE) support
- [ ] WebSocket client wrapper

### 5. Form System Completion

- [x] Fix duplicate method definitions in `form_helpers.py`
- [x] Implement `network_request` DAP operation for `FormData.submit()`
- [x] Client-side validation rules: `required`, `email`, `minLength`, `maxLength`, `pattern`, `custom`
- [x] Server-side validation via Pydantic schemas (or internal validation equivalent)
- [ ] Inline error display per field
- [ ] Form-level error summary
- [ ] `Form` wrapper component with built-in validation
- [ ] `Field` component for labeled inputs with error display
- [ ] CSRF token auto-injection in forms and fetch requests
- [ ] Form state persistence (save draft to localStorage)
- [ ] Multi-step form support

### 6. FileUpload Complete Pipeline

- [ ] `on_file_selected` callback with file metadata (name, size, type, preview URL)
- [ ] Image preview before upload
- [ ] Drag-and-drop zone support
- [ ] Max size / file type validation in browser runtime
- [ ] Upload progress indicator
- [ ] `uploadTo(url)` helper that sends files via `FormData`
- [ ] Backend file receiver endpoint template
- [ ] Multiple file handling with individual progress

### 7. Security Hardening

- [ ] CSRF token generation per session
- [ ] CSRF auto-injection in forms and fetch requests
- [ ] CSRF validation middleware
- [x] Security headers: CSP, HSTS, X-Frame-Options, X-Content-Type-Options, Referrer-Policy
- [ ] HTTPS enforcement / automatic HTTP → HTTPS redirect
- [ ] Python-side input sanitization utilities
- [ ] SQL injection prevention in data layer (parameterized queries)
- [ ] Audit logging system

### 8. Browser API Helpers

- [ ] `sessionStorage` helpers (get/set/remove/clear)
- [ ] Cookie management helpers (get/set/delete with options)
- [ ] `notify()` — Web Notifications API wrapper
- [ ] Network status detection (`navigator.onLine`)
- [ ] `IntersectionObserver` for lazy loading / scroll triggers
- [ ] `matchMedia` for responsive breakpoint detection
- [ ] `IndexedDB` wrapper for large client-side datasets
- [ ] Geolocation API helper
- [ ] Web Share API (`navigator.share()`)
- [ ] `ResizeObserver` for responsive components
- [ ] `window.print()` helper

### 9. Business Logic Patterns

- [ ] `useComputed()` / `useMemo()` — derived reactive values with dependency tracking
- [x] `Show(condition, component)` — toggle visibility
- [x] `Each(items, template_fn)` / `For` — list rendering with keys
- [ ] Server Actions — call Python functions from client-side events
- [ ] `debounce(ms, action)` — debounce event handlers
- [ ] `throttle(ms, action)` — throttle event handlers
- [ ] Global event bus / pub-sub system
- [ ] Error boundaries for component error isolation
- [ ] Suspense / loading states for async data

### 10. Missing Components

- [ ] `Toast` — notification toasts with auto-dismiss and stacking
- [ ] `Drawer` — slide-in side panel (left/right/top/bottom)
- [ ] `Breadcrumb` — navigation breadcrumbs
- [ ] `Pagination` — standalone pagination component
- [ ] `Badge` — status badges / chips
- [ ] `Avatar` — user avatar with fallback initials
- [ ] `Skeleton` — loading skeleton placeholders
- [ ] `Switch` / `Toggle` — boolean toggle switch
- [ ] `ColorPicker` — color selection input
- [ ] `RichTextEditor` — WYSIWYG text editing integration

### 11. Existing Component Upgrades

- [ ] `Table` — client-side pagination, sorting, filtering, row selection, column resize
- [ ] `Select` — search/filter, multi-select, async options loading
- [ ] `Input` — input masks, debounced `on_change`, inline validation display
- [ ] `Modal` — transition animations, backdrop click to close, nested modals
- [ ] `Navbar` — mobile responsive hamburger menu, dropdown submenus
- [ ] `Tabs` — lazy-load tab content, URL synchronization
- [ ] `Accordion` — multi-open mode, collapse/expand animations

### 12. Developer Experience

- [x] `.env` file support for secrets and environment variables
- [x] `dars.config.json` awareness in CLI (preview/dev ports and paths)
- [x] `dars generate` — scaffold new pages
- [x] `dars generate component <name>` — scaffold new components
- [x] `dars generate page <name>` — scaffold new pages
- [ ] `dars generate model <name>` — scaffold data models
- [ ] Error overlay in browser dev mode (show Python tracebacks)
- [ ] Source maps for generated JS
- [ ] Docker deployment guide and `Dockerfile` template
- [ ] Vercel / Railway deployment guides
- [ ] Production build optimization checklist

### 13. Testing & Quality

- [ ] Component unit testing helpers (render + assert)
- [ ] Integration test utilities
- [ ] E2E testing guide (Playwright/Cypress)
- [ ] Snapshot testing for exported HTML output
- [ ] CI/CD pipeline templates (GitHub Actions)

---

## Priority Order

| #   | Area                    | Why First                                  |
| --- | ----------------------- | ------------------------------------------ |
| 1   | **Authentication**      | Nothing works without user identity        |
| 2   | **Middleware**          | Auth depends on middleware pipeline        |
| 3   | **Data Persistence**    | Apps need to store data                    |
| 4   | **Form Validation**     | Every app has forms                        |
| 5   | **HTTP Client**         | Frontend needs to talk to backend reliably |
| 6   | **FileUpload Pipeline** | Current component is non-functional        |
| 7   | **Security Hardening**  | Required for production                    |
| 8   | **Business Logic**      | Conditional rendering, computed state      |
| 9   | **Browser APIs**        | Quality of life                            |
| 10  | **Components**          | New + upgraded components                  |
| 11  | **DX & Testing**        | Developer happiness                        |
