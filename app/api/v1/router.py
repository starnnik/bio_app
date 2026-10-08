from fastapi import APIRouter

from app.api.v1.routes import admin, auth, modules, progress, subjects

api_router = APIRouter(prefix="/api/v1")
for r in (auth.router, subjects.router, modules.router, progress.router, admin.router):
    api_router.include_router(r)
