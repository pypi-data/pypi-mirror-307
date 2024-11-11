# Pyglet CornerPin

This is a little utility that adds corner pin transforms to a pyglet window.

## Installation

```bash
pip install pyglet-cornerpin
```

## Usage

Create instance for a window, and register the event handlers for dragging the pins. A `on_key_release` is also registered to handle keyboard controls to move the pins.


```python

pins = PygletCornerPin(window)
# event handlers for dragging:
window.push_handlers(pins)
```

Then you can draw the pins in your `on_draw()` event.

```python
@window.event
def on_draw():
    window.clear()
    ...
    # draw corner pins
    pins.draw()
```


Optionally you can provide initial positions for the pins.

```python
corners = [
    (0, 0),                        # Bottom left
    (window.width),                # Bottom right
    (0, window.height),            # Top left
    (window.width, window.height), # Top right
]
pins = PygletCornerPin(window, corners)

```

Run [pattern.py](examples/pattern.py) in the examples folder for a demo.

To use the keyboard, select a pin with number keys 1-4, the use the arrow keys (optionally with ctrl/shift modifier) to move the handle.
