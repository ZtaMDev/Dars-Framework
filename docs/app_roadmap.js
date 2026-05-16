(()=>{var h=Object.create;var p=Object.defineProperty;var w=Object.getOwnPropertyDescriptor;var b=Object.getOwnPropertyNames;var x=Object.getPrototypeOf,v=Object.prototype.hasOwnProperty;var y=(t,n,i,e)=>{if(n&&typeof n=="object"||typeof n=="function")for(let r of b(n))!v.call(t,r)&&r!==i&&p(t,r,{get:()=>n[r],enumerable:!(e=w(n,r))||e.enumerable});return t};var s=(t,n,i)=>(i=t!=null?h(x(t)):{},y(n||!t||!t.__esModule?p(i,"default",{value:t,enumerable:!0}):i,t));(function(){function t(){var e=document.getElementById("image_0_0_0_0_0");e&&e.addEventListener("click",async function(o){if(!window.Dars)try{const a=await import("/lib/dars.min.js");window.Dars=a.default||a}catch{}try{window.location.href="https://ztamdev.github.io/Dars-Framework/"}catch(a){console.error("Error en handler:",a)}});var r=document.getElementById("text_0_0_0_0_1");r&&r.addEventListener("click",async function(o){if(!window.Dars)try{const a=await import("/lib/dars.min.js");window.Dars=a.default||a}catch{}try{window.location.href="https://ztamdev.github.io/Dars-Framework/"}catch(a){console.error("Error en handler:",a)}})}function n(){try{const e=[{name:"counter",id:"counter",defaultValue:{count:0},isV2:!0}];window.Dars&&typeof window.Dars.registerStates=="function"?window.Dars.registerStates(e):window.__DARS_STATES_FN?window.__DARS_STATES_FN(e):(async()=>{try{const r=await import("./lib/dars.min.js"),o=r.registerStates||r.default&&r.default.registerStates;typeof o=="function"&&(o(e),window.__DARS_STATES_FN=o)}catch(r){console.error("[Dars] Failed to initialize states",r)}})()}catch(e){console.error("[Dars] State initialization error",e)}}function i(){n(),t();try{window.Dars&&typeof window.Dars.addReactiveBinding=="function"?window.Dars.addReactiveBinding(function(e){if(e&&e.dynamic&&e.id&&e.id==="counter"){let r;if(e.attrs&&e.attrs.count!==void 0?r=e.attrs.count:e.count!==void 0&&(r=e.count),r!==void 0){const o=document.getElementById("demo-counter-value");o&&(o.hasAttribute("data-server-component")&&o.firstElementChild?o.firstElementChild.textContent=String(r):o.textContent=String(r),o.hasAttribute("data-server-component")&&o.firstElementChild?o.firstElementChild.textContent=String(r):o.textContent=String(r))}}}):console.warn("[Dars:Debug] window.Dars.addReactiveBinding NOT found. Skipping reactive bindings.")}catch(e){console.error("[Dars] Failed to initialize reactive bindings",e)}}document.readyState==="complete"||document.readyState==="interactive"?i():document.addEventListener("DOMContentLoaded",i)})();window.addEventListener("scroll",()=>{const t=document.getElementById("dars-navbar");t&&(window.scrollY>20?t.classList.add("scrolled"):t.classList.remove("scrolled"))});document.addEventListener("DOMContentLoaded",function(){const t=document.getElementById("hamburger-btn"),n=document.getElementById("mobile-menu"),i=document.body;t&&n&&(t.addEventListener("click",function(e){e.stopPropagation(),n.style.display==="flex"?(n.style.display="none",t.classList.remove("menu-open"),i.classList.remove("menu-open")):(n.style.display="flex",t.classList.add("menu-open"),i.classList.add("menu-open"))}),n.querySelectorAll("a").forEach(e=>{e.addEventListener("click",function(){n.style.display="none",t.classList.remove("menu-open"),i.classList.remove("menu-open")})}),document.addEventListener("click",function(e){!t.contains(e.target)&&!n.contains(e.target)&&(n.style.display="none",t.classList.remove("menu-open"),i.classList.remove("menu-open"))}),document.addEventListener("keydown",function(e){e.key==="Escape"&&n.style.display==="flex"&&(n.style.display="none",t.classList.remove("menu-open"),i.classList.remove("menu-open"))}))});(function(){var t=document.getElementById("markdown-content-container");if(t){var n=document.createElement("style");n.textContent=`
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
    `,document.head.appendChild(n);for(var i=0,e=0,r=t.querySelectorAll("li"),o=0;o<r.length;o++){var a=r[o],d=a.textContent;if(/^\s*\[[ x]\]/.test(d)){i++;var c=/^\s*\[x\]/i.test(d);c&&e++;var f=c?"checked":"unchecked",g='<span class="dars-checkbox '+f+'"></span>';a.innerHTML=a.innerHTML.replace(/\[[ x]\]\s*/,""),a.insertAdjacentHTML("afterbegin",g),a.classList.add("dars-cb-li")}}if(i>0){var l=Math.round(e/i*100),m=document.getElementById("roadmap-progress-fill"),u=document.getElementById("roadmap-progress-text");m&&setTimeout(function(){m.style.width=l+"%"},300),u&&(u.textContent=e+" / "+i+" tasks ("+l+"%)")}}})();window.Prism=window.Prism||{};Prism.plugins=Prism.plugins||{};Prism.plugins.autoloader=Prism.plugins.autoloader||{};Prism.plugins.autoloader.languages_path="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/";(function(){window.DarsMarkdown={_retries:0,addCopyButtons:function(t){(t||document).querySelectorAll("pre code").forEach(function(n){var i=n.parentElement;if(!(!i||i.querySelector(".dars-code-copy"))){getComputedStyle(i).position==="static"&&(i.style.position="relative");var e=document.createElement("button");e.className="dars-code-copy",e.type="button",e.textContent="Copy",e.addEventListener("click",async function(r){r.stopPropagation();try{await navigator.clipboard.writeText(n.innerText),e.textContent="Copied",e.classList.add("copied"),setTimeout(function(){e.textContent="Copy",e.classList.remove("copied")},1200)}catch{e.textContent="Error",setTimeout(function(){e.textContent="Copy"},1200)}}),i.appendChild(e)}})},guessLang:function(t){var n=t.trim();return/^{[\s\S]*}$/.test(n)||/^\[/.test(n)?"json":/^(pip |python |python3 |dars |#|\$ )/m.test(n)?"bash":/\b(def |class |import |from |print\(|self\b)/.test(n)?"python":null},stripPygments:function(t){t&&t.innerHTML&&t.innerHTML.indexOf("<span")!==-1&&(t.textContent=t.innerText)},highlight:function(t){var n=this;if(!window.Prism||!Prism.highlightElement){n._retries<20&&(n._retries++,setTimeout(function(){n.highlight(t)},150));return}(t||document).querySelectorAll("pre code").forEach(function(i){if(n.stripPygments(i),!i.className||i.className.indexOf("language-")===-1){var e=n.guessLang(i.innerText);i.classList.add("language-"+(e||"none"))}Prism.highlightElement(i)}),n.addCopyButtons(t)}},document.readyState==="complete"?window.DarsMarkdown.highlight():window.addEventListener("load",function(){window.DarsMarkdown.highlight()}),document.addEventListener("DOMContentLoaded",function(){window.DarsMarkdown.highlight()}),document.addEventListener("dars:content-loaded",function(t){t.detail&&t.detail.element&&window.DarsMarkdown.highlight(t.detail.element)})})();})();
