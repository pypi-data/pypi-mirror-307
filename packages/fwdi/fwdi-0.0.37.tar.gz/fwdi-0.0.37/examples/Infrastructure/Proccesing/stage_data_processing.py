import os
import re
import pandas as pd
from tqdm import tqdm
from Application.Abstractions.base_stage_data_processing import BaseStageDataProcessing
from Application.Abstractions.base_text_tools import BaseTextTools
from Application.Abstractions.base_usecase_task_manager import BaseUsecaseTaskManager
from Application.DTO.ContextReqestToLLMModel.context_update_to_llm import UpdateRequestToLLM
from Application.DTO.Request.custom_prompt_view_model import CustomPromptViewModel
from Domain.Enums.enumTypeInference import TypeInference
from Utilites.ext_dict import ExtDictionary
from Application.Usecases.usecase_task_manager import UsecaseTaskManager
from threading import Event

check_answer_summarize_pref = 'Краткое содержание:'
len_check_answ_summ_preff = len(check_answer_summarize_pref)
new_db_doc_sents:str = 'Databases/picklestore/doc_sents_new_db_v1.pkl'

class StageDataProcessing(BaseStageDataProcessing):

    @staticmethod
    def preprocessing_text(lst_doc: list) -> list[dict]:
        lst_source_data_stand:list[dict] = StageDataProcessing.__get_or_create_source_db_v1(lst_doc)

        lst_final_doc_sent_summ = []
        for doc in lst_source_data_stand['sentences']:
            text = doc['llm_about_text_cleared'] + doc['llm_question_text_cleared'] + doc['text']
            dct_doc = {'doc_id': doc['doc_id'], 'name': doc['name'], 'context_for_llm': doc['text'], 'context': text, 'url': doc['url'],  'article': doc['article']}
            lst_final_doc_sent_summ.append(dct_doc)

        return lst_final_doc_sent_summ

    @staticmethod
    def prepared_sentences__universal(lst_final_doc_sent_summ:list[dict], contexts_field:list[str], text_tools: BaseTextTools) -> list[dict]:
        lst_final_text:list[dict] = []

        with tqdm(desc="Prepared text format for vector:", total=len(lst_final_doc_sent_summ)) as pb:
            for item in lst_final_doc_sent_summ: # article text text_freq_summarize llm_summarize_text llm_about_text llm_question_text llm_metrics_text
                context_text:str = ''

                for field in contexts_field:
                    context_text += text_tools.delete_bad_word_v2(item[field])

                cleared_full_text = context_text
                tmp_item = ExtDictionary.merge(item, {'final_context': cleared_full_text})
                
                splited_text = []
                for item in text_tools.split_fn_v1(cleared_full_text, 2):
                    if len(item) > 1 and len(item.split()) > 4:
                        item = StageDataProcessing.__clear_text_for_vector(item)
                        if item != '':
                            splited_text.append(item.replace('.', ' '))
                if len(splited_text) == 1:
                    splited_text = []
                    for item in cleared_full_text.split('.'):
                        if len(item) > 1 and len(item.split()) > 4:
                            item = StageDataProcessing.__clear_text_for_vector(item)
                            if item != '':
                                splited_text.append(item.replace('.', ' '))
                    #splited_text =  [item.replace('.', '') for item in cleared_full_text.split('.') if len(item) > 1 and len(item.split()) > 4]

                tmp_item = ExtDictionary.merge(tmp_item, {f'sentences': splited_text})

                lst_final_text.append(tmp_item)

                pb.update(1)

        to_export = [{
                'doc_id': item['doc_id'],
                'title': item['name'], 
                'url': item['url'],
                'fulltext': item['final_context'],
                'sentences': item['sentences']
                } 
                for item in lst_final_text]
        
        return to_export
    

    def __clear_text_for_vector(text: str) -> str:
        matches = re.finditer(r"(.одробн..)?.?(См|см.[также]?[:]?)(\W*)", text, flags=re.ASCII)
        for matchNum, match in enumerate(matches, start=1):
            text = text.replace(str(match.group()), '')
        return text
    
    
    def __get_or_create_source_db_v1(lst_docs: list[dict]) -> list[dict]:
        result:list[dict] = []
        if not os.path.exists(new_db_doc_sents):
            #logger.info('Creating vector database')
            lst_doc_text_source = StageDataProcessing.__prepared_text_v2(lst_docs)
            lst_doc_sent = lst_doc_text_source['doc_text']
            #logger.info('start creation "about" database')
            lst_doc_text_adding = StageDataProcessing.__get_llm_about_text(lst_doc_sent, 'text') # <<<-----------------------------
            #logger.info('end creation "about" database')
            #logger.info('start creation "question" database')
            lst_doc_text_adding = StageDataProcessing.__get_llm_question_text(lst_doc_text_adding, 'text') # <<<-----------------------------
            #logger.info('end creation "question" database')

            result = StageDataProcessing.__get_or_create_source_db_v2(lst_doc_text_adding)

        else:
            result = StageDataProcessing.__get_or_create_source_db_v2(None)

        return result
    

    def __prepared_text_v2(docs: list[dict], text_tools: BaseTextTools) -> dict:
        lst_doc:list[dict] = []
        lst_doc_texts:list[dict] = []

        for doc in docs:
            lst_doc.append({'id':doc['id'], 
                            'doc_file':doc['name'],
                            'url':doc['url']})
            #### tools
            text = text_tools.clearing_text_fn_v1(doc['context_for_vector'])

            lst_doc_texts.append({'doc_id': doc['id'],
                                'article': doc['total_name'],
                                'text': text,
                                'url': doc['url'],
                                'name': doc['name']})
        
        return {'lst_doc': lst_doc, 'doc_text': lst_doc_texts}
    

    def __get_llm_about_text(sentences: list, field_name: str, text_tools: BaseTextTools) -> list:
        lst_summ:list[dict] = []
        error_sum_count:int = 0

        with tqdm(desc="Create LLM about sentences:", total=len(sentences)) as pb:
            for item in sentences:
                text = StageDataProcessing.__request_about_text_v1(item[field_name])
                clear_text = text_tools.clean_and_repack_text(text)
                if text != None:
                    if check_answer_summarize_pref in text:
                        text_index = text.rfind(check_answer_summarize_pref)
                        if text_index != -1:
                            text = text[text_index + len_check_answ_summ_preff:]
                            final_dict = ExtDictionary.merge(item, {'llm_about_text': text, 'llm_about_text_cleared': clear_text})
                            lst_summ.append(final_dict)
                        else:
                            final_dict = ExtDictionary.merge(item, {'llm_about_text': text, 'llm_about_text_cleared': clear_text})
                            lst_summ.append(final_dict)
                    else:
                        final_dict = ExtDictionary.merge(item, {'llm_about_text': text, 'llm_about_text_cleared': clear_text})
                        lst_summ.append(final_dict)
                else:
                    #logger.info('Return None from LLM when forming about.')
                    error_sum_count += 1

                pb.update(1)

        #logger.info(f'Total count error text about:{error_sum_count}')        
        return lst_summ
    


    def __get_llm_question_text(sentences: list, filed_name: str, text_tools: BaseTextTools) -> list:
        lst_summ:list[dict] = []
        error_sum_count:int = 0

        with tqdm(desc="Create LLM question sentences:", total=len(sentences)) as pb:
            for item in sentences:
                text = StageDataProcessing.__request_questions_text_v1(item[filed_name])
                clear_text = text_tools.clean_and_repack_text(text)
                if text != None:
                    if check_answer_summarize_pref in text:
                        text_index = text.rfind(check_answer_summarize_pref)
                        if text_index != -1:
                            text = text[text_index + len_check_answ_summ_preff:]
                            final_dict = ExtDictionary.merge(item, {'llm_question_text': text, 'llm_question_text_cleared': clear_text[6::]})
                            lst_summ.append(final_dict)
                        else:
                            final_dict = ExtDictionary.merge(item, {'llm_question_text': text, 'llm_question_text_cleared': clear_text[6::]})
                            lst_summ.append(final_dict)
                    else:
                        final_dict = ExtDictionary.merge(item, {'llm_question_text': text, 'llm_question_text_cleared': clear_text[6::]})
                        lst_summ.append(final_dict)
                else:
                    #logger.error('Return None from LLM when forming questions.')
                    error_sum_count += 1

                pb.update(1)
        #logger.info(f'Total count error text question:{error_sum_count}')
        return lst_summ
    


    def __get_or_create_source_db_v2(lst_final_doc_sent_summ: list[dict] = None) -> dict:
        
        if not os.path.exists(new_db_doc_sents):

            if lst_final_doc_sent_summ != None:
                df = pd.DataFrame(lst_final_doc_sent_summ)
                df.to_pickle(new_db_doc_sents)
                #logger.info("Save all data sets.")
            else:
                pass
                #logger.info("Empty datases.")
        else:
            df:pd.DataFrame = pd.read_pickle(new_db_doc_sents)
            lst_final_doc_sent_summ = df.to_dict('records')
            #logger.info("Data sets is loaded.")        
        
        return {'sentences': lst_final_doc_sent_summ}
    

    def __request_about_text_v1(text: str, task_manager: BaseUsecaseTaskManager) -> str:
        default_prompt = "<|im_start|>system: Тщательно проанализируй прилагаемый документ и составь краткое содержание. Для ответа используй не более 10 предложений. Ответ должен быть напиисан на русском языке, кратким,  лаконичным и понятным.<|im_end|>"
        lst_arg:list[dict] = []
        lst_arg.append({
            'type':'system',
            "arg_prompt": "<|im_start|>Контекст: {context}<|im_end|><|im_start|>assistant", 
                "arg_name":"context",
                "arg_value": text
            })
        
        req_custom_prompt = CustomPromptViewModel(type=TypeInference.RAG, username='alitrix', max_token=1000, prompt=default_prompt, lst_arg=lst_arg, type_prompt='default')
        event: Event = Event()
        add_request_update_LLM = UpdateRequestToLLM(project='test', custom_prompt=req_custom_prompt, source=event)
        task_manager.add_task_for_update(add_request_update_LLM)
        event.wait()
        response = task_manager.get_update()
        if response != None:
            return response[0] if isinstance(response, list) else response 
        else:
            return None 
        

    def __request_questions_text_v1(text: str, task_manager: BaseUsecaseTaskManager) -> str:
        default_prompt = "<|im_start|>system: Тщательно проанализируй контекст не упуская ни каких деталей. Я хочу получить не более 30 возможных вопросов по контексту ниже. Убедись, что в вопросах отражены основные положения, ключевые аргументы. Вопросы должны быть только на русском языке. Формат ответа: 'Ответ:' сформированные вопросы.<|im_end|>" 
        lst_arg:list[dict] = []
        lst_arg.append({
            'type':'system',
            "arg_prompt": "<|im_start|>Контекст: {context}<|im_end|><|im_start|>assistant", 
                "arg_name":"context",
                "arg_value": text
            })
        
        req_custom_prompt = CustomPromptViewModel(type=TypeInference.RAG, username='alitrix', max_token=1000, prompt=default_prompt, lst_arg=lst_arg, type_prompt='default')
        event: Event = Event()
        add_request_update_LLM = UpdateRequestToLLM(project='test', custom_prompt=req_custom_prompt, source=event)
        task_manager.add_task_for_update(add_request_update_LLM)
        event.wait()
        response = task_manager.get_update()
        if response != None:
            return response[0] if isinstance(response, list) else response 
        else:
            return None 
        

    

    