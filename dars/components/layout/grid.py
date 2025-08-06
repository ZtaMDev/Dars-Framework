from dars.core.component import Component
from typing import List, Optional, Dict, Any

class LayoutBase(Component):
    """
    Base class for all layout components. Allows adding children and anchor/positioning info.
    """
    def __init__(self, children: Optional[List[Component]] = None, anchors: Optional[Dict[str, Any]] = None, **kwargs):
        super().__init__(**kwargs)
        self.children = children or []
        self.anchors = anchors or {}

    def add_child(self, child: Component):
        self.children.append(child)

    def render(self, exporter=None):
        # Layouts se renderizan solo por el exporter, pero se requiere para evitar TypeError
        return ""

class GridLayout(LayoutBase):
    """
    Responsive grid layout component. Supports rows/columns and anchor points for children.
    """
    def __init__(self, rows: int = 1, cols: int = 1, children: Optional[List[Component]] = None, anchors: Optional[Dict[str, Any]] = None, gap: str = "16px", **kwargs):
        super().__init__(children=children, anchors=anchors, **kwargs)
        self.rows = rows
        self.cols = cols
        self.gap = gap

    def add_child(self, child: Component, row: int = 0, col: int = 0, row_span: int = 1, col_span: int = 1, anchor: Optional[str] = None):
        # Store child with layout info
        if not hasattr(self, '_child_layout'):
            self._child_layout = []
        self._child_layout.append({
            'child': child,
            'row': row,
            'col': col,
            'row_span': row_span,
            'col_span': col_span,
            'anchor': anchor
        })
        self.children.append(child)

    def get_child_layout(self):
        return getattr(self, '_child_layout', [])
