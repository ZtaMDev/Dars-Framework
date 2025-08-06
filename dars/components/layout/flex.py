from dars.components.layout.grid import LayoutBase
from typing import List, Optional

class FlexLayout(LayoutBase):
    """
    Responsive flexbox layout component. Allows direction, wrap, justify, align, and anchor points for children.
    """
    def __init__(self, 
                 children: Optional[List[object]] = None,
                 direction: str = "row",
                 wrap: str = "wrap",
                 justify: str = "flex-start",
                 align: str = "stretch",
                 gap: str = "16px",
                 anchors: Optional[dict] = None,
                 **kwargs):
        super().__init__(children=children, anchors=anchors, **kwargs)
        self.direction = direction
        self.wrap = wrap
        self.justify = justify
        self.align = align
        self.gap = gap

    def add_child(self, child, anchor: Optional[str] = None):
        self.children.append(child)
        # Could store anchor info per child if needed
