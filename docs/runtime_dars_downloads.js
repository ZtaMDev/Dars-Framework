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
document.getElementById('comp_a89b5276').onclick = function(event) {
navigator.clipboard.writeText('pip install dars-framework')
                                        .then(() => alert('Command copied to clipboard!'))
                                        .catch(err => console.error('Failed to copy: ', err));
};
document.getElementById('comp_5662129b').onclick = function(event) {
window.location.href = '/getting-started.html';
};
document.getElementById('comp_14a15aba').onclick = function(event) {
window.open('https://github.com/ZtaMDev/Dars-Framework/tree/CrystalMain/examples', '_blank');
};
