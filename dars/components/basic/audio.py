from typing import Optional, Dict, Any

from dars.core.component import Component


class Audio(Component):
    """
    Advanced HTML5 audio component for playing sound files.
    
    Props:
    - **src** (str): URL or path to the audio source.
    - **controls** (bool): Whether to display audio controls (play/pause, volume, etc.).
    - **autoplay** (bool): If True, the audio will start playing automatically.
    - **loop** (bool): If True, the audio will play in a loop.
    - **muted** (bool): If True, the audio will be muted by default.
    - **preload** (str): Strategy for preloading ('auto', 'metadata', 'none').
    - **id** (str): Unique identifier for the component.
    - **class_name** (str): String containing CSS utility classes.
    - **style** (dict): Optional dictionary for direct inline styles (prefer `class_name`).
    - **children** (list): List of child components.
    - **Events**: Handlers like `on_play`, `on_pause`, `on_ended`, etc.
    
    Example:
    ```python
    Audio(
        src="https://example.com/podcast.mp3",
        controls=True,
        class_name="w-full max-w-md"
    )
    ```
    """

    def __init__(
        self,
        src: str,
        controls: bool = True,
        autoplay: bool = False,
        loop: bool = False,
        muted: bool = False,
        preload: Optional[str] = None,
        class_name: Optional[str] = None,
        style: Optional[Dict[str, Any]] = None,
        attrs: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(class_name=class_name, style=style, **kwargs)
        self.src = src
        self.controls = controls
        self.autoplay = autoplay
        self.loop = loop
        self.muted = muted
        self.preload = preload
        self.extra_attrs = attrs or {}

    def render(self) -> str:
        raise NotImplementedError("El método render debe ser implementado por el exportador")
