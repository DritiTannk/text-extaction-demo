import os
import glob

from extraction.nltk_analysis import NltkAnalysis
from extraction.spacy_analysis import SpacyTextAnalysis


def report_generation(output_path, report_data, spacy_data):
    """
    This method generates the statistic report of analysis done using nltk and spacy
    """
    output_file_name = 'analysis_report.txt'
    output_file_path = output_path + output_file_name

    with open(output_file_path, 'a') as fa:
        fa.write(f'\n\n\n {"----" * 10} {report_data.get("output_file_name", 0)} {"----" * 10} \n'
                 f'\n\n NLTK TOTAL SENTENCES ==> {report_data.get("total_sentences", 0)}'
                 f'\t\t\t SPACY TOTAL SENTENCES ==> {spacy_data.get("total_sentences", 0)}'
                 f'\n\n NLTK TOTAL TOKENS  ==>  {report_data.get("total_tokens", 0)} '
                 f'\t\t\t SPACY TOTAL TOKENS  ==>  {spacy_data.get("total_tokens", 0)}'
                 f'\n\n NLTK TOTAL FILTERED TOKENS  ==>  {report_data.get("total_filter_token", 0)} '
                 f'\t\t\t SPACY TOTAL FILTERED TOKENS  ==>  {spacy_data.get("total_filter_token", 0)}'
                 f'\n\n TOTAL BIGRAMS   ==>  {report_data.get("total_bigrams", 0)}'
                 f'\n\n TOTAL TRIGRAMS  ==>  {report_data.get("total_trigrams", 0)}'
                 f'\n\n NLTK TOTAL NOUN-PHRASES  ==>  {report_data.get("total_np", 0)}'
                 f'\t\t SPACY TOTAL NOUN-PHRASES  ==>  {spacy_data.get("total_np", 0)}'
                 f'\n\n TOTAL PORTER STEM WORDS  ==>  {report_data.get("total_p_stem", 0)}'
                 f'\n\n TOTAL SNOWBALL WORDS  ==>  {report_data.get("total_s_stem", 0)}'
                 f'\n\n TOTAL LEMMATIZATE WORDS  ==>  {report_data.get("total_lemmas", 0)}'
                 f'\n\n NLTK TOTAL ORGANIZATION  ==>  {report_data.get("total_org", 0)}'
                 f'\t\t\t SPACY TOTAL ORGANIZATION  ==>  {spacy_data.get("total_org", 0)}'
                 f'\n\n NLTK TOTAL PERSONS  ==>  {report_data.get("total_persons", 0)}'
                 f'\t\t\t SPACY TOTAL PERSONS  ==>  {spacy_data.get("total_persons", 0)}'
                 f'\n\n NLTK TOTAL PLACES  ==>  {report_data.get("total_places", 0)}'
                 f'\t\t\t SPACY TOTAL PLACES  ==>  {spacy_data.get("total_places", 0)}'
                 f'\n\n NLTK TOTAL DATES  ==>  {report_data.get("total_dates", 0)}'
                 f'\t\t\t SPACY TOTAL DATES  ==>  {spacy_data.get("total_dates", 0)}'
                 )


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

            print(f'\n\n -------- {fname} Processing Starts ---------- \n\n')

            # NLTK object
            nltk_obj = NltkAnalysis(new_i_path, o_path, filename, lines)
            res_dict = nltk_obj.sentence_extraction()
            print('\n\n ------ NLTK result dict ------ \n\n')
            print('\n\n ', res_dict)

            # Spacy object
            spacy_obj = SpacyTextAnalysis(o_path, filename, lines)
            spacy_dict = spacy_obj.tokens_extraction()
            print('\n\n ------ SPACY result dict ------ \n\n')
            print('\n\n ', spacy_dict)

            report_generation(o_path, res_dict, spacy_dict)
            print(f'\n\n -------- {fname} Processing Ends ---------- \n\n')

    else:
        print("\n \n INVALID PATHS ")
