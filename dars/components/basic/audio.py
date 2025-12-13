from typing import Optional, Dict, Any

from dars.core.component import Component


class Audio(Component):
    """Advanced HTML5 audio component.

    Highly customizable wrapper around the <audio> element.
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
