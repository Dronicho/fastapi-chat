from fastapi import FastAPI

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
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

        <!-- Bootstrap CSS -->
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css">
    </head>
    <body>
        <div class="container">
            <div class="row justify-content-md-center">
                <div class="column">
                <form action="" onsubmit="sendMessage(event)">
                    <div class="row mt-3">
                    <input type="text" class="form-control" placeholder="Username" id="username" autocomplete="off"/>
                    </div>
                    <div class="row mt-3">
                    <input type="text" class="form-control" placeholder="Room Id" id="roomId" autocomplete="off"/>
                    </div>
                    <div class="row mt-3">
                    <input type="text" class="form-control" placeholder="Message" id="messageText" autocomplete="off"/>
                    </div>
                    <div class="row mt-3 justify-content-md-center">
                    <button class="btn btn-primary">Send</button>
                    </div>
                </form>
                </div>
            
            </div>
            <div class="row mt-6">
            <ul id="messages">
            </ul>
            </dib>
        </div>
            
        
        <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>
        <script>
            var href = window.location.href
            href = href.replace('https', 'wss')
            href = href.replace('http', 'ws')
            href = href.replace('?', '')
            var ws = new WebSocket(href + 'ws');
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages');
                var message = document.createElement('li');
                var data = JSON.parse(event.data);
                message.innerHTML = `<h6 class="font-weight-bold text-primary">${data.username}</h6> <h5 class="">${data.message}</h5>`;
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
from app import db
conn = db.engine.connect()
from app import routes, config, chat, authenticate, models, register

