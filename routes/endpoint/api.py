from .diamond_image.diamond_image_api import router as diamond_image
from .diamond_text.diamond_text_api import router as diamond_text

from fastapi import APIRouter

api_router = APIRouter(prefix="/v1")

api_router.include_router(diamond_image, prefix="/diamond_image", tags=["diamond_image"])
api_router.include_router(diamond_text, prefix="/diamond_text", tags=["diamond_text"])
