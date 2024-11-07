from abc import abstractmethod, ABCMeta
from fwdi.Application.Abstractions.base_service import BaseServiceFWDI


class BaseSimilarityDataStore(BaseServiceFWDI, metaclass=ABCMeta):

    @staticmethod
    @abstractmethod
    def read(path: str) -> list[dict]:
        pass

    @staticmethod
    @abstractmethod
    def write(lst_doc: list, path: str, columns: list) -> bool:
        pass