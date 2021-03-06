from typing import List

from fastapi import Depends

from app import app, html
from starlette.websockets import WebSocket
from starlette.responses import HTMLResponse
from app.db import database, messages, users, rooms, conn
from app.authenticate import get_current_active_user
from app.models import Token, TokenData, UserInDB, User, Message, Room
from authy.api import AuthyApiClient


@app.get("/")
async def get():
    return HTMLResponse(html)


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    conn.close()
    await database.disconnect()


@app.get('/message/', response_model=List[Message])
async def read_messages():
    query = messages.select()
    return await database.fetch_all(query)


@app.post('/message/', response_model=Message)
async def create_message(message: Message):
    room_q = rooms.select().where(rooms.c.name == message.room_name)
    r = await database.fetch_one(room_q)
    if r == None:
        room_q = rooms.insert().values(name=message.room_name, messages=[])
        r = await database.execute(room_q)
    query = messages.insert().values(text=message.text, username=message.username, room_name=message.room_name)
    last_record_id = await database.execute(query)
    return {**message.dict(), 'id': last_record_id}


@app.get('/test', response_model=UserInDB, response_model_exclude=['hashed_password'])
async def test_auth(token: User = Depends(get_current_active_user)):
    return token


@app.get('/search/{username}', response_model=UserInDB, response_model_exclude=['hashed_password'])
async def get_user_by_username(username: str):
    q = users.select().where(users.c.username == username)
    return await database.fetch_one(q)


@app.get('/rooms', response_model=List[Room])
async def get_rooms():
    q = rooms.select()
    return await database.fetch_all(q)


@app.post('/rooms', response_model=Room)
async def create_room(room: Room):
    q = rooms.insert().values(name=room.name, messages=[])
    lrid = await database.execute(q)
    return {**room.dict(), 'id': lrid}


@app.delete('/rooms/{room_name}')
async def delete_room(room_name: str):
    q = rooms.delete().where(rooms.c.name == room_name)
    return await database.execute(q)


@app.delete('/message/{ms_id}')
async def delete_message(ms_id: int):
    q = messages.delete().where(messages.c.id == ms_id)
    return await database.execute(q)


@app.post('/verify_phone')
async def start_verification(
        *,
        coutry_code: str,
        phone_number: str,
        method: str = 'sms'
):
    pass