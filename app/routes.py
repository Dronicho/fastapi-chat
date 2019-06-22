from typing import List

from fastapi import Depends

from app import app, html, conn
from starlette.websockets import WebSocket
from starlette.responses import HTMLResponse
from app.db import database, messages, notes, users
from app.authenticate import get_current_active_user
from app.models import Token, TokenData, UserInDB, User, Note, NoteIn, Message


@app.get("/")
async def get():
    query = messages.select()
    async for row in database.iterate(query):
        ms_id, ms_text, author_id = row
        user_q = users.select().where(users.c.id == author_id)
        res = await database.fetch_one(user_q)
        if res == None:
            user_name = 'Stanger'
        else:
            user_name = res[1]
        print('text:', ms_text, 'author:', user_name)
    return HTMLResponse(html)


# @app.websocket("/ws")
# async def websocket_endpoint(websocket: WebSocket):
#     await websocket.accept()
#     while True:
#         data = await websocket.receive_text()
#         await websocket.send_text(f"Message text was: {data}")


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    conn.close()
    await database.disconnect()


@app.get("/notes/", response_model=List[Note])
async def read_notes():
    query = notes.select()
    return await database.fetch_all(query)


@app.post("/notes/", response_model=Note)
async def create_note(note: NoteIn):
    query = notes.insert().values(text=note.text, completed=note.completed)
    last_record_id = await database.execute(query)
    return {**note.dict(), "id": last_record_id}


@app.get('/message/', response_model=List[Message])
async def read_messages():
    query = messages.select()
    return await database.fetch_all(query)


@app.post('/message/', response_model=Message)
async def create_message(message: Message):
    query = messages.insert().values(text=message.text, author_id=message.author_id)
    last_record_id = await database.execute(query)
    return {**message.dict(), 'id': last_record_id}


@app.get('/test', response_model=UserInDB)
async def test_auth(token: User = Depends(get_current_active_user)):
    return token
