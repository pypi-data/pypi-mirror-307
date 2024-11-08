from . import TimestampValidationMixin, UpdateableMixin
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from bson import ObjectId
from ...models.utils.types import StrObjectId

class ChattyAssetModel(TimestampValidationMixin, UpdateableMixin, BaseModel):
    id: StrObjectId = Field(alias="_id", default_factory=lambda: str(ObjectId()), frozen=True)
    name: str