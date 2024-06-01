from fastapi import Request, status
from fastapi.responses import ORJSONResponse

from src.core.exceptions import InvalidMediaType


async def media_type_is_not_valid(request: Request, exc: InvalidMediaType):
    return ORJSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "code": status.HTTP_422_UNPROCESSABLE_ENTITY, "error": exc.message
        }
    )
