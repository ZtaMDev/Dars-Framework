from dars.core.component import Component
from typing import List, Dict, Any, Optional

class Table(Component):
    """
    Component to display tabular data with columns, data, pagination, sorting, and filtering.
    columns: List of dictionaries with keys 'title', 'field', 'sortable', 'width', etc.
    data: List of dictionaries (each one is a row)
    page_size: Number of rows per page (optional)
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
