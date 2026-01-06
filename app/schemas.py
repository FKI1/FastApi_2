ffrom pydantic import BaseModel, Field, ConfigDict, field_validator
from typing import Optional, List
from datetime import datetime
from .models import UserGroup  # ✅ Импортируем Enum из моделей

# Token schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
    user_id: Optional[int] = None
    group: Optional[UserGroup] = None  # ✅ Используем Enum

class LoginRequest(BaseModel):
    username: str
    password: str

# User schemas
class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: str = Field(..., min_length=5, max_length=100)
    
    @field_validator('email')
    def validate_email(cls, v):
        if '@' not in v:
            raise ValueError('Invalid email format')
        return v

class UserCreate(UserBase):
    password: str = Field(..., min_length=6)
    group: UserGroup = UserGroup.USER  # ✅ Используем Enum

class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    email: Optional[str] = Field(None, min_length=5, max_length=100)
    password: Optional[str] = Field(None, min_length=6)
    group: Optional[UserGroup] = None  # ✅ Используем Enum
    
    @field_validator('email')
    def validate_email(cls, v):
        if v is not None and '@' not in v:
            raise ValueError('Invalid email format')
        return v

class UserResponse(UserBase):
    id: int
    group: UserGroup  # ✅ Используем Enum
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