from nejma.ext.starlette import WebSocketEndpoint
import typing
from starlette.websockets import WebSocket
from app import app
from app.db import messages, database
from app.crud import async_create


@app.websocket_route('/ws')
class Chat(WebSocketEndpoint):
    encoding = 'json'

    async def on_receive(self, websocket: WebSocket, data: typing.Any):
        room_id = data['room_id']
        message = data['message']
        username = data.pop('username')

        record = {
            'text': message,
            'username': username,
            'room_id': room_id
        }

        lrid = await async_create(database, messages, **record)
        print('message saved with id:', lrid)

        if message.strip():
            group = f'group_{room_id}'

            self.channel_layer.add(group, self.channel)

            payload = {
                'username': username,
                'message': message,
                'room_id': room_id
            }

            await self.channel_layer.group_send(group, payload)
