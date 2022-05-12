
from json import JSONEncoder
#from fastapi_pagination import paginate
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
# python model.py db init                              #
# python model.py db migrate                           #
# export PYTHONPATH=.                                  #
# alembic upgrade head                                 #
# alembic revision --autogenerate -m "first migration" #
# alembic upgrade head                                 #
########################################################


##############################
# ENUM USER AND TYPE OFF PAY #
##############################
class LikeUnlike(str, enum.Enum):
    Like = 'Like'
    Unlike = 'Unlike'


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

    @declared_attr
    def deleted(self):
        return Column(Boolean, default=False)

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
    date_of_birth = Column(DateTime, nullable=False)
    password = Column(String, nullable=False)
    role = Column(Enum(Role), default=Role.users)  # Enum polje
    session_id = Column(String(100))
    hashed_password = Column(String(150))
    block = Column(Boolean, default=False)

    #####################
    # GET USER BY EMAIL #
    #####################

    @classmethod
    def get_user_by_email(cls, email):
        return db.query(cls) \
            .filter(cls.email == email, ~cls.deleted) \
            .first()

    @classmethod
    def get_user_by_email_and_password(cls, email, password):
        return db.query(cls) \
            .filter(cls.email == email, cls.password == password, ~cls.deleted) \
            .first()

    @classmethod
    def get_by_session_id(cls, session_id):
        return db.query(cls).filter(cls.session_id == session_id, ~cls.deleted).first()

    @classmethod
    def edit_user(cls, user_id, user_data):
        return db.query(cls).filter(cls.id == user_id, ~cls.deleted) \
            .update(user_data, synchronize_session=False)

    @classmethod
    def edit_user_holiday(cls, email, user_data):
        return db.query(cls).filter(cls.email == email, ~cls.deleted) \
            .update(cls.holiday==user_data, synchronize_session=False)


class Posts(Base, BaseModels, JSONEncoder):
    __tablename__ = 'posts'

    post_content = Column(Text)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    numbers_of_likes = Column(Integer, default=0)
    numbers_of_comments = Column(Integer, default=0)

    comm_a = relationship('Comments')

    @classmethod
    def get_all_posts(cls):
        return db.query(cls).filter(~cls.deleted).all()

    @classmethod
    def get_posts_id(cls, id_1):
        return db.query(cls).filter(cls.id == id_1, ~cls.deleted).first()


    @classmethod
    def get_posts_by_id(cls, id):
        return db.query(cls) \
            .join(Comments, Comments.post_id == Posts.id) \
            .filter(cls.id == id, ~cls.deleted) \
            .options(joinedload(cls.comm_a)).all()

    @classmethod
    def edit_post(cls, post_id, user_data):
        return db.query(cls).filter(cls.id == post_id, ~cls.deleted) \
            .update(user_data, synchronize_session=False)


class Comments(Base, BaseModels, JSONEncoder):
    __tablename__ = 'comments'

    comment_content = Column(Text)
    numbers_of_likes = Column(Integer, default=0)
    post_id = Column(Integer, ForeignKey('posts.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)

    user_a = relationship('User', viewonly=True, foreign_keys="Comments.user_id")
    post_a = relationship('Posts', viewonly=True, foreign_keys="Comments.post_id")


class Like(Base, BaseModels, JSONEncoder):
    __tablename__ = 'like'

    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    post_id = Column(Integer, ForeignKey('posts.id'), nullable=False)
    # comments_id = Column(Integer, ForeignKey('comments.id'), nullable=False)

    user_a = relationship('User', viewonly=True, foreign_keys="Like.user_id")
    post_a = relationship('Posts', viewonly=True, foreign_keys="Like.post_id")

    @classmethod
    def check_like(cls, user, post_a):
        return db.query(cls) \
            .filter(cls.user_id == user, ~cls.deleted, cls.post_id == post_a) \
            .first()

    @classmethod
    def delete_like(cls, user, post_a):
        return db.query(cls) \
            .filter(cls.user_id == user, cls.post_id == post_a) \
            .delete()





