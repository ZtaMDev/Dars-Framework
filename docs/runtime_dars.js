// Dars Runtime - Página específica
    document.addEventListener('DOMContentLoaded', function() {
        console.log('Dars App loaded');
        
        // Inicializar eventos de componentes
        initializeEvents();
    });

    function initializeEvents() {
        // Asociación automática de eventos para componentes (bindings generados)
    var el = document.getElementById('comp_16'); if (el) el.addEventListener('click', function(event) {
document.getElementById('getting-started-section').scrollIntoView({
                                    behavior: 'smooth'
                                });
});
    var el = document.getElementById('comp_17'); if (el) el.addEventListener('click', function(event) {
window.open('https://ztamdev.github.io/Dars-Framework/documentation.html', '_blank');
});
}

// Fin del runtime generado para esta página
