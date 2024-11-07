from fastapi import Depends, Security
from fwdi.Application.Abstractions.base_service import BaseServiceFWDI
from fwdi.Application.DTO.Auth.model_user import User
from fwdi.Infrastructure.JwtService.jwt_service import JwtServiceFWDI
from Application.Abstractions.base_usecase_context_data_base import BaseUsecaseContextDataBase
from Application.Usecases.usecase_context_database import UsecaseContextDataBase



class ParseEndpoint(BaseServiceFWDI):
    def parse(usecase_create_db: UsecaseContextDataBase=Depends(), 
              current_user: User = Security(JwtServiceFWDI.get_current_active_user, scopes=["admin"]),):
        try:                    
            usecase_create_db.create_vectore_database()
        except Exception as ex:
            ParseEndpoint.__log__(ex, "ERROR")




        
