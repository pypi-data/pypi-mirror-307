import queue
from Application.Abstractions.base_task_manager import BaseTaskManager
from Application.Abstractions.base_usecase_task_manager import BaseUsecaseTaskManager
from Application.DTO.ContextReqestToLLMModel.context_request_to_llm import DataForLlmModel
from Application.DTO.ContextReqestToLLMModel.context_update_to_llm import UpdateRequestToLLM


class UsecaseTaskManager(BaseUsecaseTaskManager):

    def add_task(self, context_LLM: DataForLlmModel, task_manager: BaseTaskManager) -> str:
        place_queue = task_manager.add(context_LLM)
        if place_queue is None:
            #logger.info('Repeated request from one user.')
            return 'Вы выполнили запрос к системе, ожидайте, пожалуйста, ответа.'
        
        #logger.info('Add task for request to LLM.')
        
        if place_queue == 0:
            return 'Обрабатываю ваш запрос.'
        return f'Ваш запрос принят, вы {place_queue} в очереди.'
    
    def get_answer(self, task_manager: BaseTaskManager):
        answer = task_manager.get()
        if answer is not None:
            return answer
        
    def add_task_for_update(self, context_LLM: UpdateRequestToLLM, task_manager: BaseTaskManager):
        task_manager.add_task_for_update(context_LLM)

    def get_update(self, task_manager: BaseTaskManager) -> list:
        answer = task_manager.get_update()

        return answer