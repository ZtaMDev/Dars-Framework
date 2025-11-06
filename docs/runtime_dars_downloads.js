// Dars Runtime (Hydration + Delegated Events + Diff/Patch + Hot Reload)
(function(){
  const eventMap = new Map(); // id -> {ev: fn}
  let currentSnapshot = null;
  let currentVersion = null;

  // Registro de componentes (skeleton). En siguientes iteraciones añadiremos create/patch por tipo built-in
  const registry = {
    // Implementación mínima segura para crear nodos cuando se agregan hijos
    'Text': {
      create(v){
        if(!v || v.isIsland) return null;
        const el = document.createElement('span');
        if(v.id) el.id = v.id;
        if(v.class) el.className = v.class;
        if(v.style){ for(const k in v.style){ try{ el.style.setProperty(k.replace(/_/g,'-'), String(v.style[k])); }catch{} } }
        if(Object.prototype.hasOwnProperty.call(v,'text')){ el.textContent = String(v.text||''); }
        // props
        if(v.props){ for(const k in v.props){ const val=v.props[k]; try{ if(val===false||val===null||typeof val==='undefined'){ el.removeAttribute(k);} else { el.setAttribute(k, String(val)); } }catch{} } }
        return el;
      }
    },
    'Container': {
      create(v){
        if(!v || v.isIsland) return null;
        const el = document.createElement('div');
        if(v.id) el.id = v.id;
        const base = 'dars-container';
        el.className = (v.class ? (base + ' ' + v.class) : base);
        if(v.style){ for(const k in v.style){ try{ el.style.setProperty(k.replace(/_/g,'-'), String(v.style[k])); }catch{} } }
        // props
        if(v.props){ for(const k in v.props){ const val=v.props[k]; try{ if(val===false||val===null||typeof val==='undefined'){ el.removeAttribute(k);} else { el.setAttribute(k, String(val)); } }catch{} } }
        return el;
      }
    },
  };

  function walk(v, fn){
    if(!v) return;
    fn(v);
    const ch = v.children || [];
    for(let i=0;i<ch.length;i++){ walk(ch[i], fn); }
  }

  function bindEventsFromVNode(snapshot){
    // Construir tabla de eventos a partir del snapshot
    walk(snapshot, (v)=>{
      if(v && v.id && v.events){
        const handlers = {};
        for(const ev in v.events){
          const spec = v.events[ev];
          if(spec && spec.type==='inline' && spec.code){
            try { handlers[ev] = new Function('event', spec.code); } catch(err){ /* ignore compile error */ }
          }
        }
        if(Object.keys(handlers).length){ eventMap.set(v.id, handlers); } else { eventMap.delete(v.id); }
      }
    });
  }

  // Utilities
  function setProps(el, props){
    if(!el || !props) return;
    for(const [k,v] of Object.entries(props)){
      try {
        if(v === false || v === null || typeof v === 'undefined'){
          el.removeAttribute(k);
        } else {
          el.setAttribute(k, String(v));
        }
      } catch(err) { /* ignore */ }
    }
  }
  function diffProps(el, oldP={}, newP={}){
    // remove
    for(const k in oldP){ if(!(k in newP)){ try{ el.removeAttribute(k); }catch{} } }
    // add/update
    for(const k in newP){ const v=newP[k]; try{ if(v===false||v===null||typeof v==='undefined'){ el.removeAttribute(k);} else { el.setAttribute(k, String(v)); } }catch{} }
  }
  function diffStyles(el, oldS={}, newS={}){
    for(const k in oldS){ if(!(k in newS)){ try{ el.style.removeProperty(k.replace(/_/g,'-')); }catch{} } }
    for(const k in newS){ const v=newS[k]; try{ el.style.setProperty(k.replace(/_/g,'-'), String(v)); }catch{} }
  }

  // Event delegation helper (restored)
  function delegate(eventName, root){
    (root||document).addEventListener(eventName, function(e){
      let node = e.target;
      const boundary = root||document;
      while(node && node !== boundary){
        const id = node.id;
        if(id && eventMap.has(id)){
          const handlers = eventMap.get(id);
          const h = handlers[eventName];
          if(typeof h === 'function'){
            try { h.call(node, e); } catch(err){ console.error('[Dars] handler error', err); }
            return;
          }
        }
        node = node.parentNode;
      }
    }, true);
  }

  function typesDiffer(a,b){ return (a && b) ? a.type !== b.type : a!==b; }

  // Elimina un subárbol del DOM (y del mapa de eventos) usando los ids del VDOM
  function removeSubtree(v){
    if(!v) return;
    // eliminar hijos primero (postorden)
    const ch = (v.children||[]);
    for(let i=0;i<ch.length;i++){ removeSubtree(ch[i]); }
    // limpiar handlers
    if(v.id){ eventMap.delete(v.id); }
    // quitar elemento del DOM
    if(v.id){ const el = document.getElementById(v.id); if(el && el.parentNode){ try{ el.parentNode.removeChild(el); }catch(_){} }}
  }

  function updateNode(oldV, newV){
    if(!newV || !newV.id){ return { ok:false, reason:'missing-new' }; }
    let el = document.getElementById(newV.id);
    if(!el){
      // Fallback: si cambió el id entre snapshots pero es el mismo nodo lógico, reasignamos id
      const oldEl = (oldV && oldV.id) ? document.getElementById(oldV.id) : null;
      if(oldEl){ try { oldEl.id = newV.id; el = oldEl; } catch(_){} }
    }
    if(!el){ return { ok:false, reason:'missing-el' }; }

    // Si cambia el tipo, estructura u orden de hijos, pedimos reload completo (fase 2 simplificada)
    if(typesDiffer(oldV, newV)){
      return { ok:false, reason:'type-changed' };
    }

    const isIsland = !!newV.isIsland;

    // class -> atributo className
    if(!isIsland && newV.class){ el.className = newV.class; }

    // props
    if(!isIsland){ diffProps(el, (oldV&&oldV.props)||{}, newV.props||{}); }

    // styles
    if(!isIsland){ diffStyles(el, (oldV&&oldV.style)||{}, newV.style||{}); }

    // text
    if(!isIsland && Object.prototype.hasOwnProperty.call(newV, 'text')){
      if(el.textContent !== String(newV.text||'')){
        el.textContent = String(newV.text||'');
      }
    }

    // events
    if(newV.events){
      const handlers = {};
      for(const ev in newV.events){
        const spec = newV.events[ev];
        if(spec && spec.type==='inline' && spec.code){
          try { handlers[ev] = new Function('event', spec.code); } catch(err){ /* ignore compile error */ }
        }
      }
      if(Object.keys(handlers).length){ eventMap.set(newV.id, handlers); } else { eventMap.delete(newV.id); }
    } else {
      eventMap.delete(newV.id);
    }

    // hijos (reconciliación por id/key). Para islas, tratamos el subárbol como opaco.
    if(isIsland){ return { ok:true }; }

    // Permitimos REMOCIONES sin recarga.
    const oldC = (oldV && oldV.children) ? oldV.children : [];
    const newC = (newV.children) ? newV.children : [];

    // Construir índice de hijos viejos por id o key
    const oldIndex = new Map(); // clave -> vnode viejo
    for(let i=0;i<oldC.length;i++){
      const k = (oldC[i] && (oldC[i].id || oldC[i].key)) || null;
      if(k){ oldIndex.set(String(k), oldC[i]); }
    }

    // Seguimiento de cuáles viejos fueron actualizados
    const seenOld = new Set();

    // Actualizar/validar hijos nuevos
    for(let i=0;i<newC.length;i++){
      const newChild = newC[i];
      const k = (newChild && (newChild.id || newChild.key)) || null;
      if(!k){
        // sin id/key fiable: conservador => usar reconciliación por índice si existe par
        if(i < oldC.length){
          const r = updateNode(oldC[i], newChild);
          if(!r.ok){ return r; }
          seenOld.add(oldC[i]);
          continue;
        } else {
          // no podemos crear de forma segura
          return { ok:false, reason:'children-added' };
        }
      }
      const oldChild = oldIndex.get(String(k));
      if(oldChild){
        const r = updateNode(oldChild, newChild);
        if(!r.ok){ return r; }
        seenOld.add(oldChild);
      } else {
        // Fallback conservador: si hay viejo en la misma posición y el tipo coincide, lo reutilizamos
        if(i < oldC.length){
          const candidate = oldC[i];
          if(!typesDiffer(candidate, newChild)){
            const r = updateNode(candidate, newChild);
            if(!r.ok){ return r; }
            seenOld.add(candidate);
            continue;
          }
        }
        // Intentar crear subárbol si es un tipo soportado por el registry (no isla)
        const subtree = createSubtree(newChild);
        if(subtree){
          // insertar en la posición i dentro del DOM
          const refChildVNode = (i < oldC.length) ? oldC[i] : null;
          if(refChildVNode && refChildVNode.id){
            const refEl = document.getElementById(refChildVNode.id);
            if(refEl && refEl.parentNode){ refEl.parentNode.insertBefore(subtree, refEl); }
            else { el.appendChild(subtree); }
          } else {
            el.appendChild(subtree);
          }
          // marcar como visto (no había old), nada que añadir a seenOld
          continue;
        }
        // hijo nuevo de tipo no soportado => recarga por seguridad
        return { ok:false, reason:'children-added' };
      }
    }

    // Eliminar los viejos no vistos (removidos)
    for(let i=0;i<oldC.length;i++){
      const v = oldC[i];
      if(!seenOld.has(v)){
        removeSubtree(v);
      }
    }
    return { ok:true };
  }

  function schedule(fn){
    if(typeof requestAnimationFrame === 'function'){
      requestAnimationFrame(fn);
    } else { setTimeout(fn, 16); }
  }

  function update(newSnapshot){
    const old = currentSnapshot;
    if(!old){
      // primera vez: solo (re)hidratar eventos
      bindEventsFromVNode(newSnapshot);
      currentSnapshot = newSnapshot;
      try{ window.__DARS_VDOM__ = newSnapshot; }catch(_){ /* ignore */ }
      return;
    }
    schedule(()=>{
      const res = updateNode(old, newSnapshot);
      if(!res.ok){
        console.warn('[Dars] Structural change detected (', res.reason, '), reloading...');
        try { location.reload(); } catch(e) { /* ignore */ }
        return;
      }
      // Re-vincular mapa de eventos por si cambió
      bindEventsFromVNode(newSnapshot);
      currentSnapshot = newSnapshot;
      try{ window.__DARS_VDOM__ = newSnapshot; }catch(_){ /* ignore */ }
    });
  }

  function hydrate(snapshot){
    bindEventsFromVNode(snapshot);
    currentSnapshot = snapshot;
    try{ window.__DARS_VDOM__ = snapshot; }catch(_){ /* ignore */ }

    // Delegar eventos comunes (extendido)
    const delegated = [
      'click','dblclick',
      'mousedown','mouseup','mouseenter','mouseleave','mousemove',
      'keydown','keyup','keypress',
      'change','input','submit',
      'focus','blur'
    ];
    delegated.forEach(ev => delegate(ev, document));
  }

  function startHotReload(){
    const vurl = (window.__DARS_VERSION_URL || 'version.txt');
    let timer = null;
    let warnedVersionMissing = false;

    function httpGet(url, onSuccess, onError, responseType){
      try{
        const xhr = new XMLHttpRequest();
        if(responseType){ xhr.responseType = responseType; }
        xhr.open('GET', url, true);
        xhr.timeout = 5000;
        xhr.onreadystatechange = function(){
          if(xhr.readyState === 4){
            if(xhr.status >= 200 && xhr.status < 300){
              onSuccess(xhr.response);
            } else {
              onError();
            }
          }
        };
        xhr.onerror = onError;
        xhr.ontimeout = onError;
        xhr.setRequestHeader('Cache-Control', 'no-store');
        xhr.send();
      }catch(e){ onError(); }
    }

    function tick(){
      httpGet(vurl, function(text){
        let ver = (text || '').toString().trim();
        if(ver){ warnedVersionMissing = false; }
        if(!currentVersion){ currentVersion = ver; }
        if(ver && ver !== currentVersion){
          currentVersion = ver;
          // Política solicitada: siempre recargar por completo al detectar nueva versión
          try { location.reload(); } catch(_) {}
          return;
        }
        timer = setTimeout(tick, 600);
      }, function(){
        if(!warnedVersionMissing){ console.log('[Dars] waiting for version.txt'); warnedVersionMissing = true; }
        timer = setTimeout(tick, 600);
      }, 'text');
    }
    tick();
    return ()=>{ if(timer) clearTimeout(timer); };
  }

  document.addEventListener('DOMContentLoaded', function(){
    if(window.__DARS_VDOM__){
      hydrate(window.__DARS_VDOM__);
    } else {
      console.warn('[Dars] No VDOM snapshot found for hydration');
    }
    // Activar hot-reload incremental en dev si hay URLs definidas
    if(window.__DARS_VERSION_URL && window.__DARS_SNAPSHOT_URL){
      startHotReload();
    }
  });
})();
