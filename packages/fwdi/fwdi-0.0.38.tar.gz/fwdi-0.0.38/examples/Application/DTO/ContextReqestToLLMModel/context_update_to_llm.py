from threading import Event
from pydantic import BaseModel, ConfigDict
from Application.DTO.Request.custom_prompt_view_model import CustomPromptViewModel

class Model(BaseModel):

    model_config = ConfigDict(arbitrary_types_allowed=True)


class UpdateRequestToLLM(Model):

    custom_prompt: CustomPromptViewModel
    source: Event
