(()=>{var c=Object.create;var s=Object.defineProperty;var l=Object.getOwnPropertyDescriptor;var m=Object.getOwnPropertyNames;var p=Object.getPrototypeOf,u=Object.prototype.hasOwnProperty;var f=(e,n,o,t)=>{if(n&&typeof n=="object"||typeof n=="function")for(let i of m(n))!u.call(e,i)&&i!==o&&s(e,i,{get:()=>n[i],enumerable:!(t=l(n,i))||t.enumerable});return e};var d=(e,n,o)=>(o=e!=null?c(p(e)):{},f(n||!e||!e.__esModule?s(o,"default",{value:e,enumerable:!0}):o,e));(function(){function e(){var t=document.getElementById("image_0_0_0_0_0");t&&t.addEventListener("click",async function(r){if(!window.Dars)try{const a=await import("./lib/dars.min.js");window.Dars=a.default||a}catch{}try{window.location.href="https://ztamdev.github.io/Dars-Framework/"}catch(a){console.error("Error en handler:",a)}});var i=document.getElementById("text_0_0_0_0_1");i&&i.addEventListener("click",async function(r){if(!window.Dars)try{const a=await import("./lib/dars.min.js");window.Dars=a.default||a}catch{}try{window.location.href="https://ztamdev.github.io/Dars-Framework/"}catch(a){console.error("Error en handler:",a)}})}function n(){try{const t=[{name:"counter",id:"counter",defaultValue:{count:0},isV2:!0}];window.Dars&&typeof window.Dars.registerStates=="function"?window.Dars.registerStates(t):window.__DARS_STATES_FN?window.__DARS_STATES_FN(t):(async()=>{try{const i=await import("./lib/dars.min.js"),r=i.registerStates||i.default&&i.default.registerStates;typeof r=="function"&&(r(t),window.__DARS_STATES_FN=r)}catch(i){console.error("[Dars] Failed to initialize states",i)}})()}catch(t){console.error("[Dars] State initialization error",t)}}function o(){(async()=>{try{const t=await import("./lib/dap.js");t.__darsConfig&&(t.__darsConfig.allowInlineJS=!0)}catch{}})(),window.__DARS_SPA_CONFIG__?window.__DARS_SPA_CONFIG__.backendUrl||(window.__DARS_SPA_CONFIG__.backendUrl="/"):window.__DARS_SPA_CONFIG__={backendUrl:"/"},n(),e();try{window.Dars&&typeof window.Dars.addReactiveBinding=="function"?window.Dars.addReactiveBinding(function(t){if(t&&t.dynamic&&t.id&&t.id==="counter"){let i;if(t.attrs&&t.attrs.count!==void 0?i=t.attrs.count:t.count!==void 0&&(i=t.count),i!==void 0){const r=document.getElementById("demo-counter-value");r&&(r.hasAttribute("data-server-component")&&r.firstElementChild?r.firstElementChild.textContent=String(i):r.textContent=String(i),r.hasAttribute("data-server-component")&&r.firstElementChild?r.firstElementChild.textContent=String(i):r.textContent=String(i),r.hasAttribute("data-server-component")&&r.firstElementChild?r.firstElementChild.textContent=String(i):r.textContent=String(i),r.hasAttribute("data-server-component")&&r.firstElementChild?r.firstElementChild.textContent=String(i):r.textContent=String(i),r.hasAttribute("data-server-component")&&r.firstElementChild?r.firstElementChild.textContent=String(i):r.textContent=String(i),r.hasAttribute("data-server-component")&&r.firstElementChild?r.firstElementChild.textContent=String(i):r.textContent=String(i))}}}):console.warn("[Dars:Debug] window.Dars.addReactiveBinding NOT found. Skipping reactive bindings.")}catch(t){console.error("[Dars] Failed to initialize reactive bindings",t)}(async()=>{try{const t=await import("./lib/dap.js");t._initConditionalElements&&await t._initConditionalElements({})}catch{}})()}document.readyState==="complete"||document.readyState==="interactive"?o():document.addEventListener("DOMContentLoaded",o)})();window.addEventListener("scroll",()=>{const e=document.getElementById("dars-navbar");e&&(window.scrollY>20?e.classList.add("scrolled"):e.classList.remove("scrolled"))});document.addEventListener("DOMContentLoaded",function(){const e=document.getElementById("hamburger-btn"),n=document.getElementById("mobile-menu"),o=document.body;e&&n&&(e.addEventListener("click",function(t){t.stopPropagation(),n.style.display==="flex"?(n.style.display="none",e.classList.remove("menu-open"),o.classList.remove("menu-open")):(n.style.display="flex",e.classList.add("menu-open"),o.classList.add("menu-open"))}),n.querySelectorAll("a").forEach(t=>{t.addEventListener("click",function(){n.style.display="none",e.classList.remove("menu-open"),o.classList.remove("menu-open")})}),document.addEventListener("click",function(t){!e.contains(t.target)&&!n.contains(t.target)&&(n.style.display="none",e.classList.remove("menu-open"),o.classList.remove("menu-open"))}),document.addEventListener("keydown",function(t){t.key==="Escape"&&n.style.display==="flex"&&(n.style.display="none",e.classList.remove("menu-open"),o.classList.remove("menu-open"))}))});(function(){var e=document.getElementById("markdown-layout");if(e){var n=document.createElement("style");n.textContent=`
        /* Enhanced docs tables */
        #markdown-content-container table {
            border-collapse: separate;
            border-spacing: 0;
            border-radius: 8px;
            overflow: hidden;
            border: 1px solid rgba(146, 255, 229, 0.1);
            width: 100%;
            margin: 16px 0;
        }
        #markdown-content-container th {
            background: rgba(16, 185, 129, 0.1) !important;
            border-bottom: 1px solid rgba(146, 255, 229, 0.12) !important;
            padding: 10px 14px !important;
            font-weight: 600;
            text-align: left;
            font-size: 13px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            color: #92ffe5;
        }
        #markdown-content-container td {
            padding: 10px 14px !important;
            border-bottom: 1px solid rgba(255,255,255,0.03) !important;
        }
        #markdown-content-container tr:last-child td {
            border-bottom: none !important;
        }

        /* Blockquote styling */
        #markdown-content-container blockquote {
            border-left: 3px solid #10b981;
            background: rgba(16, 185, 129, 0.06);
            padding: 12px 20px;
            border-radius: 0 8px 8px 0;
            margin: 16px 0;
        }

        /* HR dividers */
        #markdown-content-container hr {
            border: none;
            height: 1px;
            background: linear-gradient(90deg, transparent, rgba(146,255,229,0.12), transparent);
            margin: 32px 0;
        }

        /* Code inline */
        #markdown-content-container code:not(pre code) {
            background: rgba(146, 255, 229, 0.08);
            border: 1px solid rgba(146, 255, 229, 0.1);
            border-radius: 4px;
            padding: 2px 6px;
            font-size: 0.9em;
        }
    `,document.head.appendChild(n)}})();(function(){var e=document.getElementById("markdown-layout");if(e){var n=document.createElement("style");n.textContent=`
        /* Enhanced docs tables */
        #markdown-content-container table {
            border-collapse: separate;
            border-spacing: 0;
            border-radius: 8px;
            overflow: hidden;
            border: 1px solid rgba(146, 255, 229, 0.1);
            width: 100%;
            margin: 16px 0;
        }
        #markdown-content-container th {
            background: rgba(16, 185, 129, 0.1) !important;
            border-bottom: 1px solid rgba(146, 255, 229, 0.12) !important;
            padding: 10px 14px !important;
            font-weight: 600;
            text-align: left;
            font-size: 13px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            color: #92ffe5;
        }
        #markdown-content-container td {
            padding: 10px 14px !important;
            border-bottom: 1px solid rgba(255,255,255,0.03) !important;
        }
        #markdown-content-container tr:last-child td {
            border-bottom: none !important;
        }

        /* Blockquote styling */
        #markdown-content-container blockquote {
            border-left: 3px solid #10b981;
            background: rgba(16, 185, 129, 0.06);
            padding: 12px 20px;
            border-radius: 0 8px 8px 0;
            margin: 16px 0;
        }

        /* HR dividers */
        #markdown-content-container hr {
            border: none;
            height: 1px;
            background: linear-gradient(90deg, transparent, rgba(146,255,229,0.12), transparent);
            margin: 32px 0;
        }

        /* Code inline */
        #markdown-content-container code:not(pre code) {
            background: rgba(146, 255, 229, 0.08);
            border: 1px solid rgba(146, 255, 229, 0.1);
            border-radius: 4px;
            padding: 2px 6px;
            font-size: 0.9em;
        }
    `,document.head.appendChild(n)}})();window.Prism=window.Prism||{};Prism.plugins=Prism.plugins||{};Prism.plugins.autoloader=Prism.plugins.autoloader||{};Prism.plugins.autoloader.languages_path="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/";(function(){window.DarsMarkdown={_retries:0,addCopyButtons:function(e){(e||document).querySelectorAll("pre code").forEach(function(n){var o=n.parentElement;if(!(!o||o.querySelector(".dars-code-copy"))){getComputedStyle(o).position==="static"&&(o.style.position="relative");var t=document.createElement("button");t.className="dars-code-copy",t.type="button",t.textContent="Copy",t.addEventListener("click",async function(i){i.stopPropagation();try{await navigator.clipboard.writeText(n.innerText),t.textContent="Copied",t.classList.add("copied"),setTimeout(function(){t.textContent="Copy",t.classList.remove("copied")},1200)}catch{t.textContent="Error",setTimeout(function(){t.textContent="Copy"},1200)}}),o.appendChild(t)}})},guessLang:function(e){var n=e.trim();return/^{[\s\S]*}$/.test(n)||/^\[/.test(n)?"json":/^(pip |python |python3 |dars |#|\$ )/m.test(n)?"bash":/\b(def |class |import |from |print\(|self\b)/.test(n)?"python":null},stripPygments:function(e){e&&e.innerHTML&&e.innerHTML.indexOf("<span")!==-1&&(e.textContent=e.innerText)},highlight:function(e){var n=this;if(!window.Prism||!Prism.highlightElement){n._retries<20&&(n._retries++,setTimeout(function(){n.highlight(e)},150));return}(e||document).querySelectorAll("pre code").forEach(function(o){if(n.stripPygments(o),!o.className||o.className.indexOf("language-")===-1){var t=n.guessLang(o.innerText);o.classList.add("language-"+(t||"none"))}Prism.highlightElement(o)}),n.addCopyButtons(e)}},document.readyState==="complete"?window.DarsMarkdown.highlight():window.addEventListener("load",function(){window.DarsMarkdown.highlight()}),document.addEventListener("DOMContentLoaded",function(){window.DarsMarkdown.highlight()}),document.addEventListener("dars:content-loaded",function(e){e.detail&&e.detail.element&&window.DarsMarkdown.highlight(e.detail.element)})})();})();
