// ==================== ROUTER ====================
import { dispatch, __darsConfig } from "./dap.js";
import { _sanitize, $, _attachEventsMap, registerStates } from "./dars.min.js";
import { updatePageMetadata } from "./ssr.js";
import { _executeExternalScript } from "./dap.js";
// Vite minification compatible - uses string literals for all object properties

export const __spaRoutes = []; // Array of route configs (for pattern matching)
export const __spaRoutesMap = new Map(); // name -> route config
export const __spaPreloaded = new Set(); // preloaded routes
export let __spaCurrentRoute = null;
export let __spaCurrentParams = {};
window.__DARS_INITIAL_LOAD__ = true;
export let __spaConfig = null;
export let __spa404Route = null;

export function _normalizePath(input) {
  try {
    let p = String(input || "");
    const hashIdx = p.indexOf("#");
    if (hashIdx >= 0) p = p.slice(0, hashIdx);
    const qIdx = p.indexOf("?");
    if (qIdx >= 0) p = p.slice(0, qIdx);
    if (!p) return "/";
    if (!p.startsWith("/")) p = "/" + p;
    while (p.length > 1 && p.endsWith("/")) p = p.slice(0, -1);
    return p;
  } catch (e) {
    return "/";
  }
}

/**
 * Convert route pattern to regex (Vite-safe)
 * /user/:id -> /user/(?<id>[^/]+)
 */
export function _routeToRegex(pattern) {
  try {
    const regexStr = String(pattern).replace(
      /:([a-zA-Z_][a-zA-Z0-9_]*)/g,
      "(?<$1>[^/]+)",
    );
    return new RegExp(`^${regexStr}$`);
  } catch (e) {
    return null;
  }
}

/**
 * Match a path against all routes
 * Returns { route, params } or null
 */
export function _matchRoute(path) {
  try {
    const normalized = _normalizePath(path);
    for (let i = 0; i < __spaRoutes.length; i++) {
      const route = __spaRoutes[i];
      const regex = route["_regex"] || _routeToRegex(route["path"]);
      if (regex) {
        route["_regex"] = regex;
      } // Cache regex

      const match = String(normalized).match(regex);
      if (match) {
        const params = match["groups"] || {};
        return { route: route, params: params };
      }
    }
  } catch (e) {}
  return null;
}

/**
 * Register SPA routing configuration (Vite-safe)
 */
export function registerSPAConfig(config) {
  try {
    if (config.strictMode !== undefined)
      __darsConfig.strictMode = config.strictMode;
    if (config.allowInlineJS !== undefined)
      __darsConfig.allowInlineJS = config.allowInlineJS;
    if (__darsConfig.strictMode) __darsConfig.allowInlineJS = false;

    if (config.routes) {
      __spaConfig = config;
      if (!config || !Array.isArray(config["routes"])) return;

      // Clear and rebuild routes
      __spaRoutes.length = 0;
      __spaRoutesMap.clear();

      const routes = config["routes"];
      for (let i = 0; i < routes.length; i++) {
        const route = routes[i];
        if (!route["path"] || !route["name"]) continue;
        __spaRoutes.push(route);
        __spaRoutesMap.set(route["name"], route);
      }

      // Register 404 page if exists
      if (config["notFound"]) {
        __spa404Route = config["notFound"];
      }

      // Robust initialization strategy
      window.__DARS_ROUTER_INIT = false;

      function _attemptInit() {
        if (window.__DARS_ROUTER_INIT) return;

        // If VDOM is missing but might be coming (interactive/loading), wait unless it's the 'load' event
        const hasData = window.__ROUTE_VDOM__ || window.__DARS_VDOM__;
        const isComplete = document.readyState === "complete";

        if (hasData || isComplete) {
          window.__DARS_ROUTER_INIT = true;
          _initializeRouter();
        }
      }

      // 1. Try immediately
      _attemptInit();

      // 2. Try on DOMContentLoaded (earliest safe moment)
      if (!window.__DARS_ROUTER_INIT) {
        document.addEventListener("DOMContentLoaded", _attemptInit);
      }

      // 3. Try on load (fallback for late scripts)
      if (!window.__DARS_ROUTER_INIT) {
        window.addEventListener("load", function () {
          // Force init on load even if data missing (it's not coming)
          if (!window.__DARS_ROUTER_INIT) {
            window.__DARS_ROUTER_INIT = true;
            _initializeRouter();
          }
        });
      }
    }
  } catch (e) {
    console.error("[Dars Router] Config error:", e);
  }
}

/**
 * Initialize the SPA router
 */
export function _initializeRouter() {
  try {
    // Handle initial route
    const initialPath = _normalizePath(window.location.pathname);

    // Skip initial fetch if already hydrated (SSR)
    let skipInit = false;
    const match = _matchRoute(initialPath);

    const isSSRRoute = match && match.route && match.route["type"] === "ssr";
    const vdomSource =
      isSSRRoute ? window.__ROUTE_VDOM__ || window.__DARS_VDOM__ : null;
    const hydratedPath = window.__DARS_HYDRATED_PATH__ || "/";

    if (
      isSSRRoute &&
      vdomSource &&
      (initialPath === hydratedPath ||
        (initialPath === "/" && hydratedPath === "/index.html"))
    ) {
      // Find matching route to set as current
      if (match && match.route) {
        // Update global state to reflect current route without navigating
        __spaCurrentRoute = initialPath;
        __spaCurrentParams = match.params || {};
        window["__DARS_ROUTE_PARAMS__"] = __spaCurrentParams;

        // Mark the route as loaded and populate its data from SSR
        match.route.vdom = vdomSource;
        match.route.html =
          document.getElementById("__dars_spa_root__") ?
            document.getElementById("__dars_spa_root__").innerHTML
          : "";
        match.route.loaded = true;

        // Ensure history state is correctly set for the initial page
        window.history.replaceState(
          {
            path: initialPath,
            params: __spaCurrentParams,
          },
          document.title,
          initialPath,
        );

        skipInit = true;
      }
    }

    if (!skipInit) {
      // Only take over if the current path matches an SPA route
      if (match) {
        // HIDE STATIC CONTENT IMMEDIATELY to avoid flash of fallback index.html
        const container = document.getElementById("__dars_spa_root__");
        if (container) {
          document.querySelectorAll(".dars-page").forEach((el) => {
            if (el !== container && !container.contains(el))
              el.style.display = "none";
          });
          container.style.display = "";
        }
        _navigateToRoute(initialPath, { replace: true, skipPushState: true });
      } else {
        // Fallback for missing SPA routes in combined mode
        if (
          initialPath !== "/" &&
          initialPath !== "/index.html" &&
          !initialPath.endsWith(".html")
        ) {
          const notFoundPath = __spaConfig ? __spaConfig["notFoundPath"] : null;
          if (notFoundPath) {
            _navigateToRoute(notFoundPath, {
              replace: true,
              skipPushState: true,
            });
          } else {
            // No 404 path defined? reveal the page just in case
            document.documentElement.setAttribute("dars-ready", "true");
          }
        }
      }
    }

    // Listen for popstate (browser back/forward)
    window.addEventListener("popstate", function (event) {
      try {
        const path = _normalizePath(
          (event.state && event.state["path"]) || window.location.pathname,
        );
        const params = (event.state && event.state["params"]) || {};

        const match = _matchRoute(path);
        if (match) {
          _navigateToRoute(path, {
            replace: true,
            skipPushState: true,
            params: params,
          });
        } else {
          // Back to static page: hide SPA root and show static content
          const container = document.getElementById("__dars_spa_root__");
          if (container) container.style.display = "none";
          document.querySelectorAll(".dars-page").forEach((el) => {
            if (el !== container) el.style.display = "";
          });
          document.documentElement.setAttribute("dars-ready", "true");
        }
      } catch (e) {}
    });

    // Intercept link clicks for SPA navigation
    document.addEventListener("click", function (event) {
      try {
        const link = event.target.closest("a[href]");
        if (!link) return;

        const href = link.getAttribute("href");
        if (
          !href ||
          href.startsWith("http") ||
          href.startsWith("//") ||
          href.startsWith("#")
        ) {
          return; // External link or anchor
        }

        const normalizedHref = _normalizePath(href);

        // Check if this matches any SPA route
        const match = _matchRoute(normalizedHref);

        // Intercept if it matches an SPA route, OR if it's a potential 404 (no file extension)
        // This ensures smooth 404 handling even when navigating from a static root
        const isFile = normalizedHref
          .split("?")[0]
          .split("/")
          .pop()
          .includes(".");

        if (match || (!isFile && __spaConfig && __spaConfig["notFoundPath"])) {
          event.preventDefault();
          navigateTo(normalizedHref);
        }
      } catch (e) {}
    });
  } catch (e) {
    console.error("[Dars Router] Init error:", e);
  }
}

/**
 * Navigate to a route path (public API)
 */
export function navigateTo(path, params) {
  try {
    _navigateToRoute(_normalizePath(path), {
      replace: false,
      params: params || {},
    });
  } catch (e) {
    console.error("[Dars Router] Navigate error:", e);
  }
}

/**
 * Internal navigation handler
 */
export async function _navigateToRoute(path, options) {
  try {
    options = options || {};

    path = _normalizePath(path);

    // Match route (supports parameters)
    let match = _matchRoute(path);
    let params = options["params"] || {};

    // If no match AND path is root, try index route (redirect to index)
    if (
      !match &&
      (path === "/" || path === "") &&
      __spaConfig &&
      __spaConfig["index"]
    ) {
      const indexRoute = __spaRoutesMap.get(__spaConfig["index"]);
      if (indexRoute) {
        match = { route: indexRoute, params: {} };
        path = indexRoute["path"];
      }
    }

    // If still no match, try 404 page
    if (!match) {
      console.log("[Dars Router] No match for:", path);

      // Try redirect to configured 404 path
      if (__spaConfig && __spaConfig["notFoundPath"]) {
        const notFoundPath = __spaConfig["notFoundPath"];
        // Avoid infinite loop if 404 page itself is missing
        if (path !== notFoundPath) {
          console.log("[Dars Router] Redirecting to 404 path:", notFoundPath);
          await _navigateToRoute(notFoundPath, {
            replace: true,
            skipPushState: false,
          });
          return;
        }
      }

      if (__spa404Route) {
        console.log("[Dars Router] Using legacy 404 route object");
        match = { route: __spa404Route, params: {} };
      } else {
        console.error(
          "[Dars Router] Route not found and no 404 page configured:",
          path,
        );
        return;
      }
    }

    const route = match["route"];
    const matchedParams = match["params"] || {};

    // Merge params
    for (const key in matchedParams) {
      params[key] = matchedParams[key];
    }

    // Update browser history
    if (!options["skipPushState"]) {
      const state = { path: path, params: params };
      if (options["replace"]) {
        history.replaceState(state, "", path);
      } else {
        history.pushState(state, "", path);
      }
    }

    // Load route content (await for lazy loading)
    await _loadRoute(route, params);

    // Update current route
    __spaCurrentRoute = path;
    __spaCurrentParams = params;

    // Store params in window for access in components
    window["__DARS_ROUTE_PARAMS__"] = params;

    // Preload specified routes
    const preload = route["preload"];
    if (preload && Array.isArray(preload)) {
      for (let i = 0; i < preload.length; i++) {
        _preloadRoute(preload[i]);
      }
    }

    // Dispatch custom event
    try {
      const detail = {
        from: __spaCurrentRoute,
        to: path,
        route: route,
        params: params,
      };
      const ev = new CustomEvent("dars:route-change", { detail: detail });
      window.dispatchEvent(ev);
    } catch (e) {}
  } catch (e) {
    console.error("[Dars Router] Navigation error:", e);
  }
}

/**
 * Load and render a route (Hierarchical)
 */
export async function _loadRoute(route, params) {
  try {
    function _getLoadingHTML(r) {
      try {
        // 1) Per-route loading override
        if (r && r["loadingHtml"]) {
          const raw = String(r["loadingHtml"]);
          if (raw.includes('data-dars-ssr-loading="1"')) return raw;
          return `<div data-dars-ssr-loading="1">${raw}</div>`;
        }
        // 2) Global SPA config loading override
        if (__spaConfig && __spaConfig["loadingHtml"]) {
          const raw = String(__spaConfig["loadingHtml"]);
          if (raw.includes('data-dars-ssr-loading="1"')) return raw;
          return `<div data-dars-ssr-loading="1">${raw}</div>`;
        }
      } catch (e) {}
      return '<div data-dars-ssr-loading="1" style="padding:24px;font-family:system-ui,-apple-system,sans-serif;opacity:.75">Loading...</div>';
    }

    function _getErrorHTML(r) {
      try {
        // 1) Per-route error override
        if (r && r["errorHtml"]) {
          const raw = String(r["errorHtml"]);
          if (raw.includes('data-dars-ssr-error="1"')) return raw;
          return `<div data-dars-ssr-error="1">${raw}</div>`;
        }
        // 2) Global SPA config error override
        if (__spaConfig && __spaConfig["errorHtml"]) {
          const raw = String(__spaConfig["errorHtml"]);
          if (raw.includes('data-dars-ssr-error="1"')) return raw;
          return `<div data-dars-ssr-error="1">${raw}</div>`;
        }
      } catch (e) {}
      return '<div data-dars-ssr-error="1" style="padding:24px;font-family:system-ui,-apple-system,sans-serif;opacity:.75">Failed to load page.</div>';
    }

    function _getOutletEl(wrapper, outletId) {
      try {
        if (!wrapper) return null;
        const wanted = String(outletId || "main");
        // Prefer explicit id match
        const sel = `[data-dars-outlet="true"][data-dars-outlet-id="${wanted}"]`;
        const found = wrapper.querySelector(sel);
        if (found) return found;
        // Backward compat: first outlet
        return wrapper.querySelector('[data-dars-outlet="true"]');
      } catch (e) {
        return null;
      }
    }

    function _applyParamsToHTML(html, p) {
      try {
        let out = String(html || "");
        const pp = p || {};
        for (const key in pp) {
          try {
            const value = pp[key];
            const regex = new RegExp(`\\{\\{${key}\\}\\}`, "g");
            out = out.replace(regex, String(value));
          } catch (e) {}
        }
        return out;
      } catch (e) {
        return String(html || "");
      }
    }

    function _renderRouteInto(mountEl, r, p, isRootLevel) {
      try {
        if (!mountEl) return null;

        let wrapper = null;
        if (window.__DARS_INITIAL_LOAD__) {
          wrapper = mountEl.querySelector(
            `[data-dars-route-wrapper="${r["name"]}"]`,
          );
        }

        if (wrapper) {
          // Real SSR: HTML is already there. Just hydrate it.
        } else {
          // Create wrapper for this route
          wrapper = document.createElement("div");
          wrapper.setAttribute("data-dars-route-wrapper", r["name"]);
          wrapper.style.height = "100%";
          wrapper.style.width = "100%";

          // Fill HTML (with params) - Sanitized
          const html = _applyParamsToHTML(r["html"] || "", p);
          wrapper.innerHTML = _sanitize(html);

          // Replace content
          mountEl.innerHTML = "";
          mountEl.appendChild(wrapper);
        }

        // Assets / hydration
        if (r["title"]) document.title = String(r["title"]);
        if (r["styles"]) _injectStyles(r["name"], r["styles"]);
        if (r["scripts"]) _executeScripts(r["scripts"], r["name"]);
        if (r["events"]) _attachEventsMap(r["events"]);

        if (r["states"] && Array.isArray(r["states"])) {
          registerStates(r["states"]);
        }
        if (r["vdom"] && Object.keys(r["vdom"]).length > 0) {
          try {
            if (typeof window["DarsHydrate"] === "function")
              window["DarsHydrate"](wrapper);
          } catch (e) {}
        }

        // Dispatch content-loaded event for external highlighters (e.g. Markdown)
        document.dispatchEvent(
          new CustomEvent("dars:content-loaded", {
            detail: { element: wrapper, route: r["name"] },
          }),
        );

        if (isRootLevel)
          try {
            window.scrollTo(0, 0);
          } catch (e) {}
        return wrapper;
      } catch (e) {
        return null;
      }
    }

    function _renderChain(chain, p) {
      try {
        let container = document.getElementById("__dars_spa_root__");
        if (!container) return;

        // In Combined Mode: hide static pages and show SPA root
        document.querySelectorAll(".dars-page").forEach((el) => {
          if (el !== container && !container.contains(el))
            el.style.display = "none";
        });
        container.style.display = "";
        document.documentElement.setAttribute("dars-ready", "true");

        // Cleanup assets for inactive routes BEFORE rendering new chain
        const activeRouteNames = new Set(chain.map((r) => r["name"]));

        const allScripts = document.querySelectorAll(".dars-route-script");
        allScripts.forEach((script) => {
          const scriptRoute = script.getAttribute("data-route");
          if (scriptRoute && !activeRouteNames.has(scriptRoute)) {
            try {
              script.remove();
            } catch (e) {}
          }
        });

        const allStyles = document.querySelectorAll(
          'style[id^="dars-route-styles-"]',
        );
        allStyles.forEach((style) => {
          const styleId = style.id;
          const routeName = styleId.replace("dars-route-styles-", "");
          if (routeName && !activeRouteNames.has(routeName)) {
            try {
              style.remove();
            } catch (e) {}
          }
        });

        // Render each level into its mount
        let lastWrapper = null;
        for (let i = 0; i < chain.length; i++) {
          const r = chain[i];
          const isRootLevel = i === 0;

          // Render this route into current container
          lastWrapper = _renderRouteInto(container, r, p, isRootLevel);
          if (!lastWrapper) return;

          // Move container to next outlet
          if (i < chain.length - 1) {
            const nextOutletId = String(chain[i + 1]["outletId"] || "main");
            const outlet = _getOutletEl(lastWrapper, nextOutletId);
            if (!outlet) {
              console.error(
                "[Dars Router] Missing outlet in parent route:",
                r["name"],
              );
              return;
            }
            container = outlet;
          }
        }

        // Update page metadata (title, description, OG tags, etc.) if available
        const leafRoute = chain[chain.length - 1];
        if (leafRoute) {
          if (leafRoute["headMetadata"]) {
            try {
              updatePageMetadata(leafRoute["headMetadata"]);
            } catch (e) {
              console.error("[Dars Router] Error updating metadata:", e);
            }
          } else if (leafRoute["title"]) {
            try {
              document.title = leafRoute["title"];
            } catch (e) {}
          }
        }
      } catch (e) {
        console.error("[Dars Router] Render chain error:", e);
      }
    }

    // If route is public but missing content (Combined Mode / Lazy Load), fetch manifest
    if (route["type"] === "public" && !route["html"]) {
      try {
        const manifestUrl = `/route_${route["name"]}.json`;
        const response = await fetch(manifestUrl + "?t=" + Date.now());
        if (response.ok) {
          const routeData = await response.json();
          route["html"] = routeData["html"] || "";
          route["vdom"] = routeData["vdom"] || {};
          route["scripts"] = routeData["scripts"] || [];
          route["styles"] = routeData["styles"] || "";
          route["headMetadata"] = routeData["headMetadata"] || {};
        }
      } catch (e) {
        console.warn(
          "[Dars Router] Failed to load lazy manifest for:",
          route["name"],
        );
      }
    }

    // If route is SSR and needs fetching, wait for it BEFORE rendering to avoid suspense flashes
    if (route["type"] === "ssr" && !route["html"]) {
      try {
        const backendUrl = (__spaConfig && __spaConfig["backendUrl"]) || "";
        const loaderUrl = route["ssr_endpoint"] || `/api/ssr/${route["name"]}`;
        let fullUrl = loaderUrl;
        if (backendUrl && backendUrl !== "/") {
          fullUrl =
            backendUrl.replace(/\/$/, "") +
            (loaderUrl.startsWith("/") ? loaderUrl : "/" + loaderUrl);
        }

        const sep = fullUrl.includes("?") ? "&" : "?";
        fullUrl = fullUrl + sep + "_t=" + Date.now();

        const response = await fetch(fullUrl, {
          headers: { "Content-Type": "application/json" },
          mode: "same-origin",
          credentials: "same-origin",
        });

        if (!response.ok)
          throw new Error(`Failed to load route: ${response.status}`);

        const routeData = await response.json();

        route["html"] = routeData["html"] || "";
        route["scripts"] = routeData["scripts"] || [];
        route["events"] = routeData["events"] || {};
        route["vdom"] = routeData["vdom"] || {};
        route["states"] = routeData["states"] || [];
        route["styles"] = routeData["styles"] || route["styles"] || "";
        route["headMetadata"] =
          routeData["headMetadata"] || route["headMetadata"];

        // Native scripts will execute automatically when scripts are appended
      } catch (error) {
        console.error("[Dars Router] Error loading SSR route:", error);
        route["html"] = _getErrorHTML(route);
      }
    }

    // 1. Build route chain [Root, ..., Parent, Child]
    const chain = [];
    let curr = route;
    while (curr) {
      chain.unshift(curr);
      curr = curr["parent"] ? __spaRoutesMap.get(curr["parent"]) : null;
    }

    // Single paint with real content (no suspense flash)
    _renderChain(chain, params);

    // After the first render chain is complete, unset initial load flag
    window.__DARS_INITIAL_LOAD__ = false;
  } catch (e) {
    console.error("[Dars Router] Load error:", e);
  }
}

/**
 * Inject styles for a route
 */
export function _injectStyles(routeName, styles) {
  try {
    const styleId = `dars-route-styles-${routeName}`;

    // Remove old styles for this route
    const oldStyle = document.getElementById(styleId);
    if (oldStyle) {
      oldStyle.remove();
    }

    // Add new styles
    const styleEl = document.createElement("style");
    styleEl.id = styleId;
    styleEl.textContent = String(styles);
    document.head.appendChild(styleEl);
  } catch (e) {}
}

/**
 * Execute scripts for a route
 */
export function _executeScripts(scripts, routeName) {
  try {
    if (!Array.isArray(scripts)) return;

    for (let i = 0; i < scripts.length; i++) {
      const script = scripts[i];
      if (typeof script === "string") {
        // Check if it's a filename (ends with .js)
        if (script.endsWith(".js")) {
          _loadExternalScript(script, false, routeName);
        } else {
          // Inline script code
          try {
            const s = document.createElement("script");
            s.textContent = script;
            document.body.appendChild(s);
            s.remove();
          } catch (e) {
            console.error("[Dars Router] Script error:", e);
          }
        }
      } else {
        // Script object
        if (script["src"]) {
          _loadExternalScript(script["src"], script["module"], routeName);
        } else if (script["code"]) {
          try {
            const s = document.createElement("script");
            s.textContent = script["code"];
            s.className = "dars-route-script";
            if (routeName) s.setAttribute("data-route", routeName);
            if (script["module"]) s.type = "module";
            document.body.appendChild(s);
          } catch (e) {
            console.error("[Dars Router] Script error:", e);
          }
        }
      }
    }
  } catch (e) {}
}

/**
 * Load external script
 */
export function _loadExternalScript(src, isModule, routeName) {
  try {
    const existingScript = document.querySelector(`script[src="${src}"]`);
    if (existingScript) {
      if (!existingScript.classList.contains("dars-route-script")) {
        existingScript.classList.add("dars-route-script");
        if (routeName) existingScript.setAttribute("data-route", routeName);
      }
      return;
    }

    const script = document.createElement("script");
    script.src = String(src);
    script.async = false; // Ensure sequential execution
    script.className = "dars-route-script"; // Tag for cleanup
    if (routeName) script.setAttribute("data-route", routeName);
    if (isModule) {
      script.type = "module";
    }

    // Simulate DOMContentLoaded for scripts that depend on it
    script.onload = function () {
      try {
        // Trigger a custom event that scripts can listen to
        const event = new Event("DOMContentLoaded");
        document.dispatchEvent(event);
      } catch (e) {}
    };

    script.onerror = function () {
      console.error("[Dars Router] Script load failed:", src);
    };
    document.body.appendChild(script);
  } catch (e) {}
}

/**
 * Preload a route in the background
 */
export function _preloadRoute(path) {
  try {
    if (__spaPreloaded.has(path)) return; // Already preloaded
    const route = _matchRoute(path);
    if (!route) return;
    __spaPreloaded.add(path);
    route["route"]["__preloaded"] = true;
  } catch (e) {}
}

/**
 * Get current route (public API)
 */
export function getCurrentRoute() {
  return __spaCurrentRoute;
}

/**
 * Get current route parameters (public API)
 */
export function getRouteParams() {
  return __spaCurrentParams;
}
