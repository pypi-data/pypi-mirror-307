from pydantic import BaseModel


class RequestToLLM(BaseModel):
    question: str
    project: str
    k_top: int
    max_new_token: int
    prompt: str
    id_discussion: str
    refined_question: bool

