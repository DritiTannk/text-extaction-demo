import os
import glob
import re

from nltk import sent_tokenize, word_tokenize


def sentence_extraction(output_path, filename, data):
    """
    This method extracts sentence from the given text file.

    Keyword arguments:
    output_path -- output path for the file
    filename -- name of the file
    data -- file content

    """

    output_file_name = filename + '_nltk.txt'
    output_file_path = output_path + output_file_name

    pattern = '\se.g.\s'

    data = data.replace('\n\n', ' ')  # Replacing extra new lines.
    data = data.replace('\n', ' ')
    data = re.sub(pattern, ' e.g.- ', data)  # Replacing whitespace and newline.

    res = sent_tokenize(data)  # Sentence tokenization

    with open(output_file_path, 'w') as fw:
        sentence_cnt = 1
        for s in res:
            fw.write(f'{sentence_cnt} --> {str(s)} \n')
            tokens = word_tokenize(s)  # Words tokenization
            fw.write(f'\n TOKENS --> {tokens} \n\n')
            sentence_cnt += 1

    return sentence_cnt


if __name__ == '__main__':
    i_path = input('Enter The Input Path: ')  # Get user's input files directory path
    o_path = input('Enter The Output Path: ')  # Get user's output files directory path

    i_path_exist = os.path.exists(i_path)  # Check the user input path
    o_path_exist = os.path.exists(o_path)  # Check the user output path

    if i_path_exist and o_path_exist:
        input_path = i_path + '*'

        for file in glob.glob(input_path):
            fname = os.path.basename(file)
            filename, ext = os.path.splitext(fname)
            new_i_path = i_path + fname

            with open(new_i_path, "r") as fr:
                lines = fr.read()

            total_sentences = sentence_extraction(o_path, filename, lines)
            print(f"\n \n Total Sentences For  {fname} - {total_sentences} ")
    else:
        print("\n \n INVALID PATHS ")

