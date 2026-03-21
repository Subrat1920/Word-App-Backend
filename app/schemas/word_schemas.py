from pydantic import BaseModel


class WordRequest(BaseModel):
    word: str
    user_id: int


class WordResponse(BaseModel):
    word: str
    meaning: str
    definition: str
    example: str

