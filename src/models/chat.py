from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ChatBase(BaseModel):
    telegram_chat_id: int
    chat_type: str
    title: str | None = None
    personality_id: str | None = None


class ChatCreate(ChatBase):
    pass


class ChatUpdate(BaseModel):
    title: str | None = None
    personality_id: str | None = None


class ChatResponse(ChatBase):
    model_config = ConfigDict(from_attributes=True)

    id: str
    created_at: datetime
