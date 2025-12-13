from dars.core.component import Component
from typing import Optional

class ProgressBar(Component):
    """
    Visual progress bar.
    value: current value (0-100)
    max_value: maximum value (default 100)
    """

    def __init__(self, value: int, max_value: int = 100, **props):
        super().__init__(**props)
        self.value = value
        self.max_value = max_value

    def render(self) -> str:
        percent = min(max(self.value / self.max_value * 100, 0), 100)
        return f'<div class="dars-progressbar"><div class="dars-progressbar-bar" style="width: {percent}%;"></div></div>'
