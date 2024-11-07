from pydantic import BaseModel

class CustomPromptViewModel(BaseModel):

    type:int
    username:str
    max_token:int
    prompt:str
    lst_arg:list[dict]
    type_prompt: str
