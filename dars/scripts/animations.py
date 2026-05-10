# Dars Framework - Core Source File
#
# This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0.
# If a copy of the MPL was not distributed with this file, You can obtain one at
# https://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2025 ZtaDev
"""
Dars Framework Animation Utilities

Provides a comprehensive set of animation functions following the utils_ds.py pattern.
All functions return dScript objects that can be chained with .then() for complex animations.

Usage:
    from dars.all import fadeIn, pulse, sequence
    
    button.on_click = fadeIn(id="modal", duration=500)
    button.on_click = sequence(fadeIn(id="box1"), slideIn(id="box2"), pulse(id="box3"))
"""

from dars.scripts.dscript import dScript
from dars.actionProtocol import Action
from typing import Union, List


# ============= FADE ANIMATIONS =============

def fadeIn(id: str, duration: int = 300, easing: str = "ease") -> dScript:
    """Fade in an element with secure DAP."""
    return dScript(data=Action.sequence([
        Action.dom_set_style(id, {"transition": "none", "opacity": "0", "display": "block"}),
        Action.dom_reflow(id),
        Action.delay(ms=20),
        Action.dom_set_style(id, {"transition": f"opacity {duration}ms {easing}", "opacity": "1"}),
        Action.delay(ms=duration)
    ]))


def fadeOut(id: str, duration: int = 300, easing: str = "ease", hide: bool = True) -> dScript:
    """Fade out an element with secure DAP."""
    sequence = [
        Action.dom_set_style(id, {"transition": f"opacity {duration}ms {easing}", "opacity": "0"}),
        Action.delay(ms=duration)
    ]
    if hide:
        sequence.append(Action.dom_hide(id))
    
    return dScript(data=Action.sequence(sequence))


# ============= SLIDE ANIMATIONS =============

def slideIn(id: str, direction: str = "down", duration: int = 300, easing: str = "ease") -> dScript:
    """Slide in an element with secure DAP."""
    transforms = {
        'up': 'translateY(100%)',
        'down': 'translateY(-100%)',
        'left': 'translateX(100%)',
        'right': 'translateX(-100%)'
    }
    initial_transform = transforms.get(direction, 'translateY(-100%)')
    
    return dScript(data=Action.sequence([
        Action.dom_set_style(id, {"transition": "none", "transform": initial_transform, "display": "block"}),
        Action.dom_reflow(id),
        Action.delay(ms=20),
        Action.dom_set_style(id, {"transition": f"transform {duration}ms {easing}", "transform": "translateX(0) translateY(0)"}),
        Action.delay(ms=duration)
    ]))


def slideOut(id: str, direction: str = "up", duration: int = 300, easing: str = "ease", hide: bool = True) -> dScript:
    """Slide out an element with secure DAP."""
    transforms = {
        'up': 'translateY(-100%)',
        'down': 'translateY(100%)',
        'left': 'translateX(-100%)',
        'right': 'translateX(100%)'
    }
    final_transform = transforms.get(direction, 'translateY(-100%)')
    
    sequence = [
        Action.dom_set_style(id, {"transition": f"transform {duration}ms {easing}", "transform": final_transform}),
        Action.delay(ms=duration)
    ]
    if hide:
        sequence.append(Action.dom_hide(id))
        
    return dScript(data=Action.sequence(sequence))


# ============= SCALE ANIMATIONS =============

def scaleIn(id: str, duration: int = 300, easing: str = "ease", from_scale: float = 0.0) -> dScript:
    """Scale in an element with secure DAP."""
    return dScript(data=Action.sequence([
        Action.dom_set_style(id, {"transition": "none", "transform": f"scale({from_scale})", "opacity": "0", "display": "block"}),
        Action.dom_reflow(id),
        Action.delay(ms=20),
        Action.dom_set_style(id, {"transition": f"transform {duration}ms {easing}, opacity {duration}ms {easing}", "transform": "scale(1)", "opacity": "1"}),
        Action.delay(ms=duration)
    ]))


def scaleOut(id: str, duration: int = 300, easing: str = "ease", to_scale: float = 0.0, hide: bool = True) -> dScript:
    """Scale out an element with secure DAP."""
    sequence = [
        Action.dom_set_style(id, {"transition": f"transform {duration}ms {easing}, opacity {duration}ms {easing}", "transform": f"scale({to_scale})", "opacity": "0"}),
        Action.delay(ms=duration)
    ]
    if hide:
        sequence.append(Action.dom_hide(id))
        
    return dScript(data=Action.sequence(sequence))


# ============= ATTENTION ANIMATIONS =============

def shake(id: str, intensity: int = 5, duration: int = 500) -> dScript:
    """Shake an element horizontally (secure DAP)."""
    keyframes = [
        {"transform": "translateX(0)"},
        {"transform": f"translateX(-{intensity}px)"},
        {"transform": f"translateX({intensity}px)"},
        {"transform": f"translateX(-{intensity}px)"},
        {"transform": f"translateX({intensity}px)"},
        {"transform": "translateX(0)"}
    ]
    return dScript(data=Action.dom_animate(id, keyframes, {"duration": duration, "easing": "ease-in-out"}))


def bounce(id: str, distance: int = 20, duration: int = 600) -> dScript:
    """Bounce an element vertically (secure DAP)."""
    keyframes = [
        {"transform": "translateY(0)"},
        {"transform": f"translateY(-{distance}px)"},
        {"transform": "translateY(0)"},
        {"transform": f"translateY(-{distance//2}px)"},
        {"transform": "translateY(0)"}
    ]
    return dScript(data=Action.dom_animate(id, keyframes, {
        "duration": duration,
        "easing": "cubic-bezier(0.68, -0.55, 0.265, 1.55)"
    }))


def pulse(id: str, scale: float = 1.1, duration: int = 400, iterations: Union[int, str] = 1) -> dScript:
    """Pulse an element (secure DAP)."""
    iter_value = 1000000 if iterations == 'infinite' else iterations # DAP should handle 'Infinity' but let's be safe
    keyframes = [
        {"transform": "scale(1)"},
        {"transform": f"scale({scale})"},
        {"transform": "scale(1)"}
    ]
    return dScript(data=Action.dom_animate(id, keyframes, {
        "duration": duration,
        "iterations": iter_value,
        "easing": "ease-in-out"
    }))


# ============= ROTATION ANIMATIONS =============

def rotate(id: str, degrees: int = 360, duration: int = 500, easing: str = "ease") -> dScript:
    """Rotate an element (secure DAP)."""
    return dScript(data=Action.sequence([
        Action.dom_set_style(id, {"transition": f"transform {duration}ms {easing}", "transform": f"rotate({degrees}deg)"}),
        Action.delay(ms=duration)
    ]))


def flip(id: str, axis: str = "y", duration: int = 600) -> dScript:
    """Flip an element (secure DAP)."""
    axis_upper = axis.upper()
    keyframes = [
        {"transform": f"rotate{axis_upper}(0deg)"},
        {"transform": f"rotate{axis_upper}(180deg)"}
    ]
    return dScript(data=Action.dom_animate(id, keyframes, {
        "duration": duration,
        "easing": "ease-in-out",
        "fill": "forwards"
    }))


# ============= COLOR & SIZE ANIMATIONS =============

def colorChange(id: str, from_color: str, to_color: str, duration: int = 500, property: str = "background-color") -> dScript:
    """Transition a color property (secure DAP)."""
    # Convert property to camelCase for JavaScript
    prop_parts = property.split('-')
    prop_camel = prop_parts[0] + ''.join(p.capitalize() for p in prop_parts[1:])
    
    return dScript(data=Action.sequence([
        Action.dom_set_style(id, {"transition": "none", prop_camel: from_color}),
        Action.dom_reflow(id),
        Action.delay(ms=20),
        Action.dom_set_style(id, {"transition": f"{property} {duration}ms ease", prop_camel: to_color}),
        Action.delay(ms=duration)
    ]))


def morphSize(id: str, to_width: str, to_height: str, duration: int = 500, easing: str = "ease") -> dScript:
    """Morph element size (secure DAP)."""
    return dScript(data=Action.sequence([
        Action.dom_set_style(id, {"transition": f"width {duration}ms {easing}, height {duration}ms {easing}", "width": to_width, "height": to_height}),
        Action.dom_reflow(id),
        Action.delay(ms=duration)
    ]))


# ============= COMPOSITE ANIMATIONS =============

def popIn(id: str, duration: int = 400) -> dScript:
    """
    Pop-in animation (scale + fade combination).
    
    Args:
        id: Element ID to animate
        duration: Animation duration in milliseconds
        
    Example:
        Button("Show Notification", on_click=popIn(id="notification"))
    """
    return scaleIn(id, duration=duration, from_scale=0.8)


def popOut(id: str, duration: int = 400) -> dScript:
    """
    Pop-out animation (scale + fade combination).
    
    Args:
        id: Element ID to animate
        duration: Animation duration in milliseconds
        
    Example:
        Button("Hide Notification", on_click=popOut(id="notification"))
    """
    return scaleOut(id, duration=duration, to_scale=0.8)


# ============= CHAINED ANIMATIONS =============

def sequence(*animations: dScript) -> dScript:
    """
    Execute animations in sequence (secure DAP).
    """
    if not animations:
        return dScript(data=Action.sequence([]))
    
    actions = []
    for anim in animations:
        act = anim.get_action()
        if act:
            actions.append(act)
        else:
            # Fallback for legacy code
            actions.append({"op": "inline", "args": {"code": anim.get_code()}})
            
    return dScript(data=Action.sequence(actions))
