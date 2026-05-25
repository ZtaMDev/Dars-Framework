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


class AuthMiddleware(BaseHTTPMiddleware):
    """
    Starlette/FastAPI middleware that validates a JWT Bearer token or cookie.
    
    If the token is valid, it injects the decoded payload dictionary into 
    ``request.state.user``.
    
    If a protected route is requested and no token is present or it is invalid,
    it returns an HTTP 401 response.
    
    Args:
        app: ASGI application.
        secret: Signing secret key.
        exclude_paths: List of string URL path prefixes that do not require authentication.
    """
    def __init__(self, app, secret: str, exclude_paths: Optional[list] = None) -> None:
        super().__init__(app)
        self.secret = secret
        self.exclude_paths = exclude_paths or []

    async def dispatch(self, request: Request, call_next) -> Response:
        path = request.url.path
        
        # Check if the path is explicitly excluded, or a standard API doc path, or health check
        is_excluded = (
            any(path.startswith(p) for p in self.exclude_paths) or
            path in ['/docs', '/openapi.json', '/redoc', '/_dars/health']
        )
        
        if is_excluded:
            return await call_next(request)
            
        # Extract token from the Authorization header or the dars_access_token cookie
        token = None
        auth_id = "default"
        auth_header = request.headers.get("Authorization")
        is_bearer = False
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header[7:]
            is_bearer = True
        else:
            for cookie_key, cookie_val in request.cookies.items():
                if cookie_key == "dars_access_token":
                    token = cookie_val
                    auth_id = "default"
                    break
                elif cookie_key.startswith("dars_access_token_"):
                    token = cookie_val
                    auth_id = cookie_key[len("dars_access_token_"):]
                    break
            if not token:
                token = request.cookies.get("dars_access_token_default")
                if token:
                    auth_id = "default"
            
        if not token:
            return Response("Unauthorized: Session token missing", status_code=401)
            
        # CSRF Protection for cookie-based auth
        if not is_bearer and request.method in ["POST", "PUT", "DELETE", "PATCH"]:
            xsrf_cookie = request.cookies.get("XSRF-TOKEN")
            xsrf_header = request.headers.get("X-XSRF-TOKEN")
            if not xsrf_cookie or not xsrf_header or xsrf_cookie != xsrf_header:
                return Response("Forbidden: Invalid CSRF token", status_code=403)
            
        try:
            from dars.core.auth import DarsAuth
            from dars.backend.auth_routes import get_auth_config
            
            config = get_auth_config(auth_id)
            secret = config["secret"] if config else self.secret
            
            user_payload = DarsAuth.decode_token(token, secret)
            # Inject user dictionary securely into request state
            request.state.user = user_payload
            request.state.auth_id = auth_id
        except Exception as e:
            return Response(f"Unauthorized: Invalid session token ({e})", status_code=401)
            
        return await call_next(request)
