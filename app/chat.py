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
    user = None

    async def on_receive(self, websocket: WebSocket, data: typing.Any):
        print(data)
        ms_type = data['type']

        if ms_type == 'connect':
            response = {}
            used_rooms = set()
            self.user = await find_by_col_name(users, 'username', data['username'])
            for name in self.user['group_list']:
                self.channel_layer.add(f'group_{name}', self.channel)
                room = await find_by_col_name(rooms, 'name', name)
                if not(room is None) and name not in used_rooms:

                    for ms_id in room['messages']:
                        ms = await find_by_col_name(messages, 'id', ms_id)
                        message = {
                            'username': ms['username'],
                            'message': ms['text'],
                            'room_name': ms['room_name']
                        }
                        response[name] = response.get(name, list()) + [message]
                used_rooms.add(name)
            add_rooms = {name: [] for name in used_rooms - set(response.keys())}
            response.update(add_rooms)
            await self.channel.send(response)
        elif ms_type == 'change_room':
            print('changing room...')
            room_name = data['room_name']

            self.group = f'group_{room_name}'
            self.channel_layer.add(self.group, self.channel)
            await create(rooms, name=room_name, messages=[])

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
