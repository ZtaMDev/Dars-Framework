#!/usr/bin/env python3
"""
Dars Translations - Translation system for Dars CLI
"""

# Diccionario de traducciones
translations = {
    'en': {
        # CLI descriptions
        'cli_description': "Dars Exporter - Export Dars applications to Web",
        'cli_subtitle': "Multiplatform UI Framework in Python",
        'main_description': "Export Dars applications to Web",
        
        # Commands
        'available_commands': "Available commands",
        'export_help': "Export application",
        'info_help': "Show application information",
        'formats_help': "Show supported formats",
        'preview_help': "Preview information",
        'preview_cmd_help': "Preview exported application",
        'init_help': "Create a Dars project",
        
        # Export command
        'file_help': "Python file with Dars application",
        'format_help': "Export format",
        'output_help': "Output directory",
        'preview_arg_help': "Show preview information (HTML only)",
        
        # Init command
        'name_help': "Project name",
        'template_help': "Initial template: category/name (e.g. basic/hello_world)",
        
        # Preview command
        'path_help': "Directory with exported application",
        'preview_description': "Dars Preview - Preview system",
        'directory_help': "Directory with the exported application",
        'no_open_help': "Do not automatically open the browser",
        'port_help': "Port for the server (HTML only)",
        'lang_help': "Language for the preview (en or es)",
        
        # Preview server messages
        'server_start_error': "Error starting server: {error}",
        'preview_server_started': "Preview server started",
        'directory': "Directory",
        'port': "Port",
        'press_ctrl_c': "Press Ctrl+C to stop the server",
        'opening_in_browser': "Opening in browser: {url}",
        'browser_open_error': "Could not open browser automatically: {error}",
        'open_manually': "Open manually: {url}",
        'stopping_server': "Stopping server...",
        'server_stopped': "Server stopped",
        
        # Preview HTML app
        'html_preview': "HTML Preview",
        'index_html_missing': "Error: index.html not found in {directory}",
        
        # Preview React app
        'react_preview': "React App Preview",
        'react_package_json_missing': "Error: package.json not found in {directory}",
        'react_navigate': "1. Navigate to the directory: cd {directory}",
        'react_install': "2. Install dependencies: npm install",
        'react_start': "3. Start the development server: npm start",
        'react_auto_open': "The app will open automatically in your browser",
        
        # Preview React Native app
        'react_native_preview': "React Native App Preview",
        'react_native_package_json_missing': "Error: package.json not found in {directory}",
        'react_native_navigate': "1. Navigate to the directory: cd {directory}",
        'react_native_install': "2. Install dependencies: npm install",
        'react_native_android': "3. For Android: npm run android",
        'react_native_ios': "4. For iOS: npm run ios",
        'react_native_start': "5. Start Metro bundler: npm start",
        'react_native_note': "Note: Make sure you have the React Native development environment set up",
        
        # Preview PySide6 app
        'pyside6_preview': "PySide6 App Preview",
        'pyside6_main_missing': "Error: main.py not found in {directory}",
        'pyside6_navigate': "1. Navigate to the directory: cd {directory}",
        'pyside6_install': "2. Install dependencies: pip install -r requirements.txt (if available)",
        'pyside6_run': "3. Run the application: python main.py",
        'pyside6_note': "Note: Make sure you have PySide6 installed (pip install pyside6)",
        
        # Preview C# app
        'csharp_preview': "C# App Preview",
        'csharp_project_missing': "Error: No .csproj file found in {directory}",
        'csharp_navigate': "1. Navigate to the directory: cd {directory}",
        'csharp_restore': "2. Restore dependencies: dotnet restore",
        'csharp_build': "3. Build the application: dotnet build",
        'csharp_run': "4. Run the application: dotnet run",
        'csharp_note': "Note: Make sure you have .NET SDK installed",
        
        # Preview Kotlin app
        'kotlin_preview': "Kotlin Multiplatform App Preview",
        'kotlin_gradle_missing': "Error: build.gradle.kts not found in {directory}",
        'kotlin_navigate': "1. Navigate to the directory: cd {directory}",
        'kotlin_desktop': "2. Run for desktop: ./gradlew run",
        'kotlin_android': "3. Install for Android: ./gradlew installDebug",
        'kotlin_build_all': "4. Build for all platforms: ./gradlew build",
        'kotlin_note': "Note: Make sure you have JDK and Android SDK installed",
        
        # Preview app
        'directory_not_exists': "Error: The directory {directory} does not exist",
        'format_not_detected': "Error: Could not detect the application format in {directory}",
        'detected_format': "Detected format",
        'format_not_supported': "Error: Format '{format}' not supported for preview",
        
        # Help sections
        'usage': "USAGE",
        'positional_arguments': "POSITIONAL ARGUMENTS",
        'options': "OPTIONS",
        'commands': "AVAILABLE COMMANDS",
        'examples': "EXAMPLES",
        'help_arg_message': "show this help message and exit",
        
        # Examples
        'usage_examples': "Usage examples",
        'examples_text': """
        dars export app.py --format html --output ./dist
        dars info app.py
        dars preview ./dist
        dars init my_new_project
        dars init my_new_project -t demo/complete_app
        """,
        
        # Messages
        'app_found': "Application found at: {}",
        'open_in_browser': "Open in browser: file://{}",
        'preview_question': "Do you want to see the preview? [green]y[/green] / [red]n[/red] [y/n] ",
        'index_not_found': "index.html not found in {}",
        'dir_created': "Directory '{}' created",
        'template_copied': "Template '{template}' copied as main.py",
        'main_created': "main.py file created (default Hello World)",
        'project_initialized': "🎉 Dars project successfully initialized",
        'export_command': "To export the template use",
        'preview_command': "To view the project in a browser use",
        
        # Formats
        'supported_formats': "Supported export formats",
        'format_name': "Format",
        'format_description': "Description",
        'html_description': "Standard HTML/CSS/JavaScript",
        
        # App info
        'app_info': "Application Information: {}",
        'property': "Property",
        'value': "Value",
        'title': "Title",
        'total_components': "Total components",
        'max_depth': "Maximum depth",
        'scripts': "Scripts",
        'global_styles': "Global styles",
        'theme': "Theme",
        'responsive': "Responsive",
        'component_structure': "Component Structure"
    },
    'es': {
        # CLI descriptions
        'cli_description': "Dars Exporter - Exporta aplicaciones Dars a Web",
        'cli_subtitle': "Framework de UI multiplataforma en Python",
        'main_description': "Dars Exporter - Exporta aplicaciones Dars a Web",
        
        # Commands
        'available_commands': "Comandos disponibles",
        'export_help': "Exportar aplicación",
        'info_help': "Mostrar información de la aplicación",
        'formats_help': "Mostrar formatos soportados",
        'preview_help': "Información de preview",
        'preview_cmd_help': "Previsualizar aplicación exportada",
        'init_help': "Crea un proyecto Dars",
        
        # Export command
        'file_help': "Archivo Python con la aplicación Dars",
        'format_help': "Formato de exportación",
        'output_help': "Directorio de salida",
        'preview_arg_help': "Mostrar información de preview (solo para HTML)",
        
        # Init command
        'name_help': "Nombre del proyecto",
        'template_help': "Plantilla inicial: categoría/nombre (por ejemplo basic/hello_world)",
        
        # Preview command
        'path_help': "Directorio con la aplicación exportada",
        'preview_description': "Dars Preview - Sistema de preview",
        'directory_help': "Directorio con la aplicación exportada",
        'no_open_help': "No abrir automáticamente el navegador",
        'port_help': "Puerto para el servidor (solo HTML)",
        'lang_help': "Idioma para la preview (en o es)",
        
        # Preview server messages
        'server_start_error': "Error al iniciar el servidor: {error}",
        'preview_server_started': "Servidor de preview iniciado",
        'directory': "Directorio",
        'port': "Puerto",
        'press_ctrl_c': "Presiona Ctrl+C para detener el servidor",
        'opening_in_browser': "Abriendo en navegador: {url}",
        'browser_open_error': "No se pudo abrir el navegador automáticamente: {error}",
        'open_manually': "Abrir manualmente: {url}",
        'stopping_server': "Deteniendo servidor...",
        'server_stopped': "Servidor detenido",
        
        # Preview HTML app
        'html_preview': "Preview HTML",
        'index_html_missing': "Error: No se encontró index.html en {directory}",
        
        # Preview React app
        'react_preview': "Preview de App React",
        'react_package_json_missing': "Error: No se encontró package.json en {directory}",
        'react_navigate': "1. Navega al directorio: cd {directory}",
        'react_install': "2. Instala dependencias: npm install",
        'react_start': "3. Inicia el servidor de desarrollo: npm start",
        'react_auto_open': "La aplicación se abrirá automáticamente en tu navegador",
        
        # Preview React Native app
        'react_native_preview': "Preview de App React Native",
        'react_native_package_json_missing': "Error: No se encontró package.json en {directory}",
        'react_native_navigate': "1. Navega al directorio: cd {directory}",
        'react_native_install': "2. Instala dependencias: npm install",
        'react_native_android': "3. Para Android: npm run android",
        'react_native_ios': "4. Para iOS: npm run ios",
        'react_native_start': "5. Inicia Metro bundler: npm start",
        'react_native_note': "Nota: Asegúrate de tener configurado el entorno de desarrollo de React Native",
        
        # Preview PySide6 app
        'pyside6_preview': "Preview de App PySide6",
        'pyside6_main_missing': "Error: No se encontró main.py en {directory}",
        'pyside6_navigate': "1. Navega al directorio: cd {directory}",
        'pyside6_install': "2. Instala dependencias: pip install -r requirements.txt (si está disponible)",
        'pyside6_run': "3. Ejecuta la aplicación: python main.py",
        'pyside6_note': "Nota: Asegúrate de tener PySide6 instalado (pip install pyside6)",
        
        # Preview C# app
        'csharp_preview': "Preview de App C#",
        'csharp_project_missing': "Error: No se encontró archivo .csproj en {directory}",
        'csharp_navigate': "1. Navega al directorio: cd {directory}",
        'csharp_restore': "2. Restaura dependencias: dotnet restore",
        'csharp_build': "3. Compila la aplicación: dotnet build",
        'csharp_run': "4. Ejecuta la aplicación: dotnet run",
        'csharp_note': "Nota: Asegúrate de tener instalado .NET SDK",
        
        # Preview Kotlin app
        'kotlin_preview': "Preview de App Kotlin Multiplatform",
        'kotlin_gradle_missing': "Error: No se encontró build.gradle.kts en {directory}",
        'kotlin_navigate': "1. Navega al directorio: cd {directory}",
        'kotlin_desktop': "2. Ejecutar para desktop: ./gradlew run",
        'kotlin_android': "3. Instalar para Android: ./gradlew installDebug",
        'kotlin_build_all': "4. Compilar para todas las plataformas: ./gradlew build",
        'kotlin_note': "Nota: Asegúrate de tener instalado JDK y Android SDK",
        
        # Preview app
        'directory_not_exists': "Error: El directorio {directory} no existe",
        'format_not_detected': "Error: No se pudo detectar el formato de la aplicación en {directory}",
        'detected_format': "Formato detectado",
        'format_not_supported': "Error: Formato '{format}' no soportado para preview",
        
        # Help sections
        'usage': "USO",
        'positional_arguments': "ARGUMENTOS POSICIONALES",
        'options': "OPCIONES",
        'commands': "COMANDOS DISPONIBLES",
        'examples': "EJEMPLOS",
        'help_arg_message': "muestra este mensaje de ayuda y sal",
        
        # Examples
        'usage_examples': "Ejemplos de uso",
        'examples_text': """
        dars export app.py --format html --output ./dist
        dars info app.py
        dars preview ./dist
        dars init mi_nuevo_proyecto
        dars init mi_nuevo_proyecto -t demo/complete_app
        """,
        
        # Messages
        'app_found': "Aplicación encontrada en: {}",
        'open_in_browser': "Abrir en navegador: file://{}",
        'preview_question': "¿Quieres ver la preview? [green]y[/green] / [red]n[/red] [y/n] ",
        'index_not_found': "No se encontró index.html en {}",
        'dir_created': "Directorio '{}' creado",
        'template_copied': "Template '{template}' copiado como main.py",
        'main_created': "Archivo main.py creado (Hello World por defecto)",
        'project_initialized': "🎉 Proyecto Dars inicializado exitosamente",
        'export_command': "Para exportar el template usa",
        'preview_command': "Para ver el proyecto en un navegador usa",
        
        # Formats
        'supported_formats': "Formatos de exportación soportados",
        'format_name': "Formato",
        'format_description': "Descripción",
        'html_description': "HTML/CSS/JavaScript estándar",
        
        # App info
        'app_info': "Información de la Aplicación: {}",
        'property': "Propiedad",
        'value': "Valor",
        'title': "Título",
        'total_components': "Componentes totales",
        'max_depth': "Profundidad máxima",
        'scripts': "Scripts",
        'global_styles': "Estilos globales",
        'theme': "Tema",
        'responsive': "Responsive",
        'component_structure': "Estructura de Componentes"
    }
}

import os
import configparser

class Translator:
    """Class for handling translations"""
    
    def __init__(self, language='en'):
        self.config_file = self._get_config_path()
        self.language = self._load_language_preference() or language
        
    def _get_config_path(self):
        """Returns the path to the configuration file"""
        # Use user's home directory for configuration
        home_dir = os.path.expanduser("~")
        dars_config_dir = os.path.join(home_dir, ".dars")
        
        # Create the directory if it doesn't exist
        if not os.path.exists(dars_config_dir):
            os.makedirs(dars_config_dir)
            
        return os.path.join(dars_config_dir, "config.ini")
    
    def _load_language_preference(self):
        """Loads the language preference from the configuration file"""
        config = configparser.ConfigParser()
        
        if os.path.exists(self.config_file):
            config.read(self.config_file)
            if 'preferences' in config and 'language' in config['preferences']:
                lang = config['preferences']['language']
                if lang in translations:
                    return lang
        return None
    
    def _save_language_preference(self):
        """Saves the current language preference to the configuration file"""
        config = configparser.ConfigParser()
        
        # Load existing config if it exists
        if os.path.exists(self.config_file):
            config.read(self.config_file)
        
        # Ensure the preferences section exists
        if 'preferences' not in config:
            config['preferences'] = {}
        
        # Update the language preference
        config['preferences']['language'] = self.language
        
        # Save the configuration
        with open(self.config_file, 'w') as configfile:
            config.write(configfile)
        
    def set_language(self, language, save=True):
        """Sets the current language and optionally saves the preference"""
        if language in translations:
            self.language = language
            if save:
                self._save_language_preference()
        else:
            print(f"Language {language} not supported, using default (en)")
            self.language = 'en'
            if save:
                self._save_language_preference()
    
    def get(self, key, **kwargs):
        """Gets a translation by its key"""
        if self.language in translations and key in translations[self.language]:
            text = translations[self.language][key]
            # Apply formatting if there are arguments
            if kwargs:
                return text.format(**kwargs)
            return text
        # Fallback to English if the key is not found in current language
        if 'en' in translations and key in translations['en']:
            text = translations['en'][key]
            if kwargs:
                return text.format(**kwargs)
            return text
        # If not found in any language, return the key
        return key

# Instancia global del traductor
translator = Translator()