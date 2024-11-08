from __future__ import annotations
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
from datetime import datetime
from ....messages.chatty_messages import MessageRequest

class ChattyFastAnswer(BaseModel):
    id: str = Field(alias="_id")
    updated_at: datetime
    created_at: datetime
    deleted_at: Optional[datetime] = Field(default=None)
    messages: List[MessageRequest]
    
    model_config = ConfigDict(
        populate_by_name=True
    )