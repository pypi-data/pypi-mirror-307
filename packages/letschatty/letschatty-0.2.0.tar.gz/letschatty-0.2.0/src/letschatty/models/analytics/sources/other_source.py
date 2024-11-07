from __future__ import annotations
from typing import List, Optional, Any
from pydantic import Field, ConfigDict, model_validator

from .source_base import SourceBase
from ...utils.types.source_types import SourceType, SourceCheckerType
from ...utils.types.serializer_type import SerializerType
from ...utils.types.identifier import StrObjectId

class OtherSource(SourceBase):
    topic_id: Optional[StrObjectId] = None
    trigger: Optional[str] = Field(default="")
    threshold: float = Field(default=0)
    embedding: List[float] = Field(default_factory=list)
    model_config = ConfigDict(extra='ignore')

    @property
    def type(self) -> SourceType:
        return SourceType.OTHER_SOURCE
    
    @model_validator(mode='after')
    def validate_other_source(self):
        match self.source_checker:
            case SourceCheckerType.SIMILARITY:
                if not self.trigger:
                    raise ValueError("Trigger must be provided for Similarity")
                if self.threshold == 0:
                    self.threshold = 0.96
            case SourceCheckerType.LITERAL:
                if not self.trigger:
                    raise ValueError("Trigger must be provided for Literal")
            case SourceCheckerType.SMART_MESSAGES:
                if not self.topic_id:
                    raise ValueError("Topic id must be provided for Smart Messages")
        return self
    
    def __eq__(self, other: OtherSource) -> bool:
        if not isinstance(other, OtherSource):
            return False
        return bool(self.trigger and other.trigger and self.trigger == other.trigger)
    
    def __hash__(self) -> int:
        return hash(self.trigger)

    def model_dump(
        self, 
        *args, 
        serializer: SerializerType = SerializerType.DATABASE, 
        **kwargs
    ) -> dict[str, Any]:
        """Dumps the model according to the specified serializer type
        
        Args:
            serializer: The type of serialization to perform
            *args: Additional positional arguments for model_dump
            **kwargs: Additional keyword arguments for model_dump
            
        Returns:
            A dictionary representation of the model
        """
        data = super().model_dump(*args, **kwargs)
        
        match serializer:
            case SerializerType.FRONTEND:
                data.pop('embedding')
                data.pop('threshold')
            case SerializerType.DATABASE:
                pass
                
        return data
