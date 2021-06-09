import PyPDF2

def pdf_text_extraction(filename):

    input_path = 'input_files/' + filename

    file_obj = open(input_path, 'rb')
    output_file = open('Paper1_output.txt', 'w')  # Output file

    try:
        pdf_reader = PyPDF2.PdfFileReader(file_obj)  # PDF file reader object

        total_pages = pdf_reader.getNumPages()  # Get total pages
        information = pdf_reader.getDocumentInfo()  # Get file details

        output_file.write("Document Information: \n \n " + str(information) + "\n \n")
        output_file.write("Total Pages:\t" + str(total_pages) + "\n \n ")

        # Iterating through each page, extract text & writing to the file.
        for page_count in range(0, total_pages):
            page_data = pdf_reader.getPage(page_count)
            output_file.write(page_data.extractText())

    except Exception as e:
        print("\n \n Exception Arise \n \n ", e)

    finally:
        output_file.close()
        file_obj.close()


if __name__ == '__main__':
    pdf_text_extraction('paper1.pdf')

