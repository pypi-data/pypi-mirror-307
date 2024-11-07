from pydantic import BaseModel
from Application.DTO.Request.rag_question_project import RequestToLLM


class DataForLlmModel(BaseModel):
        
        request: RequestToLLM
        context: str
        lst_link_distance: list[dict]
