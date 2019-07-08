from nejma.ext.starlette import WebSocketEndpoint
import typing
import datetime
from starlette.websockets import WebSocket
from app import app
from app.db import database, messages, rooms, users

from utils.database import create, update, delete, find_by_col_name, select_all

from collections import namedtuple

Message = namedtuple('Message', 'username message room_name')


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
                print(room)
                if not(room is None) and name not in used_rooms:

                    for ms_id in room['messages']:
                        ms = await find_by_col_name(messages, 'id', ms_id)
                        print(ms.items(), end='\n\n')
                        
                        message = {
                            'username': ms['username'],
                            'message': ms['text'],
                            'room_name': ms['room_name'],
                            'message_id': ms['id'],
                            'viewed': ms['viewed'],
                            'timestamp': ms['timestamp'].isoformat()
                        }
                        response[name] = response.get(name, list()) + [message]
                used_rooms.add(name)
            add_rooms = {name: [] for name in used_rooms - set(response.keys())}
            response.update(add_rooms)
            await self.channel.send(response)

        elif ms_type == 'create_room':
            print('changing room...')
            room_name = data['room_name']

            await create(rooms, name=room_name, messages=[])

            for name in room_name.split('_'):
                _ = await update(users, {'username': name}, 'group_list', [room_name])

        elif ms_type == 'view':
            print('update views')
            room_name = data['room_name']
            username = data['username']
            ms_id = data['message_id']
            group = f'group_{room_name}'

            message = await find_by_col_name(messages, 'id', ms_id)
            viewed = message['viewed']
            for name in room_name.split('_'):
                if name == username:
                    viewed.update({name: True})
                    print(viewed)
                    _ = await update(messages, {'id': ms_id}, 'viewed', viewed, update_type='replace')
ир
            payload = {
                'type': 'update_message_viewed',
                'message_id': ms_id,
                'viewed': viewed
            }    

            await self.channel_layer.group_send(group, payload)

        elif ms_type == 'message':
            room_name = data['room_name']
            message = data['message']
            username = data.pop('username')

            group = f'group_{room_name}'

            record = {
                'text': message,
                'username': username,
                'room_name': room_name,
                'viewed': {name: False for name in room_name.split('_')},
                'timestamp': datetime.datetime.now()
            }

            lrid = await create(messages, **record)
            if lrid:
                _ = await update(rooms, {'name': room_name}, 'messages', [lrid])

            print('message saved with id:', lrid)

            if message.strip():
                payload = {
                    'username': username,
                    'message': message,
                    'room_name': room_name
                }
                await self.channel_layer.group_send(group, payload)
