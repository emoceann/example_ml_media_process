from fastapi import FastAPI

from src.core.exception_handlers.invalid_media import media_type_is_not_valid
from src.core.exception_handlers.not_found import not_found
from src.core.exception_handlers.result_is_not_ready import result_is_not_ready_yet
from src.core.exceptions import InvalidMediaType, ResultIsNotReady, NotFound
from src.media_analyze.routes import router as media_process_router
from src.server.lifespan import lifespan


def get_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan)
    app.include_router(router=media_process_router, prefix="/media")
    app.exception_handler(InvalidMediaType)(media_type_is_not_valid)
    app.exception_handler(ResultIsNotReady)(result_is_not_ready_yet)
    app.exception_handler(NotFound)(not_found)
    return app
