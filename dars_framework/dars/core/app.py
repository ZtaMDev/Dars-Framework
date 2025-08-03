from typing import Optional, List, Dict, Any
from .component import Component
from .events import EventManager

class App:
    """Clase principal que representa una aplicación Dars"""
    
    def __init__(self, title: str = "Dars App", **config):
        self.title = title
        self.root: Optional[Component] = None
        self.scripts: List['Script'] = []
        self.global_styles: Dict[str, Any] = {}
        self.event_manager = EventManager()
        self.config = config
        
        # Configuración por defecto
        self.config.setdefault('viewport', {
            'width': 'device-width',
            'initial_scale': 1.0
        })
        self.config.setdefault('theme', 'light')
        self.config.setdefault('responsive', True)
        
    def set_root(self, component: Component):
        """Establece el componente raíz de la aplicación"""
        self.root = component
        
    def add_script(self, script: 'Script'):
        """Agrega un script a la aplicación"""
        self.scripts.append(script)
        
    def add_global_style(self, selector: str, styles: Dict[str, Any]):
        """Agrega estilos globales a la aplicación"""
        self.global_styles[selector] = styles
        
    def set_theme(self, theme: str):
        """Establece el tema de la aplicación"""
        self.config['theme'] = theme
        
    def export(self, exporter: 'Exporter', output_path: str) -> bool:
        """Exporta la aplicación usando el exportador especificado"""
        if not self.root:
            raise ValueError("No se ha establecido un componente raíz")
        
        return exporter.export(self, output_path)
        
    def validate(self) -> List[str]:
        """Valida la aplicación y retorna una lista de errores"""
        errors = []
        
        if not self.root:
            errors.append("No se ha establecido un componente raíz")
            
        if not self.title:
            errors.append("El título de la aplicación no puede estar vacío")
            
        # Validar componentes recursivamente
        if self.root:
            errors.extend(self._validate_component(self.root))
            
        return errors
        
    def _validate_component(self, component: Component, path: str = "root") -> List[str]:
        """Valida un componente y sus hijos recursivamente"""
        errors = []
        
        # Validar que el componente tenga un método render
        if not hasattr(component, 'render'):
            errors.append(f"El componente en {path} no tiene método render")
            
        # Validar hijos
        for i, child in enumerate(component.children):
            child_path = f"{path}.children[{i}]"
            errors.extend(self._validate_component(child, child_path))
            
        return errors
        
    def get_component_tree(self) -> Dict[str, Any]:
        """Retorna la estructura del árbol de componentes"""
        if not self.root:
            return {}
            
        return self._component_to_dict(self.root)
        
    def _component_to_dict(self, component: Component) -> Dict[str, Any]:
        """Convierte un componente a diccionario para inspección"""
        return {
            'type': component.__class__.__name__,
            'id': component.id,
            'class_name': component.class_name,
            'props': component.props,
            'style': component.style,
            'children': [self._component_to_dict(child) for child in component.children]
        }
        
    def find_component_by_id(self, component_id: str) -> Optional[Component]:
        """Busca un componente por su ID"""
        if not self.root:
            return None
            
        return self._find_component_recursive(self.root, component_id)
        
    def _find_component_recursive(self, component: Component, target_id: str) -> Optional[Component]:
        """Busca un componente recursivamente por ID"""
        if component.id == target_id:
            return component
            
        for child in component.children:
            result = self._find_component_recursive(child, target_id)
            if result:
                return result
                
        return None
        
    def get_stats(self) -> Dict[str, Any]:
        """Retorna estadísticas de la aplicación"""
        if not self.root:
            return {
                'total_components': 0,
                'max_depth': 0,
                'scripts_count': len(self.scripts),
                'global_styles_count': len(self.global_styles)
            }
            
        stats = {
            'total_components': self._count_components(self.root),
            'max_depth': self._calculate_max_depth(self.root),
            'scripts_count': len(self.scripts),
            'global_styles_count': len(self.global_styles)
        }
        
        return stats
        
    def _count_components(self, component: Component) -> int:
        """Cuenta el número total de componentes"""
        count = 1
        for child in component.children:
            count += self._count_components(child)
        return count
        
    def _calculate_max_depth(self, component: Component, current_depth: int = 0) -> int:
        """Calcula la profundidad máxima del árbol de componentes"""
        if not component.children:
            return current_depth
            
        max_child_depth = 0
        for child in component.children:
            child_depth = self._calculate_max_depth(child, current_depth + 1)
            max_child_depth = max(max_child_depth, child_depth)
            
        return max_child_depth

