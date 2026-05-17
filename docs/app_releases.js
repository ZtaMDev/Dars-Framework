(()=>{var c=Object.create;var d=Object.defineProperty;var l=Object.getOwnPropertyDescriptor;var u=Object.getOwnPropertyNames;var m=Object.getPrototypeOf,p=Object.prototype.hasOwnProperty;var f=(t,n,i,e)=>{if(n&&typeof n=="object"||typeof n=="function")for(let o of u(n))!p.call(t,o)&&o!==i&&d(t,o,{get:()=>n[o],enumerable:!(e=l(n,o))||e.enumerable});return t};var s=(t,n,i)=>(i=t!=null?c(m(t)):{},f(n||!t||!t.__esModule?d(i,"default",{value:t,enumerable:!0}):i,t));(function(){function t(){var e=document.getElementById("image_0_0_0_0_0");e&&e.addEventListener("click",async function(r){if(!window.Dars)try{const a=await import("./lib/dars.min.js");window.Dars=a.default||a}catch{}try{window.location.href="https://ztamdev.github.io/Dars-Framework/"}catch(a){console.error("Error en handler:",a)}});var o=document.getElementById("text_0_0_0_0_1");o&&o.addEventListener("click",async function(r){if(!window.Dars)try{const a=await import("./lib/dars.min.js");window.Dars=a.default||a}catch{}try{window.location.href="https://ztamdev.github.io/Dars-Framework/"}catch(a){console.error("Error en handler:",a)}})}function n(){try{const e=[{name:"counter",id:"counter",defaultValue:{count:0},isV2:!0}];window.Dars&&typeof window.Dars.registerStates=="function"?window.Dars.registerStates(e):window.__DARS_STATES_FN?window.__DARS_STATES_FN(e):(async()=>{try{const o=await import("./lib/dars.min.js"),r=o.registerStates||o.default&&o.default.registerStates;typeof r=="function"&&(r(e),window.__DARS_STATES_FN=r)}catch(o){console.error("[Dars] Failed to initialize states",o)}})()}catch(e){console.error("[Dars] State initialization error",e)}}function i(){(async()=>{try{const e=await import("./lib/dap.js");e.__darsConfig&&(e.__darsConfig.allowInlineJS=!0)}catch{}})(),n(),t();try{window.Dars&&typeof window.Dars.addReactiveBinding=="function"?window.Dars.addReactiveBinding(function(e){if(e&&e.dynamic&&e.id&&e.id==="counter"){let o;if(e.attrs&&e.attrs.count!==void 0?o=e.attrs.count:e.count!==void 0&&(o=e.count),o!==void 0){const r=document.getElementById("demo-counter-value");r&&(r.hasAttribute("data-server-component")&&r.firstElementChild?r.firstElementChild.textContent=String(o):r.textContent=String(o),r.hasAttribute("data-server-component")&&r.firstElementChild?r.firstElementChild.textContent=String(o):r.textContent=String(o))}}}):console.warn("[Dars:Debug] window.Dars.addReactiveBinding NOT found. Skipping reactive bindings.")}catch(e){console.error("[Dars] Failed to initialize reactive bindings",e)}}document.readyState==="complete"||document.readyState==="interactive"?i():document.addEventListener("DOMContentLoaded",i)})();window.addEventListener("scroll",()=>{const t=document.getElementById("dars-navbar");t&&(window.scrollY>20?t.classList.add("scrolled"):t.classList.remove("scrolled"))});document.addEventListener("DOMContentLoaded",function(){const t=document.getElementById("hamburger-btn"),n=document.getElementById("mobile-menu"),i=document.body;t&&n&&(t.addEventListener("click",function(e){e.stopPropagation(),n.style.display==="flex"?(n.style.display="none",t.classList.remove("menu-open"),i.classList.remove("menu-open")):(n.style.display="flex",t.classList.add("menu-open"),i.classList.add("menu-open"))}),n.querySelectorAll("a").forEach(e=>{e.addEventListener("click",function(){n.style.display="none",t.classList.remove("menu-open"),i.classList.remove("menu-open")})}),document.addEventListener("click",function(e){!t.contains(e.target)&&!n.contains(e.target)&&(n.style.display="none",t.classList.remove("menu-open"),i.classList.remove("menu-open"))}),document.addEventListener("keydown",function(e){e.key==="Escape"&&n.style.display==="flex"&&(n.style.display="none",t.classList.remove("menu-open"),i.classList.remove("menu-open"))}))});(function(){var t=document.getElementById("markdown-content-container");if(t){var n=document.createElement("style");n.textContent=`
        /* Version badges for h1 headings */
        #markdown-content-container h1 {
            position: relative;
            padding-bottom: 12px;
            margin-top: 48px;
        }
        #markdown-content-container h1::after {
            content: "";
            position: absolute;
            bottom: 0; left: 0;
            width: 60px; height: 3px;
            background: linear-gradient(90deg, #10b981, #059669);
            border-radius: 3px;
        }

        /* Blockquote as version summary */
        #markdown-content-container blockquote {
            border-left: 3px solid #059669;
            background: rgba(16, 185, 129, 0.06);
            padding: 12px 20px;
            border-radius: 0 8px 8px 0;
            margin: 12px 0 20px 0;
            font-style: italic;
        }
        #markdown-content-container blockquote p {
            margin: 0;
            color: #a0cfc0;
        }

        /* Code blocks */
        #markdown-content-container pre {
            border: 1px solid rgba(146, 255, 229, 0.08);
            border-radius: 8px;
        }

        /* Inline code */
        #markdown-content-container code:not(pre code) {
            background: rgba(146, 255, 229, 0.08);
            border: 1px solid rgba(146, 255, 229, 0.1);
            border-radius: 4px;
            padding: 2px 6px;
            font-size: 0.9em;
        }

        /* HR dividers between versions */
        #markdown-content-container hr {
            border: none;
            height: 1px;
            background: linear-gradient(90deg, transparent, rgba(146,255,229,0.15), transparent);
            margin: 40px 0;
        }

        /* H2 section headers */
        #markdown-content-container h2 {
            font-size: 20px;
            color: #92ffe5;
            margin-top: 28px;
        }

        /* H3 feature headers */
        #markdown-content-container h3 {
            position: relative;
            padding-left: 16px;
            margin-top: 24px;
        }
        #markdown-content-container h3::before {
            content: "";
            position: absolute;
            left: 0; top: 4px; bottom: 4px;
            width: 3px;
            background: linear-gradient(180deg, #10b981, #059669);
            border-radius: 3px;
        }
    `,document.head.appendChild(n)}})();window.Prism=window.Prism||{};Prism.plugins=Prism.plugins||{};Prism.plugins.autoloader=Prism.plugins.autoloader||{};Prism.plugins.autoloader.languages_path="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/";(function(){window.DarsMarkdown={_retries:0,addCopyButtons:function(t){(t||document).querySelectorAll("pre code").forEach(function(n){var i=n.parentElement;if(!(!i||i.querySelector(".dars-code-copy"))){getComputedStyle(i).position==="static"&&(i.style.position="relative");var e=document.createElement("button");e.className="dars-code-copy",e.type="button",e.textContent="Copy",e.addEventListener("click",async function(o){o.stopPropagation();try{await navigator.clipboard.writeText(n.innerText),e.textContent="Copied",e.classList.add("copied"),setTimeout(function(){e.textContent="Copy",e.classList.remove("copied")},1200)}catch{e.textContent="Error",setTimeout(function(){e.textContent="Copy"},1200)}}),i.appendChild(e)}})},guessLang:function(t){var n=t.trim();return/^{[\s\S]*}$/.test(n)||/^\[/.test(n)?"json":/^(pip |python |python3 |dars |#|\$ )/m.test(n)?"bash":/\b(def |class |import |from |print\(|self\b)/.test(n)?"python":null},stripPygments:function(t){t&&t.innerHTML&&t.innerHTML.indexOf("<span")!==-1&&(t.textContent=t.innerText)},highlight:function(t){var n=this;if(!window.Prism||!Prism.highlightElement){n._retries<20&&(n._retries++,setTimeout(function(){n.highlight(t)},150));return}(t||document).querySelectorAll("pre code").forEach(function(i){if(n.stripPygments(i),!i.className||i.className.indexOf("language-")===-1){var e=n.guessLang(i.innerText);i.classList.add("language-"+(e||"none"))}Prism.highlightElement(i)}),n.addCopyButtons(t)}},document.readyState==="complete"?window.DarsMarkdown.highlight():window.addEventListener("load",function(){window.DarsMarkdown.highlight()}),document.addEventListener("DOMContentLoaded",function(){window.DarsMarkdown.highlight()}),document.addEventListener("dars:content-loaded",function(t){t.detail&&t.detail.element&&window.DarsMarkdown.highlight(t.detail.element)})})();})();
