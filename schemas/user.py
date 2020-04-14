"User Schema"

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class UserBase(BaseModel):
    user_id: Optional[str] = None
    username: Optional[str] = Field(
        None,
        title="The user's Username",
        description="Must be a string",
        example="dasaf",
    )
    roles: Optional[str] = Field(None, example="admin")
    is_active: Optional[bool] = None
    created_datetime: Optional[datetime] = None


class UserBaseInDB(UserBase):
    user_id: str

    class Config:
        orm_mode = True


class UserInDb(UserBaseInDB):
    """
    Unique config for password so that we don't deserialize the hashed password
    when using the "User" class
    """

    password: str


class User(UserBaseInDB):
    pass


class UserWithPassword(UserInDb):
    pass


# Properties to receive via API on creation
class UserCreate(UserBase):
    username: str = Field(..., example="dasaf")
    password: str = Field(..., example="password")


# Properties to receive via API on update
class UserUpdate(UserBaseInDB):
    password: Optional[str] = None
