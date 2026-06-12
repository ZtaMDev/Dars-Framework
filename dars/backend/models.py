from __future__ import annotations

"""
Dars Model Layer — Declarative ORM for SQLite with auto-generated CRUD API.

Provides:
- ``DarsModel`` — declarative model base class
- Field types: ``IntegerField``, ``TextField``, ``FloatField``, ``BooleanField``,
  ``DateTimeField``, ``JSONField``, ``ForeignKey``
- ``ModelManager`` — per-model query API (``all()``, ``get()``, ``filter()``, etc.)
- ``ModelAPI`` — auto-generated FastAPI CRUD router
- ``register_model_api()`` — wire up CRUD endpoints on a FastAPI app

Usage::

    from dars.backend.models import DarsModel, TextField, IntegerField
    from dars.backend.database import Database

    class Product(DarsModel):
        __tablename__ = "products"
        name = TextField(nullable=False)
        price = IntegerField(default=0)

    db = Database("app.db")
    db.register(Product)
    db.create_all()

    # Create
    product = Product(name="Widget", price=99)
    product.save()

    # Query
    all_products = Product.objects.all()
    cheap = Product.objects.filter(price=0)
"""

import json
import datetime
from typing import Any, Optional, ClassVar, Type, TYPE_CHECKING

from fastapi import HTTPException
from fastapi.responses import JSONResponse

if TYPE_CHECKING:
    from dars.backend.database import Database


# ---------------------------------------------------------------------------
# Field types
# ---------------------------------------------------------------------------

class Field:
    """Base field descriptor shared by all column types."""

    sql_type: str = "TEXT"
    name: str = ""
    primary_key: bool = False
    nullable: bool = True
    unique: bool = False
    index: bool = False
    default: Any = None
    autoincrement: bool = False
    references: Optional[str] = None

    def __init__(
        self,
        default: Any = None,
        nullable: bool = True,
        primary_key: bool = False,
        unique: bool = False,
        index: bool = False,
    ) -> None:
        self.default = default
        self.nullable = nullable
        self.primary_key = primary_key
        self.unique = unique
        self.index = index
        self.autoincrement = False

    def __set_name__(self, owner: type, name: str) -> None:
        self.name = name


class IntegerField(Field):
    sql_type = "INTEGER"

    def __init__(
        self,
        default: Any = None,
        nullable: bool = True,
        primary_key: bool = False,
        unique: bool = False,
        index: bool = False,
    ) -> None:
        super().__init__(default, nullable, primary_key, unique, index)
        self.autoincrement = primary_key


class TextField(Field):
    sql_type = "TEXT"


class FloatField(Field):
    sql_type = "REAL"


class BooleanField(Field):
    sql_type = "INTEGER"

    def __init__(
        self,
        default: bool = False,
        nullable: bool = True,
        **kwargs,
    ) -> None:
        super().__init__(int(default) if isinstance(default, bool) else default, nullable, **kwargs)


class DateTimeField(Field):
    sql_type = "TEXT"

    def __init__(
        self,
        auto_now: bool = False,
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        self.auto_now = auto_now


class JSONField(Field):
    sql_type = "TEXT"

    def __init__(self, default: Any = None, nullable: bool = True, **kwargs) -> None:
        super().__init__(default, nullable, **kwargs)


class ForeignKey(Field):
    """Foreign key field referencing another table.

    Args:
        model: The referenced model class (e.g., ``User``).
        on_delete: CASCADE, SET NULL, or RESTRICT (default: CASCADE).
    """

    sql_type = "INTEGER"

    def __init__(
        self,
        model: Type[DarsModel],
        on_delete: str = "CASCADE",
        nullable: bool = True,
        **kwargs,
    ) -> None:
        super().__init__(nullable=nullable, **kwargs)
        self.references = f"{model._table_name}(id)"
        self.referenced_model = model
        self.on_delete = on_delete


# ---------------------------------------------------------------------------
# ModelManager — per-class query interface
# ---------------------------------------------------------------------------

class ModelManager:
    """
    Query API for a single model.

    Accessed via ``MyModel.objects``.
    """

    def __init__(self, model_cls: Type[DarsModel]) -> None:
        self.model = model_cls

    @property
    def _db(self) -> Database:
        db = self.model._db
        if db is None:
            raise RuntimeError(
                f"Model {self.model.__name__} has not been registered with a Database. "
                "Call db.register(MyModel) first."
            )
        return db

    def all(self) -> list[DarsModel]:
        """Return all rows as model instances."""
        rows = self._db.fetch_all(f"SELECT * FROM {self.model._table_name}")
        return [self._row_to_model(r) for r in rows]

    def get(self, id: int) -> Optional[DarsModel]:
        """Return a single row by primary key, or ``None``."""
        row = self._db.fetch_one(
            f"SELECT * FROM {self.model._table_name} WHERE id = ?", (id,)
        )
        return self._row_to_model(row) if row else None

    def filter(self, **kwargs) -> list[DarsModel]:
        """Return rows matching keyword field=value conditions."""
        if not kwargs:
            return self.all()
        clauses = []
        params = []
        for key, value in kwargs:
            clauses.append(f"{key} = ?")
            params.append(self._serialize_field(key, value))
        sql = f"SELECT * FROM {self.model._table_name} WHERE {' AND '.join(clauses)}"
        rows = self._db.fetch_all(sql, tuple(params))
        return [self._row_to_model(r) for r in rows]

    def count(self) -> int:
        """Return the number of rows."""
        row = self._db.fetch_one(f"SELECT COUNT(*) AS cnt FROM {self.model._table_name}")
        return row["cnt"] if row else 0

    def create(self, **kwargs) -> DarsModel:
        """Create and persist a new instance."""
        instance = self.model(**kwargs)
        instance.save()
        return instance

    def delete(self, id: int) -> bool:
        """Delete a row by primary key. Returns ``True`` if a row was deleted."""
        cur = self._db.execute(
            f"DELETE FROM {self.model._table_name} WHERE id = ?", (id,)
        )
        self._db.connection.commit()
        return cur.rowcount > 0

    def _row_to_model(self, row) -> DarsModel:
        data = dict(row)
        instance = self.model.__new__(self.model)
        object.__setattr__(instance, '_db', self._db)
        object.__setattr__(instance, '_exists', True)
        object.__setattr__(instance, '_data', {})
        for field_name, field in self.model._fields.items():
            raw = data.get(field_name)
            instance._data[field_name] = self._deserialize_field(field, raw)
        return instance

    def _serialize_field(self, field_name: str, value: Any) -> Any:
        field = self.model._fields.get(field_name)
        if isinstance(field, JSONField) and value is not None:
            return json.dumps(value)
        if isinstance(field, BooleanField):
            return 1 if value else 0
        if isinstance(field, DateTimeField) and isinstance(value, datetime.datetime):
            return value.isoformat()
        return value

    def _deserialize_field(self, field, value: Any) -> Any:
        if isinstance(field, JSONField) and isinstance(value, str):
            try:
                return json.loads(value)
            except (json.JSONDecodeError, TypeError):
                return value
        if isinstance(field, BooleanField):
            return bool(value) if value is not None else None
        if isinstance(field, DateTimeField) and isinstance(value, str):
            try:
                return datetime.datetime.fromisoformat(value)
            except (ValueError, TypeError):
                return value
        return value


# ---------------------------------------------------------------------------
# DarsModel metaclass
# ---------------------------------------------------------------------------

class ModelMeta(type):
    """Metaclass that collects field definitions for each model subclass."""

    def __new__(mcs, name: str, bases: tuple, namespace: dict) -> type:
        cls = super().__new__(mcs, name, bases, namespace)

        if name == "DarsModel" and not bases:
            return cls

        fields: dict[str, Field] = {}
        # Collect fields from base classes first
        for base in bases:
            if hasattr(base, "_fields"):
                fields.update(base._fields)

        # Collect from current namespace
        for attr_name, attr_value in namespace.items():
            if isinstance(attr_value, Field):
                attr_value.name = attr_name
                fields[attr_name] = attr_value

        cls._fields = fields
        cls._table_name = namespace.get("__tablename__", name.lower())
        cls.objects = ModelManager(cls)

        return cls


# ---------------------------------------------------------------------------
# DarsModel base class
# ---------------------------------------------------------------------------

class DarsModel(metaclass=ModelMeta):
    """
    Declarative model base class.

    Subclasses define fields as class attributes. Each instance represents
    a row in the database.

    Usage::

        class Product(DarsModel):
            __tablename__ = "products"
            name = TextField(nullable=False)
            price = IntegerField(default=0)
    """

    # Set by Database.register()
    _db: Optional[Database] = None
    _fields: ClassVar[dict[str, Field]] = {}
    _table_name: ClassVar[str] = ""

    def __init__(self, **kwargs) -> None:
        object.__setattr__(self, '_data', {})
        object.__setattr__(self, '_exists', False)

        for field_name, field in self._fields.items():
            if field_name in kwargs:
                value = kwargs[field_name]
            elif field.default is not None:
                value = field.default() if callable(field.default) else field.default
            else:
                value = None

            # Serialize complex types
            if isinstance(field, JSONField) and value is not None and not isinstance(value, str):
                value = json.dumps(value)
            elif isinstance(field, BooleanField) and value is not None:
                value = bool(value) if not isinstance(value, bool) else value
            elif isinstance(field, DateTimeField) and field.auto_now and value is None:
                value = datetime.datetime.utcnow().isoformat()
            elif isinstance(field, DateTimeField) and isinstance(value, datetime.datetime):
                value = value.isoformat()

            self._data[field_name] = value

    # ------------------------------------------------------------------
    # Attribute access — map ``self.field`` to ``self._data[field]``
    # ------------------------------------------------------------------

    def __getattr__(self, name: str) -> Any:
        if name in ('_data', '_exists', '_db', '_fields', '_table_name'):
            raise AttributeError(name)
        if name.startswith("_"):
            raise AttributeError(name)
        data = object.__getattribute__(self, '_data')
        if name in object.__getattribute__(self, '_fields'):
            return data.get(name)
        raise AttributeError(f"'{type(self).__name__}' has no attribute '{name}'")

    def __setattr__(self, name: str, value: Any) -> None:
        if name.startswith("_") or name not in self._fields:
            object.__setattr__(self, name, value)
        else:
            object.__getattribute__(self, '_data')[name] = value

    # ------------------------------------------------------------------
    # Persistence
    # ------------------------------------------------------------------

    def save(self) -> None:
        """Insert or update the row."""
        db = self._db
        if db is None:
            raise RuntimeError("Model not registered with a database. Call db.register() first.")

        table = self._table_name
        fields = [f for f in self._fields.values() if f.name and f.name != "id"]

        if self._exists and self._data.get("id") is not None:
            # UPDATE
            set_clause = ", ".join(f"{f.name} = ?" for f in fields)
            values = [self._data.get(f.name) for f in fields]
            values.append(self._data["id"])
            db.execute(f"UPDATE {table} SET {set_clause} WHERE id = ?", tuple(values))
        else:
            # INSERT
            col_names = ", ".join(f.name for f in fields)
            placeholders = ", ".join("?" for _ in fields)
            values = [self._data.get(f.name) for f in fields]
            cur = db.execute(
                f"INSERT INTO {table} ({col_names}) VALUES ({placeholders})",
                tuple(values),
            )
            self._data["id"] = cur.lastrowid
            self._exists = True

        db.connection.commit()

    def delete(self) -> None:
        """Delete the row from the database."""
        if not self._exists or self._data.get("id") is None:
            return
        db = self._db
        if db:
            db.execute(f"DELETE FROM {self._table_name} WHERE id = ?", (self._data["id"],))
            db.connection.commit()
            self._exists = False

    def to_dict(self) -> dict:
        """Return the row data as a plain dict."""
        return dict(self._data)

    def __repr__(self) -> str:
        pk = self._data.get("id", None)
        return f"<{type(self).__name__} id={pk}>"


# ---------------------------------------------------------------------------
# Auto-generated CRUD API (FastAPI router)
# ---------------------------------------------------------------------------

def register_model_api(app, db: "Database", prefix: str = "/api/models") -> None:
    """
    Auto-generate CRUD endpoints for all registered models.

    Endpoints generated for each model ``Product`` (table ``products``):

    - ``GET    {prefix}/products``        — list all
    - ``GET    {prefix}/products/{id}``   — get by id
    - ``POST   {prefix}/products``        — create
    - ``PUT    {prefix}/products/{id}``   — update
    - ``DELETE {prefix}/products/{id}``   — delete

    Args:
        app: FastAPI application instance.
        db: Database instance with registered models.
        prefix: URL prefix for all model endpoints.
    """
    from fastapi import APIRouter, HTTPException
    from fastapi.responses import JSONResponse
    from pydantic import create_model as pydantic_create_model

    router = APIRouter(prefix=prefix)

    for model_name, model_cls in db._models.items():
        table = model_cls._table_name

        # Dynamically create a Pydantic model for request validation
        field_defs = {}
        for fname, field in model_cls._fields.items():
            if fname == "id":
                continue
            py_type = _field_to_python_type(field)
            field_defs[fname] = (py_type, None)

        PydanticModel = pydantic_create_model(f"{model_name}Schema", **field_defs)

        _register_crud_routes(router, db, model_name, model_cls, table, PydanticModel)

    app.include_router(router)


def _register_crud_routes(router, db, model_name, model_cls, table, PydanticModel):
    """Register CRUD endpoints for a single model (avoids closure variable capture issues)."""

    @router.get(f"/{table}")
    async def list_all():
        rows = db.fetch_all(f"SELECT * FROM {table}")
        return JSONResponse([dict(r) for r in rows])

    @router.get(f"/{table}/{{item_id}}")
    async def get_one(item_id: int):
        row = db.fetch_one(f"SELECT * FROM {table} WHERE id = ?", (item_id,))
        if not row:
            raise HTTPException(status_code=404, detail=f"{model_name} not found")
        return JSONResponse(dict(row))

    async def create_item(data): # type: ignore
        # Fix FastAPI resolving PydanticModel as a string due to __future__ annotations

        fields = [f for f in model_cls._fields.values() if f.name and f.name != "id"]
        col_names = ", ".join(f.name for f in fields)
        placeholders = ", ".join("?" for _ in fields)
        values = [getattr(data, f.name) for f in fields]
        cur = db.execute(
            f"INSERT INTO {table} ({col_names}) VALUES ({placeholders})",
            tuple(values),
        )
        db.connection.commit()
        row = db.fetch_one(f"SELECT * FROM {table} WHERE id = ?", (cur.lastrowid,))
        return JSONResponse(dict(row), status_code=201)
    
    create_item.__annotations__['data'] = PydanticModel
    router.post(f"/{table}")(create_item)

    async def update_item(item_id: int, data): # type: ignore
        existing = db.fetch_one(f"SELECT * FROM {table} WHERE id = ?", (item_id,))
        if not existing:
            raise HTTPException(status_code=404, detail=f"{model_name} not found")
        fields = [f for f in model_cls._fields.values() if f.name and f.name != "id"]
        set_clause = ", ".join(f"{f.name} = ?" for f in fields)
        values = [getattr(data, f.name) for f in fields]
        values.append(item_id)
        db.execute(f"UPDATE {table} SET {set_clause} WHERE id = ?", tuple(values))
        db.connection.commit()
        row = db.fetch_one(f"SELECT * FROM {table} WHERE id = ?", (item_id,))
        return JSONResponse(dict(row))
    
    update_item.__annotations__['data'] = PydanticModel
    router.put(f"/{table}/{{item_id}}")(update_item)

    @router.delete(f"/{table}/{{item_id}}")
    async def delete_item(item_id: int):
        existing = db.fetch_one(f"SELECT * FROM {table} WHERE id = ?", (item_id,))
        if not existing:
            raise HTTPException(status_code=404, detail=f"{model_name} not found")
        db.execute(f"DELETE FROM {table} WHERE id = ?", (item_id,))
        db.connection.commit()
        return JSONResponse({"deleted": True})


def _field_to_python_type(field) -> type:
    """Map a Dars Field to its closest Python type."""
    if isinstance(field, IntegerField):
        return int
    if isinstance(field, FloatField):
        return float
    if isinstance(field, BooleanField):
        return bool
    if isinstance(field, JSONField):
        return str
    if isinstance(field, ForeignKey):
        return int
    return str
