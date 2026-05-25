(function(){function t(){var t,e;(async()=>{try{let t=await import("./lib/dap.js");t.__darsConfig&&(t.__darsConfig.allowInlineJS=!0);}catch(t){}})(),window.__DARS_SPA_CONFIG__?window.__DARS_SPA_CONFIG__.backendUrl||(window.__DARS_SPA_CONFIG__.backendUrl="/"):window.__DARS_SPA_CONFIG__={backendUrl:"/"},function(){try{let t=[{name:"counter",id:"counter",defaultValue:{count:0},isV2:!0}];window.Dars&&"function"==typeof window.Dars.registerStates?window.Dars.registerStates(t):window.__DARS_STATES_FN?window.__DARS_STATES_FN(t):(async()=>{try{let e=await import("./lib/dars.min.js"),n=e.registerStates||e.default&&e.default.registerStates;"function"==typeof n&&(n(t),window.__DARS_STATES_FN=n);}catch(t){console.error("[Dars] Failed to initialize states",t);}})();}catch(t){console.error("[Dars] State initialization error",t);}}(),(t=document.getElementById("image_0_0_0_0_0"))&&t.addEventListener("click",async function(t){if(!window.Dars)try{let t=await import("./lib/dars.min.js");window.Dars=t.default||t;}catch(t){}try{window.location.href="https://ztamdev.github.io/Dars-Framework/";}catch(t){console.error("Error en handler:",t);}}),(e=document.getElementById("text_0_0_0_0_1"))&&e.addEventListener("click",async function(t){if(!window.Dars)try{let t=await import("./lib/dars.min.js");window.Dars=t.default||t;}catch(t){}try{window.location.href="https://ztamdev.github.io/Dars-Framework/";}catch(t){console.error("Error en handler:",t);}}),(async()=>{try{let t=await import("./lib/dap.js");t._initConditionalElements&&await t._initConditionalElements({});}catch(t){}})();}"complete"===document.readyState||"interactive"===document.readyState?t():document.addEventListener("DOMContentLoaded",t);})(),window.addEventListener("scroll",()=>{let t=document.getElementById("dars-navbar");t&&(window.scrollY>20?t.classList.add("scrolled"):t.classList.remove("scrolled"));}),document.addEventListener("DOMContentLoaded",function(){let t=document.getElementById("hamburger-btn"),e=document.getElementById("mobile-menu"),n=document.body;t&&e&&(t.addEventListener("click",function(o){o.stopPropagation(),"flex"===e.style.display?(e.style.display="none",t.classList.remove("menu-open"),n.classList.remove("menu-open")):(e.style.display="flex",t.classList.add("menu-open"),n.classList.add("menu-open"));}),e.querySelectorAll("a").forEach(o=>{o.addEventListener("click",function(){e.style.display="none",t.classList.remove("menu-open"),n.classList.remove("menu-open");});}),document.addEventListener("click",function(o){t.contains(o.target)||e.contains(o.target)||(e.style.display="none",t.classList.remove("menu-open"),n.classList.remove("menu-open"));}),document.addEventListener("keydown",function(o){"Escape"===o.key&&"flex"===e.style.display&&(e.style.display="none",t.classList.remove("menu-open"),n.classList.remove("menu-open"));}));}),function(){var t=document.getElementById("markdown-content-container");if(t){var e=document.createElement("style");e.textContent=`
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
    `,document.head.appendChild(e);for(var n=0,o=0,r=t.querySelectorAll("li"),a=0;a<r.length;a++){var i=r[a],d=i.textContent;if(/^\s*\[[ x]\]/.test(d)){n++;var s=/^\s*\[x\]/i.test(d);s&&o++;var c='<span class="dars-checkbox '+(s?"checked":"unchecked")+'"></span>';i.innerHTML=i.innerHTML.replace(/\[[ x]\]\s*/,""),i.insertAdjacentHTML("afterbegin",c),i.classList.add("dars-cb-li");}}if(n>0){var l=Math.round(o/n*100),p=document.getElementById("roadmap-progress-fill"),m=document.getElementById("roadmap-progress-text");p&&setTimeout(function(){p.style.width=l+"%";},300),m&&(m.textContent=o+" / "+n+" tasks ("+l+"%)");}}}(),function(){var t=document.getElementById("markdown-content-container");if(t){var e=document.createElement("style");e.textContent=`
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
    `,document.head.appendChild(e);for(var n=0,o=0,r=t.querySelectorAll("li"),a=0;a<r.length;a++){var i=r[a],d=i.textContent;if(/^\s*\[[ x]\]/.test(d)){n++;var s=/^\s*\[x\]/i.test(d);s&&o++;var c='<span class="dars-checkbox '+(s?"checked":"unchecked")+'"></span>';i.innerHTML=i.innerHTML.replace(/\[[ x]\]\s*/,""),i.insertAdjacentHTML("afterbegin",c),i.classList.add("dars-cb-li");}}if(n>0){var l=Math.round(o/n*100),p=document.getElementById("roadmap-progress-fill"),m=document.getElementById("roadmap-progress-text");p&&setTimeout(function(){p.style.width=l+"%";},300),m&&(m.textContent=o+" / "+n+" tasks ("+l+"%)");}}}(),window.Prism=window.Prism||{},Prism.plugins=Prism.plugins||{},Prism.plugins.autoloader=Prism.plugins.autoloader||{},Prism.plugins.autoloader.languages_path="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/",function(){window.DarsMarkdown={_retries:0,addCopyButtons:function(t){(t||document).querySelectorAll("pre code").forEach(function(t){var e=t.parentElement;if(!(!e||e.querySelector(".dars-code-copy"))){"static"===getComputedStyle(e).position&&(e.style.position="relative");var n=document.createElement("button");n.className="dars-code-copy",n.type="button",n.textContent="Copy",n.addEventListener("click",async function(e){e.stopPropagation();try{await navigator.clipboard.writeText(t.innerText),n.textContent="Copied",n.classList.add("copied"),setTimeout(function(){n.textContent="Copy",n.classList.remove("copied");},1200);}catch(t){n.textContent="Error",setTimeout(function(){n.textContent="Copy";},1200);}}),e.appendChild(n);}});},guessLang:function(t){var e=t.trim();return/^{[\s\S]*}$/.test(e)||/^\[/.test(e)?"json":/^(pip |python |python3 |dars |#|\$ )/m.test(e)?"bash":/\b(def |class |import |from |print\(|self\b)/.test(e)?"python":null;},stripPygments:function(t){t&&t.innerHTML&&-1!==t.innerHTML.indexOf("<span")&&(t.textContent=t.innerText);},highlight:function(t){var e=this;if(!window.Prism||!Prism.highlightElement){e._retries<20&&(e._retries++,setTimeout(function(){e.highlight(t);},150));return;}(t||document).querySelectorAll("pre code").forEach(function(t){if(e.stripPygments(t),!t.className||-1===t.className.indexOf("language-")){var n=e.guessLang(t.innerText);t.classList.add("language-"+(n||"none"));}Prism.highlightElement(t);}),e.addCopyButtons(t);}},"complete"===document.readyState?window.DarsMarkdown.highlight():window.addEventListener("load",function(){window.DarsMarkdown.highlight();}),document.addEventListener("DOMContentLoaded",function(){window.DarsMarkdown.highlight();}),document.addEventListener("dars:content-loaded",function(t){t.detail&&t.detail.element&&window.DarsMarkdown.highlight(t.detail.element);});}();