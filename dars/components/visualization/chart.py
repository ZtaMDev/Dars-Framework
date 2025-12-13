from dars.core.component import Component
import json
import uuid

class Chart(Component):
    """
    Chart component supporting Plotly (interactive).
    
    **Plotly**: Embeds Plotly.js and renders interactive charts from figure JSON
    
    Args:
        figure: plotly.graph_objects.Figure
        width (int/str): Width in pixels or CSS value
        height (int/str): Height in pixels or CSS value
        config (dict): Plotly configuration options
        id (str): Component ID
        style (dict): CSS styles
        **props: Additional properties
    
    Examples:
        # Plotly
        import plotly.graph_objects as go
        fig = go.Figure(data=[go.Bar(x=['A', 'B'], y=[10, 20])])
        chart = Chart(fig, width=800, height=400)
    """
    
    def __init__(self, figure, width=None, height=None, config=None, id=None, style=None, **props):
        super().__init__(id=id, style=style, **props)
        
        if not self.id:
            self.id = f"chart-{str(uuid.uuid4())[:8]}"
        
        # Render immediately to avoid deepcopy issues
        try:
            self._html = self._render_chart(figure, width, height, config or {})
        except Exception as e:
            print(f"Warning: Failed to render chart: {e}")
            self._html = f'<div id="{self.id}" class="dars-chart-error" style="border: 1px solid red; padding: 10px; color: red;">Error rendering chart: {str(e)}</div>'
    
    def __deepcopy__(self, memo):
        """Return self to avoid deepcopy issues."""
        return self
    
    def _is_plotly(self, figure):
        """Check if figure is a Plotly figure."""
        return hasattr(figure, 'to_json') or hasattr(figure, 'to_plotly_json')
    
    def _render_chart(self, figure, width, height, config):
        """Render chart immediately."""
        if self._is_plotly(figure):
            return self._render_plotly(figure, width, height, config)
        else:
            return f'<div id="{self.id}">Error: Unsupported figure type. Only Plotly figures are supported.</div>'
    
    def _render_plotly(self, figure, width, height, config):
        """Render Plotly figure as interactive chart."""
        # Get figure JSON
        if hasattr(figure, 'to_json'):
            fig_json = figure.to_json()
        elif hasattr(figure, 'to_plotly_json'):
            fig_json_dict = figure.to_plotly_json()
            fig_json = json.dumps(fig_json_dict)
        else:
            fig_json = json.dumps(figure)
        
        fig_dict = json.loads(fig_json)
        data = json.dumps(fig_dict.get('data', []))
        layout = json.dumps(fig_dict.get('layout', {}))
        
        default_config = {'responsive': True, 'displayModeBar': True, 'displaylogo': False}
        final_config = {**default_config, **config}
        config_json = json.dumps(final_config)
        
        container_style = []
        if width:
            w = f"{width}px" if isinstance(width, int) else width
            container_style.append(f"width: {w}")
        else:
            container_style.append("width: 100%")
            
        if height:
            h = f"{height}px" if isinstance(height, int) else height
            container_style.append(f"height: {h}")
        else:
            container_style.append("height: 400px")
        
        style_str = "; ".join(container_style)
        
        return f'''
<div id="{self.id}" style="{style_str}" class="{self.class_name or ''}"></div>
<script>
(function() {{
    var plotDiv = document.getElementById('{self.id}');
    var data = {data};
    var layout = {layout};
    var config = {config_json};
    
    function initPlot() {{
        Plotly.newPlot(plotDiv, data, layout, config);
    }}
    
    if (typeof Plotly === 'undefined') {{
        if (!window.dars_plotly_loading) {{
            window.dars_plotly_loading = true;
            var script = document.createElement('script');
            script.src = 'https://cdn.plot.ly/plotly-2.27.0.min.js';
            script.onload = function() {{
                window.dars_plotly_loaded = true;
                window.dispatchEvent(new Event('plotly_loaded'));
            }};
            document.head.appendChild(script);
        }}
        window.addEventListener('plotly_loaded', initPlot);
    }} else {{
        initPlot();
    }}
}})();
</script>
'''
    
    def render(self, exporter) -> str:
        """Return pre-rendered HTML."""
        return self._html
