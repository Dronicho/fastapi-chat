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
    room_name: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str = None


class User(BaseModel):
    username: str
    email: str
    password: str
    rooms: List[str]


class UserInDB(BaseModel):
    username: str
    email: str
    hashed_password: str
    group_list: List[str]
