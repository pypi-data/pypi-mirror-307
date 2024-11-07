from __future__ import annotations
from datetime import datetime
from typing import List, Optional, Dict, Any, TYPE_CHECKING

from .meta_base_notification_json import BaseMetaNotificationJson
from .schema.content_messages import MetaTextContent, MetaImageContent, MetaStickerContent, MetaAudioContent, MetaVideoContent, MetaDocumentContent, MetaContactContent, MetaLocationContent, MetaSystemContent
from ...utils.types.message_types import MessageType

if TYPE_CHECKING:
    from .schema.values.value_messages import Message, MetaContext
    from .meta_base_notification_json import Contact
class MetaMessageJson(BaseMetaNotificationJson):
    pass

    @property
    def message(self) -> Message:
        return self.get_value().messages[0]

    def get_wa_id(self) -> str:
        return self.message.id

    def get_created_at(self) -> datetime:
        return self.message.timestamp

    def get_referral(self) -> Optional[Dict[str, Any]]:
        return self.message.referral

    def get_type(self) -> MessageType:
        if self.message.errors is not None:
            self.message.type = MessageType.ERROR
        return self.message.type
    
    def get_message_content(self) -> MetaTextContent | MetaImageContent | MetaStickerContent | MetaAudioContent | MetaVideoContent | MetaDocumentContent | MetaContactContent | MetaSystemContent | MetaLocationContent:
        return self.message.get_content()

    def get_message_content_dict(self) -> dict:
        content = self.get_message_content()
        if content is None:
            return {}  # Retorna un diccionario vacío si el contenido es None
        return dict(content)

    def get_client(self) -> Contact:
        return self.get_value().contacts[0]

    def get_client_wa_id(self) -> str:
        return self.get_client().get_wa_id()

    def get_context(self) -> MetaContext:
        return self.message.context