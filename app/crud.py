import sqlalchemy
from app import app

from app.db import messages, users


def create(executor, db: sqlalchemy.Table, **kwargs):
    q = db.insert().values(**kwargs)
    last_record_id = executor.execute(q)
    return last_record_id


async def async_create(ex, db, **kwargs):
    q = db.insert().values(**kwargs)
    lrid = await ex.execute(q)
    return lrid
