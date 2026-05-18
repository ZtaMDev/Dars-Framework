(()=>{var b=Object.create;var f=Object.defineProperty;var h=Object.getOwnPropertyDescriptor;var x=Object.getOwnPropertyNames;var w=Object.getPrototypeOf,v=Object.prototype.hasOwnProperty;var y=(e,n,o,t)=>{if(n&&typeof n=="object"||typeof n=="function")for(let i of x(n))!v.call(e,i)&&i!==o&&f(e,i,{get:()=>n[i],enumerable:!(t=h(n,i))||t.enumerable});return e};var m=(e,n,o)=>(o=e!=null?b(w(e)):{},y(n||!e||!e.__esModule?f(o,"default",{value:e,enumerable:!0}):o,e));(function(){function e(){var t=document.getElementById("image_0_0_0_0_0");t&&t.addEventListener("click",async function(r){if(!window.Dars)try{const a=await import("./lib/dars.min.js");window.Dars=a.default||a}catch{}try{window.location.href="https://ztamdev.github.io/Dars-Framework/"}catch(a){console.error("Error en handler:",a)}});var i=document.getElementById("text_0_0_0_0_1");i&&i.addEventListener("click",async function(r){if(!window.Dars)try{const a=await import("./lib/dars.min.js");window.Dars=a.default||a}catch{}try{window.location.href="https://ztamdev.github.io/Dars-Framework/"}catch(a){console.error("Error en handler:",a)}})}function n(){try{const t=[{name:"counter",id:"counter",defaultValue:{count:0},isV2:!0}];window.Dars&&typeof window.Dars.registerStates=="function"?window.Dars.registerStates(t):window.__DARS_STATES_FN?window.__DARS_STATES_FN(t):(async()=>{try{const i=await import("./lib/dars.min.js"),r=i.registerStates||i.default&&i.default.registerStates;typeof r=="function"&&(r(t),window.__DARS_STATES_FN=r)}catch(i){console.error("[Dars] Failed to initialize states",i)}})()}catch(t){console.error("[Dars] State initialization error",t)}}function o(){(async()=>{try{const t=await import("./lib/dap.js");t.__darsConfig&&(t.__darsConfig.allowInlineJS=!0)}catch{}})(),window.__DARS_SPA_CONFIG__?window.__DARS_SPA_CONFIG__.backendUrl||(window.__DARS_SPA_CONFIG__.backendUrl="/"):window.__DARS_SPA_CONFIG__={backendUrl:"/"},n(),e();try{window.Dars&&typeof window.Dars.addReactiveBinding=="function"?window.Dars.addReactiveBinding(function(t){if(t&&t.dynamic&&t.id&&t.id==="counter"){let i;if(t.attrs&&t.attrs.count!==void 0?i=t.attrs.count:t.count!==void 0&&(i=t.count),i!==void 0){const r=document.getElementById("demo-counter-value");r&&(r.hasAttribute("data-server-component")&&r.firstElementChild?r.firstElementChild.textContent=String(i):r.textContent=String(i),r.hasAttribute("data-server-component")&&r.firstElementChild?r.firstElementChild.textContent=String(i):r.textContent=String(i),r.hasAttribute("data-server-component")&&r.firstElementChild?r.firstElementChild.textContent=String(i):r.textContent=String(i),r.hasAttribute("data-server-component")&&r.firstElementChild?r.firstElementChild.textContent=String(i):r.textContent=String(i),r.hasAttribute("data-server-component")&&r.firstElementChild?r.firstElementChild.textContent=String(i):r.textContent=String(i),r.hasAttribute("data-server-component")&&r.firstElementChild?r.firstElementChild.textContent=String(i):r.textContent=String(i))}}}):console.warn("[Dars:Debug] window.Dars.addReactiveBinding NOT found. Skipping reactive bindings.")}catch(t){console.error("[Dars] Failed to initialize reactive bindings",t)}(async()=>{try{const t=await import("./lib/dap.js");t._initConditionalElements&&await t._initConditionalElements({})}catch{}})()}document.readyState==="complete"||document.readyState==="interactive"?o():document.addEventListener("DOMContentLoaded",o)})();window.addEventListener("scroll",()=>{const e=document.getElementById("dars-navbar");e&&(window.scrollY>20?e.classList.add("scrolled"):e.classList.remove("scrolled"))});document.addEventListener("DOMContentLoaded",function(){const e=document.getElementById("hamburger-btn"),n=document.getElementById("mobile-menu"),o=document.body;e&&n&&(e.addEventListener("click",function(t){t.stopPropagation(),n.style.display==="flex"?(n.style.display="none",e.classList.remove("menu-open"),o.classList.remove("menu-open")):(n.style.display="flex",e.classList.add("menu-open"),o.classList.add("menu-open"))}),n.querySelectorAll("a").forEach(t=>{t.addEventListener("click",function(){n.style.display="none",e.classList.remove("menu-open"),o.classList.remove("menu-open")})}),document.addEventListener("click",function(t){!e.contains(t.target)&&!n.contains(t.target)&&(n.style.display="none",e.classList.remove("menu-open"),o.classList.remove("menu-open"))}),document.addEventListener("keydown",function(t){t.key==="Escape"&&n.style.display==="flex"&&(n.style.display="none",e.classList.remove("menu-open"),o.classList.remove("menu-open"))}))});(function(){var e=document.getElementById("markdown-content-container");if(e){var n=document.createElement("style");n.textContent=`
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
    `,document.head.appendChild(n);for(var o=0,t=0,i=e.querySelectorAll("li"),r=0;r<i.length;r++){var a=i[r],d=a.textContent;if(/^\s*\[[ x]\]/.test(d)){o++;var s=/^\s*\[x\]/i.test(d);s&&t++;var g=s?"checked":"unchecked",u='<span class="dars-checkbox '+g+'"></span>';a.innerHTML=a.innerHTML.replace(/\[[ x]\]\s*/,""),a.insertAdjacentHTML("afterbegin",u),a.classList.add("dars-cb-li")}}if(o>0){var c=Math.round(t/o*100),l=document.getElementById("roadmap-progress-fill"),p=document.getElementById("roadmap-progress-text");l&&setTimeout(function(){l.style.width=c+"%"},300),p&&(p.textContent=t+" / "+o+" tasks ("+c+"%)")}}})();(function(){var e=document.getElementById("markdown-content-container");if(e){var n=document.createElement("style");n.textContent=`
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
    `,document.head.appendChild(n);for(var o=0,t=0,i=e.querySelectorAll("li"),r=0;r<i.length;r++){var a=i[r],d=a.textContent;if(/^\s*\[[ x]\]/.test(d)){o++;var s=/^\s*\[x\]/i.test(d);s&&t++;var g=s?"checked":"unchecked",u='<span class="dars-checkbox '+g+'"></span>';a.innerHTML=a.innerHTML.replace(/\[[ x]\]\s*/,""),a.insertAdjacentHTML("afterbegin",u),a.classList.add("dars-cb-li")}}if(o>0){var c=Math.round(t/o*100),l=document.getElementById("roadmap-progress-fill"),p=document.getElementById("roadmap-progress-text");l&&setTimeout(function(){l.style.width=c+"%"},300),p&&(p.textContent=t+" / "+o+" tasks ("+c+"%)")}}})();window.Prism=window.Prism||{};Prism.plugins=Prism.plugins||{};Prism.plugins.autoloader=Prism.plugins.autoloader||{};Prism.plugins.autoloader.languages_path="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/";(function(){window.DarsMarkdown={_retries:0,addCopyButtons:function(e){(e||document).querySelectorAll("pre code").forEach(function(n){var o=n.parentElement;if(!(!o||o.querySelector(".dars-code-copy"))){getComputedStyle(o).position==="static"&&(o.style.position="relative");var t=document.createElement("button");t.className="dars-code-copy",t.type="button",t.textContent="Copy",t.addEventListener("click",async function(i){i.stopPropagation();try{await navigator.clipboard.writeText(n.innerText),t.textContent="Copied",t.classList.add("copied"),setTimeout(function(){t.textContent="Copy",t.classList.remove("copied")},1200)}catch{t.textContent="Error",setTimeout(function(){t.textContent="Copy"},1200)}}),o.appendChild(t)}})},guessLang:function(e){var n=e.trim();return/^{[\s\S]*}$/.test(n)||/^\[/.test(n)?"json":/^(pip |python |python3 |dars |#|\$ )/m.test(n)?"bash":/\b(def |class |import |from |print\(|self\b)/.test(n)?"python":null},stripPygments:function(e){e&&e.innerHTML&&e.innerHTML.indexOf("<span")!==-1&&(e.textContent=e.innerText)},highlight:function(e){var n=this;if(!window.Prism||!Prism.highlightElement){n._retries<20&&(n._retries++,setTimeout(function(){n.highlight(e)},150));return}(e||document).querySelectorAll("pre code").forEach(function(o){if(n.stripPygments(o),!o.className||o.className.indexOf("language-")===-1){var t=n.guessLang(o.innerText);o.classList.add("language-"+(t||"none"))}Prism.highlightElement(o)}),n.addCopyButtons(e)}},document.readyState==="complete"?window.DarsMarkdown.highlight():window.addEventListener("load",function(){window.DarsMarkdown.highlight()}),document.addEventListener("DOMContentLoaded",function(){window.DarsMarkdown.highlight()}),document.addEventListener("dars:content-loaded",function(e){e.detail&&e.detail.element&&window.DarsMarkdown.highlight(e.detail.element)})})();})();
