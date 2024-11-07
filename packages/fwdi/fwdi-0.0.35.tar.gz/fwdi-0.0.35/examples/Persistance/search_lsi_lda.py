from argparse import Action
import gensim
from Application.Abstractions.base_lsi_lda import BaseLsiLda
from Application.Abstractions.base_search_lsi_lda import BaseSearchLsiLda
from Utilites.tools import TextTools



class SearchLsiLda(BaseSearchLsiLda):

    def __init__(self) -> None:
        super().__init__()
        self.__lemmatize_fn: Action = TextTools.lemmatize_fn
        self.__clearing_stopword: Action = TextTools.delete_stop_word


    def search(self, text_to_search: str, k_top: int, lsi_lda_db: BaseLsiLda) -> list:
        new_doc = self.__lemmatize_fn(text_to_search)
        new_doc = self.__clearing_stopword(new_doc)
        new_doc = gensim.parsing.preprocessing.preprocess_string(new_doc)
        new_vec = lsi_lda_db.dict_corp[0].doc2bow(new_doc)
        vec_bow_tfidf = lsi_lda_db.tfidf[new_vec]
        vec_lsi = lsi_lda_db.lsi[vec_bow_tfidf]
        sims = lsi_lda_db.index[vec_lsi]

        result_search = sorted(enumerate(sims), key=lambda item: -item[1])[:k_top]

        return result_search

    # -----------------------------------------------------------------------------------------------------------------------

    def get_doc_by_result(self, result_search: list, lsi_lda_db: BaseLsiLda) -> list[dict]:
        lst_doc_result: list = []

        for i, result in enumerate(result_search):
            sentence = [item for item in lsi_lda_db.lst_all_doc_sentences if item['id'] == result[0]]
            if len(sentence) > 0:
                document = [doc for doc in lsi_lda_db.lst_all_doc if doc['id'] == sentence[0]['index_art']]
                if len(document) > 0:
                    document = document[0]
                    lst_doc_result.append({'id': i, 'document': document, 'distance': result[1]})

        return lst_doc_result
    