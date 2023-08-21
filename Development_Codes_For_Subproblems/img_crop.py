import cv2

# Load the image as a Mat object
image_front = cv2.imread('front.png')
image_back = cv2.imread('back.png')

# FRONT PAGE
# left questions
# x1, y1 = 95, 294
# x2, y2 = 806, 2224
# left numbers
# x1, y1 = 42, 294
# x2, y2 = 95, 2224
# right questions
# x1, y1 = 900, 294
# x2, y2 = 1625, 2224
# right numbers
# x1, y1 = 850, 294
# x2, y2 = 900, 2224

top_front = 0.127
bottom_front = 0.056
top_back = 0.086
bottom_back = 0.081
height_front = image_front.shape[0]
height_back = image_back.shape[0]
width_front = image_front.shape[1]
width_back = image_back.shape[1]
print(height_front,height_back,width_front,width_back)

# Draw the rectangle on the image
# cv2.rectangle(image_front, (0, int(height_front*top_front)), (width_front, int(height_front-height_front*bottom_front)), (0, 0, 255), thickness=1)
# cv2.rectangle(image_back, (0, int(height_back*top_back)), (width_back, int(height_back-height_back*bottom_back)), (0, 0, 255), thickness=1)
# cv2.rectangle(image_back, (x1, y1), (x2, y2), (0, 0, 255), thickness=1)

# Crop the region inside the rectangle
x1, x2, y1, y2 = 0, width_front, int(height_front*top_front), int(height_front-height_front*bottom_front)
front_image = cv2.getRectSubPix(image_front, (x2-x1, y2-y1), ((x1+x2)/2, (y1+y2)/2))
front_image = image_front[y1:y2, x1:x2]
x1, x2, y1, y2 = 0, width_back, int(height_back*top_back), int(height_back-height_back*bottom_back)
back_image = cv2.getRectSubPix(image_back, (x2-x1, y2-y1), ((x1+x2)/2, (y1+y2)/2))


cv2.imwrite('front_cropped.png', front_image)
cv2.imwrite('back_cropped.png', back_image)