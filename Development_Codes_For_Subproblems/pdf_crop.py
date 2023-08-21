from PyPDF2 import PdfWriter, PdfReader, generic
import os, cv2

test = [[[318, 1324, 94, 802, 'A'], [1324, 2218, 94, 802, 'B'], [318, 1011, 909, 1622, 'C'], [1011, 1616, 909, 1622, 'D'], [1616, 2218, 909, 1622, 'A']], [[229, 758, 86, 794, 'B'], [758, 1530, 86, 794, 'C'], [1530, 2155, 86, 794, 'D'], [230, 751, 902, 1615, 'A'], [751, 1531, 902, 1615, 'B'], [1531, 2155, 902, 1615, 'C']]]
front_image = cv2.imread('front.png')
back_image = cv2.imread('back.png')

# count = 1
# for fq in test[0]:
#     x1, x2, y1, y2 = fq[2], fq[3], fq[0], fq[1]
#     crop = cv2.getRectSubPix(front_image, (x2-x1, y2-y1), ((x1+x2)/2, (y1+y2)/2))
#     cv2.imshow(str(count), crop)
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()
#     count += 1
# for bq in test[1]:
#     x1, x2, y1, y2 = bq[2], bq[3], bq[0], bq[1]
#     crop = cv2.getRectSubPix(back_image, (x2-x1, y2-y1), ((x1+x2)/2, (y1+y2)/2))
#     cv2.imshow(str(count), crop)
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()
#     count += 1
convert_img2pdf = 595/1654
with open("deneme.pdf", "rb") as in_f:
    input1 = PdfReader(in_f)
    output = PdfWriter()

    page = input1.pages[0]
    print(test[0])
    page.cropbox = generic.RectangleObject([100,100,500,600])
    output.add_page(page)
    for i in range(len(test[0])):
        print(page.mediabox.height, page.mediabox.width)
        page.cropbox = generic.RectangleObject([
            int(test[0][i][2]*convert_img2pdf),
            int(page.mediabox.height)  - int(test[0][i][0]*convert_img2pdf),
            int(test[0][i][3]*convert_img2pdf),
            int(page.mediabox.height)  - int(test[0][i][1]*convert_img2pdf)
        ])
        print(int(test[0][i][0]*convert_img2pdf), int(test[0][i][1]*convert_img2pdf), int(test[0][i][2]*convert_img2pdf), int(test[0][i][3]*convert_img2pdf))
        output.add_page(page)

    with open("{}.pdf".format(str(i+1)), "wb") as out_f:
        output.write(out_f)
exit()

os.system("/home/alperenlcr/Downloads/Inkscape-b0a8486-x86_64.AppImage --export-type=svg --export-filename=/home/alperenlcr/Code/Projects/Extraction_Automation/temp.svg /home/alperenlcr/Code/Projects/Extraction_Automation/out.pdf")
