from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.core.settings import get_settings
from src.core.tasks.broker import start_broker, stop_broker
from src.core.utils.create_folder import create_folder

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI) -> None:
    await start_broker()
    await create_folder(settings.TEMP_MEDIA_FOLDER)
    yield
    await stop_broker()
