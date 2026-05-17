from dars.core.component import Component
from dars.core.events import EventTypes
from typing import Optional, Dict, Any, Callable, List, Union


class FileUpload(Component):
    """
    File selection and upload component.

    Wraps ``<input type="file">`` and optionally wires a ``network_request``
    DAP action that POSTs the selected file to *upload_url* as
    ``multipart/form-data``.

    Props:
    - **accept** (str): Allowed file types (e.g. ``"image/*"``, ``".pdf"``).
    - **multiple** (bool): Allow selecting multiple files.
    - **disabled** (bool): Disable the input.
    - **required** (bool): Mark the field as required.
    - **max_size** (int): Legacy max-size in bytes (kept for backward compat).
    - **label** (str): Button label (default ``"Choose File"``).
    - **upload_url** (str): Endpoint to POST the file to (default ``"/api/upload"``).
    - **accepted_types** (list[str]): MIME types for the HTML ``accept`` attribute.
    - **max_size_bytes** (int): Client-side size limit; triggers *on_upload_error*
      before any network request when exceeded.
    - **on_upload_complete** (dScript): Executed after a successful upload response.
    - **on_upload_error** (dScript): Executed on upload failure or size violation.
    - **on_change**: Low-level change handler (use *on_upload_complete* for uploads).

    Example::

        FileUpload(
            accepted_types=["image/png", "image/jpeg"],
            max_size_bytes=5 * 1024 * 1024,
            upload_url="/api/upload",
            on_upload_complete=alert("Upload complete!"),
            on_upload_error=alert("Upload failed"),
        )
    """

    def __init__(
        self,
        accept: Optional[str] = None,
        multiple: bool = False,
        disabled: bool = False,
        required: bool = False,
        max_size: Optional[int] = None,
        label: Optional[str] = "Choose File",
        # Upload pipeline props
        upload_url: str = "/api/upload",
        accepted_types: Optional[List[str]] = None,
        max_size_bytes: Optional[int] = None,
        on_upload_complete=None,
        on_upload_error=None,
        # Standard props
        id: Optional[str] = None,
        class_name: Optional[str] = None,
        style: Optional[Dict[str, Any]] = None,
        on_change: Optional[Callable] = None,
        **props,
    ):
        super().__init__(id=id, class_name=class_name, style=style, **props)
        self.accept = accept
        self.multiple = multiple
        self.disabled = disabled
        self.required = required
        self.max_size = max_size
        self.label = label

        # Upload pipeline
        self.upload_url = upload_url
        self.accepted_types = accepted_types or []
        self.max_size_bytes = max_size_bytes
        self.on_upload_complete = on_upload_complete
        self.on_upload_error = on_upload_error

        if on_change:
            self.set_event(EventTypes.CHANGE, on_change)

    def render(self, exporter: Any) -> str:
        raise NotImplementedError("render method must be implemented by exporter")
