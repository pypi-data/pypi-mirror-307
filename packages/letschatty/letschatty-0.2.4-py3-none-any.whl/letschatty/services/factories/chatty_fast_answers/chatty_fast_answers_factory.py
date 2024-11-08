from __future__ import annotations
from pydantic import BaseModel, Field
from typing import List, Dict, Any
from datetime import datetime
from zoneinfo import ZoneInfo
from bson import ObjectId
from ....models.messages.chatty_messages import MessageRequest
from ....models.company.assets import ChattyFastAnswer
from ....models.messages.chatty_messages.schema import ChattyContext
from ....models.utils import MessageSubtype

class ChattyFastAnswersFactory:
    
    @staticmethod
    def from_json(json_data: Dict[str, Any]) -> ChattyFastAnswer:
        """This method is used to create a ChattyResponse from a JSON object"""
        return ChattyFastAnswer(**json_data)
    
    @staticmethod
    def create(messages: List[Dict[str, Any]]) -> ChattyFastAnswer:
        """This method is used to create a ChattyResponse from a JSON object"""
        id = str(ObjectId())
        updated_at = datetime.now(tz=ZoneInfo("UTC"))
        created_at = datetime.now(tz=ZoneInfo("UTC"))
        chatty_context = ChattyContext(response_id=id)
        subtype = MessageSubtype.CHATTY_FAST_ANSWER
        messages = [MessageRequest.from_response(data=message, context=chatty_context, subtype=subtype) for message in messages]
        return ChattyFastAnswer(id=id, updated_at=updated_at, created_at=created_at, messages=messages)
    
    @staticmethod
    def update(chatty_fast_answer: ChattyFastAnswer, messages: List[Dict[str, Any]]) -> ChattyFastAnswer:
        """This method is used to update a ChattyResponse with a new list of messages"""
        chatty_context = ChattyContext(response_id=chatty_fast_answer.id)
        subtype = MessageSubtype.CHATTY_FAST_ANSWER
        messages = [MessageRequest.from_response(data=message, context=chatty_context, subtype=subtype) for message in messages]
        chatty_fast_answer.updated_at = datetime.now(tz=ZoneInfo("UTC"))
        chatty_fast_answer.messages = messages
        return chatty_fast_answer