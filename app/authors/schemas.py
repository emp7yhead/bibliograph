from pydantic import BaseModel


class Author(BaseModel):
    name: str

    class Config:
        orm_mode = True
