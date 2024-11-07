from fwdi.Application.Abstractions.base_service_collection import BaseServiceCollectionFWDI
from Application.Abstractions.base_lsi_lda import BaseLsiLda
from Application.Abstractions.base_manager_db import BaseManagerContextDB
from Application.Abstractions.base_search_lsi_lda import BaseSearchLsiLda
from Persistance.lsi_lda_matrix_db import LsiLdaVector
from Persistance.manager_db import ManagerDbContext
from Persistance.search_lsi_lda import SearchLsiLda

class DependencyInjection():
    def AddPersistance(services:BaseServiceCollectionFWDI):
        services.AddSingleton(BaseLsiLda, LsiLdaVector)
        services.AddTransient(BaseSearchLsiLda, SearchLsiLda)
        services.AddSingleton(BaseManagerContextDB, ManagerDbContext)