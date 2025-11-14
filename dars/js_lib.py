from dars.version import __version__, __release_url__

DARS_MIN_JS = f"""/* Dars minimal runtime script */
const DARS_VERSION = '{__version__}';
const DARS_RELEASE_URL = '{__release_url__}';

const __registry = new Map();
const __vdom = new Map();

function $(id){{ return document.getElementById(id) || document.querySelector(`[data-id="${{id}}"]`) || null; }}

// Alert helper (non-fatal)
function _alert(msg){{ try{{ alert(String(msg)); }}catch(_ ){{ try{{ console.error(String(msg)); }}catch(_ ){{ }} }} }}

// CSS.escape fallback
function _cssEscape(s){{
  try{{ if (globalThis.CSS && typeof CSS.escape==='function') return CSS.escape(String(s)); }}catch(_ ){{ }}
  try{{ return String(s).replace(/[^a-zA-Z0-9_\-]/g, '\\$&'); }}catch(_ ){{ return String(s); }}
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
        el.__darsEv = el.__darsEv || {{}};
        if(el.__darsEv[type]){{ try{{ el.removeEventListener(type, el.__darsEv[type], true); }}catch(_ ){{ }} try{{ el.removeEventListener(type, el.__darsEv[type], false); }}catch(_ ){{ }} }}
        const handler = function(ev){{ try{{ ev.stopImmediatePropagation(); ev.stopPropagation(); ev.preventDefault(); ev.cancelBubble = true; }}catch(_ ){{ }}
          for(const c of codes){{ try{{ (0,eval)(c); }}catch(_ ){{ }} }}
        }};
        try{{ el.addEventListener(type, handler, {{ capture: true }}); }}catch(_ ){{ }}
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
        el.__darsEv = el.__darsEv || {{}};
        if(el.__darsEv[type]){{ try{{ el.removeEventListener(type, el.__darsEv[type], true); }}catch(_ ){{ }} try{{ el.removeEventListener(type, el.__darsEv[type], false); }}catch(_ ){{ }} }}
        const handler = function(ev){{ try{{ ev.stopImmediatePropagation(); ev.stopPropagation(); ev.preventDefault(); ev.cancelBubble = true; }}catch(_ ){{ }}
          for(const c of codes){{ try{{ (0,eval)(c); }}catch(_ ){{ }} }}
        }};
        try{{ el.addEventListener(type, handler, {{ capture: true }}); }}catch(_ ){{ }}
        el.__darsEv[type] = handler;
      }}
    }}catch(_ ){{ }}
  }}
}}

const runtime = {{
  deleteComponent(id){{
    try{{
      const el = $(id); if(!el) return;
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
    __defaultSnapshot: null
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

function getState(name){{ return __registry.get(name); }}

function _restoreDefault(id, snap){{
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
    try{{
      const current = el.getAttributeNames ? el.getAttributeNames() : [];
      for(const n of current){{ if(n !== 'id') el.removeAttribute(n); }}
      for(const k in snap.attrs){{ if(k !== 'id') el.setAttribute(k, snap.attrs[k]); }}
    }}catch(_){{ }}
    try{{ el.innerHTML = snap.html || ''; }}catch(_){{ }}
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
                el.__darsEv = el.__darsEv || {{}};
                if(el.__darsEv[type]){{
                  try{{ el.removeEventListener(type, el.__darsEv[type], true); }}catch(_){{ }}
                  try{{ el.removeEventListener(type, el.__darsEv[type], false); }}catch(_){{ }}
                }}
                const handler = function(ev){{
                  try{{ ev.stopImmediatePropagation(); }}catch(_){{ }}
                  try{{ ev.stopPropagation(); }}catch(_){{ }}
                  try{{ ev.preventDefault(); }}catch(_){{ }}
                  try{{ ev.cancelBubble = true; }}catch(_){{ }}
                  let propName = 'on'+type;
                  let prevOn = null;
                  try{{ prevOn = el[propName]; el[propName] = null; }}catch(_){{ }}
                  try{{ 
                    // NUEVO: ejecutar todos los códigos en secuencia
                    for(const c of codes){{ 
                      try{{ (0,eval)(c); }}catch(_){{ }} 
                    }} 
                  }} finally{{
                    try{{ setTimeout(()=>{{ try{{ el[propName] = prevOn; }}catch(_){{ }} }}, 0); }}catch(_){{ }}
                  }}
                }};
                try{{ el.addEventListener(type, handler, {{ capture: true }}); }}catch(_){{ }}
                el.__darsEv[type] = handler;
                continue;
              }}
            }}
            el.setAttribute(k, String(attrs[k]));
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
    if(/^[-+]\\\\d+$/.test(goto)){{
      const delta = parseInt(goto, 10);
      const next = cur + delta;
      if(statesLen && statesLen > 0){{ return Math.max(0, Math.min(statesLen-1, next)); }}
      return next;
    }}
    const n = parseInt(goto, 10);
    if(!isNaN(n)) return n;
  }}
  return cur;
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
      _restoreDefault(st.id, st.__defaultSnapshot);
      if(rules){{ try{{ console.error('[Dars] Default state (index 0) is immutable. Rules for state 0 are ignored.'); }}catch(_){{ }} }}
    }} else if(rules){{
      if(Array.isArray(rules.mods)){{ _applyMods(st.id, rules.mods); }}
      if(rules.hasOwnProperty('goto')){{
        const nxt = _resolveGoto(st.current, rules.goto, len);
        if(nxt !== st.current){{ st.current = nxt; }}
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

const Dars = {{ 
    registerState, 
    registerStates, 
    getState, 
    change, 
    $, 
    runtime,
    version: DARS_VERSION,
    releaseUrl: DARS_RELEASE_URL
}};
try {{ window.Dars = window.Dars || Dars; }} catch(_) {{}}
export {{ registerState, registerStates, getState, change, $ }};
export default Dars;
"""