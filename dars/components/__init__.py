# Dars Framework - Core Source File
#
# This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0.
# If a copy of the MPL was not distributed with this file, You can obtain one at
# https://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2025 ZtaDev
"""## Introduction to Components

Components are the fundamental UI elements in Dars. Each component encapsulates its appearance, behavior, and state.
In modern Dars, you should heavily rely on **Utility Classes** (Tailwind-like classes) using the `class_name` property instead of the old `style` dictionary, and use **DAP Functions** (`show()`, `hide()`, `log()`, `alert()`, `updateVRef()`) instead of writing raw inline JavaScript for events.

For custom components, refer to [Custom Components](#custom-components).

---

## Base Component Class

All UI elements inherit from the `Component` base class, which provides standard attributes and DOM manipulation methods.

### Global Properties

- **id**: Unique identifier for the component.
- **class_name**: String containing CSS utility classes (e.g., `"flex flex-col bg-slate-100 p-4 rounded-lg"`).
- **style**: Optional dictionary or string for direct inline styles (prefer `class_name`).
- **children**: List of child components.
- **Events**: Handlers like `on_click`, `on_change`, `on_mouse_enter`, etc. Accept DAP utility functions or state setters.
"""