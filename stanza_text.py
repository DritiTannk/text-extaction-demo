import os
import glob

import stanza


def report_generation(report_data, output_path):
    """
    This method generates the statistic report for stanza analysis
    """
    output_file_name = 'stanza_analysis_report.txt'
    output_file_path = output_path + output_file_name

    with open(output_file_path, 'a') as fa:
        fa.write(f'\n\n FILE NAME ==> {report_data.get("output_file_name", 0)}'
                 f'\n\n TOTAL SENTENCES ==> {report_data.get("total_sentences", 0)}'
                 f'\n\n TOTAL TOKENS  ==>  {report_data.get("total_tokens", 0)}'
                 f'\n\n TOTAL ORGANIZATION  ==>  {report_data.get("total_org", 0)}'
                 f'\n\n TOTAL PERSONS  ==>  {report_data.get("total_persons", 0)}'
                 f'\n\n TOTAL PLACES  ==>  {report_data.get("total_places", 0)}'
                 f'\n\n TOTAL DATES  ==>  {report_data.get("total_dates", 0)}'
                 f'\n\n {"*****"*20}\n\n'
                 )


def text_analysis(output_path, filename, data, nlp):
    """
    This method performs analysis on raw text like tokenization, post, etc using stanza library.

    Keyword arguments:
    output_path -- output path for the file
    filename -- name of the file
    data -- file content
    nlp -- pipeline object
    """
    output_file_name = filename + '_stanza.txt'
    output_file_path = output_path + output_file_name

    doc = nlp(data)

    sent_count, tokens_count, person_ent, org_ent, loc_ent, date_ent = 0, 0, [], [], [], []

    with open(output_file_path, 'w') as fw:

        for i, sentence in enumerate(doc.sentences, start=1):
            fw.write(f'\n\n {i} --->  {sentence.text}')

            # Tokenization
            sent_tokens = [f'{token.text}' for token in sentence.tokens]
            tokens_len = len(sent_tokens)
            tokens_count += tokens_len
            fw.write(f'\n\n {"----" * 5} TOKENS {"----" * 5} \n\n {sent_tokens}')
            fw.write(f'\n\n TOTAL TOKENS  ---> {tokens_len}')

            # POS tagging
            words_pos = [f'{(token.text, token.upos)}' for token in sentence.words]
            fw.write(f'\n\n {"----" * 5} POST {"----" * 5} \n\n {words_pos}')

            # Lemmatization
            words_lemma = [f'{(token.text, token.lemma)}' for token in sentence.words]
            fw.write(f'\n\n {"----" * 5} LEMMAS {"----" * 5} \n\n {words_lemma}')
            fw.write(f'\n\n TOTAL LEMMAS ---> {len(words_lemma)}')

            # Dependency parsing
            words_dp = [f'{(word.text, word.deprel)}' for word in sentence.words]
            fw.write(f'\n\n {"----" * 5} DEPENDENCY PARSING {"----" * 5} \n\n {words_dp}')

            # NER
            fw.write(f'\n\n {"----" * 5} NER {"----" * 5} \n\n')
            for ent in sentence.ents:
                fw.write(f'\n\n {ent.text} --> {ent.type}')
                if ent.type == 'PERSON':
                    person_ent.append(ent.text)
                if ent.type == 'ORG':
                    org_ent.append(ent.text)
                if ent.type == 'DATE':
                    date_ent.append(ent.text)
                if ent.type == 'GPE':
                    loc_ent.append(ent.text)

            fw.write(f'\n\n\n {"*****" * 10}')
            sent_count = i

    # Report data
    report_dict = {'output_file_name': output_file_name,
                   'total_sentences': sent_count,
                   'total_tokens': tokens_count,
                   'total_lemmas': len(words_lemma),
                   'total_org': len(org_ent),
                   'total_persons': len(person_ent),
                   'total_places': len(loc_ent),
                   'total_dates': len(date_ent)
                   }

    report_generation(report_dict, output_path)

    return sent_count


if __name__ == '__main__':
    i_path = input('Enter The Input Path: ')  # Get user's input files directory path
    o_path = input('Enter The Output Path: ')  # Get user's output files directory path

    i_path_exist = os.path.exists(i_path)  # Check the user input path
    o_path_exist = os.path.exists(o_path)  # Check the user output path

    if i_path_exist and o_path_exist:
        input_path = i_path + '*'
        nlp = stanza.Pipeline(lang='en', processors='tokenize, pos, lemma, depparse, ner')

        for file in glob.glob(input_path):
            fname = os.path.basename(file)
            filename, ext = os.path.splitext(fname)
            new_i_path = i_path + fname

            print(f'\n\n {"-----" * 5} {fname} Processing Starts {"-----" * 5}')

            with open(new_i_path, "r") as fr:
                lines = fr.read()

            total_sentences = text_analysis(o_path, filename, lines, nlp)
            print(f"\n \n Total Sentences For  {fname} - {total_sentences} ")
    else:
        print("\n \n INVALID PATHS ")

