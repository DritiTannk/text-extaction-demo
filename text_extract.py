import os
import glob
import PyPDF2
from tika import parser


def pdf_text_extraction(filepath, filename):
    """
    It handles text extraction process from PDF files.
    """
    output_filename = str(filename.split('.')[0]) + '_output.txt'

    file_obj = open(filepath, 'rb')
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


def pdf_to_text_using_tikka(filepath, filename):
    """
    This method extract text from PDF using tikka library.
    """
    output_file_name = filename + '_tikka.txt'
    parsed_file = parser.from_file(filepath)  # Parsing PDF file
    content = parsed_file['content']  # Extracting content

    with open(f'output_files/{output_file_name}', 'w') as f:
        f.write(content.strip())


if __name__ == '__main__':
    i_path = './input_files/*'  # Input files path

    for file in glob.glob(i_path):
        fname = os.path.basename(file)  # Get file name from path
        filename, ext = os.path.splitext(fname)  # Extract filename & extension

        if fname.endswith('.pdf') and ext == '.pdf':
            pdf_text_extraction(file, fname)
            pdf_to_text_using_tikka(file, fname)

