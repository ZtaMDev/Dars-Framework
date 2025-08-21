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
document.getElementById('comp_f470a6da').onclick = function(event) {
document.getElementById('mobile-warning-modal').style.display = 'none';
};
document.getElementById('comp_9e8c8554').onclick = function(event) {
document.getElementById('getting-started-section').scrollIntoView({
                                    behavior: 'smooth'
                                });
};
document.getElementById('comp_96c800e3').onclick = function(event) {
window.open('https://github.com/ZtaMDev/Dars-Framework', '_blank');
};
