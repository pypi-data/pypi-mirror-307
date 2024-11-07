import os
import pandas as pd

from Application.Abstractions.base_similarity_data_store import BaseSimilarityDataStore
from Utilites.ext_path import ExtPath

class SimilarityDataStore(BaseSimilarityDataStore):

    @staticmethod
    def read(path: str) -> list[dict]:
        lst_doc = pd.read_pickle(path).to_dict('records')

        return lst_doc

    @staticmethod
    def write(lst_doc: list[dict], path: str, columns: list = None) -> bool:
        try:
            ExtPath.exists_or_create_path(os.path.dirname(path))
            if columns is not None:
                data_frame = pd.DataFrame(lst_doc, columns=columns)
            else:
                data_frame = pd.DataFrame(lst_doc)
            data_frame.to_pickle(path)

            return True
        except Exception as ex:
            raise Exception(ex)