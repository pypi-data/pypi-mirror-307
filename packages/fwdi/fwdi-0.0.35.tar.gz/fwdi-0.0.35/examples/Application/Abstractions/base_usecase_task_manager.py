from abc import ABCMeta, abstractmethod
import queue
from fwdi.Application.Abstractions.base_service import BaseServiceFWDI

from Application.Abstractions.base_task_manager import BaseTaskManager
from Application.DTO.ContextReqestToLLMModel.context_update_to_llm import UpdateRequestToLLM

answer = queue.Queue()

class BaseUsecaseTaskManager(BaseServiceFWDI, metaclass=ABCMeta):

    @abstractmethod
    def add_task(self) -> str:
        pass
    
    @abstractmethod
    def get_answer(self):
        pass

    @abstractmethod
    def add_task_for_update(self, context_LLM: UpdateRequestToLLM, task_manager: BaseTaskManager):
        pass

    @abstractmethod
    def get_update(self, task_manager: BaseTaskManager) -> list:
        pass