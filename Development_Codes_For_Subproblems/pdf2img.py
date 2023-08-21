from pdf2image import convert_from_path
import cv2
import numpy as np

images = convert_from_path('/home/alperenlcr/Code/Projects/Extraction_Automation/Meb-Soruları/deneme.pdf')
print(len(images))
#for image_pil in images:
images[0].save('front.png', 'PNG')
images[1].save('back.png', 'PNG')
# Convert the image to a NumPy array
image_np = cv2.cvtColor(np.array(images[1]), cv2.COLOR_RGB2BGR)

# Convert the NumPy array to a Mat object
image = cv2.cvtColor(image_np, cv2.COLOR_BGR2GRAY)

print(type(image), image.shape)

# Convert the image to a NumPy array
image_np = cv2.cvtColor(np.array(images[6]), cv2.COLOR_RGB2BGR)

# Convert the NumPy array to a Mat object
image = cv2.cvtColor(image_np, cv2.COLOR_BGR2GRAY)

print(type(image), image.shape)
#cv2.imshow('img', image)
#cv2.waitKey(0)
#cv2.destroyAllWindows()