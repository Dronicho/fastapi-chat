from nejma.ext.starlette import WebSocketEndpoint
import typing
from starlette.websockets import WebSocket
from app import app
from app.db import database, messages, rooms, users
from app.crud import async_create, update_user_rooms, get_user


@app.websocket_route('/ws')
class Chat(WebSocketEndpoint):
    encoding = 'json'
    first_send = True
    messages = []

    async def on_receive(self, websocket: WebSocket, data: typing.Any):

        if self.first_send:
            print('Hello')
            q = messages.select().where(messages.c.room_name == data['room_name'])
            res = await database.fetch_all(q)
            for row in res:
                print('Sended:', row)
                self.messages.append(row)
                payload = {
                    'username': row['username'],
                    'message': row['text'],
                    'room_name': row['room_name']
                }
                await self.channel.send(payload)
            self.first_send = False
        else:

            room_name = data['room_name']
            message = data['message']
            username = data.pop('username')

            record = {
                'text': message,
                'username': username,
                'room_name': room_name
            }

            user = await get_user(database, users, username)
            if user:
                _ = await update_user_rooms(database, users, [int(room_name)], user.id)

            lrid = await async_create(database, messages, **record)
            print('message saved with id:', lrid)

            if message.strip():
                group = f'group_{room_name}'

                self.channel_layer.add(group, self.channel)

                payload = {
                    'username': username,
                    'message': message,
                    'room_name': room_name
                }

                await self.channel_layer.group_send(group, payload)
