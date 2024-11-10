'''
[2024-11-9] [Note] User messages can be lists of multiple messages at once; 
    whereas system messages must be only single strings
'''

import os

from base64 import b64encode
from typing import Union, Optional

from .types import (
    UserMessage,
    ImageDetails,
    SystemMessage,
    UserTextMessage,
    UserImageMessage,
)

def system(message: str) -> SystemMessage:
    return {"role": "system", "content": message}


def user(
    message: Union[str, UserTextMessage, UserImageMessage]
) -> Optional[UserMessage]:
    if not message: return None
    return {"role": "user", "content": [message]}


def _encode_image(image_path: str) -> str:
    with open(image_path, "rb") as f:
        return b64encode(f.read()).decode()


def image(
    image_path: str, 
    detail: str = ImageDetails.AUTO.value,
) -> UserImageMessage:
    if detail not in ImageDetails:
            return None

    if not image_path.startswith("https"):
        image_enc = _encode_image(image_path)
        ext = os.path.splitext(image_path)[1][1:]
        url = f"data:image/{ext};base64,{image_enc}"
    else:
        url = image_path

    
    return {
        "type": "image_url",
        "image_url": {"url": url, "detail": detail}
    }