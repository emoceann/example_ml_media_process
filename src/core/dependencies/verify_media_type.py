from fastapi import UploadFile

from src.core.constants.allowed_media_types import ALLOWED_MEDIA_TYPES
from src.core.exceptions.invalid_media_type import InvalidMediaType


async def check_media_content_type(
        file: UploadFile
) -> None:
    media_type, _ = file.content_type.split("/")
    if media_type not in ALLOWED_MEDIA_TYPES:
        raise InvalidMediaType
