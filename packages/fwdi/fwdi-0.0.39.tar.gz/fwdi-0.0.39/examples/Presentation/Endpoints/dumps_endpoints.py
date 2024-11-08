import os
from fastapi import Depends, Security
from fwdi.Application.Abstractions.base_service import BaseServiceFWDI
from fwdi.Application.DTO.Auth.model_user import User
from fwdi.Infrastructure.JwtService.jwt_service import JwtServiceFWDI
#from fwdi.Infrastructure.LoggingService.logging_service import LoggingServiceFWDI

from fwdi.Application.Configs.service_congif import ServiceConfig
from Application.DTO.Request.request_detail_dump import RequestDetailDump
from Application.DTO.Request.request_upload_dump import RequestUploadDump
from Utilites.ext_rest import RestResponse


class DumpEndpoint(BaseServiceFWDI):
    def dumps_list(request_pack:RequestUploadDump,
                  config: ServiceConfig=Depends(),
                  current_user: User = Security(JwtServiceFWDI.get_current_active_user, scopes=["admin"]),):
            if not config.service_avaible:
                print('Сервис не доступен.')
                return RestResponse.response_200("Сервис временно недоступен.")
            DumpEndpoint.__log__(f'Request dumps list: {request_pack}')

            dumps = os.listdir("Dumps")[-int(request_pack.quantity)::1]

            DumpEndpoint.__log__(f'Response dumps list: {len(dumps)}')
            return dumps

        
    def dump(request_pack: RequestDetailDump,
            config: ServiceConfig=Depends(),
            current_user: User = Security(JwtServiceFWDI.get_current_active_user, scopes=["admin"]),):
            if not config.service_avaible:
                print('Сервис не доступен.')
                return RestResponse.response_200("Сервис временно недоступен.")
            
            dump_name = request_pack.name
            DumpEndpoint.__log__(f'Request dump: {dump_name}')
            
            if os.path.exists(f"Dumps/{dump_name}"):
                with open(f"Dumps/{dump_name}", 'r', encoding="UTF-8") as fl:
                    text_dump = fl.read()
                    DumpEndpoint.__log__(f'Returning dump with name: {dump_name}')
                    return RestResponse.response_200(str(text_dump))
            
            DumpEndpoint.__log__(f'Is no dump named: {dump_name}')

            return RestResponse.response_200("Текстовый файл с таким именем не найден.")
    
    


