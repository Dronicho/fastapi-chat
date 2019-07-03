from typing import List
import databases
import sqlalchemy
from app.config import DATABASE_URL
from sqlalchemy import Table, Column, Integer, ForeignKey, String, PickleType
from sqlalchemy.ext.declarative import declarative_base

database = databases.Database(DATABASE_URL)
Base = declarative_base()
metadata = sqlalchemy.MetaData()

rooms = sqlalchemy.Table(
    'rooms',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String, unique=True),
    Column('messages', PickleType, default=list())
)

users = sqlalchemy.Table(
    'users',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('username', String, unique=True),
    Column('email', String),
    Column('hashed_password', String),
    Column('group_list', PickleType)
)

messages = sqlalchemy.Table(
    'messages',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('text', String),
    Column('username', String, ForeignKey('users.username'), back_populates='users'),
    Column('room_name', String, ForeignKey('rooms.name'), back_populates='rooms')
)





# class User(Base):
#     __tablename__ = 'users'
#     id = Column(Integer, primary_key=True)
#     username = Column(String)
#     display_name = Column(String)
#     messages = relationship('Message', back_populates="user")
#
#     def __repr__(self):
#         return f'<User(id={self.id}, username={self.username}, display_name={self.display_name})>'


# class Message(Base):
#     __tablename__ = 'messages'
#     id = Column(Integer, primary_key=True)
#     text = Column(String)
#     author_id = Column(Integer, ForeignKey('user.id'), back_populates="user")
#
#     def __repr__(self):
#         return f'<Message(id={self.id}, text={self.text[:20]}, author_id={self.author_id})>'


if 'postgres' in DATABASE_URL:
    engine = sqlalchemy.create_engine(
        DATABASE_URL
    )
else:
    engine = sqlalchemy.create_engine(
        DATABASE_URL, connect_args={"check_same_thread": False}
    )
conn = engine.connect()

metadata.create_all(engine)
