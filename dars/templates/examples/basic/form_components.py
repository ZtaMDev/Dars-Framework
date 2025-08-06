#!/usr/bin/env python3
"""
Plantilla: Componentes de Formulario - Dars Framework
Demuestra el uso completo de todos los componentes básicos de formulario:
Checkbox, RadioButton, Select, Slider, DatePicker

Esta plantilla es ideal para:
- Aprender a usar los nuevos componentes básicos
- Crear formularios complejos e interactivos
- Entender el sistema de eventos de Dars
- Diseñar interfaces de usuario modernas

Uso:
dars init mi_proyecto -t basic/form_components
"""

from dars.core.app import App
from dars.components.basic.container import Container
from dars.components.basic.text import Text
from dars.components.basic.button import Button
from dars.components.basic.checkbox import Checkbox
from dars.components.basic.radiobutton import RadioButton
from dars.components.basic.select import Select, SelectOption
from dars.components.basic.slider import Slider
from dars.components.basic.datepicker import DatePicker
from dars.scripts.script import InlineScript

# Crear aplicación
app = App(title="Dars - Componentes de Formulario")

# Contenedor principal
main_container = Container(style={
    'max-width': '800px',
    'margin': '0 auto',
    'padding': '40px 20px',
    'font-family': 'Arial, sans-serif'
})

# Título principal
title = Text(
    text="📋 Formulario Completo con Dars",
    style={
        'font-size': '32px',
        'font-weight': 'bold',
        'color': '#2c3e50',
        'text-align': 'center',
        'margin-bottom': '20px',
        'display': 'block'
    }
)

# Descripción
description = Text(
    text="Ejemplo completo de todos los componentes básicos de formulario disponibles en Dars Framework",
    style={
        'font-size': '16px',
        'color': '#7f8c8d',
        'text-align': 'center',
        'margin-bottom': '40px',
        'display': 'block'
    }
)

# Sección 1: Información Personal
personal_section = Container(style={
    'margin-bottom': '30px',
    'padding': '20px',
    'border': '1px solid #e0e0e0',
    'border-radius': '8px',
    'background-color': '#f9f9f9'
})

personal_title = Text(
    text="👤 Información Personal",
    style={
        'font-size': '20px',
        'font-weight': 'bold',
        'color': '#34495e',
        'margin-bottom': '15px',
        'display': 'block'
    }
)

# DatePicker para fecha de nacimiento
birth_date = DatePicker(
    placeholder="Fecha de nacimiento",
    format="DD/MM/YYYY",
    required=True,
    style={'margin-bottom': '15px', 'width': '200px'}
)

# Select para país
country_select = Select(
    options=[
        SelectOption("es", "España"),
        SelectOption("mx", "México"),
        SelectOption("ar", "Argentina"),
        SelectOption("co", "Colombia"),
        SelectOption("pe", "Perú"),
        SelectOption("cl", "Chile"),
        SelectOption("ve", "Venezuela"),
        SelectOption("ec", "Ecuador")
    ],
    placeholder="Selecciona tu país",
    required=True,
    style={'margin-bottom': '15px', 'width': '200px'}
)

# Sección 2: Preferencias
preferences_section = Container(style={
    'margin-bottom': '30px',
    'padding': '20px',
    'border': '1px solid #e0e0e0',
    'border-radius': '8px',
    'background-color': '#f9f9f9'
})

preferences_title = Text(
    text="⚙️ Preferencias",
    style={
        'font-size': '20px',
        'font-weight': 'bold',
        'color': '#34495e',
        'margin-bottom': '15px',
        'display': 'block'
    }
)

# Checkboxes para notificaciones
notifications_label = Text(
    text="Notificaciones:",
    style={'display': 'block', 'margin-bottom': '8px', 'font-weight': 'bold'}
)

email_notifications = Checkbox(
    label="Recibir notificaciones por email",
    name="notifications",
    value="email",
    checked=True
)

sms_notifications = Checkbox(
    label="Recibir notificaciones por SMS",
    name="notifications",
    value="sms"
)

push_notifications = Checkbox(
    label="Notificaciones push en el navegador",
    name="notifications",
    value="push",
    checked=True
)

# Radio buttons para tema
theme_label = Text(
    text="Tema de la aplicación:",
    style={'display': 'block', 'margin-bottom': '8px', 'margin-top': '20px', 'font-weight': 'bold'}
)

theme_light = RadioButton(
    label="Tema claro",
    name="theme",
    value="light",
    checked=True
)

theme_dark = RadioButton(
    label="Tema oscuro",
    name="theme",
    value="dark"
)

theme_auto = RadioButton(
    label="Automático (según sistema)",
    name="theme",
    value="auto"
)

# Sección 3: Configuración Avanzada
advanced_section = Container(style={
    'margin-bottom': '30px',
    'padding': '20px',
    'border': '1px solid #e0e0e0',
    'border-radius': '8px',
    'background-color': '#f9f9f9'
})

advanced_title = Text(
    text="🔧 Configuración Avanzada",
    style={
        'font-size': '20px',
        'font-weight': 'bold',
        'color': '#34495e',
        'margin-bottom': '15px',
        'display': 'block'
    }
)

# Slider para volumen
volume_slider = Slider(
    min_value=0,
    max_value=100,
    value=75,
    step=5,
    label="Volumen de notificaciones:",
    show_value=True,
    style={'margin-bottom': '20px'}
)

# Slider para calidad
quality_slider = Slider(
    min_value=1,
    max_value=5,
    value=3,
    step=1,
    label="Calidad de imagen (1=baja, 5=alta):",
    show_value=True,
    style={'margin-bottom': '20px'}
)

# Select múltiple para habilidades
skills_label = Text(
    text="Habilidades técnicas:",
    style={'display': 'block', 'margin-bottom': '8px', 'font-weight': 'bold'}
)

skills_select = Select(
    options=[
        "Python", "JavaScript", "HTML/CSS", "React", "Vue.js", 
        "Django", "Flask", "Node.js", "MongoDB", "PostgreSQL",
        "Docker", "Kubernetes", "AWS", "Git", "Linux"
    ],
    placeholder="Selecciona tus habilidades (múltiple)",
    multiple=True,
    size=6,
    style={'width': '100%', 'max-width': '400px'}
)

# Sección 4: Programación
schedule_section = Container(style={
    'margin-bottom': '30px',
    'padding': '20px',
    'border': '1px solid #e0e0e0',
    'border-radius': '8px',
    'background-color': '#f9f9f9'
})

schedule_title = Text(
    text="📅 Programación",
    style={
        'font-size': '20px',
        'font-weight': 'bold',
        'color': '#34495e',
        'margin-bottom': '15px',
        'display': 'block'
    }
)

# DatePicker con tiempo para cita
appointment_label = Text(
    text="Próxima cita:",
    style={'display': 'block', 'margin-bottom': '8px', 'font-weight': 'bold'}
)

appointment_date = DatePicker(
    placeholder="Selecciona fecha y hora",
    format="YYYY-MM-DD",
    show_time=True,
    style={'margin-bottom': '15px', 'width': '250px'}
)

# DatePicker para evento
event_label = Text(
    text="Fecha del evento (solo 2024):",
    style={'display': 'block', 'margin-bottom': '8px', 'font-weight': 'bold'}
)

event_date = DatePicker(
    placeholder="Fecha del evento",
    format="DD-MM-YYYY",
    min_date="01-01-2024",
    max_date="31-12-2024",
    style={'width': '200px'}
)

# Botones de acción
actions_container = Container(style={
    'text-align': 'center',
    'margin-top': '40px'
})

save_button = Button(
    text="💾 Guardar Configuración",
    style={
        'background-color': '#27ae60',
        'color': 'white',
        'padding': '12px 24px',
        'font-size': '16px',
        'font-weight': 'bold',
        'border': 'none',
        'border-radius': '6px',
        'cursor': 'pointer',
        'margin-right': '15px'
    }
)

reset_button = Button(
    text="🔄 Restablecer",
    style={
        'background-color': '#e74c3c',
        'color': 'white',
        'padding': '12px 24px',
        'font-size': '16px',
        'font-weight': 'bold',
        'border': 'none',
        'border-radius': '6px',
        'cursor': 'pointer'
    }
)

# Script para interactividad
script = InlineScript("""
document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 Formulario de componentes Dars cargado');
    
    // Actualizar valores de sliders en tiempo real
    const sliders = document.querySelectorAll('input[type="range"]');
    sliders.forEach(slider => {
        const valueDisplay = slider.parentElement.querySelector('.dars-slider-value');
        if (valueDisplay) {
            slider.addEventListener('input', function() {
                valueDisplay.textContent = this.value;
            });
        }
    });
    
    // Manejar botón de guardar
    const saveBtn = document.querySelector('button[style*="27ae60"]');
    if (saveBtn) {
        saveBtn.addEventListener('click', function() {
            const formData = collectFormData();
            console.log('📊 Datos del formulario:', formData);
            alert('✅ Configuración guardada exitosamente!\\n\\nRevisa la consola del navegador para ver todos los datos recopilados.');
        });
    }
    
    // Manejar botón de reset
    const resetBtn = document.querySelector('button[style*="e74c3c"]');
    if (resetBtn) {
        resetBtn.addEventListener('click', function() {
            if (confirm('¿Estás seguro de que quieres restablecer todos los valores?')) {
                resetForm();
                alert('🔄 Formulario restablecido a valores por defecto.');
            }
        });
    }
    
    // Función para recopilar datos del formulario
    function collectFormData() {
        const data = {
            personalInfo: {},
            preferences: {},
            advanced: {},
            schedule: {}
        };
        
        // Información personal
        const birthDate = document.querySelector('input[type="date"]');
        if (birthDate && birthDate.value) {
            data.personalInfo.birthDate = birthDate.value;
        }
        
        const countrySelect = document.querySelector('select:not([multiple])');
        if (countrySelect && countrySelect.value) {
            data.personalInfo.country = countrySelect.value;
        }
        
        // Preferencias - Checkboxes
        const notifications = [];
        const checkboxes = document.querySelectorAll('input[type="checkbox"]:checked');
        checkboxes.forEach(cb => {
            if (cb.name === 'notifications') {
                notifications.push(cb.value);
            }
        });
        data.preferences.notifications = notifications;
        
        // Preferencias - Tema
        const selectedTheme = document.querySelector('input[type="radio"]:checked');
        if (selectedTheme) {
            data.preferences.theme = selectedTheme.value;
        }
        
        // Configuración avanzada - Sliders
        const sliders = document.querySelectorAll('input[type="range"]');
        if (sliders.length >= 2) {
            data.advanced.volume = parseInt(sliders[0].value);
            data.advanced.quality = parseInt(sliders[1].value);
        }
        
        // Habilidades
        const skillsSelect = document.querySelector('select[multiple]');
        if (skillsSelect) {
            data.advanced.skills = Array.from(skillsSelect.selectedOptions).map(opt => opt.value);
        }
        
        // Programación
        const datetimeInput = document.querySelector('input[type="datetime-local"]');
        if (datetimeInput && datetimeInput.value) {
            data.schedule.appointment = datetimeInput.value;
        }
        
        return data;
    }
    
    // Función para restablecer formulario
    function resetForm() {
        // Restablecer checkboxes
        document.querySelectorAll('input[type="checkbox"]').forEach(cb => {
            cb.checked = cb.defaultChecked;
        });
        
        // Restablecer radio buttons
        document.querySelectorAll('input[type="radio"]').forEach(radio => {
            radio.checked = radio.defaultChecked;
        });
        
        // Restablecer selects
        document.querySelectorAll('select').forEach(select => {
            select.selectedIndex = 0;
        });
        
        // Restablecer sliders
        document.querySelectorAll('input[type="range"]').forEach(slider => {
            slider.value = slider.defaultValue;
            const valueDisplay = slider.parentElement.querySelector('.dars-slider-value');
            if (valueDisplay) {
                valueDisplay.textContent = slider.value;
            }
        });
        
        // Restablecer fechas
        document.querySelectorAll('input[type="date"], input[type="datetime-local"]').forEach(date => {
            date.value = '';
        });
    }
});
""")

# Ensamblar aplicación
main_container.add_child(title)
main_container.add_child(description)

# Sección personal
personal_section.add_child(personal_title)
personal_section.add_child(Text(text="Fecha de nacimiento:", style={'display': 'block', 'margin-bottom': '5px', 'font-weight': 'bold'}))
personal_section.add_child(birth_date)
personal_section.add_child(Text(text="País:", style={'display': 'block', 'margin-bottom': '5px', 'margin-top': '15px', 'font-weight': 'bold'}))
personal_section.add_child(country_select)
main_container.add_child(personal_section)

# Sección preferencias
preferences_section.add_child(preferences_title)
preferences_section.add_child(notifications_label)
preferences_section.add_child(email_notifications)
preferences_section.add_child(sms_notifications)
preferences_section.add_child(push_notifications)
preferences_section.add_child(theme_label)
preferences_section.add_child(theme_light)
preferences_section.add_child(theme_dark)
preferences_section.add_child(theme_auto)
main_container.add_child(preferences_section)

# Sección avanzada
advanced_section.add_child(advanced_title)
advanced_section.add_child(volume_slider)
advanced_section.add_child(quality_slider)
advanced_section.add_child(skills_label)
advanced_section.add_child(skills_select)
main_container.add_child(advanced_section)

# Sección programación
schedule_section.add_child(schedule_title)
schedule_section.add_child(appointment_label)
schedule_section.add_child(appointment_date)
schedule_section.add_child(event_label)
schedule_section.add_child(event_date)
main_container.add_child(schedule_section)

# Botones de acción
actions_container.add_child(save_button)
actions_container.add_child(reset_button)
main_container.add_child(actions_container)

# Configurar aplicación
app.set_root(main_container)
app.add_script(script)

# Añadir estilos globales
app.add_global_style('body', {
    'background-color': '#ecf0f1',
    'line-height': '1.6'
})

app.add_global_style('.dars-checkbox-wrapper, .dars-radio-wrapper', {
    'margin': '8px 0'
})

app.add_global_style('button:hover', {
    'transform': 'translateY(-1px)',
    'box-shadow': '0 4px 8px rgba(0,0,0,0.2)'
})

if __name__ == "__main__":
    app.rTimeCompile()  # Preview/compilación rápida
