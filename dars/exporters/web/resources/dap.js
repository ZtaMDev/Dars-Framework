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
_registerCommand("change", (args) => change(args));
_registerCommand("navigate", (args) => {
  const url = args.path || args;
  if (typeof url === "string" && /^\s*javascript\s*:/i.test(url)) {
    console.warn("[Dars:Security] Blocked javascript: URI in navigate");
    return;
  }
  window.location.href = url;
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

_registerCommand("sequence", (args, ctx) => {
  const actions = Array.isArray(args) ? args : args.actions || [];
  for (const a of actions) {
    if (a && a.op === "delay") {
      const ms = a.args?.ms || a.ms || 0;
      setTimeout(() => dispatch(a.args.action, ctx), ms);
    } else {
      dispatch(a, ctx);
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
  const el = $(args.id);
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
  "onclick","ondblclick","onmousedown","onmouseup","onmouseover","onmouseout",
  "onmousemove","onkeydown","onkeyup","onkeypress","onchange","oninput",
  "onfocus","onblur","onsubmit","onreset","onselect","onload","onunload",
  "onerror","onabort","onresize","onscroll","oncontextmenu","ondrag",
  "ondragend","ondragenter","ondragleave","ondragover","ondragstart","ondrop",
  "onanimationstart","onanimationend","ontransitionend","onpointerdown",
  "onpointerup","onpointermove","onpointerover","onpointerout","onpointerenter",
  "onpointerleave","onpointercancel","ontouchstart","ontouchend","ontouchmove",
  "ontouchcancel","onwheel","oncopy","oncut","onpaste","onbeforeinput",
  "onformdata","oninvalid","onprogress","onratechange","onseeked","onseeking",
  "onstalled","onsuspend","ontimeupdate","onvolumechange","onwaiting",
  "oncanplay","oncanplaythrough","ondurationchange","onemptied","onended",
  "onloadeddata","onloadedmetadata","onloadstart","onplay","onplaying","onpause",
  "srcdoc","formaction","action","href","src","data","codebase","classid",
]);

_registerCommand("dom_set_attr", (args) => {
  const el = $(args.id);
  if (!el) return;
  const attrName = String(args.name).toLowerCase().trim();
  if (_BLOCKED_ATTRS.has(attrName)) {
    console.warn(`[Dars:Security] Blocked attempt to set dangerous attribute: "${attrName}"`);
    return;
  }
  // Block javascript: protocol in any remaining attribute value
  const val = String(args.value);
  if (/^\s*javascript\s*:/i.test(val)) {
    console.warn(`[Dars:Security] Blocked javascript: URI in attribute "${attrName}"`);
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

_registerCommand("conditional", (args, ctx) => {
  const cond = args.condition;
  // Note: conditions might still need evaluation if they are strings,
  // but in DAP they should be pre-evaluated or use a mini-DSL.
  // For now, support basic equality check if args.left/right provided.
  let result = false;
  if (args.left !== undefined && args.right !== undefined) {
    if (args.op === "==") result = args.left == args.right;
    else if (args.op === "!=") result = args.left != args.right;
    else if (args.op === ">") result = args.left > args.right;
    else if (args.op === "<") result = args.left < args.right;
  }

  if (result) {
    if (args.on_true) dispatch(args.on_true, ctx);
  } else {
    if (args.on_false) dispatch(args.on_false, ctx);
  }
});

_registerCommand("comp_update", (args) => change(args));

_registerCommand("fetch", async (args, ctx) => {
  try {
    const resp = await fetch(args.url, args.options || {});
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

_registerCommand("transform", async (args, ctx) => {
  const input = await _resolveVal(args.input, ctx);
  if (args.method === "int") return parseInt(input, 10);
  if (args.method === "float") return parseFloat(input);
  if (args.method === "upper") return String(input).toUpperCase();
  if (args.method === "lower") return String(input).toLowerCase();
  if (args.method === "validate_operator")
    return ["+", "-", "*", "/", "%", "**"].includes(input) ? input : "+";
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

  // 1. Update global vref registry if it exists
  if (
    window.__DARS_VREF_VALUES__ &&
    typeof selector === "string" &&
    selector in window.__DARS_VREF_VALUES__
  ) {
    window.__DARS_VREF_VALUES__[selector] = val;
  }

  // 2. Update DOM elements
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
        el.textContent = val;
      }
    });

    // 3. Trigger lifecycles using updateVRef
    if (typeof updateVRef === "function") updateVRef(selector);
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
_registerCommand("dom_set_html", (args) => {
  const el = $(args.id);
  if (el) el.innerHTML = _sanitize(args.html);
});
