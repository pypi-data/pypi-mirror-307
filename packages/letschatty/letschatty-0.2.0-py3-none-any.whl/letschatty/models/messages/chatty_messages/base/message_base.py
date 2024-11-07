from pydantic import BaseModel, Field, field_validator, ValidationInfo
from datetime import datetime, timezone
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError
from typing import Dict, Any, Optional

from bson import ObjectId
from ....utils import MessageType, Status, MessageSubtype
from ..schema import ChattyContent, ChattyContext, ChattyReferral

class Message(BaseModel):
    created_at: datetime
    updated_at: datetime
    type: MessageType
    content: ChattyContent
    status: Status
    is_incoming_message: bool
    id: str = Field(default_factory=lambda: str(ObjectId()),description="Unique identifier for the message. In case it's a central notification or a message request (still not confirmed by external API) we'll use an object id as default. Also known as wamid form Meta")
    sent_by: Optional[str] = Field(description="Email of the agent who sent the message. If it's incoming, it'll be None")
    starred: bool = Field(default=False)
    subtype: MessageSubtype = Field(default_factory=lambda: MessageSubtype.NONE)
    referral: ChattyReferral = Field(default_factory=lambda: ChattyReferral.default())
    context: ChattyContext = Field(default_factory=lambda: ChattyContext.default())
    
    def model_dump(self, *args, **kwargs) -> Dict[str, Any]:
        """
        Dump the message to a dictionary, with the option to convert datetimes to a specific timezone.
        """
        timezone = kwargs.pop('timezone', None)
        data = super().model_dump(*args, **kwargs)
        if timezone:
            try:
                tz = ZoneInfo(timezone)
                data['created_at'] = self.created_at.astimezone(tz).isoformat()
                data['updated_at'] = self.updated_at.astimezone(tz).isoformat()
            except ZoneInfoNotFoundError:
                raise ValueError(f"Invalid timezone: {timezone}")
        return data

    class ConfigDict:
        validate_assignment = True
    
    @field_validator('sent_by', mode='before')
    def validate_sent_by(cls, v: Optional[str], info: ValidationInfo) -> Optional[str]:
        """Ensure that the sent_by field is not required for incoming messages, and that it's a valid email for outgoing messages."""
        is_incoming = info.data.get('is_incoming_message', False)
        if is_incoming:
            return None
        if not is_incoming and not v:
            raise ValueError("sent_by is required for outgoing messages")
        return v
    
    @field_validator('status', mode='before')
    def validate_status(cls, v: Optional[str], info: ValidationInfo) -> Status:
        """Status should be validated always, both instantiation and assignment"""
        if isinstance(v, str):
            return Status(v)
        return v
    
    @field_validator('subtype', mode='before')
    def validate_subtype(cls, v: Optional[str], info: ValidationInfo) -> MessageSubtype:
        """If there's no subtype, we'll use the subtype NONE."""
        if v is None or v == "":
            return MessageSubtype.NONE
        return v
    
    @field_validator('referral', mode='before')
    def validate_referral(cls, v: Optional[Dict], info: ValidationInfo) -> ChattyReferral:
        """If there's no referral, we'll use the referral default."""
        if v is None or v == {}:
            return ChattyReferral.default()
        return v
    
    @field_validator('context', mode='before')
    def validate_context(cls, v: Optional[Dict], info: ValidationInfo) -> ChattyContext:
        """If there's no context, we'll use the context default."""
        if v is None or v == {}:
            return ChattyContext.default()
        return v
    
    @field_validator('context', mode='after')
    def validate_context_based_on_subtype(cls, v: ChattyContext, info: ValidationInfo) -> ChattyContext:
        """We'll validate the context based on the subtype. 
        And if there's no context, we'll use the context default."""
        subtype = info.data.get('subtype')
        if subtype == MessageSubtype.TEMPLATE:
            if v.template_name is None:
                raise ValueError("template_name is required for template messages")
        elif subtype == MessageSubtype.CHATTY_RESPONSE:
            if v.response_id is None:
                raise ValueError("response_id is required for chatty_response messages")
        return v

    @field_validator('created_at', 'updated_at')
    def ensure_utc(cls, v):
        if isinstance(v, datetime):
            return v.replace(tzinfo=ZoneInfo("UTC")) if v.tzinfo is None else v.astimezone(ZoneInfo("UTC"))
        raise ValueError('must be a datetime')
    
    def update_status(self, new_status: Status, status_datetime: datetime):
        if new_status not in Status:
            raise ValueError(f"Invalid status: {new_status}")
        self.status = new_status
        self.updated_at = status_datetime
        
    def mark_as_read(self):
        self.status = Status.READ
        self.updated_at = datetime.now(ZoneInfo("UTC"))
    
    def mark_as_unread(self):
        self.status = Status.UNREAD
        self.updated_at = datetime.now(ZoneInfo("UTC"))
    
    def mark_as_starred(self):
        self.starred = True
        self.updated_at = datetime.now(ZoneInfo("UTC"))
    
    def mark_as_unstarred(self):
        self.starred = False
        self.updated_at = datetime.now(ZoneInfo("UTC"))
    
    def mark_as_failed(self):
        self.status = Status.FAILED
        self.updated_at = datetime.now(ZoneInfo("UTC"))
        
    def mark_as_sent(self):
        self.status = Status.SENT
        self.updated_at = datetime.now(ZoneInfo("UTC"))
        
    def mark_as_delivered(self):
        self.status = Status.DELIVERED
        self.updated_at = datetime.now(ZoneInfo("UTC"))