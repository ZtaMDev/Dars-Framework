# Dars Animation System

Dars provides a powerful and easy-to-use animation system built on top of the Web Animations API. It allows you to add professional-grade animations to your components with simple Python function calls.

## Animation Overview

All animations in Dars are **dScript** objects. This means they:
- Run entirely on the client side (zero latency)
- Can be assigned to any event handler (`on_click`, `on_mouseover`, etc.)
- Can be chained together using `.then()` or the `sequence()` helper
- Return Promises, allowing for complex orchestration

## Animation Quick Start

```python
from dars.all import *

# Simple fade in
button.on_click = fadeIn(id="my-element")

# Chain animations
button.on_click = sequence(
    fadeOut(id="old-panel"),
    fadeIn(id="new-panel")
)
```

## Animation Reference

### Fade Animations

Control visibility with opacity transitions.

#### `fadeIn(id, duration=300, easing="ease")`
Fades an element in from opacity 0 to 1. Sets `display: block` automatically.

```python
fadeIn(id="modal", duration=500)
```

#### `fadeOut(id, duration=300, easing="ease", hide=True)`
Fades an element out from current opacity to 0.
- `hide`: If `True` (default), sets `display: none` after animation completes.

```python
fadeOut(id="notification", duration=2000, hide=True)
```

### Slide Animations

Move elements into or out of view.

#### `slideIn(id, direction="down", duration=300, easing="ease")`
Slides an element into its final position.
- `direction`: `"up"`, `"down"`, `"left"`, `"right"` (from where it enters)

```python
slideIn(id="sidebar", direction="left", duration=400)
```

#### `slideOut(id, direction="up", duration=300, easing="ease", hide=True)`
Slides an element out of view.
- `direction`: `"up"`, `"down"`, `"left"`, `"right"` (to where it exits)

```python
slideOut(id="sidebar", direction="left", duration=400)
```

### Scale Animations

Zoom elements in and out.

#### `scaleIn(id, duration=300, easing="ease", from_scale=0.0)`
Scales an element up to its natural size (scale 1).
- `from_scale`: Starting scale factor (0.0 to 1.0)

```python
scaleIn(id="popup", from_scale=0.5)
```

#### `scaleOut(id, duration=300, easing="ease", to_scale=0.0, hide=True)`
Scales an element down.
- `to_scale`: Ending scale factor (0.0 to 1.0)

```python
scaleOut(id="popup", to_scale=0.0)
```

### Attention Seekers

Draw user attention to elements.

#### `shake(id, intensity=5, duration=500)`
Shakes an element horizontally. Great for error feedback.
- `intensity`: Shake distance in pixels.

```python
shake(id="login-form", intensity=10)
```

#### `bounce(id, distance=20, duration=600)`
Bounces an element vertically.
- `distance`: Bounce height in pixels.

```python
bounce(id="notification-icon", distance=15)
```

#### `pulse(id, scale=1.1, duration=400, iterations=1)`
Pulses an element (scales up and down).
- `scale`: Max scale during pulse.
- `iterations`: Number of pulses. Use `"infinite"` for continuous pulsing.

```python
# Single pulse
pulse(id="heart-icon")

# Continuous heartbeat
pulse(id="status-dot", iterations="infinite", duration=1000)
```

### Transformations

Rotate and flip elements.

#### `rotate(id, degrees=360, duration=500, easing="ease")`
Rotates an element.

```python
rotate(id="refresh-icon", degrees=180)
```

#### `flip(id, axis="y", duration=600)`
Flips an element 180 degrees around an axis.
- `axis`: `"x"` (horizontal flip) or `"y"` (vertical flip).

```python
flip(id="card", axis="y")
```

### Property Transitions

Animate specific CSS properties.

#### `colorChange(id, from_color, to_color, duration=500, property="background-color")`
Smoothly transitions a color property.

```python
colorChange(id="btn", from_color="#fff", to_color="#f00", property="background-color")
```

#### `morphSize(id, to_width, to_height, duration=500, easing="ease")`
Changes the dimensions of an element.

```python
morphSize(id="panel", to_width="100%", to_height="500px")
```

## Scroll & Viewport Animations

Dars provides a powerful, highly optimized Web Animations API-based engine for scroll and viewport-triggered animations. These run autonomously on the client, without `eval()` or string-execution vulnerabilities.

### `animateOnView(id, keyframes, duration=300, easing="ease", threshold=0.1, ...)`
Triggers an animation as soon as an element enters the viewport.
- `keyframes`: A list of dictionaries representing CSS properties (e.g., `[{"opacity": "0"}, {"opacity": "1"}]`).
- `threshold`: How much of the element must be visible (0.0 to 1.0) before triggering.
- `once`: If `True`, the animation only runs the first time it enters the viewport.

```python
# Fade and slide up when scrolled into view
index.add_script(animateOnView("my-card", [
    {"opacity": "0", "transform": "translateY(50px)"},
    {"opacity": "1", "transform": "translateY(0)"}
], duration=800, threshold=0.2))
```

### `staggerOnView(ids, keyframes, duration=300, stagger_delay=100, threshold=0.1, ...)`
Animates a list of elements sequentially with a delay as soon as the *first* element enters the viewport.
- `ids`: List of element IDs.
- `stagger_delay`: Milliseconds to wait between starting each element's animation.

```python
index.add_script(staggerOnView(
    ["card-1", "card-2", "card-3"],
    [{"opacity": "0", "transform": "scale(0.9)"},
     {"opacity": "1", "transform": "scale(1)"}],
    duration=500, stagger_delay=150
))
```

### `scrollProgress(id, property, from_val, to_val, unit="", start=0, end=1)`
Ties a CSS property directly to the page's scroll progress (0.0 = top of page, 1.0 = bottom).
- `property`: CSS property to animate (e.g., `"opacity"`, `"translateY"`).
- `start` / `end`: The scroll progress range where the animation occurs.

```python
# Fades out the hero section as the user scrolls down
index.add_script(scrollProgress("hero-section", "opacity", 1.0, 0.0, start=0, end=0.2))
```

### `runOnView(id, code, threshold=0.1, once=True)`
Executes arbitrary JavaScript code (via a secure callback mechanism) when an element enters the viewport.

```python
index.add_script(runOnView("trigger-zone", "console.log('User reached the bottom!');"))
```

## Chaining & Sequencing

You can run animations in sequence using the `sequence()` helper or the `.then()` method.

### Using `sequence()`

The easiest way to run animations one after another.

```python
from dars.all import sequence, fadeIn, slideIn

button.on_click = sequence(
    fadeIn(id="header"),
    slideIn(id="content", direction="up"),
    fadeIn(id="footer")
)
```

### Using `.then()`

For more granular control or branching logic.

```python
anim1 = fadeIn(id="box1")
anim2 = slideIn(id="box2")

# Run anim1, then anim2
button.on_click = anim1.then(anim2)
```

### Parallel Animations

To run animations simultaneously, simply trigger them in the same event handler (or use a list of handlers).

```python
# Both start at the same time
button.on_click = [
    fadeIn(id="box1"),
    slideIn(id="box2")
]
```
