import asyncio
import uuid

import pytest
import aiofiles
from sqlalchemy import text, table, column
from sqlalchemy.dialects.postgresql import JSONB

from src.media_analyze.schemas.process_result import ProcessResultWithId
from tests.media_analyzer.mock_data.analyze_data import dumped_analyze_data


class TestAnalyzeEndpoints:
    @pytest.mark.parametrize(
        "path",
        [
            "tests/media_analyzer/test_media/test_video.mp4",
            "tests/media_analyzer/test_media/test_pic.webp",
        ]
    )
    async def test_analyze_media_video(self, client, path) -> None:
        async with aiofiles.open(path, "rb") as file:
            resp = await client.post(
                "/media/analysis",
                files={"file": (file.name, await file.read())}
            )
        res = resp.json()
        assert isinstance(res, str)

    async def test_get_analyzed_data(self, client, get_db_session) -> None:
        result_id = uuid.uuid4().hex
        schema_data = ProcessResultWithId(result_id=result_id, data=dumped_analyze_data)
        stmt = table(
            "processed_data",
            column("result_id"),
            column("data", JSONB(none_as_null=True))
        ).insert().values(
            data=schema_data.data.model_dump_json(),
            result_id=schema_data.result_id
        )
        await get_db_session.execute(stmt)
        await get_db_session.commit()
        resp = await client.get(
            f"/media/analysis/{result_id}"
        )
        resp = ProcessResultWithId(**resp.json())
        assert resp.data == schema_data.data

    async def test_delete_analyzed_data(self, client, get_db_session) -> None:
        result_id = uuid.uuid4().hex
        schema_data = ProcessResultWithId(result_id=result_id, data=dumped_analyze_data)
        stmt = table(
            "processed_data",
            column("result_id"),
            column("data", JSONB(none_as_null=True))
        ).insert().values(
            data=schema_data.data.model_dump_json(),
            result_id=schema_data.result_id
        )
        await get_db_session.execute(stmt)
        await get_db_session.commit()
        resp = await client.delete(
            f"/media/analysis/delete/{result_id}"
        )
        assert resp.status_code == 204
        result = await get_db_session.execute(
            text("select * from processed_data where result_id = :result_id").bindparams(result_id=result_id)
        )
        assert result.mappings().first() is None
