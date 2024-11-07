from Application.Abstractions.base_llm_service import BaseLlmService
from Application.DTO.Request.custom_prompt_view_model import CustomPromptViewModel
from Application.DTO.Response.response_rag_inference_view_model import ResponseRagInferenceViewModel
from Application.DTO.Request.request_answering_llm import RequestLLN
from fwdi.Application.Abstractions.base_rest_client import BaseRestClientFWDI


class LLMService(BaseLlmService):

    def __init__(self, rest_client: BaseRestClientFWDI) -> None:
        super().__init__()
        self.__is_busy: bool = False
        self.__rest_client: BaseRestClientFWDI = rest_client

    def request_to_llm(self, project: str, question: str,
                context_question: list, max_new_token: int, prompt: str) -> ResponseRagInferenceViewModel | None:
            
            if not self.__rest_client.IsAuth:
                self.__rest_client.login()

                #logger.info('Auth to Rest service is OK !')

            self.__is_busy = True

            custom_prompt_template = prompt
            request = RequestLLN(question=question, project=project, article=context_question, distance=[],
                                max_new_token=max_new_token, template_pompt=custom_prompt_template)
            
            result = self.__rest_client.get(path='/api/v1.0/rag_query', _data=request)

            self.__is_busy = False

            return result


    def IsBusy(self):

        return self.__is_busy
    
    def request_v2(self,
                   view_model: CustomPromptViewModel) -> ResponseRagInferenceViewModel | None:
        try:
            if self.__rest_client.login():
                print()
                #logger.info('Auth to Rest service is OK !')
                
                result = self.__rest_client.get('/api/v1.0/rag_inference', _data=view_model)
                return result
            else:
                return None
        except Exception as ex:
            LLMService.__log__(ex, 'error')
            return None


