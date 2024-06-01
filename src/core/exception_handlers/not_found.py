from fastapi import Request, status
from fastapi.responses import ORJSONResponse

from src.core.exceptions.not_found import NotFound


async def not_found(request: Request, exc: NotFound):
    return ORJSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            "code": status.HTTP_404_NOT_FOUND, "error": exc.message
        }
    )
