# Dars Framework - Core Source File
#
# This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0.
# If a copy of the MPL was not distributed with this file, You can obtain one at
# https://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2025 ZtaDev
"""
The core module of Dars, it has the app class, events, routing and state definitions.

# App Class and PWA Features in Dars Framework

## Overview

The `App` class is the core of any Dars Framework application. It represents the complete application and manages all configuration, components, pages, and functionalities, including Progressive Web App (PWA) support.

## Basic Structure

```python
class App:
    def __init__(
        self, 
        title: str = "Dars App",
        description: str = "",
        author: str = "",
        keywords: List[str] = None,
        language: str = "en",
        favicon: str = "",
        icon: str = "",
        apple_touch_icon: str = "",
        manifest: str = "",
        theme_color: str = "#000000",
        background_color: str = "#ffffff",
        service_worker_path: str = "",
        service_worker_enabled: bool = False,
        **config
    ):
```

# State Management in Dars

Dars Framework features **powerful state management systems**, designed for different use cases:

# State V2 - Dynamic State Management

Modern, Pythonic state management for reactive UIs.

## Quick Start

```python
from dars.all import *

# Create a component
display = Text("0", id="counter")

# Create state
counter = State(display, text=0)

# Use reactive properties
increment_btn = Button("Increment", on_click=counter.text.increment(by=1))
decrement_btn = Button("Decrement", on_click=counter.text.decrement(by=1))
reset_btn = Button("Reset", on_click=counter.reset())
```

etc... see docs.
"""
