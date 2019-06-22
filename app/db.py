from typing import List
import databases
import sqlalchemy
from pydantic import BaseModel
from starlette.authentication import SimpleUser
from app.config import DATABASE_URL
from sqlalchemy import Table, Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

database = databases.Database(DATABASE_URL)
Base = declarative_base()
metadata = sqlalchemy.MetaData()

notes = sqlalchemy.Table(
    'notes',
    metadata,
    sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("text", sqlalchemy.String),
    sqlalchemy.Column("completed", sqlalchemy.Boolean),
)

messages = sqlalchemy.Table(
    'messages',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('text', String),
    Column('author_id', Integer, ForeignKey('users.id'), back_populates='users')
)

users = sqlalchemy.Table(
    'users',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('username', String),
    Column('email', String),
    Column('hashed_password', String),
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

metadata.create_all(engine)



