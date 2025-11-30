from dars.core.component import Component
import uuid

class DataTable(Component):
    """
    Professional HTML table component with pandas DataFrame support.
    
    Features:
    - Pandas DataFrame or list of dicts
    - Auto-infers columns from data
    - Custom column definitions with formatters
    - Built-in themes (light, dark, custom)
    - Striped rows, hover effects, borders
    - Responsive design
    
    Args:
        data: pandas.DataFrame, list[dict], or list[list]
        columns (list): Column definitions [{'key': str, 'label': str, 'align': str, 'formatter': callable}]
        index (bool): Show DataFrame index column
        header (bool): Show header row
        striped (bool): Alternating row colors
        hover (bool): Hover effects
        bordered (bool): Cell borders
        compact (bool): Compact spacing
        theme (str|dict): 'light', 'dark', or custom theme dict
        formatters (dict): Column formatters {column_key: callable}
        id (str): Component ID
        style (dict): CSS styles
        **props: Additional properties
    
    Examples:
        # Pandas DataFrame
        import pandas as pd
        df = pd.DataFrame({'name': ['Alice', 'Bob'], 'age': [30, 25]})
        table = DataTable(df, theme='dark')
        
        # List of dicts with formatters
        data = [{'price': 99.99, 'qty': 5}]
        table = DataTable(
            data,
            columns=[
                {'key': 'price', 'label': 'Price', 'formatter': lambda x: f'${x:.2f}'},
                {'key': 'qty', 'label': 'Quantity', 'align': 'center'}
            ]
        )
    """
    
    THEMES = {
        'light': {
            'header_bg': '#f8f9fa',
            'header_color': '#212529',
            'header_border': '#dee2e6',
            'row_even_bg': '#ffffff',
            'row_odd_bg': '#f9f9f9',
            'row_hover_bg': '#e9ecef',
            'border_color': '#dee2e6',
            'text_color': '#212529'
        },
        'dark': {
            'header_bg': '#343a40',
            'header_color': '#f8f9fa',
            'header_border': '#495057',
            'row_even_bg': '#212529',
            'row_odd_bg': '#2c3034',
            'row_hover_bg': '#3d4449',
            'border_color': '#495057',
            'text_color': '#f8f9fa'
        }
    }
    
    def __init__(self, data, columns=None, index=False, header=True, striped=True, 
                 hover=True, bordered=True, compact=False, theme='light', 
                 formatters=None, id=None, style=None, **props):
        super().__init__(id=id, style=style, **props)
        
        if not self.id:
            self.id = f"table-{str(uuid.uuid4())[:8]}"
        
        # Render immediately to avoid deepcopy issues with DataFrames and formatters
        try:
            self._html = self._render_table(data, columns, index, header, striped, hover, 
                                           bordered, compact, theme, formatters or {})
        except Exception as e:
            import traceback
            traceback.print_exc()
            self._html = f'<div id="{self.id}" class="dars-table-error" style="border: 1px solid red; padding: 10px; color: red;">Error rendering table: {str(e)}</div>'
    
    def __deepcopy__(self, memo):
        """Return self to avoid deepcopy issues."""
        return self
    
    def _normalize_data(self, data, index, columns):
        """Convert data to list of dicts format."""        
        # Check if pandas DataFrame
        try:
            import pandas as pd
            if isinstance(data, pd.DataFrame):
                if index:
                    df_with_index = data.reset_index()
                    return df_with_index.to_dict('records'), list(df_with_index.columns)
                else:
                    return data.to_dict('records'), list(data.columns)
        except ImportError:
            pass
        
        # List of dicts
        if isinstance(data, list) and len(data) > 0:
            if isinstance(data[0], dict):
                keys = list(data[0].keys())
                return data, keys
            elif isinstance(data[0], (list, tuple)):
                if columns:
                    keys = [col.get('key', f'col_{i}') for i, col in enumerate(columns)]
                else:
                    keys = [f'col_{i}' for i in range(len(data[0]))]
                return [dict(zip(keys, row)) for row in data], keys
        
        return [], []
    
    def _get_columns(self, inferred_keys, columns):
        """Get column definitions."""
        if columns:
            normalized = []
            for col in columns:
                if isinstance(col, str):
                    normalized.append({
                        'key': col,
                        'label': col.replace('_', ' ').title(),
                        'align': 'left',
                        'formatter': None
                    })
                elif isinstance(col, dict):
                    normalized.append({
                        'key': col.get('key', ''),
                        'label': col.get('label', col.get('key', '').replace('_', ' ').title()),
                        'align': col.get('align', 'left'),
                        'formatter': col.get('formatter', None)
                    })
            return normalized
        else:
            return [{
                'key': key,
                'label': str(key).replace('_', ' ').title(),
                'align': 'left',
                'formatter': None
            } for key in inferred_keys]
    
    def _get_theme(self, theme):
        """Get theme colors."""
        if isinstance(theme, dict):
            return {**self.THEMES['light'], **theme}
        return self.THEMES.get(theme, self.THEMES['light'])
    
    def _format_value(self, value, column, formatters):
        """Format cell value."""
        if column['formatter']:
            try:
                return str(column['formatter'](value))
            except:
                pass
        
        if column['key'] in formatters:
            try:
                return str(formatters[column['key']](value))
            except:
                pass
        
        if value is None:
            return ''
        return str(value)
    
    def _render_table(self, data, columns, index, header, striped, hover, bordered, compact, theme, formatters):
        """Render table immediately."""
        rows, inferred_keys = self._normalize_data(data, index, columns)
        cols = self._get_columns(inferred_keys, columns)
        theme_colors = self._get_theme(theme)
        
        if not rows:
            return f'<div id="{self.id}" class="{self.class_name or ""}">No data available</div>'
        
        padding = '8px 12px' if compact else '12px 16px'
        border_style = f'1px solid {theme_colors["border_color"]}' if bordered else 'none'
        
        # Header
        header_html = ''
        if header:
            header_cells = []
            for col in cols:
                header_cells.append(f'<th style="padding: {padding}; text-align: {col["align"]}; background-color: {theme_colors["header_bg"]}; color: {theme_colors["header_color"]}; border-bottom: 2px solid {theme_colors["header_border"]}; border-right: {border_style}; font-weight: 600; white-space: nowrap;">{col["label"]}</th>')
            header_html = f'<thead><tr>{"".join(header_cells)}</tr></thead>'
        
        # Body
        body_rows = []
        for i, row in enumerate(rows):
            bg_color = theme_colors['row_even_bg'] if i % 2 == 0 else theme_colors['row_odd_bg']
            if not striped:
                bg_color = theme_colors['row_even_bg']
            
            hover_style = f"onmouseover=\"this.style.backgroundColor='{theme_colors['row_hover_bg']}'\" onmouseout=\"this.style.backgroundColor='{bg_color}'\"" if hover else ""
            
            cells = []
            for col in cols:
                value = row.get(col['key'], '')
                formatted_value = self._format_value(value, col, formatters)
                cells.append(f'<td style="padding: {padding}; text-align: {col["align"]}; border-bottom: {border_style}; border-right: {border_style}; color: {theme_colors["text_color"]};">{formatted_value}</td>')
            
            body_rows.append(f'<tr style="background-color: {bg_color}; transition: background-color 0.2s;" {hover_style}>{"".join(cells)}</tr>')
        
        body_html = f'<tbody>{"".join(body_rows)}</tbody>'
        
        # Container style
        container_style = "overflow-x: auto; width: 100%;"
        if self.style:
            if isinstance(self.style, dict):
                container_style += "; " + "; ".join([f"{k}: {v}" for k, v in self.style.items()])
            else:
                container_style += "; " + str(self.style)
        
        # Table style
        table_style = f'width: 100%; border-collapse: collapse; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif; font-size: 14px; border: {border_style};'
        
        return f'<div id="{self.id}-container" class="{self.class_name or ""}" style="{container_style}"><table id="{self.id}" style="{table_style}">{header_html}{body_html}</table></div>'
    
    def render(self, exporter) -> str:
        """Return pre-rendered HTML."""
        return self._html
