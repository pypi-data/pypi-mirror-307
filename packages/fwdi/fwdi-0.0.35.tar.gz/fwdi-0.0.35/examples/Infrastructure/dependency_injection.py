from fwdi.Application.Abstractions.base_service_collection import BaseServiceCollectionFWDI
from fwdi.Infrastructure.Configs.rest_client_config import RestClientConfig

from Application.Abstractions.base_embedding_model import BaseEmbeddingModel
from Application.Abstractions.base_proxy_web_parse import BaseProxyWebParse
from Application.Abstractions.base_similarity_data_store import BaseSimilarityDataStore
from Application.Abstractions.base_stage_data_processing import BaseStageDataProcessing
from Application.Abstractions.base_vectore_service import BaseVectoreService
from Infrastructure.Config.web_parse_bsp_config import WebParseBSPConfig
from Infrastructure.Embeding.embeding_model import EmbeddingModel
from Infrastructure.Parse.proxy_web_parse import ProxyWebParse
from Infrastructure.Proccesing.stage_data_processing import StageDataProcessing
from Infrastructure.SmilarityService.vectore_service import VectoreService
from Infrastructure.similarity_data_store import SimilarityDataStore

class DependencyInjection():

    @staticmethod
    def AddConfigs(services:BaseServiceCollectionFWDI):

        web_parse_bsp = WebParseBSPConfig()
        web_parse_bsp.login='v.kurgin'
        web_parse_bsp.password='Vke667161!'
        services.AddSingleton(web_parse_bsp)

        restConfig = RestClientConfig()
        restConfig.server = 'cd-host-va.codev.dom'
        #restConfig.server = 'localhost'
        restConfig.port = 5100
        #restConfig.port = 5000
        restConfig.security_layer = False
        restConfig.username = 'admin'
        restConfig.password = 'admin'
        
        services.AddSingleton(restConfig)

        
    @staticmethod
    def AddInfrastructure(services:BaseServiceCollectionFWDI):
        services.AddSingleton(BaseEmbeddingModel, EmbeddingModel)
        services.AddTransient(BaseVectoreService, VectoreService)
        services.AddTransient(BaseStageDataProcessing, StageDataProcessing)
        services.AddTransient(BaseSimilarityDataStore, SimilarityDataStore)
        services.AddTransient(BaseProxyWebParse, ProxyWebParse)
    