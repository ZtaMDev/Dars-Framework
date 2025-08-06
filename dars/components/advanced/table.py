from dars.core.component import Component
from typing import List, Dict, Any, Optional

class Table(Component):
    """
    Componente para mostrar datos tabulares con columnas, datos, paginación, orden y filtrado.
    columns: Lista de diccionarios con claves 'title', 'field', 'sortable', 'width', etc.
    data: Lista de diccionarios (cada uno es una fila).
    page_size: Número de filas por página (opcional).
    """
    def __init__(self, columns: List[Dict[str, Any]], data: List[Dict[str, Any]], page_size: Optional[int]=None, **props):
        super().__init__(**props)
        self.columns = columns
        self.data = data
        self.page_size = page_size

    def render(self) -> str:
        # Renderiza la tabla en HTML (solo vista simple, sin JS avanzado todavía)
        thead = '<thead><tr>' + ''.join(f'<th>{col["title"]}</th>' for col in self.columns) + '</tr></thead>'
        rows = self.data[:self.page_size] if self.page_size else self.data
        tbody = '<tbody>' + ''.join(
            '<tr>' + ''.join(f'<td>{row.get(col["field"], "")}</td>' for col in self.columns) + '</tr>'
            for row in rows) + '</tbody>'
        return f'<table class="dars-table">{thead}{tbody}</table>'
