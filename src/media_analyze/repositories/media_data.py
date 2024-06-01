from fastapi import Depends
from sqlalchemy import text, null, table, column
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database.config import get_session
from src.core.exceptions.not_found import NotFound
from src.media_analyze.repositories.base import AbstractMediaDataRepo
from src.media_analyze.schemas.process_result import ProcessResultWithId
from src.media_analyze.serializers.processed_media_serializer import MediaSerializer


class MediaDataRepo(AbstractMediaDataRepo):
    def __init__(
            self,
            session: AsyncSession = Depends(get_session),
            serializer: MediaSerializer = Depends()
    ):
        self.session = session
        self.serializer = serializer

    async def get_by_request_id(self, result_id: str) -> ProcessResultWithId:
        stmt = text(
            "select * from processed_data where result_id = :result_id"
        ).bindparams(
            result_id=result_id
        )
        res = await self.session.execute(stmt)
        mapped_res = res.mappings().first()
        if not mapped_res:
            raise NotFound
        return self.serializer.serialize(mapped_res)

    async def delete_by_request_id(self, result_id: str) -> None:
        stmt = text("delete from processed_data where result_id = :result_id").bindparams(result_id=result_id)
        await self.session.execute(stmt)
        await self.session.commit()

    async def create_result_record(self, result: ProcessResultWithId) -> None:
        stmt = table(
            "processed_data",
            column("result_id"),
            column("data", JSONB(none_as_null=True))
        ).insert().values(
            data=result.data.model_dump_json() if result.data else null(),
            result_id=result.result_id
        )
        await self.session.execute(stmt)
        await self.session.commit()
