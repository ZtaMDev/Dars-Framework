import { $ } from "./dars.min.js";

const __observers = new Map();
const __scrollHandlers = new Map();
let __scrollRAF = null;

/**
 * DarsAnimation - Complete animation engine
 * Provides: viewport triggers, keyframe animations, stagger, timeline, scroll-progress
 */
export const DarsAnimation = {
  /**
   * Internal: run fn when DOM is ready. If already ready, run immediately.
   */
  _whenReady(fn) {
    if (document.readyState === "loading") {
      document.addEventListener("DOMContentLoaded", fn, { once: true });
    } else {
      fn();
    }
  },

  /**
   * Helper: Apply styles without triggering CSS transitions.
   */
  _setStylesWithoutTransition(el, styles) {
    if (!el || !styles) return;
    try {
      const oldTrans = el.style.getPropertyValue('transition');
      const oldPri = el.style.getPropertyPriority('transition');
      el.style.setProperty('transition', 'none', 'important');
      
      for (const k in styles) {
        if (k !== 'offset' && k !== 'easing') {
          el.style[k] = styles[k];
        }
      }
      
      void el.offsetHeight; // Force reflow
      
      if (oldTrans) el.style.setProperty('transition', oldTrans, oldPri);
      else el.style.removeProperty('transition');
    } catch(e) {}
  },

  /**
   * Observe an element for viewport entry/exit via IntersectionObserver.
   */
  observe(id, opts = {}) {
    const _run = () => {
      try {
        const el = $(id);
        if (!el) return;
        if (__observers.has(id)) {
          __observers.get(id).disconnect();
          __observers.delete(id);
        }
        const threshold = opts.threshold ?? 0.1;
        const rootMargin = opts.rootMargin || "0px";
        const once = opts.once !== false;
        const observer = new IntersectionObserver((entries) => {
          for (const entry of entries) {
            if (entry.isIntersecting) {
              if (opts.enterClass) el.classList.add(opts.enterClass);
              if (opts.leaveClass) el.classList.remove(opts.leaveClass);
              if (typeof opts.onEnter === "function") opts.onEnter(el, entry);
              if (once) { observer.unobserve(el); __observers.delete(id); }
            } else {
              if (opts.leaveClass) el.classList.add(opts.leaveClass);
              if (opts.enterClass) el.classList.remove(opts.enterClass);
              if (typeof opts.onLeave === "function") opts.onLeave(el, entry);
            }
          }
        }, { threshold, rootMargin });
        observer.observe(el);
        __observers.set(id, observer);
      } catch(e) { console.error("[DarsAnimation:observe]", e); }
    };
    this._whenReady(_run);
  },

  /**
   * Unobserve an element.
   */
  unobserve(id) {
    if (__observers.has(id)) {
      __observers.get(id).disconnect();
      __observers.delete(id);
    }
  },

  /**
   * Run a Web Animations API animation on an element.
   * @param {string} id - Element ID
   * @param {Array} keyframes - Keyframe array
   * @param {object} options - { duration, easing, fill, iterations, delay, direction }
   * @returns {Promise} resolves when animation finishes
   */
  animate(id, keyframes, options = {}) {
    return new Promise((resolve, reject) => {
      try {
        const el = $(id);
        if (!el) {
          resolve();
          return;
        }
        const opts = {
          duration: options.duration ?? 300,
          easing: options.easing || "ease",
          fill: options.fill || "forwards",
          iterations: options.iterations ?? 1,
          delay: options.delay ?? 0,
          direction: options.direction || "normal",
        };
        if (options.iterations === "infinite") opts.iterations = Infinity;
        const anim = el.animate(keyframes, opts);
        
        anim.onfinish = () => {
          try {
            if (opts.fill === "forwards" && keyframes.length > 0) {
              const finalFrame = keyframes[keyframes.length - 1];
              // Apply final frame inline safely
              DarsAnimation._setStylesWithoutTransition(el, finalFrame);
              // Cancel WAAPI animation to release its priority lock over CSS !important
              anim.cancel();
            }
          } catch (_) {}
          resolve(anim);
        };
        
        anim.oncancel = () => resolve(anim);
      } catch (e) {
        console.error("[DarsAnimation:animate]", e);
        resolve();
      }
    });
  },

  /**
   * Animate when element enters viewport.
   * @param {string} id - Element ID
   * @param {Array} keyframes - Keyframe array
   * @param {object} animOpts - Animation options
   * @param {object} viewOpts - Viewport observer options
   */
  animateOnView(id, keyframes, animOpts = {}, viewOpts = {}) {
    const self = this;
    this._whenReady(() => {
      // Set initial hidden state
      try {
        const el = $(id);
        if (el && keyframes.length > 0) {
          self._setStylesWithoutTransition(el, keyframes[0]);
        }
      } catch (_) {}
      self.observe(id, {
        threshold: viewOpts.threshold ?? 0.1,
        rootMargin: viewOpts.rootMargin || "0px",
        once: viewOpts.once !== false,
        onEnter(el) {
          self.animate(id, keyframes, animOpts);
        },
        onLeave: viewOpts.onLeave || null,
      });
    });
  },

  /**
   * Stagger animations across multiple elements.
   * @param {Array<string>} ids - Array of element IDs
   * @param {Array} keyframes - Shared keyframes
   * @param {object} options - Animation options + staggerDelay (ms between each)
   * @returns {Promise}
   */
  stagger(ids, keyframes, options = {}) {
    const staggerDelay = options.staggerDelay ?? 100;
    const promises = ids.map((id, i) => {
      const opts = Object.assign({}, options, {
        delay: (options.delay ?? 0) + i * staggerDelay,
      });
      delete opts.staggerDelay;
      return this.animate(id, keyframes, opts);
    });
    return Promise.all(promises);
  },

  /**
   * Stagger on viewport entry.
   */
  staggerOnView(ids, keyframes, animOpts = {}, viewOpts = {}) {
    if (!ids.length) return;
    const self = this;
    this._whenReady(() => {
      // Set initial state on all elements
      try {
        if (keyframes.length > 0) {
          ids.forEach((id) => {
            const el = $(id);
            if (el) self._setStylesWithoutTransition(el, keyframes[0]);
          });
        }
      } catch (_) {}
      // Observe first element as trigger
      self.observe(ids[0], {
        threshold: viewOpts.threshold ?? 0.1,
        rootMargin: viewOpts.rootMargin || "0px 0px -50px 0px",
        once: viewOpts.once !== false,
        onEnter() {
          self.stagger(ids, keyframes, animOpts);
        },
      });
    });
  },

  /**
   * Run a timeline of sequential animations.
   * @param {Array<{id, keyframes, options}>} steps
   * @returns {Promise}
   */
  async timeline(steps) {
    for (const step of steps) {
      if (step.delay) await new Promise((r) => setTimeout(r, step.delay));
      await this.animate(step.id, step.keyframes, step.options || {});
    }
  },

  /**
   * Link an element's style to scroll progress (0-1).
   * @param {string} id - Element ID
   * @param {object} opts - { property, from, to, unit, start, end }
   */
  scrollProgress(id, opts = {}) {
    const config = {
      property: opts.property || "opacity",
      from: opts.from ?? 0,
      to: opts.to ?? 1,
      unit: opts.unit || "",
      start: opts.start ?? 0,
      end: opts.end ?? 1,
    };
    __scrollHandlers.set(id, config);
    if (!__scrollRAF) {
      const tick = () => {
        const scrollTop = window.scrollY || document.documentElement.scrollTop;
        const docHeight = Math.max(
          document.documentElement.scrollHeight - window.innerHeight,
          1,
        );
        const progress = Math.min(Math.max(scrollTop / docHeight, 0), 1);
        for (const [eid, cfg] of __scrollHandlers) {
          try {
            const el = $(eid);
            if (!el) continue;
            const range = cfg.end - cfg.start;
            const local =
              range > 0
                ? Math.min(Math.max((progress - cfg.start) / range, 0), 1)
                : 0;
            const val = cfg.from + (cfg.to - cfg.from) * local;
            el.style[cfg.property] = val + cfg.unit;
          } catch (_) {}
        }
        __scrollRAF = requestAnimationFrame(tick);
      };
      __scrollRAF = requestAnimationFrame(tick);
    }
  },

  /**
   * Remove scroll progress handler.
   */
  removeScrollProgress(id) {
    __scrollHandlers.delete(id);
    if (__scrollHandlers.size === 0 && __scrollRAF) {
      cancelAnimationFrame(__scrollRAF);
      __scrollRAF = null;
    }
  },

  /**
   * Add CSS class when element is in viewport (simple utility).
   */
  classOnView(id, className, opts = {}) {
    this.observe(id, {
      threshold: opts.threshold ?? 0.1,
      rootMargin: opts.rootMargin || "0px",
      once: opts.once !== false,
      enterClass: className,
      leaveClass: opts.leaveClass || null,
    });
  },

  /**
   * Execute arbitrary code when element enters viewport.
   */
  runOnView(id, code, opts = {}) {
    this.observe(id, {
      threshold: opts.threshold ?? 0.1,
      rootMargin: opts.rootMargin || "0px",
      once: opts.once !== false,
      onEnter: code,
    });
  },

  /**
   * Cleanup all observers and scroll handlers.
   */
  destroy() {
    for (const [, obs] of __observers) obs.disconnect();
    __observers.clear();
    __scrollHandlers.clear();
    if (__scrollRAF) {
      cancelAnimationFrame(__scrollRAF);
      __scrollRAF = null;
    }
  },
};
