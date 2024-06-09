from datetime import datetime
from typing import List

from pydantic import BaseModel
from enum import Enum


class UserRole(str, Enum):
    ROLE_USER = "ROLE_USER"
    ROLE_ADMIN = "ROLE_ADMIN"


class User(BaseModel):
    id: int
    firstName: str
    lastName: str
    email: str
    role: UserRole


class BlogPydantic(BaseModel):
    title: str
    blog_text: str


class CommentDetails(BaseModel):
    comment_id: int
    user_id: int
    comment_text: str
    date_created: datetime


class BlogDetails(BaseModel):
    id: int
    user_id: int
    title: str
    blog_text: str
    date_created: datetime
    comments: List[CommentDetails]
