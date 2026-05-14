# Dars Framework - Core Source File
#
# This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0.
# If a copy of the MPL was not distributed with this file, You can obtain one at
# https://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2025 ZtaDev
from dars.components.layout.grid import LayoutBase
from typing import List, Optional

class FlexLayout(LayoutBase):
    """
    Layout component based on CSS Flexbox for organizing child components in rows or columns.
    
    Props:
    - **direction** (str): Flex direction (`"row"`, `"row-reverse"`, `"column"`, `"column-reverse"`).
    - **wrap** (str): Flex wrap behavior (`"nowrap"`, `"wrap"`, `"wrap-reverse"`).
    - **justify** (str): Main axis alignment (`"flex-start"`, `"center"`, `"flex-end"`, `"space-between"`, `"space-around"`).
    - **align** (str): Cross axis alignment (`"stretch"`, `"center"`, `"flex-start"`, `"flex-end"`, `"baseline"`).
    - **gap** (str): Space between child components (e.g., `"16px"`, `"1rem"`).
    - **id** (str): Unique identifier for the component.
    - **class_name** (str): String containing regular CSS class names.
    - **style** (dict): Optional dictionary for CSS utility classes (prefer `style`).
    - **children** (list): List of child components.
    - **Events**: Handlers like `on_click`, `on_mouse_enter`, etc.
    
    Example:
    ```python
    FlexLayout(
        Button("Cancel"),
        Button("Save", class_name="bg-indigo-600 text-white"),
        direction="row",
        justify="flex-end",
        gap="12px",
        class_name="w-full p-4 border-t border-slate-100"
    )
    ```
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
