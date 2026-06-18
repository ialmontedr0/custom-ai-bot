from datetime import datetime

from pydantic import BaseModel, ConfigDict


class UserBase(BaseModel):
    telegram_id: int
    username: str | None = None
    first_name: str | None = None
    language: str = "es"
    is_active: bool = True


class UserCreate(UserBase):
    pass


class UserUpdate(BaseModel):
    username: str | None = None
    first_name: str | None = None
    language: str | None = None
    is_active: bool | None = None


class UserResponse(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: str
    created_at: datetime
    updated_at: datetime | None = None
