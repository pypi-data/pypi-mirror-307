from shutil import move
from Application.Abstractions.base_proxy_web_parse import BaseProxyWebParse
from Application.Abstractions.base_similarity_data_store import BaseSimilarityDataStore
from Application.Abstractions.base_stage_data_processing import BaseStageDataProcessing
from Application.Abstractions.base_usecase_context_data_base import BaseUsecaseContextDataBase
from Application.Abstractions.base_vectore_service import BaseVectoreService
from Application.Abstractions.base_web_parse import BaseWebParse
from fwdi.Application.Configs.service_congif import ServiceConfig


class UsecaseContextDataBase(BaseUsecaseContextDataBase):

    def __parse_stand(self, web_parse_service: BaseProxyWebParse, data_store: BaseSimilarityDataStore) -> bool:
        try:
            web_parse_service:BaseWebParse = web_parse_service.get_parse_stand()
            lst_doc = web_parse_service.parse()
            data_store.write(lst_doc=lst_doc, 
                             path='Databases/picklestore/ParseData.pkl', 
                             columns=['id', 'name', 'context', 'context_for_vector', 'url', "total_name"])
            
            lst_doc = data_store.read('Databases/picklestore/ParseData.pkl')
            return True
        except Exception as ex:
            UsecaseContextDataBase.__log__(ex, "ERROR")
            return False
        
    def __preprocessing_text(self, stage_data: BaseStageDataProcessing, data_store: BaseSimilarityDataStore) -> list[dict]:
        lst_doc = data_store.read('Databases/picklestore/ParseData.pkl')
        lst_doc = stage_data.preprocessing_text(lst_doc[:2:])

        return lst_doc

    def __parse_bsp(self, web_parse_service_bsp: BaseProxyWebParse) -> list[dict]:
        web_parse_service_bsp: BaseWebParse = web_parse_service_bsp.get_parse_bsp()
        lst_doc = web_parse_service_bsp.parse()

        return lst_doc 
    
    def __merge_parse_data(self, lst_docs: list[list], data_store: BaseSimilarityDataStore) -> list[dict]:
        count = len(lst_docs[0])
        lst_result = lst_docs[0]
        for doc in lst_docs[1::]:
            for item in doc:
                item['doc_id'] = count
                lst_result.append(item)
                count += 1
        data_store.write(lst_doc=lst_result, 
                    path='Databases/picklestore/temp/ParseData.pkl'
                    )
        return lst_result
    
    def __prepared_sentences(self, lst_result: list[dict], list_field: list[str], stage_data: BaseStageDataProcessing, data_store: BaseSimilarityDataStore) -> list[dict]:
        lst_doc = stage_data.prepared_sentences__universal(lst_result, list_field)
        data_store.write(lst_doc, 'Databases/picklestore/temp/ExportData.pkl')

        lst_data_to_vector:list[dict] = []
        for item in lst_doc:
            tmp_item = [{'doc_id': item['doc_id'], 'context': text} for text in item[f'sentences']] # sentences
            lst_data_to_vector += tmp_item

        return lst_data_to_vector

    def __create_new_vectore_store(self, lst_result: list[dict], context_field: str, vectore_path: str, vectore_service: BaseVectoreService) -> bool:    # context_field = 'context'
        try:
            vectore_service.create_vector_db_v1(vectore_path, lst_result, context_field)
            return True
        except Exception as ex:
            UsecaseContextDataBase.__log__(ex, "ERROR")
            raise Exception(ex)

    def create_vectore_database(self, config: ServiceConfig):
        if not self.__parse_stand():
            return False
        lst_doc = self.__preprocessing_text()
        lst_doc = self.__prepared_sentences(lst_doc, ['article', 'context'])
        lst_doc_bsp = self.__parse_bsp()
        total_lst_doc = []
        total_lst_doc.append(lst_doc)
        total_lst_doc.append(lst_doc_bsp)
        lst_doc = self.__merge_parse_data(total_lst_doc)
        self.__create_new_vectore_store(lst_doc, 'context', 'Databases/vectorstore/temp/index.faiss')
        config.service_avaible = False
        move('Databases/picklestore/temp/ParseData.pkl', 'Databases/picklestore/ParseData.pkl')
        move('Databases/vectorstore/temp/index.faiss', 'Databases/vectorstore/index.faiss')
        config.service_avaible = True




    

        

