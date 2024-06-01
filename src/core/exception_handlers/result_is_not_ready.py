from fastapi import Request, status
from fastapi.responses import ORJSONResponse

from src.core.exceptions import ResultIsNotReady


async def result_is_not_ready_yet(request: Request, exc: ResultIsNotReady):
    return ORJSONResponse(
        status_code=status.HTTP_202_ACCEPTED,
        content={
            "code": status.HTTP_202_ACCEPTED, "error": exc.message
        }
    )
