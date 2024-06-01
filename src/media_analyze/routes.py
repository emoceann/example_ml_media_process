from fastapi import APIRouter, UploadFile, Depends, status

from src.core.dependencies.verify_media_type import check_media_content_type
from src.media_analyze.controller import MediaProcessController
from src.media_analyze.schemas.process_result import ProcessResultWithId

router = APIRouter()


@router.get(
    "/analysis/{result_id}",
    response_model=ProcessResultWithId
)
async def get_media_analyze(
        result_id: str,
        controller: MediaProcessController = Depends()
):
    return await controller.get_result(result_id=result_id)


@router.delete(
    "/analysis/delete/{result_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_media_analyze_result(
        result_id: str,
        controller: MediaProcessController = Depends()
):
    return await controller.delete_result(result_id=result_id)


@router.post(
    "/analysis",
    dependencies=[Depends(check_media_content_type)]
)
async def analyze_media(
        file: UploadFile,
        controller: MediaProcessController = Depends()
) -> str:
    return await controller.media_process(file)
