# State V2 Example Template

A professional, production-ready demonstration of Dars Framework's State V2 system.

## Features Demonstrated

### Pure Pythonic State API
```python
counter = State(display, text=0)
increment_btn.on_click = counter.text.increment(by=1)
```

### Auto Operations
```python
timer = State(display, text=0)
start_btn.on_click = timer.text.auto_increment(by=1, interval=1000)
stop_btn.on_click = timer.text.stop_auto()
```

### Animation System
```python
button.on_click = sequence(
    fadeIn(id="box"),
    pulse(id="box", scale=1.1),
    shake(id="box")
)
```

## Components

- `hero_component.py` - Hero section with title and description
- `counter_component.py` - Interactive counter with increment/decrement
- `timer_component.py` - Auto-incrementing timer demonstration
- `animation_component.py` - Animation system showcase with 15+ animations
- `main.py` - Main application file
- `styles.css` - Global styles and responsive design

## Running

```bash
cd dars/templates/examples/advanced/StateV2
python main.py
```

## Structure

This template follows best practices:
- Function components for reusability
- Clean separation of concerns
- Responsive design
- Professional styling
- Comprehensive documentation
