from typing import Optional, List, Dict, Any
from .component import Component
from .events import EventManager

class App:
    """Clase principal que representa una aplicación Dars"""
    
    def __init__(
        self, 
        title: str = "Dars App",
        description: str = "",
        author: str = "",
        keywords: List[str] = None,
        language: str = "es",
        favicon: str = "",
        icon: str = "",
        apple_touch_icon: str = "",
        manifest: str = "",
        theme_color: str = "#000000",
        background_color: str = "#ffffff",
        **config
    ):
        # Propiedades básicas de la aplicación
        self.title = title
        self.description = description
        self.author = author
        self.keywords = keywords or []
        self.language = language
        
        # Iconos y favicon
        self.favicon = favicon
        self.icon = icon  # Para PWA y meta tags
        self.apple_touch_icon = apple_touch_icon
        self.manifest = manifest  # Para PWA manifest.json
        
        # Colores para PWA y tema
        self.theme_color = theme_color
        self.background_color = background_color
        
        # Propiedades Open Graph (para redes sociales)
        self.og_title = config.get('og_title', title)
        self.og_description = config.get('og_description', description)
        self.og_image = config.get('og_image', '')
        self.og_url = config.get('og_url', '')
        self.og_type = config.get('og_type', 'website')
        self.og_site_name = config.get('og_site_name', '')
        
        # Twitter Cards
        self.twitter_card = config.get('twitter_card', 'summary')
        self.twitter_site = config.get('twitter_site', '')
        self.twitter_creator = config.get('twitter_creator', '')
        
        # SEO y robots
        self.robots = config.get('robots', 'index, follow')
        self.canonical_url = config.get('canonical_url', '')
        
        # PWA configuración
        self.pwa_enabled = config.get('pwa_enabled', False)
        self.pwa_name = config.get('pwa_name', title)
        self.pwa_short_name = config.get('pwa_short_name', title[:12])
        self.pwa_display = config.get('pwa_display', 'standalone')
        self.pwa_orientation = config.get('pwa_orientation', 'portrait')
        
        # Propiedades del framework
        self.root: Optional[Component] = None
        self.scripts: List['Script'] = []
        self.global_styles: Dict[str, Any] = {}
        self.event_manager = EventManager()
        self.config = config
        
        # Configuración por defecto
        self.config.setdefault('viewport', {
            'width': 'device-width',
            'initial_scale': 1.0,
            'user_scalable': 'yes'
        })
        self.config.setdefault('theme', 'light')
        self.config.setdefault('responsive', True)
        self.config.setdefault('charset', 'UTF-8')
        
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
        
    def set_favicon(self, favicon_path: str):
        """Establece el favicon de la aplicación"""
        self.favicon = favicon_path
    
    def set_icon(self, icon_path: str):
        """Establece el icono principal de la aplicación"""
        self.icon = icon_path
    
    def set_apple_touch_icon(self, icon_path: str):
        """Establece el icono para dispositivos Apple"""
        self.apple_touch_icon = icon_path
    
    def set_manifest(self, manifest_path: str):
        """Establece el archivo manifest para PWA"""
        self.manifest = manifest_path
    
    def add_keyword(self, keyword: str):
        """Añade una palabra clave para SEO"""
        if keyword not in self.keywords:
            self.keywords.append(keyword)
    
    def add_keywords(self, keywords: List[str]):
        """Añade múltiples palabras clave para SEO"""
        for keyword in keywords:
            self.add_keyword(keyword)
    
    def set_open_graph(self, **og_data):
        """Configura propiedades Open Graph para redes sociales"""
        if 'title' in og_data:
            self.og_title = og_data['title']
        if 'description' in og_data:
            self.og_description = og_data['description']
        if 'image' in og_data:
            self.og_image = og_data['image']
        if 'url' in og_data:
            self.og_url = og_data['url']
        if 'type' in og_data:
            self.og_type = og_data['type']
        if 'site_name' in og_data:
            self.og_site_name = og_data['site_name']
    
    def set_twitter_card(self, card_type: str = 'summary', site: str = '', creator: str = ''):
        """Configura Twitter Card meta tags"""
        self.twitter_card = card_type
        if site:
            self.twitter_site = site
        if creator:
            self.twitter_creator = creator
    
    def enable_pwa(self, name: str = None, short_name: str = None, display: str = 'standalone'):
        """Habilita configuración PWA (Progressive Web App)"""
        self.pwa_enabled = True
        if name:
            self.pwa_name = name
        if short_name:
            self.pwa_short_name = short_name
        self.pwa_display = display
    
    def set_theme_colors(self, theme_color: str, background_color: str = None):
        """Establece colores del tema para PWA y navegadores"""
        self.theme_color = theme_color
        if background_color:
            self.background_color = background_color
    
    def get_meta_tags(self) -> Dict[str, str]:
        """Obtiene todos los meta tags configurados como diccionario"""
        meta_tags = {}
        
        # Meta tags básicos
        if self.description:
            meta_tags['description'] = self.description
        if self.author:
            meta_tags['author'] = self.author
        if self.keywords:
            meta_tags['keywords'] = ', '.join(self.keywords)
        if self.robots:
            meta_tags['robots'] = self.robots
        
        # Viewport
        viewport_parts = []
        for key, value in self.config['viewport'].items():
            if key == 'initial_scale':
                viewport_parts.append(f'initial-scale={value}')
            elif key == 'user_scalable':
                viewport_parts.append(f'user-scalable={value}')
            else:
                viewport_parts.append(f'{key.replace("_", "-")}={value}')
        meta_tags['viewport'] = ', '.join(viewport_parts)
        
        # PWA y tema
        meta_tags['theme-color'] = self.theme_color
        if self.pwa_enabled:
            meta_tags['mobile-web-app-capable'] = 'yes'
            meta_tags['apple-mobile-web-app-capable'] = 'yes'
            meta_tags['apple-mobile-web-app-status-bar-style'] = 'default'
            meta_tags['apple-mobile-web-app-title'] = self.pwa_short_name
        
        return meta_tags
    
    def get_open_graph_tags(self) -> Dict[str, str]:
        """Obtiene todos los tags Open Graph configurados"""
        og_tags = {}
        
        if self.og_title:
            og_tags['og:title'] = self.og_title
        if self.og_description:
            og_tags['og:description'] = self.og_description
        if self.og_image:
            og_tags['og:image'] = self.og_image
        if self.og_url:
            og_tags['og:url'] = self.og_url
        if self.og_type:
            og_tags['og:type'] = self.og_type
        if self.og_site_name:
            og_tags['og:site_name'] = self.og_site_name
        
        return og_tags
    
    def get_twitter_tags(self) -> Dict[str, str]:
        """Obtiene todos los tags de Twitter Card configurados"""
        twitter_tags = {}
        
        if self.twitter_card:
            twitter_tags['twitter:card'] = self.twitter_card
        if self.twitter_site:
            twitter_tags['twitter:site'] = self.twitter_site
        if self.twitter_creator:
            twitter_tags['twitter:creator'] = self.twitter_creator
        
        return twitter_tags
        
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

