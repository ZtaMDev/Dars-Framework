// Dars Runtime - Página específica
    document.addEventListener('DOMContentLoaded', function() {
        console.log('Dars App loaded');
        
        // Inicializar eventos de componentes
        initializeEvents();
    });

    function initializeEvents() {
        // Los eventos específicos se agregarán aquí
    }

// Asociación automática de eventos Script para esta página
document.getElementById('comp_082828d4').onclick = function(event) {
document.getElementById('mobile-warning-modal').style.display = 'none';
};
document.getElementById('comp_3226e215').onclick = function(event) {
document.getElementById('getting-started-section').scrollIntoView({
                                    behavior: 'smooth'
                                });
};
document.getElementById('comp_1b6a9aa4').onclick = function(event) {
window.open('https://github.com/ZtaMDev/Dars-Framework', '_blank');
};
