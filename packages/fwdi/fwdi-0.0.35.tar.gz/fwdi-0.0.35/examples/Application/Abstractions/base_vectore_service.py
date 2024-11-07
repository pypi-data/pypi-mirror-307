from abc import ABCMeta, abstractmethod
import faiss
from fwdi.Application.Abstractions.base_service import BaseServiceFWDI


class BaseVectoreService(BaseServiceFWDI, metaclass=ABCMeta):

    @abstractmethod
    def create_vector_db_v1(vector_db_path:str, lst_final_doc_sent_summ:list, filed_name:str) -> faiss.IndexIVFFlat:
        pass
