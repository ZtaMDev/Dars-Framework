from dars.all import *
from dars.core.component import Component
from dars.exporters.web.html_css_js import *
import re
import os

class DocsSidebar(Component):
    def __init__(self, markdown_files: list, **props):
        """
        markdown_files: Lista de rutas a archivos markdown en el orden deseado.
        """
        super().__init__(**props)
        self.markdown_files = markdown_files
        
    def extract_headings_from_all_markdown(self):
        """Extrae los encabezados de todos los archivos markdown en la lista proporcionada"""
        headings = []
        
        try:
            for file_path in self.markdown_files:
                if not os.path.exists(file_path):
                    print(f"File not found: {file_path}")
                    continue
                    
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                
                # Procesar el contenido para excluir bloques de código
                processed_content = self.remove_code_blocks(content)
                
                # Patrón regex para encontrar encabezados markdown (#, ##, ###, ####, #####, ######)
                pattern = r'^(#{1,6})\s+(.+)$'
                filename = os.path.basename(file_path)
                
                for line in processed_content.split('\n'):
                    match = re.match(pattern, line)
                    if match:
                        level = len(match.group(1))  # Nivel del encabezado (1, 2, 3, 4, 5, 6)
                        text = match.group(2).strip()
                        
                        # Generar slug para el enlace
                        slug = self.generate_slug(text)
                        
                        headings.append({
                            'level': level,
                            'text': text,
                            'slug': slug,
                            'file': filename
                        })
            
            return headings
        except Exception as e:
            print(f"Error reading markdown files: {e}")
            return []
    
    def remove_code_blocks(self, content):
        """Elimina bloques de código del contenido para no procesar encabezados dentro de ellos"""
        # Patrón para bloques de código con ```
        code_block_pattern = r'```[^`]*?```'
        # Patrón para bloques de código con indentación (menos común)
        indented_code_pattern = r'(?<=\n)(?:(?: {4,}|\t).*(?:\n|$))+'
        
        # Reemplazar bloques de código con vacío
        content = re.sub(code_block_pattern, '', content, flags=re.DOTALL)
        content = re.sub(indented_code_pattern, '', content)
        
        return content
    
    def generate_slug(self, text):
        """Genera un slug a partir del texto del encabezado"""
        # Convertir a minúsculas y reemplazar espacios/caracteres especiales
        slug = text.lower()
        slug = re.sub(r'[^a-z0-9\s-]', '', slug)  # Remover caracteres especiales
        slug = re.sub(r'\s+', '-', slug)          # Reemplazar espacios con guiones
        slug = re.sub(r'-+', '-', slug)           # Remover guiones múltiples
        return slug
    
    def render(self, exporter: 'Exporter') -> str:
        headings = self.extract_headings_from_all_markdown()
        
        # Generar los enlaces del sidebar
        links_html = ""
        current_file = None
        
        for heading in headings:
            # Agregar separador si cambia el archivo
            if heading['file'] != current_file:
                if current_file is not None:
                    links_html += '<div class="sidebar-divider"></div>'
                current_file = heading['file']
                # Mostrar nombre del archivo como categoría
                file_display_name = heading['file'].replace('.md', '').replace('_', ' ').title()
                links_html += f'''
                <div class="sidebar-category">
                    {file_display_name}
                </div>
                '''
            
            indent = (heading['level'] - 1) * 20  # Indentación basada en el nivel
            links_html += f'''
            <a href="#{heading['slug']}" 
               class="sidebar-link sidebar-level-{heading['level']}"
               style="margin-left: {indent}px">
                {heading['text']}
            </a>
            '''
        
        return f'''
        <div class="docs-sidebar" id="docs-sidebar">
            <div class="sidebar-header">
                <h3>Documentation</h3>
            </div>
            <div class="sidebar-links">
                {links_html}
            </div>
        </div>
        {self.add_styles()}
        {self.add_scripts()}
        '''
    
    def add_styles(self):
        """Añade los estilos CSS para el sidebar"""
        return '''
        <style>
        .docs-sidebar {
            position: fixed;
            left: 0;
            top: 64px;
            width: 280px;
            height: calc(100vh - 64px);
            background: rgba(15, 25, 22, 0.95);
            backdrop-filter: blur(12px);
            border-right: 1px solid rgba(100, 255, 200, 0.15);
            padding: 20px 0;
            overflow-y: auto;
            z-index: 100;
            transition: all 0.3s ease;
        }
        
        .sidebar-header {
            padding: 0 25px 20px 25px;
            border-bottom: 1px solid rgba(100, 255, 200, 0.1);
            margin-bottom: 15px;
        }
        
        .sidebar-header h3 {
            color: #a2ffe2;
            font-size: 18px;
            font-weight: 700;
            margin: 0;
            text-shadow: 0 0 10px rgba(162, 255, 226, 0.3);
        }
        
        .sidebar-links {
            display: flex;
            flex-direction: column;
            gap: 8px;
            padding: 0 15px;
        }
        
        .sidebar-category {
            color: #92ffe5;
            font-size: 14px;
            font-weight: 700;
            margin: 15px 0 8px 0;
            padding: 8px 15px;
            background: rgba(162, 255, 226, 0.1);
            border-radius: 6px;
            border-left: 3px solid #a2ffe2;
        }
        
        .sidebar-divider {
            height: 1px;
            background: rgba(100, 255, 200, 0.1);
            margin: 15px 0;
        }
        
        .sidebar-link {
            color: #a0cfc0;
            text-decoration: none;
            padding: 10px 15px;
            border-radius: 8px;
            font-size: 14px;
            font-weight: 500;
            transition: all 0.3s ease;
            border: 1px solid transparent;
            cursor: pointer;
            display: block;
        }
        
        .sidebar-link:hover {
            color: #92ffe5;
            background: rgba(162, 255, 226, 0.1);
            border-color: rgba(162, 255, 226, 0.2);
            transform: translateX(5px);
            text-shadow: 0 0 8px rgba(162, 255, 226, 0.4);
        }
        
        .sidebar-link.sidebar-level-1 {
            font-weight: 700;
            color: #a2ffe2;
            font-size: 15px;
        }
        
        .sidebar-link.sidebar-level-2 {
            font-weight: 600;
            color: #9ad8c5;
        }
        
        .sidebar-link.sidebar-level-3 {
            font-weight: 500;
            color: #a0cfc0;
            font-size: 13px;
        }
        
        .sidebar-link.sidebar-level-4 {
            font-weight: 500;
            color: #a0cfc0;
            font-size: 12px;
        }
        
        .sidebar-link.sidebar-level-5 {
            font-weight: 500;
            color: #a0cfc0;
            font-size: 12px;
        }
        
        .sidebar-link.sidebar-level-6 {
            font-weight: 500;
            color: #a0cfc0;
            font-size: 12px;
        }
        
        .sidebar-link.active {
            background: rgba(162, 255, 226, 0.15) !important;
            border-color: rgba(162, 255, 226, 0.4) !important;
            color: #92ffe5 !important;
            text-shadow: 0 0 10px rgba(162, 255, 226, 0.6) !important;
        }
        
        /* Scrollbar personalizado */
        .docs-sidebar::-webkit-scrollbar {
            width: 4px;
        }
        
        .docs-sidebar::-webkit-scrollbar-track {
            background: rgba(10, 20, 15, 0.3);
        }
        
        .docs-sidebar::-webkit-scrollbar-thumb {
            background: rgba(162, 255, 226, 0.3);
            border-radius: 2px;
        }
        
        .docs-sidebar::-webkit-scrollbar-thumb:hover {
            background: rgba(162, 255, 226, 0.5);
        }
        
        /* Responsive */
        @media (max-width: 1024px) {
            .docs-sidebar {
                width: 250px;
            }
        }
        
        @media (max-width: 768px) {
            .docs-sidebar {
                transform: translateX(-100%);
                width: 280px;
                box-shadow: 4px 0 20px rgba(0,0,0,0.3);
            }
            
            .docs-sidebar.mobile-open {
                transform: translateX(0);
            }
        }
        </style>
        '''
    
    def add_scripts(self):
        """Añade scripts JavaScript para funcionalidad del sidebar"""
        return '''
        <script>
        document.addEventListener('DOMContentLoaded', function() {
            const sidebar = document.getElementById('docs-sidebar');
            const sidebarLinks = document.querySelectorAll('.sidebar-link');
            
            // Smooth scroll para los enlaces del sidebar
            sidebarLinks.forEach(link => {
                link.addEventListener('click', function(e) {
                    e.preventDefault();
                    
                    const targetId = this.getAttribute('href').substring(1);
                    const targetElement = document.getElementById(targetId);
                    
                    if (targetElement) {
                        // Scroll suave al elemento - el CSS se encarga del offset con scroll-margin-top
                        targetElement.scrollIntoView({
                            behavior: 'smooth',
                            block: 'start'
                        });
                        
                        // Cerrar sidebar en móviles después de hacer clic
                        if (window.innerWidth <= 768) {
                            sidebar.classList.remove('mobile-open');
                        }
                    }
                });
            });
            
            // Toggle para móviles
            const toggleBtn = document.createElement('button');
            toggleBtn.innerHTML = '☰';
            toggleBtn.className = 'sidebar-toggle';
            toggleBtn.style.display = window.innerWidth <= 768 ? 'flex' : 'none';
            
            toggleBtn.addEventListener('click', function() {
                sidebar.classList.toggle('mobile-open');
            });
            
            document.body.appendChild(toggleBtn);
            
            // Ocultar sidebar al hacer clic fuera en móviles
            document.addEventListener('click', function(e) {
                if (window.innerWidth <= 768) {
                    const toggleBtn = document.querySelector('.sidebar-toggle');
                    
                    if (!sidebar.contains(e.target) && !toggleBtn.contains(e.target) && sidebar.classList.contains('mobile-open')) {
                        sidebar.classList.remove('mobile-open');
                    }
                }
            });
            
            // Actualizar visibilidad del toggle en resize
            window.addEventListener('resize', function() {
                const toggleBtn = document.querySelector('.sidebar-toggle');
                toggleBtn.style.display = window.innerWidth <= 768 ? 'flex' : 'none';
                
                if (window.innerWidth > 768) {
                    sidebar.classList.remove('mobile-open');
                }
            });
            
            // Resaltar enlace activo mientras se desplaza
            function highlightActiveLink() {
                const sections = document.querySelectorAll('h1, h2, h3, h4, h5, h6');
                const sidebarLinks = document.querySelectorAll('.sidebar-link');
                
                let currentSection = '';
                
                sections.forEach(section => {
                    const sectionTop = section.offsetTop - 100;
                    if (window.scrollY >= sectionTop) {
                        currentSection = section.id;
                    }
                });
                
                sidebarLinks.forEach(link => {
                    link.classList.remove('active');
                    if (link.getAttribute('href') === '#' + currentSection) {
                        link.classList.add('active');
                    }
                });
            }
            
            window.addEventListener('scroll', highlightActiveLink);
        });
        </script>
        '''

def create_sidebar():
    markdown_files = [
        "./documentation/markdown/index.md",
        "./documentation/markdown/install.md",
        "./documentation/markdown/getting_started.md",
        "./documentation/markdown/config.md",
        "./documentation/markdown/app.md",
        "./documentation/markdown/routing.md",
        "./documentation/markdown/backend_api.md",
        "./documentation/markdown/state_management.md",
        "./documentation/markdown/components.md",
        "./documentation/markdown/animations.md",
        "./documentation/markdown/custom_components.md",
        "./documentation/markdown/hooks.md",
        "./documentation/markdown/events.md",
        "./documentation/markdown/exporters.md",
        "./documentation/markdown/scripts.md",
        "./documentation/markdown/cli.md",
    ]
    return DocsSidebar(
        markdown_files=markdown_files,
        id="documentation-sidebar"
    )
    