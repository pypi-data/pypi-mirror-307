from enum import Enum
from typing import Union
from pydantic import BaseModel

class UserTextMessage(BaseModel):
    type: str = "text"
    text: str

class UserImageMessage(BaseModel):
    type: str = "image_url"
    image_url: dict[str, str]

class UserMessage(BaseModel):
    role: str = "user"
    content: list[Union[UserTextMessage, UserImageMessage]]

class SystemMessage(BaseModel):
    role: str = "system"
    content: str

class Messages(BaseModel):
    role: str
    content: list[Union[SystemMessage, UserMessage]]

class ImageDetails(str, Enum):
    AUTO: str = "auto"
    LOW: str = "low"
    HIGH: str = "high"
