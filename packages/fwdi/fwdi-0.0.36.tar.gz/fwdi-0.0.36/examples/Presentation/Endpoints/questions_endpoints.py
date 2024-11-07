from fastapi import Depends, Security
from fwdi.Application.Abstractions.base_service import BaseServiceFWDI
from fwdi.Application.DTO.Auth.model_user import User
from fwdi.Infrastructure.JwtService.jwt_service import JwtServiceFWDI
from fwdi.Application.Configs.service_congif import ServiceConfig
from Application.DTO.ContextReqestToLLMModel.context_request_to_llm import DataForLlmModel
from Application.DTO.Request.rag_question_project import RequestToLLM
from Application.Usecases.usecase_search import ServiceSearch
from Application.Usecases.usecase_task_manager import UsecaseTaskManager
from Utilites.ext_rest import RestResponse


class QuestionEndpoint(BaseServiceFWDI):
    def search(question_pack:RequestToLLM,
                  search_answer: ServiceSearch=Depends(), 
                  config: ServiceConfig=Depends(),
                  task_manager: UsecaseTaskManager=Depends(),
                  current_user: User = Security(JwtServiceFWDI.get_current_active_user, scopes=["question"]),):
        if not config.service_avaible:
            QuestionEndpoint.__log__('Сервис не доступен.')
            return RestResponse.response_200("Сервис временно недоступен.")
            
        if not question_pack.refined_question:
            context_LLM = DataForLlmModel(question_pack, '', None)
            place_queue = task_manager.add_task(context_LLM)
            if place_queue is None:
                QuestionEndpoint.__log__('Repeated request from one user.')                
                response = 'Вы выполнили запрос к системе, ожидайте, пожалуйста, ответа.'
            elif place_queue == 0:
                response = 'Предварительная обработка текста вашего вопроса.'
            else:
                response = f'Предварительная обработка текста вашего вопроса. Ваш запрос принят, вы {place_queue} в очереди.'
        else:
            context_for_llm = search_answer.relevant_search(question_pack)
            if type(context_for_llm) != str:
                response = task_manager.add_task(context_LLM=context_for_llm)
            else:
                response = context_for_llm
        
        QuestionEndpoint.__log__(f"Response:{response}")

        if response == None:
            return RestResponse.make_response("Error auth")
        else:
            return RestResponse.response_200(response)

        
    def answer(task_manager: UsecaseTaskManager=Depends(),
                config: ServiceConfig=Depends(),
               current_user: User = Security(JwtServiceFWDI.get_current_active_user, scopes=["question"]),):
        
        if not config.service_avaible:
            QuestionEndpoint.__log__('Сервис не доступен.')
            return RestResponse.response_200("Сервис временно недоступен.")
            
        response = task_manager.get_answer()

        return response
        

