import sys
from functools import cache

from taskiq import InMemoryBroker, AsyncBroker
from taskiq_redis import PubSubBroker, RedisAsyncResultBackend

from src.core.settings import get_settings

settings = get_settings()


@cache
def get_result_backend() -> RedisAsyncResultBackend:
    return RedisAsyncResultBackend(
        redis_url=settings.REDIS_DSN
    )


@cache
def get_broker(
) -> AsyncBroker:
    if "pytest" in sys.modules:
        return InMemoryBroker()
    return PubSubBroker(
        url=settings.REDIS_DSN
    ).with_result_backend(result_backend=get_result_backend())


async def start_broker() -> None:
    await get_broker().startup()


async def stop_broker() -> None:
    await get_broker().shutdown()


broker = get_broker()
