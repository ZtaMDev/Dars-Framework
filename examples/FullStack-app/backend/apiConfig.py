import os
import sys


class DarsEnv:
    # ── Mode ──────────────────────────────────────────────────────────────────
    # Set to "production" before deploying, or set DARS_MODE env var.
    # dars dev  → development (two servers, CORS enabled)
    # Production deploy   → change to "production" (one server, serves frontend)
    MODE = os.environ.get("DARS_MODE", "development")

    DEV   = "development"
    BUILD = "production"

    @staticmethod
    def get_env():
        return DarsEnv.MODE

    @staticmethod
    def is_dev():
        return DarsEnv.get_env() == DarsEnv.DEV

    @staticmethod
    def get_urls():
        """
        Development:  two separate servers (dars dev + dars dev --backend)
        Production:   single server, same origin — backend serves the frontend
        """
        if DarsEnv.is_dev():
            return {
                "backend":  os.environ.get("DARS_BACKEND_URL",  "http://localhost:3000"),
                "frontend": os.environ.get("DARS_FRONTEND_URL", "http://localhost:4000"),
            }
        # Production: same origin — all requests go to the same server
        return {
            "backend":  os.environ.get("DARS_BACKEND_URL",  "/"),
            "frontend": os.environ.get("DARS_FRONTEND_URL", "/"),
        }

    @staticmethod
    def get_frontend_dist_dir() -> str:
        """
        Return the absolute path to the frontend static files directory.

        In production the backend serves the Dars export (dist/) as static files
        so that frontend and API share the same origin.

        Resolution order:
          1. DARS_FRONTEND_DIR env var (explicit override)
          2. outdir from dars.config.json in the project root
          3. Fallback: <project_root>/dist
        """
        # Env var override
        env_dir = os.environ.get("DARS_FRONTEND_DIR", "")
        if env_dir and os.path.isdir(env_dir):
            return env_dir

        # Walk up from backend/ to find dars.config.json
        backend_dir  = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(backend_dir)

        config_path = os.path.join(project_root, "dars.config.json")
        if os.path.isfile(config_path):
            try:
                import json
                with open(config_path, "r", encoding="utf-8") as f:
                    cfg = json.load(f)
                outdir = cfg.get("outdir", "dist")
                # outdir may be relative or absolute
                if not os.path.isabs(outdir):
                    outdir = os.path.join(project_root, outdir)
                return os.path.normpath(outdir)
            except Exception:
                pass

        # Fallback
        return os.path.join(project_root, "dist")
