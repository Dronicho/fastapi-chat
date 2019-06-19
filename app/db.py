
import databases
import sqlalchemy
from pydantic import BaseModel

from app.config import DATABASE_URL


database = databases.Database(DATABASE_URL)

metadata = sqlalchemy.MetaData()

notes = sqlalchemy.Table(
    'notes',
    metadata,
    sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("text", sqlalchemy.String),
    sqlalchemy.Column("completed", sqlalchemy.Boolean),
)

if 'postgres' in DATABASE_URL:
    engine = sqlalchemy.create_engine(
        DATABASE_URL
    )
else:
    engine = sqlalchemy.create_engine(
        DATABASE_URL, connect_args={"check_same_thread": False}
    )

metadata.create_all(engine)


class NoteIn(BaseModel):
    id: int
    text: str
    completed: bool


class Note(BaseModel):
    id: int
    text: str
    completed: bool
