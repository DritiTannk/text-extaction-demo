import os
import glob
import PyPDF2
from tika import parser


def pdf_text_extraction(filepath, filename, output_path):
    """
    It handles text extraction process from PDF files.
    """
    output_file_name = filename + '_output.txt'
    output_file_path = output_path + output_file_name

    file_obj = open(filepath, 'rb')
    output_file = open(output_file_path, 'w')  # Output file

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


def pdf_to_text_using_tikka(filepath, filename, output_path):
    """
    This method extract text from PDF using tika library.
    """
    output_file_name = filename + '_tikka.txt'
    output_file_path = output_path + output_file_name
    parsed_file = parser.from_file(filepath)  # Parsing PDF file
    content = parsed_file['content']  # Extracting content

    with open(output_file_path, 'w') as f:
        res = f.write(content.strip())

    return res


def html_to_text(filepath, filename, output_path):
    """
    This method extract text from HTML files using tika library.
    """
    output_file_name = filename + '.txt'
    output_file_path = output_path + output_file_name
    parsed_file = parser.from_file(filepath)
    content = parsed_file['content']

    with open(output_file_path, 'w') as file1:
        res = file1.write(content.strip())

    return res


def ppt_to_text(filepath, filename, output_path):
    """
    This method extract text from power-point presentation files using tika library.
    """
    output_file_name = filename + '.txt'
    output_file_path = output_path + output_file_name
    parsed_file = parser.from_file(filepath)
    content = parsed_file['content']

    with open(output_file_path, 'w') as file1:
        res = file1.write(content.strip())

    return res


def word_to_text(filepath, filename, output_path):
    """
    This method extract text from word files using tika library.
    """
    output_file_name = filename + '.txt'
    parsed_file = parser.from_file(filepath)
    content = parsed_file['content']
    output_file_path = output_path + output_file_name

    with open(output_file_path, 'w') as file1:
        res = file1.write(content.strip())

    return res


def file_search(input_path, output_path):
    """
    This method gets files from given input path & checks extension.

    :param input_path: input files path
    :param output_path: output files path

    :return: statistics dictionary
    """
    pdf_counter, ppt_counter, html_counter, word_counter = 0, 0, 0, 0
    input_path = input_path + '*'

    for file in glob.glob(input_path):
        fname = os.path.basename(file)  # Get file name from path
        filename, ext = os.path.splitext(fname)  # Extract filename & extension

        if fname.endswith('.pdf') and ext == '.pdf':
            pdf_text_extraction(file, filename, output_path)
            res = pdf_to_text_using_tikka(file, filename, output_path)

            if res > 0:
                pdf_counter += 1

        elif fname.endswith('.html') and ext == '.html':
            res = html_to_text(file, filename, output_path)

            if res > 0:
                html_counter += 1

        elif fname.endswith('.ppt') and ext == '.ppt':
            res = ppt_to_text(file, filename, output_path)

            if res > 0:
                ppt_counter += 1

        elif fname.endswith('.doc') and ext == '.doc':
            res = word_to_text(file, filename, output_path)

            if res > 0:
                word_counter += 1

        else:
            print(f"Invalid File Format for {filename}")

    return {'pdf_counter': pdf_counter, 'html_counter': html_counter,
            'ppt_counter': ppt_counter, 'word_counter': word_counter
            }


if __name__ == '__main__':
    i_path = input('Enter The Input Path: ')  # Get user's input files directory path
    o_path = input('Enter The Output Path: ')  # Get user's output files directory path

    i_path_exist = os.path.exists(i_path)  # Check the user input path
    o_path_exist = os.path.exists(o_path)  # Check the user output path

    if i_path_exist and o_path_exist:
        stats = file_search(i_path, o_path)
        print(f"\n Extraction Result \n {'-' * 20}"
              f"\n PDF Files ==> {stats.get('pdf_counter')}, "
              f"\n HTML Files ==> {stats.get('html_counter')},"
              f"\n PPT Files ==> {stats.get('ppt_counter')},"
              f"\n DOC Files ==> {stats.get('word_counter')}")
    else:
        print("\n \n Given paths does not exists")

