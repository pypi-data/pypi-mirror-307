from abc import ABCMeta, abstractmethod
from fwdi.Application.Abstractions.base_service import BaseServiceFWDI


class BaseUploadRestClient(BaseServiceFWDI, metaclass=ABCMeta):
    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def auth(self):
        pass

    @abstractmethod
    def request_llm_service(self, pack):
        pass