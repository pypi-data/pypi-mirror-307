from pydantic import BaseModel


class AnswerFromLLM(BaseModel):
        answer: str
        id_discussion: str
        lst_link_distance: list[dict]
        ellapsed: float
        refined_question: bool
