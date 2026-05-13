# Dars Framework - Development Roadmap

This document outlines the development roadmap for Dars Framework, covering implemented features, planned improvements to existing systems, and ecosystem expansions. The goal is to guide the framework's growth towards a robust and viable alternative for Python-based user interface development.

## Project Metrics

### Lines of Code (LOC) - Approximate

Based on the current analysis of the source code (Python, Markdown, JavaScript, CSS):

- **Total**: 836931 lines
- **Docs**: 30021 lines

## Development Roadmap

The following features and components have been successfully implemented in Dars Framework:

- [x] **Framework Core**
  - [x] Base `Component` class for all UI elements.
  - [x] Main `App` class for application management.
- [x] **Component System**
  - [x] **Basic Components**: `Text`, `Button`, `Input`, `Container`, `Page` (with support for per-page scripts in multipage), `Checkbox`, `RadioButton`, `Select`, `Slider`, `DatePicker`, `Image`, `Link`, `Textarea`, `ProgressBar`, `Tooltip`.
  - [x] **Advanced Components**: `Card`, `Modal`, `Navbar`.
  - [x] **Layout Components**: `Flex`, `Grid`, `Anchor`.
  - [x] **Custom Component System**: Support for extending the base `Component` class and creating custom components with customizable `render` methods and events.
- [x] **Script System**
  - [x] `dScript`: Flexible script class supporting both inline and file-based JavaScript, allowing editable presets and advanced actions.
  - [x] Event Handling: Event binding system for custom components, supporting a wide range of `EventTypes` (Mouse, Keyboard, Form, Load & Window, Custom).
- [x] **Exporter System**
  - [x] HTML/CSS/JS Exporter: Generates static web applications, now with native `dScript` support.
- [x] **Development Tools**
  - [x] CLI (Command Line Interface) with `Rich` for an improved user experience.
  - [x] Preview System: Allows quick preview of generated applications.
- [x] **Documentation and Examples**
  - [x] Comprehensive documentation, including sections on custom component creation and event handling.
  - [x] Functional examples demonstrating various framework capabilities.
- [x] **Hot Reloading**: Implemented in development/beta for a smoother development experience.
- [x] **Integrated Testing Framework**

### Phase 1: Consolidation and Optimization (Short-Term)

This phase will focus on strengthening the framework's current foundation, improving performance and stability, and optimizing the developer experience.

- [x] **Framework Core Enhancements**
  - [x] **Rendering Optimization**: Research and apply techniques to improve the `render` method's performance, especially for applications with many elements or frequent updates. Consider implementing a Virtual DOM or an efficient reconciliation mechanism to minimize direct DOM manipulations.
  - [x] **Reactive State Management**: Develop a robust system for global and local application state management, enabling efficient reactive UI updates.
  - [x] **Improved Property Typing and Validation**: Extend the property system to include more complex validations and clear error messages at development time, facilitating debugging.
  - [x] **Error Handling and Debugging**: Implement robust tools and mechanisms for runtime error handling and facilitate debugging of Dars applications, both in Python and in the generated JavaScript code.

- [c] **Component System Enhancements**
  - [x] **Component Lifecycle**: Define and document a clear lifecycle for components (mounting, updating, unmounting) that allows developers to execute logic at specific times.
  - [x] **Hooks or Mixins**: Explore the implementation of patterns like Hooks or Mixins to reuse state and behavior logic between components more cleanly and modularly.

- [x] **HTML/CSS/JS Exporter Optimization**
  - [x] **Minification and Bundling**: Integrate minification and bundling tools (e.g., based on `esbuild` or `rollup` via Python) to reduce the size of generated JavaScript and CSS files, improving loading times.
  - [x] **Asset Optimization**: Implement automatic optimization of images and other static assets during the export process.
  - [x] **Scoped CSS Generation**: Explore options for generating CSS with scope limited to components, avoiding style conflicts and facilitating the development of reusable components.

- [x] **CLI Enhancements**
  - [x] **Additional Commands**: Add commands for creating new projects (`dars init project`).
  - [x] **Integration with Testing Tools**: Facilitate the execution of unit and integration tests directly from the CLI.
  - [x] **Detailed Feedback**: Improve CLI error messages and feedback to guide the developer more effectively.

### Phase 2: Ecosystem Expansion and Cross-Platform (Mid-Term)

This phase will focus on expanding Dars' capabilities to new platforms and building a richer ecosystem around the framework.

- [x] **Desktop Application Support with Electron**: Enhance the Dars API with a specialized submodule for integration with Electron, enabling the creation of cross-platform desktop applications from Python. This will include:
  - [x] A dedicated submodule in the Dars API to interact with Electron functionalities.
  - [x] Handling bidirectional communication between the main Electron process (Node.js) and the rendering process (Python/JS).
  - [x] Tools and templates to facilitate the packaging and distribution of Electron applications.

- [x] **More Integrated Components**
  - [x] **Data Visualization Components**: `Chart` (integration with libraries like Chart.js or D3.js), `Table` (with pagination, sorting, and filtering).
  - [x] **Multimedia Components**: `Video`, `Audio`.
  - [x] **Advanced Navigation**: `Router` (for single-page application route management), `Tabs`, `Accordion`.
  - [x] **Advanced Components**:`FileUpload`.

- [x] **Plugin and Extension System**
  - [x] Develop a clear API for developers to create their own plugins and extensions for Dars, facilitating integration with third-party tools and framework customization.

- [x] **dScript Enhancements**
  - [x] **dScript Modules**: Allow importing and exporting modules within dScript to better organize JavaScript logic.
  - [x] **Integration with Popular JS Libraries**: Facilitate the integration of popular JavaScript libraries (e.g., for animations, DOM manipulation, etc.) within dScript.

### Phase 3: Maturity and Adoption (Long-Term)

This phase will focus on mass adoption, long-term stability, and community growth.

- [x] **Ecosystem Development Tools**
  - [x] **VS Code Extension**: Develop a comprehensive extension for Visual Studio Code including:
    - [x] Intelligent autocompletion for components, properties, and events.
    - [x] Real-time UI preview within the editor.
    - [x] Integrated debugging tools.
    - [x] Code snippet generation.
  - [x] **IDE Integration**: Explore integration with other popular Python IDEs (PyCharm, etc.).
  - [x] **Automated Testing Tools**: An integrated testing framework that facilitates writing unit, integration, and end-to-end tests for Dars applications.

- [x] **Documentation and Community Resources**
  - [x] **Interactive Tutorials and Advanced Examples**: Create a series of step-by-step tutorials and complete application examples for different use cases.
  - [x] **Contribution Guides**: Facilitate contribution to the Dars codebase and its documentation.

### Phase 2.5: Fullstack Framework & Security Architecture (v1.6.9 - v1.9.0)

This phase transforms Dars into a complete fullstack Python framework with enterprise-grade security and automatic backend integration.

#### Security & Routing

- [x] **Secure Router Foundation**
  - [x] Lazy loading for private routes
  - [x] Route obfuscation (hide sensitive routes from client)
  - [x] Route types: `public`, `private`, `protected`
  - [x] Backend route loader endpoints

- [ ] **VRef Hooks + Middleware**
  - [x] Complete `setVRef()` exporter integration
  - [ ] Middleware system (AuthMiddleware, RateLimitMiddleware, CORSMiddleware)
  - [ ] Middleware chain execution
  - [ ] Route-specific and global middleware

- [x] **FastAPI Backend Plugin**
  - [x] `DarsBackend` class for FastAPI integration
  - [x] Route loading endpoints
  - [x] Middleware execution in backend
  - [x] Request/response serialization

- [ ] **Authentication System**
  - [ ] JWT token generation and verification
  - [ ] Session management
  - [ ] Frontend auth helpers (`login()`, `logout()`, `isAuthenticated()`)
  - [ ] Auth endpoints (`/api/auth/login`, `/api/auth/logout`, `/api/auth/refresh`)

- [x] **SSR Implementation**
  - [x] Server-side rendering without middleware
  - [x] Direct backend integration for SSR
  - [x] Context injection
  - [x] Client-side hydration

- [ ] **Route Guards & Permissions**
  - [ ] Role-based access control (RBAC)
  - [ ] Permission system with custom checks
  - [ ] Route guard decorators

- [ ] **Production Hardening**
  - [ ] HTTPS enforcement
  - [ ] CSRF protection
  - [x] XSS prevention
  - [ ] Security headers
  - [ ] Audit logging

#### Fullstack Integration

- [x] **Backend Auto-Detection**
  - [x] Automatic detection of `/backend` or `/darsBackend` directories
  - [x] Detection of `api.py` and `apiConfig.py`
  - [x] Desktop mode support (Electron)

- [x] **apiConfig.py System**
  - [x] Centralized URL configuration
  - [x] `DEV_FRONTEND_URL` and `DEV_BACKEND_URL` constants
  - [x] `BUILD_FRONTEND_URL` and `BUILD_BACKEND_URL` constants
  - [x] `get_frontend_url()` and `get_backend_url()` helpers
  - [x] Accessible from both frontend and backend

- [x] **Dev Server Orchestration**
  - [x] `dars dev` starts both frontend and backend concurrently
  - [x] Frontend on `localhost:8000` (rTimeCompile)
  - [x] Backend on `localhost:3000` (uvicorn)
  - [x] Hot reload for both servers
  - [x] Clear console output with URLs
  - [x] Graceful shutdown

- [x] **Fullstack Polish & Documentation**
  - [x] Unified CLI experience
  - [x] Fullstack tutorial
  - [x] Backend integration guide
  - [x] Deployment guide
  - [x] Best practices documentation

**Target**: v2.0.0 - Complete Fullstack Python Framework
