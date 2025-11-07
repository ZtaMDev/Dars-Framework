(function(){const eventMap=new Map();let currentSnapshot=null;let currentVersion=null;const registry={'Text':{create(v){if(!v||v.isIsland)return null;const el=document.createElement('span');if(v.id)el.id=v.id;if(v.class)el.className=v.class;if(v.style){for(const k in v.style){try{el.style.setProperty(k.replace(/_/g,'-'),String(v.style[k]));}catch{}}}
if(Object.prototype.hasOwnProperty.call(v,'text')){el.textContent=String(v.text||'');}
if(v.props){for(const k in v.props){const val=v.props[k];try{if(val===false||val===null||typeof val==='undefined'){el.removeAttribute(k);}else{el.setAttribute(k,String(val));}}catch{}}}
return el;}},'Container':{create(v){if(!v||v.isIsland)return null;const el=document.createElement('div');if(v.id)el.id=v.id;const base='dars-container';el.className=(v.class?(base+' '+v.class):base);if(v.style){for(const k in v.style){try{el.style.setProperty(k.replace(/_/g,'-'),String(v.style[k]));}catch{}}}
if(v.props){for(const k in v.props){const val=v.props[k];try{if(val===false||val===null||typeof val==='undefined'){el.removeAttribute(k);}else{el.setAttribute(k,String(val));}}catch{}}}
return el;}},};function walk(v,fn){if(!v)return;fn(v);const ch=v.children||[];for(let i=0;i<ch.length;i++){walk(ch[i],fn);}}
function _decodeCodeB64(b64){try{if(typeof atob==='function')return atob(b64);if(typeof Buffer!=='undefined'){return Buffer.from(b64,'base64').toString('utf8');}}catch(_){}
return'';}
function _compileHandlerFromSpec(spec){try{if(!spec)return null;if(spec&&spec.type==='inline'&&spec.code){return new Function('event',spec.code);}
const b64=(spec&&(spec.b||spec.code_b64))||null;if(b64){const code=_decodeCodeB64(b64);if(code)return new Function('event',code);}}catch(_){}
return null;}
function bindEventsFromVNode(snapshot){walk(snapshot,(v)=>{if(v&&v.id&&v.events){const handlers={};for(const ev in v.events){const spec=v.events[ev];const fn=_compileHandlerFromSpec(spec);if(fn){handlers[ev]=fn;}}
if(Object.keys(handlers).length){eventMap.set(v.id,handlers);}else{eventMap.delete(v.id);}}});}
function setProps(el,props){if(!el||!props)return;for(const[k,v]of Object.entries(props)){try{if(v===false||v===null||typeof v==='undefined'){el.removeAttribute(k);}else{el.setAttribute(k,String(v));}}catch(err){}}}
function diffProps(el,oldP={},newP={}){for(const k in oldP){if(!(k in newP)){try{el.removeAttribute(k);}catch{}}}
for(const k in newP){const v=newP[k];try{if(v===false||v===null||typeof v==='undefined'){el.removeAttribute(k);}else{el.setAttribute(k,String(v));}}catch{}}}
function diffStyles(el,oldS={},newS={}){for(const k in oldS){if(!(k in newS)){try{el.style.removeProperty(k.replace(/_/g,'-'));}catch{}}}
for(const k in newS){const v=newS[k];try{el.style.setProperty(k.replace(/_/g,'-'),String(v));}catch{}}}
function delegate(eventName,root){(root||document).addEventListener(eventName,function(e){let node=e.target;const boundary=root||document;while(node&&node!==boundary){const id=node.id;if(id&&eventMap.has(id)){const handlers=eventMap.get(id);const h=handlers[eventName];if(typeof h==='function'){try{h.call(node,e);}catch(err){console.error('[Dars] handler error',err);}
return;}}
node=node.parentNode;}},true);}
function typesDiffer(a,b){return(a&&b)?a.type!==b.type:a!==b;}
function removeSubtree(v){if(!v)return;const ch=(v.children||[]);for(let i=0;i<ch.length;i++){removeSubtree(ch[i]);}
if(v.id){eventMap.delete(v.id);}
if(v.id){const el=document.getElementById(v.id);if(el&&el.parentNode){try{el.parentNode.removeChild(el);}catch(_){}}}}
function updateNode(oldV,newV){if(!newV||!newV.id){return{ok:false,reason:'missing-new'};}
let el=document.getElementById(newV.id);if(!el){const oldEl=(oldV&&oldV.id)?document.getElementById(oldV.id):null;if(oldEl){try{oldEl.id=newV.id;el=oldEl;}catch(_){}}}
if(!el){return{ok:false,reason:'missing-el'};}
if(typesDiffer(oldV,newV)){return{ok:false,reason:'type-changed'};}
const isIsland=!!newV.isIsland;if(!isIsland&&newV.class){el.className=newV.class;}
if(!isIsland){diffProps(el,(oldV&&oldV.props)||{},newV.props||{});}
if(!isIsland){diffStyles(el,(oldV&&oldV.style)||{},newV.style||{});}
if(!isIsland&&Object.prototype.hasOwnProperty.call(newV,'text')){if(el.textContent!==String(newV.text||'')){el.textContent=String(newV.text||'');}}
if(newV.events){const handlers={};for(const ev in newV.events){const spec=newV.events[ev];const fn=_compileHandlerFromSpec(spec);if(fn){handlers[ev]=fn;}}
if(Object.keys(handlers).length){eventMap.set(newV.id,handlers);}else{eventMap.delete(newV.id);}}else{eventMap.delete(newV.id);}
if(isIsland){return{ok:true};}
const oldC=(oldV&&oldV.children)?oldV.children:[];const newC=(newV.children)?newV.children:[];const oldIndex=new Map();for(let i=0;i<oldC.length;i++){const k=(oldC[i]&&(oldC[i].id||oldC[i].key))||null;if(k){oldIndex.set(String(k),oldC[i]);}}
const seenOld=new Set();for(let i=0;i<newC.length;i++){const newChild=newC[i];const k=(newChild&&(newChild.id||newChild.key))||null;if(!k){if(i<oldC.length){const r=updateNode(oldC[i],newChild);if(!r.ok){return r;}
seenOld.add(oldC[i]);continue;}else{return{ok:false,reason:'children-added'};}}
const oldChild=oldIndex.get(String(k));if(oldChild){const r=updateNode(oldChild,newChild);if(!r.ok){return r;}
seenOld.add(oldChild);}else{if(i<oldC.length){const candidate=oldC[i];if(!typesDiffer(candidate,newChild)){const r=updateNode(candidate,newChild);if(!r.ok){return r;}
seenOld.add(candidate);continue;}}
const subtree=createSubtree(newChild);if(subtree){const refChildVNode=(i<oldC.length)?oldC[i]:null;if(refChildVNode&&refChildVNode.id){const refEl=document.getElementById(refChildVNode.id);if(refEl&&refEl.parentNode){refEl.parentNode.insertBefore(subtree,refEl);}
else{el.appendChild(subtree);}}else{el.appendChild(subtree);}
continue;}
return{ok:false,reason:'children-added'};}}
for(let i=0;i<oldC.length;i++){const v=oldC[i];if(!seenOld.has(v)){removeSubtree(v);}}
return{ok:true};}
function schedule(fn){if(typeof requestAnimationFrame==='function'){requestAnimationFrame(fn);}else{setTimeout(fn,16);}}
function update(newSnapshot){const old=currentSnapshot;if(!old){bindEventsFromVNode(newSnapshot);currentSnapshot=newSnapshot;try{window.__DARS_VDOM__=newSnapshot;}catch(_){}
return;}
schedule(()=>{const res=updateNode(old,newSnapshot);if(!res.ok){console.warn('[Dars] Structural change detected (',res.reason,'), reloading...');try{location.reload();}catch(e){}
return;}
bindEventsFromVNode(newSnapshot);currentSnapshot=newSnapshot;try{window.__DARS_VDOM__=newSnapshot;}catch(_){}});}
function hydrate(snapshot){bindEventsFromVNode(snapshot);currentSnapshot=snapshot;try{window.__DARS_VDOM__=snapshot;}catch(_){}
const delegated=['click','dblclick','mousedown','mouseup','mouseenter','mouseleave','mousemove','keydown','keyup','keypress','change','input','submit','focus','blur'];delegated.forEach(ev=>delegate(ev,document));}
function startHotReload(){const vurl=(window.__DARS_VERSION_URL||'version.txt');let timer=null;let warnedVersionMissing=false;function httpGet(url,onSuccess,onError,responseType){try{const xhr=new XMLHttpRequest();if(responseType){xhr.responseType=responseType;}
xhr.open('GET',url,true);xhr.timeout=5000;xhr.onreadystatechange=function(){if(xhr.readyState===4){if(xhr.status>=200&&xhr.status<300){onSuccess(xhr.response);}else{onError();}}};xhr.onerror=onError;xhr.ontimeout=onError;xhr.setRequestHeader('Cache-Control','no-store');xhr.send();}catch(e){onError();}}
function tick(){httpGet(vurl,function(text){let ver=(text||'').toString().trim();if(ver){warnedVersionMissing=false;}
if(!currentVersion){currentVersion=ver;}
if(ver&&ver!==currentVersion){currentVersion=ver;try{location.reload();}catch(_){}
return;}
timer=setTimeout(tick,600);},function(){if(!warnedVersionMissing){console.log('[Dars] waiting for version.txt');warnedVersionMissing=true;}
timer=setTimeout(tick,600);},'text');}
tick();return()=>{if(timer)clearTimeout(timer);};}
document.addEventListener('DOMContentLoaded',function(){if(window.__DARS_VDOM__){hydrate(window.__DARS_VDOM__);}else{console.warn('[Dars] No VDOM snapshot found for hydration');}
if(window.__DARS_VERSION_URL&&window.__DARS_SNAPSHOT_URL){startHotReload();}});})();