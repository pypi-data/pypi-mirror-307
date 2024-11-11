from . import TimestampValidationMixin, UpdateableMixin
from pydantic import BaseModel, Field
from typing import Any, ClassVar
from bson import ObjectId
from ...models.utils.types import StrObjectId
from ...models.utils.types.serializer_type import SerializerType

class ChattyAssetModel(TimestampValidationMixin, UpdateableMixin, BaseModel):
    id: StrObjectId = Field(alias="_id", default_factory=lambda: str(ObjectId()), frozen=True)
    name: str
    exclude_fields: ClassVar[dict[SerializerType, set[str]]] = {}


    def model_dump(
        self, 
        *args, 
        serializer: SerializerType = SerializerType.DATABASE, 
        **kwargs
    ) -> dict[str, Any]:
        # Get fields to exclude for this serializer type
        exclude = self.exclude_fields.get(serializer, set())
        
        # Add exclude to kwargs if not present, or update existing exclude
        if 'exclude' in kwargs:
            if isinstance(kwargs['exclude'], set):
                kwargs['exclude'].update(exclude)
            else:
                kwargs['exclude'] = exclude
        else:
            kwargs['exclude'] = exclude

        data = super().model_dump(*args, **kwargs)
        return data

    def model_dump_json(
        self, 
        *args,
        serializer: SerializerType = SerializerType.API,  # Default to API for JSON
        **kwargs
    ) -> str:
        # Just add serializer to kwargs and let parent handle the JSON conversion
        return super().model_dump_json(*args, exclude=self.exclude_fields.get(serializer, set()), **kwargs)
