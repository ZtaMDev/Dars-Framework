// Dars Runtime
document.addEventListener('DOMContentLoaded', function() {
    console.log('Dars App loaded');
    
    // Inicializar eventos de componentes
    initializeEvents();
});

function initializeEvents() {
    // Los eventos específicos se agregarán aquí
}

// Script: InlineScript

function manejarClick() {
    alert('¡Felicidades! Has creado tu primera aplicación Dars');
    console.log('Botón presionado en Hello World');
}

document.addEventListener('DOMContentLoaded', function() {
    const boton = document.querySelector('button');
    if (boton) {
        boton.addEventListener('click', manejarClick);
        
        // Efecto hover
        boton.addEventListener('mouseenter', function() {
            this.style.backgroundColor = '#2980b9';
        });
        
        boton.addEventListener('mouseleave', function() {
            this.style.backgroundColor = '#3498db';
        });
    }
});


