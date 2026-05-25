# Dars Framework - Backend Session Module
#
# This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0.
# If a copy of the MPL was not distributed with this file, You can obtain one at
# https://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2026 ZtaDev

import time
import secrets
from typing import Dict, Optional, Protocol, Any

class SessionStore(Protocol):
    """
    Protocol for Dars Session Stores.
    Handles the storage, retrieval, and invalidation of refresh tokens.
    """
    def create_session(self, user_id: str, payload: dict, expires_in: int) -> str:
        ...

    def get_session(self, refresh_token: str) -> Optional[dict]:
        ...

    def revoke_session(self, refresh_token: str) -> bool:
        ...

    def cleanup_expired(self) -> int:
        ...


class InMemorySessionStore:
    """
    Default in-memory session store for development or single-node deployments.
    Stores sessions in a Python dict. Not recommended for multi-instance deployments.
    """
    def __init__(self):
        # Maps refresh_token -> {"user_id": str, "payload": dict, "exp": int}
        self._sessions: Dict[str, dict] = {}

    def create_session(self, user_id: str, payload: dict, expires_in: int) -> str:
        refresh_token = secrets.token_urlsafe(64)
        exp = int(time.time()) + expires_in
        self._sessions[refresh_token] = {
            "user_id": user_id,
            "payload": payload,
            "exp": exp
        }
        return refresh_token

    def get_session(self, refresh_token: str) -> Optional[dict]:
        session = self._sessions.get(refresh_token)
        if not session:
            return None
        if session["exp"] < time.time():
            self.revoke_session(refresh_token)
            return None
        return session

    def revoke_session(self, refresh_token: str) -> bool:
        if refresh_token in self._sessions:
            del self._sessions[refresh_token]
            return True
        return False

    def cleanup_expired(self) -> int:
        now = time.time()
        expired = [t for t, s in self._sessions.items() if s["exp"] < now]
        for t in expired:
            del self._sessions[t]
        return len(expired)


class SessionManager:
    """
    Manages the lifecycle of user sessions.
    """
    def __init__(self, store: SessionStore):
        self.store = store
        
    def issue_refresh_token(self, user_id: str, payload: dict, expires_in: int = 604800) -> str:
        """
        Issues a new refresh token and saves it to the store.
        Default expiration is 7 days (604800 seconds).
        """
        return self.store.create_session(user_id, payload, expires_in)
        
    def validate_refresh_token(self, refresh_token: str) -> Optional[dict]:
        """
        Validates a refresh token and returns the session payload if valid.
        """
        return self.store.get_session(refresh_token)
        
    def revoke_refresh_token(self, refresh_token: str) -> bool:
        """
        Revokes a refresh token.
        """
        return self.store.revoke_session(refresh_token)

