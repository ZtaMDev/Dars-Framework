from typing import Optional, Dict, Any

from dars.core.component import Component


class Video(Component):
    """
    Advanced HTML5 video component for embedding and controlling video content.
    
    Props:
    - **src** (str): URL or path to the video source.
    - **poster** (str): URL of an image to be shown while the video is downloading.
    - **width** (str): Width of the video player.
    - **height** (str): Height of the video player.
    - **controls** (bool): Whether to display video controls.
    - **autoplay** (bool): If True, the video starts playing automatically.
    - **loop** (bool): If True, the video plays in a loop.
    - **muted** (bool): If True, the audio is muted by default.
    - **preload** (str): Preload strategy (`"auto"`, `"metadata"`, `"none"`).
    - **plays_inline** (bool): If True, the video plays inline on mobile browsers.
    - **id** (str): Unique identifier for the component.
    - **class_name** (str): String containing regular CSS class names.
    - **style** (dict): Optional dictionary for CSS utility classes (prefer `style`).
    - **children** (list): List of child components.
    - **Events**: Handlers like `on_play`, `on_pause`, `on_ended`, etc.
    
    Example:
    ```python
    Video(
        src="https://example.com/demo.mp4",
        poster="https://example.com/thumb.jpg",
        class_name="w-full max-w-4xl rounded-2xl shadow-xl border-4 border-white"
    )
    ```
    """

    def __init__(
        self,
        src: str,
        poster: Optional[str] = None,
        width: Optional[str] = None,
        height: Optional[str] = None,
        controls: bool = True,
        autoplay: bool = False,
        loop: bool = False,
        muted: bool = False,
        preload: Optional[str] = None,
        plays_inline: bool = True,
        class_name: Optional[str] = None,
        style: Optional[Dict[str, Any]] = None,
        attrs: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> None:
        # attrs: extra raw attributes to allow advanced customization
        super().__init__(class_name=class_name, style=style, **kwargs)
        self.src = src
        self.poster = poster
        self.width = width
        self.height = height
        self.controls = controls
        self.autoplay = autoplay
        self.loop = loop
        self.muted = muted
        self.preload = preload
        self.plays_inline = plays_inline
        self.extra_attrs = attrs or {}

    def render(self) -> str:
        raise NotImplementedError("El método render debe ser implementado por el exportador")