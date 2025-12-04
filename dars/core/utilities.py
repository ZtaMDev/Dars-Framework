# Dars Framework - Core Source File
#
# This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0.
# If a copy of the MPL was not distributed with this file, You can obtain one at
# https://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2025 ZtaDev

from typing import Dict, Any, List, Optional
import re

def _fmt_rem(v: str) -> str:
    try:
        # Check if it's a number
        if v.replace('.', '', 1).isdigit():
            num = float(v) * 0.25
            # Format to remove trailing .0 if integer
            return f"{num:g}rem"
        return v
    except:
        return v

# Mapping of prefixes/keywords to CSS properties
UTILITY_PROPERTY_MAP = {
    # Layout
    "block": "display: block",
    "inline-block": "display: inline-block",
    "inline": "display: inline",
    "flex": "display: flex",
    "inline-flex": "display: inline-flex",
    "grid": "display: grid",
    "inline-grid": "display: inline-grid",
    "hidden": "display: none",
    
    # Flexbox
    "flex-row": "flex-direction: row",
    "flex-col": "flex-direction: column",
    "flex-wrap": "flex-wrap: wrap",
    "flex-nowrap": "flex-wrap: nowrap",
    "items-start": "align-items: flex-start",
    "items-end": "align-items: flex-end",
    "items-center": "align-items: center",
    "items-baseline": "align-items: baseline",
    "items-stretch": "align-items: stretch",
    "justify-start": "justify-content: flex-start",
    "justify-end": "justify-content: flex-end",
    "justify-center": "justify-content: center",
    "justify-between": "justify-content: space-between",
    "justify-around": "justify-content: space-around",
    "justify-evenly": "justify-content: space-evenly",
    "grow": "flex-grow: 1",
    "grow-0": "flex-grow: 0",
    "shrink": "flex-shrink: 1",
    "shrink-0": "flex-shrink: 0",

    # Positioning
    "static": "position: static",
    "fixed": "position: fixed",
    "absolute": "position: absolute",
    "relative": "position: relative",
    "sticky": "position: sticky",
    
    # Typography
    "italic": "font-style: italic",
    "not-italic": "font-style: normal",
    "underline": "text-decoration: underline",
    "line-through": "text-decoration: line-through",
    "no-underline": "text-decoration: none",
    "uppercase": "text-transform: uppercase",
    "lowercase": "text-transform: lowercase",
    "capitalize": "text-transform: capitalize",
    "text-left": "text-align: left",
    "text-center": "text-align: center",
    "text-right": "text-align: right",
    "text-justify": "text-align: justify",
    
    # Cursor
    "cursor-auto": "cursor: auto",
    "cursor-default": "cursor: default",
    "cursor-pointer": "cursor: pointer",
    "cursor-wait": "cursor: wait",
    "cursor-text": "cursor: text",
    "cursor-move": "cursor: move",
    "cursor-help": "cursor: help",
    "cursor-not-allowed": "cursor: not-allowed",
}

# Prefix-based utilities that take values
# Format: prefix: (css_property, value_transformer)
UTILITY_PREFIX_MAP = {
    # Spacing (Padding)
    "p-": ("padding", _fmt_rem),
    "pt-": ("padding-top", _fmt_rem),
    "pr-": ("padding-right", _fmt_rem),
    "pb-": ("padding-bottom", _fmt_rem),
    "pl-": ("padding-left", _fmt_rem),
    "px-": (["padding-left", "padding-right"], _fmt_rem),
    "py-": (["padding-top", "padding-bottom"], _fmt_rem),
    
    # Spacing (Margin)
    "m-": ("margin", _fmt_rem),
    "mt-": ("margin-top", _fmt_rem),
    "mr-": ("margin-right", _fmt_rem),
    "mb-": ("margin-bottom", _fmt_rem),
    "ml-": ("margin-left", _fmt_rem),
    "mx-": (["margin-left", "margin-right"], lambda v: "auto" if v == "auto" else _fmt_rem(v)),
    "my-": (["margin-top", "margin-bottom"], lambda v: "auto" if v == "auto" else _fmt_rem(v)),
    
    # Sizing
    "w-": ("width", lambda v: "100%" if v == "full" else ("100vw" if v == "screen" else _fmt_rem(v))),
    "h-": ("height", lambda v: "100%" if v == "full" else ("100vh" if v == "screen" else _fmt_rem(v))),
    "min-w-": ("min-width", lambda v: "100%" if v == "full" else ("100vw" if v == "screen" else _fmt_rem(v))),
    "min-h-": ("min-height", lambda v: "100%" if v == "full" else ("100vh" if v == "screen" else _fmt_rem(v))),
    "max-w-": ("max-width", lambda v: "100%" if v == "full" else ("100vw" if v == "screen" else _fmt_rem(v))),
    "max-h-": ("max-height", lambda v: "100%" if v == "full" else ("100vh" if v == "screen" else _fmt_rem(v))),
    
    # Typography
    "text-": ("font-size", lambda v: _get_font_size(v)), # Special handler for text-
    "font-": ("font-weight", lambda v: _get_font_weight(v)), # Special handler for font-
    
    # Background
    "bg-": ("background-color", lambda v: _get_color(v)),
    
    # Border
    "border-": ("border-color", lambda v: _get_color(v)), # Simplified, assumes color
    "rounded-": ("border-radius", lambda v: _get_radius(v)),
    
    # Grid
    "grid-cols-": ("grid-template-columns", lambda v: f"repeat({v}, minmax(0, 1fr))" if v.isdigit() else v),
    "gap-": ("gap", _fmt_rem),
    "gap-x-": ("column-gap", _fmt_rem),
    "gap-y-": ("row-gap", _fmt_rem),
    
    # Position
    "top-": ("top", _fmt_rem),
    "right-": ("right", _fmt_rem),
    "bottom-": ("bottom", _fmt_rem),
    "left-": ("left", _fmt_rem),
    "z-": ("z-index", lambda v: v),
    
    # Effects
    "opacity-": ("opacity", lambda v: str(float(v)/100) if v.isdigit() else v),
    "shadow-": ("box-shadow", lambda v: _get_shadow(v)),
}

def _get_font_size(v: str) -> str:
    sizes = {
        "xs": "0.75rem", "sm": "0.875rem", "base": "1rem", "lg": "1.125rem",
        "xl": "1.25rem", "2xl": "1.5rem", "3xl": "1.875rem", "4xl": "2.25rem",
        "5xl": "3rem", "6xl": "3.75rem", "7xl": "4.5rem", "8xl": "6rem", "9xl": "8rem"
    }
    if v in sizes: return sizes[v]
    # Check if it's a color (text-red-500)
    if v in _COLORS or any(v.startswith(c) for c in _COLORS.keys()) or v.startswith('[') or v.startswith('#'):
        return "color" # Special signal to change property to 'color'
    return v

def _get_font_weight(v: str) -> str:
    weights = {
        "thin": "100", "extralight": "200", "light": "300", "normal": "400",
        "medium": "500", "semibold": "600", "bold": "700", "extrabold": "800", "black": "900"
    }
    return weights.get(v, v)

def _get_radius(v: str) -> str:
    radii = {
        "none": "0px", "sm": "0.125rem", "md": "0.375rem", "lg": "0.5rem",
        "xl": "0.75rem", "2xl": "1rem", "3xl": "1.5rem", "full": "9999px"
    }
    # rounded (no suffix) is handled in UTILITY_PROPERTY_MAP if added, but here we handle rounded-
    return radii.get(v, "0.25rem" if v == "" else v) # rounded-DEFAULT not really standard, but handled

def _get_shadow(v: str) -> str:
    shadows = {
        "sm": "0 1px 2px 0 rgb(0 0 0 / 0.05)",
        "md": "0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1)",
        "lg": "0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1)",
        "xl": "0 20px 25px -5px rgb(0 0 0 / 0.1), 0 8px 10px -6px rgb(0 0 0 / 0.1)",
        "2xl": "0 25px 50px -12px rgb(0 0 0 / 0.25)",
        "inner": "inset 0 2px 4px 0 rgb(0 0 0 / 0.05)",
        "none": "none"
    }
    return shadows.get(v, "0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1)") # default shadow

# Basic color palette (simplified)
_COLORS = {
    "black": "#000", "white": "#fff",
    "slate": {"50": "#f8fafc", "100": "#f1f5f9", "200": "#e2e8f0", "300": "#cbd5e1", "400": "#94a3b8", "500": "#64748b", "600": "#475569", "700": "#334155", "800": "#1e293b", "900": "#0f172a"},
    "gray": {"50": "#f9fafb", "100": "#f3f4f6", "200": "#e5e7eb", "300": "#d1d5db", "400": "#9ca3af", "500": "#6b7280", "600": "#4b5563", "700": "#374151", "800": "#1f2937", "900": "#111827"},
    "red": {"50": "#fef2f2", "100": "#fee2e2", "200": "#fecaca", "300": "#fca5a5", "400": "#f87171", "500": "#ef4444", "600": "#dc2626", "700": "#b91c1c", "800": "#991b1b", "900": "#7f1d1d"},
    "orange": {"50": "#fff7ed", "100": "#ffedd5", "200": "#fed7aa", "300": "#fdba74", "400": "#fb923c", "500": "#f97316", "600": "#ea580c", "700": "#c2410c", "800": "#9a3412", "900": "#7c2d12"},
    "yellow": {"50": "#fefce8", "100": "#fef9c3", "200": "#fef08a", "300": "#fde047", "400": "#facc15", "500": "#eab308", "600": "#ca8a04", "700": "#a16207", "800": "#854d0e", "900": "#713f12"},
    "green": {"50": "#f0fdf4", "100": "#dcfce7", "200": "#bbf7d0", "300": "#86efac", "400": "#4ade80", "500": "#22c55e", "600": "#16a34a", "700": "#15803d", "800": "#166534", "900": "#14532d"},
    "blue": {"50": "#eff6ff", "100": "#dbeafe", "200": "#bfdbfe", "300": "#93c5fd", "400": "#60a5fa", "500": "#3b82f6", "600": "#2563eb", "700": "#1d4ed8", "800": "#1e40af", "900": "#1e3a8a"},
    "indigo": {"50": "#eef2ff", "100": "#e0e7ff", "200": "#c7d2fe", "300": "#a5b4fc", "400": "#818cf8", "500": "#6366f1", "600": "#4f46e5", "700": "#4338ca", "800": "#3730a3", "900": "#312e81"},
    "violet": {"50": "#f5f3ff", "100": "#ede9fe", "200": "#ddd6fe", "300": "#c4b5fd", "400": "#a78bfa", "500": "#8b5cf6", "600": "#7c3aed", "700": "#6d28d9", "800": "#5b21b6", "900": "#4c1d95"},
    "purple": {"50": "#faf5ff", "100": "#f3e8ff", "200": "#e9d5ff", "300": "#d8b4fe", "400": "#c084fc", "500": "#a855f7", "600": "#9333ea", "700": "#7e22ce", "800": "#6b21a8", "900": "#581c87"},
    "pink": {"50": "#fdf2f8", "100": "#fce7f3", "200": "#fbcfe8", "300": "#f9a8d4", "400": "#f472b6", "500": "#ec4899", "600": "#db2777", "700": "#be185d", "800": "#9d174d", "900": "#831843"},
}

def _get_color(v: str) -> str:
    # Handle arbitrary color: bg-[#f00]
    if v.startswith('[') and v.endswith(']'):
        return v[1:-1]
    
    # Handle palette colors: red-500
    parts = v.split('-')
    if len(parts) == 2:
        color, shade = parts
        if color in _COLORS and isinstance(_COLORS[color], dict) and shade in _COLORS[color]:
            return _COLORS[color][shade]
    elif len(parts) == 1:
        color = parts[0]
        if color in _COLORS and isinstance(_COLORS[color], str):
            return _COLORS[color]
            
    return v

def parse_utility_string(utility_string: str) -> Dict[str, Any]:
    """
    Parses a string of utility classes into a CSS dictionary.
    
    Example:
        "p-4 bg-red-500 flex" -> {'padding': '1rem', 'background-color': '#ef4444', 'display': 'flex'}
    """
    if not utility_string or not isinstance(utility_string, str):
        return {}
        
    styles = {}
    classes = utility_string.split()
    
    for cls in classes:
        # 1. Exact match (e.g., "flex", "hidden")
        if cls in UTILITY_PROPERTY_MAP:
            prop_val = UTILITY_PROPERTY_MAP[cls]
            prop, val = prop_val.split(':', 1)
            styles[prop.strip()] = val.strip()
            continue
            
        # 2. Prefix match (e.g., "p-4", "w-[100px]")
        matched = False
        for prefix, (prop, transformer) in UTILITY_PREFIX_MAP.items():
            if cls.startswith(prefix):
                value_part = cls[len(prefix):]
                
                # Handle arbitrary values [value]
                if value_part.startswith('[') and value_part.endswith(']'):
                    value = value_part[1:-1]
                    # Replace underscores with spaces in arbitrary values
                    value = value.replace('_', ' ')
                else:
                    value = transformer(value_part)
                
                # Special case: text-red-500 returns "color" as value to signal property change
                if prefix == "text-" and value == "color":
                    prop = "color"
                    value = _get_color(value_part)
                
                if isinstance(prop, list):
                    for p in prop:
                        styles[p] = value
                else:
                    styles[prop] = value
                matched = True
                break
        
        if not matched:
            # Fallback: maybe it's a border-radius shorthand "rounded"
            if cls == "rounded":
                styles["border-radius"] = "0.25rem"
            elif cls.startswith("border") and cls != "border":
                # border-red-500 -> border-color
                # border-2 -> border-width
                suffix = cls[7:] # remove "border-"
                if suffix.isdigit():
                    styles["border-width"] = f"{suffix}px"
                else:
                    styles["border-color"] = _get_color(suffix)
            elif cls == "border":
                 styles["border-width"] = "1px"
            
    return styles
