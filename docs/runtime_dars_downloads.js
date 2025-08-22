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
document.getElementById('comp_f2cb9337').onclick = function(event) {
navigator.clipboard.writeText('pip install dars-framework')
                                        .then(() => alert('Command copied to clipboard!'))
                                        .catch(err => console.error('Failed to copy: ', err));
};
document.getElementById('comp_49acef48').onclick = function(event) {
window.location.href = 'https://github.com/ZtaMDev/Dars-Framework/tree/CrystalMain/dars/docs/getting_started.md';
};
document.getElementById('comp_21dc88ed').onclick = function(event) {
window.open('https://github.com/ZtaMDev/Dars-Framework/tree/CrystalMain/dars/templates/examples', '_blank');
};
