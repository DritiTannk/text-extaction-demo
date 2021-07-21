import re

import nltk
from nltk import sent_tokenize, word_tokenize, ne_chunk, Tree
from nltk.corpus import stopwords
from nltk.parse.stanford import StanfordDependencyParser
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.stem.snowball import SnowballStemmer


class NltkAnalysis:
    """
    This class handles all the text analysis through nltk library.
    """

    def __init__(self, i_path, o_path, fname, lines):
        self.i_path = i_path
        self.o_path = o_path
        self.file_name = fname
        self.f_data = lines

    def extract_noun_phrase(self, filtered_post):
        """
        This method extracts noun phrases from given tokens

        filtered_post: word tokens with its post
        """
        pattern = 'NP: {<DT>?<JJ>*<NN>}'  # Chunking pattern
        chunk_result = nltk.RegexpParser(pattern)
        result = chunk_result.parse(filtered_post)

        try:
            parse_tree = Tree.fromstring(str(result))

            final_result = [" ".join([leaf.split('/')[0] for leaf in subtree.leaves()]) for subtree in parse_tree if
                            type(subtree) == Tree and subtree.label() == "NP"]

            return final_result

        except Exception as e:
            print(e)

    def ner_tree_traverse(self, filtered_post):
        """
        It extracts NER - Persons, GPE, Organization, Date
        """
        ner, ner_res = ['ORGANIZATION', 'PERSON', 'GPE', 'DATE'], {}

        try:
            ner_result = ne_chunk(filtered_post)
            main_tree = Tree.fromstring(str(ner_result))

            for e in ner:
                key_name = e + '_result'
                key_result = [" ".join([leaf.split('/')[0] for leaf in subtree.leaves()]) for subtree in main_tree if
                        type(subtree) == Tree and subtree.label() == e]
                ner_res[e] = key_result

            return ner_res

        except Exception as e:
            print(e)

    def generate_bigrams(self, filtered_tk):
        """
        This method generates bigrams for the given tokens.
        """
        bigrams_obj = nltk.bigrams(filtered_tk)
        bg_list = []

        for a, b in bigrams_obj:
            bg = ' '.join((a, b))
            bg_list.append(bg)

        return bg_list

    def generate_trigrams(self, filtered_tk):
        """
        This method generates trigrams for the given tokens.
        """
        trigrams_obj = nltk.trigrams(filtered_tk)
        tg_list = []

        for a, b, c in trigrams_obj:
            tg = ' '.join((a, b, c))
            tg_list.append(tg)

        return tg_list

    def porter_stemming(self, filtered_tk):
        """
        This method performs stemming process using porter algorithm
        """
        p_stem_list = []
        porter = PorterStemmer()

        for w in filtered_tk:
            p_result = porter.stem(w)
            p_stem_list.append(p_result)

        return p_stem_list

    def snowball_stemming(self, filtered_tk):
        """
        This method performs stemming process using snowball algorithm
        """
        s_stem_list = []
        snowball = SnowballStemmer(language='english')

        for w in filtered_tk:
            s_result = snowball.stem(w)
            s_stem_list.append(s_result)

        return s_stem_list

    def word_lemmetization(self, filtered_tk):
        """
        This method performs lemmetization process.
        """
        lemmas_list = []
        lemmetizer = WordNetLemmatizer()

        for w in filtered_tk:
            l_result = lemmetizer.lemmatize(w)
            lemmas_list.append(l_result)

        return lemmas_list

    def np_write(self, nps):
        """
        This method creates new file for the noun-phrases.
        """
        output_file_name = self.file_name + '_noun_phrases.txt'
        output_file_path = self.o_path + output_file_name

        with open(output_file_path, 'a') as npw:
            if len(nps) != 0:
                npw.write(f'\n\n {nps}\n\n')

        return 'success'

    def sentence_extraction(self):
        """
        This method extracts sentence from the given text file.
        """
        entities = ['ORGANIZATION', 'PERSON', 'GPE', 'DATE']

        output_file_name = self.file_name + '_nltk.txt'
        output_file_path = self.o_path + output_file_name
        data = self.f_data

        stop_words = set(stopwords.words('english'))
        jar_path = '/home/dritit/NLP_Projects/text_extaction_demo/stanford-parser-4.2.0/stanford-parser-full-2020-11-17' \
                   '/stanford-parser.jar'
        models_path = '/home/dritit/NLP_Projects/text_extaction_demo/stanford-parser-4.2.0/stanford-parser-full-2020-11' \
                      '-17/stanford-parser-4.2.0-models.jar'

        dependency_parser = StanfordDependencyParser(path_to_jar=jar_path, path_to_models_jar=models_path)

        print('\n\n NLTK Output File Name --> ', output_file_name)
        pattern = '\se.g.\s'

        data = data.replace('\n\n', ' ')  # Replacing extra new lines.
        data = data.replace('\n', ' ')
        data = re.sub(pattern, ' e.g.- ', data)  # Replacing whitespace and newline.

        res = sent_tokenize(data)  # Sentence tokenization

        total_tokens, total_filtered_tokens, total_bigrams = 0, 0, 0
        total_trigrams, total_np, total_p_stem = 0, 0, 0
        total_org, total_person, total_gpe = 0, 0, 0
        total_dates, total_s_stem, total_lemmas = 0, 0, 0

        with open(output_file_path, 'w') as fw:
            sentence_cnt = 1

            for s in res:
                fw.write(f'{sentence_cnt} --> {str(s)} \n')

                # Words tokenization
                tokens = word_tokenize(s)
                total_tokens += len(tokens)
                fw.write(f'\n\n ---- TOKENS ----\n\n {tokens} \n\n TOTAL TOKENS ==> {len(tokens)}')

                # POS tagging for tokens
                tokens_post = nltk.pos_tag(tokens)
                fw.write(f'\n\n ---- POST ----\n\n {tokens_post} \n\n')

                # Filtering tokens
                filtered_result = [w for w in tokens if not w.lower() in stop_words]
                total_filtered_tokens += len(filtered_result)
                fw.write(f'\n\n ---- TOKENS AFTER STOP-WORDS REMOVAL ---- \n\n {filtered_result}')
                fw.write(f'\n\n TOTAL FILTERED TOKENS ==>  {len(filtered_result)}')

                # POS tagging for filtered tokens
                filtered_post = nltk.pos_tag(filtered_result)
                fw.write(f'\n\n ---- POST FOR FILTERED TOKENS ----\n\n {filtered_post} \n\n')

                # Dependency parsing
                d_result = dependency_parser.raw_parse(s)
                result_tree = next(d_result)
                fw.write(f'\n\n --- DEPENDENCY --- \n\n {list(result_tree.triples())}\n\n')

                # Bigrams
                bigrams = self.generate_bigrams(filtered_result)
                total_bigrams += len(bigrams)
                fw.write(f'\n\n ---- BI-GRAMS ---- \n\n {bigrams} \n\n TOTAL BIGRAMS --> {len(bigrams)} \n\n')

                # Trigrams
                trigrams = self.generate_trigrams(filtered_result)
                total_trigrams += len(trigrams)
                fw.write(f'\n\n ---- TRI-GRAMS ---- \n\n {trigrams} \n\n TOTAL TRIGRAMS --> {len(trigrams)} \n\n')

                # Noun phrase chunks
                np = self.extract_noun_phrase(filtered_post)
                total_np += len(np) if np is not None else 0

                if np is not None:
                    np_len = len(np)
                    total_np += np_len
                else:
                    np = '[]'
                    np_len = 0

                fw.write(f'\n\n ---- NOUN PHRASES ---- \n\n {np} \n\n TOTAL NOUN PHRASES --> {np_len} \n\n')
                self.np_write(np)

                # NER extraction
                ner_r = self.ner_tree_traverse(filtered_post)
                fw.write('\n\n ---- NER ----\n\n ')

                if ner_r is not None:
                    for e in entities:
                        fw.write(f'\n {e} ---> {ner_r[e]}')
                        fw.write(f'\n TOTAL {e} ENTITY --> {len(ner_r[e])} \n\n')
                        if e == 'ORGANIZATION':
                            total_org += len(ner_r[e])
                        elif e == 'PERSON':
                            total_person += len(ner_r[e])
                        elif e == 'GPE':
                            total_gpe += len(ner_r[e])
                        elif e == 'DATE':
                            total_dates += len(ner_r[e])
                        else:
                            print('\n \n NOT FOUND')
                else:
                    fw.write(f'\n []')

                # Porter stemming
                p_stem_res = self.porter_stemming(filtered_result)
                total_p_stem += len(p_stem_res)
                fw.write(f'\n\n ---- PORTER STEMMING ----\n\n{p_stem_res}')
                fw.write(f'\n\n TOTAL PORTER STEM WORDS ==> {len(p_stem_res)}\n\n')

                # Snowball stemming
                s_stem_res = self.snowball_stemming(filtered_result)
                total_s_stem += len(s_stem_res)
                fw.write(f'\n\n ---- SNOWBALL STEMMING ----\n\n{s_stem_res}')
                fw.write(f'\n\n TOTAL SNOWBALL STEM WORDS ==> {len(s_stem_res)}\n\n')

                # Lemmatization
                lemma_res = self.word_lemmetization(filtered_result)
                total_lemmas += len(lemma_res)
                fw.write(f'\n\n ---- LEMMATIZATION ----\n\n{lemma_res}')
                fw.write(f'\n\n TOTAL LEMMATIZE WORDS ==> {len(lemma_res)}\n\n')

                sentence_cnt += 1
                fw.write(f'{"******" * 20}\n\n')

        # Report data
        report_dict = {'output_file_name': output_file_name,
                       'total_sentences': sentence_cnt,
                       'total_tokens': total_tokens,
                       'total_filter_token': total_filtered_tokens,
                       'total_bigrams': total_bigrams,
                       'total_trigrams': total_trigrams,
                       'total_np': total_np,
                       'total_p_stem': total_p_stem,
                       'total_s_stem': total_s_stem,
                       'total_lemmas': total_lemmas,
                       'total_org': total_org,
                       'total_persons': total_person,
                       'total_places': total_gpe,
                       'total_dates': total_dates
                     }

        return report_dict
