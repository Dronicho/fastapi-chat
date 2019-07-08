from pydantic import BaseModel
from typing import List


class Message(BaseModel):
    id: int = None
    text: str
    username: str
    room_name: str
    viewed: dict = None
    timestamp: str = None


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str = None


class User(BaseModel):
    username: str
    email: str
    password: str
    rooms: List[str] = None


class UserInDB(BaseModel):
    username: str
    email: str
    hashed_password: str
    group_list: List[str]


class Room(BaseModel):
    id: int = None
    name: str
    messages: List[int] = None
