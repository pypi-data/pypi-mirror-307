import pandas as pd
from Application.Abstractions.base_lsi_lda import BaseLsiLda
from Application.Abstractions.base_search_lsi_lda import BaseSearchLsiLda
from Utilites.ext_path import ExtPath
import faiss
from pandas import DataFrame
from Application.Abstractions.base_manager_db import BaseManagerContextDB



class ManagerDbContext(BaseManagerContextDB):
    
    def __init__(self, lsi_lda_db: BaseLsiLda, search_lsi_lda: BaseSearchLsiLda) -> None:
        super().__init__()
        self.vectore_store = faiss.read_index('Persistance/Databases/vectorstore/index.faiss') if ExtPath.exists_file('Persistance/Databases/vectorstore/index.faiss') else None
        self.pickle_store = pd.read_pickle('Persistance/Databases/picklestore/ParseData.pkl') if ExtPath.exists_file('Persistance/Databases/picklestore/ParseData.pkl') else None
        self.lsi_lda = lsi_lda_db.create_lsi_lda_matrix_db_v2(False)
        self.search_lsi_lda = search_lsi_lda
    
    def get_vector_store(self) -> faiss.IndexIVFFlat:
        return self.vectore_store

    def get_pickle_store(self) -> DataFrame:
        return self.pickle_store

    def get_matrix_store(self) -> BaseSearchLsiLda:
        return self.search_lsi_lda
    

