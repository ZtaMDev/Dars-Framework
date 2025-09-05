// Dars Runtime - Página específica
    document.addEventListener('DOMContentLoaded', function() {
        console.log('Dars App loaded');
        
        // Inicializar eventos de componentes
        initializeEvents();
    });

    function initializeEvents() {
        // Asociación automática de eventos para componentes (bindings generados)
    var el = document.getElementById('comp_179'); if (el) el.addEventListener('click', function(event) {
navigator.clipboard.writeText('pip install dars-framework')
                                        .then(() => alert('Command copied to clipboard!'))
                                        .catch(err => console.error('Failed to copy: ', err));
});
    var el = document.getElementById('comp_231'); if (el) el.addEventListener('click', function(event) {
window.location.href = 'https://ztamdev.github.io/Dars-Framework/documentation.html#getting-started-with-dars';
});
    var el = document.getElementById('comp_232'); if (el) el.addEventListener('click', function(event) {
window.open('https://github.com/ZtaMDev/Dars-Framework/tree/CrystalMain/dars/templates/examples', '_blank');
});
}

// Fin del runtime generado para esta página
