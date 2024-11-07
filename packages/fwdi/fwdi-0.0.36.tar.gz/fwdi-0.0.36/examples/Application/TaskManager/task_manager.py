import threading
import queue
from Application.Abstractions.base_llm_service import BaseLlmService
from Application.Abstractions.base_task_manager import BaseTaskManager
from Application.Abstractions.base_text_tools import BaseTextTools
from Application.DTO.ContextReqestToLLMModel.context_request_to_llm import DataForLlmModel
from Application.DTO.ContextReqestToLLMModel.context_update_to_llm import UpdateRequestToLLM
from Application.DTO.Response.rag_responce_project import AnswerFromLLM
from Application.DTO.Response.response_rag_inference_view_model import ResponseRagInferenceViewModel
from Infrastructure.rag_llm_service import LLMService
from Utilites.tools import PostProccessingText


class TaskManager(BaseTaskManager):

    def __init__(self, tools: BaseTextTools, post_procceing_text: PostProccessingText, llm_service: BaseLlmService) -> None:
        super().__init__()

        self.lst_requests = queue.Queue()
        self.lst_answer = queue.Queue()
        self.lst_update_db = queue.Queue()
        self.lst_update_db_answer = queue.Queue()
        self.lst_id_discussion = []
        self.main_thread: threading.Thread = None
        self.tools: BaseTextTools = tools
        self.post_procceing_text: PostProccessingText = post_procceing_text
        self.llm_service: BaseLlmService = llm_service

    def add(self, task: DataForLlmModel) -> int:
        if task.request.id_discussion not in self.lst_id_discussion:
            self.lst_id_discussion.append(task.request.id_discussion)
            self.lst_requests.put(task)
            if self.main_thread is None:
                self.main_thread = threading.Thread(target=self.__execute, daemon=True)
                self.main_thread.start()

            return self.lst_requests.qsize()
        else:
            return None
        
    def add_task_for_update(self, task: UpdateRequestToLLM) -> None:
        self.lst_update_db.put(task)
        if self.main_thread is None:
                self.main_thread = threading.Thread(target=self.__execute, daemon=True)
                self.main_thread.start()

    def __execute(self):
        while not self.lst_requests.empty() or not self.lst_update_db.empty():
            if not self.lst_requests.empty():
                task = self.lst_requests.get()
                question_pack = task.request
                if task.context != '':
                    response, code = self.llm_service.request_to_llm(project=question_pack.project,
                                                                                question=question_pack.question,
                                                                                context_question=task.context,
                                                                                max_new_token=question_pack.max_new_token,
                                                                                prompt=question_pack.prompt)

                    if response is not None and code == 200:
                        answer = response[0]['response']
                        if answer[0] == ':':
                            answer = answer[2::]
                        answer = self.post_procceing_text.delete_tags_in_answer(answer)
                        answer_from_LLM = AnswerFromLLM(answer=answer,
                                                        id_discussion=task.request.id_discussion,
                                                        lst_link_distance=task.lst_link_distance,
                                                        ellapsed=round(response[0]['ellapsed'], 2),
                                                        refined_question=True)

                        self.lst_id_discussion.remove(task.request.id_discussion)

                        self.lst_answer.put(answer_from_LLM)
                    else:
                        #logger.warning('llm is not available')
                        self.add(task)
                        answer_from_LLM = AnswerFromLLM("Я не смог сформировать вам развернутый ответ, но вы можете "
                                                        "воспользоваться ссылками ниже.",
                                                        task.request.id_discussion,
                                                        task.lst_link_distance, 
                                                        task.ellapsed_time_search,
                                                        refined_question = True)
                        
                        self.lst_id_discussion.remove(task.request.id_discussion)
                        self.lst_answer.put(answer_from_LLM)
                else:
                    prompt = "<|im_start|>system: Изучи текст и сформулируй на основе этого предложения вопрос и ничего больше. Ответ должен быть лаконичным, кратким и только на русском языке. Если текст в вопросительной форме и  не содержит ошибок, то ответом будет служить заданный текст. Формат ответа: 'Правильный вопрос:' ответ.<|im_end|><|im_start|><|im_end|><|im_start|>Текст: {context}<|im_end|><|im_start|>assistant"
                    response: ResponseRagInferenceViewModel = self.llm_service.request_to_llm("alitrix",
                                                                                "123123",
                                                                                question_pack.project,
                                                                                '',
                                                                                question_pack.question,
                                                                                question_pack.max_new_token,
                                                                                prompt)
                    
                    if response is not None:
                        question = self.tools.parse_responce_llm_question(response.response)

                        dct_question = {'new_question': question, 'old_question': question_pack.question}

                        answer_from_LLM = AnswerFromLLM(dct_question,
                                                        task.request.id_discussion,
                                                        None,
                                                        None,
                                                        True)

                        self.lst_id_discussion.remove(task.request.id_discussion)

                        self.lst_answer.put(answer_from_LLM)

                    
            elif not self.lst_update_db.empty():
                task = self.lst_update_db.get()

                response, code = self.llm_service.request_v2(task.custom_prompt)

                if response is not None and code == 200:
                        answer = response[0]['response']
                        if answer[0] == ':':
                            answer = answer[2::]
                        self.lst_update_db_answer.put(answer)
                        #answer.put(response.response)
                        task.source.set()
                else:
                    print()

        self.main_thread = None

    def get(self) -> list[AnswerFromLLM]:
        if self.lst_answer.qsize() > 0:
            lst_answer: list[AnswerFromLLM] = []
            while not self.lst_answer.empty():
                lst_answer.append(self.lst_answer.get())
            return lst_answer
        else:
            return None

    def get_update(self) -> list:
        if self.lst_update_db_answer.qsize() != 0:
            answer = []
            answer.append(self.lst_update_db_answer.get())
            return answer
        else:
            return None

