from fastapi import FastAPI
from app.db import database, Note, NoteIn, notes

from starlette.middleware.cors import CORSMiddleware
app = FastAPI()
origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http:localhost",
    "http:localhost:8080",
    "http://localhost:8080",
    "https://localhost:8080",
    "htpps://pegass.herokuapp.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


html = """
<!DOCTYPE html>
<html>
    <head>
        <title>ws</title>
    </head>
    <body>
        <h1>Nejma ⭐ Chat</h1>
        <form action="" onsubmit="sendMessage(event)">
            <label>username : </label><input type="text" id="username" autocomplete="off"/><br/>
            <label>room id : </label><input type="text" id="roomId" autocomplete="off"/><br/>
            <label>message : </label><input type="text" id="messageText" autocomplete="off"/><br/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var ws = new WebSocket("ws://localhost:8000/ws");
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages');
                var message = document.createElement('li');
                var data = JSON.parse(event.data);
                message.innerHTML = `<strong>${data.username} :</strong> ${data.message}`;
                messages.appendChild(message);
            };
            function sendMessage(event) {
                var username = document.getElementById("username");
                var room = document.getElementById("roomId");
                var input = document.getElementById("messageText");
                var data = {
                    "room_id": room.value, 
                    "username": username.value,
                    "message": input.value,
                };
                ws.send(JSON.stringify(data));
                input.value = '';
                event.preventDefault();
            }
        </script>
    </body>
</html>
"""
from app import routes, db, config, chat