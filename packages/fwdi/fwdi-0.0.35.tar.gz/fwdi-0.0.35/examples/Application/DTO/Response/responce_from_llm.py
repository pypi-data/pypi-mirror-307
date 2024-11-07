from Application.DTO.Abstractions.serializable_model import BaseSerializeble


class ResponceAnswerFromLLM(BaseSerializeble):

    def __init__(self, responce: list) -> None:
        super().__init__()
        if responce is not None:
            if len(responce) > 0:
                self.responce = [item.to_json() for item in responce]
            else:
                self.responce = []
        else:
            self.responce = []

