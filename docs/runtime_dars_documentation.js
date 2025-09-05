// Dars Runtime - Página específica
    document.addEventListener('DOMContentLoaded', function() {
        console.log('Dars App loaded');
        
        // Inicializar eventos de componentes
        initializeEvents();
    });

    function initializeEvents() {
        // Asociación automática de eventos para componentes (bindings generados)
    var el = document.getElementById('comp_249'); if (el) el.addEventListener('click', function(event) {
const sidebar = document.getElementById('sidebar-links');
            if (sidebar.style.display === 'none' || sidebar.style.display === '') {
                sidebar.style.display = 'block';
            } else {
                sidebar.style.display = 'none';
            }
});
}

// Fin del runtime generado para esta página
