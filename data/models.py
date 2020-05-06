import datetime

from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy_serializer import SerializerMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import orm

from .db_session import Base_orm


class User(Base_orm, UserMixin, SerializerMixin):
    __tablename__ = 'users'

    id = Column(Integer,
                primary_key=True,
                autoincrement=True)
    login = Column(String,
                   nullable=False,
                   unique=True)
    hashed_password = Column(String,
                             nullable=False)

    def __init__(self, login, password):
        self.login = login
        self.hashed_password = generate_password_hash(password)

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)


class Pet(Base_orm, SerializerMixin):
    __tablename__ = 'pets'

    id = Column(Integer,
                primary_key=True,
                autoincrement=True)

    pet_name = Column(String,
                      nullable=False)

    type = Column(String,
                  nullable=False)

    age = Column(Integer,
                 nullable=False)

    poroda = Column(String,
                    nullable=False)

    user_id = Column(Integer,
                     ForeignKey("users.id"))
    user = orm.relation('User', backref='pets')

    def __init__(self, pet_name, type, age, poroda):
        self.pet_name = pet_name
        self.type = type
        self.age = age
        self.poroda = poroda


class Feedback(Base_orm, SerializerMixin):
    __tablename__ = 'feedbacks'

    id = Column(Integer,
                primary_key=True,
                autoincrement=True)
    title = Column(String,
                   nullable=True)
    content = Column(String,
                     nullable=True)
    created_date = Column(DateTime,
                          default=datetime.datetime.now)

    user_id = Column(Integer,
                     ForeignKey("users.id"))
    user = orm.relation('User', backref='feedbacks')

    def __init__(self, title, content, created_date, user_id):
        self.pet_name = title
        self.type = content
        self.user_id = user_id
        self.created_date = created_date

