# Dars Framework - Backend Auth Routes
#
# This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0.
# If a copy of the MPL was not distributed with this file, You can obtain one at
# https://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2026 ZtaDev

import secrets
from fastapi import APIRouter, Request, Response, HTTPException
from pydantic import BaseModel
from typing import Callable, Awaitable, Optional, Any
from dars.core.auth import DarsAuth, requires_auth
from dars.backend.session import SessionManager

# The user-provided verify callback. Signature: (username, password) -> Optional[dict]
# It should return a dictionary payload for the user if valid, or None if invalid.
_verify_callback: Optional[Callable[[str, str], Any]] = None
_session_manager: Optional[SessionManager] = None
_app_secret: str = ""

_auth_configs = {}

def register_auth_config(verify_credentials_callback, secret: str, auth_id: str = "default"):
    from dars.backend.session import SessionManager, InMemorySessionStore
    _auth_configs[auth_id] = {
        "verify_callback": verify_credentials_callback,
        "session_manager": SessionManager(InMemorySessionStore()),
        "secret": secret
    }
    # Backward compatibility for global variables
    if auth_id == "default":
        global _verify_callback, _session_manager, _app_secret
        _verify_callback = verify_credentials_callback
        _session_manager = _auth_configs["default"]["session_manager"]
        _app_secret = secret
    return auth_id

def get_auth_config(auth_id: str = "default"):
    return _auth_configs.get(auth_id)

auth_router = APIRouter(prefix="/_dars/auth", tags=["Dars Auth"])

class LoginRequest(BaseModel):
    username: str
    password: str

@auth_router.post("/login")
@auth_router.post("/{auth_id}/login")
async def login(req: LoginRequest, response: Response, auth_id: str = "default"):
    """
    Validates credentials using the configured callback and issues secure tokens.
    """
    config = get_auth_config(auth_id)
    if not config:
        raise HTTPException(status_code=500, detail=f"Auth with ID '{auth_id}' not configured")

    verify_cb = config["verify_callback"]
    sess_mgr = config["session_manager"]
    app_secret = config["secret"]

    # Call the verify function (support both sync and async)
    import inspect
    if inspect.iscoroutinefunction(verify_cb):
        user_payload = await verify_cb(req.username, req.password)
    else:
        user_payload = verify_cb(req.username, req.password)
        
    if not user_payload:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # The payload MUST include an id or username for the session
    user_id = str(user_payload.get("id", user_payload.get("username", "unknown")))
    
    # 1. Issue short-lived Access Token (15m)
    access_token = DarsAuth.encode_token(user_payload, app_secret, expires_in=900)
    
    # 2. Issue long-lived Refresh Token (7d)
    refresh_token = sess_mgr.issue_refresh_token(user_id, user_payload, expires_in=604800)
    
    # 3. Issue CSRF Token
    xsrf_token = secrets.token_urlsafe(32)
    
    # Set cookies
    DarsAuth.set_auth_cookies(response, access_token, refresh_token, xsrf_token, auth_id=auth_id)
    
    return {"status": "success", "user": user_payload}

@auth_router.post("/refresh")
@auth_router.post("/{auth_id}/refresh")
async def refresh(request: Request, response: Response, auth_id: str = "default"):
    """
    Uses the refresh token cookie to issue a new access token.
    """
    config = get_auth_config(auth_id)
    if not config:
        raise HTTPException(status_code=500, detail=f"Auth with ID '{auth_id}' not configured")
        
    sess_mgr = config["session_manager"]
    app_secret = config["secret"]
        
    refresh_key = "dars_refresh_token" if auth_id == "default" else f"dars_refresh_token_{auth_id}"
    refresh_token = request.cookies.get(refresh_key)
    if not refresh_token and auth_id == "default":
        refresh_token = request.cookies.get("dars_refresh_token_default")
        
    if not refresh_token:
        raise HTTPException(status_code=401, detail="No refresh token")
        
    session = sess_mgr.validate_refresh_token(refresh_token)
    if not session:
        # Invalid or expired refresh token. Clear cookies.
        DarsAuth.clear_auth_cookies(response, auth_id=auth_id)
        raise HTTPException(status_code=401, detail="Invalid refresh token")
        
    # Generate new tokens
    user_payload = session["payload"]
    user_id = session["user_id"]
    
    # Revoke old refresh token and issue a new one (Refresh Token Rotation)
    sess_mgr.revoke_refresh_token(refresh_token)
    new_refresh_token = sess_mgr.issue_refresh_token(user_id, user_payload, expires_in=604800)
    
    new_access_token = DarsAuth.encode_token(user_payload, app_secret, expires_in=900)
    xsrf_token = secrets.token_urlsafe(32)
    
    DarsAuth.set_auth_cookies(response, new_access_token, new_refresh_token, xsrf_token, auth_id=auth_id)
    
    return {"status": "success"}

@auth_router.post("/logout")
@auth_router.post("/{auth_id}/logout")
async def logout(request: Request, response: Response, auth_id: str = "default"):
    """
    Revokes the refresh token and clears auth cookies.
    """
    config = get_auth_config(auth_id)
    if config:
        sess_mgr = config["session_manager"]
        refresh_key = "dars_refresh_token" if auth_id == "default" else f"dars_refresh_token_{auth_id}"
        refresh_token = request.cookies.get(refresh_key)
        if not refresh_token and auth_id == "default":
            refresh_token = request.cookies.get("dars_refresh_token_default")
        if refresh_token:
            sess_mgr.revoke_refresh_token(refresh_token)
            
    DarsAuth.clear_auth_cookies(response, auth_id=auth_id)
    return {"status": "success"}

@auth_router.get("/me")
@auth_router.get("/{auth_id}/me")
async def get_me(request: Request, auth_id: str = "default"):
    """
    Returns the currently authenticated user's data.
    """
    from dars.core.auth import _verify_request_for_auth_id
    user = await _verify_request_for_auth_id(request, auth_id)
    if not user:
        raise HTTPException(status_code=401, detail="Authentication required")
    return {"user": user}
