from abc import ABC, abstractmethod
from typing import Dict, Any
import os

class Exporter(ABC):
    """Clase base para todos los exportadores"""
    
    def __init__(self):
        self.templates_path = os.path.join(os.path.dirname(__file__), "..", "templates")
        
    @abstractmethod
    def export(self, app: 'App', output_path: str) -> bool:
        """Exporta la aplicación al formato específico"""
        pass
        
    @abstractmethod
    def render_component(self, component: 'Component') -> str:
        """Renderiza un componente individual"""
        pass
        
    def load_template(self, template_name: str) -> str:
        """Carga una plantilla desde el directorio de templates"""
        template_path = os.path.join(self.templates_path, self.get_platform(), template_name)
        try:
            with open(template_path, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            raise FileNotFoundError(f"Plantilla no encontrada: {template_path}")
            
    @abstractmethod
    def get_platform(self) -> str:
        """Retorna el nombre de la plataforma (html, react, etc.)"""
        pass
        
    def create_output_directory(self, output_path: str):
        """Crea el directorio de salida si no existe"""
        os.makedirs(output_path, exist_ok=True)
        
    def write_file(self, file_path: str, content: str):
        """Escribe contenido a un archivo"""
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
            
    def copy_file(self, source_path: str, dest_path: str):
        """Copia un archivo de origen a destino"""
        import shutil
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)
        shutil.copy2(source_path, dest_path)
        
    def render_styles(self, styles: Dict[str, Any]) -> str:
        """Convierte un diccionario de estilos a CSS"""
        if not styles:
            return ""
            
        css_rules = []
        for property_name, value in styles.items():
            # Convertir snake_case a kebab-case
            css_property = property_name.replace('_', '-')
            css_rules.append(f"{css_property}: {value}")
            
        return "; ".join(css_rules)
        
    def generate_unique_id(self, component: 'Component') -> str:
        """Genera un ID único para un componente si no tiene uno"""
        if component.id:
            return component.id
        return f"component_{id(component)}"

