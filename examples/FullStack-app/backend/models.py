"""
Dars Data Layer - Model Definitions for FullStack App.

Uses DarsModel + SQLite via Database for persistence.
Auto-generates CRUD API via register_model_api().
"""

import datetime
from dars.backend.models import DarsModel, TextField, FloatField, BooleanField, DateTimeField
from dars.backend.database import Database


class Product(DarsModel):
    __tablename__ = "products"
    name = TextField(nullable=False)
    price = FloatField(default=0.0)
    description = TextField(default="")
    category = TextField(default="general")
    published = BooleanField(default=False)
    created_at = DateTimeField(auto_now=True)


def get_db() -> Database:
    """Get or create the application database with registered models."""
    import os
    db_path = os.environ.get(
        "DARS_DB_PATH",
        os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "app.db"),
    )
    db = Database(db_path)
    db.register(Product)
    db.create_all()
    return db
