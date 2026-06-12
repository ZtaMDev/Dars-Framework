
    
    // Runtime
    // Dars Runtime
(function(){
    function initializeEvents() {
    // Evento click para componente image_0_1_0_0_0
    var __el_image_0_1_0_0_0 = document.getElementById("image_0_1_0_0_0");
    if (__el_image_0_1_0_0_0) {
        if (!__el_image_0_1_0_0_0.dataset.darsEvt_click) {
            __el_image_0_1_0_0_0.dataset.darsEvt_click = "1";
            __el_image_0_1_0_0_0.addEventListener("click", async function(event) {
            // Ensure runtime loaded if used
            if (!window.Dars) {
                try {
                    const m = await import('./lib/dars.min.js');
                    window.Dars = m.default || m;
                } catch (e) { }
            }
            try { window.location.href = 'https://ztamdev.github.io/Dars-Framework/'; } catch(e) { console.error("Error en handler:", e); }
        });
        }
    }

    // Evento click para componente text_0_1_0_0_1
    var __el_text_0_1_0_0_1 = document.getElementById("text_0_1_0_0_1");
    if (__el_text_0_1_0_0_1) {
        if (!__el_text_0_1_0_0_1.dataset.darsEvt_click) {
            __el_text_0_1_0_0_1.dataset.darsEvt_click = "1";
            __el_text_0_1_0_0_1.addEventListener("click", async function(event) {
            // Ensure runtime loaded if used
            if (!window.Dars) {
                try {
                    const m = await import('./lib/dars.min.js');
                    window.Dars = m.default || m;
                } catch (e) { }
            }
            try { window.location.href = 'https://ztamdev.github.io/Dars-Framework/'; } catch(e) { console.error("Error en handler:", e); }
        });
        }
    }

    
    // --- Default Logic for Advanced Components ---

    }
    
    function initializeStates() {
    // Inicializar estados
    try {
        const statesConfig = [
            {
                        "name": "counter",
                        "id": "counter",
                        "defaultValue": { "count": 0 },
                        "isV2": true
                    },
        ];
        if (window.Dars && typeof window.Dars.registerStates === "function") {
            window.Dars.registerStates(statesConfig);
        } else if (window.__DARS_STATES_FN) {
            window.__DARS_STATES_FN(statesConfig);
        } else {
            // Fallback: cargar runtime y luego registrar estados
            (async () => {
                try {
                    const m = await import("./lib/dars.min.js");
                    const registerStates = m.registerStates || (m.default && m.default.registerStates);
                    if (typeof registerStates === "function") {
                        registerStates(statesConfig);
                        window.__DARS_STATES_FN = registerStates;
                    }
                } catch (e) {
                    console.error("[Dars] Failed to initialize states", e);
                }
            })();
        }
    } catch (e) {
        console.error("[Dars] State initialization error", e);
    }
    }

    function _darsInit(){
        // Enable inline JS execution for compile-time generated code only.
        (async () => {
            try {
                const dap = await import('./lib/dap.js');
                if (dap.__darsConfig) dap.__darsConfig.allowInlineJS = true;
            } catch(_) {}
        })();
        // Ensure __DARS_SPA_CONFIG__ is available synchronously so that
        // network_request can resolve relative URLs against backendUrl
        // before the router finishes async initialisation.
        if (!window.__DARS_SPA_CONFIG__) {
            window.__DARS_SPA_CONFIG__ = {"backendUrl": "/"};
        } else if (!window.__DARS_SPA_CONFIG__.backendUrl) {
            window.__DARS_SPA_CONFIG__.backendUrl = {"backendUrl": "/"}.backendUrl;
        }
        initializeStates();
        initializeEvents();
        
            // No reactive bindings
        
            // No VRef bindings
        
        
        // Initialize Show/If conditional elements after VRef registry is ready
        (async () => {
            try {
                const dap = await import('./lib/dap.js');
                if (dap._initConditionalElements) await dap._initConditionalElements({});
            } catch(_) {}
        })();
    }

    if(document.readyState === 'complete' || document.readyState === 'interactive'){
        _darsInit();
    } else {
        document.addEventListener('DOMContentLoaded', _darsInit);
    }
})();


    // Page Scripts
    // Scripts específicos de esta página (combinados)
// Script: dScript
window.addEventListener("scroll", () => {
  const navbar = document.getElementById("dars-navbar");
  if (navbar) {
    if (window.scrollY > 20) {
      navbar.classList.add("scrolled");
    } else {
      navbar.classList.remove("scrolled");
    }
  }
});


document.addEventListener('DOMContentLoaded', function () {
  const hamburgerBtn = document.getElementById('hamburger-btn');
  const mobileMenu = document.getElementById('mobile-menu');
  const body = document.body;

  if (hamburgerBtn && mobileMenu) {
    hamburgerBtn.addEventListener('click', function (e) {
      e.stopPropagation();
      const isOpen = mobileMenu.style.display === 'flex';

      if (isOpen) {
        // Cerrar menÃº
        mobileMenu.style.display = 'none';
        hamburgerBtn.classList.remove('menu-open');
        body.classList.remove('menu-open');
      } else {
        // Abrir menÃº
        mobileMenu.style.display = 'flex';
        hamburgerBtn.classList.add('menu-open');
        body.classList.add('menu-open');
      }
    });

    // Cerrar menÃº al hacer clic en un enlace
    mobileMenu.querySelectorAll('a').forEach(link => {
      link.addEventListener('click', function () {
        mobileMenu.style.display = 'none';
        hamburgerBtn.classList.remove('menu-open');
        body.classList.remove('menu-open');
      });
    });

    // Cerrar menÃº al hacer clic fuera
    document.addEventListener('click', function (event) {
      if (!hamburgerBtn.contains(event.target) && !mobileMenu.contains(event.target)) {
        mobileMenu.style.display = 'none';
        hamburgerBtn.classList.remove('menu-open');
        body.classList.remove('menu-open');
      }
    });

    // Cerrar menÃº con tecla Escape
    document.addEventListener('keydown', function (event) {
      if (event.key === 'Escape' && mobileMenu.style.display === 'flex') {
        mobileMenu.style.display = 'none';
        hamburgerBtn.classList.remove('menu-open');
        body.classList.remove('menu-open');
      }
    });
  }
});

// Script: dScript
(function() {
    var layout = document.getElementById('markdown-layout');
    if (!layout) return;

    var style = document.createElement('style');
    style.textContent = `
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
    `;
    document.head.appendChild(style);
})();

// Script: dScript
(function() {
    var layout = document.getElementById('markdown-layout');
    if (!layout) return;

    var style = document.createElement('style');
    style.textContent = `
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
    `;
    document.head.appendChild(style);
})();

// Inline dict script
window.Prism=window.Prism||{};Prism.plugins=Prism.plugins||{};Prism.plugins.autoloader=Prism.plugins.autoloader||{};Prism.plugins.autoloader.languages_path="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/";

// Inline dict script
(function(){window.DarsMarkdown={_retries:0,addCopyButtons:function(root){(root||document).querySelectorAll("pre code").forEach(function(code){var pre=code.parentElement;if(!pre||pre.querySelector(".dars-code-copy"))return;if(getComputedStyle(pre).position==="static")pre.style.position="relative";var btn=document.createElement("button");btn.className="dars-code-copy";btn.type="button";btn.textContent="Copy";btn.addEventListener("click",async function(e){e.stopPropagation();try{await navigator.clipboard.writeText(code.innerText);btn.textContent="Copied";btn.classList.add("copied");setTimeout(function(){btn.textContent="Copy";btn.classList.remove("copied")},1200)}catch(err){btn.textContent="Error";setTimeout(function(){btn.textContent="Copy"},1200)}});pre.appendChild(btn)})},guessLang:function(text){var t=text.trim();if(/^{[\s\S]*}$/.test(t)||/^\[/.test(t))return "json";if(/^(pip |python |python3 |dars |#|\$ )/m.test(t))return "bash";if(/\b(def |class |import |from |print\(|self\b)/.test(t))return "python";return null},stripPygments:function(code){if(code&&code.innerHTML&&code.innerHTML.indexOf("<span")!==-1){code.textContent=code.innerText}},highlight:function(root){var self=this;if(!window.Prism||!Prism.highlightElement){if(self._retries<20){self._retries++;setTimeout(function(){self.highlight(root)},150)}return}(root||document).querySelectorAll("pre code").forEach(function(code){self.stripPygments(code);if(!code.className||code.className.indexOf("language-")===-1){var g=self.guessLang(code.innerText);code.classList.add("language-"+(g||"none"))}Prism.highlightElement(code)});self.addCopyButtons(root)}};if(document.readyState==="complete")window.DarsMarkdown.highlight();else window.addEventListener("load",function(){window.DarsMarkdown.highlight()});document.addEventListener("DOMContentLoaded",function(){window.DarsMarkdown.highlight()});document.addEventListener("dars:content-loaded",function(e){if(e.detail&&e.detail.element){window.DarsMarkdown.highlight(e.detail.element)}})})();

    