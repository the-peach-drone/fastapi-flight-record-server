from pydantic import BaseModel

class Record(BaseModel):
    serial: str
    incomming_time: str
    fileName: str

    class Config:
        orm_mode = True