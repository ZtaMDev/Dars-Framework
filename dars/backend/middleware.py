# Dars Framework - Core Source File
#
# This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0.
# If a copy of the MPL was not distributed with this file, You can obtain one at
# https://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2025 ZtaDev
"""
Dars backend middleware collection.

Currently provides:

- :class:`SecurityHeadersMiddleware` — injects HTTP security headers into every response.

The full middleware system (base class, :class:`CORSMiddleware`,
:class:`AuthMiddleware`) is added in a later task.
"""

from typing import Optional

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """
    Starlette/FastAPI middleware that injects HTTP security headers.

    Headers are only added when they are **not already present** in the
    response, so application code can override any individual header.

    Args:
        app: The ASGI application (passed automatically by FastAPI).
        csp: Optional ``Content-Security-Policy`` header value.
        hsts: When ``True``, adds ``Strict-Transport-Security`` with a
              one-year ``max-age`` and ``includeSubDomains``.

    Example::

        from fastapi import FastAPI
        from dars.backend.middleware import SecurityHeadersMiddleware

        app = FastAPI()
        app.add_middleware(SecurityHeadersMiddleware, csp="default-src 'self'", hsts=True)
    """

    DEFAULT_HEADERS: dict = {
        "X-Content-Type-Options": "nosniff",
        "X-Frame-Options": "DENY",
        "X-XSS-Protection": "1; mode=block",
        "Referrer-Policy": "strict-origin-when-cross-origin",
        "Permissions-Policy": "geolocation=(), microphone=(), camera=()",
    }

    def __init__(
        self,
        app,
        csp: Optional[str] = None,
        hsts: bool = False,
    ) -> None:
        super().__init__(app)
        self._csp = csp
        self._hsts = hsts

    async def dispatch(self, request: Request, call_next) -> Response:
        response: Response = await call_next(request)

        # Inject each default header only when not already set
        for name, value in self.DEFAULT_HEADERS.items():
            if name.lower() not in response.headers:
                response.headers[name] = value

        if self._csp and "content-security-policy" not in response.headers:
            response.headers["Content-Security-Policy"] = self._csp

        if self._hsts and "strict-transport-security" not in response.headers:
            response.headers["Strict-Transport-Security"] = (
                "max-age=31536000; includeSubDomains"
            )

        return response
