from pydantic import BaseModel


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
    author_id: int


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str = None


class User(BaseModel):
    username: str
    email: str
    password: str


class UserInDB(BaseModel):
    username: str
    email: str
    hashed_password: str
