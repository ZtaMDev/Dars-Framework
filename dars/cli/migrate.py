"""
CLI commands for database schema management.

Usage::

    dars migrate          -- Auto-create all registered tables
    dars migrate --check  -- Show pending migrations without running them
    dars migrate --drop   -- Drop all tables (destructive!)
"""

import ast
import os
import sys
import argparse
from pathlib import Path


def _get_project_root() -> Path:
    """Walk up from cwd to find the project root (where ``main.py`` or ``dars.config.json`` lives)."""
    cwd = Path.cwd()
    for parent in [cwd] + list(cwd.parents):
        if (parent / "main.py").exists() or (parent / "dars.config.json").exists():
            return parent
    return cwd


def _discover_models() -> list:
    """
    Scan the project's ``backend/`` directory for Python files that import and
    subclass ``DarsModel``. Returns a list of model classes.
    
    This is a simple heuristic: it looks for files that contain
    ``class ...(DarsModel)`` and tries to import them.
    """
    root = _get_project_root()
    backend_dir = root / "backend"
    if not backend_dir.exists():
        print("No backend/ directory found. Create models in backend/models.py first.")
        return []

    models = []
    sys.path.insert(0, str(root))

    for pyfile in sorted(backend_dir.glob("**/*.py")):
        if pyfile.name.startswith("_"):
            continue
        try:
            with open(pyfile, encoding="utf-8") as f:
                source = f.read()
            tree = ast.parse(source)
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    for base in node.bases:
                        if isinstance(base, ast.Name) and base.id == "DarsModel":
                            # Try to import it
                            rel_path = pyfile.relative_to(root).with_suffix("")
                            module_path = ".".join(rel_path.parts)
                            try:
                                mod = __import__(module_path, fromlist=[node.name])
                                cls = getattr(mod, node.name)
                                models.append(cls)
                            except (ImportError, AttributeError) as e:
                                print(f"  Warning: could not import {node.name} from {module_path}: {e}")
        except SyntaxError:
            pass

    return models


def run_migrate(args: argparse.Namespace) -> None:
    """Execute the ``dars migrate`` command."""
    from dars.backend.database import Database
    from dars.backend.models import DarsModel

    models = _discover_models()

    if not models:
        print("No DarsModel subclasses found.")
        return

    # Filter to only DarsModel subclasses (not DarsModel itself)
    models = [m for m in models if m is not DarsModel and issubclass(m, DarsModel)]

    if not models:
        print("No DarsModel subclasses found.")
        return

    print(f"Found {len(models)} model(s):")
    for m in models:
        print(f"  - {m.__name__} (table: {m._table_name})")

    if args.check:
        print("\nRun `dars migrate` to create these tables.")
        return

    if args.drop:
        confirm = input("\nWARNING: Dropping all tables! Type 'yes' to confirm: ")
        if confirm.lower() != "yes":
            print("Aborted.")
            return

    db_path = os.environ.get("DARS_DB_PATH", os.path.join(str(_get_project_root()), "app.db"))
    db = Database(db_path)
    db.register(*models)

    if args.drop:
        db.drop_all()
        print(f"Dropped all tables from {db_path}")
        return

    db.create_all()
    print(f"\nCreated tables in {db_path}")
    print("Migration complete.")


def add_subparser(subparsers) -> None:
    """Register the ``migrate`` subcommand."""
    parser = subparsers.add_parser(
        "migrate",
        help="Database migration management",
        description="Create, check, or drop database tables for registered DarsModel classes.",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Show pending migrations without running them",
    )
    parser.add_argument(
        "--drop",
        action="store_true",
        help="Drop all registered tables (destructive!)",
    )
    parser.set_defaults(func=run_migrate)
