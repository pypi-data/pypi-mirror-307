from abc import abstractmethod, ABCMeta
from fwdi.Application.Abstractions.base_service import BaseServiceFWDI


class BaseTextTools(BaseServiceFWDI, metaclass=ABCMeta):
    @abstractmethod
    def clear_garbage_v1(text: str) -> str:
        pass
    
    @abstractmethod
    def clear_garbage_v2(text: str) -> str:
        pass

    @abstractmethod
    def clear_garbage_hard_v1(text: str) -> str:
        pass
    
    @abstractmethod
    def clear_numerics(text: str) -> str:
        pass

    @abstractmethod
    def clear_regex_text(text: str) -> str:
        pass

    @abstractmethod
    def clear_other_text(text: str) -> str:
        pass

    @abstractmethod
    def clear_garbage_hard_v1(text: str) -> str:
        pass
    
    @abstractmethod
    def lemmatize_fn(text: str) -> str:
        pass
    
    @abstractmethod
    def delete_stop_word(text: str) -> str:
        pass
    
    @abstractmethod
    def parse_responce_llm_question(responce)->str:
        pass

    @abstractmethod   
    def clearing_text_fn_v1(text: str) -> str:
        pass

    @abstractmethod   
    def split_fn_v1(text:str, min_len:int=2)->list[str]:
        pass

    @abstractmethod 
    def clean_and_repack_text(text:str) -> str:
        pass

    @abstractmethod 
    def delete_bad_word_v2(test_str: str) -> str:
        pass