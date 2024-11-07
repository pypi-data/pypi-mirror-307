from abc import abstractmethod, ABCMeta
from fwdi.Application.Abstractions.base_service import BaseServiceFWDI



class BaseEmbeddingModel(BaseServiceFWDI, metaclass=ABCMeta):

    @abstractmethod
    def encode(self, text:str) -> list:
        pass