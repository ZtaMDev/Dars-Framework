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
document.getElementById('comp_af5c5d9e').onclick = function(event) {
navigator.clipboard.writeText('pip install dars-framework')
                                        .then(() => alert('Command copied to clipboard!'))
                                        .catch(err => console.error('Failed to copy: ', err));
};
document.getElementById('comp_5edceb9c').onclick = function(event) {
window.location.href = '/getting-started.html';
};
document.getElementById('comp_16bdde71').onclick = function(event) {
window.open('https://github.com/ZtaMDev/Dars-Framework/tree/CrystalMain/examples', '_blank');
};
