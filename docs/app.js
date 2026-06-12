
    
    // Runtime
    // Dars Runtime
(function(){
    function initializeEvents() {
    // Evento click para componente image_0_0_0_0_0
    var __el_image_0_0_0_0_0 = document.getElementById("image_0_0_0_0_0");
    if (__el_image_0_0_0_0_0) {
        if (!__el_image_0_0_0_0_0.dataset.darsEvt_click) {
            __el_image_0_0_0_0_0.dataset.darsEvt_click = "1";
            __el_image_0_0_0_0_0.addEventListener("click", async function(event) {
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

    // Evento click para componente text_0_0_0_0_1
    var __el_text_0_0_0_0_1 = document.getElementById("text_0_0_0_0_1");
    if (__el_text_0_0_0_0_1) {
        if (!__el_text_0_0_0_0_1.dataset.darsEvt_click) {
            __el_text_0_0_0_0_1.dataset.darsEvt_click = "1";
            __el_text_0_0_0_0_1.addEventListener("click", async function(event) {
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

    // Evento click para componente copy-btn
    var __el_copy_btn = document.getElementById("copy-btn");
    if (__el_copy_btn) {
        if (!__el_copy_btn.dataset.darsEvt_click) {
            __el_copy_btn.dataset.darsEvt_click = "1";
            __el_copy_btn.addEventListener("click", async function(event) {
            // Ensure runtime loaded if used
            if (!window.Dars) {
                try {
                    const m = await import('./lib/dars.min.js');
                    window.Dars = m.default || m;
                } catch (e) { }
            }
            try { var el = document.getElementById('pip-command-text'); if(el) navigator.clipboard.writeText(el.textContent || ''); } catch(e) { console.error("Error en handler:", e); }
            try { var _opts = {"dynamic": true, "text": "Copied!", "style": {"background": "linear-gradient(135deg, #38c49f 0%, #2a6b5b 100%) !important"}}; _opts.id = event.currentTarget ? event.currentTarget.id : (event.target ? event.target.id : ''); if (window.Dars && typeof window.Dars.change === 'function') window.Dars.change(_opts); else if (typeof change === 'function') change(_opts); } catch(e) { console.error("Error en handler:", e); }
            try { (new Promise((_res_timeout, _rej_timeout) => setTimeout(async () => { try { var _opts = {"dynamic": true, "text": "Copy", "style": {"background": "linear-gradient(135deg, #1d4a3f 0%, #2a6b5b 100%) !important"}}; _opts.id = event.currentTarget ? event.currentTarget.id : (event.target ? event.target.id : ''); if (window.Dars && typeof window.Dars.change === 'function') window.Dars.change(_opts); else if (typeof change === 'function') change(_opts);; _res_timeout(); } catch(e) { _rej_timeout(e); } }, 1000))) } catch(e) { console.error("Error en handler:", e); }
        });
        }
    }

    // Evento click para componente get-started-btn
    var __el_get_started_btn = document.getElementById("get-started-btn");
    if (__el_get_started_btn) {
        if (!__el_get_started_btn.dataset.darsEvt_click) {
            __el_get_started_btn.dataset.darsEvt_click = "1";
            __el_get_started_btn.addEventListener("click", async function(event) {
            // Ensure runtime loaded if used
            if (!window.Dars) {
                try {
                    const m = await import('./lib/dars.min.js');
                    window.Dars = m.default || m;
                } catch (e) { }
            }
            try { window.open('https://ztamdev.github.io/Dars-Framework/docs.html', '_blank'); } catch(e) { console.error("Error en handler:", e); }
        });
        }
    }

    // Evento click para componente demo-dec-btn
    var __el_demo_dec_btn = document.getElementById("demo-dec-btn");
    if (__el_demo_dec_btn) {
        if (!__el_demo_dec_btn.dataset.darsEvt_click) {
            __el_demo_dec_btn.dataset.darsEvt_click = "1";
            __el_demo_dec_btn.addEventListener("click", async function(event) {
            // Ensure runtime loaded if used
            if (!window.Dars) {
                try {
                    const m = await import('./lib/dars.min.js');
                    window.Dars = m.default || m;
                } catch (e) { }
            }
            try { if (window.Dars && typeof window.Dars.change === 'function') window.Dars.change({ id: "counter", dynamic: true, "count": (((window.Dars && window.Dars.getState('counter') && window.Dars.getState('counter').values && window.Dars.getState('counter').values['count'] !== undefined) ? window.Dars.getState('counter').values['count'] : 0) + -1) }); } catch(e) { console.error("Error en handler:", e); }
        });
        }
    }

    // Evento click para componente demo-inc-btn
    var __el_demo_inc_btn = document.getElementById("demo-inc-btn");
    if (__el_demo_inc_btn) {
        if (!__el_demo_inc_btn.dataset.darsEvt_click) {
            __el_demo_inc_btn.dataset.darsEvt_click = "1";
            __el_demo_inc_btn.addEventListener("click", async function(event) {
            // Ensure runtime loaded if used
            if (!window.Dars) {
                try {
                    const m = await import('./lib/dars.min.js');
                    window.Dars = m.default || m;
                } catch (e) { }
            }
            try { if (window.Dars && typeof window.Dars.change === 'function') window.Dars.change({ id: "counter", dynamic: true, "count": (((window.Dars && window.Dars.getState('counter') && window.Dars.getState('counter').values && window.Dars.getState('counter').values['count'] !== undefined) ? window.Dars.getState('counter').values['count'] : 0) + 1) }); } catch(e) { console.error("Error en handler:", e); }
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
        
            // Reactive bindings for useDynamic
    try {
        if (window.Dars && typeof window.Dars.addReactiveBinding === 'function') {
            window.Dars.addReactiveBinding(function(payload) {
                // Update reactive elements if this is a dynamic change
                if (payload && payload.dynamic && payload.id) {
                    // Built-in bindings for state 'counter'
                    if (payload.id === 'counter') {
                        let val_count = undefined;
                        if (payload.attrs && payload.attrs.count !== undefined) val_count = payload.attrs.count;
                        else if (payload.count !== undefined) val_count = payload.count;
                        if (val_count !== undefined) {
                            const el_demo_counter_value = document.getElementById('demo-counter-value');
                            if (el_demo_counter_value) {
                                if (el_demo_counter_value.hasAttribute('data-server-component') && el_demo_counter_value.firstElementChild) {
                                    el_demo_counter_value.firstElementChild.textContent = String(val_count);
                                } else {
                                    el_demo_counter_value.textContent = String(val_count);
                                }
                                if (el_demo_counter_value.hasAttribute('data-server-component') && el_demo_counter_value.firstElementChild) {
                                    el_demo_counter_value.firstElementChild.textContent = String(val_count);
                                } else {
                                    el_demo_counter_value.textContent = String(val_count);
                                }
                                if (el_demo_counter_value.hasAttribute('data-server-component') && el_demo_counter_value.firstElementChild) {
                                    el_demo_counter_value.firstElementChild.textContent = String(val_count);
                                } else {
                                    el_demo_counter_value.textContent = String(val_count);
                                }
                                if (el_demo_counter_value.hasAttribute('data-server-component') && el_demo_counter_value.firstElementChild) {
                                    el_demo_counter_value.firstElementChild.textContent = String(val_count);
                                } else {
                                    el_demo_counter_value.textContent = String(val_count);
                                }
                            }
                        }
                    }
                }
            });
        } else {
            console.warn('[Dars:Debug] window.Dars.addReactiveBinding NOT found. Skipping reactive bindings.');
        }
    } catch(e) {
        console.error('[Dars] Failed to initialize reactive bindings', e);
    }
        
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

// Fallback script: RawJS
(async () => {
    try {
        const result = await (async () => {
    try {
        const result = await (async () => {
    try {
        const result = await (async () => {
    try {
        const result = await (new Promise((_res_timeout, _rej_timeout) => setTimeout(async () => { try { var _el = document.getElementById("hero-logo"); if(_el) _el.classList.add("show");; _res_timeout(); } catch(e) { _rej_timeout(e); } }, 5)));
        // Make result available as 'value' or argument to next script
        const value = result; 
        await (async (value) => { 
            (new Promise((_res_timeout, _rej_timeout) => setTimeout(async () => { try { var _el = document.getElementById("hero-title"); if(_el) _el.classList.add("show");; _res_timeout(); } catch(e) { _rej_timeout(e); } }, 350))) 
        })(result);
        return result;
    } catch (e) {
        console.error("Chained script error:", e);
        throw e;
    }
})();
        // Make result available as 'value' or argument to next script
        const value = result; 
        await (async (value) => { 
            (new Promise((_res_timeout, _rej_timeout) => setTimeout(async () => { try { var _el = document.getElementById("hero-description"); if(_el) _el.classList.add("show");; _res_timeout(); } catch(e) { _rej_timeout(e); } }, 650))) 
        })(result);
        return result;
    } catch (e) {
        console.error("Chained script error:", e);
        throw e;
    }
})();
        // Make result available as 'value' or argument to next script
        const value = result; 
        await (async (value) => { 
            (new Promise((_res_timeout, _rej_timeout) => setTimeout(async () => { try { var _el = document.getElementById("pip-command"); if(_el) _el.classList.add("show");; _res_timeout(); } catch(e) { _rej_timeout(e); } }, 950))) 
        })(result);
        return result;
    } catch (e) {
        console.error("Chained script error:", e);
        throw e;
    }
})();
        // Make result available as 'value' or argument to next script
        const value = result; 
        await (async (value) => { 
            (new Promise((_res_timeout, _rej_timeout) => setTimeout(async () => { try { var _el = document.getElementById("get-started-btn"); if(_el) _el.classList.add("show");; _res_timeout(); } catch(e) { _rej_timeout(e); } }, 1250))) 
        })(result);
        return result;
    } catch (e) {
        console.error("Chained script error:", e);
        throw e;
    }
})()

// Fallback script: RawJS
;(function _w(){ if(window.DarsAnimation) window.DarsAnimation.animateOnView("example-title", [{"opacity": "0", "transform": "translateY(40px)"}, {"opacity": "1", "transform": "translateY(0)"}], {"duration": 800, "easing": "cubic-bezier(0.16, 1, 0.3, 1)", "fill": "forwards"}, {"threshold": 0.1, "rootMargin": "0px", "once": true}); else setTimeout(_w, 20); })();

// Fallback script: RawJS
;(function _w(){ if(window.DarsAnimation) window.DarsAnimation.animateOnView("example-subtitle", [{"opacity": "0", "transform": "translateY(30px)"}, {"opacity": "1", "transform": "translateY(0)"}], {"duration": 800, "easing": "cubic-bezier(0.16, 1, 0.3, 1)", "fill": "forwards"}, {"threshold": 0.2, "rootMargin": "0px", "once": true}); else setTimeout(_w, 20); })();

// Fallback script: RawJS
;(function _w(){ if(window.DarsAnimation) window.DarsAnimation.animateOnView("code-showcase", [{"opacity": "0", "transform": "translateY(50px) scale(0.97)"}, {"opacity": "1", "transform": "translateY(0) scale(1)"}], {"duration": 1000, "easing": "cubic-bezier(0.16, 1, 0.3, 1)", "fill": "forwards"}, {"threshold": 0.1, "rootMargin": "0px", "once": true}); else setTimeout(_w, 20); })();

// Fallback script: RawJS
;(function _w(){ if(window.DarsAnimation) window.DarsAnimation.staggerOnView(["feature-card-0", "feature-card-1", "feature-card-2"], [{"opacity": "0", "transform": "translateY(50px) rotateX(10deg)"}, {"opacity": "1", "transform": "translateY(0) rotateX(0deg)"}], {"duration": 800, "easing": "cubic-bezier(0.16, 1, 0.3, 1)", "fill": "forwards", "staggerDelay": 150}, {"threshold": 0.15, "once": true}); else setTimeout(_w, 20); })();

// Fallback script: RawJS
;(function _w(){ if(window.DarsAnimation) window.DarsAnimation.staggerOnView(["howitworks-step-1", "howitworks-step-2", "howitworks-step-3"], [{"opacity": "0", "transform": "translateY(40px) scale(0.95)"}, {"opacity": "1", "transform": "translateY(0) scale(1)"}], {"duration": 700, "easing": "cubic-bezier(0.16, 1, 0.3, 1)", "fill": "forwards", "staggerDelay": 180}, {"threshold": 0.1, "once": true}); else setTimeout(_w, 20); })();

// Fallback script: RawJS
(async () => {
    try {
        const result = await (async () => {
    try {
        const result = await (async () => {
    try {
        const result = await (async () => {
    try {
        const result = await (new Promise((_res_timeout, _rej_timeout) => setTimeout(async () => { try { var _el = document.getElementById("hero-logo"); if(_el) _el.classList.add("show");; _res_timeout(); } catch(e) { _rej_timeout(e); } }, 5)));
        // Make result available as 'value' or argument to next script
        const value = result; 
        await (async (value) => { 
            (new Promise((_res_timeout, _rej_timeout) => setTimeout(async () => { try { var _el = document.getElementById("hero-title"); if(_el) _el.classList.add("show");; _res_timeout(); } catch(e) { _rej_timeout(e); } }, 350))) 
        })(result);
        return result;
    } catch (e) {
        console.error("Chained script error:", e);
        throw e;
    }
})();
        // Make result available as 'value' or argument to next script
        const value = result; 
        await (async (value) => { 
            (new Promise((_res_timeout, _rej_timeout) => setTimeout(async () => { try { var _el = document.getElementById("hero-description"); if(_el) _el.classList.add("show");; _res_timeout(); } catch(e) { _rej_timeout(e); } }, 650))) 
        })(result);
        return result;
    } catch (e) {
        console.error("Chained script error:", e);
        throw e;
    }
})();
        // Make result available as 'value' or argument to next script
        const value = result; 
        await (async (value) => { 
            (new Promise((_res_timeout, _rej_timeout) => setTimeout(async () => { try { var _el = document.getElementById("pip-command"); if(_el) _el.classList.add("show");; _res_timeout(); } catch(e) { _rej_timeout(e); } }, 950))) 
        })(result);
        return result;
    } catch (e) {
        console.error("Chained script error:", e);
        throw e;
    }
})();
        // Make result available as 'value' or argument to next script
        const value = result; 
        await (async (value) => { 
            (new Promise((_res_timeout, _rej_timeout) => setTimeout(async () => { try { var _el = document.getElementById("get-started-btn"); if(_el) _el.classList.add("show");; _res_timeout(); } catch(e) { _rej_timeout(e); } }, 1250))) 
        })(result);
        return result;
    } catch (e) {
        console.error("Chained script error:", e);
        throw e;
    }
})()

// Fallback script: RawJS
;(function _w(){ if(window.DarsAnimation) window.DarsAnimation.animateOnView("example-title", [{"opacity": "0", "transform": "translateY(40px)"}, {"opacity": "1", "transform": "translateY(0)"}], {"duration": 800, "easing": "cubic-bezier(0.16, 1, 0.3, 1)", "fill": "forwards"}, {"threshold": 0.1, "rootMargin": "0px", "once": true}); else setTimeout(_w, 20); })();

// Fallback script: RawJS
;(function _w(){ if(window.DarsAnimation) window.DarsAnimation.animateOnView("example-subtitle", [{"opacity": "0", "transform": "translateY(30px)"}, {"opacity": "1", "transform": "translateY(0)"}], {"duration": 800, "easing": "cubic-bezier(0.16, 1, 0.3, 1)", "fill": "forwards"}, {"threshold": 0.2, "rootMargin": "0px", "once": true}); else setTimeout(_w, 20); })();

// Fallback script: RawJS
;(function _w(){ if(window.DarsAnimation) window.DarsAnimation.animateOnView("code-showcase", [{"opacity": "0", "transform": "translateY(50px) scale(0.97)"}, {"opacity": "1", "transform": "translateY(0) scale(1)"}], {"duration": 1000, "easing": "cubic-bezier(0.16, 1, 0.3, 1)", "fill": "forwards"}, {"threshold": 0.1, "rootMargin": "0px", "once": true}); else setTimeout(_w, 20); })();

// Fallback script: RawJS
;(function _w(){ if(window.DarsAnimation) window.DarsAnimation.staggerOnView(["feature-card-0", "feature-card-1", "feature-card-2"], [{"opacity": "0", "transform": "translateY(50px) rotateX(10deg)"}, {"opacity": "1", "transform": "translateY(0) rotateX(0deg)"}], {"duration": 800, "easing": "cubic-bezier(0.16, 1, 0.3, 1)", "fill": "forwards", "staggerDelay": 150}, {"threshold": 0.15, "once": true}); else setTimeout(_w, 20); })();

// Fallback script: RawJS
;(function _w(){ if(window.DarsAnimation) window.DarsAnimation.staggerOnView(["howitworks-step-1", "howitworks-step-2", "howitworks-step-3"], [{"opacity": "0", "transform": "translateY(40px) scale(0.95)"}, {"opacity": "1", "transform": "translateY(0) scale(1)"}], {"duration": 700, "easing": "cubic-bezier(0.16, 1, 0.3, 1)", "fill": "forwards", "staggerDelay": 180}, {"threshold": 0.1, "once": true}); else setTimeout(_w, 20); })();

// Inline dict script
window.Prism=window.Prism||{};Prism.plugins=Prism.plugins||{};Prism.plugins.autoloader=Prism.plugins.autoloader||{};Prism.plugins.autoloader.languages_path="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/";

// Inline dict script
(function(){window.DarsMarkdown={_retries:0,addCopyButtons:function(root){(root||document).querySelectorAll("pre code").forEach(function(code){var pre=code.parentElement;if(!pre||pre.querySelector(".dars-code-copy"))return;if(getComputedStyle(pre).position==="static")pre.style.position="relative";var btn=document.createElement("button");btn.className="dars-code-copy";btn.type="button";btn.textContent="Copy";btn.addEventListener("click",async function(e){e.stopPropagation();try{await navigator.clipboard.writeText(code.innerText);btn.textContent="Copied";btn.classList.add("copied");setTimeout(function(){btn.textContent="Copy";btn.classList.remove("copied")},1200)}catch(err){btn.textContent="Error";setTimeout(function(){btn.textContent="Copy"},1200)}});pre.appendChild(btn)})},guessLang:function(text){var t=text.trim();if(/^{[\s\S]*}$/.test(t)||/^\[/.test(t))return "json";if(/^(pip |python |python3 |dars |#|\$ )/m.test(t))return "bash";if(/\b(def |class |import |from |print\(|self\b)/.test(t))return "python";return null},stripPygments:function(code){if(code&&code.innerHTML&&code.innerHTML.indexOf("<span")!==-1){code.textContent=code.innerText}},highlight:function(root){var self=this;if(!window.Prism||!Prism.highlightElement){if(self._retries<20){self._retries++;setTimeout(function(){self.highlight(root)},150)}return}(root||document).querySelectorAll("pre code").forEach(function(code){self.stripPygments(code);if(!code.className||code.className.indexOf("language-")===-1){var g=self.guessLang(code.innerText);code.classList.add("language-"+(g||"none"))}Prism.highlightElement(code)});self.addCopyButtons(root)}};if(document.readyState==="complete")window.DarsMarkdown.highlight();else window.addEventListener("load",function(){window.DarsMarkdown.highlight()});document.addEventListener("DOMContentLoaded",function(){window.DarsMarkdown.highlight()});document.addEventListener("dars:content-loaded",function(e){if(e.detail&&e.detail.element){window.DarsMarkdown.highlight(e.detail.element)}})})();

    