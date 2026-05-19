# Dars Framework - Core Source File
#
# This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0.
# If a copy of the MPL was not distributed with this file, You can obtain one at
# https://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2025 ZtaDev
"""
# Dars - Script & Action System

Dars Framework features a dual-layer logic system: **Structured DAP Actions** for high-security, high-performance interactions, and **JavaScript Scripts** for complex client-side logic.

---

## The Dars Action Protocol (DAP)

DAP is the modern backbone of Dars interactivity. It replaces raw JavaScript strings with structured data objects that describe actions.

### Why DAP?
1. **Security**: DAP actions are executed by a built-in registry, avoiding dangerous `eval()` or `new Function()` calls. This enables a strict Content Security Policy (CSP).
2. **Predictability**: Actions are defined as Python dictionaries, making them easier to debug and validate.
3. **Full-Stack Consistency**: The same action structure works in SPA, SSR, and Desktop targets.
"""