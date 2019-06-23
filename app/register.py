from typing import List

from app import app
from app.db import database, users
from app.models import User, UserInDB
from app.authenticate import get_password_hash


@app.post('/register', response_model=User)
async def create_user(user: User):
    hash = get_password_hash(user.password)
    print('hashed password:', hash)
    q = users.insert().values(email=user.email, username=user.username, hashed_password=hash, group_list=user.rooms)
    last_record_id = await database.execute(q)
    return {**user.dict(), 'id': last_record_id}


@app.get('/register', response_model=List[UserInDB])
async def get_users():
    q = users.select()
    return await database.fetch_all(q)


