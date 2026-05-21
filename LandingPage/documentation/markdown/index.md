# Dars Framework Documentation

Dars Framework is a full-stack Python UI framework for building web applications. It provides a declarative component-based architecture where developers define UIs in Python, which are then compiled to optimized HTML, CSS, and JavaScript. The framework supports multiple deployment targets from a single codebase: Single-Page Applications (SPA), Multi-Page Applications (MPA), and Server-Side Rendered (SSR) applications with FastAPI.

---

## Why use Dars Framework?

- **Python-Native**: Write your entire application, from UI to backend logic, using 100% Python. No need to switch between multiple languages.
- **Modern Styling System**: Built-in Tailwind-like utility system that compiles directly to optimized CSS without external build tools like Node.js or PostCSS.
- **Full-Stack by Design**: Seamlessly transition from static SPAs to complex SSR applications with FastAPI integration.
- **Declarative & Reactive**: Build complex UIs with ease using a component-based architecture and a powerful reactive state management system (Hooks).
- **Multi-Target Deployment**: One codebase for Web (SPA/SSR).
- **SEO Ready**: Advanced SSR and Metadata (Head) management ensure your application is fully discoverable by search engines.
- **Developer Experience**: Fast feedback loop with a powerful CLI, hot reloading, and zero-config deployment options.

---

## Getting Started

If you are new to Dars, we recommend following the learning path in this order:

### 1. Installation & Setup

- [**Installation Guide**](#installation-guide-dars-framework): Get Dars running on your machine and set up the VS Code extension.
- [**Quick Start**](#getting-started-with-dars): Create your first "Hello World" application in minutes.
- [**CLI Reference**](#dars-cli-reference): Learn how to use the `dars` command to init, build, and export projects.

### 2. Core Concepts

- [**Components**](#dars-components-documentation): Explore the library of built-in components like Containers, Buttons, and Inputs.
- [**Styling System**](#styling-system-in-dars): Master the utility-class styling system to create stunning UIs.
- [**State Management**](#state-management-in-dars): Understand how to manage application state and reactivity.
- [**Hooks System**](#hooks-system): Learn about `V()`, `setVRef()`, `useVRef()`, and `updateVRef()` for modern component-level behavior.
- [**Global Application State & App-level Hooks**](#global-application-state): Learn about `useDynamic`, `useValue`, and other hooks for modern component behavior.

### 3. Advanced Features

- [**SPA Routing**](#spa-routing-in-dars-framework): Build fast, interactive single-page applications.
- [**SSR & FastAPI**](#server-side-rendering-in-dars-framework): Implement server-side rendering for better performance and SEO.
- [**Operations (DAP)**](#operations-in-dars): Use the Dars Action Protocol to perform client-side logic without writing JavaScript.
- [**Custom Components**](#custom-components-in-dars-framework): Learn how to extend the framework with your own reusable components.

### 4. Specialized Topics

- [**Animations**](#dars-animation-system): Add smooth transitions and interactive animations to your UI.
- [**Key Events**](#keyboard-events-in-dars): Handle global and component-level keyboard shortcuts.
- [**Exporters**](#dars-exporter-documentation): Understand how your code is compiled for different platforms.
- [**Project Config**](#dars-project-configuration): Deep dive into `dars.config.json` and environmental variables.

---

## Community & Support

- **GitHub**: [Dars Framework Repository](https://github.com/ZtaMDev/Dars-Framework)
