from abc import ABCMeta, abstractmethod
from fwdi.Application.Abstractions.base_service import BaseServiceFWDI

from Application.Abstractions.base_text_tools import BaseTextTools


class BaseStageDataProcessing(BaseServiceFWDI, metaclass=ABCMeta):

    @staticmethod
    @abstractmethod
    def preprocessing_text(lst_doc: list) -> list[dict]:
        pass

    @staticmethod
    @abstractmethod
    def prepared_sentences__universal(lst_final_doc_sent_summ:list[dict], contexts_field:list[str], text_tools: BaseTextTools) -> list[dict]:
        pass