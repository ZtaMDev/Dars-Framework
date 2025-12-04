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
    "table": "display: table",
    "table-row": "display: table-row",
    "table-cell": "display: table-cell",
    "hidden": "display: none",
    "contents": "display: contents",
    "flow-root": "display: flow-root",
    
    # Flexbox
    "flex-row": "flex-direction: row",
    "flex-row-reverse": "flex-direction: row-reverse",
    "flex-col": "flex-direction: column",
    "flex-col-reverse": "flex-direction: column-reverse",
    "flex-wrap": "flex-wrap: wrap",
    "flex-wrap-reverse": "flex-wrap: wrap-reverse",
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
    "justify-items-start": "justify-items: start",
    "justify-items-end": "justify-items: end",
    "justify-items-center": "justify-items: center",
    "justify-items-stretch": "justify-items: stretch",
    "content-start": "align-content: flex-start",
    "content-end": "align-content: flex-end",
    "content-center": "align-content: center",
    "content-between": "align-content: space-between",
    "content-around": "align-content: space-around",
    "content-evenly": "align-content: space-evenly",
    "self-auto": "align-self: auto",
    "self-start": "align-self: flex-start",
    "self-end": "align-self: flex-end",
    "self-center": "align-self: center",
    "self-stretch": "align-self: stretch",
    "self-baseline": "align-self: baseline",
    "grow": "flex-grow: 1",
    "grow-0": "flex-grow: 0",
    "shrink": "flex-shrink: 1",
    "shrink-0": "flex-shrink: 0",
    
    # Grid
    "grid-flow-row": "grid-auto-flow: row",
    "grid-flow-col": "grid-auto-flow: column",
    "grid-flow-dense": "grid-auto-flow: dense",
    "grid-flow-row-dense": "grid-auto-flow: row dense",
    "grid-flow-col-dense": "grid-auto-flow: column dense",
    "auto-cols-auto": "grid-auto-columns: auto",
    "auto-cols-min": "grid-auto-columns: min-content",
    "auto-cols-max": "grid-auto-columns: max-content",
    "auto-cols-fr": "grid-auto-columns: minmax(0, 1fr)",
    "auto-rows-auto": "grid-auto-rows: auto",
    "auto-rows-min": "grid-auto-rows: min-content",
    "auto-rows-max": "grid-auto-rows: max-content",
    "auto-rows-fr": "grid-auto-rows: minmax(0, 1fr)",

    # Positioning
    "static": "position: static",
    "fixed": "position: fixed",
    "absolute": "position: absolute",
    "relative": "position: relative",
    "sticky": "position: sticky",
    
    # Float & Clear
    "float-right": "float: right",
    "float-left": "float: left",
    "float-none": "float: none",
    "clear-left": "clear: left",
    "clear-right": "clear: right",
    "clear-both": "clear: both",
    "clear-none": "clear: none",
    
    # Overflow
    "overflow-auto": "overflow: auto",
    "overflow-hidden": "overflow: hidden",
    "overflow-clip": "overflow: clip",
    "overflow-visible": "overflow: visible",
    "overflow-scroll": "overflow: scroll",
    "overflow-x-auto": "overflow-x: auto",
    "overflow-x-hidden": "overflow-x: hidden",
    "overflow-x-clip": "overflow-x: clip",
    "overflow-x-visible": "overflow-x: visible",
    "overflow-x-scroll": "overflow-x: scroll",
    "overflow-y-auto": "overflow-y: auto",
    "overflow-y-hidden": "overflow-y: hidden",
    "overflow-y-clip": "overflow-y: clip",
    "overflow-y-visible": "overflow-y: visible",
    "overflow-y-scroll": "overflow-y: scroll",
    
    # Visibility
    "visible": "visibility: visible",
    "invisible": "visibility: hidden",
    "collapse": "visibility: collapse",
    
    # Typography
    "italic": "font-style: italic",
    "not-italic": "font-style: normal",
    "underline": "text-decoration: underline",
    "overline": "text-decoration: overline",
    "line-through": "text-decoration: line-through",
    "no-underline": "text-decoration: none",
    "uppercase": "text-transform: uppercase",
    "lowercase": "text-transform: lowercase",
    "capitalize": "text-transform: capitalize",
    "normal-case": "text-transform: none",
    "text-left": "text-align: left",
    "text-center": "text-align: center",
    "text-right": "text-align: right",
    "text-justify": "text-align: justify",
    "text-start": "text-align: start",
    "text-end": "text-align: end",
    "align-baseline": "vertical-align: baseline",
    "align-top": "vertical-align: top",
    "align-middle": "vertical-align: middle",
    "align-bottom": "vertical-align: bottom",
    "align-text-top": "vertical-align: text-top",
    "align-text-bottom": "vertical-align: text-bottom",
    "align-sub": "vertical-align: sub",
    "align-super": "vertical-align: super",
    "whitespace-normal": "white-space: normal",
    "whitespace-nowrap": "white-space: nowrap",
    "whitespace-pre": "white-space: pre",
    "whitespace-pre-line": "white-space: pre-line",
    "whitespace-pre-wrap": "white-space: pre-wrap",
    "whitespace-break-spaces": "white-space: break-spaces",
    "break-normal": "word-break: normal",
    "break-words": "word-break: break-word",
    "break-all": "word-break: break-all",
    "break-keep": "word-break: keep-all",
    "truncate": "overflow: hidden; text-overflow: ellipsis; white-space: nowrap",
    "text-ellipsis": "text-overflow: ellipsis",
    "text-clip": "text-overflow: clip",
    
    # Cursor
    "cursor-auto": "cursor: auto",
    "cursor-default": "cursor: default",
    "cursor-pointer": "cursor: pointer",
    "cursor-wait": "cursor: wait",
    "cursor-text": "cursor: text",
    "cursor-move": "cursor: move",
    "cursor-help": "cursor: help",
    "cursor-not-allowed": "cursor: not-allowed",
    "cursor-none": "cursor: none",
    "cursor-context-menu": "cursor: context-menu",
    "cursor-progress": "cursor: progress",
    "cursor-cell": "cursor: cell",
    "cursor-crosshair": "cursor: crosshair",
    "cursor-vertical-text": "cursor: vertical-text",
    "cursor-alias": "cursor: alias",
    "cursor-copy": "cursor: copy",
    "cursor-no-drop": "cursor: no-drop",
    "cursor-grab": "cursor: grab",
    "cursor-grabbing": "cursor: grabbing",
    "cursor-all-scroll": "cursor: all-scroll",
    "cursor-col-resize": "cursor: col-resize",
    "cursor-row-resize": "cursor: row-resize",
    "cursor-n-resize": "cursor: n-resize",
    "cursor-e-resize": "cursor: e-resize",
    "cursor-s-resize": "cursor: s-resize",
    "cursor-w-resize": "cursor: w-resize",
    "cursor-ne-resize": "cursor: ne-resize",
    "cursor-nw-resize": "cursor: nw-resize",
    "cursor-se-resize": "cursor: se-resize",
    "cursor-sw-resize": "cursor: sw-resize",
    "cursor-ew-resize": "cursor: ew-resize",
    "cursor-ns-resize": "cursor: ns-resize",
    "cursor-nesw-resize": "cursor: nesw-resize",
    "cursor-nwse-resize": "cursor: nwse-resize",
    "cursor-zoom-in": "cursor: zoom-in",
    "cursor-zoom-out": "cursor: zoom-out",
    
    # Pointer Events
    "pointer-events-none": "pointer-events: none",
    "pointer-events-auto": "pointer-events: auto",
    
    # User Select
    "select-none": "user-select: none",
    "select-text": "user-select: text",
    "select-all": "user-select: all",
    "select-auto": "user-select: auto",
    
    # Object Fit
    "object-contain": "object-fit: contain",
    "object-cover": "object-fit: cover",
    "object-fill": "object-fit: fill",
    "object-none": "object-fit: none",
    "object-scale-down": "object-fit: scale-down",
    
    # Object Position
    "object-bottom": "object-position: bottom",
    "object-center": "object-position: center",
    "object-left": "object-position: left",
    "object-left-bottom": "object-position: left bottom",
    "object-left-top": "object-position: left top",
    "object-right": "object-position: right",
    "object-right-bottom": "object-position: right bottom",
    "object-right-top": "object-position: right top",
    "object-top": "object-position: top",
    
    # Box Sizing
    "box-border": "box-sizing: border-box",
    "box-content": "box-sizing: content-box",
    
    # Border Style
    "border-solid": "border-style: solid",
    "border-dashed": "border-style: dashed",
    "border-dotted": "border-style: dotted",
    "border-double": "border-style: double",
    "border-hidden": "border-style: hidden",
    "border-none": "border-style: none",
    
    # Mix Blend Mode
    "mix-blend-normal": "mix-blend-mode: normal",
    "mix-blend-multiply": "mix-blend-mode: multiply",
    "mix-blend-screen": "mix-blend-mode: screen",
    "mix-blend-overlay": "mix-blend-mode: overlay",
    "mix-blend-darken": "mix-blend-mode: darken",
    "mix-blend-lighten": "mix-blend-mode: lighten",
    "mix-blend-color-dodge": "mix-blend-mode: color-dodge",
    "mix-blend-color-burn": "mix-blend-mode: color-burn",
    "mix-blend-hard-light": "mix-blend-mode: hard-light",
    "mix-blend-soft-light": "mix-blend-mode: soft-light",
    "mix-blend-difference": "mix-blend-mode: difference",
    "mix-blend-exclusion": "mix-blend-mode: exclusion",
    "mix-blend-hue": "mix-blend-mode: hue",
    "mix-blend-saturation": "mix-blend-mode: saturation",
    "mix-blend-color": "mix-blend-mode: color",
    "mix-blend-luminosity": "mix-blend-mode: luminosity",
    
    # Background Blend Mode
    "bg-blend-normal": "background-blend-mode: normal",
    "bg-blend-multiply": "background-blend-mode: multiply",
    "bg-blend-screen": "background-blend-mode: screen",
    "bg-blend-overlay": "background-blend-mode: overlay",
    "bg-blend-darken": "background-blend-mode: darken",
    "bg-blend-lighten": "background-blend-mode: lighten",
    "bg-blend-color-dodge": "background-blend-mode: color-dodge",
    "bg-blend-color-burn": "background-blend-mode: color-burn",
    "bg-blend-hard-light": "background-blend-mode: hard-light",
    "bg-blend-soft-light": "background-blend-mode: soft-light",
    "bg-blend-difference": "background-blend-mode: difference",
    "bg-blend-exclusion": "background-blend-mode: exclusion",
    "bg-blend-hue": "background-blend-mode: hue",
    "bg-blend-saturation": "background-blend-mode: saturation",
    "bg-blend-color": "background-blend-mode: color",
    "bg-blend-luminosity": "background-blend-mode: luminosity",
    
    # Background Attachment
    "bg-fixed": "background-attachment: fixed",
    "bg-local": "background-attachment: local",
    "bg-scroll": "background-attachment: scroll",
    
    # Background Clip
    "bg-clip-border": "background-clip: border-box",
    "bg-clip-padding": "background-clip: padding-box",
    "bg-clip-content": "background-clip: content-box",
    "bg-clip-text": "background-clip: text",
    
    # Background Origin
    "bg-origin-border": "background-origin: border-box",
    "bg-origin-padding": "background-origin: padding-box",
    "bg-origin-content": "background-origin: content-box",
    
    # Background Position
    "bg-bottom": "background-position: bottom",
    "bg-center": "background-position: center",
    "bg-left": "background-position: left",
    "bg-left-bottom": "background-position: left bottom",
    "bg-left-top": "background-position: left top",
    "bg-right": "background-position: right",
    "bg-right-bottom": "background-position: right bottom",
    "bg-right-top": "background-position: right top",
    "bg-top": "background-position: top",
    
    # Background Repeat
    "bg-repeat": "background-repeat: repeat",
    "bg-no-repeat": "background-repeat: no-repeat",
    "bg-repeat-x": "background-repeat: repeat-x",
    "bg-repeat-y": "background-repeat: repeat-y",
    "bg-repeat-round": "background-repeat: round",
    "bg-repeat-space": "background-repeat: space",
    
    # Background Size
    "bg-auto": "background-size: auto",
    "bg-cover": "background-size: cover",
    "bg-contain": "background-size: contain",
    
    # Isolation
    "isolate": "isolation: isolate",
    "isolation-auto": "isolation: auto",
    
    # List Style Type
    "list-none": "list-style-type: none",
    "list-disc": "list-style-type: disc",
    "list-decimal": "list-style-type: decimal",
    
    # List Style Position
    "list-inside": "list-style-position: inside",
    "list-outside": "list-style-position: outside",
    
    # Appearance
    "appearance-none": "appearance: none",
    "appearance-auto": "appearance: auto",
    
    # Resize
    "resize-none": "resize: none",
    "resize-y": "resize: vertical",
    "resize-x": "resize: horizontal",
    "resize": "resize: both",
    
    # Scroll Behavior
    "scroll-auto": "scroll-behavior: auto",
    "scroll-smooth": "scroll-behavior: smooth",
    
    # Scroll Snap Align
    "snap-start": "scroll-snap-align: start",
    "snap-end": "scroll-snap-align: end",
    "snap-center": "scroll-snap-align: center",
    "snap-align-none": "scroll-snap-align: none",
    
    # Scroll Snap Stop
    "snap-normal": "scroll-snap-stop: normal",
    "snap-always": "scroll-snap-stop: always",
    
    # Scroll Snap Type
    "snap-none": "scroll-snap-type: none",
    "snap-x": "scroll-snap-type: x var(--tw-scroll-snap-strictness)",
    "snap-y": "scroll-snap-type: y var(--tw-scroll-snap-strictness)",
    "snap-both": "scroll-snap-type: both var(--tw-scroll-snap-strictness)",
    "snap-mandatory": "scroll-snap-type: var(--tw-scroll-snap-axis) mandatory",
    "snap-proximity": "scroll-snap-type: var(--tw-scroll-snap-axis) proximity",
    
    # Touch Action
    "touch-auto": "touch-action: auto",
    "touch-none": "touch-action: none",
    "touch-pan-x": "touch-action: pan-x",
    "touch-pan-left": "touch-action: pan-left",
    "touch-pan-right": "touch-action: pan-right",
    "touch-pan-y": "touch-action: pan-y",
    "touch-pan-up": "touch-action: pan-up",
    "touch-pan-down": "touch-action: pan-down",
    "touch-pinch-zoom": "touch-action: pinch-zoom",
    "touch-manipulation": "touch-action: manipulation",
    
    # Will Change
    "will-change-auto": "will-change: auto",
    "will-change-scroll": "will-change: scroll-position",
    "will-change-contents": "will-change: contents",
    "will-change-transform": "will-change: transform",
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
    "ps-": ("padding-inline-start", _fmt_rem),
    "pe-": ("padding-inline-end", _fmt_rem),
    
    # Spacing (Margin)
    "m-": ("margin", _fmt_rem),
    "mt-": ("margin-top", _fmt_rem),
    "mr-": ("margin-right", _fmt_rem),
    "mb-": ("margin-bottom", _fmt_rem),
    "ml-": ("margin-left", _fmt_rem),
    "mx-": (["margin-left", "margin-right"], lambda v: "auto" if v == "auto" else _fmt_rem(v)),
    "my-": (["margin-top", "margin-bottom"], lambda v: "auto" if v == "auto" else _fmt_rem(v)),
    "ms-": ("margin-inline-start", _fmt_rem),
    "me-": ("margin-inline-end", _fmt_rem),
    
    # Space Between
    "space-x-": ("margin-left", _fmt_rem),  # Simplified
    "space-y-": ("margin-top", _fmt_rem),   # Simplified
    
    # Sizing
    "w-": ("width", lambda v: "100%" if v == "full" else ("100vw" if v == "screen" else ("auto" if v == "auto" else ("fit-content" if v == "fit" else ("min-content" if v == "min" else ("max-content" if v == "max" else _fmt_rem(v))))))),
    "h-": ("height", lambda v: "100%" if v == "full" else ("100vh" if v == "screen" else ("auto" if v == "auto" else ("fit-content" if v == "fit" else ("min-content" if v == "min" else ("max-content" if v == "max" else _fmt_rem(v))))))),
    "min-w-": ("min-width", lambda v: "100%" if v == "full" else ("100vw" if v == "screen" else ("min-content" if v == "min" else ("max-content" if v == "max" else ("fit-content" if v == "fit" else _fmt_rem(v)))))),
    "min-h-": ("min-height", lambda v: "100%" if v == "full" else ("100vh" if v == "screen" else ("min-content" if v == "min" else ("max-content" if v == "max" else ("fit-content" if v == "fit" else _fmt_rem(v)))))),
    "max-w-": ("max-width", lambda v: _get_max_width(v)),
    "max-h-": ("max-height", lambda v: "100%" if v == "full" else ("100vh" if v == "screen" else ("min-content" if v == "min" else ("max-content" if v == "max" else ("fit-content" if v == "fit" else ("none" if v == "none" else _fmt_rem(v))))))),
    "size-": (["width", "height"], _fmt_rem),
    
    # Typography
    "text-": ("font-size", lambda v: _get_font_size(v)), # Special handler for text-
    "font-": ("font-weight", lambda v: _get_font_weight(v)), # Special handler for font-
    "fs-": ("font-size", lambda v: v),  # Direct font-size: fs-[32px]
    "leading-": ("line-height", lambda v: _get_line_height(v)),
    "tracking-": ("letter-spacing", lambda v: _get_letter_spacing(v)),
    "indent-": ("text-indent", _fmt_rem),
    
    # Background
    "bg-": ("background-color", lambda v: _get_color(v)),
    
    # Border
    "border-": ("border-color", lambda v: _get_color(v)), # Simplified, assumes color
    "border-t-": ("border-top-color", lambda v: _get_color(v)),
    "border-r-": ("border-right-color", lambda v: _get_color(v)),
    "border-b-": ("border-bottom-color", lambda v: _get_color(v)),
    "border-l-": ("border-left-color", lambda v: _get_color(v)),
    "border-x-": (["border-left-color", "border-right-color"], lambda v: _get_color(v)),
    "border-y-": (["border-top-color", "border-bottom-color"], lambda v: _get_color(v)),
    "rounded-": ("border-radius", lambda v: _get_radius(v)),
    "rounded-t-": (["border-top-left-radius", "border-top-right-radius"], lambda v: _get_radius(v)),
    "rounded-r-": (["border-top-right-radius", "border-bottom-right-radius"], lambda v: _get_radius(v)),
    "rounded-b-": (["border-bottom-left-radius", "border-bottom-right-radius"], lambda v: _get_radius(v)),
    "rounded-l-": (["border-top-left-radius", "border-bottom-left-radius"], lambda v: _get_radius(v)),
    "rounded-tl-": ("border-top-left-radius", lambda v: _get_radius(v)),
    "rounded-tr-": ("border-top-right-radius", lambda v: _get_radius(v)),
    "rounded-br-": ("border-bottom-right-radius", lambda v: _get_radius(v)),
    "rounded-bl-": ("border-bottom-left-radius", lambda v: _get_radius(v)),
    
    # Outline
    "outline-": ("outline-color", lambda v: _get_color(v)),
    "outline-offset-": ("outline-offset", lambda v: f"{v}px"),
    
    # Ring (simplified as box-shadow)
    "ring-": ("box-shadow", lambda v: f"0 0 0 {v}px rgba(59, 130, 246, 0.5)"),
    "ring-offset-": ("box-shadow", lambda v: f"0 0 0 {v}px #fff, 0 0 0 calc({v}px + 3px) rgba(59, 130, 246, 0.5)"),
    
    # Grid
    "grid-cols-": ("grid-template-columns", lambda v: f"repeat({v}, minmax(0, 1fr))" if v.isdigit() else v),
    "grid-rows-": ("grid-template-rows", lambda v: f"repeat({v}, minmax(0, 1fr))" if v.isdigit() else v),
    "col-span-": ("grid-column", lambda v: f"span {v} / span {v}" if v.isdigit() else v),
    "col-start-": ("grid-column-start", lambda v: v),
    "col-end-": ("grid-column-end", lambda v: v),
    "row-span-": ("grid-row", lambda v: f"span {v} / span {v}" if v.isdigit() else v),
    "row-start-": ("grid-row-start", lambda v: v),
    "row-end-": ("grid-row-end", lambda v: v),
    "gap-": ("gap", _fmt_rem),
    "gap-x-": ("column-gap", _fmt_rem),
    "gap-y-": ("row-gap", _fmt_rem),
    
    # Flex
    "flex-": ("flex", lambda v: _get_flex(v)),
    "order-": ("order", lambda v: v),
    "basis-": ("flex-basis", _fmt_rem),
    
    # Position
    "top-": ("top", _fmt_rem),
    "right-": ("right", _fmt_rem),
    "bottom-": ("bottom", _fmt_rem),
    "left-": ("left", _fmt_rem),
    "inset-": (["top", "right", "bottom", "left"], _fmt_rem),
    "inset-x-": (["left", "right"], _fmt_rem),
    "inset-y-": (["top", "bottom"], _fmt_rem),
    "z-": ("z-index", lambda v: v),
    
    # Effects
    "opacity-": ("opacity", lambda v: str(float(v)/100) if v.isdigit() else v),
    "shadow-": ("box-shadow", lambda v: _get_shadow(v)),
    
    # Filters
    "blur-": ("filter", lambda v: f"blur({_get_blur(v)})"),
    "brightness-": ("filter", lambda v: f"brightness({v}%)"),
    "contrast-": ("filter", lambda v: f"contrast({v}%)"),
    "grayscale-": ("filter", lambda v: f"grayscale({v}%)"),
    "hue-rotate-": ("filter", lambda v: f"hue-rotate({v}deg)"),
    "invert-": ("filter", lambda v: f"invert({v}%)"),
    "saturate-": ("filter", lambda v: f"saturate({v}%)"),
    "sepia-": ("filter", lambda v: f"sepia({v}%)"),
    "drop-shadow-": ("filter", lambda v: f"drop-shadow({_get_drop_shadow(v)})"),
    
    # Backdrop Filters
    "backdrop-blur-": ("backdrop-filter", lambda v: f"blur({_get_blur(v)})"),
    "backdrop-brightness-": ("backdrop-filter", lambda v: f"brightness({v}%)"),
    "backdrop-contrast-": ("backdrop-filter", lambda v: f"contrast({v}%)"),
    "backdrop-grayscale-": ("backdrop-filter", lambda v: f"grayscale({v}%)"),
    "backdrop-hue-rotate-": ("backdrop-filter", lambda v: f"hue-rotate({v}deg)"),
    "backdrop-invert-": ("backdrop-filter", lambda v: f"invert({v}%)"),
    "backdrop-opacity-": ("backdrop-filter", lambda v: f"opacity({v}%)"),
    "backdrop-saturate-": ("backdrop-filter", lambda v: f"saturate({v}%)"),
    "backdrop-sepia-": ("backdrop-filter", lambda v: f"sepia({v}%)"),
    
    # Transforms
    "scale-": ("transform", lambda v: f"scale({float(v)/100})"),
    "scale-x-": ("transform", lambda v: f"scaleX({float(v)/100})"),
    "scale-y-": ("transform", lambda v: f"scaleY({float(v)/100})"),
    "rotate-": ("transform", lambda v: f"rotate({v}deg)"),
    "translate-x-": ("transform", lambda v: f"translateX({_fmt_rem(v)})"),
    "translate-y-": ("transform", lambda v: f"translateY({_fmt_rem(v)})"),
    "skew-x-": ("transform", lambda v: f"skewX({v}deg)"),
    "skew-y-": ("transform", lambda v: f"skewY({v}deg)"),
    
    # Transform Origin
    "origin-": ("transform-origin", lambda v: _get_transform_origin(v)),
    
    # Transitions
    "transition-": ("transition-property", lambda v: _get_transition_property(v)),
    "duration-": ("transition-duration", lambda v: f"{v}ms"),
    "delay-": ("transition-delay", lambda v: f"{v}ms"),
    "ease-": ("transition-timing-function", lambda v: _get_timing_function(v)),
    
    # Animations
    "animate-": ("animation", lambda v: _get_animation(v)),
    
    # Aspect Ratio
    "aspect-": ("aspect-ratio", lambda v: _get_aspect_ratio(v)),
    
    # Columns
    "columns-": ("columns", lambda v: v),
    
    # Break After/Before/Inside
    "break-after-": ("break-after", lambda v: v),
    "break-before-": ("break-before", lambda v: v),
    "break-inside-": ("break-inside", lambda v: v),
    
    # Scroll Margin
    "scroll-m-": ("scroll-margin", _fmt_rem),
    "scroll-mx-": (["scroll-margin-left", "scroll-margin-right"], _fmt_rem),
    "scroll-my-": (["scroll-margin-top", "scroll-margin-bottom"], _fmt_rem),
    "scroll-mt-": ("scroll-margin-top", _fmt_rem),
    "scroll-mr-": ("scroll-margin-right", _fmt_rem),
    "scroll-mb-": ("scroll-margin-bottom", _fmt_rem),
    "scroll-ml-": ("scroll-margin-left", _fmt_rem),
    
    # Scroll Padding
    "scroll-p-": ("scroll-padding", _fmt_rem),
    "scroll-px-": (["scroll-padding-left", "scroll-padding-right"], _fmt_rem),
    "scroll-py-": (["scroll-padding-top", "scroll-padding-bottom"], _fmt_rem),
    "scroll-pt-": ("scroll-padding-top", _fmt_rem),
    "scroll-pr-": ("scroll-padding-right", _fmt_rem),
    "scroll-pb-": ("scroll-padding-bottom", _fmt_rem),
    "scroll-pl-": ("scroll-padding-left", _fmt_rem),
}

def _get_max_width(v: str) -> str:
    sizes = {
        "none": "none",
        "xs": "20rem",
        "sm": "24rem",
        "md": "28rem",
        "lg": "32rem",
        "xl": "36rem",
        "2xl": "42rem",
        "3xl": "48rem",
        "4xl": "56rem",
        "5xl": "64rem",
        "6xl": "72rem",
        "7xl": "80rem",
        "full": "100%",
        "min": "min-content",
        "max": "max-content",
        "fit": "fit-content",
        "prose": "65ch",
        "screen-sm": "640px",
        "screen-md": "768px",
        "screen-lg": "1024px",
        "screen-xl": "1280px",
        "screen-2xl": "1536px",
    }
    return sizes.get(v, _fmt_rem(v))

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

def _get_line_height(v: str) -> str:
    heights = {
        "none": "1",
        "tight": "1.25",
        "snug": "1.375",
        "normal": "1.5",
        "relaxed": "1.625",
        "loose": "2",
    }
    return heights.get(v, _fmt_rem(v))

def _get_letter_spacing(v: str) -> str:
    spacings = {
        "tighter": "-0.05em",
        "tight": "-0.025em",
        "normal": "0em",
        "wide": "0.025em",
        "wider": "0.05em",
        "widest": "0.1em",
    }
    return spacings.get(v, v)

def _get_radius(v: str) -> str:
    radii = {
        "none": "0px", "sm": "0.125rem", "md": "0.375rem", "lg": "0.5rem",
        "xl": "0.75rem", "2xl": "1rem", "3xl": "1.5rem", "full": "9999px"
    }
    return radii.get(v, "0.25rem" if v == "" else v)

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
    return shadows.get(v, "0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1)")

def _get_blur(v: str) -> str:
    blurs = {
        "none": "0",
        "sm": "4px",
        "md": "12px",
        "lg": "16px",
        "xl": "24px",
        "2xl": "40px",
        "3xl": "64px",
    }
    return blurs.get(v, f"{v}px")

def _get_drop_shadow(v: str) -> str:
    shadows = {
        "sm": "0 1px 1px rgb(0 0 0 / 0.05)",
        "md": "0 4px 3px rgb(0 0 0 / 0.07), 0 2px 2px rgb(0 0 0 / 0.06)",
        "lg": "0 10px 8px rgb(0 0 0 / 0.04), 0 4px 3px rgb(0 0 0 / 0.1)",
        "xl": "0 20px 13px rgb(0 0 0 / 0.03), 0 8px 5px rgb(0 0 0 / 0.08)",
        "2xl": "0 25px 25px rgb(0 0 0 / 0.15)",
        "none": "0 0 #0000",
    }
    return shadows.get(v, "0 1px 2px rgb(0 0 0 / 0.1), 0 1px 1px rgb(0 0 0 / 0.06)")

def _get_flex(v: str) -> str:
    flex_values = {
        "1": "1 1 0%",
        "auto": "1 1 auto",
        "initial": "0 1 auto",
        "none": "none",
    }
    return flex_values.get(v, v)

def _get_transform_origin(v: str) -> str:
    origins = {
        "center": "center",
        "top": "top",
        "top-right": "top right",
        "right": "right",
        "bottom-right": "bottom right",
        "bottom": "bottom",
        "bottom-left": "bottom left",
        "left": "left",
        "top-left": "top left",
    }
    return origins.get(v, v)

def _get_transition_property(v: str) -> str:
    properties = {
        "none": "none",
        "all": "all",
        "colors": "color, background-color, border-color, text-decoration-color, fill, stroke",
        "opacity": "opacity",
        "shadow": "box-shadow",
        "transform": "transform",
    }
    return properties.get(v, v)

def _get_timing_function(v: str) -> str:
    functions = {
        "linear": "linear",
        "in": "cubic-bezier(0.4, 0, 1, 1)",
        "out": "cubic-bezier(0, 0, 0.2, 1)",
        "in-out": "cubic-bezier(0.4, 0, 0.2, 1)",
    }
    return functions.get(v, v)

def _get_animation(v: str) -> str:
    animations = {
        "none": "none",
        "spin": "spin 1s linear infinite",
        "ping": "ping 1s cubic-bezier(0, 0, 0.2, 1) infinite",
        "pulse": "pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite",
        "bounce": "bounce 1s infinite",
    }
    return animations.get(v, v)

def _get_aspect_ratio(v: str) -> str:
    ratios = {
        "auto": "auto",
        "square": "1 / 1",
        "video": "16 / 9",
    }
    return ratios.get(v, v.replace("-", " / "))

# Expanded color palette with ALL Tailwind colors
_COLORS = {
    "black": "#000",
    "white": "#fff",
    "transparent": "transparent",
    "current": "currentColor",
    
    # Slate
    "slate": {
        "50": "#f8fafc", "100": "#f1f5f9", "200": "#e2e8f0", "300": "#cbd5e1",
        "400": "#94a3b8", "500": "#64748b", "600": "#475569", "700": "#334155",
        "800": "#1e293b", "900": "#0f172a", "950": "#020617"
    },
    
    # Gray
    "gray": {
        "50": "#f9fafb", "100": "#f3f4f6", "200": "#e5e7eb", "300": "#d1d5db",
        "400": "#9ca3af", "500": "#6b7280", "600": "#4b5563", "700": "#374151",
        "800": "#1f2937", "900": "#111827", "950": "#030712"
    },
    
    # Zinc
    "zinc": {
        "50": "#fafafa", "100": "#f4f4f5", "200": "#e4e4e7", "300": "#d4d4d8",
        "400": "#a1a1aa", "500": "#71717a", "600": "#52525b", "700": "#3f3f46",
        "800": "#27272a", "900": "#18181b", "950": "#09090b"
    },
    
    # Neutral
    "neutral": {
        "50": "#fafafa", "100": "#f5f5f5", "200": "#e5e5e5", "300": "#d4d4d4",
        "400": "#a3a3a3", "500": "#737373", "600": "#525252", "700": "#404040",
        "800": "#262626", "900": "#171717", "950": "#0a0a0a"
    },
    
    # Stone
    "stone": {
        "50": "#fafaf9", "100": "#f5f5f4", "200": "#e7e5e4", "300": "#d6d3d1",
        "400": "#a8a29e", "500": "#78716c", "600": "#57534e", "700": "#44403c",
        "800": "#292524", "900": "#1c1917", "950": "#0c0a09"
    },
    
    # Red
    "red": {
        "50": "#fef2f2", "100": "#fee2e2", "200": "#fecaca", "300": "#fca5a5",
        "400": "#f87171", "500": "#ef4444", "600": "#dc2626", "700": "#b91c1c",
        "800": "#991b1b", "900": "#7f1d1d", "950": "#450a0a"
    },
    
    # Orange
    "orange": {
        "50": "#fff7ed", "100": "#ffedd5", "200": "#fed7aa", "300": "#fdba74",
        "400": "#fb923c", "500": "#f97316", "600": "#ea580c", "700": "#c2410c",
        "800": "#9a3412", "900": "#7c2d12", "950": "#431407"
    },
    
    # Amber
    "amber": {
        "50": "#fffbeb", "100": "#fef3c7", "200": "#fde68a", "300": "#fcd34d",
        "400": "#fbbf24", "500": "#f59e0b", "600": "#d97706", "700": "#b45309",
        "800": "#92400e", "900": "#78350f", "950": "#451a03"
    },
    
    # Yellow
    "yellow": {
        "50": "#fefce8", "100": "#fef9c3", "200": "#fef08a", "300": "#fde047",
        "400": "#facc15", "500": "#eab308", "600": "#ca8a04", "700": "#a16207",
        "800": "#854d0e", "900": "#713f12", "950": "#422006"
    },
    
    # Lime
    "lime": {
        "50": "#f7fee7", "100": "#ecfccb", "200": "#d9f99d", "300": "#bef264",
        "400": "#a3e635", "500": "#84cc16", "600": "#65a30d", "700": "#4d7c0f",
        "800": "#3f6212", "900": "#365314", "950": "#1a2e05"
    },
    
    # Green
    "green": {
        "50": "#f0fdf4", "100": "#dcfce7", "200": "#bbf7d0", "300": "#86efac",
        "400": "#4ade80", "500": "#22c55e", "600": "#16a34a", "700": "#15803d",
        "800": "#166534", "900": "#14532d", "950": "#052e16"
    },
    
    # Emerald
    "emerald": {
        "50": "#ecfdf5", "100": "#d1fae5", "200": "#a7f3d0", "300": "#6ee7b7",
        "400": "#34d399", "500": "#10b981", "600": "#059669", "700": "#047857",
        "800": "#065f46", "900": "#064e3b", "950": "#022c22"
    },
    
    # Teal
    "teal": {
        "50": "#f0fdfa", "100": "#ccfbf1", "200": "#99f6e4", "300": "#5eead4",
        "400": "#2dd4bf", "500": "#14b8a6", "600": "#0d9488", "700": "#0f766e",
        "800": "#115e59", "900": "#134e4a", "950": "#042f2e"
    },
    
    # Cyan
    "cyan": {
        "50": "#ecfeff", "100": "#cffafe", "200": "#a5f3fc", "300": "#67e8f9",
        "400": "#22d3ee", "500": "#06b6d4", "600": "#0891b2", "700": "#0e7490",
        "800": "#155e75", "900": "#164e63", "950": "#083344"
    },
    
    # Sky
    "sky": {
        "50": "#f0f9ff", "100": "#e0f2fe", "200": "#bae6fd", "300": "#7dd3fc",
        "400": "#38bdf8", "500": "#0ea5e9", "600": "#0284c7", "700": "#0369a1",
        "800": "#075985", "900": "#0c4a6e", "950": "#082f49"
    },
    
    # Blue
    "blue": {
        "50": "#eff6ff", "100": "#dbeafe", "200": "#bfdbfe", "300": "#93c5fd",
        "400": "#60a5fa", "500": "#3b82f6", "600": "#2563eb", "700": "#1d4ed8",
        "800": "#1e40af", "900": "#1e3a8a", "950": "#172554"
    },
    
    # Indigo
    "indigo": {
        "50": "#eef2ff", "100": "#e0e7ff", "200": "#c7d2fe", "300": "#a5b4fc",
        "400": "#818cf8", "500": "#6366f1", "600": "#4f46e5", "700": "#4338ca",
        "800": "#3730a3", "900": "#312e81", "950": "#1e1b4b"
    },
    
    # Violet
    "violet": {
        "50": "#f5f3ff", "100": "#ede9fe", "200": "#ddd6fe", "300": "#c4b5fd",
        "400": "#a78bfa", "500": "#8b5cf6", "600": "#7c3aed", "700": "#6d28d9",
        "800": "#5b21b6", "900": "#4c1d95", "950": "#2e1065"
    },
    
    # Purple
    "purple": {
        "50": "#faf5ff", "100": "#f3e8ff", "200": "#e9d5ff", "300": "#d8b4fe",
        "400": "#c084fc", "500": "#a855f7", "600": "#9333ea", "700": "#7e22ce",
        "800": "#6b21a8", "900": "#581c87", "950": "#3b0764"
    },
    
    # Fuchsia
    "fuchsia": {
        "50": "#fdf4ff", "100": "#fae8ff", "200": "#f5d0fe", "300": "#f0abfc",
        "400": "#e879f9", "500": "#d946ef", "600": "#c026d3", "700": "#a21caf",
        "800": "#86198f", "900": "#701a75", "950": "#4a044e"
    },
    
    # Pink
    "pink": {
        "50": "#fdf2f8", "100": "#fce7f3", "200": "#fbcfe8", "300": "#f9a8d4",
        "400": "#f472b6", "500": "#ec4899", "600": "#db2777", "700": "#be185d",
        "800": "#9d174d", "900": "#831843", "950": "#500724"
    },
    
    # Rose
    "rose": {
        "50": "#fff1f2", "100": "#ffe4e6", "200": "#fecdd3", "300": "#fda4af",
        "400": "#fb7185", "500": "#f43f5e", "600": "#e11d48", "700": "#be123c",
        "800": "#9f1239", "900": "#881337", "950": "#4c0519"
    },
}

def _get_color(v: str) -> str:
    # Handle arbitrary color: bg-[#f00]
    if v.startswith('[') and v.endswith(']'):
        return v[1:-1]
    
    # Handle palette colors: red-500
    parts = v.split('-')
    if len(parts) >= 2:
        color = '-'.join(parts[:-1])  # Handle multi-part colors like "light-blue"
        shade = parts[-1]
        if color in _COLORS and isinstance(_COLORS[color], dict) and shade in _COLORS[color]:
            return _COLORS[color][shade]
    if len(parts) == 1:
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
            # Handle multiple properties (like truncate)
            if ';' in prop_val:
                for prop_val_pair in prop_val.split(';'):
                    if ':' in prop_val_pair:
                        prop, val = prop_val_pair.split(':', 1)
                        styles[prop.strip()] = val.strip()
            else:
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
