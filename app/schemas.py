from pydantic import BaseModel, EmailStr, conint
from datetime import datetime
from typing import Optional

class PostBase(BaseModel):
    title : str
    content : str
    published : bool = True

class Post(PostBase):
    id : int
    created_At : datetime
    owner_id : int

    class Config:
        from_attributes  = True

class PostOut(BaseModel):
    Post : Post
    votes : int

    class Config:
        from_attributes  = True


class UpdatePost(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None

class UserCreate(BaseModel):
    email : EmailStr
    password : str

class UserOut(BaseModel):
    id : int
    email : EmailStr
    created_At : datetime

    class Config:
        orm_model = True

class UserLogin(BaseModel):
    email : EmailStr
    password : str

class Token(BaseModel):
    access_token : str
    token_type : str

class TokenData(BaseModel):
    id : int | None = None

from typing import Annotated

class Vote(BaseModel):
    post_id : int
    dir : Annotated[int, conint(le=1)]  # Validates integer between 0 and 1