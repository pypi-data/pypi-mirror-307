from pydantic import BaseModel


class RequestUploadDump(BaseModel):
    quantity: int
