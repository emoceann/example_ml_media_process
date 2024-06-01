from src.core.exceptions.base import BaseException_


class ResultIsNotReady(BaseException_):
    def __init__(self, result_id: str, *args) -> None:
        super().__init__(
            message=f"result is not ready for '{result_id}'",
            *args
        )
