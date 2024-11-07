import numpy as np
from sentence_transformers import SentenceTransformer
import torch
from Application.Abstractions.base_embedding_model import BaseEmbeddingModel
from Utilites.ext_sys import ExtSys


class EmbeddingModel(BaseEmbeddingModel):
    def __init__(self) -> None:
        self.__model_name = 'intfloat/multilingual-e5-large'
        self.__model = SentenceTransformer(self.__model_name)

        #if ExtSys.is_debug():
            #self.__model = self.__model.to(torch.device("cpu"))
        #else:
        if torch.cuda.is_available(): 
            self.__model = self.__model.to(torch.device("cuda"))

    def __enter__(self):
        return self 
    
    def __exit__(self, *args):
        del self.__model

    def encode(self, text:str) -> list:
        try:
            embeddings = self.__model.encode(text, show_progress_bar=True)
            embeddings = np.array([embedding for embedding in embeddings]).astype("float32")
            lst_embedding = embeddings.tolist()
            del embeddings

            return lst_embedding
        
        except Exception as ex:
            print(f"ERROR:{ex}")


