
import cv2
import numpy as np
from services.diamond_image_service import *
# from test import *
from starlette.responses import StreamingResponse
import io
from fastapi.responses import JSONResponse
from PIL import Image, ImageOps
from io import BytesIO
from ultralytics import YOLO
model = YOLO("model/best.pt")

async def detect_diamond_image(file):
    try:
        contents = await file.read()
        nparr = np.frombuffer(contents, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        results = model.predict(image)
        box_diamond = None
        for r in results:
            boxes = r.boxes
            for box in boxes:
                box_diamond = box.xyxy[0]
        if box_diamond is not None:
            x1,y1,x2,y2 =box
            x1,y1,x2,y2 = int(x1)-20,int(y1)-20,int(x2)+20,int(y2)+20
            cropped_object_image = image[y1:y2,x1:x2]
            #remove background
            remove_bg_mask= remove_bg(cropped_object_image, mask= True)
            #tìm tâm, bán kính của image sau khi remove background 
            x2,y2,r2 = find_circle(remove_bg_mask)
            #cắt lấy hình kim cương
            diamond_image = get_diamond_image(cropped_object_image, x2,y2,r2)
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
