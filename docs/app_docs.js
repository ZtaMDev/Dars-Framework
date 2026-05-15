(()=>{(function(){function t(){}function e(){}function o(){}document.readyState==="complete"||document.readyState==="interactive"?o():document.addEventListener("DOMContentLoaded",o)})();window.addEventListener("scroll",()=>{const t=document.getElementById("dars-navbar");window.scrollY>20?t.classList.add("scrolled"):t.classList.remove("scrolled");const e=document.getElementById("features-section");if(e&&!e.classList.contains("visible")){const o=e.getBoundingClientRect().top,n=window.innerHeight/1.5;o<n&&(e.classList.add("visible"),document.querySelectorAll('[id^="feature-card-"]').forEach((r,a)=>{setTimeout(()=>{r.style.opacity="1",r.style.transform="translateY(0)"},a*100)}))}});document.addEventListener("DOMContentLoaded",function(){const t=document.getElementById("hamburger-btn"),e=document.getElementById("mobile-menu"),o=document.body;t&&e&&(t.addEventListener("click",function(n){n.stopPropagation(),e.style.display==="flex"?(e.style.display="none",t.classList.remove("menu-open"),o.classList.remove("menu-open")):(e.style.display="flex",t.classList.add("menu-open"),o.classList.add("menu-open"))}),e.querySelectorAll("a").forEach(n=>{n.addEventListener("click",function(){e.style.display="none",t.classList.remove("menu-open"),o.classList.remove("menu-open")})}),document.addEventListener("click",function(n){!t.contains(n.target)&&!e.contains(n.target)&&(e.style.display="none",t.classList.remove("menu-open"),o.classList.remove("menu-open"))}),document.addEventListener("keydown",function(n){n.key==="Escape"&&e.style.display==="flex"&&(e.style.display="none",t.classList.remove("menu-open"),o.classList.remove("menu-open"))}))});(function(){var t=document.getElementById("markdown-layout");if(t){var e=document.createElement("style");e.textContent=`
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
    `,document.head.appendChild(e)}})();window.Prism=window.Prism||{};Prism.plugins=Prism.plugins||{};Prism.plugins.autoloader=Prism.plugins.autoloader||{};Prism.plugins.autoloader.languages_path="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/";(function(){window.DarsMarkdown={_retries:0,addCopyButtons:function(t){(t||document).querySelectorAll("pre code").forEach(function(e){var o=e.parentElement;if(!(!o||o.querySelector(".dars-code-copy"))){getComputedStyle(o).position==="static"&&(o.style.position="relative");var n=document.createElement("button");n.className="dars-code-copy",n.type="button",n.textContent="Copy",n.addEventListener("click",async function(i){i.stopPropagation();try{await navigator.clipboard.writeText(e.innerText),n.textContent="Copied",n.classList.add("copied"),setTimeout(function(){n.textContent="Copy",n.classList.remove("copied")},1200)}catch{n.textContent="Error",setTimeout(function(){n.textContent="Copy"},1200)}}),o.appendChild(n)}})},guessLang:function(t){var e=t.trim();return/^{[\s\S]*}$/.test(e)||/^\[/.test(e)?"json":/^(pip |python |python3 |dars |#|\$ )/m.test(e)?"bash":/\b(def |class |import |from |print\(|self\b)/.test(e)?"python":null},stripPygments:function(t){t&&t.innerHTML&&t.innerHTML.indexOf("<span")!==-1&&(t.textContent=t.innerText)},highlight:function(t){var e=this;if(!window.Prism||!Prism.highlightElement){e._retries<20&&(e._retries++,setTimeout(function(){e.highlight(t)},150));return}(t||document).querySelectorAll("pre code").forEach(function(o){if(e.stripPygments(o),!o.className||o.className.indexOf("language-")===-1){var n=e.guessLang(o.innerText);o.classList.add("language-"+(n||"none"))}Prism.highlightElement(o)}),e.addCopyButtons(t)}},document.readyState==="complete"?window.DarsMarkdown.highlight():window.addEventListener("load",function(){window.DarsMarkdown.highlight()}),document.addEventListener("DOMContentLoaded",function(){window.DarsMarkdown.highlight()}),document.addEventListener("dars:content-loaded",function(t){t.detail&&t.detail.element&&window.DarsMarkdown.highlight(t.detail.element)})})();})();
