import cv2
from paddleocr import PaddleOCR
import numpy as np


ocr = PaddleOCR(show_log=False, use_angle_cls=False, lang="en", det_db_thresh=0.05)

def detect_box(img):
    boxes = ocr.ocr(img, rec=False)
    best_box = None
    max_aera = 0
    for box in boxes:
        height = box[0][0] - box[1][0]
        weight = box[1][1] - box[2][1]
        
        area = height * weight
        if area > max_aera:
            max_aera = area 
            best_box = box
    return best_box

def crop_image(image, box, extension=35):
    # Convert box coordinates to integers
    box = np.array([[int(coord[0]), int(coord[1])] for coord in box], dtype=np.float32)
    box[0] += [-extension, -extension]
    box[1] += [extension, -extension]
    box[2] += [extension, extension]
    box[3] += [-extension, extension]

    # Get the width and height of the bounding box
    w = int(max(np.linalg.norm(box[1] - box[0]), np.linalg.norm(box[2] - box[3])))
    h = int(max(np.linalg.norm(box[2] - box[1]), np.linalg.norm(box[3] - box[0])))
    # Get the perspective transformation matrix
    dst_pts = np.array([[0, 0], [w - 1, 0], [w - 1, h - 1], [0, h - 1]], dtype=np.float32)
    M = cv2.getPerspectiveTransform(box, dst_pts)
    # Warp the image based on the perspective transformation matrix
    cropped_image = cv2.warpPerspective(image, M, (w, h))
    return cropped_image



