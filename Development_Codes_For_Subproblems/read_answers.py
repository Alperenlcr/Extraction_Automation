# importing required modules
from PyPDF2 import PdfReader

# creating a pdf reader object
reader = PdfReader('out.pdf')

# printing number of pages in pdf file
print(len(reader.pages))

# getting a specific page from the pdf file
page = reader.pages[1]

# extracting text from page
text = page.extract_text().split('\n')

lines = [line[4:] for line in text if line[:4]=='Test']
answers = ["".join([char for char in l if char.isalpha()]) for l in lines]

print(answers)
