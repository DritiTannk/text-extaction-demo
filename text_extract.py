import PyPDF2

def pdf_text_extraction(filename):
    """
    It handles text extraction process from PDF files.
    """
    input_path = 'input_files/' + filename
    output_filename = str(filename.split('.')[0]) + '_output.txt'

    file_obj = open(input_path, 'rb')
    output_file = open(f'output_files/{output_filename}', 'w')  # Output file

    try:
        pdf_reader = PyPDF2.PdfFileReader(file_obj, strict=False)  # PDF file reader object

        total_pages = pdf_reader.getNumPages()  # Get total pages
        information = pdf_reader.getDocumentInfo()  # Get file details

        output_file.write("Document Information: \n \n " + str(information) + "\n \n")
        output_file.write("Total Pages:\t" + str(total_pages) + "\n \n ")

        # Iterating through each page, extract text & writing to the file.
        for page_count in range(0, total_pages):
            page_data = pdf_reader.getPage(page_count)
            content = page_data.extractText()
            output_file.write(f'\n ----- Page {page_count + 1} ------  \n \n ')
            output_file.write(content)

    except Exception as e:
        print("\n \n Exception Arise \n \n ", e)

    finally:
        output_file.close()
        file_obj.close()

if __name__ == '__main__':
    pdf_text_extraction('paper_1.pdf')

