// Scripts específicos de esta página (combinados)
// Script: dScript
document.addEventListener('DOMContentLoaded', function initNav() {
    const navRight = document.getElementById('navbar-right');
    const burger = document.getElementById('navbar-hamburger');

    // Safety guards in case elements are not present yet
    if (!burger || !navRight) return;

    // Ensure overlay exists (hidden) so we can reuse it
    let overlay = document.getElementById('nav-overlay');
    if (!overlay) {
        overlay = document.createElement('div');
        overlay.id = 'nav-overlay';
        overlay.style.position = 'fixed';
        overlay.style.top = '0';
        overlay.style.left = '0';
        overlay.style.width = '100%';
        overlay.style.height = '100%';
        overlay.style.background = 'rgba(0,0,0,0.35)';
        overlay.style.zIndex = '1999';
        overlay.style.display = 'none';
        document.body.appendChild(overlay);
    }

    function openMenu() {
        navRight.classList.add('open');
        overlay.style.display = 'block';
    }
    function closeMenu() {
        navRight.classList.remove('open');
        overlay.style.display = 'none';
    }

    burger.addEventListener('click', function (e) {
        e.stopPropagation();
        if (navRight.classList.contains('open')) closeMenu(); else openMenu();
    });

    // Close when clicking overlay
    overlay.addEventListener('click', function () {
        closeMenu();
    });

    // Close menu when any nav link is clicked (mobile behavior)
    const links = navRight.querySelectorAll('.nav-link');
    links.forEach(link => link.addEventListener('click', closeMenu));

    // Also close when tapping outside via document listener
    document.addEventListener('click', function (ev) {
        const target = ev.target;
        if (!navRight.contains(target) && target !== burger) {
            if (navRight.classList.contains('open')) closeMenu();
        }
    });
});

// Script: dScript
window.addEventListener('load', () => {
    const overlay = document.getElementById('page-overlay');
    if (overlay) {
        overlay.style.opacity = '0';
        setTimeout(() => overlay.remove(), 1600);  // se elimina después de la transición
    }
});

// Script: dScript
document.addEventListener('DOMContentLoaded', () => {
    // Selecciona todos los bloques Markdown sin tocar su id
    const markdownBlocks = document.querySelectorAll('.markdown-docs');

    markdownBlocks.forEach(block => {
        block.classList.add('lazy-hidden'); // Oculto al inicio
    });

    const observerOptions = {
        root: null,
        rootMargin: '300px',
        threshold: 0.1
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if(entry.isIntersecting){
                entry.target.classList.add('lazy-visible');
                entry.target.classList.remove('lazy-hidden');
            } else {
                entry.target.classList.remove('lazy-visible');
                entry.target.classList.add('lazy-hidden');
            }
        });
    }, observerOptions);

    markdownBlocks.forEach(block => observer.observe(block));
});

// Script: dScript
function isMobileDevice() {
    return (typeof window.orientation !== "undefined") || 
           (navigator.userAgent.indexOf('IEMobile') !== -1) ||
           (navigator.userAgent.indexOf('Android') !== -1) ||
           (navigator.userAgent.indexOf('iPhone') !== -1) ||
           (navigator.userAgent.indexOf('iPad') !== -1) ||
           (navigator.userAgent.indexOf('iPod') !== -1) ||
           (window.innerWidth <= 850);
}

function handlePlaygroundLink() {
    // KEEP: Always keep the Playground link visible on all devices
    var playgroundLink = document.getElementById('linkPlayground');
    if (!playgroundLink) return;
    playgroundLink.style.display = ""; // ensure visible
}

function initMobileDetection() {
    // Ejecutar al cargar
    handlePlaygroundLink();

    // Re-verificar al redimensionar (no ocultaremos el playground)
    window.addEventListener('resize', handlePlaygroundLink);
}

// Esperar a que el DOM esté cargado
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initMobileDetection);
} else {
    initMobileDetection();
}

// Script: dScript
console.log('Dars-framework version: 1.1.8 running...')
