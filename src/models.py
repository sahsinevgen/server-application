from sqlalchemy import Column, ForeignKey, String, Integer
from flask_restx import fields

from base import Base

class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True)
    name = Column(String(255))


    def __init__(self, name):
        self.name = name

user_serializer = {
    "user_id": fields.Integer(),
    "name": fields.String(max_length=255, required=True)
}

class Quote(Base):
    __tablename__ = 'quotes'

    quote_id = Column(Integer, primary_key=True)
    quote = Column(String(255))
    user_id = Column(Integer, ForeignKey('users'))

    def __init__(self, quote, user_id):
        self.quote = quote
        self.user_id = user_id

quote_serializer = {
    "quote_id": fields.Integer(),
    "quote": fields.String(max_length=255, required=True),
    "user_id": fields.Integer(required=True)
}

class Comment(Base):
    __tablename__ = 'comments'

    comment_id = Column(Integer, primary_key=True)
    comment = Column(String(255))
    quote_id = Column(Integer, ForeignKey('quotes'))
    user_id = Column(Integer, ForeignKey('users'))

    def __init__(self, comment, quote_id, user_id):
        self.comment = comment
        self.quote_id = quote_id
        self.user_id = user_id

comment_serializer = {
    "comment_id": fields.Integer,
    "comment": fields.String(max_length=255, required=True),
    "quote_id": fields.Integer(required=True),
    "user_id": fields.Integer(required=True)
}

def as_dict(object): 
        return {c.name: getattr(object, c.name) for c in object.__table__.columns}