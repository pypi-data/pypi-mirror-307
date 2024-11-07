from abc import ABCMeta, abstractmethod
from fwdi.Application.Abstractions.base_service import BaseServiceFWDI

from Application.DTO.ContextReqestToLLMModel.context_request_to_llm import DataForLlmModel
from Application.DTO.ContextReqestToLLMModel.context_update_to_llm import UpdateRequestToLLM
from Application.DTO.Response.rag_responce_project import AnswerFromLLM


class BaseTaskManager(BaseServiceFWDI, metaclass=ABCMeta):

    @abstractmethod
    def add(task: DataForLlmModel) -> int:
        pass

    @abstractmethod
    def add_task_for_update(task: UpdateRequestToLLM):
        pass

    @abstractmethod
    def get() -> list[AnswerFromLLM]:
        pass

    @abstractmethod    
    def get_update() -> list:
        pass