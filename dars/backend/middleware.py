# Dars Framework - Core Source File
#
# This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0.
# If a copy of the MPL was not distributed with this file, You can obtain one at
# https://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2026 ZtaDev
"""
Dars Backend Middleware System

Provides a complete middleware pipeline for FastAPI/Starlette applications:

- :class:`DarsMiddleware` — Abstract base class with ``before_request`` / ``after_response`` hooks.
- :class:`MiddlewareChain` — Composes multiple middlewares into a single Starlette middleware.
- :class:`SecurityHeadersMiddleware` — Injects CSP, HSTS, X-Frame-Options and other security headers.
- :class:`AuthMiddleware` — JWT Bearer / cookie validation with CSRF protection.
- :class:`CORSMiddleware` — Configurable cross-origin resource sharing.
- :class:`RateLimitMiddleware` — Per-IP / per-user rate limiting (sliding window).
- :class:`LoggingMiddleware` — Structured request/response logging.
- :class:`CompressionMiddleware` — Gzip/brotli response compression.

Usage::

    from fastapi import FastAPI
    from dars.backend.middleware import (
        SecurityHeadersMiddleware,
        CORSMiddleware,
        RateLimitMiddleware,
        LoggingMiddleware,
    )

    app = FastAPI()

    # Register via Starlette's add_middleware (order matters)
    app.add_middleware(
        SecurityHeadersMiddleware,
        csp="default-src 'self'",
        hsts=True,
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["https://example.com"],
        allow_methods=["*"],
    )
    app.add_middleware(
        RateLimitMiddleware,
        calls_per_minute=60,
    )
    app.add_middleware(LoggingMiddleware)
"""

from __future__ import annotations

import asyncio
import ipaddress
import json
import logging
import os
import time
from collections import defaultdict
from typing import (
    Any,
    Callable,
    Dict,
    List,
    Optional,
    Sequence,
    Set,
    Tuple,
    Type,
    Union,
)

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response
from starlette.types import ASGIApp

logger = logging.getLogger("dars.middleware")


# ═══════════════════════════════════════════════════════════════════════════════
# Base class
# ═══════════════════════════════════════════════════════════════════════════════

class DarsMiddleware(BaseHTTPMiddleware):
    """
    Abstract base middleware that provides ``before_request`` / ``after_response``
    lifecycle hooks.

    Subclasses override one or both hooks instead of ``dispatch`` directly::

        class MyMiddleware(DarsMiddleware):
            async def before_request(self, request: Request) -> Optional[Response]:
                # Inspect / mutate request before handler runs.
                # Return a Response to short-circuit the chain.
                return None

            async def after_response(self, request: Request, response: Response) -> Response:
                # Inspect / mutate response after handler runs.
                return response
    """

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        early = await self.before_request(request)
        if early is not None:
            return early
        response = await call_next(request)
        return await self.after_response(request, response)

    async def before_request(self, request: Request) -> Optional[Response]:
        """Called before the request reaches the route handler. Return a ``Response`` to short-circuit."""
        return None

    async def after_response(self, request: Request, response: Response) -> Response:
        """Called after the route handler returns. May mutate the response."""
        return response


# ═══════════════════════════════════════════════════════════════════════════════
# Middleware chain — compose several DarsMiddleware into one Starlette middleware
# ═══════════════════════════════════════════════════════════════════════════════

class MiddlewareChain(BaseHTTPMiddleware):
    """
    Composes multiple :class:`DarsMiddleware` instances into a single Starlette
    middleware.  Each middleware in the chain is called in registration order.

    Example::

        chain = MiddlewareChain(
            app,
            middlewares=[
                SecurityHeadersMiddleware(None, csp="default-src 'self'"),
                LoggingMiddleware(None),
            ],
        )
        # Then register *only* the chain on the FastAPI app:
        # (MiddlewareChain is itself a valid Starlette middleware, but since
        #  FastAPI's ``add_middleware`` instantiates the class, you normally
        #  register each middleware separately.)
    """

    def __init__(self, app: ASGIApp, middlewares: Optional[List[DarsMiddleware]] = None) -> None:
        super().__init__(app)
        self._middlewares = middlewares or []

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        # Build a composed call chain.
        async def runner(idx: int, request: Request) -> Response:
            if idx < len(self._middlewares):
                mw = self._middlewares[idx]
                early = await mw.before_request(request)
                if early is not None:
                    return early
                response = await runner(idx + 1, request)
                return await mw.after_response(request, response)
            return await call_next(request)

        return await runner(0, request)


# ═══════════════════════════════════════════════════════════════════════════════
# SecurityHeadersMiddleware (enhanced)
# ═══════════════════════════════════════════════════════════════════════════════

class SecurityHeadersMiddleware(DarsMiddleware):
    """
    Injects HTTP security headers into every response.

    Headers are only added when they are **not already present** in the
    response, so application code can override any individual header.

    Args:
        app: The ASGI application (passed automatically by FastAPI).
        csp: Optional ``Content-Security-Policy`` header value.
        hsts: When ``True``, adds ``Strict-Transport-Security`` with a
              one-year ``max-age`` and ``includeSubDomains``.
        csp_report_only: Optional ``Content-Security-Policy-Report-Only``.
        frame_options: ``X-Frame-Options`` value (default ``"DENY"``).
        nosniff: When ``True`` (default), adds ``X-Content-Type-Options: nosniff``.
        referrer_policy: ``Referrer-Policy`` value (default ``"strict-origin-when-cross-origin"``).
        permissions_policy: ``Permissions-Policy`` value.
        xss_protection: ``X-XSS-Protection`` value (default ``"1; mode=block"``).
        exclude_paths: List of path prefixes to skip.
    """

    DEFAULT_HEADERS: Dict[str, str] = {
        "X-Content-Type-Options": "nosniff",
        "X-Frame-Options": "DENY",
        "X-XSS-Protection": "1; mode=block",
        "Referrer-Policy": "strict-origin-when-cross-origin",
        "Permissions-Policy": "geolocation=(), microphone=(), camera=()",
    }

    def __init__(
        self,
        app: ASGIApp,
        csp: Optional[str] = None,
        hsts: bool = False,
        csp_report_only: Optional[str] = None,
        frame_options: Optional[str] = None,
        nosniff: Optional[bool] = None,
        referrer_policy: Optional[str] = None,
        permissions_policy: Optional[str] = None,
        xss_protection: Optional[str] = None,
        exclude_paths: Optional[List[str]] = None,
    ) -> None:
        super().__init__(app)
        self._csp = csp
        self._hsts = hsts
        self._csp_report_only = csp_report_only
        self._exclude_paths = exclude_paths or []
        self._overrides: Dict[str, str] = {}
        if frame_options is not None:
            self._overrides["X-Frame-Options"] = frame_options
        if nosniff is not None:
            self._overrides["X-Content-Type-Options"] = "nosniff" if nosniff else ""
        if referrer_policy is not None:
            self._overrides["Referrer-Policy"] = referrer_policy
        if permissions_policy is not None:
            self._overrides["Permissions-Policy"] = permissions_policy
        if xss_protection is not None:
            self._overrides["X-XSS-Protection"] = xss_protection

    async def after_response(self, request: Request, response: Response) -> Response:
        path = request.url.path
        for prefix in self._exclude_paths:
            if path.startswith(prefix):
                return response

        headers = dict(self.DEFAULT_HEADERS)
        headers.update({k: v for k, v in self._overrides.items() if v})

        for name, value in headers.items():
            if name.lower() not in response.headers:
                response.headers[name] = value

        if self._csp and "content-security-policy" not in response.headers:
            response.headers["Content-Security-Policy"] = self._csp

        if self._csp_report_only and "content-security-policy-report-only" not in response.headers:
            response.headers["Content-Security-Policy-Report-Only"] = self._csp_report_only

        if self._hsts and "strict-transport-security" not in response.headers:
            response.headers["Strict-Transport-Security"] = (
                "max-age=31536000; includeSubDomains"
            )

        return response


# ═══════════════════════════════════════════════════════════════════════════════
# AuthMiddleware (enhanced)
# ═══════════════════════════════════════════════════════════════════════════════

class AuthMiddleware(DarsMiddleware):
    """
    Validates JWT tokens (Bearer or cookie) on every request (except excluded paths).

    On success, injects ``request.state.user`` (dict) and ``request.state.auth_id``.

    Args:
        app: ASGI application.
        secret: Signing secret key.
        exclude_paths: List of URL path prefixes that do NOT require authentication.
        csrf_protection: When ``True`` (default), enforces CSRF token check for
                         state-changing methods when using cookie auth.
    """

    def __init__(
        self,
        app: ASGIApp,
        secret: str,
        exclude_paths: Optional[List[str]] = None,
        csrf_protection: bool = True,
    ) -> None:
        super().__init__(app)
        self.secret = secret
        self.exclude_paths = exclude_paths or []
        self.csrf_protection = csrf_protection

    async def before_request(self, request: Request) -> Optional[Response]:
        path = request.url.path
        is_excluded = (
            any(path.startswith(p) for p in self.exclude_paths)
            or path in ("/docs", "/openapi.json", "/redoc", "/_dars/health")
        )
        if is_excluded:
            return None

        token = None
        auth_id: str = "default"
        auth_header = request.headers.get("Authorization")
        is_bearer = False

        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header[7:]
            is_bearer = True
        else:
            for cookie_key, cookie_val in request.cookies.items():
                if cookie_key == "dars_access_token":
                    token = cookie_val
                    break
                if cookie_key.startswith("dars_access_token_"):
                    token = cookie_val
                    auth_id = cookie_key[len("dars_access_token_"):]
                    break
            if not token:
                token = request.cookies.get("dars_access_token_default")
                if token:
                    auth_id = "default"

        if not token:
            return Response("Unauthorized: Session token missing", status_code=401)

        # CSRF protection for cookie-based auth on mutating methods
        if self.csrf_protection and not is_bearer and request.method in ("POST", "PUT", "DELETE", "PATCH"):
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
            request.state.user = user_payload
            request.state.auth_id = auth_id
        except Exception as e:
            return Response(f"Unauthorized: Invalid session token ({e})", status_code=401)

        return None


# ═══════════════════════════════════════════════════════════════════════════════
# CORSMiddleware
# ═══════════════════════════════════════════════════════════════════════════════

class CORSMiddleware(DarsMiddleware):
    """
    Configurable CORS middleware.

    Args:
        app: ASGI application.
        allow_origins: List of allowed origins (e.g. ``["https://example.com"]``).
                       ``["*"]`` allows all (not recommended for production).
        allow_origin_regex: Regex pattern to match origins.
        allow_methods: Allowed HTTP methods (default ``["GET"]``).
        allow_headers: Allowed request headers (default ``["*"]``).
        expose_headers: Response headers exposed to the client.
        allow_credentials: When ``True``, sets ``Access-Control-Allow-Credentials``.
        max_age: ``Access-Control-Max-Age`` in seconds.
    """

    def __init__(
        self,
        app: ASGIApp,
        allow_origins: Optional[Sequence[str]] = None,
        allow_origin_regex: Optional[str] = None,
        allow_methods: Optional[Sequence[str]] = None,
        allow_headers: Optional[Sequence[str]] = None,
        expose_headers: Optional[Sequence[str]] = None,
        allow_credentials: bool = False,
        max_age: int = 600,
    ) -> None:
        super().__init__(app)
        self.allow_origins: List[str] = list(allow_origins) if allow_origins else []
        self.allow_origin_regex = allow_origin_regex
        self.allow_all_origins = "*" in self.allow_origins
        self.allow_methods: List[str] = list(allow_methods) if allow_methods else ["GET"]
        self.allow_headers: List[str] = list(allow_headers) if allow_headers else ["*"]
        self.expose_headers: List[str] = list(expose_headers) if expose_headers else []
        self.allow_credentials = allow_credentials
        self.max_age = max_age
        self._simple_headers = self._build_simple_headers()

    def _build_simple_headers(self) -> Dict[str, str]:
        h: Dict[str, str] = {}
        if self.allow_all_origins and not self.allow_credentials:
            h["Access-Control-Allow-Origin"] = "*"
        if self.allow_credentials:
            h["Access-Control-Allow-Credentials"] = "true"
        if self.expose_headers:
            h["Access-Control-Expose-Headers"] = ", ".join(self.expose_headers)
        return h

    def _match_origin(self, origin: str) -> bool:
        if self.allow_all_origins:
            return True
        if origin in self.allow_origins:
            return True
        if self.allow_origin_regex:
            import re
            if re.match(self.allow_origin_regex, origin):
                return True
        return False

    async def before_request(self, request: Request) -> Optional[Response]:
        if request.method == "OPTIONS":
            origin = request.headers.get("origin")
            if origin and self._match_origin(origin):
                headers = dict(self._simple_headers)
                if not self.allow_all_origins:
                    headers["Access-Control-Allow-Origin"] = origin
                if self.allow_methods:
                    headers["Access-Control-Allow-Methods"] = ", ".join(self.allow_methods)
                if self.allow_headers:
                    if self.allow_credentials and self.allow_headers == ["*"]:
                        req_h = request.headers.get("Access-Control-Request-Headers")
                        headers["Access-Control-Allow-Headers"] = req_h if req_h else "*"
                    else:
                        headers["Access-Control-Allow-Headers"] = ", ".join(self.allow_headers)
                if self.max_age:
                    headers["Access-Control-Max-Age"] = str(self.max_age)
                return Response(status_code=204, headers=headers)
            return Response(status_code=400, content="CORS: origin not allowed")
        return None

    async def after_response(self, request: Request, response: Response) -> Response:
        origin = request.headers.get("origin")
        if origin and self._match_origin(origin):
            if self.allow_all_origins and not self.allow_credentials:
                response.headers.setdefault("Access-Control-Allow-Origin", "*")
            else:
                response.headers.setdefault("Access-Control-Allow-Origin", origin)
            if self.allow_credentials:
                response.headers.setdefault("Access-Control-Allow-Credentials", "true")
            if self.expose_headers:
                response.headers.setdefault(
                    "Access-Control-Expose-Headers", ", ".join(self.expose_headers)
                )
        return response


# ═══════════════════════════════════════════════════════════════════════════════
# RateLimitMiddleware
# ═══════════════════════════════════════════════════════════════════════════════

class RateLimitMiddleware(DarsMiddleware):
    """
    Sliding-window rate limiter keyed by IP address (or user ID if available
    via ``request.state.user``).

    Args:
        app: ASGI application.
        calls_per_minute: Max requests per minute per client (default ``60``).
        calls_per_hour: Max requests per hour per client.
        calls_per_day: Max requests per day per client.
        burst: Number of additional burst requests allowed (default ``10``).
        exclude_paths: Path prefixes that bypass rate limiting.
        limit_by: Callable ``(request) -> str`` that returns the rate-limit key.
                 Defaults to IP address.
        backend: Storage backend for counters.  Defaults to in-memory dict.
    """

    def __init__(
        self,
        app: ASGIApp,
        calls_per_minute: int = 60,
        calls_per_hour: Optional[int] = None,
        calls_per_day: Optional[int] = None,
        burst: int = 10,
        exclude_paths: Optional[List[str]] = None,
        limit_by: Optional[Callable[[Request], str]] = None,
        backend: Optional["RateLimitBackend"] = None,
    ) -> None:
        super().__init__(app)
        self.calls_per_minute = calls_per_minute
        self.calls_per_hour = calls_per_hour
        self.calls_per_day = calls_per_day
        self.burst = burst
        self.exclude_paths = exclude_paths or []
        self._limit_by = limit_by or self._default_key
        self._backend = backend or InMemoryRateLimitBackend()

    @staticmethod
    def _default_key(request: Request) -> str:
        forwarded = request.headers.get("X-Forwarded-For", "")
        if forwarded:
            client_ip = forwarded.split(",")[0].strip()
        else:
            client_ip = request.client.host if request.client else "127.0.0.1"
        try:
            ipaddress.ip_address(client_ip)
        except ValueError:
            client_ip = "127.0.0.1"
        return client_ip

    async def before_request(self, request: Request) -> Optional[Response]:
        path = request.url.path
        for prefix in self.exclude_paths:
            if path.startswith(prefix):
                return None

        key = self._limit_by(request)
        now = int(time.time())

        limits = []
        if self.calls_per_minute:
            limits.append((self.calls_per_minute, 60, "minute"))
        if self.calls_per_hour:
            limits.append((self.calls_per_hour, 3600, "hour"))
        if self.calls_per_day:
            limits.append((self.calls_per_day, 86400, "day"))

        for max_calls, window_seconds, label in limits:
            count = self._backend.increment(key, now, window_seconds, max_calls + self.burst)
            remaining = max(0, max_calls + self.burst - count)
            if count > max_calls + self.burst:
                retry_after = self._backend.retry_after(key, now, window_seconds)
                headers = {
                    "Retry-After": str(retry_after),
                    "X-RateLimit-Limit": str(max_calls),
                    "X-RateLimit-Remaining": "0",
                    "X-RateLimit-Reset": str(now + retry_after),
                }
                return Response(
                    content=json.dumps({
                        "error": "rate_limit_exceeded",
                        "detail": f"Rate limit exceeded: {max_calls} per {label}",
                    }),
                    status_code=429,
                    headers=headers,
                    media_type="application/json",
                )
            # Set remaining headers on the eventual response (via request.state)
            if not hasattr(request.state, "_rate_limit_headers"):
                request.state._rate_limit_headers = {}
            request.state._rate_limit_headers.update({
                "X-RateLimit-Limit": str(max_calls),
                "X-RateLimit-Remaining": str(remaining),
                "X-RateLimit-Reset": str(now + window_seconds),
            })

        return None

    async def after_response(self, request: Request, response: Response) -> Response:
        headers = getattr(request.state, "_rate_limit_headers", None)
        if headers:
            for k, v in headers.items():
                if k.lower() not in response.headers:
                    response.headers[k] = v
        return response


class RateLimitBackend:
    """Abstract rate-limit storage backend."""

    def increment(self, key: str, now: int, window: int, max_count: int) -> int:
        raise NotImplementedError

    def retry_after(self, key: str, now: int, window: int) -> int:
        raise NotImplementedError


class InMemoryRateLimitBackend(RateLimitBackend):
    """In-memory sliding-window rate limit store (single-process only)."""

    def __init__(self) -> None:
        self._buckets: Dict[str, List[int]] = defaultdict(list)

    def increment(self, key: str, now: int, window: int, max_count: int) -> int:
        ts_list = self._buckets[key]
        cutoff = now - window
        # Prune expired timestamps
        self._buckets[key] = [t for t in ts_list if t > cutoff]
        bucket = self._buckets[key]
        bucket.append(now)
        return len(bucket)

    def retry_after(self, key: str, now: int, window: int) -> int:
        bucket = self._buckets.get(key, [])
        if len(bucket) < 2:
            return 0
        return max(0, int(bucket[0] + window - now))


# ═══════════════════════════════════════════════════════════════════════════════
# LoggingMiddleware
# ═══════════════════════════════════════════════════════════════════════════════

class LoggingMiddleware(DarsMiddleware):
    """
    Logs every request (method, path, status, duration).

    Args:
        app: ASGI application.
        log_body: When ``True``, logs request body (up to 4096 bytes).
        log_headers: When ``True``, logs selected request headers.
        include_paths: If set, only log paths matching these prefixes (further filtered by ``exclude_paths``).
        exclude_paths: Path prefixes to skip logging.
        logger_name: Logger name (default ``"dars.middleware"``).
        sensitive_headers: Header names whose values are masked (default ``["authorization", "cookie", "x-xsrf-token"]``).
    """

    def __init__(
        self,
        app: ASGIApp,
        log_body: bool = False,
        log_headers: bool = False,
        include_paths: Optional[List[str]] = None,
        exclude_paths: Optional[List[str]] = None,
        logger_name: str = "dars.middleware",
        sensitive_headers: Optional[Set[str]] = None,
    ) -> None:
        super().__init__(app)
        self.log_body = log_body
        self.log_headers = log_headers
        self.include_paths = include_paths or []
        self.exclude_paths = exclude_paths or []
        self._logger = logging.getLogger(logger_name)
        self._sensitive = sensitive_headers or {"authorization", "cookie", "x-xsrf-token", "set-cookie"}

    def _should_log(self, path: str) -> bool:
        if self.include_paths and not any(path.startswith(p) for p in self.include_paths):
            return False
        if any(path.startswith(p) for p in self.exclude_paths):
            return False
        return True

    async def before_request(self, request: Request) -> Optional[Response]:
        if not self._should_log(request.url.path):
            return None
        request.state._dars_start_time = time.perf_counter()
        return None

    async def after_response(self, request: Request, response: Response) -> Response:
        path = request.url.path
        start: float = getattr(request.state, "_dars_start_time", 0)
        duration_ms = (time.perf_counter() - start) * 1000 if start else 0

        if not self._should_log(path):
            return response

        extra: Dict[str, Any] = {
            "method": request.method,
            "path": path,
            "status": response.status_code,
            "duration_ms": round(duration_ms, 2),
            "client_ip": request.client.host if request.client else "unknown",
            "user_agent": request.headers.get("user-agent", ""),
        }

        if self.log_headers:
            masked: Dict[str, str] = {}
            for k, v in request.headers.items():
                masked[k] = "[REDACTED]" if k.lower() in self._sensitive else v
            extra["request_headers"] = masked

        if self.log_body and request.method in ("POST", "PUT", "PATCH"):
            try:
                body = await request.body()
                extra["request_body"] = body[:4096].decode("utf-8", errors="replace")
            except Exception:
                extra["request_body"] = "<unreadable>"

        self._logger.info("%s %s → %d (%sms)", request.method, path, response.status_code, round(duration_ms, 1), extra=extra)
        return response


# ═══════════════════════════════════════════════════════════════════════════════
# CompressionMiddleware
# ═══════════════════════════════════════════════════════════════════════════════

class CompressionMiddleware(DarsMiddleware):
    """
    Enables gzip compression for responses.

    This is a lightweight wrapper; for production use, consider placing a
    reverse proxy (nginx, Caddy) in front of the app.

    Args:
        app: ASGI application.
        minimum_size: Minimum response body size in bytes to compress (default ``1024``).
        exclude_paths: Path prefixes to skip compression.
    """

    def __init__(
        self,
        app: ASGIApp,
        minimum_size: int = 1024,
        exclude_paths: Optional[List[str]] = None,
    ) -> None:
        super().__init__(app)
        self.minimum_size = minimum_size
        self.exclude_paths = exclude_paths or []
        try:
            import gzip
            self._gzip = gzip
        except ImportError:
            self._gzip = None

    async def after_response(self, request: Request, response: Response) -> Response:
        if self._gzip is None:
            return response

        path = request.url.path
        for prefix in self.exclude_paths:
            if path.startswith(prefix):
                return response

        # Only compress if client accepts gzip
        accept_encoding = request.headers.get("Accept-Encoding", "")
        if "gzip" not in accept_encoding:
            return response

        # Only compress text-based content types
        content_type = response.headers.get("content-type", "").lower()
        if not any(t in content_type for t in ("text/", "application/json", "application/javascript", "application/xml")):
            return response

        if not hasattr(response, 'body'):
            return response
        body: bytes = response.body
        if body is None or len(body) < self.minimum_size:
            return response

        compressed = self._gzip.compress(body)
        response.body = compressed
        response.headers["Content-Encoding"] = "gzip"
        response.headers["Content-Length"] = str(len(compressed))
        # Remove ETag when compressing (content has changed)
        response.headers.pop("ETag", None)
        return response


# ═══════════════════════════════════════════════════════════════════════════════
# Convenience: register all standard middlewares on a FastAPI app
# ═══════════════════════════════════════════════════════════════════════════════

DEFAULT_MIDDLEWARE_CONFIG: Dict[str, Any] = {
    "security_headers": {
        "csp": "default-src 'self'",
        "hsts": True,
    },
    "cors": {
        "allow_origins": [],
        "allow_methods": ["*"],
        "allow_headers": ["*"],
        "allow_credentials": True,
    },
    "rate_limit": {
        "calls_per_minute": 60,
        "burst": 10,
    },
    "logging": {
        "log_body": False,
        "log_headers": False,
    },
}


def register_default_middlewares(app, config: Optional[Dict[str, Any]] = None) -> None:
    """
    Register the default middleware stack on a FastAPI application.

    Order: Logging → RateLimit → CORS → SecurityHeaders

    Args:
        app: FastAPI application instance.
        config: Optional overrides for each middleware's kwargs.
                Keys match ``DEFAULT_MIDDLEWARE_CONFIG``.
    """
    cfg = dict(DEFAULT_MIDDLEWARE_CONFIG)
    if config:
        for k, v in config.items():
            if k in cfg and isinstance(v, dict):
                cfg[k].update(v)
            else:
                cfg[k] = v

    app.add_middleware(LoggingMiddleware, **cfg["logging"])
    app.add_middleware(RateLimitMiddleware, **cfg["rate_limit"])
    app.add_middleware(CORSMiddleware, **cfg["cors"])
    app.add_middleware(SecurityHeadersMiddleware, **cfg["security_headers"])
