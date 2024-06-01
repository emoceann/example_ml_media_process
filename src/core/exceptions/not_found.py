from src.core.exceptions.base import BaseException_


class NotFound(BaseException_):
    def __init__(self, *args) -> None:
        super().__init__(
            message="Not found record",
            *args
        )
