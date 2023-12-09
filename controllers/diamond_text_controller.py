

import cv2
import numpy as np
from services.diamond_text_service import *
from starlette.responses import StreamingResponse
import io
from fastapi.responses import JSONResponse

async def detect_diamond_text(file):
    try:
        contents = await file.read()
        nparr = np.frombuffer(contents, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        best_box = detect_box(image)

        cropped_image = crop_image(image, best_box)
        # Convert the processed image to bytes
        retval, img_bytes = cv2.imencode('.jpg', cropped_image)
        content = img_bytes.tobytes()

        # Return the processed image as a file response
        return StreamingResponse(io.BytesIO(content), media_type="image/jpeg")
    except Exception as e:
        return JSONResponse(content={"message": str(e)}, status_code=500)