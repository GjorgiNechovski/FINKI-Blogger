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


class CommentPydantic(BaseModel):
    blog_id: int
    comment_text: str
