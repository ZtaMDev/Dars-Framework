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
document.getElementById('comp_d8146a5f').onclick = function(event) {
document.getElementById('getting-started-section').scrollIntoView({
                                    behavior: 'smooth'
                                });
};
document.getElementById('comp_e1f0cf7c').onclick = function(event) {
window.open('https://github.com/ZtaMDev/Dars-Framework', '_blank');
};
