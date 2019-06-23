import sqlalchemy
from app import app

from app.db import messages, users
from app.authenticate import get_current_active_user


def create(executor, db: sqlalchemy.Table, **kwargs):
    q = db.insert().values(**kwargs)
    last_record_id = executor.execute(q)
    return last_record_id


async def async_create(ex, db, **kwargs):
    q = db.insert().values(**kwargs)
    lrid = await ex.execute(q)
    return lrid


async def update_user_rooms(ex, db: sqlalchemy.Table, rooms, user_id):
    q = db.select().where(users.c.id == user_id)
    user = await ex.fetch_one(q)
    new_rooms = list(set(user.group_list + rooms))
    update_q = db.update().where(users.c.id == user_id).values(group_list=new_rooms)
    return await ex.execute(update_q)


async def get_user(ex, db, username):
    q = db.select().where(users.c.username == username)
    return await ex.fetch_one(q)
