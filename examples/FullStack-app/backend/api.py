"""
Fullstack Backend - Dars Framework

Demonstrates:
  - SSRApp with middleware system (Auth, CORS, Logging, RateLimit, SecurityHeaders)
  - Data Layer: Database + DarsModel + auto CRUD API
  - Server Actions: @server_action decorator
  - Custom API routes with JsonStore (backward compatible)
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dars.backend.ssr import SSRApp
from dars.backend.middleware import (
    SecurityHeadersMiddleware,
    AuthMiddleware,
    CORSMiddleware,
    RateLimitMiddleware,
    LoggingMiddleware,
    CompressionMiddleware,
    DarsMiddleware,
)
from dars.backend.actions import server_action, register_actions_on_app
from dars.backend.models import register_model_api
# pyrefly: ignore [missing-import]
from backend.apiConfig import DarsEnv
# pyrefly: ignore [missing-import]
from backend.models import get_db, Product
# pyrefly: ignore [missing-import]
from main import app as dars_app

# ── Middleware (MUST be registered BEFORE SSRApp) ────────────────────────
dars_app.use(SecurityHeadersMiddleware, csp=None, hsts=True)

dars_app.use(
    LoggingMiddleware,
    include_paths=["/api/"],
    exclude_paths=["/api/ssr/"],
    log_headers=True,
    log_body=False,
    sensitive_headers=["authorization", "cookie", "x-auth-token"],
)

dars_app.use(
    RateLimitMiddleware,
    calls_per_minute=120,
)

dars_app.use(
    CompressionMiddleware,
    minimum_size=500,
)

# CORS (only needed in development)
urls = DarsEnv.get_urls()
if DarsEnv.is_dev():
    dars_app.use(
        CORSMiddleware,
        allow_origins=[urls["frontend"], "http://127.0.0.1:4000"],
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    )

# ── Database setup ────────────────────────────────────────────────────────
db = get_db()

# ── SSR app (applies middlewares from dars_app automatically) ────────────
ssr = SSRApp(dars_app, prefix="/api/ssr", title="Dars FullStack Demo - Backend")

# File upload endpoint
ssr.use_upload(
    upload_dir=os.path.join(os.path.dirname(os.path.dirname(__file__)), "uploads"),
    allowed_types=["image/png", "image/jpeg", "image/gif", "image/webp", "application/pdf"],
    max_size_bytes=10 * 1024 * 1024,
    path="/api/upload",
)

app = ssr.fastapi_app

# ── Auto-generated CRUD API for models ───────────────────────────────────
register_model_api(app, db, prefix="/api/models")

# Register actions on the FastAPI app
register_actions_on_app(app)

# ── Custom API routes (backward compatible with existing task manager) ────
# pyrefly: ignore [missing-import]
from fastapi import Request
# pyrefly: ignore [missing-import]
from fastapi.responses import JSONResponse
from dars.backend.store import JsonStore

_store = JsonStore(
    path=os.path.join(os.path.dirname(os.path.dirname(__file__)), "tasks_db.json"),
    default={"tasks": []},
)


@app.get("/api/tasks")
async def get_tasks():
    return JSONResponse({"tasks": _store.get("tasks", [])})


@app.post("/api/tasks")
async def create_task(request: Request):
    body = await request.json()
    tasks = _store.get("tasks", [])
    task = {"id": len(tasks) + 1, "title": body.get("title", ""), "done": False}
    tasks.append(task)
    _store.set("tasks", tasks)
    return JSONResponse(task, status_code=201)


@app.put("/api/tasks/{task_id}")
async def update_task(task_id: int, request: Request):
    body = await request.json()
    tasks = _store.get("tasks", [])
    for t in tasks:
        if t["id"] == task_id:
            t.update({k: v for k, v in body.items() if k != "id"})
            _store.set("tasks", tasks)
            return JSONResponse(t)
    return JSONResponse({"error": "Not found"}, status_code=404)


@app.post("/api/deltasks")
async def delete_task_post(request: Request):
    body = await request.json()
    name = body.get("title", "").strip()
    if not name:
        return JSONResponse({"error": "Title/name is required"}, status_code=400)
    tasks = _store.get("tasks", [])
    filtered_tasks = [t for t in tasks if t.get("title", "").strip().lower() != name.lower()]
    if len(filtered_tasks) < len(tasks):
        _store.set("tasks", filtered_tasks)
        return JSONResponse({"success": True, "message": f"Task '{name}' deleted"})
    return JSONResponse({"error": f"Task '{name}' not found"}, status_code=404)


@app.delete("/api/tasks/{task_id}")
async def delete_task(task_id: int):
    tasks = _store.get("tasks", [])
    tasks = [t for t in tasks if t["id"] != task_id]
    _store.set("tasks", tasks)
    return JSONResponse({"ok": True})


# ── Production: serve dist/ as static files with SPA fallback ─────────────
if not DarsEnv.is_dev():
    ssr.use_spa_fallback()


if __name__ == "__main__":
    # pyrefly: ignore [missing-import]
    import uvicorn
    print("\n" + "=" * 60)
    print("Dars FullStack Backend  [NEW: Data Layer + Middleware + Server Actions]")
    print("=" * 60)
    if DarsEnv.is_dev():
        print(f"  Backend:  {urls['backend']}")
        print(f"  Frontend: {urls['frontend']}  (run 'dars dev' separately)")
        print(f"  API Docs: {urls['backend']}/docs")
        print(f"  Models:   {urls['backend']}/api/models/products")
        print(f"  Actions:  {urls['backend']}/api/actions/get_product_stats")
        port, host = 3000, "127.0.0.1"
    else:
        frontend_dir = DarsEnv.get_frontend_dist_dir()
        print(f"  App:      http://0.0.0.0:8000  (frontend + API, same origin)")
        print(f"  Frontend: {frontend_dir}")
        port, host = 8000, "0.0.0.0"
    print("=" * 60 + "\n")
    uvicorn.run(app, host=host, port=port)
