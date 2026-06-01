"""
Dars Database Layer — SQLite connection manager with schema management.

Provides:
- ``Database`` — connection manager for SQLite with auto-migration tracking
- ``register_models()`` — wraps models with a database connection

Usage::

    from dars.backend.database import Database
    from dars.backend.models import DarsModel, TextField, IntegerField

    class User(DarsModel):
        __tablename__ = "users"
        name = TextField()
        email = TextField(unique=True)
        age = IntegerField()

    db = Database("app.db")
    db.register(User)
    db.create_all()

    user = User(name="Alice", email="alice@example.com", age=30)
    db.session.add(user)
    db.session.commit()
"""

from __future__ import annotations

import sqlite3
import threading
import os
from typing import Any, Optional, Type, TYPE_CHECKING

if TYPE_CHECKING:
    from dars.backend.models import DarsModel

# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------

def _get_column_sql(field) -> str:
    """Return the SQL fragment for a single column."""
    parts = [field.name, field.sql_type]

    if getattr(field, "primary_key", False):
        parts.append("PRIMARY KEY")
        if getattr(field, "autoincrement", True):
            parts.append("AUTOINCREMENT")

    if not field.nullable:
        parts.append("NOT NULL")

    if getattr(field, "unique", False):
        parts.append("UNIQUE")

    default = field.default
    if default is not None:
        if isinstance(default, str):
            parts.append(f"DEFAULT '{default}'")
        elif isinstance(default, bool):
            parts.append(f"DEFAULT {'1' if default else '0'}")
        else:
            parts.append(f"DEFAULT {default}")

    return " ".join(parts)


def _get_foreign_key_sql(field) -> Optional[str]:
    """Return a FOREIGN KEY constraint fragment, or None."""
    ref = getattr(field, "references", None)
    if ref:
        return f"FOREIGN KEY ({field.name}) REFERENCES {ref}"
    return None


# ---------------------------------------------------------------------------
# Database
# ---------------------------------------------------------------------------

class Database:
    """
    SQLite connection manager with schema tracking.

    Thread-safe: each thread gets its own connection via ``threading.local``.

    Args:
        path: Path to the SQLite file (``":memory:"`` for in-memory).
    """

    def __init__(self, path: str = ":memory:") -> None:
        self.path = path
        self._local = threading.local()
        self._models: dict[str, Type[DarsModel]] = {}
        self._lock = threading.Lock()
        self._migrations_table = "_dars_schema_version"

        # Ensure parent directory exists for file-based databases
        if path and path != ":memory:":
            parent = os.path.dirname(os.path.abspath(path))
            if parent:
                os.makedirs(parent, exist_ok=True)

    # ------------------------------------------------------------------
    # Connection management
    # ------------------------------------------------------------------

    @property
    def connection(self) -> sqlite3.Connection:
        """Get the connection for the current thread (auto-created)."""
        if not hasattr(self._local, "conn") or self._local.conn is None:
            self._local.conn = self._create_connection()
        return self._local.conn

    def _create_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.path, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA journal_mode=WAL;")
        conn.execute("PRAGMA foreign_keys=ON;")
        return conn

    def close(self) -> None:
        """Close the connection for the current thread."""
        if hasattr(self._local, "conn") and self._local.conn:
            self._local.conn.close()
            self._local.conn = None

    def close_all(self) -> None:
        """Close the connection for the current thread (same as :meth:`close`)."""
        self.close()

    # ------------------------------------------------------------------
    # Model registration & schema management
    # ------------------------------------------------------------------

    def register(self, *models: Type[DarsModel]) -> None:
        """
        Register one or more model classes with this database.

        Sets ``model._db`` on each class so that ``model.objects`` works.
        """
        with self._lock:
            for model in models:
                name = model.__name__
                model._db = self
                self._models[name] = model
                model._fields["id"] = _AutoIntegerField()

    def create_all(self) -> None:
        """Create all registered tables that do not yet exist."""
        with self._lock:
            self._ensure_migrations_table()
            for name, model in self._models.items():
                self._create_table(model)

    def _ensure_migrations_table(self) -> None:
        self.connection.execute(
            f"CREATE TABLE IF NOT EXISTS {self._migrations_table} ("
            "model_name TEXT PRIMARY KEY, "
            "version INTEGER DEFAULT 1"
            ")"
        )
        self.connection.commit()

    def _create_table(self, model: Type[DarsModel]) -> None:
        table = model._table_name
        columns = []
        foreign_keys = []

        for field in model._fields.values():
            if not field.name:
                continue
            columns.append(_get_column_sql(field))
            fk = _get_foreign_key_sql(field)
            if fk:
                foreign_keys.append(fk)

        sql = f"CREATE TABLE IF NOT EXISTS {table} (\n  " + ",\n  ".join(columns + foreign_keys) + "\n)"
        self.connection.execute(sql)
        self.connection.execute(
            f"INSERT OR REPLACE INTO {self._migrations_table} (model_name, version) VALUES (?, ?)",
            (model.__name__, 1),
        )
        self.connection.commit()

    def drop_all(self) -> None:
        """Drop all registered tables."""
        with self._lock:
            for model in self._models.values():
                self.connection.execute(f"DROP TABLE IF EXISTS {model._table_name}")
            self.connection.execute(f"DROP TABLE IF EXISTS {self._migrations_table}")
            self.connection.commit()

    # ------------------------------------------------------------------
    # Query helpers
    # ------------------------------------------------------------------

    def execute(self, sql: str, params: tuple = ()) -> sqlite3.Cursor:
        """Execute a raw SQL query and return the cursor."""
        return self.connection.execute(sql, params)

    def fetch_all(self, sql: str, params: tuple = ()) -> list[sqlite3.Row]:
        """Execute a query and return all rows as ``sqlite3.Row`` objects."""
        return self.connection.execute(sql, params).fetchall()

    def fetch_one(self, sql: str, params: tuple = ()) -> Optional[sqlite3.Row]:
        """Execute a query and return one row or ``None``."""
        cur = self.connection.execute(sql, params)
        return cur.fetchone()

    # ------------------------------------------------------------------
    # Convenience
    # ------------------------------------------------------------------

    def table_exists(self, table_name: str) -> bool:
        """Check whether a table exists in the database."""
        row = self.fetch_one(
            "SELECT name FROM sqlite_master WHERE type='table' AND name=?",
            (table_name,),
        )
        return row is not None


# ---------------------------------------------------------------------------
# Internal auto-increment field (used for model.id)
# ---------------------------------------------------------------------------

class _AutoIntegerField:
    """Minimal field descriptor used internally for the auto-generated ``id`` column."""
    name = "id"
    sql_type = "INTEGER"
    primary_key = True
    nullable = False
    unique = True
    default = None
    autoincrement = True
    references = None
