from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional
from datetime import datetime
from enum import Enum

class UserGroup(str, Enum):
    USER = "user"
    ADMIN = "admin"

# Token schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
    user_id: Optional[int] = None
    group: Optional[UserGroup] = None

class LoginRequest(BaseModel):
    username: str
    password: str

# User schemas
class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str = Field(..., min_length=6)
    group: UserGroup = UserGroup.USER

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=6)
    group: Optional[UserGroup] = None

class UserResponse(UserBase):
    id: int
    group: UserGroup
    is_active: bool
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

# Advertisement schemas
class AdvertisementBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    price: int = Field(..., ge=0)

class AdvertisementCreate(AdvertisementBase):
    pass

class AdvertisementUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    price: Optional[int] = Field(None, ge=0)

class AdvertisementResponse(AdvertisementBase):
    id: int
    owner_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)
