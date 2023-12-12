import os
from rembg import remove
import  cv2
import numpy as np 

def remove_bg(image):
    remove_bg = remove(image)
    remove_bg_mask = remove(image, only_mask=True)
    return remove_bg, remove_bg_mask

def find_circle(image):

    # gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, mask = cv2.threshold(image, 150, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    max_contour = max(contours, key=cv2.contourArea)
    x, y, w, h = cv2.boundingRect(max_contour)
    if w < h:
        r = int(w/2)
        #chiều cao
        a =  int(h/2)
    else:
        r = int(h/2)
        a =  int(w/2)

    x1 = int(x+a)
    y1 = int(y+a)
    return x1,y1,r

def get_image_box_out_circle(image, x,y,r):
    mask = np.zeros(image.shape[:2], dtype="uint8")
    cv2.rectangle( mask, (x - r , y - r), (x + r , y + r), (255, 255, 255), thickness=-1)
    result = cv2.bitwise_and(image,image, mask =mask)
    cropped_object = result[y-r:y+r, x-r:x+ r]
    cropped_raw_image = image[y-r:y+r, x-r:x+ r]
    return cropped_object, cropped_raw_image

def get_diamond_image(image, x,y,r):
    mask = np.zeros(image.shape[:2], dtype="uint8")
    cv2.circle(mask, (x, y), r, (255, 255, 255), thickness=-1)
    result = cv2.bitwise_and(image,image, mask =mask)
    cropped_object = result[y-r:y+r, x-r:x+ r]
    return cropped_object