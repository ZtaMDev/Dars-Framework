from typing import Any, Callable, Dict, Optional, cast

from dars.core.component import Component
from dars.core.events import EventTypes
from dars.core.properties import StyleProps
from dars.scripts.script import Script


class Button(Component):
    """
    Interactive button component that triggers actions when clicked.

    Props:
    - **text** (str): The label text displayed on the button.
    - **disabled** (bool): Whether the button is interactive or not.
    - **button_type** (str): HTML type of the button ('button', 'submit', 'reset').
    - **id** (str): Unique identifier for the component.
    - **class_name** (str): String containing regular CSS class names.
    - **style** (dict): Optional dictionary for CSS utility classes (prefer `style`).
    - **children** (list): List of child components to render inside the button.
    - **Events**: Handlers like `on_click`, `on_double_click`, `on_mouse_enter`, `on_mouse_leave`, `on_mouse_down`, `on_mouse_up`, `on_key_down`, `on_key_up`.

    Example:
    ```python
    Button(
        text="Click me!",
        class_name="bg-indigo-600 text-white px-4 py-2 rounded shadow-md hover:shadow-lg transition-all",
        on_click=log("Button clicked!")
    )
    ```
    """

    def __init__(
        self,
        text: Any = "Button",
        id: Any = None,
        class_name: Any = None,
        style: Optional[Dict[str, Any] | str] = None,
        hover_style: Optional[Dict[str, Any] | str] = None,
        disabled: bool = False,
        button_type: Any = "button",  # "button", "submit", "reset"
        on_click: Any = None,
        on_double_click: Any = None,
        on_mouse_enter: Any = None,
        on_mouse_leave: Any = None,
        on_mouse_down: Optional[Callable] = None,
        on_mouse_up: Optional[Callable] = None,
        on_key_down: Optional[Callable] = None,
        on_key_up: Optional[Callable] = None,
        **props,
    ):
        super().__init__(
            id=id, class_name=class_name, style=style, hover_style=hover_style, **props
        )
        self.text = text
        self.disabled = disabled
        self.button_type = button_type

        # Soporte para presets JS editables con dScript u otros Script
        if on_click:
            # Convertir a Script si es necesario
            if not isinstance(on_click, Script) and callable(on_click):
                from dars.scripts.dscript import dScript

                on_click = dScript(cast(Any, on_click.__code__))
            self.set_event(EventTypes.CLICK, on_click)
        if on_double_click:
            self.set_event(EventTypes.DOUBLE_CLICK, on_double_click)
        if on_mouse_enter:
            self.set_event(EventTypes.MOUSE_ENTER, on_mouse_enter)
        if on_mouse_leave:
            self.set_event(EventTypes.MOUSE_LEAVE, on_mouse_leave)
        if on_mouse_down:
            self.set_event(EventTypes.MOUSE_DOWN, on_mouse_down)
        if on_mouse_up:
            self.set_event(EventTypes.MOUSE_UP, on_mouse_up)
        if on_key_down:
            self.set_event(EventTypes.KEY_DOWN, on_key_down)
        if on_key_up:
            self.set_event(EventTypes.KEY_UP, on_key_up)

    def render(self, exporter: Any) -> str:
        # El método render será implementado por cada exportador
        raise NotImplementedError(
            "El método render debe ser implementado por el exportador"
        )
