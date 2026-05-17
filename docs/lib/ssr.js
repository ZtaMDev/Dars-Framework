import{registerStates}from"./dars.min.js";export function _executeExternalScript(code,context){if(!code)return null;try{const s=document.createElement("script");const ctxId="__dars_ctx_"+Math.random().toString(36).substr(2,9);if(context)window[ctxId]=context;const setup=context?`const event = window["${ctxId}"].event; const element = window["${ctxId}"].element; delete window["${ctxId}"];`:"";s.textContent=`(async () => { 
          ${setup}
          try { 
              ${code} 
          } catch(e) { 
              console.error('[Dars] Script execution error:', e); 
          } 
      })();`;document.body.appendChild(s);s.remove();}catch(e){console.error("[Dars:Security] Error executing external script:",e);}
return null;}
try{if(typeof window!=="undefined"&&Array.isArray(window.__DARS_STATE_V2__)){Dars.stateV2Snapshot=window.__DARS_STATE_V2__;}}catch(_){}
export function updatePageMetadata(metadata){if(!metadata)return;try{if(metadata.title){document.title=metadata.title;}
_updateMeta("description",metadata.description);_updateMeta("author",metadata.author);_updateMeta("robots",metadata.robots);if(metadata.keywords){const kw=Array.isArray(metadata.keywords)?metadata.keywords.join(", "):metadata.keywords;_updateMeta("keywords",kw);}
if(metadata.canonical){_updateLink("canonical",metadata.canonical);}
if(metadata.favicon){_updateLink("icon",metadata.favicon);}
const og=metadata.og||{};_updateMeta("og:title",og.title,"property");_updateMeta("og:description",og.description,"property");_updateMeta("og:image",og.image,"property");_updateMeta("og:type",og.type,"property");_updateMeta("og:url",og.url,"property");_updateMeta("og:site_name",og.site_name,"property");_updateMeta("og:locale",og.locale,"property");const twitter=metadata.twitter||{};_updateMeta("twitter:card",twitter.card);_updateMeta("twitter:site",twitter.site);_updateMeta("twitter:creator",twitter.creator);_updateMeta("twitter:title",twitter.title);_updateMeta("twitter:description",twitter.description);_updateMeta("twitter:image",twitter.image);}catch(e){try{console.error("[Dars] Metadata update error:",e);}catch(_){}}}
export function _updateMeta(name,content,attr){attr=attr||"name";if(!content)return;try{let meta=document.querySelector(`meta[${attr}="${name}"]`);if(!meta){meta=document.createElement("meta");meta.setAttribute(attr,name);document.head.appendChild(meta);}
meta.setAttribute("content",String(content));}catch(_){}}
export function _updateLink(rel,href){if(!href)return;try{let link=document.querySelector(`link[rel="${rel}"]`);if(!link){link=document.createElement("link");link.setAttribute("rel",rel);document.head.appendChild(link);}
link.setAttribute("href",String(href));}catch(_){}}
try{window.Dars=window.Dars||Dars;}catch(_){}
try{const dspScript=document.getElementById("__DARS_DSP_DATA__");if(dspScript){if(dspScript.type==="application/json"){try{const payload=JSON.parse(dspScript.textContent);if(payload){if(!window.__DARS_SPA_CONFIG__&&payload.spaConfig)
window.__DARS_SPA_CONFIG__=payload.spaConfig;if(!window.__ROUTE_VDOM__&&payload.vdom)
window.__ROUTE_VDOM__=payload.vdom;if(!window.__DARS_STATE__&&payload.states)
window.__DARS_STATE__=payload.states;if(!window.__DARS_STATE_V2__&&payload.statesV2)
window.__DARS_STATE_V2__=payload.statesV2;if(payload.events){_attachEventsMap(payload.events);}
if(payload.styles){let styleReg=document.getElementById("dars-style-registry");if(!styleReg){styleReg=document.createElement("style");styleReg.id="dars-style-registry";document.head.appendChild(styleReg);}
styleReg.textContent=payload.styles;}
if(payload.reactiveBindings){try{const s=document.createElement("script");s.textContent=payload.reactiveBindings;document.body.appendChild(s);s.remove();}catch(e){console.error("[Dars] Reactive bindings error:",e);}}
if(payload.vrefBindings){try{const s=document.createElement("script");s.textContent=payload.vrefBindings;document.body.appendChild(s);s.remove();}catch(e){console.error("[Dars] VRef bindings error:",e);}}
if(payload.metaTags){const temp=document.createElement("div");const sanitized=(typeof DOMPurify!=="undefined")?DOMPurify.sanitize(payload.metaTags,{FORCE_BODY:true}):payload.metaTags.replace(/<script[\s\S]*?<\/script>/gi,"");temp.innerHTML=sanitized;const newMetas=temp.childNodes;for(let i=0;i<newMetas.length;i++){const node=newMetas[i];if(node.nodeType===1){const tag=node.tagName.toLowerCase();if(!["meta","link","title"].includes(tag))continue;const attr=node.getAttribute("name")||node.getAttribute("property");let existing=null;if(attr){existing=document.head.querySelector(`${tag}[name="${attr}"], ${tag}[property="${attr}"]`,);}
if(existing){existing.content=node.getAttribute("content");}else{document.head.appendChild(node.cloneNode(true));}}}}}else{console.warn("[Dars:Hydration] Payload is empty or falsy");}}catch(e){console.error("[Dars] Failed to parse DSP payload:",e);}}}
if(typeof window!=="undefined"&&Array.isArray(window.__DARS_STATE__)){if(window.Dars&&window.Dars.registerStates){window.Dars.registerStates(window.__DARS_STATE__);}else if(typeof registerStates==="function"){registerStates(window.__DARS_STATE__);}}
if(typeof window!=="undefined"&&Array.isArray(window.__DARS_STATE_V2__)){if(window.Dars&&window.Dars.registerStates){window.Dars.registerStates(window.__DARS_STATE_V2__);}else if(typeof registerStates==="function"){registerStates(window.__DARS_STATE_V2__);}}}catch(err){console.error("[Dars:Debug] Critical error during hydration block:",err);}