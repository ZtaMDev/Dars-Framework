from dars.core.component import Component
from typing import List, Dict, Any, Optional

class Table(Component):
    """
    Component for displaying structured data in a tabular format with support for sorting and pagination.
    
    Props:
    - **columns** (list): List of dictionaries defining columns (e.g., `[{"title": "Name", "field": "name", "sortable": True}]`).
    - **data** (list): List of row dictionaries where keys match the `field` defined in `columns`.
    - **page_size** (int): Number of rows to display per page (optional).
    - **id** (str): Unique identifier for the component.
    - **class_name** (str): String containing regular CSS class names.
    - **style** (dict): Optional dictionary for CSS utility classes (prefer `style`).
    - **children** (list): List of child components.
    - **Events**: Handlers for sorting, filtering, and row clicks.
    
    Example:
    ```python
    Table(
        columns=[
            {"title": "User", "field": "user"},
            {"title": "Status", "field": "status"}
        ],
        data=[
            {"user": "John Doe", "status": "Active"},
            {"user": "Jane Smith", "status": "Pending"}
        ],
        page_size=10,
        class_name="min-w-full divide-y divide-slate-200 shadow-sm rounded-lg overflow-hidden"
    )
    ```
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
