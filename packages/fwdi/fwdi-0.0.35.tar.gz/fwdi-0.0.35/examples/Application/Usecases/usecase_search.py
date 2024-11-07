import time
from typing import Optional
from Application.Abstractions.base_embedding_model import BaseEmbeddingModel
from Application.Abstractions.base_manager_db import BaseManagerContextDB
from Application.Abstractions.base_service_search import BaseServiceSearch
import faiss
import numpy as np
from Application.Abstractions.base_text_tools import BaseTextTools
from Utilites.ext_dump_relevant_search_question import ExtDump
from ..DTO.ContextReqestToLLMModel.context_request_to_llm import DataForLlmModel
from Application.DTO.Request.rag_question_project import RequestToLLM





class ServiceSearch(BaseServiceSearch):
    def __init__(self) -> None:
        super().__init__()


    def relevant_search(self, 
                        question_pack: RequestToLLM, 
                        manager_db: BaseManagerContextDB, 
                        tools: BaseTextTools, 
                        embeding: BaseEmbeddingModel
                        ) -> DataForLlmModel:
        if manager_db.get_vector_store() is None or manager_db.get_pickle_store() is None:
            pass
            print('1')
            #logger.warning('Database is missing')
        start_time = time.time()
 
        cleared_question = tools.clear_garbage_hard_v1(question_pack.question)
        question_lem = tools.lemmatize_fn(cleared_question)
        question = tools.delete_stop_word(question_lem)
        embedding_question = embeding.encode(question)
        _vector = np.array([embedding_question]).astype("float32")
        faiss.normalize_L2(_vector)

        index = manager_db.get_vector_store()

        distance = 0.25
        index.nprobe = 2

        context_LLM = self.__vector_search(index, _vector, question_pack, distance, manager_db)
        if context_LLM is None:
            lst_answer = self.__search_result_lsi(question_pack, manager_db)
            lst_answer = self.__uniq_answer(lst_answer, question_pack)
            if lst_answer is None:
                #logger.info('No relevant answer to question asked.')
                return 'Ответ на Ваш запрос не содержится в моей базе данных.'
            lst_context, lst_link_distance = self.__check_quantity_words(lst_answer, question_pack, 'LSI')
            context_llm_str = self.__create_context_for_llm(lst_context)
            context_LLM = DataForLlmModel(request=question_pack, 
                                          context=context_llm_str, 
                                          lst_link_distance=lst_link_distance)
        #if res is None:
        #    logger.info('No relevant answer to question asked.')
        #    return jsonify(message='Ответ на Ваш запрос не содержится в моей базе данных.'), 200
        
        ellapsed_time  = time.time() - start_time
        print("Ellapsed: ", ellapsed_time)

        return context_LLM 


    def __vector_search(self, index: faiss.IndexIVFFlat, 
                      question_vector: np.ndarray, 
                      question_pack: RequestToLLM,  
                      distance: float, 
                      manager_db: BaseManagerContextDB) -> DataForLlmModel:

        distances, ann = index.search(question_vector, k=int(question_pack.k_top))

        lst = []

        data_frame = manager_db.get_pickle_store()

        for i, index in enumerate(ann[0]):
            if index != -1:
                lst.append({'distance': distances[0][i], 'context': data_frame.loc[data_frame.doc_id == index].values[0]})

        lst = sorted(lst, key=lambda d: d['distance'])

        lst_answer = [{'id': item['context'][0],
            'name': item['context'][1],
            'context': item['context'][2],
            'url': item['context'][4],
            'distance': item['distance']} for item in lst if float(item['distance']) < distance]
        if lst_answer == []:
            return None
        lst_answer = self.__uniq_answer(lst_answer, question_pack)
        if lst_answer == []:
            return None
        lst_context, lst_link_distance = self.__check_quantity_words(lst_answer, question_pack, 'VECTOR')
        context_for_llm_str = self.__create_context_for_llm(lst_context)

        context_LLM = DataForLlmModel(request=question_pack, context=context_for_llm_str, lst_link_distance=lst_link_distance)

        return context_LLM
    

    def __uniq_answer(self,
                    lst_answer: list[dict],
                    question_pack: RequestToLLM) -> Optional[list]:
        
        if not lst_answer:
            method = 'LSI_LDA_search'
            #logger.info('No relevant answer in vector base, using lsi/lda search.')
            if not lst_answer:
                return None
        else:
            method = 'VECTOR_search'

        uniq_answer_lst = []
        for result in lst_answer:
            for i in uniq_answer_lst:
                if i['id'] == result['id']:
                    break
            else:
                uniq_answer_lst.append(result)

        if len(uniq_answer_lst) == 1:
            return None
        
        ExtDump.formated_result(question_pack=question_pack, lst_answer=uniq_answer_lst, method=method)

        return uniq_answer_lst
    

    def __search_result_lsi(self, 
                          question_pack: RequestToLLM, 
                           manager_db: BaseManagerContextDB) -> list[dict]:
        
        result_search = manager_db.get_matrix_store().search(question_pack.question, question_pack.k_top)

        lst_answer = manager_db.get_matrix_store().get_doc_by_result(result_search)
        
        lst = []

        data_frame = manager_db.get_pickle_store()

        for id in lst_answer:
            lst.append({'distance': id['distance'], 'context': data_frame.loc[data_frame.doc_id == id['document']['id']].values[0]})

        lst = sorted(lst, key=lambda d: d['distance'], reverse=True)

        lst_answer = [{'id': item['context'][0],
                    'name': item['context'][1],
                    'context': item['context'][2],
                    'url': item['context'][4],
                    'distance': item['distance']} for item in lst if float(item['distance']) >= 0.65]

        return lst_answer
    
    def __check_quantity_words(self,
                             lst_answer: list[dict], 
                             question_pack: RequestToLLM,
                             method: str) -> list[dict]:
        
        count = 0
        max_words = 4500
        lst_context = []
        for context in lst_answer:
            max_words = max_words - len(context['context'].split())
            if max_words <= 0:
                break
            else:
                count += 1
                lst_context.append(context['context'])

        lst_link_distance = []
        for answer in lst_answer:
            if len(lst_link_distance) >= count:
                break
            else:
                lst_link_distance.append(
                    {"Name": answer["name"], "URL": answer['url'], "DISTANCE": str(answer['distance'])})
                
        if max_words >= 500 and method == 'VECTOR':
            lst_answer_lsi = self.__search_result_lsi(question_pack)
            union_answer_list = self.__unity_answer(lst_answer, lst_answer_lsi, question_pack)
                
            lst_context, lst_link_distance = self.__check_quantity_words(union_answer_list, question_pack, 'UNION')

        return lst_context, lst_link_distance
    
    def __unity_answer(self, list_answer_vector: list[dict], list_answer_lsi: list[dict], question_pack: RequestToLLM):

        union_answer_list = []
        if len(list_answer_vector) > len(list_answer_lsi): 
            for index in range(len(list_answer_lsi)):
                union_answer_list.append(list_answer_vector[index])
                union_answer_list.append(list_answer_lsi[index])

            for answer in list_answer_vector[len(list_answer_lsi)::]:
                union_answer_list.append(answer)

        elif len(list_answer_vector) < len(list_answer_lsi): 
            for index in range(len(list_answer_vector)):
                union_answer_list.append(list_answer_vector[index])
                union_answer_list.append(list_answer_lsi[index])

            for answer in list_answer_lsi[len(list_answer_vector)::]:
                union_answer_list.append(answer)

        else:
            for index, answer in enumerate(list_answer_vector):
                union_answer_list.append(answer) 
                union_answer_list.append(list_answer_lsi[index])

        union_answer_list = self.__uniq_answer(union_answer_list, question_pack)

        return union_answer_list
    

    def __create_context_for_llm(self,
                               lst_context: list[dict]) -> str:

        final_context = ""

        for count, context in enumerate(lst_context):
            if context[-1] != '.':
                final_context += f"{count + 1}.{context}.\n"
            else:
                final_context += f"{count + 1}.{context}\n"

        return final_context
