from abc import ABCMeta, abstractmethod
from fwdi.Application.Abstractions.base_service import BaseServiceFWDI

from Application.Abstractions.base_proxy_web_parse import BaseProxyWebParse
from Application.Abstractions.base_similarity_data_store import BaseSimilarityDataStore
from Application.Abstractions.base_stage_data_processing import BaseStageDataProcessing
from Application.Abstractions.base_vectore_service import BaseVectoreService



class BaseUsecaseContextDataBase(BaseServiceFWDI, metaclass=ABCMeta):

    @abstractmethod
    def create_vectore_database(self):
        pass