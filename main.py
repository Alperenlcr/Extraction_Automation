from PyPDF2 import PdfReader, PdfWriter, generic
from pdf2image import convert_from_path
import os
import cv2
import numpy as np
from PIL import Image
from pytesseract import pytesseract

class Extraction():
    def __init__(self):
        self.pdf_path = ''
        self.path_folder = ''
        self.lecture_name = ''
        self.answer_key = []
        self.answer_pages = ''
        self.top_front = 295
        self.bottom_front = 2218
        self.top_back = 202
        self.bottom_back = 2155
        self.question = 0.425
        self.reader = ''
        self.convert_img2pdf = 595/1654
        self.pdf_combined = PdfWriter()


    def setup(self, path):
        self.pdf_path = path
        self.reader = PdfReader(self.pdf_path)            # read pdf from given path
        self.answer_pages = []
        i = len(self.reader.pages)-1
        while 'Test ' in self.reader.pages[i].extract_text():
            self.answer_pages.append(self.reader.pages[i])
            i -= 1
        self.answer_pages = list(reversed(self.answer_pages))
        # self.answer_pages = self.reader.pages[-((len(self.reader.pages)//81)+1):] # every 80 pages means 40 test and 40 test means 1 answer page
        self.lecture_name = ''.join(self.reader.pages[-1].extract_text().split(')')[1].split('Test')[0].split('\n'))
        if 'Yeterlilik' in path:
            self.path_folder = '/'.join(path.split('/')[:-1]) + '/' + self.lecture_name + ' Yeterlilik'    # folder path to save svg files
        else:
            self.path_folder = '/'.join(path.split('/')[:-1]) + '/' + self.lecture_name    # folder path to save svg files
        if not os.path.exists(self.path_folder):    # if the directory is not present then create it.
            os.makedirs(self.path_folder)
        if not os.path.exists(self.path_folder+'/svg'):
            os.makedirs(self.path_folder+'/svg')
        if not os.path.exists(self.path_folder+'/pdf'):
            os.makedirs(self.path_folder+'/pdf')
        self.read_answer_key()


    def read_answer_key(self):
        for page in self.answer_pages:
            text = page.extract_text().split('\n')
            lines = [line[line.index("Test")+4:] for line in text if 'Test' in line]
            self.answer_key += ["".join([char for char in l if char.isalpha()]) for l in lines]


    def crop_top_bottom(self, raw_0, raw_1):
        image_np = cv2.cvtColor(np.array(raw_0), cv2.COLOR_RGB2BGR)     # Convert the image to a NumPy array
        image_0 = cv2.cvtColor(image_np, cv2.COLOR_BGR2GRAY)      # Convert the NumPy array to a Mat object

        image_np = cv2.cvtColor(np.array(raw_1), cv2.COLOR_RGB2BGR)     # Convert the image to a NumPy array
        image_1 = cv2.cvtColor(image_np, cv2.COLOR_BGR2GRAY)      # Convert the NumPy array to a Mat object

        height_front = image_0.shape[0]
        height_back = image_1.shape[0]
        width_front = image_0.shape[1]
        width_back = image_1.shape[1]

        x1, x2, y1, y2 = 0, width_front, self.top_front, self.bottom_front
        front_image = cv2.getRectSubPix(image_0, (x2-x1, y2-y1), ((x1+x2)/2, (y1+y2)/2))

        x1, x2, y1, y2 = 0, width_back, self.top_back, self.bottom_back
        back_image = cv2.getRectSubPix(image_1, (x2-x1, y2-y1), ((x1+x2)/2, (y1+y2)/2))

        return image_0, image_1, front_image, back_image


    def crop_left_right(self, f_img, b_img):
        height_front = f_img.shape[0]
        height_back = b_img.shape[0]
        width_front = f_img.shape[1]
        width_back = b_img.shape[1]

# take a rectangle from mid of image to process
        v = 50
        x1, x2, y1, y2 = width_front//2 - v, width_front//2 + v, height_front - v, height_front - v//2
        f_rect = cv2.getRectSubPix(f_img, (x2-x1, y2-y1), ((x1+x2)/2, (y1+y2)/2))

        x1, x2, y1, y2 = width_back//2 - v, width_back//2 + v, height_back - v, height_back - v//2
        b_rect = cv2.getRectSubPix(b_img, (x2-x1, y2-y1), ((x1+x2)/2, (y1+y2)/2))


# find a pixel point for left questions rightest which includes numbers too
        tf = width_front//2 + v -self.rightmost_non_white_pixel(f_rect)
        tb = width_back//2 + v - self.rightmost_non_white_pixel(b_rect)

        x1, x2, y1, y2 = 0, tf - 22, 0, height_front
        f_left_t = cv2.getRectSubPix(f_img, (x2-x1, y2-y1), ((x1+x2)/2, (y1+y2)/2))

        x1, x2, y1, y2 = 0, tb - 22, 0, height_back
        b_left_t = cv2.getRectSubPix(b_img, (x2-x1, y2-y1), ((x1+x2)/2, (y1+y2)/2))

        fl = self.rightmost_non_white_pixel(f_left_t)
        bl = self.rightmost_non_white_pixel(b_left_t)


# find a pixel point for right questions leftest which includes numbers too
        fr = self.rightmost_non_white_pixel(f_img)
        br = self.rightmost_non_white_pixel(b_img)


# split pages from mid
        x1, x2, y1, y2 = 0, fl+5, 0, height_front
        f_left = cv2.getRectSubPix(f_img, (x2-x1, y2-y1), ((x1+x2)/2, (y1+y2)/2))

        x1, x2, y1, y2 = 0, bl+5, 0, height_back
        b_left = cv2.getRectSubPix(b_img, (x2-x1, y2-y1), ((x1+x2)/2, (y1+y2)/2))

        return f_left, b_left, fl+5, bl+5, fr+10, br+10


    def rightmost_non_white_pixel(self, img):
        pixel_averages_column = np.mean(img, axis=(0)).tolist()

        i = len(pixel_averages_column)-3
        while pixel_averages_column[i] > 254:
            i -= 1
        # print('Sagdan uzakligi', i)
        return i


    def number_y_indexs(self, arr, v, v2, img, x1, x2):
        r = []
        box = 20
        t = len(arr)-box-80
        k = 5
        while k < t:
            k += 1
            s=0
            for j in range(box):
                s += arr[k+j]
            s /= box
            if s < 245:
                if r == []:
                    r.append(k+v)
                else:
                    crop = img[k+v-20:k+v, x1:x2]
                    t2 = np.mean(crop, axis=(0, 1))
                    if t2 > 250:
                        r.append(k+v)
                k += 240
        r.append(v2-5)
        return r


    def questions_info(self, fh, bh, fnum_left, fnum_right, bnum_left, bnum_right, flx_min, flx_max, frx_min, frx_max,blx_min, blx_max, brx_min, brx_max, i, full_front_image, full_back_image):
        fleft_nums = []
        fl_pixel_averages_row = np.mean(fnum_left, axis=(1)).tolist()

        # k = 10
        # while k < len(pixel_averages_row)-100:
        #     if pixel_averages_row[k] < 252:
        #         fleft_nums.append(k-5+self.top_front)
        #         k += 100
        #     k += 1
        # fleft_nums.append(self.bottom_front)
        fleft_nums = self.number_y_indexs(fl_pixel_averages_row, self.top_front, self.bottom_front, full_front_image, 200, 500)

        fright_nums = []
        fr_pixel_averages_row = np.mean(fnum_right, axis=(1)).tolist()
        # k = 10
        # while k < len(pixel_averages_row)-100:
        #     if pixel_averages_row[k] < 252:
        #         fright_nums.append(k-5+self.top_front)
        #         k += 100
        #     k += 1
        # fright_nums.append(self.bottom_front)
        fright_nums = self.number_y_indexs(fr_pixel_averages_row, self.top_front, self.bottom_front, full_front_image, 1100, 1400)


        bleft_nums = []
        bl_pixel_averages_row = np.mean(bnum_left, axis=(1)).tolist()
        # k = 10
        # while k < len(pixel_averages_row)-100:
        #     if pixel_averages_row[k] < 252:
        #         bleft_nums.append(k-5+self.top_back)
        #         k += 100
        #     k += 1
        # bleft_nums.append(self.bottom_back)
        bleft_nums = self.number_y_indexs(bl_pixel_averages_row, self.top_back, self.bottom_back, full_back_image, 200, 500)

        bright_nums = []
        br_pixel_averages_row = np.mean(bnum_right, axis=(1)).tolist()
        # k = 10
        # while k < len(pixel_averages_row)-100:
        #     if pixel_averages_row[k] < 252:
        #         bright_nums.append(k-5+self.top_back)
        #         k += 100
        #     k += 1
        # bright_nums.append(self.bottom_back)
        bright_nums = self.number_y_indexs(br_pixel_averages_row, self.top_back, self.bottom_back, full_back_image, 1100, 1400)

# top_y, bottom_y, left_x, right_x, answer
        j = 0
        test = [[], []]
        if len(fleft_nums) + len(fright_nums) + len(bleft_nums) + len(bright_nums) != len(self.answer_key[i//2])+4:
            global ERROR
            #ERROR += 'ERROR AT {} TEST: {} {} {} {} {}'.format(self.lecture_name, str((i//2)+1), str(len(fleft_nums)), str(len(fright_nums)), str(len(bleft_nums)), str(len(bright_nums)), str(len(self.answer_key[i//2])))
            ERROR += str((i//2)+1) + ' '
            return []
        else:
            for k in range(len(fleft_nums)-1):
                test[0].append([fleft_nums[k], fleft_nums[k+1], flx_min, flx_max, self.answer_key[i//2][j]]);j+=1
            for k in range(len(fright_nums)-1):
                test[0].append([fright_nums[k], fright_nums[k+1], frx_min, frx_max, self.answer_key[i//2][j]]);j+=1
            for k in range(len(bleft_nums)-1):
                test[1].append([bleft_nums[k], bleft_nums[k+1], blx_min, blx_max, self.answer_key[i//2][j]]);j+=1
            for k in range(len(bright_nums)-1):
                test[1].append([bright_nums[k], bright_nums[k+1], brx_min, brx_max, self.answer_key[i//2][j]]);j+=1

            return test


    def find_questions(self, full_front_image, full_back_image, front_image, back_image, fl, bl, flx_max, blx_max, frx_max, brx_max, fw, bw, i):
# flx_min, frx_min, blx_min, brx_min values are for uncropped image
        flx_min, blx_min, frx_min, brx_min = int(fw*((flx_max/fw)-self.question)), int(bw*((blx_max/bw)-self.question)), int(fw*((frx_max/fw)-self.question)), int(bw*((brx_max/bw)-self.question))
        flx_min -= 10
        frx_min -= 10
        blx_min -= 10
        brx_min -= 10

        fh = fl.shape[0]
        bh = bl.shape[0]

        x1, x2, y1, y2 = 20, flx_min, 0, fh
        fnum_left = cv2.getRectSubPix(fl, (x2-x1, y2-y1), ((x1+x2)/2, (y1+y2)/2))

        x1, x2, y1, y2 = frx_min-50, frx_min-5, 0, fh
        fnum_right = cv2.getRectSubPix(front_image, (x2-x1, y2-y1), ((x1+x2)/2, (y1+y2)/2))

        x1, x2, y1, y2 = 20, blx_min, 0, bh
        bnum_left = cv2.getRectSubPix(bl, (x2-x1, y2-y1), ((x1+x2)/2, (y1+y2)/2))

        x1, x2, y1, y2 = brx_min-50, brx_min-5, 0, bh
        bnum_right = cv2.getRectSubPix(back_image, (x2-x1, y2-y1), ((x1+x2)/2, (y1+y2)/2))

        # cv2.imwrite('{}/{}-fl.png'.format(self.path_folder, str(i//2)), fnum_left)
        # cv2.imwrite('{}/{}-fr.png'.format(self.path_folder, str(i//2)), fnum_right)
        # cv2.imwrite('{}/{}-bl.png'.format(self.path_folder, str(i//2)), bnum_left)
        # cv2.imwrite('{}/{}-br.png'.format(self.path_folder, str(i//2)), bnum_right)
# top_y, bottom_y, left_x, right_x, answer
        test = self.questions_info(fh, bh, fnum_left, fnum_right, bnum_left, bnum_right, flx_min, flx_max, frx_min, frx_max,blx_min, blx_max, brx_min, brx_max, i, full_front_image, full_back_image)

        return test


    def crop_question_from_pdf_and_save_svg(self, test_two_face, test_num, test_name):
        count = 1
        test = test_two_face[0]
        for question in test:
            s = "/{}-{}-{}-{}-{}".format(self.lecture_name, str(test_num), test_name, str(count), question[4])
            count += 1

            output = PdfWriter()

            page = self.reader.pages[(test_num-1)*2]
            page.cropbox = generic.RectangleObject([
                int(question[2]*self.convert_img2pdf),
                int(page.mediabox.height)  - int(question[0]*self.convert_img2pdf),
                int(question[3]*self.convert_img2pdf),
                int(page.mediabox.height)  - int(question[1]*self.convert_img2pdf)
            ])
            output.add_page(page)
            self.pdf_combined.add_page(page)

            with open("{}.pdf".format(self.path_folder+'/pdf'+s), "wb") as out_f:
                output.write(out_f)

            # command = "_INKSCAPE_GC=disable /home/alperenlcr/Downloads/Inkscape-b0a8486-x86_64.AppImage --export-type=svg --export-filename=\"{}.svg\" \"{}.pdf\"".format(self.path_folder+'/svg'+s, self.path_folder+'/pdf'+s)
            # print(command)
            # os.system(command)
            command = "pdf2svg \"{}.pdf\" \"{}.svg\"".format(self.path_folder+'/pdf'+s, self.path_folder+'/svg'+s)
#            print(command)
            os.system(command)


        test = test_two_face[1]
        for question in test:
            s = "/{}-{}-{}-{}-{}".format(self.lecture_name, str(test_num), test_name, str(count), question[4])
            count += 1

            output = PdfWriter()

            page = self.reader.pages[(test_num-1)*2+1]
            page.cropbox = generic.RectangleObject([
                int(question[2]*self.convert_img2pdf),
                int(page.mediabox.height)  - int(question[0]*self.convert_img2pdf),
                int(question[3]*self.convert_img2pdf),
                int(page.mediabox.height)  - int(question[1]*self.convert_img2pdf)
            ])
            output.add_page(page)
            self.pdf_combined.add_page(page)

            with open("{}.pdf".format(self.path_folder+'/pdf'+s), "wb") as out_f:
                output.write(out_f)

            # command = "_INKSCAPE_GC=disable /home/alperenlcr/Downloads/Inkscape-b0a8486-x86_64.AppImage --export-type=svg --export-filename=\"{}.svg\" \"{}.pdf\"".format(self.path_folder+'/svg'+s, self.path_folder+'/pdf'+s)
            # print(command)
            # os.system(command)
            command = "pdf2svg \"{}.pdf\" \"{}.svg\"".format(self.path_folder+'/pdf'+s, self.path_folder+'/svg'+s)
#            print(command)
            os.system(command)
            #with open("temp.pdf", "wb") as out_f:
            #    output.write(out_f)

            #os.system("/home/alperenlcr/Downloads/Inkscape-b0a8486-x86_64.AppImage --export-type=svg --export-filename={}.svg temp.pdf".format(self.path_folder+s))



    def extract(self):
        # loop pages
            # convert page to img and crop them
            # process png and return top_y, bottom_y, left_x, right_x, answer for pdf crop
            # loop questions
                # croping questions from pdf page and counting
                # converting pdf files to svg images and saving
# !!!!!!!
        images = convert_from_path(self.pdf_path)#[:-len(self.answer_pages)]
        for i in range(0, len(images)-len(self.answer_pages), 2):
            front_image, back_image, front_image_cropped, back_image_cropped = self.crop_top_bottom(images[i], images[i+1])

            x1, x2, y1, y2 = 300, 1350, 252, 292
            crop = cv2.getRectSubPix(front_image, (x2-x1, y2-y1), ((x1+x2)/2, (y1+y2)/2))
            cv2.imwrite('crop_title.png', crop)
            test_name = pytesseract.image_to_string(Image.open('crop_title.png'), lang='tur').replace("\n", "").replace('\x0c', "").replace('/', ' ')

            front_left_image, back_left_image, flx_max, blx_max, frx_max, brx_max = self.crop_left_right(front_image_cropped, back_image_cropped)

# top_y, bottom_y, left_x, right_x, answer
            test = self.find_questions(front_image, back_image, front_image_cropped, back_image_cropped, front_left_image, back_left_image, flx_max, blx_max, frx_max, brx_max, front_image_cropped.shape[1], back_image_cropped.shape[1], i)
            #print(test)
            # j = 0
            # for fq in test[0]:
            #     x1, x2, y1, y2 = fq[2], fq[3], fq[0], fq[1]
            #     q = cv2.getRectSubPix(front_image, (x2-x1, y2-y1), ((x1+x2)/2, (y1+y2)/2))
            #     cv2.imwrite('{}/DA-{}-{}-{}.png'.format(self.path_folder, (i//2)+1, j+1, self.answer_key[(i//2)][j]), q)
            #     j += 1
            # for fq in test[1]:
            #     x1, x2, y1, y2 = fq[2], fq[3], fq[0], fq[1]
            #     q = cv2.getRectSubPix(back_image, (x2-x1, y2-y1), ((x1+x2)/2, (y1+y2)/2))
            #     cv2.imwrite('{}/DA-{}-{}-{}.png'.format(self.path_folder, (i//2)+1, j+1, self.answer_key[(i//2)][j]), q)
            #     j += 1
            if test != []:
                self.crop_question_from_pdf_and_save_svg(test, (i//2)+1, test_name)


# this class is responsible for generate images
# images will be stored at folder next to pdf
# pdf path will be taken as parameter
# images will be named as folder_name/lecture_name-test-test_number-front/back-answerkey.png


PATH = "<PATH_TO_REPO>"
pdfs = [
    PATH+"/Extraction_Automation/Meb-Soruları/2018-2019-MEZUN Biyoloji.pdf",
    PATH+"/Extraction_Automation/Meb-Soruları/2018-2019-MEZUN Coğrafya.pdf",
    PATH+"/Extraction_Automation/Meb-Soruları/2018-2019-MEZUN Din Kültürü.pdf",
    PATH+"/Extraction_Automation/Meb-Soruları/2018-2019-MEZUN Felsefe Grubu.pdf",
    PATH+"/Extraction_Automation/Meb-Soruları/2018-2019-MEZUN Fizik.pdf",
    PATH+"/Extraction_Automation/Meb-Soruları/2018-2019-MEZUN Kimya.pdf",
    PATH+"/Extraction_Automation/Meb-Soruları/2018-2019-MEZUN Matematik-2.pdf",
    PATH+"/Extraction_Automation/Meb-Soruları/2018-2019-MEZUN Tarih.pdf",
    PATH+"/Extraction_Automation/Meb-Soruları/2018-2019-MEZUN Türk Dili ve Edebiyatı.pdf",
    PATH+"/Extraction_Automation/Meb-Soruları/2018-2019-MEZUN İngilizce.pdf",
    PATH+"/Extraction_Automation/Meb-Soruları/2018-2019-MEZUN Türkçe (Sözel Yeterlilik).pdf"
]

for pdf in pdfs:
    ERROR = 'ERROR AT TESTS : '
    converter = Extraction()
    converter.setup(pdf)
    converter.extract()

    with open("{}/0All_Combined.pdf".format(converter.path_folder+'/pdf'), "wb") as out_f:
        converter.pdf_combined.write(out_f)

    f = open("{}/0log.txt".format(converter.path_folder), "w")
    f.write(ERROR)
    f.close()
    print(pdf.split('/')[-1], ERROR)
#print(len(converter.answer_key))
#print(converter.answer_key)
#converter.answer_key = ['DEACBCBDBDCB', 'DACCCABBABEB', 'EACADDCDDEAA', 'EBBEECDCEAAD', 'EBDBCAEADB', 'BCECBCACCEB', 'CCEDCDCBCBAD', 'AEDDBCECCEEC', 'DDBAADBEDD', 'ECCAABCDED', 'EDDDDDECBECC', 'CCAEAEDDAAEE', 'BDBBCEECEBEA', 'DCAEECDECCEB', 'EABCACDAABB', 'BEABACBDDEAE', 'DADDCEDDCDEE', 'EBCAEBDCADBC', 'CBDEBEBBBDCC', 'ABEDCEEAADD', 'BDEECEDADEBA', 'CBCAABCBDED', 'CBDEBEDAAEC', 'DCABCCCBEAD', 'DEDBBAEBEBA', 'CDCADAEECDE', 'EBEBADBCBEDE', 'BCBEBEDADB', 'AACCAECEDDEC', 'EDDCABABCCBC', 'BCBEDBDEBAEC', 'ECCCBABEADA', 'DABCCBEABCBD', 'DABAEDCCEEC', 'EADEBAACEE', 'ABEBCBDCCEAD', 'EBADECCACADB', 'ACCCEBAEDDDA', 'ABCBCBDEEE', 'CECEBBBECDDD', 'DCEDEBCCDAD', 'ECDDCABBAEB', 'ADBCDEACBCAD', 'AAEDAECDEDDE', 'EACADEBBEABE', 'CCCDEEACAEBB', 'ACDDBAEEDECE', 'DDBAEBDDBAE']

# /home/alperenlcr/Downloads/Inkscape-b0a8486-x86_64.AppImage --export-type="svg" /home/alperenlcr/Code/Projects/Extraction_Automation/out.pdf



#apt install tesseract-ocr libtesseract-dev libleptonica-dev pkg-config
#apt install tesseract-ocr-tur
#apt install pdf2svg 
#export TESSDATA_PREFIX=/usr/share/tesseract-ocr/4.00/tessdata
#https://inkscape.org/release/all/gnulinux/appimage/
