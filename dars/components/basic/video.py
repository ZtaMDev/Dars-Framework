from typing import Optional, Dict, Any

from dars.core.component import Component


class Video(Component):
    """Advanced HTML5 video component.

    Highly customizable wrapper around the <video> element.
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