from aiofiles import os as asyncos


async def create_folder(path: str) -> None:
    if await asyncos.path.exists(path):
        return
    await asyncos.mkdir(path=path)
