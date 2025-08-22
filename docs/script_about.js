// Scripts específicos de esta página
document.addEventListener('DOMContentLoaded', function() {
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

function initMobileDetection() {
    if (isMobileDevice()) {
        setTimeout(function() {
            var modal = document.getElementById('mobile-warning-modal');
            if (modal) {
                modal.style.display = 'flex';
            }
        }, 1000);
    }

    // También verificar al redimensionar la ventana
    window.addEventListener('resize', function() {
        var modal = document.getElementById('mobile-warning-modal');
        if (window.innerWidth <= 850) {
            if (modal) modal.style.display = 'flex';
        } else {
            if (modal) modal.style.display = 'none';
        }
    });
}

// Esperar a que el DOM esté completamente cargado
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initMobileDetection);
} else {
    initMobileDetection();
}

    // Script: dScript
    console.log('Dars-framework version: 1.0.62 running...')

});
