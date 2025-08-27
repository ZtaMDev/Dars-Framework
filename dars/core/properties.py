from typing import Union, Optional, Dict, Any, Callable
from dataclasses import dataclass

@dataclass
class StyleProps:
    """Style properties for UI components"""
    # Dimensiones
    width: Optional[Union[str, int]] = None
    height: Optional[Union[str, int]] = None
    min_width: Optional[Union[str, int]] = None
    min_height: Optional[Union[str, int]] = None
    max_width: Optional[Union[str, int]] = None
    max_height: Optional[Union[str, int]] = None
    
    # Espaciado
    margin: Optional[Union[str, int]] = None
    margin_top: Optional[Union[str, int]] = None
    margin_right: Optional[Union[str, int]] = None
    margin_bottom: Optional[Union[str, int]] = None
    margin_left: Optional[Union[str, int]] = None
    padding: Optional[Union[str, int]] = None
    padding_top: Optional[Union[str, int]] = None
    padding_right: Optional[Union[str, int]] = None
    padding_bottom: Optional[Union[str, int]] = None
    padding_left: Optional[Union[str, int]] = None
    
    # Colores
    background_color: Optional[str] = None
    color: Optional[str] = None
    border_color: Optional[str] = None
    
    # Tipografía
    font_size: Optional[Union[str, int]] = None
    font_family: Optional[str] = None
    font_weight: Optional[Union[str, int]] = None
    font_style: Optional[str] = None
    text_align: Optional[str] = None
    text_decoration: Optional[str] = None
    line_height: Optional[Union[str, int]] = None
    
    # Bordes
    border: Optional[str] = None
    border_width: Optional[Union[str, int]] = None
    border_style: Optional[str] = None
    border_radius: Optional[Union[str, int]] = None
    
    # Layout
    display: Optional[str] = None
    position: Optional[str] = None
    top: Optional[Union[str, int]] = None
    right: Optional[Union[str, int]] = None
    bottom: Optional[Union[str, int]] = None
    left: Optional[Union[str, int]] = None
    z_index: Optional[int] = None
    
    # Flexbox
    flex_direction: Optional[str] = None
    flex_wrap: Optional[str] = None
    justify_content: Optional[str] = None
    align_items: Optional[str] = None
    align_content: Optional[str] = None
    flex: Optional[Union[str, int]] = None
    flex_grow: Optional[int] = None
    flex_shrink: Optional[int] = None
    flex_basis: Optional[Union[str, int]] = None
    
    # Grid
    grid_template_columns: Optional[str] = None
    grid_template_rows: Optional[str] = None
    grid_gap: Optional[Union[str, int]] = None
    grid_column: Optional[str] = None
    grid_row: Optional[str] = None
    
    # Efectos
    opacity: Optional[float] = None
    box_shadow: Optional[str] = None
    transform: Optional[str] = None
    transition: Optional[str] = None
    
    # Overflow
    overflow: Optional[str] = None
    overflow_x: Optional[str] = None
    overflow_y: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convierte las propiedades a un diccionario, excluyendo valores None"""
        result = {}
        for key, value in self.__dict__.items():
            if value is not None:
                # Convertir snake_case a kebab-case para CSS
                css_key = key.replace('_', '-')
                result[css_key] = value
        return result

@dataclass
class EventProps:
    """Propiedades de eventos para componentes UI"""
    on_click: Optional[Callable] = None
    on_double_click: Optional[Callable] = None
    on_mouse_enter: Optional[Callable] = None
    on_mouse_leave: Optional[Callable] = None
    on_mouse_down: Optional[Callable] = None
    on_mouse_up: Optional[Callable] = None
    on_key_down: Optional[Callable] = None
    on_key_up: Optional[Callable] = None
    on_focus: Optional[Callable] = None
    on_blur: Optional[Callable] = None
    on_change: Optional[Callable] = None
    on_input: Optional[Callable] = None
    on_submit: Optional[Callable] = None
    on_load: Optional[Callable] = None
    on_error: Optional[Callable] = None

def normalize_style_value(value: Union[str, int]) -> str:
    """Normaliza un valor de estilo a string CSS"""
    if isinstance(value, int):
        return f"{value}px"
    return str(value)

def merge_styles(*styles: Dict[str, Any]) -> Dict[str, Any]:
    """Combina múltiples diccionarios de estilos"""
    result = {}
    for style in styles:
        if style:
            result.update(style)
    return result

