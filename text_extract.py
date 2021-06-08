import PyPDF2

file_obj = open('paper1.pdf', 'rb')
pdf_reader = PyPDF2.PdfFileReader(file_obj)  # PDF file reader object

pdf_writer = PyPDF2.PdfFileWriter()  # PDF file writer object
output_file = open('Paper1_output', 'w')

total_pages = pdf_reader.getNumPages()  # Get total pages
information = pdf_reader.getDocumentInfo()  # Get file details
print("\n \n ------- Document Information ------ \n \n")
print("\n \n \t", information)
print("\n \n Total pages ==> ", total_pages)

# Iterating through each page and get text
for page_count in range(0, total_pages):
    page_data = pdf_reader.getPage(page_count)
    output_file.write(page_data.extractText())  # Writing to text file

output_file.close()
file_obj.close()

