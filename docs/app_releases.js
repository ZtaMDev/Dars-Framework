(function(){function e(){var e,t;(async()=>{try{let e=await import("./lib/dap.js");e.__darsConfig&&(e.__darsConfig.allowInlineJS=!0);}catch(e){}})(),window.__DARS_SPA_CONFIG__?window.__DARS_SPA_CONFIG__.backendUrl||(window.__DARS_SPA_CONFIG__.backendUrl="/"):window.__DARS_SPA_CONFIG__={backendUrl:"/"},function(){try{let e=[{name:"counter",id:"counter",defaultValue:{count:0},isV2:!0}];window.Dars&&"function"==typeof window.Dars.registerStates?window.Dars.registerStates(e):window.__DARS_STATES_FN?window.__DARS_STATES_FN(e):(async()=>{try{let t=await import("./lib/dars.min.js"),n=t.registerStates||t.default&&t.default.registerStates;"function"==typeof n&&(n(e),window.__DARS_STATES_FN=n);}catch(e){console.error("[Dars] Failed to initialize states",e);}})();}catch(e){console.error("[Dars] State initialization error",e);}}(),(e=document.getElementById("image_0_0_0_0_0"))&&e.addEventListener("click",async function(e){if(!window.Dars)try{let e=await import("./lib/dars.min.js");window.Dars=e.default||e;}catch(e){}try{window.location.href="https://ztamdev.github.io/Dars-Framework/";}catch(e){console.error("Error en handler:",e);}}),(t=document.getElementById("text_0_0_0_0_1"))&&t.addEventListener("click",async function(e){if(!window.Dars)try{let e=await import("./lib/dars.min.js");window.Dars=e.default||e;}catch(e){}try{window.location.href="https://ztamdev.github.io/Dars-Framework/";}catch(e){console.error("Error en handler:",e);}}),(async()=>{try{let e=await import("./lib/dap.js");e._initConditionalElements&&await e._initConditionalElements({});}catch(e){}})();}"complete"===document.readyState||"interactive"===document.readyState?e():document.addEventListener("DOMContentLoaded",e);})(),window.addEventListener("scroll",()=>{let e=document.getElementById("dars-navbar");e&&(window.scrollY>20?e.classList.add("scrolled"):e.classList.remove("scrolled"));}),document.addEventListener("DOMContentLoaded",function(){let e=document.getElementById("hamburger-btn"),t=document.getElementById("mobile-menu"),n=document.body;e&&t&&(e.addEventListener("click",function(o){o.stopPropagation(),"flex"===t.style.display?(t.style.display="none",e.classList.remove("menu-open"),n.classList.remove("menu-open")):(t.style.display="flex",e.classList.add("menu-open"),n.classList.add("menu-open"));}),t.querySelectorAll("a").forEach(o=>{o.addEventListener("click",function(){t.style.display="none",e.classList.remove("menu-open"),n.classList.remove("menu-open");});}),document.addEventListener("click",function(o){e.contains(o.target)||t.contains(o.target)||(t.style.display="none",e.classList.remove("menu-open"),n.classList.remove("menu-open"));}),document.addEventListener("keydown",function(o){"Escape"===o.key&&"flex"===t.style.display&&(t.style.display="none",e.classList.remove("menu-open"),n.classList.remove("menu-open"));}));}),function(){if(document.getElementById("markdown-content-container")){var e=document.createElement("style");e.textContent=`
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
    `,document.head.appendChild(e);}}(),function(){if(document.getElementById("markdown-content-container")){var e=document.createElement("style");e.textContent=`
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
    `,document.head.appendChild(e);}}(),window.Prism=window.Prism||{},Prism.plugins=Prism.plugins||{},Prism.plugins.autoloader=Prism.plugins.autoloader||{},Prism.plugins.autoloader.languages_path="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/",function(){window.DarsMarkdown={_retries:0,addCopyButtons:function(e){(e||document).querySelectorAll("pre code").forEach(function(e){var t=e.parentElement;if(!(!t||t.querySelector(".dars-code-copy"))){"static"===getComputedStyle(t).position&&(t.style.position="relative");var n=document.createElement("button");n.className="dars-code-copy",n.type="button",n.textContent="Copy",n.addEventListener("click",async function(t){t.stopPropagation();try{await navigator.clipboard.writeText(e.innerText),n.textContent="Copied",n.classList.add("copied"),setTimeout(function(){n.textContent="Copy",n.classList.remove("copied");},1200);}catch(e){n.textContent="Error",setTimeout(function(){n.textContent="Copy";},1200);}}),t.appendChild(n);}});},guessLang:function(e){var t=e.trim();return/^{[\s\S]*}$/.test(t)||/^\[/.test(t)?"json":/^(pip |python |python3 |dars |#|\$ )/m.test(t)?"bash":/\b(def |class |import |from |print\(|self\b)/.test(t)?"python":null;},stripPygments:function(e){e&&e.innerHTML&&-1!==e.innerHTML.indexOf("<span")&&(e.textContent=e.innerText);},highlight:function(e){var t=this;if(!window.Prism||!Prism.highlightElement){t._retries<20&&(t._retries++,setTimeout(function(){t.highlight(e);},150));return;}(e||document).querySelectorAll("pre code").forEach(function(e){if(t.stripPygments(e),!e.className||-1===e.className.indexOf("language-")){var n=t.guessLang(e.innerText);e.classList.add("language-"+(n||"none"));}Prism.highlightElement(e);}),t.addCopyButtons(e);}},"complete"===document.readyState?window.DarsMarkdown.highlight():window.addEventListener("load",function(){window.DarsMarkdown.highlight();}),document.addEventListener("DOMContentLoaded",function(){window.DarsMarkdown.highlight();}),document.addEventListener("dars:content-loaded",function(e){e.detail&&e.detail.element&&window.DarsMarkdown.highlight(e.detail.element);});}();