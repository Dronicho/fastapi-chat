from app.db import database, conn
from sqlalchemy import Table


async def find_by_col_name(db: Table, col_name, target):
    """
    Finds record by column name
    :param db: SQLAlchemy.Table
    :param col_name: search column name
    :param target:
    :return: record(dict) or None
    """
    q = db.select().where(db.c[col_name] == target)
    return await database.fetch_one(q)


async def select_all(db: Table, col_name, target):
    """

    :param db:
    :param selector:
    :return:
    """
    q = db.select().where(db.c[col_name] == target)
    return await database.fetch_all(q)


async def create(db: Table, **kwargs):
    """
    Creates new record in given database
    :param db: SQLAlchemy Table object
    :param kwargs: arguments for new record
    :return: last record id or None
    """
    try:
        q = db.insert().values(**kwargs)
        return await database.execute(q)
    except:
        val = ''
        for item in kwargs.items():
            val += f'{item[0]}={item[1]}'
        print(f'record {db.name}({val}) already exists')


async def update(db: Table, selector: dict, col_name: str, value, update_type='extend'):
    """
    Updates value in given table
    :param db: SQLAlchemy database object
    :param selector: dict: {'col_name': 'value'}
    :param col_name: replace column
    :param value: new value
    :param update_type: 'extend' for append new value, 'replace' for replace value
    :return: None
    """
    ob = await find_by_col_name(db, *list(selector.items())[0])
    if ob:
        if update_type == 'extend':
            new_value = ob[col_name] + value
            new_value = list(set(new_value))
        elif update_type == 'replace':
            new_value = value
        else:
            new_value = value

        c, t = list(selector.items())[0]
        q = db.update().where(db.c[c] == t).values(**{col_name: new_value})
        return await database.execute(q)


async def delete(db: Table, col_name, target):
    """
    delete record from table
    :param db: SQLAlchemy Table object
    :param col_name: search column name
    :param target:
    :return: None
    """
    q = db.delete().where(db.c[col_name] == target)
    return await database.execute(q)


async def drop_database(db: Table):
    """
    Drops given Table
    :param db: SQLAlchemy Table object
    :return: None
    """
    return await db.drop(database)

