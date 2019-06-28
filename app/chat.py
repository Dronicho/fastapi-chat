from nejma.ext.starlette import WebSocketEndpoint
import typing
from starlette.websockets import WebSocket
from app import app
from app.db import database, messages, rooms, users

from utils.database import create, update, delete, find_by_col_name, select_all

@app.websocket_route('/ws')
class Chat(WebSocketEndpoint):
    encoding = 'json'
    group = ''

    async def on_receive(self, websocket: WebSocket, data: typing.Any):

        ms_type = data['type']

        if ms_type == 'change_room':
            print('changing room...')
            room_name = data['room_name']

            if self.group:
                self.channel_layer.remove(self.group, self.channel)

            self.group = f'group_{room_name}'
            self.channel_layer.add(self.group, self.channel)
            await create(rooms, name=room_name)

            for name in room_name.split('_'):
                _ = await update(users, {'username': name}, 'group_list', [room_name])

            message_list = []
            messages_from_room = await select_all(messages, 'room_name', data['room_name'])
            for row in messages_from_room:
                print('Sent:', row)
                payload = {
                    'username': row['username'],
                    'message': row['text'],
                    'room_name': row['room_name']
                }
                message_list.append(payload)
            await self.channel.send(message_list)
        elif ms_type == 'message':
            room_name = data['room_name']
            message = data['message']
            username = data.pop('username')

            group = f'group_{room_name}'

            record = {
                'text': message,
                'username': username,
                'room_name': room_name
            }

            lrid = await create(messages, **record)
            _ = await update(rooms, {'name': room_name}, 'messages', [lrid])

            print('message saved with id:', lrid)

            if message.strip():
                payload = {
                    'username': username,
                    'message': message,
                    'room_name': room_name
                }

                await self.channel_layer.group_send(group, payload)
