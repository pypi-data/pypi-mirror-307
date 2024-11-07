import faiss
import numpy as np

from Application.Abstractions.base_embedding_model import BaseEmbeddingModel
from Application.Abstractions.base_text_tools import BaseTextTools
from Application.Abstractions.base_vectore_service import BaseVectoreService


class VectoreService(BaseVectoreService):
    def create_vector_db_v1(vector_db_path:str, lst_final_doc_sent_summ:list, filed_name:str) -> faiss.IndexIVFFlat:
        #logger.info('Creating vector database')
        embeddings = VectoreService.__embedding_fn(lst_final_doc_sent_summ, filed_name)

        lst_id = [item['doc_id'] for item in lst_final_doc_sent_summ]
        
        k_emb = int(len(embeddings) * 0.02)
        dim_embe = len(embeddings[0])

        quantiser = faiss.IndexFlatL2(dim_embe)
        index = faiss.IndexIVFFlat(quantiser, dim_embe, k_emb)
        index.train(embeddings)
        index.add_with_ids(np.array(embeddings).astype('float32'), lst_id)
        
        faiss.write_index(index, vector_db_path)

        return index
    

    def __embedding_fn(lst_sentences:list, filed_name:str, text_tools: BaseTextTools, embedding: BaseEmbeddingModel)->list:
        embe_text = embedding.encode([text_tools.lemmatize_fn(item[filed_name]) for item in lst_sentences])
        embe_text = np.array(embe_text).astype('float32')

        return embe_text