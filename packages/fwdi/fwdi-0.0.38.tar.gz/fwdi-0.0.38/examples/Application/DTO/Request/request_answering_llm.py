from pydantic import BaseModel


class RequestLLN(BaseModel):
    question: str
    project: str
    article: str
    distance: list
    max_new_token: int
    template_pompt: str
