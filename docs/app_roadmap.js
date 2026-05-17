(()=>{var b=Object.create;var f=Object.defineProperty;var h=Object.getOwnPropertyDescriptor;var x=Object.getOwnPropertyNames;var w=Object.getPrototypeOf,v=Object.prototype.hasOwnProperty;var y=(t,n,r,e)=>{if(n&&typeof n=="object"||typeof n=="function")for(let o of x(n))!v.call(t,o)&&o!==r&&f(t,o,{get:()=>n[o],enumerable:!(e=h(n,o))||e.enumerable});return t};var m=(t,n,r)=>(r=t!=null?b(w(t)):{},y(n||!t||!t.__esModule?f(r,"default",{value:t,enumerable:!0}):r,t));(function(){function t(){var e=document.getElementById("image_0_0_0_0_0");e&&e.addEventListener("click",async function(i){if(!window.Dars)try{const a=await import("./lib/dars.min.js");window.Dars=a.default||a}catch{}try{window.location.href="https://ztamdev.github.io/Dars-Framework/"}catch(a){console.error("Error en handler:",a)}});var o=document.getElementById("text_0_0_0_0_1");o&&o.addEventListener("click",async function(i){if(!window.Dars)try{const a=await import("./lib/dars.min.js");window.Dars=a.default||a}catch{}try{window.location.href="https://ztamdev.github.io/Dars-Framework/"}catch(a){console.error("Error en handler:",a)}})}function n(){try{const e=[{name:"counter",id:"counter",defaultValue:{count:0},isV2:!0}];window.Dars&&typeof window.Dars.registerStates=="function"?window.Dars.registerStates(e):window.__DARS_STATES_FN?window.__DARS_STATES_FN(e):(async()=>{try{const o=await import("./lib/dars.min.js"),i=o.registerStates||o.default&&o.default.registerStates;typeof i=="function"&&(i(e),window.__DARS_STATES_FN=i)}catch(o){console.error("[Dars] Failed to initialize states",o)}})()}catch(e){console.error("[Dars] State initialization error",e)}}function r(){(async()=>{try{const e=await import("./lib/dap.js");e.__darsConfig&&(e.__darsConfig.allowInlineJS=!0)}catch{}})(),window.__DARS_SPA_CONFIG__?window.__DARS_SPA_CONFIG__.backendUrl||(window.__DARS_SPA_CONFIG__.backendUrl="/"):window.__DARS_SPA_CONFIG__={backendUrl:"/"},n(),t();try{window.Dars&&typeof window.Dars.addReactiveBinding=="function"?window.Dars.addReactiveBinding(function(e){if(e&&e.dynamic&&e.id&&e.id==="counter"){let o;if(e.attrs&&e.attrs.count!==void 0?o=e.attrs.count:e.count!==void 0&&(o=e.count),o!==void 0){const i=document.getElementById("demo-counter-value");i&&(i.hasAttribute("data-server-component")&&i.firstElementChild?i.firstElementChild.textContent=String(o):i.textContent=String(o),i.hasAttribute("data-server-component")&&i.firstElementChild?i.firstElementChild.textContent=String(o):i.textContent=String(o))}}}):console.warn("[Dars:Debug] window.Dars.addReactiveBinding NOT found. Skipping reactive bindings.")}catch(e){console.error("[Dars] Failed to initialize reactive bindings",e)}(async()=>{try{const e=await import("./lib/dap.js");e._initConditionalElements&&await e._initConditionalElements({})}catch{}})()}document.readyState==="complete"||document.readyState==="interactive"?r():document.addEventListener("DOMContentLoaded",r)})();window.addEventListener("scroll",()=>{const t=document.getElementById("dars-navbar");t&&(window.scrollY>20?t.classList.add("scrolled"):t.classList.remove("scrolled"))});document.addEventListener("DOMContentLoaded",function(){const t=document.getElementById("hamburger-btn"),n=document.getElementById("mobile-menu"),r=document.body;t&&n&&(t.addEventListener("click",function(e){e.stopPropagation(),n.style.display==="flex"?(n.style.display="none",t.classList.remove("menu-open"),r.classList.remove("menu-open")):(n.style.display="flex",t.classList.add("menu-open"),r.classList.add("menu-open"))}),n.querySelectorAll("a").forEach(e=>{e.addEventListener("click",function(){n.style.display="none",t.classList.remove("menu-open"),r.classList.remove("menu-open")})}),document.addEventListener("click",function(e){!t.contains(e.target)&&!n.contains(e.target)&&(n.style.display="none",t.classList.remove("menu-open"),r.classList.remove("menu-open"))}),document.addEventListener("keydown",function(e){e.key==="Escape"&&n.style.display==="flex"&&(n.style.display="none",t.classList.remove("menu-open"),r.classList.remove("menu-open"))}))});(function(){var t=document.getElementById("markdown-content-container");if(t){var n=document.createElement("style");n.textContent=`
        /* Checkboxes */
        .dars-checkbox {
            display: inline-flex; align-items: center; justify-content: center;
            width: 20px; height: 20px; border-radius: 5px; margin-right: 10px;
            flex-shrink: 0; vertical-align: middle; position: relative; top: 0px;
            transition: all 0.3s ease;
        }
        .dars-checkbox.checked {
            background: linear-gradient(135deg, #10b981, #059669);
            box-shadow: 0 0 10px rgba(16,185,129,0.3);
        }
        .dars-checkbox.checked::after {
            content: ""; display: block; width: 6px; height: 10px;
            border: solid #fff; border-width: 0 2.5px 2.5px 0;
            transform: rotate(45deg); margin-top: -2px;
        }
        .dars-checkbox.unchecked {
            background: rgba(255,255,255,0.04);
            border: 2px solid rgba(255,255,255,0.12);
        }
        .dars-cb-li {
            display: flex !important; align-items: flex-start;
            list-style: none !important; padding: 4px 0;
        }
        .dars-cb-li::before { display: none !important; }

        /* Section cards */
        #markdown-content-container h3 {
            background: rgba(255,255,255,0.03);
            border: 1px solid rgba(146, 255, 229, 0.08);
            border-radius: 10px;
            padding: 14px 20px;
            margin-top: 32px;
            margin-bottom: 16px;
            font-size: 18px;
            position: relative;
            overflow: hidden;
        }
        #markdown-content-container h3::before {
            content: "";
            position: absolute; left: 0; top: 0; bottom: 0;
            width: 3px;
            background: linear-gradient(180deg, #10b981, #059669);
            border-radius: 3px 0 0 3px;
        }

        /* Tables */
        #markdown-content-container table {
            border-collapse: separate;
            border-spacing: 0;
            border-radius: 10px;
            overflow: hidden;
            border: 1px solid rgba(146, 255, 229, 0.1);
            width: 100%;
        }
        #markdown-content-container th {
            background: rgba(16, 185, 129, 0.12) !important;
            border-bottom: 1px solid rgba(146, 255, 229, 0.15) !important;
            padding: 12px 16px !important;
            font-weight: 600;
            text-align: left;
        }
        #markdown-content-container td {
            padding: 10px 16px !important;
            border-bottom: 1px solid rgba(255,255,255,0.04) !important;
        }
        #markdown-content-container tr:last-child td {
            border-bottom: none !important;
        }

        /* HR dividers */
        #markdown-content-container hr {
            border: none;
            height: 1px;
            background: linear-gradient(90deg, transparent, rgba(146,255,229,0.15), transparent);
            margin: 36px 0;
        }

        /* Completed section */
        #markdown-content-container h2 {
            font-size: 22px;
            padding-bottom: 10px;
            border-bottom: 1px solid rgba(146, 255, 229, 0.1);
            margin-top: 40px;
        }
    `,document.head.appendChild(n);for(var r=0,e=0,o=t.querySelectorAll("li"),i=0;i<o.length;i++){var a=o[i],d=a.textContent;if(/^\s*\[[ x]\]/.test(d)){r++;var s=/^\s*\[x\]/i.test(d);s&&e++;var u=s?"checked":"unchecked",g='<span class="dars-checkbox '+u+'"></span>';a.innerHTML=a.innerHTML.replace(/\[[ x]\]\s*/,""),a.insertAdjacentHTML("afterbegin",g),a.classList.add("dars-cb-li")}}if(r>0){var c=Math.round(e/r*100),l=document.getElementById("roadmap-progress-fill"),p=document.getElementById("roadmap-progress-text");l&&setTimeout(function(){l.style.width=c+"%"},300),p&&(p.textContent=e+" / "+r+" tasks ("+c+"%)")}}})();(function(){var t=document.getElementById("markdown-content-container");if(t){var n=document.createElement("style");n.textContent=`
        /* Checkboxes */
        .dars-checkbox {
            display: inline-flex; align-items: center; justify-content: center;
            width: 20px; height: 20px; border-radius: 5px; margin-right: 10px;
            flex-shrink: 0; vertical-align: middle; position: relative; top: 0px;
            transition: all 0.3s ease;
        }
        .dars-checkbox.checked {
            background: linear-gradient(135deg, #10b981, #059669);
            box-shadow: 0 0 10px rgba(16,185,129,0.3);
        }
        .dars-checkbox.checked::after {
            content: ""; display: block; width: 6px; height: 10px;
            border: solid #fff; border-width: 0 2.5px 2.5px 0;
            transform: rotate(45deg); margin-top: -2px;
        }
        .dars-checkbox.unchecked {
            background: rgba(255,255,255,0.04);
            border: 2px solid rgba(255,255,255,0.12);
        }
        .dars-cb-li {
            display: flex !important; align-items: flex-start;
            list-style: none !important; padding: 4px 0;
        }
        .dars-cb-li::before { display: none !important; }

        /* Section cards */
        #markdown-content-container h3 {
            background: rgba(255,255,255,0.03);
            border: 1px solid rgba(146, 255, 229, 0.08);
            border-radius: 10px;
            padding: 14px 20px;
            margin-top: 32px;
            margin-bottom: 16px;
            font-size: 18px;
            position: relative;
            overflow: hidden;
        }
        #markdown-content-container h3::before {
            content: "";
            position: absolute; left: 0; top: 0; bottom: 0;
            width: 3px;
            background: linear-gradient(180deg, #10b981, #059669);
            border-radius: 3px 0 0 3px;
        }

        /* Tables */
        #markdown-content-container table {
            border-collapse: separate;
            border-spacing: 0;
            border-radius: 10px;
            overflow: hidden;
            border: 1px solid rgba(146, 255, 229, 0.1);
            width: 100%;
        }
        #markdown-content-container th {
            background: rgba(16, 185, 129, 0.12) !important;
            border-bottom: 1px solid rgba(146, 255, 229, 0.15) !important;
            padding: 12px 16px !important;
            font-weight: 600;
            text-align: left;
        }
        #markdown-content-container td {
            padding: 10px 16px !important;
            border-bottom: 1px solid rgba(255,255,255,0.04) !important;
        }
        #markdown-content-container tr:last-child td {
            border-bottom: none !important;
        }

        /* HR dividers */
        #markdown-content-container hr {
            border: none;
            height: 1px;
            background: linear-gradient(90deg, transparent, rgba(146,255,229,0.15), transparent);
            margin: 36px 0;
        }

        /* Completed section */
        #markdown-content-container h2 {
            font-size: 22px;
            padding-bottom: 10px;
            border-bottom: 1px solid rgba(146, 255, 229, 0.1);
            margin-top: 40px;
        }
    `,document.head.appendChild(n);for(var r=0,e=0,o=t.querySelectorAll("li"),i=0;i<o.length;i++){var a=o[i],d=a.textContent;if(/^\s*\[[ x]\]/.test(d)){r++;var s=/^\s*\[x\]/i.test(d);s&&e++;var u=s?"checked":"unchecked",g='<span class="dars-checkbox '+u+'"></span>';a.innerHTML=a.innerHTML.replace(/\[[ x]\]\s*/,""),a.insertAdjacentHTML("afterbegin",g),a.classList.add("dars-cb-li")}}if(r>0){var c=Math.round(e/r*100),l=document.getElementById("roadmap-progress-fill"),p=document.getElementById("roadmap-progress-text");l&&setTimeout(function(){l.style.width=c+"%"},300),p&&(p.textContent=e+" / "+r+" tasks ("+c+"%)")}}})();window.Prism=window.Prism||{};Prism.plugins=Prism.plugins||{};Prism.plugins.autoloader=Prism.plugins.autoloader||{};Prism.plugins.autoloader.languages_path="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/";(function(){window.DarsMarkdown={_retries:0,addCopyButtons:function(t){(t||document).querySelectorAll("pre code").forEach(function(n){var r=n.parentElement;if(!(!r||r.querySelector(".dars-code-copy"))){getComputedStyle(r).position==="static"&&(r.style.position="relative");var e=document.createElement("button");e.className="dars-code-copy",e.type="button",e.textContent="Copy",e.addEventListener("click",async function(o){o.stopPropagation();try{await navigator.clipboard.writeText(n.innerText),e.textContent="Copied",e.classList.add("copied"),setTimeout(function(){e.textContent="Copy",e.classList.remove("copied")},1200)}catch{e.textContent="Error",setTimeout(function(){e.textContent="Copy"},1200)}}),r.appendChild(e)}})},guessLang:function(t){var n=t.trim();return/^{[\s\S]*}$/.test(n)||/^\[/.test(n)?"json":/^(pip |python |python3 |dars |#|\$ )/m.test(n)?"bash":/\b(def |class |import |from |print\(|self\b)/.test(n)?"python":null},stripPygments:function(t){t&&t.innerHTML&&t.innerHTML.indexOf("<span")!==-1&&(t.textContent=t.innerText)},highlight:function(t){var n=this;if(!window.Prism||!Prism.highlightElement){n._retries<20&&(n._retries++,setTimeout(function(){n.highlight(t)},150));return}(t||document).querySelectorAll("pre code").forEach(function(r){if(n.stripPygments(r),!r.className||r.className.indexOf("language-")===-1){var e=n.guessLang(r.innerText);r.classList.add("language-"+(e||"none"))}Prism.highlightElement(r)}),n.addCopyButtons(t)}},document.readyState==="complete"?window.DarsMarkdown.highlight():window.addEventListener("load",function(){window.DarsMarkdown.highlight()}),document.addEventListener("DOMContentLoaded",function(){window.DarsMarkdown.highlight()}),document.addEventListener("dars:content-loaded",function(t){t.detail&&t.detail.element&&window.DarsMarkdown.highlight(t.detail.element)})})();})();
