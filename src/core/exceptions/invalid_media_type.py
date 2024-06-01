from src.core.exceptions.base import BaseException_


class InvalidMediaType(BaseException_):
    def __init__(self, *args) -> None:
        super().__init__(
            *args,
            message="Invalid media type for field 'file'. Available types 'video, image'.",
        )
