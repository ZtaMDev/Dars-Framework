# Dars Framework - Core Source File
#
# This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0.
# If a copy of the MPL was not distributed with this file, You can obtain one at
# https://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2025 ZtaDev
"""
UploadPipeline — server-side file upload handler.

Validates MIME type and size, sanitises the filename, saves the file, and
returns a JSON response with the relative URL.

Example::

    from fastapi import FastAPI
    from dars.backend.upload import UploadPipeline

    app = FastAPI()
    pipeline = UploadPipeline(
        upload_dir="uploads",
        allowed_types=["image/png", "image/jpeg"],
        max_size_bytes=5 * 1024 * 1024,
    )
    pipeline.create_endpoint(app, path="/api/upload")
"""

import os
import re
from typing import Callable, List, Optional

from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse


class UploadPipeline:
    """
    Server-side file upload handler.

    Args:
        upload_dir: Directory where uploaded files are saved.
        allowed_types: Allowed MIME types.  ``None`` means all types accepted.
        max_size_bytes: Maximum file size in bytes.  ``None`` means no limit.
        rename_fn: Optional callable ``(original_filename: str) -> str`` that
                   returns the filename to use when saving.  Defaults to the
                   sanitised original filename.
    """

    def __init__(
        self,
        upload_dir: str,
        allowed_types: Optional[List[str]] = None,
        max_size_bytes: Optional[int] = None,
        rename_fn: Optional[Callable[[str], str]] = None,
    ) -> None:
        self.upload_dir = upload_dir
        self.allowed_types = allowed_types
        self.max_size_bytes = max_size_bytes
        self.rename_fn = rename_fn

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def create_endpoint(self, app: FastAPI, path: str = "/api/upload") -> None:
        """Register a ``POST`` endpoint on *app* at *path*.

        Args:
            app: FastAPI application instance.
            path: URL path for the upload endpoint.
        """
        pipeline = self  # capture for closure

        @app.post(path)
        async def _upload_endpoint(file: UploadFile = File(...)):
            return await pipeline._handle_upload(file)

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------

    async def _handle_upload(self, file: UploadFile) -> JSONResponse:
        # 1. MIME type validation
        if self.allowed_types:
            content_type = file.content_type or ""
            if content_type not in self.allowed_types:
                return JSONResponse(
                    status_code=415,
                    content={"error": "Unsupported file type"},
                )

        # 2. Read content and size validation
        content = await file.read()
        if self.max_size_bytes is not None and len(content) > self.max_size_bytes:
            return JSONResponse(
                status_code=413,
                content={"error": "File too large"},
            )

        # 3. Sanitise filename
        original_name = file.filename or "upload"
        safe_name = self.sanitize_filename(original_name)
        if self.rename_fn:
            safe_name = self.sanitize_filename(self.rename_fn(original_name))

        # 4. Ensure upload directory exists
        os.makedirs(self.upload_dir, exist_ok=True)

        # 5. Save file
        dest = os.path.join(self.upload_dir, safe_name)
        try:
            with open(dest, "wb") as f:
                f.write(content)
        except OSError:
            return JSONResponse(
                status_code=500,
                content={"error": f"Upload failed"},
            )

        relative_url = f"/{self.upload_dir.rstrip('/')}/{safe_name}"
        return JSONResponse(status_code=200, content={"url": relative_url})

    @staticmethod
    def sanitize_filename(filename: str) -> str:
        """Remove path traversal sequences and unsafe characters.

        Args:
            filename: Raw filename from the upload.

        Returns:
            Safe filename string.
        """
        # Remove path traversal
        filename = filename.replace("../", "").replace("./", "")
        filename = os.path.basename(filename)

        # Split name and extension
        if "." in filename:
            *parts, ext = filename.rsplit(".", 1)
            name = ".".join(parts)
        else:
            name, ext = filename, ""

        # Replace unsafe chars with underscores
        name = re.sub(r"[^\w\-]", "_", name)
        ext = re.sub(r"[^\w]", "_", ext)

        return f"{name}.{ext}" if ext else name
