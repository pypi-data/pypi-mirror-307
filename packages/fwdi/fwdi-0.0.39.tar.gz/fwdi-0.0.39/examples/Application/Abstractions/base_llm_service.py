from abc import ABCMeta, abstractmethod
from fwdi.Application.Abstractions.base_service import BaseServiceFWDI

from Application.DTO.Request.custom_prompt_view_model import CustomPromptViewModel
from Application.DTO.Response.response_rag_inference_view_model import ResponseRagInferenceViewModel

class BaseLlmService(BaseServiceFWDI, metaclass=ABCMeta):

    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def request_to_llm(self,
                project: str,
                question: str,
                context_question: list,
                max_new_token: int,
                prompt: str) -> tuple | None:
        pass

    @abstractmethod  
    def IsBusy():
        pass

    @abstractmethod 
    def request_v2(self,
                    project: str,
                    view_model: CustomPromptViewModel) -> tuple | None:
        pass
