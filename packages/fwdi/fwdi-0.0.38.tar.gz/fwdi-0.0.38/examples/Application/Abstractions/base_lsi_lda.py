from abc import abstractmethod, ABCMeta
from typing import TypeVar
from fwdi.Application.Abstractions.base_service import BaseServiceFWDI


_T = TypeVar("_T", bound='BaseLsiLda')

class BaseLsiLda(BaseServiceFWDI, metaclass=ABCMeta):

    @abstractmethod
    def create_lsi_lda_matrix_db_v2(self, flag_update: bool) -> _T:
        pass

    @property
    @abstractmethod
    def dict_corp(self):
        pass

    @property
    @abstractmethod
    def tfidf(self):
        pass

    @property
    @abstractmethod
    def lsi(self):
        pass

    @property
    @abstractmethod
    def index(self):
        pass

    @property
    @abstractmethod
    def lst_all_doc_sentences(self):
        pass
    
    @property
    @abstractmethod
    def lst_all_doc(self):
        pass

