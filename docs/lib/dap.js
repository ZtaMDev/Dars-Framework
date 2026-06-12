// ==================== DARS ACTION PROTOCOL (DAP) ====================
import {
  change,
  $,
  _sanitize,
  _alert,
  createComponent,
  deleteComponent,
  updateVRef,
  __registry,
} from "./dars.min.js";

export function _executeExternalScript(code, context) {
  if (!code) return null;
  try {
    const s = document.createElement("script");
    const ctxId = "__dars_ctx_" + Math.random().toString(36).substr(2, 9);
    if (context) window[ctxId] = context;

    // Provide local 'event' and 'element' (this) to the script
    const setup =
      context ?
        `const event = window["${ctxId}"].event; const element = window["${ctxId}"].element; delete window["${ctxId}"];`
        : "";

    s.textContent = `(async () => { 
          ${setup}
          try { 
              ${code} 
          } catch(e) { 
              console.error('[Dars] Script execution error:', e); 
          } 
      })();`;

    document.body.appendChild(s);
    s.remove();
  } catch (e) {
    console.error("[Dars:Security] Error executing external script:", e);
  }
  return null;
}

export const __commandRegistry = new Map();
export const __darsConfig = {
  allowInlineJS: false, // Disabled by default; enabled only for compile-time generated code
  strictMode: false, // If true, allowInlineJS becomes false automatically
  debug: false,
};

/**
 * Execute a DAP action securely using the Command Registry.
 */
export function dispatch(action, context) {
  if (!action || typeof action !== "object") return null;

  const op = action.op;
  const args = action.args || action.data || action;

  if (__darsConfig.strictMode) __darsConfig.allowInlineJS = false;
  if (__darsConfig.debug) console.log("[Dars:DAP] Dispatching:", op, args);

  const handler = __commandRegistry.get(op);
  if (handler) {
    try {
      return handler(args, context);
    } catch (e) {
      console.error(`[Dars:DAP] Error executing command '${op}':`, e);
    }
  } else {
    console.warn(`[Dars:DAP] Unknown command: ${op}`);
  }
  return null;
}

// Internal command registration
export function _registerCommand(op, fn) {
  __commandRegistry.set(op, fn);
}

// Initialize core commands
_registerCommand("inline", (args) => {
  const code = args && (args.code || args);
  if (typeof code === "string") {
    try {
      return console.warn("[Dars:DAP] DO NOT USE INLINE CODE EXECUTION",);
    } catch (e) {
      console.error("[Dars:DAP] Error executing inline code:", e);
    }
  }
});
_registerCommand("change", (args) => change(args));
_registerCommand("navigate", (args) => {
  const url = args.path || args;
  if (typeof url === "string" && /^\s*javascript\s*:/i.test(url)) {
    console.warn("[Dars:Security] Blocked javascript: URI in navigate");
    return;
  }
  // Prefer SPA navigation if the router is available (avoids full page reload)
  if (typeof window.navigateTo === "function") {
    window.navigateTo(url);
  } else {
    window.location.href = url;
  }
});
_registerCommand("navigate_new", (args) => {
  const url = args.path || args;
  if (typeof url === "string" && /^\s*javascript\s*:/i.test(url)) {
    console.warn("[Dars:Security] Blocked javascript: URI in navigate_new");
    return;
  }
  window.open(url, "_blank", "noopener,noreferrer");
});
_registerCommand("reload", () => {
  window.location.reload();
});
_registerCommand("history_back", () => {
  window.history.back();
});
_registerCommand("history_forward", () => {
  window.history.forward();
});

_registerCommand("alert", (args) => _alert(args.message || args));
_registerCommand("confirm", (args, ctx) => {
  if (confirm(args.message || args)) {
    if (args.on_ok) dispatch(args.on_ok, ctx);
  } else {
    if (args.on_cancel) dispatch(args.on_cancel, ctx);
  }
});
_registerCommand("log", (args) => console.log(args.message || args));

_registerCommand("sequence", async (args, ctx) => {
  const actions = Array.isArray(args) ? args : args.actions || [];
  for (const a of actions) {
    if (a && a.op === "delay") {
      const ms = a.args?.ms || a.ms || 0;
      await new Promise((resolve) => setTimeout(resolve, ms));
      if (a.args && a.args.action) await dispatch(a.args.action, ctx);
    } else {
      await dispatch(a, ctx);
    }
  }
});
_registerCommand("delay", (args, ctx) => {
  if (args.action) {
    setTimeout(() => dispatch(args.action, ctx), args.ms || 0);
  }
});

_registerCommand("dom_show", (args) => {
  const el = $(args.id || args);
  if (el) el.style.display = args.display || "";
});
_registerCommand("dom_hide", (args) => {
  const el = $(args.id || args);
  if (el) el.style.display = "none";
});
_registerCommand("dom_toggle", (args) => {
  const el = $(args.id || args);
  if (el)
    el.style.display =
      el.style.display === "none" ? args.display || "" : "none";
});
_registerCommand("dom_set_text", (args) => {
  let el = $(args.id);
  if (!el) el = document.querySelector(args.id);
  if (el) el.textContent = String(args.text);
});
_registerCommand("dom_set_html", (args) => {
  const el = $(args.id);
  if (el) el.innerHTML = _sanitize(String(args.html));
});
_registerCommand("dom_set_style", (args) => {
  const el = $(args.id);
  if (el && args.style) {
    for (const k in args.style) el.style[k] = args.style[k];
  }
});
_registerCommand("dom_set_value", (args) => {
  const el = $(args.id);
  if (el) el.value = args.value;
});
// Blocked attribute names that could introduce XSS via event handlers or dangerous protocols
const _BLOCKED_ATTRS = new Set([
  "onclick",
  "ondblclick",
  "onmousedown",
  "onmouseup",
  "onmouseover",
  "onmouseout",
  "onmousemove",
  "onkeydown",
  "onkeyup",
  "onkeypress",
  "onchange",
  "oninput",
  "onfocus",
  "onblur",
  "onsubmit",
  "onreset",
  "onselect",
  "onload",
  "onunload",
  "onerror",
  "onabort",
  "onresize",
  "onscroll",
  "oncontextmenu",
  "ondrag",
  "ondragend",
  "ondragenter",
  "ondragleave",
  "ondragover",
  "ondragstart",
  "ondrop",
  "onanimationstart",
  "onanimationend",
  "ontransitionend",
  "onpointerdown",
  "onpointerup",
  "onpointermove",
  "onpointerover",
  "onpointerout",
  "onpointerenter",
  "onpointerleave",
  "onpointercancel",
  "ontouchstart",
  "ontouchend",
  "ontouchmove",
  "ontouchcancel",
  "onwheel",
  "oncopy",
  "oncut",
  "onpaste",
  "onbeforeinput",
  "onformdata",
  "oninvalid",
  "onprogress",
  "onratechange",
  "onseeked",
  "onseeking",
  "onstalled",
  "onsuspend",
  "ontimeupdate",
  "onvolumechange",
  "onwaiting",
  "oncanplay",
  "oncanplaythrough",
  "ondurationchange",
  "onemptied",
  "onended",
  "onloadeddata",
  "onloadedmetadata",
  "onloadstart",
  "onplay",
  "onplaying",
  "onpause",
  "srcdoc",
  "formaction",
  "action",
  "href",
  "src",
  "data",
  "codebase",
  "classid",
]);

_registerCommand("dom_set_attr", (args) => {
  const el = $(args.id);
  if (!el) return;
  const attrName = String(args.name).toLowerCase().trim();
  if (_BLOCKED_ATTRS.has(attrName)) {
    console.warn(
      `[Dars:Security] Blocked attempt to set dangerous attribute: "${attrName}"`,
    );
    return;
  }
  // Block javascript: protocol in any remaining attribute value
  const val = String(args.value);
  if (/^\s*javascript\s*:/i.test(val)) {
    console.warn(
      `[Dars:Security] Blocked javascript: URI in attribute "${attrName}"`,
    );
    return;
  }
  el.setAttribute(attrName, val);
});
_registerCommand("dom_remove_attr", (args) => {
  const el = $(args.id);
  if (el) el.removeAttribute(args.name);
});
_registerCommand("dom_focus", (args) => {
  const el = $(args.id || args);
  if (el) el.focus();
});
_registerCommand("dom_blur", (args) => {
  const el = $(args.id || args);
  if (el) el.blur();
});

_registerCommand("class_add", (args) => {
  const el = $(args.id);
  if (el) el.classList.add(args.className);
});
_registerCommand("class_remove", (args) => {
  const el = $(args.id);
  if (el) el.classList.remove(args.className);
});
_registerCommand("class_toggle", (args) => {
  const el = $(args.id);
  if (el) el.classList.toggle(args.className);
});

_registerCommand("scroll_to", (args) => {
  window.scrollTo({
    top: args.y || 0,
    left: args.x || 0,
    behavior: args.behavior || "auto",
  });
});
_registerCommand("scroll_top", (args) => {
  window.scrollTo({ top: 0, behavior: args.behavior || "smooth" });
});
_registerCommand("scroll_bottom", (args) => {
  window.scrollTo({
    top: document.body.scrollHeight,
    behavior: args.behavior || "smooth",
  });
});
_registerCommand("scroll_to_element", (args) => {
  const el = $(args.id || args);
  if (el) el.scrollIntoView({ behavior: args.behavior || "smooth" });
});

_registerCommand("form_submit", (args) => {
  const el = $(args.id || args);
  if (el && el.tagName === "FORM") el.submit();
});
_registerCommand("form_reset", (args) => {
  const el = $(args.id || args);
  if (el && el.tagName === "FORM") el.reset();
});
_registerCommand("input_clear", (args) => {
  const el = $(args.id || args);
  if (el) {
    el.value = "";
    el.dispatchEvent(new Event("input", { bubbles: true }));
  }
});

_registerCommand("storage_set", (args) => {
  localStorage.setItem(args.key, String(args.value));
});
_registerCommand("storage_remove", (args) => {
  localStorage.removeItem(args.key);
});
_registerCommand("storage_clear", () => {
  localStorage.clear();
});

_registerCommand("modal_show", (args) => {
  if (window.DarsModal) window.DarsModal.show(args.id || args);
});
_registerCommand("modal_hide", (args) => {
  if (window.DarsModal) window.DarsModal.hide(args.id || args);
});

_registerCommand("clipboard_write", (args) => {
  navigator.clipboard.writeText(String(args.text || args));
});
_registerCommand("clipboard_copy_element", (args) => {
  const el = $(args.id || args);
  if (el) navigator.clipboard.writeText(el.textContent || "");
});

_registerCommand("comp_create", (args) => {
  if (typeof createComponent === "function")
    createComponent(args.root_id, args.vdom, args.position);
});
_registerCommand("comp_delete", (args) => {
  const el = $(args.id || args);
  if (el && el.parentNode) el.parentNode.removeChild(el);
});
_registerCommand("storage_get", (args) => {
  const val = localStorage.getItem(args.key);
  if (args.target_state) {
    change({ id: args.target_id, [args.target_prop]: val });
  }
});

_registerCommand("dom_reflow", (args) => {
  const el = $(args.id || args);
  if (el) void el.offsetWidth;
});

_registerCommand("dom_animate", (args) => {
  const el = $(args.id);
  if (el && args.keyframes) el.animate(args.keyframes, args.options || {});
});

_registerCommand("conditional", async (args, ctx) => {
  // Resolve the condition — it may be a DAP expression (bool_expr, transform, etc.)
  let result = false;
  try {
    const resolved = await _resolveVal(args.condition, ctx);
    result = Boolean(resolved);
  } catch (_) {
    result = false;
  }

  if (result) {
    if (args.on_true) await dispatch(args.on_true, ctx);
  } else {
    if (args.on_false) await dispatch(args.on_false, ctx);
  }
});

_registerCommand("comp_update", (args) => change(args));

_registerCommand("fetch", async (args, ctx) => {
  try {
    // Resolve relative URLs against backendUrl.
    // When backendUrl is "/" or empty, keep the URL as-is (same-origin).
    let fetchUrl = args.url;
    if (fetchUrl && !/^https?:\/\//i.test(fetchUrl)) {
      const base =
        (window.__DARS_SPA_CONFIG__ && window.__DARS_SPA_CONFIG__.backendUrl) ||
        "";
      if (base && base !== "/") fetchUrl = base.replace(/\/$/, "") + fetchUrl;
    }
    const resp = await fetch(fetchUrl, args.options || {});
    const data = await resp.json();
    if (args.on_success) {
      // Prevent server responses from injecting inline JS ops via on_success dispatch
      // on_success must be a compile-time DAP action, not data from the response
      dispatch(args.on_success, { ...ctx, response: data });
    }
  } catch (e) {
    if (args.on_error) dispatch(args.on_error, { ...ctx, error: String(e) });
  }
});

async function _resolveVal(val, ctx) {
  if (val && typeof val === "object" && val.op) {
    // collect_values: resolve each field value and return a plain object
    if (val.op === "collect_values") {
      const result = {};
      const fieldArgs = val.args || {};
      for (const [key, expr] of Object.entries(fieldArgs)) {
        result[key] = await _resolveVal(expr, ctx);
      }
      return result;
    }
    return await dispatch(val, ctx);
  }
  return val;
}

_registerCommand("get_dom_value", (args) => {
  const el = document.querySelector(args.selector);
  if (!el) return null;
  if (
    el.tagName === "INPUT" ||
    el.tagName === "TEXTAREA" ||
    el.tagName === "SELECT"
  ) {
    if (el.type === "checkbox" || el.type === "radio")
      return el.checked ? true : false;
    return el.value;
  }
  return el.textContent;
});

_registerCommand("get_state_value", (args) => {
  const st = __registry.get(args.state_id);
  if (st && st.values) return st.values[args.prop_name];
  return null;
});

_registerCommand("get_context_value", (args, ctx) => {
  if (!ctx) return null;
  const key = args.key;
  // Support dotted paths like "response.user.username"
  if (key && key.includes(".")) {
    let val = ctx;
    for (const part of key.split(".")) {
      if (val == null || typeof val !== "object") return null;
      val = val[part];
    }
    return val !== undefined ? val : null;
  }
  return ctx[key] !== undefined ? ctx[key] : null;
});

_registerCommand("transform", async (args, ctx) => {
  const input = await _resolveVal(args.input, ctx);
  if (args.method === "int") return parseInt(input, 10);
  if (args.method === "float") return parseFloat(input);
  if (args.method === "upper") return String(input).toUpperCase();
  if (args.method === "lower") return String(input).toLowerCase();
  if (args.method === "trim") return String(input == null ? "" : input).trim();
  if (args.method === "length")
    return String(input == null ? "" : input).trim().length;
  if (args.method === "is_email") {
    const s = String(input == null ? "" : input).trim();
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(s);
  }
  if (args.method === "test_pattern") {
    try {
      return new RegExp(args.pattern).test(String(input == null ? "" : input));
    } catch (_) {
      return false;
    }
  }
  if (args.method === "json_stringify") {
    // Return the object itself — network_request will JSON.stringify it
    // Returning the raw object avoids double-encoding
    return input;
  }
  if (args.method === "validate_operator")
    return ["+", "-", "*", "/", "%", "**"].includes(input) ? input : "+";
  // Render a tasks API response {tasks: [...]} as HTML list items
  if (args.method === "tasks_to_html") {
    try {
      const data = typeof input === "string" ? JSON.parse(input) : input;
      const tasks =
        Array.isArray(data) ? data
          : data && data.tasks ? data.tasks
            : [];
      if (!tasks.length)
        return '<p class="text-gray-400 text-sm p-2">No tasks yet.</p>';
      return tasks
        .map((t) => {
          // Safely extract title — handle string, number, or nested object
          let title = "";
          if (t && t.title !== undefined && t.title !== null) {
            title =
              typeof t.title === "object" ?
                JSON.stringify(t.title)
                : String(t.title);
          }
          const safeTitle = _sanitize(title);
          const done = t && t.done;
          const id = t && t.id ? t.id : "";
          return `<div class="flex items-center gap-2 p-2 border rounded mb-1 bg-white">
          <span class="flex-1 ${done ? "line-through text-gray-400" : ""}">${safeTitle || '<em class="text-gray-300">untitled</em>'}</span>
          <span class="text-xs text-gray-400">#${id}</span>
        </div>`;
        })
        .join("");
    } catch (e) {
      return `<p class="text-red-400 text-sm">Error rendering tasks: ${e.message}</p>`;
    }
  }
  return input;
});

_registerCommand("math_expr", async (args, ctx) => {
  const left = parseFloat(await _resolveVal(args.left, ctx)) || 0;
  const right = parseFloat(await _resolveVal(args.right, ctx)) || 0;
  const op = await _resolveVal(args.operator, ctx);
  if (op === "+") return left + right;
  if (op === "-") return left - right;
  if (op === "*") return left * right;
  if (op === "/") return left / right;
  if (op === "%") return left % right;
  if (op === "**") return left ** right;
  return 0;
});

_registerCommand("bool_expr", async (args, ctx) => {
  const left = await _resolveVal(args.left, ctx);
  const right = await _resolveVal(args.right, ctx);
  const op = args.operator;
  if (op === "==") return left == right;
  if (op === "!=") return left != right;
  if (op === ">") return left > right;
  if (op === "<") return left < right;
  if (op === ">=") return left >= right;
  if (op === "<=") return left <= right;
  if (op === "&&") return Boolean(left) && Boolean(right);
  if (op === "||") return Boolean(left) || Boolean(right);
  return false;
});

_registerCommand("cond_expr", async (args, ctx) => {
  const cond = await _resolveVal(args.condition, ctx);
  if (cond) return await _resolveVal(args.true_val, ctx);
  return await _resolveVal(args.false_val, ctx);
});

_registerCommand("vref_update", async (args, ctx) => {
  const val = await _resolveVal(args.value, ctx);
  const selector = args.selector;

  // 1. Update global vref registry
  if (
    window.__DARS_VREF_VALUES__ &&
    typeof selector === "string" &&
    selector in window.__DARS_VREF_VALUES__
  ) {
    window.__DARS_VREF_VALUES__[selector] = val;
  }

  // 2. Update DOM elements directly bound to this selector
  if (typeof selector === "string") {
    const els = document.querySelectorAll(selector);
    els.forEach((el) => {
      if (el.tagName === "INPUT" || el.tagName === "TEXTAREA") {
        if (el.type === "checkbox" || el.type === "radio") {
          el.checked = Boolean(val);
        } else {
          el.value = val;
        }
      } else if (el.tagName === "SELECT") {
        el.value = val;
      } else {
        // Only update textContent for elements that are NOT managed by a useVRef binding
        if (!el.hasAttribute("data-vref")) {
          el.textContent = typeof val === "object" && val !== null ? JSON.stringify(val, null, 2) : val;
        }
      }
    });

    // 3. Legacy lifecycle hook
    if (typeof updateVRef === "function") updateVRef(selector);
  }

  // 4. Re-evaluate all useVRef bindings that depend on this selector.
  //    A binding with an empty dependencies array is always re-evaluated
  //    (conservative fallback for expressions we couldn't statically analyse).
  if (
    window.__DARS_VREF_BINDINGS__ &&
    window.__DARS_VREF_BINDINGS__.length > 0
  ) {
    for (const binding of window.__DARS_VREF_BINDINGS__) {
      if (!binding.elements || binding.elements.length === 0) continue;

      const deps = binding.dependencies || [];
      // Only re-evaluate if this binding explicitly depends on the updated selector.
      // Bindings with empty dependencies (e.g. static values) never update.
      const shouldUpdate =
        typeof selector === "string" && deps.includes(selector);

      if (shouldUpdate) {
        try {
          const newVal = await binding.vexpr();
          const strVal =
            newVal !== null && newVal !== undefined
              ? (typeof newVal === "object" ? JSON.stringify(newVal, null, 2) : String(newVal))
              : "";
          binding.elements.forEach((el) => {
            el.textContent = strVal;
          });
          // Fire callbacks after the DOM is updated
          if (typeof binding.callbacks === "function") {
            await binding.callbacks();
          }
        } catch (e) {
          console.error("[Dars VRef] Error re-evaluating binding:", e);
        }
      }
    }
  }
});

_registerCommand("vref_get", async (args, ctx) => {
  let val = null;
  if (
    window.__DARS_VREF_VALUES__ &&
    args.selector in window.__DARS_VREF_VALUES__
  ) {
    val = window.__DARS_VREF_VALUES__[args.selector];
  } else {
    // Fallback to DOM
    val = await dispatch(
      { op: "get_dom_value", args: { selector: args.selector } },
      ctx,
    );
  }
  if (args.target_id) change({ id: args.target_id, [args.target_prop]: val });
  return val;
});

_registerCommand("input_set", (args) => {
  const el = $(args.id);
  if (el) {
    el.value = args.value;
    el.dispatchEvent(new Event("input", { bubbles: true }));
  }
});

_registerCommand("animate", (args) => {
  const el = $(args.id);
  if (el && window.Dars && window.Dars.animate) window.Dars.animate(args);
});
// dom_set_html: async so it can resolve DAP expressions in the html arg
_registerCommand("dom_set_html", async (args, ctx) => {
  const el = $(args.id);
  if (!el) return;
  const html = await _resolveVal(args.html, ctx);
  el.innerHTML = _sanitize(String(html || ""));
});

// ==================== NETWORK & VREF UTILITIES ====================

/**
 * vref_set — set a named VRef to a value (alias for vref_update with a direct value).
 * args: { selector: string, value: any }
 */
_registerCommand("vref_set", async (args, ctx) => {
  return dispatch({ op: "vref_update", args }, ctx);
});

/**
 * storage_get_to_vref — read a localStorage key and store it in a VRef.
 * args: { storage_key: string, selector: string }
 */
_registerCommand("storage_get_to_vref", async (args, ctx) => {
  const val = localStorage.getItem(args.storage_key);
  return dispatch(
    { op: "vref_update", args: { selector: args.selector, value: val } },
    ctx,
  );
});

/**
 * network_request — async fetch with loading-state management, interceptor
 * chain, on_success / on_error callbacks, and 401 interception.
 *
 * args:
 *   url          string
 *   method       string  (default "GET")
 *   headers      object  (optional)
 *   body         any     (optional, auto-stringified if object)
 *   loading_selector  string  (optional VRef selector set to true/false)
 *   data_selector     string  (optional VRef selector for response data)
 *   error_selector    string  (optional VRef selector for error message)
 *   on_success    DAP action  (optional, dispatched after data_selector is set)
 *   on_error      DAP action  (optional, dispatched after error_selector is set)
 */
_registerCommand("network_request", async (args, ctx) => {
  const {
    url,
    method = "GET",
    headers = {},
    body,
    loading_selector,
    data_selector,
    error_selector,
    on_success,
    on_error,
  } = args;

  // Resolve relative URLs against the configured backend URL.
  // In fullstack/SSR mode the SPA config carries backendUrl (e.g. "http://localhost:3000").
  // When backendUrl is "/" or empty, the URL is already relative to the current origin —
  // do NOT prepend anything (avoids "//api/tasks" double-slash issues).
  function _resolveUrl(rawUrl) {
    if (!rawUrl) return rawUrl;
    if (/^https?:\/\//i.test(rawUrl)) return rawUrl; // already absolute
    const base =
      (window.__DARS_SPA_CONFIG__ && window.__DARS_SPA_CONFIG__.backendUrl) ||
      "";
    // Only prepend if base is a real origin (not empty, not "/")
    if (base && base !== "/") {
      return base.replace(/\/$/, "") + rawUrl;
    }
    return rawUrl; // relative URL — browser resolves against current origin
  }

  const resolvedUrl = _resolveUrl(url);

  // Set loading state
  if (loading_selector) {
    dispatch(
      { op: "vref_update", args: { selector: loading_selector, value: true } },
      ctx,
    );
  }

  try {
    const resolvedUrlIsCrossOrigin = resolvedUrl &&
      (resolvedUrl.startsWith("http://") || resolvedUrl.startsWith("https://")) &&
      !resolvedUrl.startsWith(window.location.origin);
    const fetchConfig = {
      method: method.toUpperCase(),
      headers: { ...headers },
      credentials: resolvedUrlIsCrossOrigin ? "include" : "same-origin",
    };

    // Inject auth token if present
    const token = localStorage.getItem("dars_auth_token");
    if (token && !fetchConfig.headers["Authorization"]) {
      fetchConfig.headers["Authorization"] = "Bearer " + token;
    }

    // Inject CSRF token for cookie-based auth (state-changing methods)
    const statefulMethods = ["POST", "PUT", "DELETE", "PATCH"];
    if (statefulMethods.includes(fetchConfig.method)) {
      // Read XSRF-TOKEN from document.cookie (works same-origin; cross-origin dev
      // won't have it — server should skip CSRF check for such requests)
      const m = document.cookie.match(/\bXSRF-TOKEN=([^;]+)/);
      if (m && !fetchConfig.headers["X-XSRF-TOKEN"]) {
        fetchConfig.headers["X-XSRF-TOKEN"] = m[1];
      }
    }

    if (body !== undefined && body !== null) {
      // If body is a DAP expression (has 'op'), resolve it first to get the actual value
      let resolvedBody = body;
      if (body && typeof body === "object" && body.op) {
        resolvedBody = await _resolveVal(body, ctx);
      }
      if (resolvedBody && typeof resolvedBody === "object") {
        fetchConfig.body = JSON.stringify(resolvedBody);
        if (!fetchConfig.headers["Content-Type"]) {
          fetchConfig.headers["Content-Type"] = "application/json";
        }
      } else if (resolvedBody !== undefined && resolvedBody !== null) {
        fetchConfig.body = String(resolvedBody);
      }
    }

    const resp = await fetch(resolvedUrl, fetchConfig);

    // Handle 401 — clear auth token, surface error, redirect to login
    if (resp.status === 401) {
      localStorage.removeItem("dars_auth_token");
      const errMsg = "Unauthorized (401)";
      if (loading_selector) {
        dispatch(
          {
            op: "vref_update",
            args: { selector: loading_selector, value: false },
          },
          ctx,
        );
      }
      if (error_selector) {
        dispatch(
          {
            op: "vref_update",
            args: { selector: error_selector, value: errMsg },
          },
          ctx,
        );
      }
      if (on_error) dispatch(on_error, { ...ctx, error: errMsg });
      // Redirect to login (SPA nav if possible, otherwise full reload)
      // but only if we are NOT already on the login page, to avoid redirect loops.
      const _loginPath =
        (window.__DARS_SPA_CONFIG__ && window.__DARS_SPA_CONFIG__.loginPath) ||
        "/login";
      const _currentPath = window.location.pathname.replace(/\/$/, "") || "/";
      const _targetPath = _loginPath.replace(/\/$/, "") || "/";
      if (_currentPath !== _targetPath) {
        dispatch({ op: "navigate_to_login" });
      }
      return;
    }

    let data;
    const contentType = resp.headers.get("content-type") || "";
    if (contentType.includes("application/json")) {
      data = await resp.json();
    } else {
      data = await resp.text();
    }

    if (!resp.ok) {
      throw new Error(`HTTP ${resp.status}: ${resp.statusText}`);
    }

    if (loading_selector) {
      dispatch(
        {
          op: "vref_update",
          args: { selector: loading_selector, value: false },
        },
        ctx,
      );
    }
    if (data_selector) {
      dispatch(
        { op: "vref_update", args: { selector: data_selector, value: data } },
        ctx,
      );
    }
    if (on_success) dispatch(on_success, { ...ctx, response: data });
  } catch (e) {
    const errMsg = e && e.message ? e.message : String(e);
    if (loading_selector) {
      dispatch(
        {
          op: "vref_update",
          args: { selector: loading_selector, value: false },
        },
        ctx,
      );
    }
    if (error_selector) {
      dispatch(
        {
          op: "vref_update",
          args: { selector: error_selector, value: errMsg },
        },
        ctx,
      );
    }
    if (on_error) dispatch(on_error, { ...ctx, error: errMsg });
  }
});

// ==================== AUTH & NAVIGATION COMMANDS ====================

/**
 * navigate_to_login — redirect to login page, preserving current path as redirect.
 * Args: { redirect?: string  (optional, overrides default login path) }
 */
_registerCommand("navigate_to_login", (args, ctx) => {
  const redirectPath = args && args.redirect ? args.redirect : undefined;
  const loginPath = redirectPath || "/login";
  const _currentPath = window.location.pathname.replace(/\/$/, "") || "/";
  const _targetLoginPath = loginPath.replace(/\/$/, "") || "/";
  // Avoid redirect loop — already on login page
  if (_currentPath === _targetLoginPath) return;
  if (typeof window.navigateToLogin === "function") {
    window.navigateToLogin(redirectPath);
  } else {
    const target = _currentPath !== "/"
      ? loginPath + "?redirect=" + encodeURIComponent(_currentPath)
      : loginPath;
    window.location.href = target;
  }
});

/**
 * redirect_after_login — navigate to the URL specified in ?redirect= query param.
 * The redirect may include a path + query string (e.g. "/products?sort=asc").
 * If no redirect param is set, navigates to the given fallback (default "/").
 * Args: { fallback?: string }
 */
_registerCommand("redirect_after_login", (args) => {
  let target = "/";
  try {
    const params = new URLSearchParams(window.location.search);
    const raw = params.get("redirect");
    target = raw ? decodeURIComponent(raw) : (args && args.fallback ? args.fallback : "/");
  } catch (_) {
    target = args && args.fallback ? args.fallback : "/";
  }
  if (typeof window.navigateTo === "function") {
    window.navigateTo(target);
  } else {
    window.location.href = target;
  }
});

// ==================== CONDITIONAL & LIST RENDERING ====================

/**
 * _initConditionalElements — scan the DOM for data-dap-show and data-dap-if
 * elements and evaluate their initial state. Also patches vref_update to
 * re-evaluate conditionals when a VRef changes.
 */
async function _initConditionalElements(ctx) {
  // Initialize Show elements
  for (const el of document.querySelectorAll("[data-dap-show]")) {
    try {
      // Attribute may have &quot; encoded quotes — decode before parsing
      const raw = el.getAttribute("data-dap-show").replace(/&quot;/g, '"');
      const condAction = JSON.parse(raw);
      const cond = await _resolveVal(condAction, ctx || {});
      el.style.display = cond ? "" : "none";
    } catch (_) { }
  }
  // Initialize If elements
  for (const el of document.querySelectorAll("[data-dap-if]")) {
    try {
      const raw = el.getAttribute("data-dap-if").replace(/&quot;/g, '"');
      const condAction = JSON.parse(raw);
      const cond = await _resolveVal(condAction, ctx || {});
      const thenEl = el.querySelector('[data-if-branch="then"]');
      const elseEl = el.querySelector('[data-if-branch="else"]');
      if (thenEl) thenEl.style.display = cond ? "" : "none";
      if (elseEl) elseEl.style.display = cond ? "none" : "";
    } catch (_) { }
  }
}

// _initConditionalElements is called by the vref_update patch below
// and also exported so _darsInit can call it after VRef setup.
export { _initConditionalElements };

/**
 * render_tasks — render a tasks API response into a container element.
 * args: { container_id: string }
 * ctx.response must be the API response: { tasks: [...] } or [...]
 */
_registerCommand("render_tasks", (args, ctx) => {
  const el = $(args.container_id || "task-list");
  if (!el) return;
  try {
    const data = ctx && ctx.response ? ctx.response : {};
    const tasks = Array.isArray(data) ? data : data.tasks || [];
    if (!tasks.length) {
      el.innerHTML = '<p class="text-gray-400 text-sm p-2">No tasks yet.</p>';
      return;
    }
    el.innerHTML = tasks
      .map((t) => {
        const title = _sanitize(String(t.title || ""));
        const done = t.done ? "line-through text-gray-400" : "";
        return `<div class="flex items-center gap-2 p-2 border rounded mb-1 bg-white shadow-sm">
        <span class="flex-1 ${done}">${title || "<em class='text-gray-300'>untitled</em>"}</span>
        <span class="text-xs text-gray-400 ml-2">#${t.id || ""}</span>
      </div>`;
      })
      .join("");
  } catch (e) {
    el.innerHTML = `<p class="text-red-400 text-sm p-2">Error: ${e.message}</p>`;
  }
});

// Patch vref_update to re-evaluate conditionals AND re-render Each lists after every VRef change
const _origVrefUpdate = __commandRegistry.get("vref_update");
if (_origVrefUpdate) {
  __commandRegistry.set("vref_update", async (args, ctx) => {
    const result = await _origVrefUpdate(args, ctx);
    // Re-evaluate all conditional elements after any VRef change
    await _initConditionalElements(ctx);
    // Re-render any Each containers bound to this selector
    if (args && args.selector) {
      const sel = args.selector;
      for (const container of document.querySelectorAll("[data-dap-each]")) {
        try {
          const containerSel = container.getAttribute("data-dap-each");
          if (containerSel === sel && container.id) {
            await dispatch(
              { op: "dom_each_render", args: { id: container.id } },
              ctx,
            );
          }
        } catch (_) { }
      }
    }
    return result;
  });
}

/**
 * dom_if_toggle — evaluate a DAP condition and show/hide If branches.
 * args: { id: wrapperId }
 * Reads data-dap-if (JSON condition), evaluates it, then shows/hides
 * the data-if-branch="then" and data-if-branch="else" children.
 */
_registerCommand("dom_if_toggle", async (args, ctx) => {
  const wrapper = $(args.id);
  if (!wrapper) return;
  const rawAttr = wrapper.getAttribute("data-dap-if");
  if (!rawAttr) return;
  let cond;
  try {
    const condAction = JSON.parse(rawAttr.replace(/&quot;/g, '"'));
    cond = await _resolveVal(condAction, ctx);
  } catch (_) {
    return;
  }
  const thenEl = wrapper.querySelector('[data-if-branch="then"]');
  const elseEl = wrapper.querySelector('[data-if-branch="else"]');
  if (thenEl) thenEl.style.display = cond ? "" : "none";
  if (elseEl) elseEl.style.display = cond ? "none" : "";
});

/**
 * dom_show_toggle — evaluate a DAP condition and show/hide a Show wrapper.
 * args: { id: wrapperId }
 * Reads data-dap-show (JSON condition) and calls dom_show / dom_hide.
 */
_registerCommand("dom_show_toggle", async (args, ctx) => {
  const wrapper = $(args.id);
  if (!wrapper) return;
  const rawAttr = wrapper.getAttribute("data-dap-show");
  if (!rawAttr) return;
  let cond;
  try {
    const condAction = JSON.parse(rawAttr.replace(/&quot;/g, '"'));
    cond = await _resolveVal(condAction, ctx);
  } catch (_) {
    return;
  }
  wrapper.style.display = cond ? "" : "none";
});

/**
 * dom_each_render — re-render a list container from a VRef JSON array.
 * args: { id: containerId }
 * Reads data-dap-each (VRef selector), fetches the current array value,
 * and rebuilds the container's children using the data-each-template HTML
 * with __item_<field>__ placeholder substitution.
 */
_registerCommand("dom_each_render", async (args, ctx) => {
  const container = $(args.id);
  if (!container) return;
  const selector = container.getAttribute("data-dap-each");
  if (!selector) return;

  // Resolve the current array value from the VRef registry or DOM
  let items = null;
  if (window.__DARS_VREF_VALUES__ && selector in window.__DARS_VREF_VALUES__) {
    items = window.__DARS_VREF_VALUES__[selector];
  }

  // Support response objects like { tasks: [...] } — unwrap common array keys
  if (items && !Array.isArray(items) && typeof items === "object") {
    const keys = ["tasks", "items", "data", "results", "list", "rows"];
    for (const k of keys) {
      if (Array.isArray(items[k])) {
        items = items[k];
        break;
      }
    }
  }

  if (!Array.isArray(items)) {
    container.innerHTML = "";
    return;
  }

  // Get the HTML template with __item_<field>__ placeholders
  const templateEncoded = container.getAttribute("data-each-template") || "";
  const template = templateEncoded
    .replace(/&quot;/g, '"')
    .replace(/&#39;/g, "'")
    .replace(/&amp;/g, "&");

  if (!template) {
    // Fallback: plain text rendering
    container.innerHTML = items
      .map((item) => {
        const text = _sanitize(
          String(
            item && typeof item === "object" ?
              (item.title ??
                item.name ??
                item.label ??
                item.value ??
                item.text ??
                JSON.stringify(item))
              : item,
          ),
        );
        return `<div>${text}</div>`;
      })
      .join("");
    return;
  }

  // Render each item by substituting placeholders in the template
  const rendered = items
    .map((item) => {
      if (item === null || item === undefined) return "";
      let html = template;

      if (typeof item === "object") {
        // Normalize empty/unknown title values before substitution
        if (item.title !== undefined) {
          const t = String(item.title || "").trim();
          item = {
            ...item,
            title:
              (
                t === "" ||
                t.toLowerCase() === "unknown" ||
                t.toLowerCase() === "null" ||
                t.toLowerCase() === "none"
              ) ?
                "Unknown"
                : t,
          };
        }
        // Inject a done_class placeholder value based on the done field
        const doneClass = item.done ? "line-through text-gray-400" : "";
        item = { ...item, done_class: doneClass };

        // Replace __item_<field>__ with the sanitized field value
        for (const [key, val] of Object.entries(item)) {
          const placeholder = `__item_${key}__`;
          // Don't sanitize class names — they're safe strings we control
          const safeVal =
            key === "done_class" ?
              String(val)
              : _sanitize(String(val == null ? "" : val));
          html = html.split(placeholder).join(safeVal);
        }
      } else {
        // Scalar item — replace generic __item_value__ placeholder
        const safeVal = _sanitize(String(item));
        html = html.split("__item_value__").join(safeVal);
      }

      // Remove any unreplaced sentinel placeholders
      html = html.replace(/__item_[a-zA-Z0-9_]+__/g, "");
      return html;
    })
    .join("");

  container.innerHTML = rendered;
});

// ══════════════════════════════════════════════════════════════════════
// Server Action — calls a Python backend function via POST /api/actions/:name
// ══════════════════════════════════════════════════════════════════════
_registerCommand("call_server", async (args, ctx) => {
  const actionName = args.name || args.action;
  if (!actionName) {
    console.error("[Dars:DAP] call_server requires 'name' or 'action'");
    return null;
  }
  const payload = args.params || args.args || {};
  const onSuccess = args.on_success || args.onSuccess || null;
  const onError = args.on_error || args.onError || null;

  try {
    // Resolve backend URL from SPA config or darsConfig
    const backendUrl =
      (window.__DARS_SPA_CONFIG__ && window.__DARS_SPA_CONFIG__.backendUrl) ||
      __darsConfig.backendUrl ||
      "";
    const baseUrl = backendUrl ? backendUrl.replace(/\/+$/, "") : "";
    const res = await fetch(`${baseUrl}/api/actions/${actionName}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      credentials: "same-origin",
      body: JSON.stringify(payload),
    });
    if (res.status === 401) {
      // Auth required — trigger login redirect
      if (onError) await dispatch(onError, { ...ctx, error: { status: 401 } });
      dispatch({ op: "navigate_to_login" });
      return null;
    }

    if (!res.ok) {
      const err = await res.json().catch(() => ({ error: res.statusText }));
      console.error(`[Dars:DAP] Server action '${actionName}' failed:`, err);
      if (onError) await dispatch(onError, { ...ctx, error: err });
      return null;
    }
    const data = await res.json();
    if (onSuccess) await dispatch(onSuccess, { ...ctx, response: data });
    return data;
  } catch (e) {
    console.error(`[Dars:DAP] Server action '${actionName}' network error:`, e);
    if (onError) await dispatch(onError, { ...ctx, error: String(e) });
    return null;
  }
});
