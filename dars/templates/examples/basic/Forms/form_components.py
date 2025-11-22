#!/usr/bin/env python3
"""
Plantilla: Componentes de Formulario - Dars Framework
Demuestra el uso completo de todos los componentes básicos de formulario:
Checkbox, RadioButton, Select, Slider, DatePicker
"""

from dars.all import *

# Crear aplicación
app = App(title="Dars - Componentes de Formulario")

# Script de utilidades
utils_script = dScript("""
    window.collectFormData = function() {
        const data = {
            personalInfo: {},
            preferences: {},
            advanced: {},
            schedule: {}
        };
        
        // Información personal
        const birthDate = document.querySelector('input[type="date"]');
        if (birthDate && birthDate.value) data.personalInfo.birthDate = birthDate.value;
        
        const countrySelect = document.querySelector('select:not([multiple])');
        if (countrySelect && countrySelect.value) data.personalInfo.country = countrySelect.value;
        
        // Preferencias
        const notifications = [];
        document.querySelectorAll('input[name="notifications"]:checked').forEach(cb => notifications.push(cb.value));
        data.preferences.notifications = notifications;
        
        const selectedTheme = document.querySelector('input[name="theme"]:checked');
        if (selectedTheme) data.preferences.theme = selectedTheme.value;
        
        // Avanzada
        const sliders = document.querySelectorAll('input[type="range"]');
        if (sliders.length >= 2) {
            data.advanced.volume = parseInt(sliders[0].value);
            data.advanced.quality = parseInt(sliders[1].value);
        }
        
        const skillsSelect = document.querySelector('select[multiple]');
        if (skillsSelect) {
            data.advanced.skills = Array.from(skillsSelect.selectedOptions).map(opt => opt.value);
        }
        
        // Programación
        const datetimeInput = document.querySelector('input[type="datetime-local"]');
        if (datetimeInput && datetimeInput.value) data.schedule.appointment = datetimeInput.value;
        
        return data;
    };

    window.resetForm = function() {
        document.querySelectorAll('input[type="checkbox"]').forEach(cb => cb.checked = cb.defaultChecked);
        document.querySelectorAll('input[type="radio"]').forEach(radio => radio.checked = radio.defaultChecked);
        document.querySelectorAll('select').forEach(select => select.selectedIndex = 0);
        document.querySelectorAll('input[type="range"]').forEach(slider => {
            slider.value = slider.defaultValue;
            const valueDisplay = slider.parentElement.querySelector('.dars-slider-value');
            if (valueDisplay) valueDisplay.textContent = slider.value;
        });
        document.querySelectorAll('input[type="date"], input[type="datetime-local"]').forEach(date => date.value = '');
    };
""")
app.add_script(utils_script)

# Contenedor principal
main_container = Container(style={
    'max-width': '800px',
    'margin': '0 auto',
    'padding': '40px 20px',
    'font-family': 'Arial, sans-serif'
})

# Título y descripción
title = Text("Formulario Completo con Dars", style={'font-size': '32px', 'font-weight': 'bold', 'color': '#2c3e50', 'text-align': 'center', 'margin-bottom': '20px', 'display': 'block'})
description = Text("Ejemplo completo de todos los componentes básicos de formulario disponibles en Dars Framework", style={'font-size': '16px', 'color': '#7f8c8d', 'text-align': 'center', 'margin-bottom': '40px', 'display': 'block'})

# Sección 1: Información Personal
personal_section = Container(style={'margin-bottom': '30px', 'padding': '20px', 'border': '1px solid #e0e0e0', 'border-radius': '8px', 'background-color': '#f9f9f9'})
personal_section.add_child(Text("Información Personal", style={'font-size': '20px', 'font-weight': 'bold', 'color': '#34495e', 'margin-bottom': '15px', 'display': 'block'}))

birth_date = DatePicker(placeholder="Fecha de nacimiento", format="DD/MM/YYYY", required=True, style={'margin-bottom': '15px', 'width': '200px'})
country_select = Select(
    options=[SelectOption("es", "España"), SelectOption("mx", "México"), SelectOption("ar", "Argentina"), SelectOption("co", "Colombia"), SelectOption("pe", "Perú"), SelectOption("cl", "Chile"), SelectOption("ve", "Venezuela"), SelectOption("ec", "Ecuador")],
    placeholder="Selecciona tu país", required=True, style={'margin-bottom': '15px', 'width': '200px'}
)

personal_section.add_child(Text("Fecha de nacimiento:", style={'display': 'block', 'margin-bottom': '5px', 'font-weight': 'bold'}))
personal_section.add_child(birth_date)
personal_section.add_child(Text("País:", style={'display': 'block', 'margin-bottom': '5px', 'margin-top': '15px', 'font-weight': 'bold'}))
personal_section.add_child(country_select)

# Sección 2: Preferencias
preferences_section = Container(style={'margin-bottom': '30px', 'padding': '20px', 'border': '1px solid #e0e0e0', 'border-radius': '8px', 'background-color': '#f9f9f9'})
preferences_section.add_child(Text("Preferencias", style={'font-size': '20px', 'font-weight': 'bold', 'color': '#34495e', 'margin-bottom': '15px', 'display': 'block'}))

preferences_section.add_child(Text("Notificaciones:", style={'display': 'block', 'margin-bottom': '8px', 'font-weight': 'bold'}))
preferences_section.add_child(Checkbox(label="Recibir notificaciones por email", name="notifications", value="email", checked=True))
preferences_section.add_child(Checkbox(label="Recibir notificaciones por SMS", name="notifications", value="sms"))
preferences_section.add_child(Checkbox(label="Notificaciones push en el navegador", name="notifications", value="push", checked=True))

preferences_section.add_child(Text("Tema de la aplicación:", style={'display': 'block', 'margin-bottom': '8px', 'margin-top': '20px', 'font-weight': 'bold'}))
preferences_section.add_child(RadioButton(label="Tema claro", name="theme", value="light", checked=True))
preferences_section.add_child(RadioButton(label="Tema oscuro", name="theme", value="dark"))
preferences_section.add_child(RadioButton(label="Automático (según sistema)", name="theme", value="auto"))

# Sección 3: Configuración Avanzada
advanced_section = Container(style={'margin-bottom': '30px', 'padding': '20px', 'border': '1px solid #e0e0e0', 'border-radius': '8px', 'background-color': '#f9f9f9'})
advanced_section.add_child(Text("Configuración Avanzada", style={'font-size': '20px', 'font-weight': 'bold', 'color': '#34495e', 'margin-bottom': '15px', 'display': 'block'}))

volume_slider = Slider(
    min_value=0, max_value=100, value=75, step=5, label="Volumen de notificaciones:", show_value=True, style={'margin-bottom': '20px'},
    on_input=dScript("const d = this.parentElement.querySelector('.dars-slider-value'); if(d) d.textContent = this.value;")
)
quality_slider = Slider(
    min_value=1, max_value=5, value=3, step=1, label="Calidad de imagen (1=baja, 5=alta):", show_value=True, style={'margin-bottom': '20px'},
    on_input=dScript("const d = this.parentElement.querySelector('.dars-slider-value'); if(d) d.textContent = this.value;")
)

skills_select = Select(
    options=["Python", "JavaScript", "HTML/CSS", "React", "Vue.js", "Django", "Flask", "Node.js", "MongoDB", "PostgreSQL", "Docker", "Kubernetes", "AWS", "Git", "Linux"],
    placeholder="Selecciona tus habilidades (múltiple)", multiple=True, size=6, style={'width': '100%', 'max-width': '400px'}
)

advanced_section.add_child(volume_slider)
advanced_section.add_child(quality_slider)
advanced_section.add_child(Text("Habilidades técnicas:", style={'display': 'block', 'margin-bottom': '8px', 'font-weight': 'bold'}))
advanced_section.add_child(skills_select)

# Sección 4: Programación
schedule_section = Container(style={'margin-bottom': '30px', 'padding': '20px', 'border': '1px solid #e0e0e0', 'border-radius': '8px', 'background-color': '#f9f9f9'})
schedule_section.add_child(Text("Programación", style={'font-size': '20px', 'font-weight': 'bold', 'color': '#34495e', 'margin-bottom': '15px', 'display': 'block'}))

schedule_section.add_child(Text("Próxima cita:", style={'display': 'block', 'margin-bottom': '8px', 'font-weight': 'bold'}))
schedule_section.add_child(DatePicker(placeholder="Selecciona fecha y hora", format="YYYY-MM-DD", show_time=True, style={'margin-bottom': '15px', 'width': '250px'}))
schedule_section.add_child(Text("Fecha del evento (solo 2024):", style={'display': 'block', 'margin-bottom': '8px', 'font-weight': 'bold'}))
schedule_section.add_child(DatePicker(placeholder="Fecha del evento", format="DD-MM-YYYY", min_date="01-01-2024", max_date="31-12-2024", style={'width': '200px'}))

# Botones de acción
actions_container = Container(style={'text-align': 'center', 'margin-top': '40px'})

save_button = Button(
    text="Guardar Configuración",
    on_mouse_enter=this().state(style={'transform': 'translateY(-1px)', 'box-shadow': '0 4px 8px rgba(0,0,0,0.2)'}),
    on_mouse_leave=this().state(style={'transform': 'none', 'box-shadow': 'none'}),
    on_click=dScript("""
        const formData = window.collectFormData();
        console.log('Datos del formulario:', formData);
        alert('Configuración guardada exitosamente!\\n\\nRevisa la consola del navegador.');
    """),
    style={'background-color': '#27ae60', 'color': 'white', 'padding': '12px 24px', 'font-size': '16px', 'font-weight': 'bold', 'border': 'none', 'border-radius': '6px', 'cursor': 'pointer', 'margin-right': '15px', 'transition': 'all 0.2s'}
)

reset_button = Button(
    text="Restablecer",
    on_mouse_enter=this().state(style={'transform': 'translateY(-1px)', 'box-shadow': '0 4px 8px rgba(0,0,0,0.2)'}),
    on_mouse_leave=this().state(style={'transform': 'none', 'box-shadow': 'none'}),
    on_click=dScript("""
        if (confirm('¿Estás seguro de que quieres restablecer todos los valores?')) {
            window.resetForm();
            alert('Formulario restablecido.');
        }
    """),
    style={'background-color': '#e74c3c', 'color': 'white', 'padding': '12px 24px', 'font-size': '16px', 'font-weight': 'bold', 'border': 'none', 'border-radius': '6px', 'cursor': 'pointer', 'transition': 'all 0.2s'}
)

actions_container.add_child(save_button)
actions_container.add_child(reset_button)

# Ensamblar
main_container.add_child(title)
main_container.add_child(description)
main_container.add_child(personal_section)
main_container.add_child(preferences_section)
main_container.add_child(advanced_section)
main_container.add_child(schedule_section)
main_container.add_child(actions_container)

app.set_root(main_container)

# Estilos globales
app.add_global_style('body', {'background-color': '#ecf0f1', 'line-height': '1.6'})
app.add_global_style('.dars-checkbox-wrapper, .dars-radio-wrapper', {'margin': '8px 0'})

if __name__ == '__main__':
    app.rTimeCompile()