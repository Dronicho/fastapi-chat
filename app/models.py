from pydantic import BaseModel
from typing import List

class NoteIn(BaseModel):
    id: int
    text: str
    completed: bool


class Note(BaseModel):
    id: int
    text: str
    completed: bool


class Message(BaseModel):
    id: int
    text: str
    username: str
    room_id: int


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str = None


class User(BaseModel):
    username: str
    email: str
    password: str
    rooms: List[int]


class UserInDB(BaseModel):
    username: str
    email: str
    hashed_password: str
    group_list: List[int]
