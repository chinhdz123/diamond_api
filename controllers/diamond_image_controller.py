
import cv2
import numpy as np
from services.diamond_image_service import *
from starlette.responses import StreamingResponse
import io
from fastapi.responses import JSONResponse
from PIL import Image, ImageOps
from io import BytesIO


async def detect_diamond_image(file):
    try:
        contents = await file.read()
        nparr = np.frombuffer(contents, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        #remove background lần 1
        remove_bg_image_1, remove_bg_mask_1 = remove_bg(image)

        #tìm tâm, bán kính của image sau khi remove background 
        x1,y1,r1 = find_circle(remove_bg_mask_1)
        #cắt lấy hình vuông bao quanh hình tròn tâm, bán kính trên
        cropped_object_image, cropped_raw_image  = get_image_box_out_circle(image,x1,y1,r1)
        #remove background lần 2
        remove_bg_image_2, remove_bg_mask_2 = remove_bg(cropped_object_image)
        #tìm tâm, bán kính của image sau khi remove background 
        x2,y2,r2 = find_circle(remove_bg_mask_2)
        #cắt lấy hình kim cương
        diamond_image = get_diamond_image(cropped_raw_image, x2,y2,r2)
        diamond_image = cv2.resize(diamond_image, (300,300))
        _, encoded_image = cv2.imencode(".jpg", diamond_image)
        image_bytes = encoded_image.tobytes()
        diamond_image_pillow = remove(image_bytes)
        image_bytesio = BytesIO()
        image_bytesio.write(diamond_image_pillow)  # You can change the format as needed
        def generate():
            image_bytes = image_bytesio.getvalue()
            yield image_bytes
        return StreamingResponse(generate(), media_type="image/jpeg")
    except Exception as e:
        return JSONResponse(content={"message": str(e)}, status_code=500)