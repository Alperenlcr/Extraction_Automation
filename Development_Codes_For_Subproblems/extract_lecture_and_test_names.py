# importing required modules
from PyPDF2 import PdfReader
import cv2

from PIL import Image
from pytesseract import pytesseract


# creating a pdf reader object
reader = PdfReader('Meb-Soruları/2018-2019-MEZUN Kimya.pdf')

# printing number of pages in pdf file
print(len(reader.pages))

# getting a specific page from the pdf file
page = reader.pages[-1]

# extracting text from page
text = page.extract_text().split(')')[1].split('Test')[0]

ders_adi = ''.join(text.split('\n'))
print(ders_adi)


img = cv2.imread('front.png')
x1, x2, y1, y2 = 300, 1350, 252, 292
crop = cv2.getRectSubPix(img, (x2-x1, y2-y1), ((x1+x2)/2, (y1+y2)/2))
cv2.imwrite('crop_title.png', crop)
t = pytesseract.image_to_string(Image.open('crop_title.png')).replace("\n", "").replace('\x0c', "")
print(t)




# getting a specific page from the pdf file
page = reader.pages[0]

#print(page.extract_text())
# extracting text from page
text = (page.extract_text().split(ders_adi)[1].split('.')[0])[1:]

#print(''.join(text.split('\n')))
