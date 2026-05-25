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

auth_router = APIRouter(prefix="/_dars/auth", tags=["Dars Auth"])

class LoginRequest(BaseModel):
    username: str
    password: str

@auth_router.post("/login")
async def login(req: LoginRequest, response: Response):
    """
    Validates credentials using the configured callback and issues secure tokens.
    """
    if not _verify_callback or not _session_manager or not _app_secret:
        raise HTTPException(status_code=500, detail="Auth not configured")

    # Call the verify function (support both sync and async)
    import inspect
    if inspect.iscoroutinefunction(_verify_callback):
        user_payload = await _verify_callback(req.username, req.password)
    else:
        user_payload = _verify_callback(req.username, req.password)
        
    if not user_payload:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # The payload MUST include an id or username for the session
    user_id = str(user_payload.get("id", user_payload.get("username", "unknown")))
    
    # 1. Issue short-lived Access Token (15m)
    access_token = DarsAuth.encode_token(user_payload, _app_secret, expires_in=900)
    
    # 2. Issue long-lived Refresh Token (7d)
    refresh_token = _session_manager.issue_refresh_token(user_id, user_payload, expires_in=604800)
    
    # 3. Issue CSRF Token
    xsrf_token = secrets.token_urlsafe(32)
    
    # Set cookies
    DarsAuth.set_auth_cookies(response, access_token, refresh_token, xsrf_token)
    
    return {"status": "success", "user": user_payload}

@auth_router.post("/refresh")
async def refresh(request: Request, response: Response):
    """
    Uses the refresh token cookie to issue a new access token.
    """
    if not _session_manager or not _app_secret:
        raise HTTPException(status_code=500, detail="Auth not configured")
        
    refresh_token = request.cookies.get("dars_refresh_token")
    if not refresh_token:
        raise HTTPException(status_code=401, detail="No refresh token")
        
    session = _session_manager.validate_refresh_token(refresh_token)
    if not session:
        # Invalid or expired refresh token. Clear cookies.
        DarsAuth.clear_auth_cookies(response)
        raise HTTPException(status_code=401, detail="Invalid refresh token")
        
    # Generate new tokens
    user_payload = session["payload"]
    user_id = session["user_id"]
    
    # Revoke old refresh token and issue a new one (Refresh Token Rotation)
    _session_manager.revoke_refresh_token(refresh_token)
    new_refresh_token = _session_manager.issue_refresh_token(user_id, user_payload, expires_in=604800)
    
    new_access_token = DarsAuth.encode_token(user_payload, _app_secret, expires_in=900)
    xsrf_token = secrets.token_urlsafe(32)
    
    DarsAuth.set_auth_cookies(response, new_access_token, new_refresh_token, xsrf_token)
    
    return {"status": "success"}

@auth_router.post("/logout")
async def logout(request: Request, response: Response):
    """
    Revokes the refresh token and clears auth cookies.
    """
    if _session_manager:
        refresh_token = request.cookies.get("dars_refresh_token")
        if refresh_token:
            _session_manager.revoke_refresh_token(refresh_token)
            
    DarsAuth.clear_auth_cookies(response)
    return {"status": "success"}

@auth_router.get("/me")
@requires_auth
async def get_me(request: Request):
    """
    Returns the currently authenticated user's data.
    Protected by requires_auth (needs valid access token).
    """
    return {"user": request.state.user}
