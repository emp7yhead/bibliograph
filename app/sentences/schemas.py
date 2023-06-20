from pydantic import BaseModel


class Sentence(BaseModel):
    content: str

    class Config:
        orm_mode = True
