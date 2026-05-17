# Dars Framework - Core Source File
#
# This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0.
# If a copy of the MPL was not distributed with this file, You can obtain one at
# https://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2025 ZtaDev
"""
JsonStore — simple file-backed key-value store for rapid prototyping.

Provides thread-safe, atomic-write persistence without requiring a full database.

Example::

    from dars.backend.store import JsonStore

    store = JsonStore("data.json", default={"users": []})
    store.set("users", [{"name": "Alice"}])
    users = store.get("users")          # [{"name": "Alice"}]
    store.delete("users")
    store.clear()
"""

import json
import os
import threading
from copy import deepcopy
from typing import Any, Optional


class JsonStore:
    """
    File-backed key-value store with atomic writes and thread safety.

    All mutating operations (``set``, ``delete``, ``clear``) acquire a
    per-instance :class:`threading.Lock` and write to a temporary file
    before atomically replacing the target file via :func:`os.replace`.

    Args:
        path: Path to the JSON file.  Created (with *default* contents) if
              it does not exist.
        default: Initial data written when the file is absent.  Defaults to
                 an empty dict.

    Raises:
        ValueError: If the file exists but contains malformed JSON.
    """

    def __init__(self, path: str, default: Optional[dict] = None) -> None:
        self._path = os.path.abspath(path)
        self._lock = threading.Lock()
        self._data: dict = {}

        if os.path.isfile(self._path):
            self._data = self._load()
        else:
            self._data = dict(default) if default else {}
            # Ensure parent directories exist before writing
            os.makedirs(os.path.dirname(self._path) or ".", exist_ok=True)
            self._save()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def get(self, key: str, default: Any = None) -> Any:
        """
        Return the value for *key*, or *default* if absent.

        Args:
            key: Key to look up.
            default: Fallback value (default: ``None``).
        """
        return deepcopy(self._data.get(key, default))

    def set(self, key: str, value: Any) -> None:
        """
        Store *value* under *key* and persist to disk atomically.

        Args:
            key: Key to write.
            value: JSON-serializable value.
        """
        with self._lock:
            self._data[key] = value
            self._save()

    def delete(self, key: str) -> None:
        """
        Remove *key* from the store and persist the change.

        Args:
            key: Key to remove.  No-op if the key does not exist.
        """
        with self._lock:
            self._data.pop(key, None)
            self._save()

    def all(self) -> dict:
        """Return a shallow copy of the entire in-memory store."""
        return dict(self._data)

    def clear(self) -> None:
        """Empty the store and persist an empty dict to disk."""
        with self._lock:
            self._data = {}
            self._save()

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _load(self) -> dict:
        """Read and parse the JSON file.

        Raises:
            ValueError: On malformed JSON.
        """
        try:
            with open(self._path, "r", encoding="utf-8") as f:
                data = json.load(f)
            if not isinstance(data, dict):
                raise ValueError(
                    f"JsonStore: expected a JSON object at the top level in '{self._path}', "
                    f"got {type(data).__name__}."
                )
            return data
        except json.JSONDecodeError as exc:
            raise ValueError(
                f"JsonStore: malformed JSON in '{self._path}': {exc}"
            ) from exc

    def _save(self) -> None:
        """Atomically write ``_data`` to disk (write temp → rename)."""
        tmp = self._path + ".tmp"
        try:
            with open(tmp, "w", encoding="utf-8") as f:
                json.dump(self._data, f, indent=2, ensure_ascii=False)
            os.replace(tmp, self._path)
        except Exception:
            # Clean up temp file on failure; propagate the original error
            try:
                os.remove(tmp)
            except OSError:
                pass
            raise
