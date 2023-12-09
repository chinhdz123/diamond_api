from fastapi import APIRouter,FastAPI, UploadFile, Form, File
from controllers import diamond_text_controller
router = APIRouter()

@router.post('diamond/text/upload_image')
async def detect_diamond_text(file: UploadFile = File(...)):
    result = await diamond_text_controller.detect_diamond_text(file)
    return result