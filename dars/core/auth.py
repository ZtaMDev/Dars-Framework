# Dars Framework - Core Auth Module
#
# This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0.
# If a copy of the MPL was not distributed with this file, You can obtain one at
# https://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2026 ZtaDev
import base64
import hashlib
import hmac
import json
import os
import time
import asyncio
from functools import wraps
from typing import Any, Dict, Optional, Union
from fastapi import Request, HTTPException

# Helper functions for Base64URL encoding/decoding as required by JWT specs
def base64url_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b'=').decode('utf-8')

def base64url_decode(data: str) -> bytes:
    rem = len(data) % 4
    if rem > 0:
        data += '=' * (4 - rem)
    return base64.urlsafe_b64decode(data.encode('utf-8'))


class DarsAuth:
    """
    Core security utility for JWT signing/verification and secure password hashing.
    Runs on pure Python standard libraries (zero third-party compile dependencies).
    """

    @staticmethod
    def encode_token(payload: dict, secret: str, algorithm: str = "HS256", expires_in: int = 3600) -> str:
        """
        Generate a cryptographically secure JWT signed with HMAC-SHA256.
        
        Args:
            payload: Data dictionary to encode.
            secret: Sign key.
            algorithm: Only "HS256" is supported for simplicity and robust pure-Python hmac.
            expires_in: Expiry duration in seconds (default: 1 hour).
        """
        header = {"alg": algorithm, "typ": "JWT"}
        
        # Inject standard exp claim if not present
        payload = dict(payload)
        if "exp" not in payload:
            payload["exp"] = int(time.time()) + expires_in
            
        header_b64 = base64url_encode(json.dumps(header, sort_keys=True).encode('utf-8'))
        payload_b64 = base64url_encode(json.dumps(payload, sort_keys=True).encode('utf-8'))
        
        signing_input = f"{header_b64}.{payload_b64}".encode('utf-8')
        
        if algorithm == "HS256":
            signature = hmac.new(secret.encode('utf-8'), signing_input, hashlib.sha256).digest()
        else:
            raise ValueError(f"Unsupported algorithm: {algorithm}")
            
        signature_b64 = base64url_encode(signature)
        return f"{header_b64}.{payload_b64}.{signature_b64}"

    @staticmethod
    def decode_token(token: str, secret: str, algorithm: str = "HS256") -> dict:
        """
        Validate and decode a JWT.
        
        Uses hmac.compare_digest for constant-time signature comparison to completely
        prevent timing attacks.
        
        Args:
            token: JWT string.
            secret: Sign key.
            algorithm: Signature algorithm (default: HS256).
            
        Raises:
            ValueError: If token is malformed, signature is invalid, or expired.
        """
        try:
            parts = token.split('.')
            if len(parts) != 3:
                raise ValueError("Invalid token format")
                
            header_b64, payload_b64, signature_b64 = parts
            
            # Verify signature first
            signing_input = f"{header_b64}.{payload_b64}".encode('utf-8')
            if algorithm == "HS256":
                expected_sig = hmac.new(secret.encode('utf-8'), signing_input, hashlib.sha256).digest()
            else:
                raise ValueError(f"Unsupported algorithm: {algorithm}")
                
            actual_sig = base64url_decode(signature_b64)
            
            # Use constant-time comparison to prevent timing attacks
            if not hmac.compare_digest(expected_sig, actual_sig):
                raise ValueError("Signature verification failed")
                
            payload = json.loads(base64url_decode(payload_b64).decode('utf-8'))
            
            # Check expiration
            if "exp" in payload and payload["exp"] < time.time():
                raise ValueError("Token expired")
                
            return payload
        except Exception as e:
            raise ValueError(f"Token decoding failed: {e}")

    @staticmethod
    def hash_password(password: str) -> str:
        """
        Hash a password using the highly secure PBKDF2 algorithm with SHA-256 (100,000 iterations).
        Formats hash exactly like Django to support modular, standard schema representation.
        
        Returns:
            Formatted hash string: pbkdf2_sha256$100000$salt$hash
        """
        salt = os.urandom(16)
        pwd_hash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
        salt_b64 = base64.b64encode(salt).decode('utf-8')
        hash_b64 = base64.b64encode(pwd_hash).decode('utf-8')
        return f"pbkdf2_sha256$100000${salt_b64}${hash_b64}"

    @staticmethod
    def verify_password(password: str, hashed: str) -> bool:
        """
        Verify a password against a PBKDF2 hash using timing-attack resistant comparison.
        """
        try:
            parts = hashed.split('$')
            if len(parts) != 4 or parts[0] != 'pbkdf2_sha256':
                return False
            iterations = int(parts[1])
            salt = base64.b64decode(parts[2])
            expected_hash = base64.b64decode(parts[3])
            actual_hash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, iterations)
            return hmac.compare_digest(expected_hash, actual_hash)
        except Exception:
            return False


    @staticmethod
    def set_auth_cookies(response: Any, access_token: str, refresh_token: str, xsrf_token: str, secure: bool = True, auth_id: str = "default"):
        """
        Sets the secure HttpOnly access and refresh cookies, and a readable XSRF-TOKEN cookie.
        """
        access_key = "dars_access_token" if auth_id == "default" else f"dars_access_token_{auth_id}"
        refresh_key = "dars_refresh_token" if auth_id == "default" else f"dars_refresh_token_{auth_id}"
        response.set_cookie(
            key=access_key,
            value=access_token,
            httponly=True,
            secure=secure,
            samesite="strict",
            max_age=900,  # 15 minutes
        )
        response.set_cookie(
            key=refresh_key,
            value=refresh_token,
            httponly=True,
            secure=secure,
            samesite="strict",
            max_age=604800,  # 7 days
        )
        response.set_cookie(
            key="XSRF-TOKEN",
            value=xsrf_token,
            httponly=False,
            secure=secure,
            samesite="strict",
            max_age=604800,
        )

    @staticmethod
    def clear_auth_cookies(response: Any, secure: bool = True, auth_id: str = "default"):
        """Clears all authentication and CSRF cookies."""
        access_key = "dars_access_token" if auth_id == "default" else f"dars_access_token_{auth_id}"
        refresh_key = "dars_refresh_token" if auth_id == "default" else f"dars_refresh_token_{auth_id}"
        response.delete_cookie(access_key, secure=secure, samesite="strict", httponly=True)
        response.delete_cookie(refresh_key, secure=secure, samesite="strict", httponly=True)
        response.delete_cookie("XSRF-TOKEN", secure=secure, samesite="strict", httponly=False)


# ---------------------------------------------------------------------------
# FastAPI Route Guards Decorators
# ---------------------------------------------------------------------------

def requires_auth(func=None, *, verify_credentials_callback=None, secret=None, auth_id=None):
    """
    FastAPI Route Decorator to enforce authentication.
    Injects request.state.user into the handler. Supports both sync and async.
    """
    from dars.backend.auth_routes import register_auth_config

    custom_auth_id = None
    if verify_credentials_callback is not None or secret is not None:
        if auth_id:
            custom_auth_id = register_auth_config(verify_credentials_callback, secret or "dars_default_secret_key_change_me_in_production", auth_id)

    def decorator(f):
        target_auth_id = custom_auth_id or auth_id
        if not target_auth_id:
            if verify_credentials_callback is not None or secret is not None:
                target_auth_id = f"auth_{f.__name__}"
                register_auth_config(verify_credentials_callback, secret or "dars_default_secret_key_change_me_in_production", target_auth_id)
            else:
                target_auth_id = "default"

        f.__requires_auth__ = True
        f.__auth_id__ = target_auth_id

        if asyncio.iscoroutinefunction(f):
            @wraps(f)
            async def async_wrapper(*args, **kwargs):
                request = kwargs.get("request")
                if not request:
                    for arg in args:
                        if isinstance(arg, Request):
                            request = arg
                            break
                if not request:
                    return await f(*args, **kwargs)
                
                user = await _verify_request_for_auth_id(request, target_auth_id)
                if not user:
                    raise HTTPException(status_code=401, detail="Authentication required")
                
                request.state.user = user
                request.state.auth_id = target_auth_id
                return await f(*args, **kwargs)
            return async_wrapper
        else:
            @wraps(f)
            def sync_wrapper(*args, **kwargs):
                request = kwargs.get("request")
                if not request:
                    for arg in args:
                        if isinstance(arg, Request):
                            request = arg
                            break
                if not request:
                    return f(*args, **kwargs)
                
                user = _verify_request_for_auth_id_sync(request, target_auth_id)
                if not user:
                    raise HTTPException(status_code=401, detail="Authentication required")
                
                request.state.user = user
                request.state.auth_id = target_auth_id
                return f(*args, **kwargs)
            return sync_wrapper

    if func is not None and callable(func):
        return decorator(func)
    return decorator


def _verify_request_for_auth_id_sync(request: Request, auth_id: str) -> Optional[dict]:
    from dars.backend.auth_routes import get_auth_config
    config = get_auth_config(auth_id)
    if not config:
        user = getattr(request.state, "user", None)
        return user
        
    secret = config["secret"]
    
    token = None
    auth_header = request.headers.get("Authorization")
    is_bearer = False
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header[7:]
        is_bearer = True
    else:
        cookie_name = "dars_access_token" if auth_id == "default" else f"dars_access_token_{auth_id}"
        token = request.cookies.get(cookie_name)
        if not token and auth_id == "default":
            token = request.cookies.get("dars_access_token_default")
            
    if not token:
        return None
        
    if not is_bearer and request.method in ["POST", "PUT", "DELETE", "PATCH"]:
        xsrf_cookie = request.cookies.get("XSRF-TOKEN")
        xsrf_header = request.headers.get("X-XSRF-TOKEN")
        if not xsrf_cookie or not xsrf_header or xsrf_cookie != xsrf_header:
            return None
            
    try:
        user_payload = DarsAuth.decode_token(token, secret)
        return user_payload
    except Exception:
        return None


async def _verify_request_for_auth_id(request: Request, auth_id: str) -> Optional[dict]:
    return _verify_request_for_auth_id_sync(request, auth_id)


def requires_role(role: str):
    """
    FastAPI Route Decorator to enforce role-based access control (RBAC).
    """
    def decorator(func):
        if asyncio.iscoroutinefunction(func):
            @wraps(func)
            async def async_wrapper(*args, **kwargs):
                request = kwargs.get("request")
                if not request:
                    for arg in args:
                        if isinstance(arg, Request):
                            request = arg
                            break
                if not request:
                    raise ValueError("@requires_role requires a 'request: Request' argument in the route handler function signature.")
                    
                user = getattr(request.state, "user", None)
                if not user:
                    raise HTTPException(status_code=401, detail="Authentication required")
                
                # Check role or roles list
                user_roles = user.get("roles", [])
                if isinstance(user_roles, str):
                    user_roles = [user_roles]
                if role not in user_roles and user.get("role") != role:
                    raise HTTPException(status_code=403, detail="Forbidden: Insufficient permissions")
                    
                return await func(*args, **kwargs)
            return async_wrapper
        else:
            @wraps(func)
            def sync_wrapper(*args, **kwargs):
                request = kwargs.get("request")
                if not request:
                    for arg in args:
                        if isinstance(arg, Request):
                            request = arg
                            break
                if not request:
                    raise ValueError("@requires_role requires a 'request: Request' argument in the route handler function signature.")
                    
                user = getattr(request.state, "user", None)
                if not user:
                    raise HTTPException(status_code=401, detail="Authentication required")
                
                # Check role or roles list
                user_roles = user.get("roles", [])
                if isinstance(user_roles, str):
                    user_roles = [user_roles]
                if role not in user_roles and user.get("role") != role:
                    raise HTTPException(status_code=403, detail="Forbidden: Insufficient permissions")
                    
                return func(*args, **kwargs)
            return sync_wrapper
    return decorator
