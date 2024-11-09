from datetime import datetime, timedelta
from typing import Optional, List
from bson.objectid import ObjectId
from pydantic import BaseModel, Field, field_validator, model_validator


from ...utils.types import StrObjectId
from .topic_message import MessageTopic

class Topic(BaseModel):
    name: str
    default_source_id: StrObjectId = Field(default_factory=lambda: str(ObjectId()))
    id: StrObjectId = Field(default_factory=lambda: str(ObjectId()), alias="_id")
    messages: List[MessageTopic] = Field(default_factory=list)
    lock_duration: timedelta = Field(default=timedelta(seconds=10))
    deleted_at: Optional[datetime] = None
    
    def model_dump(self, *args, **kwargs) -> dict:
        kwargs["by_alias"] = True
        return super().model_dump(*args, **kwargs)

    @model_validator(mode='after')
    def validate_messages_and_duration(self) -> 'Topic':
        """Validate messages have a default and lock_duration is correct"""
        if self.messages and not any(m.is_default for m in self.messages):
            self.messages[0].is_default = True

        return self
        
    @field_validator('lock_duration', mode='before')
    def validate_lock_duration(cls, v: int | timedelta) -> timedelta:
        if isinstance(v, int):
            return timedelta(seconds=v)
        elif isinstance(v, timedelta):
            return v
        else:
            raise ValueError("lock_duration must be a timedelta or an int")
        
    