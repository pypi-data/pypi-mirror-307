from pydantic import BaseModel


class RequestDetailDump(BaseModel):
    name: str
