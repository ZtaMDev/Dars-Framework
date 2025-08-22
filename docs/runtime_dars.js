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
document.getElementById('comp_245e6a50').onclick = function(event) {
document.getElementById('getting-started-section').scrollIntoView({
                                    behavior: 'smooth'
                                });
};
document.getElementById('comp_c6b8809d').onclick = function(event) {
window.open('https://github.com/ZtaMDev/Dars-Framework', '_blank');
};
