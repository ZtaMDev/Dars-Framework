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
from typing import Union, List


# ============= FADE ANIMATIONS =============

def fadeIn(id: str, duration: int = 300, easing: str = "ease") -> dScript:
    """
    Fade in an element with CSS transition.
    
    Args:
        id: Element ID to animate
        duration: Animation duration in milliseconds
        easing: CSS easing function (ease, linear, ease-in, ease-out, ease-in-out, cubic-bezier)
        
    Example:
        Button("Show", on_click=fadeIn(id="modal", duration=500))
    """
    code = f"""
(async () => {{
const el = document.getElementById('{id}');
if (el) {{
    el.style.transition = 'none';
    el.style.opacity = '0';
    el.style.display = 'block';
    void el.offsetWidth; // Force reflow
    await new Promise(r => setTimeout(r, 20));
    el.style.transition = 'opacity {duration}ms {easing}';
    el.style.opacity = '1';
    await new Promise(r => setTimeout(r, {duration}));
}}
}})();
""".strip()
    return dScript(code)


def fadeOut(id: str, duration: int = 300, easing: str = "ease", hide: bool = True) -> dScript:
    """
    Fade out an element with CSS transition.
    
    Args:
        id: Element ID to animate
        duration: Animation duration in milliseconds
        easing: CSS easing function
        hide: If True, sets display=none after fade completes
        
    Example:
        Button("Hide", on_click=fadeOut(id="modal", duration=500))
    """
    hide_code = "el.style.display = 'none';" if hide else ""
    code = f"""
(async () => {{
const el = document.getElementById('{id}');
if (el) {{
    el.style.transition = 'opacity {duration}ms {easing}';
    el.style.opacity = '0';
    await new Promise(r => setTimeout(r, {duration}));
    {hide_code}
}}
}})();
""".strip()
    return dScript(code)


# ============= SLIDE ANIMATIONS =============

def slideIn(id: str, direction: str = "down", duration: int = 300, easing: str = "ease") -> dScript:
    """
    Slide in an element from a direction.
    
    Args:
        id: Element ID to animate
        direction: 'up', 'down', 'left', or 'right'
        duration: Animation duration in milliseconds
        easing: CSS easing function
        
    Example:
        Button("Slide Menu", on_click=slideIn(id="sidebar", direction="left"))
    """
    transforms = {
        'up': 'translateY(100%)',
        'down': 'translateY(-100%)',
        'left': 'translateX(100%)',
        'right': 'translateX(-100%)'
    }
    initial_transform = transforms.get(direction, 'translateY(-100%)')
    
    code = f"""
(async () => {{
const el = document.getElementById('{id}');
if (el) {{
    el.style.transition = 'none';
    el.style.transform = '{initial_transform}';
    el.style.display = 'block';
    void el.offsetWidth; // Force reflow
    await new Promise(r => setTimeout(r, 20));
    el.style.transition = 'transform {duration}ms {easing}';
    el.style.transform = 'translateX(0) translateY(0)';
    await new Promise(r => setTimeout(r, {duration}));
}}
}})();
""".strip()
    return dScript(code)


def slideOut(id: str, direction: str = "up", duration: int = 300, easing: str = "ease", hide: bool = True) -> dScript:
    """
    Slide out an element to a direction.
    
    Args:
        id: Element ID to animate
        direction: 'up', 'down', 'left', or 'right'
        duration: Animation duration in milliseconds
        easing: CSS easing function
        hide: If True, sets display=none after slide completes
        
    Example:
        Button("Close", on_click=slideOut(id="sidebar", direction="left"))
    """
    transforms = {
        'up': 'translateY(-100%)',
        'down': 'translateY(100%)',
        'left': 'translateX(-100%)',
        'right': 'translateX(100%)'
    }
    final_transform = transforms.get(direction, 'translateY(-100%)')
    hide_code = "el.style.display = 'none';" if hide else ""
    
    code = f"""
(async () => {{
const el = document.getElementById('{id}');
if (el) {{
    el.style.transition = 'transform {duration}ms {easing}';
    el.style.transform = '{final_transform}';
    await new Promise(r => setTimeout(r, {duration}));
    {hide_code}
}}
}})();
""".strip()
    return dScript(code)


# ============= SCALE ANIMATIONS =============

def scaleIn(id: str, duration: int = 300, easing: str = "ease", from_scale: float = 0.0) -> dScript:
    """
    Scale in an element from a smaller size.
    
    Args:
        id: Element ID to animate
        duration: Animation duration in milliseconds
        easing: CSS easing function
        from_scale: Starting scale (0.0 to 1.0)
        
    Example:
        Button("Pop In", on_click=scaleIn(id="notification", from_scale=0.5))
    """
    code = f"""
(async () => {{
const el = document.getElementById('{id}');
if (el) {{
    el.style.transition = 'none';
    el.style.transform = 'scale({from_scale})';
    el.style.opacity = '0';
    el.style.display = 'block';
    void el.offsetWidth; // Force reflow
    await new Promise(r => setTimeout(r, 20));
    el.style.transition = 'transform {duration}ms {easing}, opacity {duration}ms {easing}';
    el.style.transform = 'scale(1)'; 
    el.style.opacity = '1'; 
    await new Promise(r => setTimeout(r, {duration}));
}}
}})();
""".strip()
    return dScript(code)


def scaleOut(id: str, duration: int = 300, easing: str = "ease", to_scale: float = 0.0, hide: bool = True) -> dScript:
    """
    Scale out an element to a smaller size.
    
    Args:
        id: Element ID to animate
        duration: Animation duration in milliseconds
        easing: CSS easing function
        to_scale: Ending scale (0.0 to 1.0)
        hide: If True, sets display=none after animation
        
    Example:
        Button("Pop Out", on_click=scaleOut(id="notification"))
    """
    hide_code = "el.style.display = 'none';" if hide else ""
    code = f"""
(async () => {{
const el = document.getElementById('{id}');
if (el) {{
    el.style.transition = 'transform {duration}ms {easing}, opacity {duration}ms {easing}';
    el.style.transform = 'scale({to_scale})';
    el.style.opacity = '0';
    await new Promise(r => setTimeout(r, {duration}));
    {hide_code}
}}
}})();
""".strip()
    return dScript(code)


# ============= ATTENTION ANIMATIONS =============

def shake(id: str, intensity: int = 5, duration: int = 500) -> dScript:
    """
    Shake an element horizontally (error/attention effect).
    
    Args:
        id: Element ID to animate
        intensity: Shake intensity in pixels
        duration: Total animation duration in milliseconds
        
    Example:
        Button("Shake", on_click=shake(id="error-message", intensity=10))
    """
    code = f"""
(async () => {{
const el = document.getElementById('{id}');
if (el) {{
    const originalTransform = el.style.transform || '';
    const keyframes = [
        {{ transform: 'translateX(0)' }},
        {{ transform: 'translateX(-{intensity}px)' }},
        {{ transform: 'translateX({intensity}px)' }},
        {{ transform: 'translateX(-{intensity}px)' }},
        {{ transform: 'translateX({intensity}px)' }},
        {{ transform: 'translateX(0)' }}
    ];
    const animation = el.animate(keyframes, {{
        duration: {duration},
        easing: 'ease-in-out'
    }});
    await animation.finished;
    el.style.transform = originalTransform;
}}
}})();
""".strip()
    return dScript(code)


def bounce(id: str, distance: int = 20, duration: int = 600) -> dScript:
    """
    Bounce an element vertically.
    
    Args:
        id: Element ID to animate
        distance: Bounce distance in pixels
        duration: Total animation duration in milliseconds
        
    Example:
        Button("Bounce", on_click=bounce(id="notification"))
    """
    code = f"""
(async () => {{
const el = document.getElementById('{id}');
if (el) {{
    const originalTransform = el.style.transform || '';
    const keyframes = [
        {{ transform: 'translateY(0)' }},
        {{ transform: 'translateY(-{distance}px)' }},
        {{ transform: 'translateY(0)' }},
        {{ transform: 'translateY(-{distance//2}px)' }},
        {{ transform: 'translateY(0)' }}
    ];
    const animation = el.animate(keyframes, {{
        duration: {duration},
        easing: 'cubic-bezier(0.68, -0.55, 0.265, 1.55)'
    }});
    await animation.finished;
    el.style.transform = originalTransform;
}}
}})();
""".strip()
    return dScript(code)


def pulse(id: str, scale: float = 1.1, duration: int = 400, iterations: Union[int, str] = 1) -> dScript:
    """
    Pulse an element (scale up and down).
    
    Args:
        id: Element ID to animate
        scale: Maximum scale during pulse
        duration: Duration of one pulse cycle in milliseconds
        iterations: Number of times to pulse (use 'infinite' for continuous)
        
    Example:
        Button("Pulse", on_click=pulse(id="button", scale=1.2, iterations=3))
    """
    iter_value = "Infinity" if iterations == 'infinite' else str(iterations)
    code = f"""
(async () => {{
const el = document.getElementById('{id}');
if (el) {{
    const originalTransform = el.style.transform || '';
    const keyframes = [
        {{ transform: 'scale(1)' }},
        {{ transform: 'scale({scale})' }},
        {{ transform: 'scale(1)' }}
    ];
    const animation = el.animate(keyframes, {{
        duration: {duration},
        iterations: {iter_value},
        easing: 'ease-in-out'
    }});
    await animation.finished;
    el.style.transform = originalTransform;
}}
}})();
""".strip()
    return dScript(code)


# ============= ROTATION ANIMATIONS =============

def rotate(id: str, degrees: int = 360, duration: int = 500, easing: str = "ease") -> dScript:
    """
    Rotate an element by specified degrees.
    
    Args:
        id: Element ID to animate
        degrees: Rotation angle in degrees
        duration: Animation duration in milliseconds
        easing: CSS easing function
        
    Example:
        Button("Rotate", on_click=rotate(id="icon", degrees=180))
    """
    code = f"""
(async () => {{
const el = document.getElementById('{id}');
if (el) {{
    const currentRotation = getComputedStyle(el).transform;
    el.style.transition = 'transform {duration}ms {easing}';
    el.style.transform = 'rotate({degrees}deg)';
    await new Promise(r => setTimeout(r, {duration}));
}}
}})();
""".strip()
    return dScript(code)


def flip(id: str, axis: str = "y", duration: int = 600) -> dScript:
    """
    Flip an element on X or Y axis.
    
    Args:
        id: Element ID to animate
        axis: 'x' for horizontal flip, 'y' for vertical flip
        duration: Animation duration in milliseconds
        
    Example:
        Button("Flip Card", on_click=flip(id="card", axis="y"))
    """
    axis_upper = axis.upper()
    code = f"""
(async () => {{
const el = document.getElementById('{id}');
if (el) {{
    const keyframes = [
        {{ transform: 'rotate{axis_upper}(0deg)' }},
        {{ transform: 'rotate{axis_upper}(180deg)' }}
    ];
    const animation = el.animate(keyframes, {{
        duration: {duration},
        easing: 'ease-in-out',
        fill: 'forwards'
    }});
    await animation.finished;
}}
}})();
""".strip()
    return dScript(code)


# ============= COLOR & SIZE ANIMATIONS =============

def colorChange(id: str, from_color: str, to_color: str, duration: int = 500, property: str = "background-color") -> dScript:
    """
    Transition a color property from one value to another.
    
    Args:
        id: Element ID to animate
        from_color: Starting color (CSS color value)
        to_color: Ending color (CSS color value)
        duration: Animation duration in milliseconds
        property: CSS property to animate ('background-color', 'color', 'border-color', etc.)
        
    Example:
        Button("Change Color", on_click=colorChange(
            id="box", 
            from_color="#ff0000", 
            to_color="#00ff00",
            property="background-color"
        ))
    """
    # Convert property to camelCase for JavaScript
    prop_camel = property.replace('-', '')
    if '-' in property:
        parts = property.split('-')
        prop_camel = parts[0] + ''.join(p.capitalize() for p in parts[1:])
    
    code = f"""
(async () => {{
const el = document.getElementById('{id}');
if (el) {{
    el.style.transition = 'none';
    el.style.{prop_camel} = '{from_color}';
    void el.offsetWidth; // Force reflow
    await new Promise(r => setTimeout(r, 20));
    el.style.transition = '{property} {duration}ms ease';
    el.style.{prop_camel} = '{to_color}'; 
    await new Promise(r => setTimeout(r, {duration}));
}}
}})();
""".strip()
    return dScript(code)


def morphSize(id: str, to_width: str, to_height: str, duration: int = 500, easing: str = "ease") -> dScript:
    """
    Morph element size to new dimensions.
    
    Args:
        id: Element ID to animate
        to_width: Target width (CSS value like '200px', '50%', etc.)
        to_height: Target height (CSS value)
        duration: Animation duration in milliseconds
        easing: CSS easing function
        
    Example:
        Button("Expand", on_click=morphSize(id="box", to_width="300px", to_height="200px"))
    """
    code = f"""
(async () => {{
const el = document.getElementById('{id}');
if (el) {{
    el.style.transition = 'width {duration}ms {easing}, height {duration}ms {easing}';
    el.style.width = '{to_width}';
    el.style.height = '{to_height}';
    void el.offsetWidth; // Force reflow
    await new Promise(r => setTimeout(r, {duration}));
}}
}})();
""".strip()
    return dScript(code)


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
    Execute animations in sequence using .then() chaining.
    
    Args:
        *animations: Variable number of dScript animation objects
        
    Example:
        Button("Sequence", on_click=sequence(
            fadeIn(id="box1"),
            slideIn(id="box2"),
            pulse(id="box3")
        ))
    """
    if not animations:
        return dScript("")
    
    # Chain promises: anim1.then(() => anim2).then(() => anim3)
    code = animations[0].code
    for anim in animations[1:]:
        # Remove trailing semicolon if present to allow .then() chaining
        if code.strip().endswith(';'):
            code = code.strip()[:-1]
        code = f"{code}.then(() => {{ {anim.code} }})"
    return dScript(code)
