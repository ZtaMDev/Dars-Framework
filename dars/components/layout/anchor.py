from typing import Optional

class AnchorPoint:
    """
    Represents an anchor or alignment point for a child in a layout (top, left, right, bottom, center, etc).
    """
    def __init__(self, x: Optional[str] = None, y: Optional[str] = None, name: Optional[str] = None):
        self.x = x  # e.g. 'left', 'center', 'right', percent or px
        self.y = y  # e.g. 'top', 'center', 'bottom', percent or px
        self.name = name  # Optional semantic name for anchor

    def __repr__(self):
        return f"AnchorPoint(x={self.x}, y={self.y}, name={self.name})"
