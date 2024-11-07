# pylint: disable=import-outside-toplevel
import asyncio
import logging
import os

LOGGER = logging.getLogger(__name__)


async def download_file(url: str, destination_path: str) -> bool:
    import aiofiles  # type: ignore
    import aiohttp

    async with aiohttp.ClientSession(
        timeout=aiohttp.ClientTimeout(total=3600)
    ) as session:
        async with session.get(url) as response:
            if response.status == 200:
                async with aiofiles.open(destination_path, "wb") as file:
                    while True:
                        try:
                            chunk = await response.content.read(1024)
                        except asyncio.TimeoutError:
                            LOGGER.warning("Read timeout")
                            return False
                        if not chunk:
                            break
                        await file.write(chunk)
                return os.path.exists(destination_path)

    return False
