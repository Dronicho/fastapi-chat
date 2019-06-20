from typing import List
from app import app, html
from starlette.websockets import WebSocket
from starlette.responses import HTMLResponse
from app.db import Note, NoteIn, database, messages, Message, notes, User, users


@app.get("/")
async def get():
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


@app.get('/users/', response_model=List[User])
async def read_users():
    query = users.select()
    return await database.fetch_all(query)


@app.post("/users/", response_model=User)
async def create_note(user: User):
    query = users.insert().values(username=user.username)
    last_record_id = await database.execute(query)
    return {**user.dict(), "id": last_record_id}
