(()=>{(function(){function t(){}function e(){}function n(){}document.readyState==="complete"||document.readyState==="interactive"?n():document.addEventListener("DOMContentLoaded",n)})();window.addEventListener("scroll",()=>{const t=document.getElementById("dars-navbar");window.scrollY>20?t.classList.add("scrolled"):t.classList.remove("scrolled");const e=document.getElementById("features-section");if(e&&!e.classList.contains("visible")){const n=e.getBoundingClientRect().top,o=window.innerHeight/1.5;n<o&&(e.classList.add("visible"),document.querySelectorAll('[id^="feature-card-"]').forEach((i,r)=>{setTimeout(()=>{i.style.opacity="1",i.style.transform="translateY(0)"},r*100)}))}});document.addEventListener("DOMContentLoaded",function(){const t=document.getElementById("hamburger-btn"),e=document.getElementById("mobile-menu"),n=document.body;t&&e&&(t.addEventListener("click",function(o){o.stopPropagation(),e.style.display==="flex"?(e.style.display="none",t.classList.remove("menu-open"),n.classList.remove("menu-open")):(e.style.display="flex",t.classList.add("menu-open"),n.classList.add("menu-open"))}),e.querySelectorAll("a").forEach(o=>{o.addEventListener("click",function(){e.style.display="none",t.classList.remove("menu-open"),n.classList.remove("menu-open")})}),document.addEventListener("click",function(o){!t.contains(o.target)&&!e.contains(o.target)&&(e.style.display="none",t.classList.remove("menu-open"),n.classList.remove("menu-open"))}),document.addEventListener("keydown",function(o){o.key==="Escape"&&e.style.display==="flex"&&(e.style.display="none",t.classList.remove("menu-open"),n.classList.remove("menu-open"))}))});(function(){var t=document.getElementById("markdown-content-container");if(t){var e=document.createElement("style");e.textContent=`
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
    `,document.head.appendChild(e);for(var n=0,o=0,a=t.querySelectorAll("li"),i=0;i<a.length;i++){var r=a[i],s=r.textContent;if(/^\s*\[[ x]\]/.test(s)){n++;var d=/^\s*\[x\]/i.test(s);d&&o++;var m=d?"checked":"unchecked",u='<span class="dars-checkbox '+m+'"></span>';r.innerHTML=r.innerHTML.replace(/\[[ x]\]\s*/,""),r.insertAdjacentHTML("afterbegin",u),r.classList.add("dars-cb-li")}}if(n>0){var c=Math.round(o/n*100),l=document.getElementById("roadmap-progress-fill"),p=document.getElementById("roadmap-progress-text");l&&setTimeout(function(){l.style.width=c+"%"},300),p&&(p.textContent=o+" / "+n+" tasks ("+c+"%)")}}})();window.Prism=window.Prism||{};Prism.plugins=Prism.plugins||{};Prism.plugins.autoloader=Prism.plugins.autoloader||{};Prism.plugins.autoloader.languages_path="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/";(function(){window.DarsMarkdown={_retries:0,addCopyButtons:function(t){(t||document).querySelectorAll("pre code").forEach(function(e){var n=e.parentElement;if(!(!n||n.querySelector(".dars-code-copy"))){getComputedStyle(n).position==="static"&&(n.style.position="relative");var o=document.createElement("button");o.className="dars-code-copy",o.type="button",o.textContent="Copy",o.addEventListener("click",async function(a){a.stopPropagation();try{await navigator.clipboard.writeText(e.innerText),o.textContent="Copied",o.classList.add("copied"),setTimeout(function(){o.textContent="Copy",o.classList.remove("copied")},1200)}catch{o.textContent="Error",setTimeout(function(){o.textContent="Copy"},1200)}}),n.appendChild(o)}})},guessLang:function(t){var e=t.trim();return/^{[\s\S]*}$/.test(e)||/^\[/.test(e)?"json":/^(pip |python |python3 |dars |#|\$ )/m.test(e)?"bash":/\b(def |class |import |from |print\(|self\b)/.test(e)?"python":null},stripPygments:function(t){t&&t.innerHTML&&t.innerHTML.indexOf("<span")!==-1&&(t.textContent=t.innerText)},highlight:function(t){var e=this;if(!window.Prism||!Prism.highlightElement){e._retries<20&&(e._retries++,setTimeout(function(){e.highlight(t)},150));return}(t||document).querySelectorAll("pre code").forEach(function(n){if(e.stripPygments(n),!n.className||n.className.indexOf("language-")===-1){var o=e.guessLang(n.innerText);n.classList.add("language-"+(o||"none"))}Prism.highlightElement(n)}),e.addCopyButtons(t)}},document.readyState==="complete"?window.DarsMarkdown.highlight():window.addEventListener("load",function(){window.DarsMarkdown.highlight()}),document.addEventListener("DOMContentLoaded",function(){window.DarsMarkdown.highlight()}),document.addEventListener("dars:content-loaded",function(t){t.detail&&t.detail.element&&window.DarsMarkdown.highlight(t.detail.element)})})();})();
