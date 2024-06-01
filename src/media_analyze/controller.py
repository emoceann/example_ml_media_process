import uuid

import aiofiles
from fastapi import UploadFile, Depends

from src.core.settings import get_settings, Settings
from src.media_analyze.repositories.media_data import MediaDataRepo
from src.media_analyze.schemas.process_result import ProcessResultWithId
from src.media_analyze.tasks import process_video, process_image


class MediaProcessController:
    def __init__(
            self,
            repo: MediaDataRepo = Depends(),
            settings: Settings = Depends(get_settings)
    ):
        self.repo = repo
        self.settings = settings

    async def media_process(
            self, media: UploadFile
    ) -> str:
        file_type, file_format = media.content_type.split("/")
        file_path = f"{self.settings.TEMP_MEDIA_FOLDER}/{uuid.uuid4()}.{file_format}"
        async with aiofiles.open(file_path, "wb") as file:
            await file.write(await media.read())
            await file.flush()
        if file_type == "video":
            task = await process_video.kiq(file_path)
        else:
            task = await process_image.kiq(file_path)
        return task.task_id

    async def get_result(self, result_id: str) -> ProcessResultWithId:
        return await self.repo.get_by_request_id(result_id=result_id)

    async def delete_result(self, result_id: str) -> None:
        return await self.repo.delete_by_request_id(result_id=result_id)
