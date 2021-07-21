import re

import spacy


class SpacyTextAnalysis:
    def __init__(self, o_path, fname, lines):
        self.o_path = o_path
        self.file_name = fname
        self.f_data = lines
        self.s_dataset = spacy.load('en_core_web_sm')

    def tokens_extraction(self):
        """
        This method extracts sentence from the given text file and
        gives POS Tag & dependency information for each sentence token.

        Keyword arguments:
        output_path -- output path for the file
        filename -- name of the file
        data -- file content
        """
        output_file_name = self.file_name + '_spacy.txt'
        output_file_path = self.o_path + output_file_name

        total_np_counter = 0
        pattern = '\se.g.\s'

        print('\n\n Spacy Output File Name --> ', output_file_name)

        data = self.f_data

        data = data.replace('\n\n', ' ')  # Replacing extra new lines.
        data = data.replace('\n', ' ')
        data = re.sub(pattern, ' e.g.- ', data)  # Replacing whitespace and newline.

        f_dataset = self.s_dataset(data)
        sentences = list(f_dataset.sents)

        with open(output_file_path, 'w') as fw:
            sentence_cnt = 0
            total_tokens = 0
            ftk_list = []
            total_org, total_person, total_gpe, total_dates = 0, 0, 0, 0

            for s in sentences:
                s_ftk_list = []
                fw.write(f'sentence {sentence_cnt + 1} --> {s} \n')

                # Word tokens for each sentence
                for w_tk in s:
                    fw.write(f'\n TOKEN ---> {w_tk.text}'
                             f'\n LEMA ---> {w_tk.lemma_}'
                             f'\n POS TAG ---> {w_tk.pos_}'
                             f'\n TAG  ---> {w_tk.tag_}'
                             f'\n DEPENDENCY  --->  {w_tk.dep_}'
                             f'\n ALPHABET  --->  {w_tk.is_alpha}'
                             f'\n IS STOPWORD ?  ---> {w_tk.is_stop}'
                             f'\n IS SPACE ? ---> {w_tk.is_space}'
                             f'\n {"*" * 50} \n\n'
                             )

                    if not w_tk.is_stop:
                        ftk_list.append(w_tk.text)
                        s_ftk_list.append(w_tk.text)

                    total_tokens += 1

                fw.write(f'\n --- FILTERED TOKENS --- \n\n {s_ftk_list}\n\n TOTAL FILTERED TOKENS ==> {len(s_ftk_list)} \n\n')

                # NER
                fw.write('\n --- NER --- \n')
                for x in s.ents:
                    if x.label_ == 'ORG':
                        total_org += 1
                    if x.label_ == 'PERSON':
                        total_person += 1
                    if x.label_ == 'GPE':
                        total_gpe += 1
                    if x.label_ == 'DATE':
                        total_dates += 1

                    fw.write('\n' + x.text + '==> ' + x.label_ + '\n\n')

                fw.write(f'\n {"*" * 50} \n\n')

                # Noun chunks
                np = list(s.noun_chunks)
                total_np_counter += len(np)
                fw.write('\n ---- NOUN CHUNKS ---- \n')
                fw.write(f'\n {np} \n')
                fw.write(f'\n TOTAL NOUN CHUNKS --> {len(np)}')
                fw.write(f'\n {"*" * 50} \n\n')

                sentence_cnt += 1

        # Report data
        report_dict = {'output_file_name': output_file_name,
                       'total_sentences': sentence_cnt,
                       'total_tokens': total_tokens,
                       'total_filter_token': len(ftk_list),
                       'total_np': total_np_counter,
                       'total_org': total_org,
                       'total_persons': total_person,
                       'total_places': total_gpe,
                       'total_dates': total_dates
                       }

        return report_dict

