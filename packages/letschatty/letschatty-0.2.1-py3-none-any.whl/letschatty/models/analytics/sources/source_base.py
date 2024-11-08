from typing import List, Optional, Dict
from datetime import datetime
from zoneinfo import ZoneInfo
from bson import ObjectId
from pydantic import BaseModel, Field, model_validator, field_validator, ValidationInfo
from abc import abstractmethod

from ...utils.types.source_types import SourceType, SourceCheckerType
from ...utils.custom_exceptions import InvalidSourceChecker
from ...utils.types.identifier import StrObjectId
from .helpers import SourceHelpers
from ....services.model_services import UpdateableMixin

class SourceBase(UpdateableMixin,BaseModel):
    id: StrObjectId = Field(default_factory=lambda: str(ObjectId()), alias="_id", frozen=True)
    name: str
    agent_email: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default="")
    deleted_at: Optional[datetime] = Field(default=None)
    tags: List[StrObjectId] = Field(default_factory=list)
    products: List[StrObjectId] = Field(default_factory=list)
    flow: List[StrObjectId] = Field(default_factory=list)
    trackeable: bool = Field(default=True)
    category: str = Field(default="")
    source_checker: SourceCheckerType
    created_at: Optional[datetime] = Field(default=None, frozen=True)
    updated_at: Optional[datetime] = Field(default_factory=lambda: datetime.now(ZoneInfo("UTC")))
    
    def model_dump(self, *args, **kwargs) -> Dict:
        kwargs["by_alias"] = True
        data = super().model_dump(*args, **kwargs)
        data["type"] = self.type
        return data


    @model_validator(mode='before')
    @classmethod
    def set_timestamps(cls, data: Dict) -> Dict:
        """Handle timestamps before model creation"""
        has_id = bool(data.get('id') or data.get('_id'))
        
        if has_id and 'created_at' not in data:
            raise ValueError("created_at is required when id is provided")
            
        if 'created_at' not in data:
            data['created_at'] = datetime.now(ZoneInfo("UTC"))
            
        return data
    
    @field_validator('created_at', 'updated_at', mode="after")
    @classmethod
    def ensure_utc(cls, v: datetime) -> datetime:
        return v.replace(tzinfo=ZoneInfo("UTC")) if v.tzinfo is None else v.astimezone(ZoneInfo("UTC"))
    
    
    @field_validator('source_checker', mode="before")
    @classmethod
    def lowercase_source_checker(cls, v: str) -> str:
        return v.lower()
    
    @model_validator(mode='after')
    def validate_source(self):
        if not SourceHelpers.is_valid_source_checker(source_type=self.type,source_checker=self.source_checker):
            raise InvalidSourceChecker(f"Source checker {self.source_checker} not valid for source type {self.type} | Allowed ones are {SourceHelpers.get_source_checkers(self.type)}")
        if self.category == "":
            self.category = self.type
        return self
    
    @property
    @abstractmethod
    def type(self) -> SourceType:
        pass
    