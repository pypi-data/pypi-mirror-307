from pydantic import BaseModel, Field

class ChattyContentSticker(BaseModel):
    url: str = Field(description="URL of the media from S3")
    mime_type: str
    sha256: str