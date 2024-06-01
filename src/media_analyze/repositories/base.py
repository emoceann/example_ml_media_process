from abc import ABC, abstractmethod

from src.media_analyze.schemas.process_result import ProcessResultWithId


class AbstractMediaDataRepo(ABC):
    @abstractmethod
    async def get_by_request_id(self, request_id: str) -> ProcessResultWithId:
        raise NotImplementedError

    @abstractmethod
    async def delete_by_request_id(self, request_id: str) -> None:
        raise NotImplementedError

    @abstractmethod
    async def create_result_record(self, result: ProcessResultWithId) -> None:
        raise NotImplementedError
