from pydantic import BaseModel

class ResponseRagInferenceViewModel(BaseModel):
        response:str
        ellapsed:float