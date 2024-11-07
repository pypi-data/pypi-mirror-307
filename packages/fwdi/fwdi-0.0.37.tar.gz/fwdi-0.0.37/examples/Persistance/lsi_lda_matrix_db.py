import gensim
import os
import pandas as pd
from tqdm import tqdm
from dawg_python import Dictionary
from gensim.interfaces import TransformedCorpus
from gensim import corpora
from gensim.models import TfidfModel, LsiModel
from gensim.parsing.preprocessing import preprocess_documents
from Application.Abstractions.base_lsi_lda import BaseLsiLda, _T
from Utilites.ext_path import ExtPath



class LsiLdaVector(BaseLsiLda):
    def __init__(self) -> None:
        self.__project_name = 'itc_helper'
        self.__model_path = 'Persistance/Databases/lsi_lda_store'
        self.__base_path: str = f'{self.__model_path}/{self.__project_name}/'
        self.__full_path_dict: str = f"{self.__base_path}{self.__project_name}.dict"
        self.__full_path_corp: str = f"{self.__base_path}{self.__project_name}.corp"
        self.__full_path_tfidf: str = f"{self.__base_path}{self.__project_name}.tdidf"
        self.__full_path_lsi: str = f"{self.__base_path}{self.__project_name}.lsi"
        self.__full_path_similar_matrix: str = f"{self.__base_path}{self.__project_name}.simat"
        self.__path_lsi_lds_sent: str = f"{self.__base_path}lsi_lda_sentences.pkl"
        self.__path_lsi_lds_doc: str = f"{self.__base_path}lsi_lda__doc.pkl"
        self.__lst_all_doc_sentences: list[dict] = []
        self.__lst_all_doc: list[dict] = []
        self.__dict_corp: tuple[Dictionary, list]
        self.__tfidf = None
        self.__corpus_tfidf = None
        self.__lsi = None
        self.__index = None
        self.__check_base_dir()

    # ===================================================================================================================
    # ===================================================================================================================
    @property
    def dict_corp(self):
        return self.__dict_corp
    @property
    def tfidf(self):
        return self.__tfidf
    @property
    def lsi(self):
        return self.__lsi
    @property
    def index(self):
        return self.__index
    @property
    def lst_all_doc_sentences(self):
        return self.__lst_all_doc_sentences
    @property
    def lst_all_doc(self):
        return self.__lst_all_doc

    def __check_base_dir(self):
        if not os.path.exists(self.__model_path):
            os.makedirs(self.__model_path)

        if not os.path.exists(self.__base_path):
            os.makedirs(self.__base_path)

    # -------------------------------------------------------------------------------------------------------------------

    def __get_or_create_dictionary_corpus(self, dataset: list) -> tuple[Dictionary, list]:
        if (not os.path.exists(self.__full_path_dict)) or (not os.path.exists(self.__full_path_corp)):

            cleared_dataset = [item['text'] for item in dataset]
            processed_corpus = preprocess_documents(cleared_dataset)

            dictionary = gensim.corpora.Dictionary(processed_corpus)
            bow_corpus = [dictionary.doc2bow(text) for text in processed_corpus]

            self.__save_corpus_dictionary(dictionary=dictionary, bow_corpus=bow_corpus)
        else:
            dictionary, bow_corpus = self.__load_corpus_dictionary()

        return tuple((dictionary, bow_corpus))

    # -------------------------------------------------------------------------------------------------------------------

    def __get_or_create_tfidf(self, bow_corpus: list) -> TfidfModel:
        if not os.path.exists(self.__full_path_tfidf):
            tfidf = gensim.models.TfidfModel(bow_corpus, smartirs='npu')    
            #tfidf = gensim.models.TfidfModel(bow_corpus, smartirs='ntc')
            tfidf.save(self.__full_path_tfidf)
        else:
            tfidf = gensim.models.TfidfModel.load(self.__full_path_tfidf)

        return tfidf

    # -----------------------------------------------------------------------------------------------------------------------

    def __get_or_create_lsi(self, corpus_tfidf: TransformedCorpus) -> LsiModel:
        if not os.path.exists(self.__full_path_lsi):
            lsi = gensim.models.LsiModel(corpus_tfidf, num_topics=100)
            lsi.save(self.__full_path_lsi)
        else:
            lsi = gensim.models.LsiModel.load(self.__full_path_lsi)

        return lsi

    # -----------------------------------------------------------------------------------------------------------------------

    def __get_or_create_similary_matrix(self, lsi: LsiModel,
                                        corpus_tfidf: TransformedCorpus) -> gensim.similarities.MatrixSimilarity:
        if not os.path.exists(self.__full_path_similar_matrix):
            index = gensim.similarities.MatrixSimilarity(lsi[corpus_tfidf])
            index.save(self.__full_path_similar_matrix)
        else:
            index = gensim.similarities.MatrixSimilarity.load(self.__full_path_similar_matrix)

        return index

    # ==================================================================================================================
    # ==================================================================================================================

    def __save_corpus_dictionary(self, dictionary: corpora.Dictionary, bow_corpus):
        dictionary.save(self.__full_path_dict)  # save dict to disk
        corpora.MmCorpus.serialize(self.__full_path_corp, bow_corpus)  # save corpus to disk

    # -----------------------------------------------------------------------------------------------------------------------

    def __load_corpus_dictionary(self):
        dictionary = corpora.Dictionary.load(self.__full_path_dict)
        bow_corpus = corpora.MmCorpus(self.__full_path_corp)

        return dictionary, bow_corpus

    # ================================================[/TEXT PREPARED SECTION]==========================================

    def create_lsi_lda_matrix_db_v2(self, flag_update: bool) -> _T:
        try:
            if not os.path.exists(f"{self.__base_path}lsi_lda__doc.pkl") or not os.path.exists(f"{self.__base_path}lsi_lda_sentences.pkl") or flag_update:
                # logger.info('LSI/LDA database does not exist')
                if ExtPath.exists_file('Persistance/Databases/picklestore/temp/ExportData.pkl'):
                    docs: list[dict] = pd.read_pickle('Persistance/Databases/picklestore/temp/ExportData.pkl').to_dict('records')
                    index_sentences:int = 0

                    for doc in docs:
                        self.__lst_all_doc.append({'id':doc['doc_id'],
                                            'document': doc['title'],
                                            'url': doc['url']})

                    with tqdm(desc="Create index document", total=len(self.__lst_all_doc)) as pb:
                        for item in self.__lst_all_doc:

                            index_art = item['id']
                            text_page = [item for item in docs if item['doc_id'] == index_art][0]['sentences']
                            for text in text_page:

                                self.__lst_all_doc_sentences.append({'id': index_sentences,
                                                                    'index_art': index_art,
                                                                    'text':text})
                                index_sentences += 1

                            pb.update(1)

                    df = pd.DataFrame(self.__lst_all_doc)
                    df.to_pickle(self.__path_lsi_lds_doc)

                    df = pd.DataFrame(self.__lst_all_doc_sentences)
                    df.to_pickle(self.__path_lsi_lds_sent)
                else:
                    #####logger.info('LSI/LDA database does not exist and ExportData.pkl does not exist')
                    return None
            else:
                ####logger.info('LSI/LDA database exists')
                df:pd.DataFrame = pd.read_pickle(f"{self.__base_path}lsi_lda_sentences.pkl")
                self.__lst_all_doc_sentences = df.to_dict('records') # values.tolist()

                df:pd.DataFrame = pd.read_pickle(f"{self.__base_path}lsi_lda__doc.pkl")
                self.__lst_all_doc = df.to_dict('records') # values.tolist()

            self.__load_or_create_vector()

        except Exception as ex:
            ####logger.error(f"ERROR:{ex}")
            return None

        finally:
            return self
    # =======================================================================================================================

    def __load_or_create_vector(self):
        self.__dict_corp = self.__get_or_create_dictionary_corpus(self.__lst_all_doc_sentences)

        self.__tfidf = self.__get_or_create_tfidf(self.__dict_corp[1])
        self.__corpus_tfidf = self.__tfidf[self.__dict_corp[1]]
        self.__lsi = self.__get_or_create_lsi(self.__corpus_tfidf)
        self.__index = self.__get_or_create_similary_matrix(self.__lsi, self.__corpus_tfidf)

