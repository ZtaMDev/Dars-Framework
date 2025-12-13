# Dars Framework - Core Source File
#
# This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0.
# If a copy of the MPL was not distributed with this file, You can obtain one at
# https://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2025 ZtaDev
from dars.version import __version__, __release_url__

DARS_MIN_JS = f"""/* Dars minimal runtime script */
const DARS_VERSION = '{__version__}';
const DARS_RELEASE_URL = '{__release_url__}';

const __registry = new Map();
const __vdom = new Map();
const __lifecycle = new Map(); // id -> lifecycle info (onMount/onUpdate/onUnmount)

// Centralized eval helper with optional global error reporting hook
function _safeEval(code, ctx){{
  if (code == null) return;
  try {{
    return (0,eval)(code);
  }} catch (err) {{
    try {{ console.error('[Dars] Eval error:', err); }} catch(_ ){{}}
    try {{
      const D = (globalThis && globalThis.Dars) || (typeof window!=='undefined' ? window.Dars : null);
      if (D && typeof D.onError === 'function') {{
        D.onError(err, Object.assign({{ code: String(code) }}, ctx || {{}}));
      }}
    }} catch(_ ){{}}
  }}
}}

function $(id){{ return document.getElementById(id) || document.querySelector(`[data-id="${{id}}"]`) || null; }}

// Alert helper (non-fatal)
function _alert(msg){{ try{{ alert(String(msg)); }}catch(_ ){{ try{{ console.error(String(msg)); }}catch(_ ){{ }} }} }}

// CSS.escape fallback
function _cssEscape(s){{
  try{{ if (globalThis.CSS && typeof CSS.escape==='function') return CSS.escape(String(s)); }}catch(_ ){{ }}
  try{{ return String(s).replace(/[^a-zA-Z0-9_\\-]/g, '\\$&'); }}catch(_ ){{ return String(s); }}
}}

function _attachEventsForVNode(el, vnode, events, markClass){{
  try{{
    if(vnode && vnode.id && events && events[vnode.id]){{
      const evs = events[vnode.id] || {{}};
      for(const type in evs){{
        const handlers = evs[type];
        const codes = [];
        const push = (it)=>{{ if(typeof it==='string') codes.push(it); else if(it&&typeof it.code==='string') codes.push(it.code); }};
        if(Array.isArray(handlers)){{ handlers.forEach(push); }} else {{ push(handlers); }}
        if(!codes.length) continue;
        
        // Parse event type for key filtering (e.g., "keydown.Enter")
        const [baseEvent, targetKey] = type.includes('.') ? type.split('.', 2) : [type, null];
        
        el.__darsEv = el.__darsEv || {{}};
        if(el.__darsEv[type]){{ try{{ el.removeEventListener(baseEvent, el.__darsEv[type], true); }}catch(_ ){{ }} try{{ el.removeEventListener(baseEvent, el.__darsEv[type], false); }}catch(_ ){{ }} }}
        const handler = function(ev){{ 
          // Key filtering for keyboard events
          if(targetKey){{
            if(!ev || !ev.key) return; // Not a keyboard event
            if(ev.key !== targetKey && ev.code !== targetKey) return; // Wrong key
          }}
          try{{ ev.stopImmediatePropagation(); ev.stopPropagation(); ev.preventDefault(); ev.cancelBubble = true; }}catch(_ ){{ }}
          for(const c of codes){{ _safeEval(c, {{ type, event: ev, phase: 'event_handler' }}); }}
        }};
        try{{ el.addEventListener(baseEvent, handler, {{ capture: true }}); }}catch(_ ){{ }}
        el.__darsEv[type] = handler;
        try{{ if(markClass) el.classList.add(markClass); }}catch(_ ){{ }}
      }}
    }}
  }}catch(_ ){{ }}
  // Recorrer hijos VDOM y DOM en paralelo (sólo elementos)
  try{{
    const vkids = (vnode && Array.isArray(vnode.children)) ? vnode.children : [];
    let ei = 0;
    for(let i=0;i<vkids.length;i++){{
      const vk = vkids[i];
      while(ei < el.childNodes.length && el.childNodes[ei].nodeType !== 1) ei++;
      const childEl = el.childNodes[ei++];
      if(childEl) _attachEventsForVNode(childEl, vk, events, markClass);
    }}
  }}catch(_ ){{ }}
}}

// ---- Runtime helpers for dynamic create/delete ----
function _elFromVNode(v){{
  const map = {{ Text: 'span', Button: 'button', Section: 'section', Div: 'div' }};
  const tag = (v && typeof v.type === 'string') ? (map[v.type] || 'div') : 'div';
  const el = document.createElement(tag);
  try{{ if(v.id) el.id = String(v.id); }}catch(_ ){{ }}
  try{{ if(v.id) el.classList.add('dars-id-' + String(v.id)); }}catch(_ ){{ }}
  try{{ if(v.class){{ el.className = String(v.class); }} }}catch(_ ){{ }}
  try{{ if(v.style && typeof v.style === 'object'){{
    for(const k in v.style){{ try{{ el.style[k] = v.style[k]; }}catch(_ ){{}}}}
  }}}}catch(_ ){{ }}
  try{{ if(typeof v.text === 'string') el.textContent = v.text; }}catch(_ ){{ }}
  // children
  try{{ if(Array.isArray(v.children)){{
    for(const c of v.children){{ const ch = _elFromVNode(c); if(ch) el.appendChild(ch); }}
  }}}}catch(_ ){{ }}
  return el;
}}

function _walkVNode(v, fn){{
  if(!v) return; try{{ fn(v); }}catch(_ ){{ }}
  try{{ if(Array.isArray(v.children)) v.children.forEach(ch=>_walkVNode(ch, fn)); }}catch(_ ){{ }}
}}

function _storeVNode(v){{ _walkVNode(v, n=>{{ try{{ if(n && n.id) __vdom.set(String(n.id), n); }}catch(_ ){{ }} }}); }}
function _removeVNodeById(id){{ try{{ __vdom.delete(String(id)); }}catch(_ ){{ }} }}

// --- Lifecycle helpers (onMount, onUpdate, onUnmount) ---
function _registerLifecycleFromVNode(v){{
  try{{
    _walkVNode(v, n=>{{
      try{{
        if(!n || !n.id || !n.lifecycle) return;
        const id = String(n.id);
        const lc = n.lifecycle || {{}};
        const entry = __lifecycle.get(id) || {{}};
        if(lc.onMount && typeof lc.onMount.code === 'string') entry.onMount = lc.onMount.code;
        if(lc.onUpdate && typeof lc.onUpdate.code === 'string') entry.onUpdate = lc.onUpdate.code;
        if(lc.onUnmount && typeof lc.onUnmount.code === 'string') entry.onUnmount = lc.onUnmount.code;
        __lifecycle.set(id, entry);
        // Fire onMount once on registration
        if(!entry._mounted && entry.onMount && typeof entry.onMount === 'string'){{
          try{{ (0,eval)(entry.onMount); }}catch(_ ){{ }}
          entry._mounted = true;
          __lifecycle.set(id, entry);
        }}
      }}catch(_ ){{ }}
    }});
  }}catch(_ ){{ }}
}}

function _runLifecycle(id, hook){{
  try{{
    const info = __lifecycle.get(String(id));
    if(!info) return;
    let code = null;
    if(hook === 'onUpdate') code = info.onUpdate;
    else if(hook === 'onUnmount') code = info.onUnmount;
    else if(hook === 'onMount') code = info.onMount;
    if(typeof code === 'string' && code.trim()){{
      _safeEval(code, {{ hook, id }});
    }}
  }}catch(_ ){{ }}
}}

// Wrap global DarsHydrate (if present) to also register lifecycle hooks
try{{
  const _oldHydrate = globalThis.DarsHydrate;
  globalThis.DarsHydrate = function(root){{
    try{{
      const vdomRoot = (globalThis.__ROUTE_VDOM__ || globalThis.__DARS_VDOM__);
      if(vdomRoot) _registerLifecycleFromVNode(vdomRoot);
    }}catch(_ ){{ }}
    try{{
      if(typeof _oldHydrate === 'function') return _oldHydrate(root);
    }}catch(_ ){{ }}
  }};
}}catch(_ ){{ }}

function _attachEventsMap(events){{
  if(!events||typeof events!=='object') return;
  for(const cid in events){{
    try{{
      const el = $(cid); if(!el) continue;
      const evs = events[cid] || {{}};
      for(const type in evs){{
        const handlers = evs[type];
        const codes = [];
        const push = (it)=>{{ if(typeof it==='string') codes.push(it); else if(it&&typeof it.code==='string') codes.push(it.code); }};
        if(Array.isArray(handlers)){{ handlers.forEach(push); }} else {{ push(handlers); }}
        if(!codes.length) continue;
        
        // Parse event type for key filtering (e.g., "keydown.Enter")
        const [baseEvent, targetKey] = type.includes('.') ? type.split('.', 2) : [type, null];
        
        el.__darsEv = el.__darsEv || {{}};
        if(el.__darsEv[type]){{ try{{ el.removeEventListener(baseEvent, el.__darsEv[type], true); }}catch(_ ){{ }} try{{ el.removeEventListener(baseEvent, el.__darsEv[type], false); }}catch(_ ){{ }} }}
        const handler = function(ev){{ 
          // Key filtering for keyboard events
          if(targetKey){{
            if(!ev || !ev.key) return; // Not a keyboard event
            if(ev.key !== targetKey && ev.code !== targetKey) return; // Wrong key
          }}
          try{{ ev.stopImmediatePropagation(); ev.stopPropagation(); ev.preventDefault(); ev.cancelBubble = true; }}catch(_ ){{ }}
          for(const c of codes){{ try{{ (0,eval)(c); }}catch(_ ){{ }} }}
        }};
        try{{ el.addEventListener(baseEvent, handler, {{ capture: true }}); }}catch(_ ){{ }}
        el.__darsEv[type] = handler;
      }}
    }}catch(_ ){{ }}
  }}
}}

const runtime = {{
  deleteComponent(id){{
    try{{
      const el = $(id); if(!el) return;
      // Lifecycle: onUnmount before removal
      _runLifecycle(id, 'onUnmount');
      try{{ __lifecycle.delete(String(id)); }}catch(_ ){{ }}
      const parent = el.parentNode; if(parent) parent.removeChild(el);
      _removeVNodeById(id);
    }}catch(e){{ try{{ console.error(e); }}catch(_ ){{ }} }}
  }},
  createComponent(root_id, vdom_data, position){{
    try{{
      const root = $(root_id); if(!root) return;
      const el = _elFromVNode(vdom_data||{{}});
      // insert
      const pos = String(position||'append');
      if(pos==='append'){{ root.appendChild(el); }}
      else if(pos==='prepend'){{ root.insertBefore(el, root.firstChild||null); }}
      else if(pos.startsWith('before:')){{ const sid = pos.slice(7); const sib = $(sid); if(sib&&sib.parentNode){{ sib.parentNode.insertBefore(el, sib); }} else {{ root.appendChild(el); }} }}
      else if(pos.startsWith('after:')){{ const sid = pos.slice(6); const sib = $(sid); if(sib&&sib.parentNode){{ sib.parentNode.insertBefore(el, sib.nextSibling); }} else {{ root.appendChild(el); }} }}
      else {{ root.appendChild(el); }}
      // store vdom and attach events if provided
      _storeVNode(vdom_data||{{}});
      if(vdom_data && vdom_data._events){{
        // marcar y rehidratar eventos en el subárbol recién creado
        const mark = 'dars-ev-' + Math.random().toString(36).slice(2);
        try{{ el.classList.add(mark); }}catch(_ ){{ }}
        _attachEventsForVNode(el, vdom_data, vdom_data._events, mark);
      }}
      // Register lifecycle hooks (and fire onMount) for this subtree if present
      if(vdom_data && typeof vdom_data === 'object'){{
        _registerLifecycleFromVNode(vdom_data);
      }}
      // hydrate newly created subtree if available
      try{{ if(typeof window.DarsHydrate === 'function') window.DarsHydrate(el); }}catch(_ ){{ }}
    }}catch(e){{ try{{ console.error(e); }}catch(_ ){{ }} }}
  }}
}};

function registerState(name, cfg){{
  if(!name || !cfg || !cfg.id) return;
  const entry = {{
    id: cfg.id,
    states: Array.isArray(cfg.states) ? cfg.states.slice() : [],
    current: 0,
    isCustom: !!cfg.isCustom,
    rules: (cfg.rules && typeof cfg.rules === 'object') ? cfg.rules : {{}},
    defaultIndex: (typeof cfg.defaultIndex === 'number') ? cfg.defaultIndex : 0,
    defaultValue: (cfg.hasOwnProperty('defaultValue') ? cfg.defaultValue : null),
    values: (cfg.hasOwnProperty('defaultValue') ? Object.assign({{}}, cfg.defaultValue) : {{}}),
    __defaultSnapshot: null,
    __vnode: null  // Store vnode reference for event re-hydration
  }};
  __registry.set(name, entry);
  try{{
    const el = $(entry.id);
    if(el){{
      const attrs = {{}};
      try{{
        for(const a of el.getAttributeNames()) attrs[a] = el.getAttribute(a);
      }}catch(_){{ }}
      entry.__defaultSnapshot = {{ attrs, html: String(el.innerHTML||'') }};
      // Try to get vnode from __vdom for event re-hydration
      try{{ entry.__vnode = __vdom.get(entry.id); }}catch(_){{ }}
    }}
  }}catch(_){{ }}
}}

function registerStates(statesConfig) {{
  if (!Array.isArray(statesConfig)) return;
  for (const state of statesConfig) {{
    if (state && state.name && state.id) {{
      registerState(state.name, state);
    }}
  }}
}}

// If the server rendered the page with an initial state snapshot
// (window.__DARS_STATE__), register it immediately so hydration can
// reuse the existing DOM without requiring a separate static export
// pipeline.
try {{
  if (typeof window !== 'undefined' && Array.isArray(window.__DARS_STATE__)) {{
    registerStates(window.__DARS_STATE__);
  }}
}} catch(_) {{ }}

function getState(name){{ return __registry.get(name); }}

function _restoreDefault(id, snap, vnode, eventsMap){{
  try{{
    const el = $(id);
    if(!el || !snap) return;
    // Remove any dynamic event listeners we attached previously
    try{{
      if(el.__darsEv){{
        for(const t in el.__darsEv){{
          const fn = el.__darsEv[t];
          try{{ el.removeEventListener(t, fn, true); }}catch(_){{ }}
          try{{ el.removeEventListener(t, fn, false); }}catch(_){{ }}
        }}
        el.__darsEv = {{}};
      }}
    }}catch(_){{ }}
    
    // Restore attributes
    try{{
      const current = el.getAttributeNames ? el.getAttributeNames() : [];
      const booleanAttrs = ['checked', 'disabled', 'readonly', 'required', 'selected', 'autofocus', 'autoplay', 'controls', 'loop', 'muted'];
      
      // Remove all current attributes except 'id'
      for(const n of current){{ 
        if(n !== 'id') el.removeAttribute(n); 
      }}
      
      // Restore attributes from snapshot
      for(const k in snap.attrs){{ 
        if(k !== 'id'){{
          const val = snap.attrs[k];
          // Handle boolean attributes
          if(booleanAttrs.includes(k)){{
            if(val === true || val === 'true' || val === k || val === ''){{
              el.setAttribute(k, '');
              // Also set property for form elements
              if(k in el) el[k] = true;
            }} else {{
              el.removeAttribute(k);
              if(k in el) el[k] = false;
            }}
          }} else {{
            el.setAttribute(k, String(val));
          }}
        }}
      }}
      
      // CRITICAL: Ensure boolean attributes NOT in snapshot are removed and set to false
      for(const boolAttr of booleanAttrs){{
        if(!snap.attrs || !(boolAttr in snap.attrs)){{
          el.removeAttribute(boolAttr);
          if(boolAttr in el) el[boolAttr] = false;
        }}
      }}
    }}catch(_){{ }}
    
    // Restore innerHTML
    try{{ el.innerHTML = snap.html || ''; }}catch(_){{ }}
    
    // Restore value property for form elements
    try{{
      if(snap.attrs && snap.attrs.value !== undefined){{
        if(el.tagName === 'INPUT' || el.tagName === 'TEXTAREA' || el.tagName === 'SELECT'){{
          el.value = String(snap.attrs.value);
        }}
      }} else {{
        // If no value in snapshot, clear it for form elements
        if(el.tagName === 'INPUT' || el.tagName === 'TEXTAREA' || el.tagName === 'SELECT'){{
          el.value = '';
        }}
      }}
    }}catch(_){{ }}
    
    // Re-attach original event handlers from vnode if available
    try{{
      if(vnode && eventsMap){{
        _attachEventsForVNode(el, vnode, eventsMap);
      }}
    }}catch(_){{ }}
  }}catch(_){{ }}
}}

function _applyMods(defaultId, mods){{
  if(!Array.isArray(mods) || !mods.length) return;
  for(const m of mods){{
    try{{
      const op = m && m.op;
      if(!op) continue;
      const tid = (m && m.target) ? m.target : defaultId;
      const el = $(tid);
      if(!el) continue;
      if(op === 'inc' || op === 'dec'){{
        const prop = m.prop || 'text';
        const by = Number(m.by || (op==='dec'?-1:1));
        if(prop === 'text'){{
          const cur = parseFloat(el.textContent||'0') || 0;
          el.textContent = String(cur + by);
        }} else {{
          const cur = parseFloat(el.getAttribute(prop)||'0') || 0;
          el.setAttribute(prop, String(cur + by));
        }}
      }} else if(op === 'set'){{
        const attrs = m.attrs || {{}};
        for(const k in attrs){{
          try{{
            if(k === 'text') {{ el.textContent = String(attrs[k]); continue; }}
            if(k === 'html') {{ el.innerHTML = String(attrs[k]); continue; }}
            if(k.startsWith('on_')){{
              const type = k.slice(3);
              const v = attrs[k];
              const codes = [];
              
              // NUEVO: soporte para arrays de handlers
              const pushCode = (item)=>{{
                if(typeof item === 'string') codes.push(item);
                else if(item && typeof item.code === 'string') codes.push(item.code);
              }};
              
              if(Array.isArray(v)) {{
                v.forEach(pushCode);
              }} else {{
                pushCode(v);
              }}
              
              if(codes.length){{
                // Parse event type for key filtering (e.g., "keydown.Enter")
                const [baseEvent, targetKey] = type.includes('.') ? type.split('.', 2) : [type, null];
                
                el.__darsEv = el.__darsEv || {{}};
                if(el.__darsEv[type]){{
                  try{{ el.removeEventListener(baseEvent, el.__darsEv[type], true); }}catch(_){{ }}
                  try{{ el.removeEventListener(baseEvent, el.__darsEv[type], false); }}catch(_){{ }}
                }}
                const handler = function(ev){{
                  // Key filtering for keyboard events
                  if(targetKey){{
                    if(!ev || !ev.key) return; // Not a keyboard event
                    if(ev.key !== targetKey && ev.code !== targetKey) return; // Wrong key
                  }}
                  try{{ ev.stopImmediatePropagation(); }}catch(_){{ }}
                  try{{ ev.stopPropagation(); }}catch(_){{ }}
                  try{{ ev.preventDefault(); }}catch(_){{ }}
                  try{{ ev.cancelBubble = true; }}catch(_){{ }}
                  let propName = 'on'+baseEvent;
                  let prevOn = null;
                  try{{ prevOn = el[propName]; el[propName] = null; }}catch(_){{ }}
                  try{{ 
                    // NUEVO: ejecutar todos los códigos en secuencia
                    for(const c of codes){{ 
                      try{{ (new Function('event', c)).call(el, ev); }}catch(_){{ }} 
                    }} 
                  }} finally{{
                    try{{ setTimeout(()=>{{ try{{ el[propName] = prevOn; }}catch(_){{ }} }}, 0); }}catch(_){{ }}
                  }}
                }};
                try{{ el.addEventListener(baseEvent, handler, {{ capture: true }}); }}catch(_){{ }}
                el.__darsEv[type] = handler;
                continue;
              }}
            }}
            // Special handling for style to merge instead of replace
            if(k === 'style' \u0026\u0026 typeof attrs[k] === 'object'){{
              for(const styleKey in attrs[k]){{
                try{{ el.style[styleKey] = attrs[k][styleKey]; }}catch(_){{ }}
              }}
              continue;
            }}
            
            // Handle boolean attributes
            const booleanAttrs = ['checked', 'disabled', 'readonly', 'required', 'selected', 'autofocus', 'autoplay', 'controls', 'loop', 'muted'];
            let attrName = k;
            let isBooleanAttr = booleanAttrs.includes(k);
            
            // Handle is_* prefix (e.g., is_disabled -> disabled)
            if (!isBooleanAttr \u0026\u0026 k.startsWith('is_')) {{
              const unprefixed = k.substring(3);
              if (booleanAttrs.includes(unprefixed)) {{
                attrName = unprefixed;
                isBooleanAttr = true;
              }}
            }}
            
            if (isBooleanAttr) {{
              const val = attrs[k];
              if (val === true || val === 'true' || val === k || val === '') {{
                el.setAttribute(attrName, '');
                if (attrName in el) el[attrName] = true;
              }} else {{
                el.removeAttribute(attrName);
                if (attrName in el) el[attrName] = false;
              }}
            }} else {{
              el.setAttribute(k, String(attrs[k]));
            }}
          }}catch(_){{ }}
        }}
      }} else if(op === 'toggleClass'){{
        const name = m.name || '';
        const on = m.hasOwnProperty('on') ? !!m.on : null;
        if(!name) continue;
        if(on === null){{ el.classList.toggle(name); }}
        else if(on){{ el.classList.add(name); }}
        else {{ el.classList.remove(name); }}
      }} else if(op === 'appendText'){{
        el.textContent = String(el.textContent||'') + String(m.value||'');
      }} else if(op === 'prependText'){{
        el.textContent = String(m.value||'') + String(el.textContent||'');
      }} else if(op === 'call'){{
        try{{
          const payload = {{}};
          if (m.name) payload.name = String(m.name);
          if (m.id) payload.id = String(m.id);
          if (m.hasOwnProperty('state')) payload.state = m.state;
          if (m.hasOwnProperty('goto')) payload.goto = m.goto;
          if (!payload.name && !payload.id && defaultId) payload.id = String(defaultId);
          // Usar el nuevo sistema de cambio de estado que es compatible con el runtime actual
          setTimeout(()=>{{ 
            try{{ 
              if (window.Dars && typeof window.Dars.change === 'function') {{
                window.Dars.change(payload);
              }} else if (window.__DARS_CHANGE_FN) {{
                window.__DARS_CHANGE_FN(payload);
              }} else {{
                console.warn('[Dars] State change function not available');
              }}
            }}catch(_){{ }} 
          }}, 0);
        }}catch(_){{ }}
      }}
    }}catch(_){{ }}
  }}
}}

function _resolveGoto(cur, goto, statesLen){{
  if(goto == null) return cur;
  if(typeof goto === 'number') return goto;
  if(typeof goto === 'string'){{
    if(/^[\\-+]\\d+$/.test(goto)){{
      const delta = parseInt(goto, 10);
      const next = cur + delta;
      if(statesLen && statesLen > 0){{ 
        // Implement wrapping (modulo arithmetic)
        return (next % statesLen + statesLen) % statesLen;
      }}
      return next;
    }}
    const n = parseInt(goto, 10);
    if(!isNaN(n)) return n;
  }}
  return cur;
}}

// ==================== WATCHERS & HOOKS ====================
const __watchers = new Map(); // state_path -> [callbacks]

function watch(state_path, callback) {{
  if (!state_path || typeof callback !== 'function') return;
  if (!__watchers.has(state_path)) __watchers.set(state_path, []);
  __watchers.get(state_path).push(callback);
}}

function change(opt){{
  if(!opt||!opt.id) return;
  
  if(opt.useCustomRender && typeof opt.html === 'string'){{
    const el = $(opt.id);
    if(!el) return;
    el.innerHTML = opt.html;
    if(typeof window.DarsHydrate === 'function'){{ try{{ window.DarsHydrate(el); }}catch(e){{}} }}
    return;
  }}

  // Dynamic state support
  if (opt.dynamic) {{
      const el = $(opt.id);
      
      // Helper to trigger watchers for a property
      const notifyWatchers = (prop, val) => {{
          const st = __registry.get(opt.id);
          if (st && st.values) {{
              st.values[prop] = val;
          }}
          
          const path = opt.id + '.' + prop;
          if (__watchers.has(path)) {{
              __watchers.get(path).forEach(cb => {{
                  try {{ cb(val); }} catch(e) {{ console.error('[Dars] Watcher error:', e); }}
              }});
          }}
      }};

      if (el) {{
          // Apply text change
          if (opt.hasOwnProperty('text')) {{
              const isFormElement = el.tagName === 'INPUT' || el.tagName === 'TEXTAREA' || el.tagName === 'SELECT';
              if (isFormElement) {{
                  el.value = String(opt.text);
              }} else {{
                  el.textContent = String(opt.text);
              }}
              notifyWatchers('text', opt.text);
          }}
          
          // Apply HTML change
          if (opt.hasOwnProperty('html')) {{
              el.innerHTML = String(opt.html);
              notifyWatchers('html', opt.html);
          }}

          // Apply Plotly figure update
          if (opt.hasOwnProperty('figure') && window.Plotly) {{
              let figData = opt.figure;
              if (typeof figData === 'string') {{
                  try {{ figData = JSON.parse(figData); }} catch(e) {{}}
              }}
              
              if (figData) {{
                 Plotly.react(el, figData.data || [], figData.layout || {{}}, figData.config || {{}});
                 notifyWatchers('figure', figData);
              }}
          }}
          
          // Apply style changes
          if (opt.style && typeof opt.style === 'object') {{
              for (const k in opt.style) {{
                  try {{ el.style[k] = opt.style[k]; }} catch (_) {{}}
              }}
              notifyWatchers('style', opt.style);
          }}
          
          // Apply attribute changes
          if (opt.attrs && typeof opt.attrs === 'object') {{
              const booleanAttrs = ['checked', 'disabled', 'readonly', 'required', 'selected', 'autofocus', 'autoplay', 'controls', 'loop', 'muted'];
              
              for (const k in opt.attrs) {{
                  try {{
                      // Special handling for 'class'
                      if (k === 'class') {{
                          const reservedPrefixes = ['dars-', 'dars-id-', 'dars-ev-'];
                          const currentClasses = Array.from(el.classList || []);
                          const reservedClasses = currentClasses.filter(cls => 
                              reservedPrefixes.some(prefix => String(cls).startsWith(prefix))
                          );
                          const newUserClasses = String(opt.attrs[k] || '')
                              .split(' ')
                              .map(c => String(c).trim())
                              .filter(c => c.length > 0);
                          const mergedClasses = [...reservedClasses, ...newUserClasses];
                          el.className = mergedClasses.join(' ');
                      }} else {{
                          // Check if this is a boolean attribute (or has is_ prefix)
                          let attrName = k;
                          let isBooleanAttr = booleanAttrs.includes(k);
                          
                          // Handle is_* prefix (e.g., is_disabled -> disabled)
                          if (!isBooleanAttr && k.startsWith('is_')) {{
                              const unprefixed = k.substring(3); // Remove 'is_'
                              if (booleanAttrs.includes(unprefixed)) {{
                                  attrName = unprefixed;
                                  isBooleanAttr = true;
                              }}
                          }}
                          
                          if (isBooleanAttr) {{
                              // Handle boolean attributes
                              const val = opt.attrs[k];
                              // Check if value is truthy for boolean attributes
                              if (val === true || val === 'true' || val === k || val === '') {{
                                  el.setAttribute(attrName, '');
                                  // Also set property for form elements
                                  if (attrName in el) el[attrName] = true;
                              }} else if (val === false || val === 'false' || val === null || val === undefined) {{
                                  // Explicitly false values - remove attribute
                                  el.removeAttribute(attrName);
                                  if (attrName in el) el[attrName] = false;
                              }} else {{
                                  // Any other value - remove attribute (safe default)
                                  el.removeAttribute(attrName);
                                  if (attrName in el) el[attrName] = false;
                              }}
                          }} else {{
                              // Normal attribute
                              el.setAttribute(k, String(opt.attrs[k]));
                              // If it's 'value' for input, also set property
                              if (k === 'value' && (el.tagName === 'INPUT' || el.tagName === 'TEXTAREA' || el.tagName === 'SELECT')) {{
                                  el.value = String(opt.attrs[k]);
                              }}
                          }}
                      }}
                      notifyWatchers(k, opt.attrs[k]);
                  }} catch (_) {{}}
              }}
          }}
          
          // Apply class changes
          if (opt.classes && typeof opt.classes === 'object') {{
              if (opt.classes.add) {{
                  const toAdd = Array.isArray(opt.classes.add) ? opt.classes.add : [opt.classes.add];
                  toAdd.forEach(c => el.classList.add(c));
              }}
              if (opt.classes.remove) {{
                  const toRemove = Array.isArray(opt.classes.remove) ? opt.classes.remove : [opt.classes.remove];
                  toRemove.forEach(c => el.classList.remove(c));
              }}
              if (opt.classes.toggle) {{
                  const toToggle = Array.isArray(opt.classes.toggle) ? opt.classes.toggle : [opt.classes.toggle];
                  toToggle.forEach(c => el.classList.toggle(c));
              }}
              notifyWatchers('classes', opt.classes);
          }}

          // Apply event handlers
          for (const k in opt) {{
              if (k.startsWith('on_')) {{
                  const eventName = k.substring(3);
                  const code = opt[k];
                  let handler = null;
                  if (Array.isArray(code)) {{
                      handler = function(e) {{
                          code.forEach(c => {{
                              try {{ new Function('event', c).call(this, e); }} catch(err) {{ console.error('[Dars] Event error:', err); }}
                          }});
                      }};
                  }} else if (typeof code === 'string') {{
                      try {{ handler = new Function('event', code); }} catch(e) {{ console.error('[Dars] Event compilation error:', e); }}
                  }}
                  if (handler) {{
                      el['on' + eventName] = handler;
                  }}
              }}
          }}
           
           // Handle custom state properties (notify watchers for any property not in known list)
           const knownProps = ['id', 'dynamic', 'text', 'html', 'style', 'attrs', 'classes', 'figure', 'useCustomRender'];
           for (const k in opt) {{
               if (!knownProps.includes(k) && !k.startsWith('on_')) {{
                   notifyWatchers(k, opt[k]);
               }}
           }}

           // Lifecycle: notify onUpdate after dynamic changes for this id
           _runLifecycle(opt.id, 'onUpdate');
       }} else {{
           // Element not found, but we should still notify watchers!
           if (opt.hasOwnProperty('text')) notifyWatchers('text', opt.text);
           if (opt.hasOwnProperty('html')) notifyWatchers('html', opt.html);
           if (opt.style) notifyWatchers('style', opt.style);
           if (opt.attrs) {{
               for (const k in opt.attrs) notifyWatchers(k, opt.attrs[k]);
           }}
           // Also notify for custom properties
           const knownProps = ['id', 'dynamic', 'text', 'html', 'style', 'attrs', 'classes', 'figure', 'useCustomRender'];
           for (const k in opt) {{
               if (!knownProps.includes(k) && !k.startsWith('on_')) {{
                   notifyWatchers(k, opt[k]);
               }}
           }}

           // Lifecycle: even if element not found, still allow logical onUpdate
           _runLifecycle(opt.id, 'onUpdate');
       }}
      
      return;
  }}

  const name = opt.name || null;
  const st = name ? __registry.get(name) : null;
  let targetState = (typeof opt.state === 'number') ? opt.state : null;
  let goto = (opt.hasOwnProperty('goto') ? opt.goto : null);
  if(st){{
    const cur = st.current || 0;
    const len = Array.isArray(st.states) ? st.states.length : 0;
    if(goto !== null){{ targetState = _resolveGoto(cur, goto, len); }}
    if(targetState === null){{ targetState = cur; }}
    
    st.current = targetState;
    
    const rules = st.rules && st.rules[String(targetState)];
    if(targetState === 0){{
      _restoreDefault(st.id, st.__defaultSnapshot, st.__vnode, (typeof window !== 'undefined' ? window.EventMap : null));
      if(rules){{ try{{ console.error('[Dars] Default state (index 0) is immutable. Rules for state 0 are ignored.'); }}catch(_){{ }} }}
    }} else if(rules){{
      if(Array.isArray(rules.mods)){{ _applyMods(st.id, rules.mods); }}
      if(rules.hasOwnProperty('goto')){{
        const nxt = _resolveGoto(st.current, rules.goto, len);
        if(nxt !== st.current){{ 
            setTimeout(() => {{
                change({{ id: opt.id, name: name, state: nxt }});
            }}, 0);
        }}
      }}
    }}
  }}

  try{{
    const el = $(opt.id);
    if(!el) return;
    const ev = new CustomEvent('dars:state', {{ detail: {{ id: opt.id, state: targetState }} }});
    el.dispatchEvent(ev);
  }}catch(e){{ }}
}}

// Notify lifecycle onUpdate for components affected by VRef changes.
// This is called from the JS generated by the Python updateVRef() helper.
function updateVRef(selector) {{
  try {{
    const els = (typeof selector === 'string') ? document.querySelectorAll(selector) : [];
    if (!els.length) return;

    const seen = new Set();

    els.forEach(el => {{
      let node = el;
      while (node) {{
        const id = node.id;
        if (id && !seen.has(id) && __lifecycle && __lifecycle.has(String(id))) {{
          seen.add(id);
          _runLifecycle(String(id), 'onUpdate');
          break;  // Stop at first lifecycle-enabled ancestor
        }}
        node = node.parentElement;
      }}
    }});
  }} catch (_e) {{ }}
}}

// ==================== ROUTER ====================
// Vite minification compatible - uses string literals for all object properties

const __spaRoutes = [];  // Array of route configs (for pattern matching)
const __spaRoutesMap = new Map();  // name -> route config
const __spaPreloaded = new Set();  // preloaded routes
let __spaCurrentRoute = null;
let __spaCurrentParams = {{}};
let __spaConfig = null;
let __spa404Route = null;

function _normalizePath(input){{
  try{{
    let p = String(input || '');
    const hashIdx = p.indexOf('#');
    if(hashIdx >= 0) p = p.slice(0, hashIdx);
    const qIdx = p.indexOf('?');
    if(qIdx >= 0) p = p.slice(0, qIdx);
    if(!p) return '/';
    if(!p.startsWith('/')) p = '/' + p;
    while(p.length > 1 && p.endsWith('/')) p = p.slice(0, -1);
    return p;
  }}catch(e){{ return '/'; }}
}}

/**
 * Convert route pattern to regex (Vite-safe)
 * /user/:id -> /user/(?<id>[^/]+)
 */
function _routeToRegex(pattern){{
  try{{
    const regexStr = String(pattern).replace(/:([a-zA-Z_][a-zA-Z0-9_]*)/g, '(?<$1>[^/]+)');
    return new RegExp(`^${{regexStr}}$`);
  }}catch(e){{ return null; }}
}}

/**
 * Match a path against all routes
 * Returns {{ route, params }} or null
 */
function _matchRoute(path){{
  try{{
    const normalized = _normalizePath(path);
    for(let i=0; i<__spaRoutes.length; i++){{
      const route = __spaRoutes[i];
      const regex = route['_regex'] || _routeToRegex(route['path']);
      if(regex){{ route['_regex'] = regex; }}  // Cache regex
      
      const match = String(normalized).match(regex);
      if(match){{
        const params = match['groups'] || {{}};
        return {{ 'route': route, 'params': params }};
      }}
    }}
  }}catch(e){{ }}
  return null;
}}

/**
 * Register SPA routing configuration (Vite-safe)
 */
function registerSPAConfig(config){{
  try{{
    __spaConfig = config;
    if(!config || !Array.isArray(config['routes'])) return;
    
    // Clear and rebuild routes
    __spaRoutes.length = 0;
    __spaRoutesMap.clear();
    
    const routes = config['routes'];
    for(let i=0; i<routes.length; i++){{
      const route = routes[i];
      if(!route['path'] || !route['name']) continue;
      __spaRoutes.push(route);
      __spaRoutesMap.set(route['name'], route);
    }}
    
    // Register 404 page if exists
    if(config['notFound']){{ __spa404Route = config['notFound']; }}
    
    // Robust initialization strategy
    window.__DARS_ROUTER_INIT = false;
    
    function _attemptInit() {{
      if (window.__DARS_ROUTER_INIT) return;
      
      // If VDOM is missing but might be coming (interactive/loading), wait unless it's the 'load' event
      const hasData = window.__ROUTE_VDOM__ || window.__DARS_VDOM__;
      const isComplete = document.readyState === 'complete';
      
      if (hasData || isComplete) {{
        window.__DARS_ROUTER_INIT = true;
        _initializeRouter();
      }}
    }}

    // 1. Try immediately
    _attemptInit();

    // 2. Try on DOMContentLoaded (earliest safe moment)
    if (!window.__DARS_ROUTER_INIT) {{
      document.addEventListener('DOMContentLoaded', _attemptInit);
    }}

    // 3. Try on load (fallback for late scripts)
    if (!window.__DARS_ROUTER_INIT) {{
      window.addEventListener('load', function() {{ 
        // Force init on load even if data missing (it's not coming)
        if (!window.__DARS_ROUTER_INIT) {{
             window.__DARS_ROUTER_INIT = true;
             _initializeRouter();
        }}
      }});
    }}
  }}catch(e){{ console.error('[Dars Router] Config error:', e); }}
}}

/**
 * Initialize the SPA router
 */
function _initializeRouter(){{
  try{{
    // Handle initial route
    const initialPath = _normalizePath(window.location.pathname);
    
    // Skip initial fetch if already hydrated (SSR)
    let skipInit = false;
    const match = _matchRoute(initialPath);

    const vdomSource = window.__ROUTE_VDOM__ || window.__DARS_VDOM__;
    if (vdomSource) {{
        
        // Find matching route to set as current
        if (match && match.route) {{
            // Update global state to reflect current route without navigating
            __spaCurrentRoute = initialPath;
            __spaCurrentParams = match.params || {{}};
            window['__DARS_ROUTE_PARAMS__'] = __spaCurrentParams;

            // Mark the route as loaded and populate its data from SSR
            match.route.vdom = vdomSource;
            match.route.html = document.getElementById('__dars_spa_root__') ? document.getElementById('__dars_spa_root__').innerHTML : '';
            match.route.loaded = true;
            
            // Ensure history state is correctly set for the initial page
            window.history.replaceState({{ 
                path: initialPath, 
                params: __spaCurrentParams
            }}, document.title, initialPath);
            
            skipInit = true;
        }}
    }}
    
    if (!skipInit) {{
        _navigateToRoute(initialPath, {{ 'replace': true, 'skipPushState': true }});
    }}
    
    // Listen for popstate (browser back/forward)
    window.addEventListener('popstate', function(event){{
      try{{
        const path = _normalizePath((event.state && event.state['path']) || window.location.pathname);
        const params = (event.state && event.state['params']) || {{}};
        _navigateToRoute(path, {{ 'replace': true, 'skipPushState': true, 'params': params }});
      }}catch(e){{ }}
    }});
    
    // Intercept link clicks for SPA navigation
    document.addEventListener('click', function(event){{
      try{{
        const link = event.target.closest('a[href]');
        if(!link) return;
        
        const href = link.getAttribute('href');
        if(!href || href.startsWith('http') || href.startsWith('//') || href.startsWith('#')){{
          return; // External link or anchor
        }}

        const normalizedHref = _normalizePath(href);
        
        // Check if this matches any SPA route
        const match = _matchRoute(normalizedHref);
        if(match){{
          event.preventDefault();
          navigateTo(normalizedHref);
        }}
      }}catch(e){{ }}
    }});
  }}catch(e){{ console.error('[Dars Router] Init error:', e); }}
}}

/**
 * Navigate to a route path (public API)
 */
function navigateTo(path, params){{
  try{{
    _navigateToRoute(_normalizePath(path), {{ 'replace': false, 'params': params || {{}} }});
  }}catch(e){{ console.error('[Dars Router] Navigate error:', e); }}
}}

/**
 * Internal navigation handler
 */
async function _navigateToRoute(path, options){{
  try{{
    options = options || {{}};

    path = _normalizePath(path);
    
    // Match route (supports parameters)
    let match = _matchRoute(path);
    let params = options['params'] || {{}};
    
    // If no match AND path is root, try index route (redirect to index)
    if(!match && (path === '/' || path === '') && __spaConfig && __spaConfig['index']){{
      const indexRoute = __spaRoutesMap.get(__spaConfig['index']);
      if(indexRoute){{
        match = {{ 'route': indexRoute, 'params': {{}} }};
        path = indexRoute['path'];
      }}
    }}
    
    // If still no match, try 404 page
    if(!match){{
      console.log('[Dars Router] No match for:', path);
      
      // Try redirect to configured 404 path
      if(__spaConfig && __spaConfig['notFoundPath']){{
         const notFoundPath = __spaConfig['notFoundPath'];
         // Avoid infinite loop if 404 page itself is missing
         if(path !== notFoundPath){{
             console.log('[Dars Router] Redirecting to 404 path:', notFoundPath);
             await _navigateToRoute(notFoundPath, {{ 'replace': true, 'skipPushState': false }});
             return;
         }}
      }}
      
      if(__spa404Route){{
        console.log('[Dars Router] Using legacy 404 route object');
        match = {{ 'route': __spa404Route, 'params': {{}} }};
      }}else{{
        console.error('[Dars Router] Route not found and no 404 page configured:', path);
        return;
      }}
    }}
    
    const route = match['route'];
    const matchedParams = match['params'] || {{}};
    
    // Merge params
    for(const key in matchedParams){{ params[key] = matchedParams[key]; }}
    
    // Update browser history
    if(!options['skipPushState']){{
      const state = {{ 'path': path, 'params': params }};
      if(options['replace']){{
        history.replaceState(state, '', path);
      }}else{{
        history.pushState(state, '', path);
      }}
    }}
    
    // Load route content (await for lazy loading)
    await _loadRoute(route, params);
    
    // Update current route
    __spaCurrentRoute = path;
    __spaCurrentParams = params;
    
    // Store params in window for access in components
    window['__DARS_ROUTE_PARAMS__'] = params;
    
    // Preload specified routes
    const preload = route['preload'];
    if(preload && Array.isArray(preload)){{
      for(let i=0; i<preload.length; i++){{
        _preloadRoute(preload[i]);
      }}
    }}
    
    // Dispatch custom event
    try{{
      const detail = {{ 'from': __spaCurrentRoute, 'to': path, 'route': route, 'params': params }};
      const ev = new CustomEvent('dars:route-change', {{ 'detail': detail }});
      window.dispatchEvent(ev);
    }}catch(e){{ }}
  }}catch(e){{ console.error('[Dars Router] Navigation error:', e); }}
}}

/**
 * Load and render a route (Hierarchical)
 */
async function _loadRoute(route, params){{
  try{{
    function _getLoadingHTML(r){{
      try{{
        // 1) Per-route loading override
        if(r && r['loadingHtml']){{
          const raw = String(r['loadingHtml']);
          if(raw.includes('data-dars-ssr-loading="1"')) return raw;
          return `<div data-dars-ssr-loading="1">${{raw}}</div>`;
        }}
        // 2) Global SPA config loading override
        if(__spaConfig && __spaConfig['loadingHtml']){{
          const raw = String(__spaConfig['loadingHtml']);
          if(raw.includes('data-dars-ssr-loading="1"')) return raw;
          return `<div data-dars-ssr-loading="1">${{raw}}</div>`;
        }}
      }}catch(e){{ }}
      return '<div data-dars-ssr-loading="1" style="padding:24px;font-family:system-ui,-apple-system,sans-serif;opacity:.75">Loading...</div>';
    }}

    function _getErrorHTML(r){{
      try{{
        // 1) Per-route error override
        if(r && r['errorHtml']){{
          const raw = String(r['errorHtml']);
          if(raw.includes('data-dars-ssr-error="1"')) return raw;
          return `<div data-dars-ssr-error="1">${{raw}}</div>`;
        }}
        // 2) Global SPA config error override
        if(__spaConfig && __spaConfig['errorHtml']){{
          const raw = String(__spaConfig['errorHtml']);
          if(raw.includes('data-dars-ssr-error="1"')) return raw;
          return `<div data-dars-ssr-error="1">${{raw}}</div>`;
        }}
      }}catch(e){{ }}
      return '<div data-dars-ssr-error="1" style="padding:24px;font-family:system-ui,-apple-system,sans-serif;opacity:.75">Failed to load page.</div>';
    }}

    function _getOutletEl(wrapper, outletId){{
      try{{
        if(!wrapper) return null;
        const wanted = String(outletId || 'main');
        // Prefer explicit id match
        const sel = `[data-dars-outlet="true"][data-dars-outlet-id="${{wanted}}"]`;
        const found = wrapper.querySelector(sel);
        if(found) return found;
        // Backward compat: first outlet
        return wrapper.querySelector('[data-dars-outlet="true"]');
      }}catch(e){{ return null; }}
    }}

    function _applyParamsToHTML(html, p){{
      try{{
        let out = String(html || '');
        const pp = p || {{}};
        for(const key in pp){{
          try{{
            const value = pp[key];
            const regex = new RegExp(`\\{{\\{{${{key}}\\}}\\}}`, 'g');
            out = out.replace(regex, String(value));
          }}catch(e){{ }}
        }}
        return out;
      }}catch(e){{ return String(html || ''); }}
    }}

    function _renderRouteInto(mountEl, r, p, isRootLevel){{
      try{{
        if(!mountEl) return null;

        // Create wrapper for this route
        const wrapper = document.createElement('div');
        wrapper.setAttribute('data-dars-route-wrapper', r['name']);
        wrapper.style.height = '100%';
        wrapper.style.width = '100%';

        // Fill HTML (with params)
        const html = _applyParamsToHTML(r['html'] || '', p);
        wrapper.innerHTML = html;

        // Replace content
        mountEl.innerHTML = '';
        mountEl.appendChild(wrapper);

        // Assets / hydration
        if(r['title']) document.title = String(r['title']);
        if(r['styles']) _injectStyles(r['name'], r['styles']);
        if(r['scripts']) _executeScripts(r['scripts'], r['name']);
        if(r['events']) _attachEventsMap(r['events']);

        if(r['states'] && Array.isArray(r['states'])){{ registerStates(r['states']); }}
        if(r['vdom']){{
          try{{ if(typeof window['DarsHydrate'] === 'function') window['DarsHydrate'](wrapper); }}catch(e){{ }}
        }}

        if(isRootLevel) try{{ window.scrollTo(0, 0); }}catch(e){{ }}
        return wrapper;
      }}catch(e){{ return null; }}
    }}

    function _renderChain(chain, p){{
      try{{
        let container = document.getElementById('__dars_spa_root__');
        if(!container) return;

        // Cleanup assets for inactive routes BEFORE rendering new chain
        const activeRouteNames = new Set(chain.map(r => r['name']));

        const allScripts = document.querySelectorAll('.dars-route-script');
        allScripts.forEach(script => {{
          const scriptRoute = script.getAttribute('data-route');
          if(scriptRoute && !activeRouteNames.has(scriptRoute)){{
            try{{ script.remove(); }}catch(e){{ }}
          }}
        }});

        const allStyles = document.querySelectorAll('style[id^="dars-route-styles-"]');
        allStyles.forEach(style => {{
          const styleId = style.id;
          const routeName = styleId.replace('dars-route-styles-', '');
          if(routeName && !activeRouteNames.has(routeName)){{
            try{{ style.remove(); }}catch(e){{ }}
          }}
        }});

        // Render each level into its mount
        let lastWrapper = null;
        for(let i=0; i<chain.length; i++){{
          const r = chain[i];
          const isRootLevel = (i === 0);

          // Render this route into current container
          lastWrapper = _renderRouteInto(container, r, p, isRootLevel);
          if(!lastWrapper) return;

          // Move container to next outlet
          if(i < chain.length - 1){{
            const nextOutletId = String(chain[i+1]['outletId'] || 'main');
            const outlet = _getOutletEl(lastWrapper, nextOutletId);
            if(!outlet){{
              console.error('[Dars Router] Missing outlet in parent route:', r['name']);
              return;
            }}
            container = outlet;
          }}
        }}

        // Update page metadata (title, description, OG tags, etc.) if available
        const leafRoute = chain[chain.length - 1];
        if (leafRoute) {{
          if (leafRoute['headMetadata']) {{
            try {{
              updatePageMetadata(leafRoute['headMetadata']);
            }} catch(e) {{
              console.error('[Dars Router] Error updating metadata:', e);
            }}
          }} else if (leafRoute['title']) {{
            try {{ document.title = leafRoute['title']; }} catch(e) {{}}
          }}
        }}
      }}catch(e){{ console.error('[Dars Router] Render chain error:', e); }}
    }}

    // Check if route is SSR and needs lazy loading
    if(route['type'] === 'ssr' && !route['html']){{
      // Render placeholder first (so navigation feels instant)
      try{{
        route['html'] = _getLoadingHTML(route);
        route['events'] = route['events'] || {{}};
        route['vdom'] = route['vdom'] || {{}};
        route['states'] = route['states'] || [];
        route['scripts'] = route['scripts'] || [];
        route['styles'] = route['styles'] || '';
      }}catch(e){{ }}
    }}
    
    // 1. Build route chain [Root, ..., Parent, Child]
    const chain = [];
    let curr = route;
    while(curr){{
      chain.unshift(curr);
      curr = curr['parent'] ? __spaRoutesMap.get(curr['parent']) : null;
    }}

    // First paint (may show placeholder for SSR routes)
    _renderChain(chain, params);

    // If SSR leaf route is still loading, fetch it now and re-render
    if(route['type'] === 'ssr' && route['html'] && String(route['html']).includes('data-dars-ssr-loading="1"')){{
      try{{
        const backendUrl = (__spaConfig && __spaConfig['backendUrl']) || '';
        const loaderUrl = route['ssr_endpoint'] || `/api/ssr/${{route['name']}}`;
        let fullUrl = backendUrl ? `${{backendUrl}}${{loaderUrl}}` : loaderUrl;

        const sep = fullUrl.includes('?') ? '&' : '?';
        fullUrl = fullUrl + sep + '_t=' + Date.now();

        const response = await fetch(fullUrl, {{
          headers: {{ 'Content-Type': 'application/json' }}
        }});

        if(!response.ok){{
          throw new Error(`Failed to load route: ${{response.status}}`);
        }}

        const routeData = await response.json();

        route['html'] = routeData['html'] || '';
        route['scripts'] = routeData['scripts'] || [];
        route['events'] = routeData['events'] || {{}};
        route['vdom'] = routeData['vdom'] || {{}};
        route['states'] = routeData['states'] || [];
        route['styles'] = routeData['styles'] || route['styles'] || '';
        route['headMetadata'] = routeData['headMetadata'] || route['headMetadata'];
      }}catch(error){{
        console.error('[Dars Router] Error loading SSR route:', error);
        try{{
          route['html'] = _getErrorHTML(route);
          route['events'] = {{}};
          route['vdom'] = {{}};
          route['states'] = [];
          route['scripts'] = [];
          route['styles'] = '';
          _renderChain(chain, params);
        }}catch(_e){{ }}
        return;
      }}

      // Second paint (real SSR content)
      _renderChain(chain, params);
    }}

  }}catch(e){{ console.error('[Dars Router] Load error:', e); }}
}}

/**
 * Inject styles for a route
 */
function _injectStyles(routeName, styles){{
  try{{
    const styleId = `dars-route-styles-${{routeName}}`;
    
    // Remove old styles for this route
    const oldStyle = document.getElementById(styleId);
    if(oldStyle){{ oldStyle.remove(); }}
    
    // Add new styles
    const styleEl = document.createElement('style');
    styleEl.id = styleId;
    styleEl.textContent = String(styles);
    document.head.appendChild(styleEl);
  }}catch(e){{ }}
}}

/**
 * Execute scripts for a route
 */
function _executeScripts(scripts, routeName){{
  try{{
    if(!Array.isArray(scripts)) return;
    
    for(let i=0; i<scripts.length; i++){{
      const script = scripts[i];
      if(typeof script === 'string'){{
        // Check if it's a filename (ends with .js)
        if(script.endsWith('.js')){{
          _loadExternalScript(script, false, routeName);
        }}else{{
          // Inline script code
          try{{ (0, eval)(script); }}catch(e){{ console.error('[Dars Router] Script error:', e); }}
        }}
      }}else{{
        // Script object
        if(script['src']){{
            _loadExternalScript(script['src'], script['module'], routeName);
        }}else if(script['code']){{
            try{{
                const s = document.createElement('script');
                s.textContent = script['code'];
                s.className = 'dars-route-script';
                if(routeName) s.setAttribute('data-route', routeName);
                if(script['module']) s.type = 'module';
                document.body.appendChild(s);
            }}catch(e){{ console.error('[Dars Router] Script error:', e); }}
        }}
      }}
    }}
  }}catch(e){{ }}
}}

/**
 * Load external script
 */
function _loadExternalScript(src, isModule, routeName){{
  try{{
    const script = document.createElement('script');
    script.src = String(src);
    script.async = false; // Ensure sequential execution
    script.className = 'dars-route-script'; // Tag for cleanup
    if(routeName) script.setAttribute('data-route', routeName);
    if(isModule){{ script.type = 'module'; }}
    
    // Simulate DOMContentLoaded for scripts that depend on it
    script.onload = function(){{
      try{{
        // Trigger a custom event that scripts can listen to
        const event = new Event('DOMContentLoaded');
        document.dispatchEvent(event);
      }}catch(e){{ }}
    }};
    
    script.onerror = function(){{ console.error('[Dars Router] Script load failed:', src); }};
    document.body.appendChild(script);
  }}catch(e){{ }}
}}

/**
 * Preload a route in the background
 */
function _preloadRoute(path){{
  try{{
    if(__spaPreloaded.has(path)) return;  // Already preloaded
    const route = _matchRoute(path);
    if(!route) return;
    __spaPreloaded.add(path);
    route['route']['__preloaded'] = true;
  }}catch(e){{ }}
}}

/**
 * Get current route (public API)
 */
function getCurrentRoute(){{
  return __spaCurrentRoute;
}}

/**
 * Get current route parameters (public API)
 */
function getRouteParams(){{
  return __spaCurrentParams;
}}

// ==================== STATE V2 LOOP SUPPORT ====================

// Registro de loops activos para auto-increment/decrement
const __activeLoops = new Map();

/**
 * Start a continuous operation loop (auto_increment, auto_decrement, etc.)
 */
function startLoop(id, config) {{
    if (__activeLoops.has(id)) {{
        clearInterval(__activeLoops.get(id).timer);
    }}
    
    const timer = setInterval(() => {{
        const el = $(id);
        if (!el) {{
            console.warn('[Dars] Element not found for loop:', id);
            stopLoop(id);
            return;
        }}
        
        if (config.type === 'auto_increment') {{
            let current = 0;
            const st = __registry.get(id);
            const prop = config.property || 'text';
            
            if (st && st.values) {{
                current = parseFloat(st.values[prop] || 0);
            }} else if (el) {{
                current = parseFloat(el.textContent || '0');
            }}
            
            current += config.by || 1;
            
            if (config.max !== null && config.max !== undefined && current >= config.max) {{
                current = config.max;
                stopLoop(id);
            }}
            
            const payload = {{ id: id, dynamic: true }};
            if (prop === 'text' || prop === 'html') {{
                payload[prop] = current;
            }} else {{
                payload.attrs = {{}};
                payload.attrs[prop] = current;
            }}
            change(payload);
            
        }} else if (config.type === 'auto_decrement') {{
            let current = 0;
            const st = __registry.get(id);
            const prop = config.property || 'text';
            
            if (st && st.values) {{
                current = parseFloat(st.values[prop] || 0);
            }} else if (el) {{
                current = parseFloat(el.textContent || '0');
            }}
            
            current -= config.by || 1;
            
            if (config.min !== null && config.min !== undefined && current <= config.min) {{
                current = config.min;
                stopLoop(id);
            }}
            
            const payload = {{ id: id, dynamic: true }};
            if (prop === 'text' || prop === 'html') {{
                payload[prop] = current;
            }} else {{
                payload.attrs = {{}};
                payload.attrs[prop] = current;
            }}
            change(payload);
        }} else if (config.type === 'custom') {{
            try {{
                (0,eval)(config.code);
            }} catch(e) {{
                console.error('[Dars Loop]', e);
            }}
        }}
    }}, config.interval || 1000);
    
    __activeLoops.set(id, {{ timer: timer, config: config }});
}}

function stopLoop(id) {{
    if (__activeLoops.has(id)) {{
        clearInterval(__activeLoops.get(id).timer);
        __activeLoops.delete(id);
    }}
}}

function stopAllLoops() {{
    for (const [id, loop] of __activeLoops) {{
        clearInterval(loop.timer);
    }}
    __activeLoops.clear();
}}

// ==================== END SPA ROUTER ====================

const Dars = {{ 
    registerState, 
    registerStates, 
    getState, 
    change, 
    watch,
    updateVRef,
    $, 
    runtime,
    // Loop support for State V2
    startLoop,
    stopLoop,
    stopAllLoops,
    router: {{
        registerConfig: registerSPAConfig,
        navigateTo: navigateTo,
        getCurrentRoute: getCurrentRoute,
        getRouteParams: getRouteParams,
        matchRoute: _matchRoute
    }},
    version: DARS_VERSION,
    releaseUrl: DARS_RELEASE_URL,
    updatePageMetadata: updatePageMetadata  // Expose for SPA metadata updates
}};

// If the SSR backend provided a snapshot for State V2, expose it on the
// Dars object so tools or advanced integrations can inspect it. The
// current runtime does not require this snapshot to function, but having
// it available keeps the data round-trip complete.
try {{
  if (typeof window !== 'undefined' && Array.isArray(window.__DARS_STATE_V2__)) {{
    Dars.stateV2Snapshot = window.__DARS_STATE_V2__;
  }}
}} catch(_) {{ }}

// ==================== HEAD METADATA UPDATES ====================
// Update head metadata on SPA route change
function updatePageMetadata(metadata) {{
    if (!metadata) return;
    
    try {{
        // Update title
        if (metadata.title) {{
            document.title = metadata.title;
        }}
        
        // Update or create meta tags
        _updateMeta('description', metadata.description);
        _updateMeta('author', metadata.author);
        _updateMeta('robots', metadata.robots);
        
        // Keywords
        if (metadata.keywords) {{
            const kw = Array.isArray(metadata.keywords) 
                ? metadata.keywords.join(', ') 
                : metadata.keywords;
            _updateMeta('keywords', kw);
        }}
        
        // Canonical
        if (metadata.canonical) {{
            _updateLink('canonical', metadata.canonical);
        }}
        
        // Favicon
        if (metadata.favicon) {{
            _updateLink('icon', metadata.favicon);
        }}
        
        // Open Graph
        const og = metadata.og || {{}};
        _updateMeta('og:title', og.title, 'property');
        _updateMeta('og:description', og.description, 'property');
        _updateMeta('og:image', og.image, 'property');
        _updateMeta('og:type', og.type, 'property');
        _updateMeta('og:url', og.url, 'property');
        _updateMeta('og:site_name', og.site_name, 'property');
        _updateMeta('og:locale', og.locale, 'property');
        
        // Twitter
        const twitter = metadata.twitter || {{}};
        _updateMeta('twitter:card', twitter.card);
        _updateMeta('twitter:site', twitter.site);
        _updateMeta('twitter:creator', twitter.creator);
        _updateMeta('twitter:title', twitter.title);
        _updateMeta('twitter:description', twitter.description);
        _updateMeta('twitter:image', twitter.image);
    }} catch(e) {{
        try {{ console.error('[Dars] Metadata update error:', e); }} catch(_) {{}}
    }}
}}

function _updateMeta(name, content, attr) {{
    attr = attr || 'name';
    if (!content) return;
    
    try {{
        let meta = document.querySelector(`meta[${{attr}}="${{name}}"]`);
        if (!meta) {{
            meta = document.createElement('meta');
            meta.setAttribute(attr, name);
            document.head.appendChild(meta);
        }}
        meta.setAttribute('content', String(content));
    }} catch(_) {{}}
}}

function _updateLink(rel, href) {{
    if (!href) return;
    
    try {{
        let link = document.querySelector(`link[rel="${{rel}}"]`);
        if (!link) {{
            link = document.createElement('link');
            link.setAttribute('rel', rel);
            document.head.appendChild(link);
        }}
        link.setAttribute('href', String(href));
    }} catch(_) {{}}
}}

try {{ window.Dars = window.Dars || Dars; }} catch(_) {{}}
export {{ registerState, registerStates, getState, change, $ }};
export default Dars;
"""
