from fastapi.routing import APIRouter

from .endpoint import api

api_router = APIRouter()
api_router.include_router(api.api_router)