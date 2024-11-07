from abc import abstractmethod, ABCMeta
from fwdi.Application.Abstractions.base_service import BaseServiceFWDI

from Application.Abstractions.base_lsi_lda import BaseLsiLda

class BaseSearchLsiLda(BaseServiceFWDI, metaclass=ABCMeta):

    @abstractmethod
    def search(self, text_to_search: str, k_top: int, lsi_lda_db: BaseLsiLda) -> list:
        pass

    @abstractmethod
    def get_doc_by_result(self, result_search: list, lsi_lda_db: BaseLsiLda) -> list[dict]:
        pass