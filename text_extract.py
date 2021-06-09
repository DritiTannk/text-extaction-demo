import PyPDF2

file_obj = open('input_files/paper1.pdf', 'rb')
pdf_reader = PyPDF2.PdfFileReader(file_obj)  # PDF file reader object

output_file = open('Paper1_output', 'w')  # Output file

total_pages = pdf_reader.getNumPages()  # Get total pages
information = pdf_reader.getDocumentInfo()  # Get file details

output_file.write("Document Information: \n \n " + str(information) + "\n \n")
output_file.write("Total Pages: \n \n " + str(total_pages) + "\n \n ")

# Iterating through each page and extract text
for page_count in range(0, total_pages):
    page_data = pdf_reader.getPage(page_count)
    output_file.write(page_data.extractText())  # Writing to text file

output_file.close()
file_obj.close()

