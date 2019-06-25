import sqlalchemy
from app import app

from app.db import messages, users, rooms
from app.authenticate import get_current_active_user


def create(executor, db: sqlalchemy.Table, **kwargs):
    q = db.insert().values(**kwargs)
    last_record_id = executor.execute(q)
    return last_record_id


async def async_create(ex, db, **kwargs):
    q = db.insert().values(**kwargs)
    lrid = await ex.execute(q)
    return lrid


async def update_user_rooms(ex, db: sqlalchemy.Table, rooms, username):
    q = db.select().where(users.c.username == username)
    user = await ex.fetch_one(q)
    print(user)
    new_rooms = list(set(user.group_list + rooms))
    update_q = db.update().where(users.c.username == username).values(group_list=new_rooms)
    return await ex.execute(update_q)


async def get_user(ex, db, username):
    q = db.select().where(users.c.username == username)
    return await ex.fetch_one(q)


async def create_room(ex, db, room_name):
    q = db.select().where(rooms.c.name == room_name)
    res = await ex.fetch_one(q)
    if res == None:
        q = db.insert().values(name=room_name, messages=[])
        print(f'room with name {room_name} created')
        return await ex.execute(q)
    print(f'Room with name {room_name} already exists')


async def add_message_to_room(ex, db: sqlalchemy.Table, room_name, ms_id):
    q = db.select().where(rooms.c.name == room_name)
    res = await ex.fetch_one(q)
    if res:
        new_messages = res.messages + [ms_id]
        q = db.update().where(rooms.c.name == room_name).values(messages=new_messages)
        return await ex.execute(q)

