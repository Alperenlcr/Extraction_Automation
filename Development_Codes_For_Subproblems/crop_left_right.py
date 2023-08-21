import cv2
import numpy as np

def rightmost_non_white_pixel(img):
    # Assuming your image is stored in the variable `image`
    nonwhite_pixels = np.where(img < 255)
    rightmost_nonwhite_pixels = np.max(nonwhite_pixels[1], axis=0)
    print(rightmost_nonwhite_pixels)
    # Assuming your image is stored in the variable `image`
    pixel_averages_column = np.mean(img, axis=(0)).tolist()
    pixel_averages = [sum(lst) / len(lst) for lst in pixel_averages_column]


    i = len(pixel_averages)-1
    while pixel_averages[i] > 245:
        i -= 1
#    print('Sagdan uzakligi', i)
    return i


def crop_left_right(fs, bs):
    f_img = cv2.imread(fs)
    b_img = cv2.imread(bs)

    height_front = f_img.shape[0]
    height_back = b_img.shape[0]
    width_front = f_img.shape[1]
    width_back = b_img.shape[1]

    v = 50
    x1, x2, y1, y2 = width_front//2 - v, width_front//2 + v, height_front - v, height_front - v//2
    f_rect = cv2.getRectSubPix(f_img, (x2-x1, y2-y1), ((x1+x2)/2, (y1+y2)/2))

    x1, x2, y1, y2 = width_back//2 - v, width_back//2 + v, height_back - v, height_back - v//2
    b_rect = cv2.getRectSubPix(b_img, (x2-x1, y2-y1), ((x1+x2)/2, (y1+y2)/2))

    cv2.imwrite('{}/test-{}-frect.png'.format(path_folder, j+1), f_rect)
    cv2.imwrite('{}/test-{}-brect.png'.format(path_folder, j+1), b_rect)

    print(f_rect)
    print(type(f_rect))
    tf = width_front//2 + v -rightmost_non_white_pixel(f_rect)
    tb = width_back//2 + v - rightmost_non_white_pixel(b_rect)

    x1, x2, y1, y2 = 0, tf - 19, 0, height_front
    f_left = cv2.getRectSubPix(f_img, (x2-x1, y2-y1), ((x1+x2)/2, (y1+y2)/2))

    x1, x2, y1, y2 = tf+17, width_front, 0, height_front
    f_right = cv2.getRectSubPix(f_img, (x2-x1, y2-y1), ((x1+x2)/2, (y1+y2)/2))

    x1, x2, y1, y2 = 0, tb-19, 0, height_back
    b_left = cv2.getRectSubPix(b_img, (x2-x1, y2-y1), ((x1+x2)/2, (y1+y2)/2))

    x1, x2, y1, y2 = tb+17, width_back, 0, height_back
    b_right = cv2.getRectSubPix(b_img, (x2-x1, y2-y1), ((x1+x2)/2, (y1+y2)/2))

    cv2.imwrite('{}/test-{}-fl.png'.format(path_folder, j+1), f_left)
    cv2.imwrite('{}/test-{}-fr.png'.format(path_folder, j+1), f_right)
    cv2.imwrite('{}/test-{}-bl.png'.format(path_folder, j+1), b_left)
    cv2.imwrite('{}/test-{}-br.png'.format(path_folder, j+1), b_right)


path_folder = '/home/alperenlcr/Code/Projects/Extraction_Automation/Meb-Soruları/deneme'
for j in range(1, 6):
    fs = path_folder+'/test-{}-f.png'.format(j)
    bs = path_folder+'/test-{}-b.png'.format(j)
    crop_left_right(fs, bs)