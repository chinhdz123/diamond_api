from fastapi import APIRouter,FastAPI, UploadFile, Form, File

from controllers import diamond_image_controller
router = APIRouter()

@router.post('diamond/image/upload_image')
async def detect_diamond_image(file: UploadFile = File(...)):
    result = await diamond_image_controller.detect_diamond_image(file)
    return result