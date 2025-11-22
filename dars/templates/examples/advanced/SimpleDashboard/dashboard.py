#!/usr/bin/env python3
"""
Dars - Ejemplo Avanzado: Dashboard
Demuestra layouts complejos, múltiples componentes y funcionalidad avanzada
"""

import sys
import os

from dars.all import *
from dars.core.state import this
from dars.scripts.dscript import dScript

# Crear la aplicación
app = App(title="Dashboard Empresarial - Dars")

# Contenedor principal
main_container = Container(
    style={
        'display': 'flex',
        'min-height': '100vh',
        'background-color': '#f8f9fa',
        'font-family': 'Arial, sans-serif'
    }
)

# Sidebar
sidebar = Container(
    id="sidebar",
    style={
        'width': '250px',
        'background-color': '#2c3e50',
        'color': 'white',
        'padding': '20px',
        'box-shadow': '2px 0 5px rgba(0,0,0,0.1)',
        'transition': 'left 0.3s ease'
    }
)

# Logo/Título del sidebar
logo = Text(
    text="Dashboard",
    style={
        'font-size': '24px',
        'font-weight': 'bold',
        'margin-bottom': '30px',
        'text-align': 'center',
        'color': '#ecf0f1'
    }
)

# Menú de navegación
menu_items = [
    ("Inicio", "inicio"),
    ("Ventas", "ventas"),
    ("Usuarios", "usuarios"),
    ("Configuracion", "config")
]

menu_container = Container(style={'margin-bottom': '30px'})

for texto, id_item in menu_items:
    menu_item = Button(
        id=f"menu-{id_item}",
        text=texto,
        style={
            'width': '100%',
            'background-color': 'transparent',
            'color': '#ecf0f1',
            'border': 'none',
            'padding': '12px 16px',
            'text-align': 'left',
            'cursor': 'pointer',
            'border-radius': '6px',
            'margin-bottom': '8px',
            'font-size': '16px',
            'transition': 'all 0.2s ease'
        },
        hover_style={
            'background-color': '#34495e',
            'transform': 'translateX(5px)'
        },
        on_click=dScript(f"cambiarPagina('{id_item}')")
    )
    menu_container.add_child(menu_item)

# Área de contenido principal
content_area = Container(
    id="content-area",
    style={
        'flex': '1',
        'padding': '30px',
        'overflow-y': 'auto',
        'transition': 'margin-left 0.3s ease'
    }
)

# Header del contenido
header = Container(
    style={
        'display': 'flex',
        'justify-content': 'space-between',
        'align-items': 'center',
        'margin-bottom': '30px',
        'padding-bottom': '20px',
        'border-bottom': '2px solid #dee2e6'
    }
)

titulo_pagina = Text(
    id="titulo-pagina",
    text="Panel de Control",
    style={
        'font-size': '32px',
        'color': '#2c3e50',
        'font-weight': 'bold'
    }
)

usuario_info = Text(
    text="Admin Usuario",
    style={
        'font-size': '16px',
        'color': '#6c757d'
    }
)

# Tarjetas de estadísticas
stats_container = Container(
    id="stats-container",
    style={
        'display': 'grid',
        'grid-template-columns': 'repeat(auto-fit, minmax(250px, 1fr))',
        'gap': '20px',
        'margin-bottom': '30px'
    }
)

# Función para crear tarjetas de estadísticas
def crear_stat_card(titulo, valor, color):
    card = Container(
        style={
            'background-color': 'white',
            'padding': '24px',
            'border-radius': '12px',
            'box-shadow': '0 2px 10px rgba(0,0,0,0.1)',
            'border-left': f'4px solid {color}',
            'transition': 'all 0.3s ease'
        },
        hover_style={
            'transform': 'translateY(-5px)',
            'box-shadow': '0 4px 20px rgba(0,0,0,0.15)'
        }
    )
    
    card_header = Container(
        style={
            'display': 'flex',
            'justify-content': 'space-between',
            'align-items': 'center',
            'margin-bottom': '10px'
        }
    )
    
    card_title = Text(
        text=titulo,
        style={
            'font-size': '14px',
            'color': '#6c757d',
            'font-weight': '500'
        }
    )
    
    card_value = Text(
        text=valor,
        style={
            'font-size': '28px',
            'color': '#2c3e50',
            'font-weight': 'bold'
        }
    )
    
    card_header.add_child(card_title)
    card.add_child(card_header)
    card.add_child(card_value)
    
    return card

# Crear tarjetas de estadísticas
stats_data = [
    ("Ventas Totales", "$125,430", "#28a745"),
    ("Usuarios Activos", "1,234", "#007bff"),
    ("Pedidos Hoy", "89", "#ffc107"),
    ("Ingresos Mes", "$45,210", "#dc3545")
]

for titulo, valor, color in stats_data:
    stats_container.add_child(crear_stat_card(titulo, valor, color))

# Área de contenido dinámico
dynamic_content = Container(
    id="dynamic-content",
    style={
        'background-color': 'white',
        'padding': '30px',
        'border-radius': '12px',
        'box-shadow': '0 2px 10px rgba(0,0,0,0.1)',
        'transition': 'opacity 0.15s ease'
    }
)

# Contenido inicial
contenido_inicial = Text(
    id="contenido-texto",
    text="Bienvenido al Dashboard. Selecciona una opción del menú para ver más información.",
    style={
        'font-size': '18px',
        'color': '#6c757d',
        'text-align': 'center',
        'line-height': '1.6'
    }
)

# Script para funcionalidad del dashboard
script = dScript("""
    // Estado de la aplicación
    window.currentPage = 'inicio';

    // Contenido de las páginas
    window.pageContent = {
        inicio: {
            titulo: 'Panel de Control',
            contenido: 'Bienvenido al Dashboard. Aquí puedes ver un resumen de todas las métricas importantes de tu negocio.'
        },
        ventas: {
            titulo: 'Gestion de Ventas',
            contenido: 'Aquí puedes ver todas las ventas realizadas, generar reportes y analizar tendencias de ventas.'
        },
        usuarios: {
            titulo: 'Gestion de Usuarios',
            contenido: 'Administra los usuarios del sistema, sus permisos y actividad reciente.'
        },
        config: {
            titulo: 'Configuracion',
            contenido: 'Configura los parámetros del sistema, notificaciones y preferencias generales.'
        }
    };

    // Función para cambiar de página
    window.cambiarPagina = function(pagina) {
        if (window.currentPage === pagina) return;
        
        window.currentPage = pagina;
        
        // Actualizar título
        const titulo = document.getElementById('titulo-pagina');
        if (titulo) {
            titulo.textContent = window.pageContent[pagina].titulo;
        }
        
        // Actualizar contenido
        const contenido = document.getElementById('contenido-texto');
        if (contenido) {
            contenido.textContent = window.pageContent[pagina].contenido;
        }
        
        // Actualizar estilos del menú
        window.actualizarMenuActivo(pagina);
        
        // Animación de entrada
        const dynamicContent = document.getElementById('dynamic-content');
        if (dynamicContent) {
            dynamicContent.style.opacity = '0';
            setTimeout(() => {
                dynamicContent.style.opacity = '1';
            }, 150);
        }
    };

    // Actualizar elemento activo del menú
    window.actualizarMenuActivo = function(paginaActiva) {
        const menuItems = ['inicio', 'ventas', 'usuarios', 'config'];
        
        menuItems.forEach(item => {
            const elemento = document.getElementById(`menu-${item}`);
            if (elemento) {
                if (item === paginaActiva) {
                    elemento.style.backgroundColor = '#34495e';
                    elemento.style.color = '#3498db';
                } else {
                    elemento.style.backgroundColor = 'transparent';
                    elemento.style.color = '#ecf0f1';
                }
            }
        });
    };

    // Animación de las tarjetas de estadísticas
    window.animarEstadisticas = function() {
        const statsContainer = document.getElementById('stats-container');
        if (!statsContainer) return;
        
        const cards = statsContainer.children;
        
        Array.from(cards).forEach((card, index) => {
            card.style.opacity = '0';
            card.style.transform = 'translateY(20px)';
            
            setTimeout(() => {
                card.style.transition = 'all 0.5s ease';
                card.style.opacity = '1';
                card.style.transform = 'translateY(0)';
            }, index * 100);
        });
    };

    // Simulación de datos en tiempo real
    window.actualizarDatosEnTiempoReal = function() {
        const valores = [
            { selector: 'Ventas Totales', base: 125430, variacion: 1000 },
            { selector: 'Usuarios Activos', base: 1234, variacion: 10 },
            { selector: 'Pedidos Hoy', base: 89, variacion: 5 },
            { selector: 'Ingresos Mes', base: 45210, variacion: 500 }
        ];
        
        valores.forEach(item => {
            const elementos = Array.from(document.querySelectorAll('span')).filter(el => 
                el.parentElement && el.parentElement.textContent.includes(item.selector)
            );
            
            if (elementos.length > 0) {
                const elemento = elementos[elementos.length - 1]; // Último elemento (el valor)
                const variacion = Math.floor(Math.random() * item.variacion * 2) - item.variacion;
                const nuevoValor = item.base + variacion;
                
                if (item.selector.includes('$')) {
                    elemento.textContent = `$${nuevoValor.toLocaleString()}`;
                } else {
                    elemento.textContent = nuevoValor.toLocaleString();
                }
            }
        });
    };

    // Configurar sidebar responsive
    window.configurarSidebarResponsive = function() {
        const sidebar = document.getElementById('sidebar');
        const contentArea = document.getElementById('content-area');
        
        function checkScreenSize() {
            if (window.innerWidth < 768) {
                sidebar.style.position = 'fixed';
                sidebar.style.left = '-250px';
                sidebar.style.zIndex = '1000';
                contentArea.style.marginLeft = '0';
            } else {
                sidebar.style.position = 'static';
                sidebar.style.left = '0';
                contentArea.style.marginLeft = '0';
            }
        }
        
        window.addEventListener('resize', checkScreenSize);
        checkScreenSize();
    };

    // Inicialización
    document.addEventListener('DOMContentLoaded', function() {
        // Configurar página inicial
        window.cambiarPagina('inicio');
        
        // Configurar animaciones
        setTimeout(() => {
            window.animarEstadisticas();
        }, 100);
        
        // Configurar responsive
        window.configurarSidebarResponsive();
        
        // Actualizar datos cada 30 segundos
        setInterval(window.actualizarDatosEnTiempoReal, 30000);
        
        console.log('Dashboard Dars cargado correctamente');
    });
""")

# Ensamblar la aplicación
sidebar.add_child(logo)
sidebar.add_child(menu_container)

header.add_child(titulo_pagina)
header.add_child(usuario_info)

dynamic_content.add_child(contenido_inicial)

content_area.add_child(header)
content_area.add_child(stats_container)
content_area.add_child(dynamic_content)

main_container.add_child(sidebar)
main_container.add_child(content_area)

app.set_root(main_container)
app.add_script(script)

if __name__ == "__main__":
    app.rTimeCompile(watchfiledialog=True)  # Preview/compilación rápida
