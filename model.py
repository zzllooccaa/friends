from _datetime import date
from json import JSONEncoder
# from fastapi_pagination import paginate
from dotenv import load_dotenv

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean, Enum, extract
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, joinedload, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.declarative import declared_attr

from dataclasses import dataclass

import enum
import simplejson
import datetime

DATABASE_URL = 'postgresql://postgres:myPassword@localhost:5432/friends'


engine = create_engine(
    DATABASE_URL, json_serializer=lambda obj: simplejson.dumps(obj)
)
SessionLocal = sessionmaker(autocommit=False, bind=engine)
db = SessionLocal()
Base = declarative_base()

load_dotenv('.env')


########################################################
# export PYTHONPATH=.                                  #
# alembic upgrade head                                 #
# alembic revision --autogenerate -m "user_phone_add"  #
# alembic upgrade head                                 #
########################################################


##############################
# ENUM USER AND TYPE OFF PAY #
##############################


class Role(str, enum.Enum):
    admin = 'admin'
    users = 'users'


class BaseModels(object):
    @declared_attr
    def id(self):
        return Column(Integer, primary_key=True, autoincrement=True, unique=True)

    @declared_attr
    def date_of_creation(self):
        return Column(DateTime(), default=datetime.datetime.today())

    @classmethod
    def get_by_id(cls, id):
        return db.query(cls) \
            .filter(cls.id == id) \
            .first()

    @classmethod
    def get_id(cls, ide):
        return db.query(cls).filter(cls.id == ide).first()


class BaseUser(BaseModels):

    @declared_attr
    def name(self):
        return Column(String(255), nullable=False)

    @declared_attr
    def email(self):
        return Column(String, unique=True)

    @declared_attr
    def address(self):
        return Column(String(255))

    @declared_attr
    def phone(self):
        return Column(String(20))


@dataclass
class User(Base, BaseUser, JSONEncoder):
    __tablename__ = 'user'

    holiday = Column(String)
    password = Column(String, nullable=False)
    role = Column(Enum(Role), default=Role.users)  # Enum polje
    session_id = Column(String(100))
    jmbg = Column(String, unique=True)
    deleted = Column(Boolean, default=False)
    hashed_password = Column(String(150))


class Posts(Base, BaseModels, JSONEncoder):
    __tablename__ = 'posts'

    post_content = Column(Text)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    numbers_of_likes = Column(Integer)
    numbers_of_comments = Column(Integer)


class Comments(Base, BaseModels, JSONEncoder):
    __tablename__ = 'comments'

    comment_content = Column(Text)
    post_id = Column(Integer, ForeignKey('posts.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)

    user_a = relationship('User', viewonly=True, foreign_keys="Comments.user_id")
    post_a = relationship('Posts', viewonly=True, foreign_keys="Comments.post_id")


class Like(Base, BaseModels, JSONEncoder):
    __tablename__ = 'like'

    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    post_id = Column(Integer, ForeignKey('posts.id'), nullable=False)
    like = Column(Boolean, default=False)

    user_a = relationship('User', viewonly=True, foreign_keys="Like.user_id")
    post_a = relationship('Posts', viewonly=True, foreign_keys="Like.post_id")

########################
# GET REVIEW BY DOCTOR #
########################

# @classmethod
# def get_review_by_doctor_paginate(cls, name):
#     return db.query(cls) \
#         .join(Review, Review.doctor_id == User.id) \
#         .filter(User.name.ilike('%' + name + '%'), ~cls.deleted) \
#         .options(joinedload(cls.reviews)) \
#         .order_by(cls.date_of_creation).all()

# @classmethod
# def get_by_session_id(cls, session_id):
#     return db.query(cls).filter(cls.session_id == session_id, ~cls.deleted).first()
#
###############################
# GET USER BY EMAIL & PASSWORD #
###############################
#
# @classmethod
# def get_user_by_email_and_password(cls, email, password):
#     return db.query(cls) \
#         .filter(cls.email == email, cls.password == password, ~cls.deleted) \
#         .first()

#####################
# GET USER BY EMAIL #
#####################

# @classmethod
# def get_user_by_email(cls, email):
#     return db.query(cls) \
#         .filter(cls.email == email, ~cls.deleted) \
#         .first()

###############################
# GET USER BY hashed_password #
###############################

# @classmethod
# def get_user_recover(cls, hashed_password):
#     return db.query(cls) \
#         .filter(cls.hashed_password == hashed_password, ~cls.deleted) \
#         .first()

#################################################
# GET ALL USER SEARCHED BY EMAIL,NAME & SURNAME #
#################################################

# @classmethod
# def get_all_user_paginate(cls, email, name):
#     users = db.query(cls).filter(~cls.deleted)
#     if email:
#         users = users.filter(cls.email == email, ~User.deleted)
#     if name:
#         users = users.filter(cls.name == name, ~User.deleted)
#
#     return users.all()

#########################################
# CHECK USER BY EMAIL , JMBG & AND ROLE #
#########################################

# @classmethod
# def check_user_by_email(cls, email):
#     return db.query(cls).filter(cls.email == email, ~User.deleted).first()
#
# @classmethod
# def check_user_by_jmbg(cls, jmbg):
#     return db.query(cls).filter(cls.jmbg == jmbg, ~User.deleted).first()

##################
# UPDATE METHODS #
##################
# @classmethod
# def edit_user(cls, user_id, user_data):
#     print('USER DATA', user_data)
#     return db.query(cls).filter(cls.id == user_id, ~cls.deleted) \
#         .update(user_data, synchronize_session=False)
#
# @classmethod
# def forgot_user(cls, email, user_data):
#     db.query(cls).filter(cls.email == email, ~cls.deleted) \
#         .update(user_data, synchronize_session=False)

##################
# GET USER BY ID #
##################
# @classmethod
# def get_search_user(cls, names, by_ids, by_roles):
#     users = db.query(cls)
#     if names:
#         users = users.filter(User.name.ilike('%' + names + '%'))
#     if by_ids:
#         users = users.filter(cls.id == by_ids)
#     if by_roles:
#         users = users.filter(cls.role == by_roles)
#
#     return paginate(users.order_by(cls.date_of_creation).all())
