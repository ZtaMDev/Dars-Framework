"""
Backend - Dars Framework

Development (two servers):
    dars dev              → frontend + backend
"""
import sys
import os

# Make the project root importable
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dars.backend.ssr import SSRApp
# pyrefly: ignore [missing-import]
from backend.apiConfig import DarsEnv

# Import the Dars app
# pyrefly: ignore [missing-import]
from main import app as dars_app

# ── Create SSR app ──────────────────────────────────────────────────────────
ssr = SSRApp(dars_app, prefix="/api/ssr", title="Dars Final Demo - Backend")

urls = DarsEnv.get_urls()

if DarsEnv.is_dev():
    # Development: CORS needed because frontend runs on a different port
    ssr.use_cors(
        origins=[urls["frontend"], "http://127.0.0.1:4000"],
        credentials=True,
    )

# Security headers (always enabled)
ssr.use_security_headers()

# File upload endpoint
ssr.use_upload(
    upload_dir=os.path.join(os.path.dirname(os.path.dirname(__file__)), "uploads"),
    allowed_types=["image/png", "image/jpeg", "image/gif", "image/webp", "application/pdf"],
    max_size_bytes=10 * 1024 * 1024,
    path="/api/upload",
)

# Expose the underlying FastAPI app for uvicorn
app = ssr.fastapi_app

# ── Custom API routes ───────────────────────────────────────────────────────
from fastapi import Request
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


# ── Production: serve frontend static files (same origin) ──────────────────
# In production the backend serves the Dars export (dist/) as static files.
# This makes frontend + API share the same origin — no CORS, no separate server.
#
# SPA fallback: all unmatched paths return index.html so the client-side
# router can handle /about, /dashboard, etc. without a 404 from the server.
# ── Production: serve dist/ as static files with SPA fallback ───────────────
if not DarsEnv.is_dev():
    ssr.use_spa_fallback()
# ────────────────────────────────────────────────────────────────────────────


if __name__ == "__main__":
    import uvicorn
    print("\n" + "=" * 60)
    print("Dars SSR Backend")
    print("=" * 60)
    if DarsEnv.is_dev():
        print(f"  Backend:  {urls['backend']}")
        print(f"  Frontend: {urls['frontend']}  (run 'dars dev' separately)")
        print(f"  API Docs: {urls['backend']}/docs")
        port, host = 3000, "127.0.0.1"
    else:
        frontend_dir = DarsEnv.get_frontend_dist_dir()
        print(f"  App:      http://0.0.0.0:8000  (frontend + API, same origin)")
        print(f"  Frontend: {frontend_dir}")
        port, host = 8000, "0.0.0.0"
    print("=" * 60 + "\n")
    uvicorn.run(app, host=host, port=port)
