import uuid

from tests.media_analyzer.mock_data.analyze_data import dumped_analyze_data
from src.media_analyze.repositories.base import AbstractMediaDataRepo
from src.media_analyze.schemas.process_result import ProcessResultWithId


class MockMediaDataRepo(AbstractMediaDataRepo):
    async def create_result_record(self, result: ProcessResultWithId) -> None:
        return None

    async def get_by_request_id(self, request_id: str) -> ProcessResultWithId:
        return ProcessResultWithId(
            result_id=uuid.uuid4().hex,
            data=dumped_analyze_data
        )