import cv2
import numpy as np

# Tạo ảnh trắng (background)
width, height = 300, 300
background = np.ones((height, width, 3), dtype=np.uint8) * 255

# Tọa độ trung tâm và bán kính của hình tròn
center = (150, 150)
radius = 50

# Màu sắc của hình tròn (BGR)
color = (0, 0, 255)  # Màu đỏ

# Độ dày của đường viền, -1 để vẽ hình tròn đặc
thickness = -1

# Vẽ hình tròn lên ảnh
cv2.circle(background, center, radius, color, thickness)

# Hiển thị ảnh kết quả
cv2.imwrite("tmp/test.png",background)
