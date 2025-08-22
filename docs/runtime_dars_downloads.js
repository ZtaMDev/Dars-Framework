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
document.getElementById('comp_0b551e91').onclick = function(event) {
navigator.clipboard.writeText('pip install dars-framework')
                                        .then(() => alert('Command copied to clipboard!'))
                                        .catch(err => console.error('Failed to copy: ', err));
};
document.getElementById('comp_a07ba0f1').onclick = function(event) {
window.location.href = '/getting-started.html';
};
document.getElementById('comp_debc4c65').onclick = function(event) {
window.open('https://github.com/ZtaMDev/Dars-Framework/tree/CrystalMain/dars/templates/examples', '_blank');
};
