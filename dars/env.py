# Dars Framework - Core Source File
#
# This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0.
# If a copy of the MPL was not distributed with this file, You can obtain one at
# https://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2025 ZtaDev
"""
Environment configuration for the Dars Framework.

Provides :class:`DarsEnv` for dev/prod mode tracking and `.env` file loading.
"""

import os
from typing import Optional, Tuple


class DarsEnv:
    """
    Environment configuration for Dars Framework.

    Attributes:
        dev (bool): ``True`` in development mode, ``False`` in production (bundle).
    """

    _dev_override: Optional[bool] = None
    dev: bool = os.environ.get("DARS_MODE", "development").strip().lower() != "production"

    @classmethod
    def set_dev_mode(cls, is_dev: bool) -> None:
        """Set the development mode flag."""
        cls.dev = is_dev
        cls._dev_override = is_dev

    @classmethod
    def get_env(cls) -> str:
        """Return the current DARS_MODE environment setting."""
        return os.environ.get("DARS_MODE", "development")

    @classmethod
    def is_dev(cls) -> bool:
        """Return whether the current environment is development."""
        return cls.dev

    @classmethod
    def _sync_dev_mode(cls) -> None:
        if cls._dev_override is None:
            cls.dev = cls.get_env().strip().lower() != "production"

    # ------------------------------------------------------------------
    # .env file support
    # ------------------------------------------------------------------

    @classmethod
    def load(cls, path: str = ".env") -> None:
        """
        Load key-value pairs from a ``.env`` file into :data:`os.environ`.

        Rules:

        - Silently returns if the file does not exist.
        - Ignores blank lines and lines whose first non-whitespace character is ``#``.
        - Splits on the **first** ``=`` only, so values may contain ``=``.
        - Strips surrounding single or double quotes from values.
        - Does **not** overwrite keys already present in :data:`os.environ`.

        Args:
            path: Path to the ``.env`` file (default: ``".env"``).
        """
        if not os.path.isfile(path):
            cls._sync_dev_mode()
            return
        try:
            with open(path, "r", encoding="utf-8") as f:
                for line in f:
                    parsed = cls._parse_env_line(line)
                    if parsed is None:
                        continue
                    key, value = parsed
                    if key and key not in os.environ:
                        os.environ[key] = value
        except OSError:
            # Best-effort: never raise on load failure
            pass
        finally:
            cls._sync_dev_mode()

    @classmethod
    def get(cls, key: str, default: Optional[str] = None) -> Optional[str]:
        """
        Return the value of an environment variable.

        Args:
            key: Variable name.
            default: Value returned when the key is absent (default: ``None``).

        Returns:
            The variable value or *default*.
        """
        return os.environ.get(key, default)

    @classmethod
    def require(cls, key: str) -> str:
        """
        Return the value of a required environment variable.

        Args:
            key: Variable name.

        Returns:
            The variable value.

        Raises:
            KeyError: If *key* is not set in :data:`os.environ`.
        """
        value = os.environ.get(key)
        if value is None:
            raise KeyError(
                f"Required environment variable '{key}' is not set. "
                "Add it to your .env file or set it in the environment."
            )
        return value

    @staticmethod
    def _parse_env_line(line: str) -> Optional[Tuple[str, str]]:
        """
        Parse a single ``.env`` line into a ``(key, value)`` tuple.

        Returns ``None`` for blank lines and comments.

        Args:
            line: Raw line from the ``.env`` file.

        Returns:
            ``(key, value)`` or ``None``.
        """
        stripped = line.strip()
        # Skip blank lines and comments
        if not stripped or stripped.startswith("#"):
            return None
        # Split on the first '=' only
        if "=" not in stripped:
            return None
        key, _, value = stripped.partition("=")
        key = key.strip()
        value = value.strip()
        if not key:
            return None
        # Strip surrounding quotes (single or double)
        if len(value) >= 2 and value[0] == value[-1] and value[0] in ('"', "'"):
            value = value[1:-1]
        return key, value
