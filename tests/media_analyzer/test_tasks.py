import uuid

import aiofiles
from sqlalchemy import text

from src.media_analyze.schemas.process_result import ProcessResultWithId
from src.media_analyze.tasks import process_video, process_image


class TestAnalyzeTasks:
    async def copy_file(self, source_path):
        async with aiofiles.open(source_path, mode='rb') as source_file:
            dest_path = f"{source_path}{str(uuid.uuid4())}.{source_file.name.split(".")[-1]}"
            async with aiofiles.open(dest_path, mode='wb') as dest_file:
                async for chunk in source_file:
                    await dest_file.write(chunk)
        return dest_path

    async def test_video_analyze_task(self, get_db_session) -> None:
        path_to_test_media = "tests/media_analyzer/test_media/test_video.mp4"
        task = await process_video.kiq(
            video_path=await self.copy_file(path_to_test_media)
        )
        await task.wait_result()
        result = await get_db_session.execute(
            text("select * from processed_data where result_id = :result_id").bindparams(result_id=task.task_id)
        )
        mapped_result = result.mappings().first()
        assert ProcessResultWithId(**mapped_result)

    async def test_image_analyze_task(self, get_db_session) -> None:
        path_to_test_media = "tests/media_analyzer/test_media/test_pic.webp"
        task = await process_image.kiq(
            image_path=await self.copy_file(path_to_test_media)
        )
        await task.wait_result()
        result = await get_db_session.execute(
            text("select * from processed_data where result_id = :result_id").bindparams(result_id=task.task_id)
        )
        mapped_result = result.mappings().first()
        assert ProcessResultWithId(**mapped_result)
