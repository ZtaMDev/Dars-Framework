// Scripts específicos de esta página (combinados)
// Script: dScript
const navRight = document.getElementById('navbar-right');
    const burger = document.getElementById('navbar-hamburger');

    burger.addEventListener('click', () => {
        if (navRight.style.right === '0px') {
            navRight.style.right = '-100%';
        } else {
            navRight.style.right = '0px';
        }
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
    var playgroundLink = document.getElementById('linkPlayground');
    if (!playgroundLink) return;

    if (isMobileDevice()) {
        playgroundLink.style.display = "none";  // Ocultar en móviles
    } else {
        playgroundLink.style.display = "";      // Mostrar en desktop
    }
}

function initMobileDetection() {
    // Ejecutar al cargar
    handlePlaygroundLink();

    // Re-verificar al redimensionar
    window.addEventListener('resize', handlePlaygroundLink);
}

// Esperar a que el DOM esté cargado
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initMobileDetection);
} else {
    initMobileDetection();
}

// Script: dScript
console.log('Dars-framework version: 1.1.1 running...')
