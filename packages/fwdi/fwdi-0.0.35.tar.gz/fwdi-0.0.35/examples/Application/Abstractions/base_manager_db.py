from abc import abstractmethod, ABCMeta
from fwdi.Application.Abstractions.base_service import BaseServiceFWDI
import faiss
from pandas import DataFrame
from Application.Abstractions.base_lsi_lda import BaseLsiLda


class BaseManagerContextDB(BaseServiceFWDI, metaclass=ABCMeta):

     @abstractmethod
     def get_vector_store(self) -> faiss.IndexIVFFlat:
          pass

     @abstractmethod
     def get_pickle_store(self) -> DataFrame:
          pass

     @abstractmethod
     def get_matrix_store(self) -> BaseLsiLda:
          pass