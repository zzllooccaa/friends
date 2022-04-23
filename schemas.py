import enum
from typing import Optional, Generic, TypeVar, Text
from pydantic import BaseModel, Field
from pydantic.generics import GenericModel
from enum import Enum
from _datetime import datetime
import model
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, fields
from pydantic import EmailStr, BaseModel
from typing import List
from datetime import date

###############
# BODY SCHEMA #
###############
T = TypeVar('T')


class BaseModelsSchema(BaseModel):
    id: Optional[int]
    date_of_creation: Optional[datetime]


class UserId(BaseModel):
    id: int


class UserLogin(BaseModel):
    email: str
    password: str


class RegisterUser(BaseModel):
    email: str
    password: str
    name: str
    address: str
    phone: str
    date_of_birth: date


class ChangePassword(BaseModel):
    password: str
    retype_password: str


class UserUpdate(BaseModel):
    email: Optional[str] = None
    password: Optional[str] = None
    name: Optional[str] = None
    role: Optional[str] = None
    phone: Optional[str]
    address: Optional[str]


###############
# POST SCHEMA #
###############

class CreatePost(BaseModel):
    post_content: str

#######################
# COMMENT POST SCHEMA #
#######################

class Comments(BaseModel):
    comment_content: str




###################
# AUTH SCHEMA #
###################
class SessionData(UserId):
    username: str
    role: Enum


###################
# RESPONSE SCHEMA #
###################
# class CommentsResponseSchema(SQLAlchemyAutoSchema):
#     class Meta:
#         model = model.Comments
#
# class AllCommentsResponseSchema(SQLAlchemyAutoSchema):
#     class Meta:
#         model = model.Posts
#
#         comm_a = fields.Nested(CommentsResponseSchema, many=True)

