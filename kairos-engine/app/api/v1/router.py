"""Central API V1 Router aggregating all sub-endpoint routers."""
from fastapi import APIRouter
from app.api.v1.endpoints.health import router as health_router
from app.api.v1.endpoints.search import router as search_router
from app.api.v1.endpoints.diagnostic import router as diagnostic_router

api_v1_router = APIRouter(prefix="/api/v1")

api_v1_router.include_router(health_router)
api_v1_router.include_router(search_router)
api_v1_router.include_router(diagnostic_router)
