(function(){function t(){var t,e;(async()=>{try{let t=await import("./lib/dap.js");t.__darsConfig&&(t.__darsConfig.allowInlineJS=!0);}catch(t){}})(),window.__DARS_SPA_CONFIG__?window.__DARS_SPA_CONFIG__.backendUrl||(window.__DARS_SPA_CONFIG__.backendUrl="/"):window.__DARS_SPA_CONFIG__={backendUrl:"/"},function(){try{let t=[{name:"counter",id:"counter",defaultValue:{count:0},isV2:!0}];window.Dars&&"function"==typeof window.Dars.registerStates?window.Dars.registerStates(t):window.__DARS_STATES_FN?window.__DARS_STATES_FN(t):(async()=>{try{let e=await import("./lib/dars.min.js"),n=e.registerStates||e.default&&e.default.registerStates;"function"==typeof n&&(n(t),window.__DARS_STATES_FN=n);}catch(t){console.error("[Dars] Failed to initialize states",t);}})();}catch(t){console.error("[Dars] State initialization error",t);}}(),(t=document.getElementById("image_0_1_0_0_0"))&&t.addEventListener("click",async function(t){if(!window.Dars)try{let t=await import("./lib/dars.min.js");window.Dars=t.default||t;}catch(t){}try{window.location.href="https://ztamdev.github.io/Dars-Framework/";}catch(t){console.error("Error en handler:",t);}}),(e=document.getElementById("text_0_1_0_0_1"))&&e.addEventListener("click",async function(t){if(!window.Dars)try{let t=await import("./lib/dars.min.js");window.Dars=t.default||t;}catch(t){}try{window.location.href="https://ztamdev.github.io/Dars-Framework/";}catch(t){console.error("Error en handler:",t);}});try{window.Dars&&"function"==typeof window.Dars.addReactiveBinding?window.Dars.addReactiveBinding(function(t){if(t&&t.dynamic&&t.id&&"counter"===t.id){let e;if(t.attrs&&void 0!==t.attrs.count?e=t.attrs.count:void 0!==t.count&&(e=t.count),void 0!==e){let t=document.getElementById("demo-counter-value");t&&(t.hasAttribute("data-server-component")&&t.firstElementChild?t.firstElementChild.textContent=String(e):t.textContent=String(e),t.hasAttribute("data-server-component")&&t.firstElementChild?t.firstElementChild.textContent=String(e):t.textContent=String(e),t.hasAttribute("data-server-component")&&t.firstElementChild?t.firstElementChild.textContent=String(e):t.textContent=String(e),t.hasAttribute("data-server-component")&&t.firstElementChild?t.firstElementChild.textContent=String(e):t.textContent=String(e),t.hasAttribute("data-server-component")&&t.firstElementChild?t.firstElementChild.textContent=String(e):t.textContent=String(e),t.hasAttribute("data-server-component")&&t.firstElementChild?t.firstElementChild.textContent=String(e):t.textContent=String(e));}}}):console.warn("[Dars:Debug] window.Dars.addReactiveBinding NOT found. Skipping reactive bindings.");}catch(t){console.error("[Dars] Failed to initialize reactive bindings",t);}(async()=>{try{let t=await import("./lib/dap.js");t._initConditionalElements&&await t._initConditionalElements({});}catch(t){}})();}"complete"===document.readyState||"interactive"===document.readyState?t():document.addEventListener("DOMContentLoaded",t);})(),window.addEventListener("scroll",()=>{let t=document.getElementById("dars-navbar");t&&(window.scrollY>20?t.classList.add("scrolled"):t.classList.remove("scrolled"));}),document.addEventListener("DOMContentLoaded",function(){let t=document.getElementById("hamburger-btn"),e=document.getElementById("mobile-menu"),n=document.body;t&&e&&(t.addEventListener("click",function(o){o.stopPropagation(),"flex"===e.style.display?(e.style.display="none",t.classList.remove("menu-open"),n.classList.remove("menu-open")):(e.style.display="flex",t.classList.add("menu-open"),n.classList.add("menu-open"));}),e.querySelectorAll("a").forEach(o=>{o.addEventListener("click",function(){e.style.display="none",t.classList.remove("menu-open"),n.classList.remove("menu-open");});}),document.addEventListener("click",function(o){t.contains(o.target)||e.contains(o.target)||(e.style.display="none",t.classList.remove("menu-open"),n.classList.remove("menu-open"));}),document.addEventListener("keydown",function(o){"Escape"===o.key&&"flex"===e.style.display&&(e.style.display="none",t.classList.remove("menu-open"),n.classList.remove("menu-open"));}));}),function(){if(document.getElementById("markdown-layout")){var t=document.createElement("style");t.textContent=`
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
    `,document.head.appendChild(t);}}(),function(){if(document.getElementById("markdown-layout")){var t=document.createElement("style");t.textContent=`
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
    `,document.head.appendChild(t);}}(),window.Prism=window.Prism||{},Prism.plugins=Prism.plugins||{},Prism.plugins.autoloader=Prism.plugins.autoloader||{},Prism.plugins.autoloader.languages_path="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/",function(){window.DarsMarkdown={_retries:0,addCopyButtons:function(t){(t||document).querySelectorAll("pre code").forEach(function(t){var e=t.parentElement;if(!(!e||e.querySelector(".dars-code-copy"))){"static"===getComputedStyle(e).position&&(e.style.position="relative");var n=document.createElement("button");n.className="dars-code-copy",n.type="button",n.textContent="Copy",n.addEventListener("click",async function(e){e.stopPropagation();try{await navigator.clipboard.writeText(t.innerText),n.textContent="Copied",n.classList.add("copied"),setTimeout(function(){n.textContent="Copy",n.classList.remove("copied");},1200);}catch(t){n.textContent="Error",setTimeout(function(){n.textContent="Copy";},1200);}}),e.appendChild(n);}});},guessLang:function(t){var e=t.trim();return/^{[\s\S]*}$/.test(e)||/^\[/.test(e)?"json":/^(pip |python |python3 |dars |#|\$ )/m.test(e)?"bash":/\b(def |class |import |from |print\(|self\b)/.test(e)?"python":null;},stripPygments:function(t){t&&t.innerHTML&&-1!==t.innerHTML.indexOf("<span")&&(t.textContent=t.innerText);},highlight:function(t){var e=this;if(!window.Prism||!Prism.highlightElement){e._retries<20&&(e._retries++,setTimeout(function(){e.highlight(t);},150));return;}(t||document).querySelectorAll("pre code").forEach(function(t){if(e.stripPygments(t),!t.className||-1===t.className.indexOf("language-")){var n=e.guessLang(t.innerText);t.classList.add("language-"+(n||"none"));}Prism.highlightElement(t);}),e.addCopyButtons(t);}},"complete"===document.readyState?window.DarsMarkdown.highlight():window.addEventListener("load",function(){window.DarsMarkdown.highlight();}),document.addEventListener("DOMContentLoaded",function(){window.DarsMarkdown.highlight();}),document.addEventListener("dars:content-loaded",function(t){t.detail&&t.detail.element&&window.DarsMarkdown.highlight(t.detail.element);});}();